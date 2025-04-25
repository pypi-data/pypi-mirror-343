"""
Created on Fri November 17 22:00:00 2023

@author: Anna Grim
@email: anna.grim@alleninstitute.org


This module implements a supervoxel-based topological loss function designed
for training neural networks to perform instance segmentation. The loss
function penalizes voxel- and structure-level mistakes by focusing on
"critical" regions in the prediction.

The core idea is to calculate the loss based on two key components:
    1. Voxel-Level Mistakes
        These occur when the predicted segmentation differs from the ground
        truth at the voxel-level.

    2. Structure-Level Mistakes
        These occur when the structure of the predicted segmentation differs
        from the ground truth, such as over- or under-segmenting individual
        objects or incorrectly merging objects.

The module supports both 2D and 3D segmentation tasks by subclassing the main
"SuperVoxel" class.

"""

from concurrent.futures import ProcessPoolExecutor, as_completed
from scipy.ndimage import label
from torch.autograd import Variable

import numpy as np
import torch
import torch.nn as nn

from nnunet_extend.training.loss.SuperVoxelLoss.critical_detection_2d import detect_critical_2d
from nnunet_extend.training.loss.SuperVoxelLoss.critical_detection_3d import detect_critical_3d
from nnunetv2.training.loss.robust_ce_loss import RobustCrossEntropyLoss
import os



class SuperVoxelLoss(nn.Module):
    """
    Supervoxel-based loss function for training neural networks to perform
    instance segmentation. This class implements a topology-aware loss
    function that penalizes both voxel- and structure-level mistakes.

    """

    def __init__(
        self,
        apply_nonlin=None,
        alpha=0.5,
        beta=0.5,
        criterion=RobustCrossEntropyLoss(reduction="none"),
        device="cuda",
        return_mask=False,
        threshold=0.0,
    ):
        """
        Instantiates SuperVoxelLoss object with the given parameters.

        Parameters
        ----------
        alpha : float, optional
            Scaling factor between 0 and 1 that determines the relative
            importance of voxel- versus structure-level mistakes. The default
            is 0.5.
        beta : float, optional
            Scaling factor between 0 and 1 that determines the relative
            importance of split versus merge mistakes. The default is 0.5.
        criterion : torch.nn.modules.loss, optional
            Loss function used to penalize voxel- and structure-level
            mistakes. If provided, must set "reduction=None". The default is
            nn.BCEWithLogitsLoss.
        device : str, optional
            Device on which to train model. The default is "cuda".
        return_mask, bool, optional
            Indication of whether to return loss as an image mask. The default
            is False.
        threshold : float, optional
            Theshold used to binarize predictions. The default is 0.0.

        Returns
        -------
        None

        """
        # Call parent class
        super(SuperVoxelLoss, self).__init__()

        # Instance attributes
        self.apply_nonlin = apply_nonlin
        self.alpha = alpha
        self.beta = beta
        self.criterion = criterion
        self.device = device
        self.return_mask = return_mask
        self.threshold = threshold

    def forward(self, preds, targets):
        """
        Computes the loss for a batch by comparing predictions and ground
        truth.

        Parameters
        ----------
        preds : torch.Tensor
            Predictions with the shape (batch_size, 1, height, width, *depth).
            This tensor should contain raw output probabilities (logits) from
            the model.
        targets : torch.Tensor
            Ground truth segmentations with the shape (batch_size, 1, height,
            width, *depth).

        Returns
        -------
        torch.Tensor
            Scalar tensor representing the mean of the loss values across the
            batch.

        """
        # Initializations
        loss = self.criterion(preds, targets)
        if self.apply_nonlin is not None:
            preds = self.apply_nonlin(preds)
        targets = np.array(targets[:, 0, ...].cpu().detach())
        preds = np.array(preds[:, 1, ...].cpu().detach())
        critical_masks = self.get_critical_masks_for_batch(preds, targets)

        for i in range(preds.shape[0]):
            structure_loss = critical_masks[i, ...] * loss[i, ...]
            loss[i, ...] = (1 - self.alpha) * loss[i, ...] + self.alpha * structure_loss
        return loss if self.return_mask else loss.mean()

    def get_critical_masks_for_batch(self, preds, targets):
        """
        Computes critical components for each example in the given batch.

        Parameters
        ----------
        preds : torch.Tensor
            Predictions with the shape (batch_size, 1, height, width, *depth).
            This tensor should contain raw output probabilities (logits) from
            the model.
        targets : torch.Tensor
            Ground truth segmentations with the shape (batch_size, 1, height,
            width, *depth).

        Returns
        -------
        torch.Tensor
            Binary masks that identify critical components.

        """
        with ProcessPoolExecutor(max_workers=2) as executor:
            # Assign processes
            processes = []
            for i in range(preds.shape[0]):
                pred, _ = label(preds[i, ...] > self.threshold)
                target, _ = label(targets[i, ...])
                processes.append(
                    executor.submit(
                        self.get_critical_mask, pred, target, i, -1
                    )
                )
                processes.append(
                    executor.submit(self.get_critical_mask, target, pred, i, 1)
                )

            # Store results
            critical_masks = np.zeros(preds.shape)
            for process in as_completed(processes):
                i, mask_i = process.result()
                critical_masks[i, ...] += mask_i
        return self.toGPU(critical_masks)


    def get_critical_mask(self, pred, target, process_id, critical_type):
        """
        Computes the critical mask for the given example.

        Parameters
        ----------
        pred : numpy.ndarray
            Predicted segmentation.
        target : numpy.ndarray
            Ground truth segmentation.
        process_id : int
            Index of the given example from a batch.
        critical_type : int
            Indication of whether to compute positive or negative critical
            components.

        Returns
        -------
        tuple
            A tuple containing the following:
            - "process_id" : Index of the given example from a batch.
            - "mask" : Binary mask that identifies the critical components.

        """
        binarized_pred = (pred > self.threshold).astype(np.float32)
        critical_mask = self.detect_critical(target, binarized_pred)
        scaling_factor = (1 - self.beta) if critical_type > 0 else self.beta
        return process_id, scaling_factor * critical_mask

    def toGPU(self, arr):
        """
        Converts the given array to a tensor and moves it to a GPU device.

        Parameters
        ----------
        arr : numpy.ndarray
            Array to be converted to a tensor and moved to GPU.

        Returns
        -------
        torch.tensor
            Tensor on GPU.

        """
        arr[np.newaxis, ...] = arr
        arr = torch.from_numpy(arr)
        return Variable(arr).to(self.device, dtype=torch.float32)


# --- Subclasses ---
class SuperVoxelLoss2D(SuperVoxelLoss):
    """
    Subclass of SuperVoxelLoss designed for 2D segmentation tasks with
    additional functionality for computing and handling critical components
    in 2D images.

    """

    def __init__(
        self,
        apply_nonlin=None,
        alpha=0.5,
        beta=0.5,
        criterion=RobustCrossEntropyLoss(reduction="none"),
        device="cuda",
        return_mask=False,
        threshold=0.0,
    ):
        """
        Instantiates SuperVoxelLoss2D object with the given parameters.

        Parameters
        ----------
        alpha : float, optional
            Scaling factor between 0 and 1 that determines the relative
            importance of voxel- versus structure-level mistakes. The default
            is 0.5.
        beta : float, optional
            Scaling factor between 0 and 1 that determines the relative
            importance of split versus merge mistakes. The default is 0.5.
        criterion : torch.nn.modules.loss, optional
            Loss function used to penalize voxel- and structure-level
            mistakes. If provided, must set "reduction=None". The default is
            nn.BCEWithLogitsLoss.
        device : str, optional
            Device on which to train model. The default is "cuda".
        return_mask, bool, optional
            Indication of whether to return loss as an image mask. The default
            is False.
        threshold : float, optional
            Theshold used to binarize predictions. The default is 0.5.

        Returns
        -------
        None

        """
        # Call parent class
        super(SuperVoxelLoss2D, self).__init__(
            apply_nonlin, alpha, beta, criterion, device, return_mask, threshold
        )

        # Instance attributes
        self.detect_critical = detect_critical_2d


class SuperVoxelLoss3D(SuperVoxelLoss):
    """
    Subclass of SuperVoxelLoss designed for 3D segmentation tasks with
    additional functionality for computing and handling critical components
    in 3D images.

    """

    def __init__(
        self,
        apply_nonlin=None,
        alpha=0.5,
        beta=0.5,
        criterion=RobustCrossEntropyLoss(reduction="none"),
        device="cuda",
        return_mask=False,
        threshold=0.0,
    ):
        """
        Instantiates SuperVoxelLoss3D object with the given parameters.

        Parameters
        ----------
        alpha : float, optional
            Scaling factor between 0 and 1 that determines the relative
            importance of voxel- versus structure-level mistakes. The default
            is 0.5.
        beta : float, optional
            Scaling factor between 0 and 1 that determines the relative
            importance of split versus merge mistakes. The default is 0.5.
        criterion : torch.nn.modules.loss, optional
            Loss function used to penalize voxel- and structure-level
            mistakes. If provided, must set "reduction=None". The default is
            nn.BCEWithLogitsLoss.
        device : str, optional
            Device on which to train model. The default is "cuda".
        return_mask, bool, optional
            Indication of whether to return loss as an image mask. The default
            is False.
        threshold : float, optional
            Theshold used to binarize predictions. The default is 0.5.

        Returns
        -------
        None

        """
        # Call parent class
        super(SuperVoxelLoss3D, self).__init__(
            apply_nonlin, alpha, beta, criterion, device, return_mask, threshold
        )

        # Instance attributes
        self.detect_critical = detect_critical_3d


if __name__ == '__main__':
    from nnunetv2.utilities.helpers import softmax_helper_dim1
    pred = torch.rand((2, 2, 64, 64, 64)).cuda()
    ref = torch.randint(0, 2, (2, 1, 64, 64, 64)).cuda()

    # loss = DC_and_DropCE_loss({'batch_dice': False, 'smooth': 1e-5, 'do_bg': False, 'ddp': False},
    #                             {'apply_nonlin':softmax_helper_dim1, 'alpha': 0.4, 'smooth': 1e-6},
    #                             weight_ce=1, weight_dice=1, ignore_label=None, dice_class=MemoryEfficientSoftDiceLoss)
    
    # loss1 = DC_and_CE_loss({'batch_dice': False, 'smooth': 1e-5, 'do_bg': False, 'ddp': False},
    #                             {},
    #                             weight_ce=1, weight_dice=1, ignore_label=None, dice_class=MemoryEfficientSoftDiceLoss)

    loss = SuperVoxelLoss3D(
        apply_nonlin=softmax_helper_dim1
    )


    print('loss', loss(pred, ref))
    # print('loss1', loss1(pred, ref))
    
    # print(loss.ce(pred, ref))
    # print(loss.dc(pred, ref))

    # print(loss1.ce(pred, ref))
    # print(loss1.dc(pred, ref))