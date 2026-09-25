---
status: Proposed
consensus: unreplicated
consensus_note: >-
  One group, one paper, convolutional image classifiers only. The
  architectures its introduction cites (ResNet, ResNeXt, DenseNet) already
  reach their best results with BN and no dropout, and SENet already put its
  only dropout before the classifier. That is adoption of the arrangement,
  not a test of it (DP-005). No second group in this record has run the
  placement comparison. Read as of 2026-09.
promote_when: >-
  An independent group, with the architecture and data held fixed, trains
  the same batch-normalized network with dropout upstream of BN, with
  dropout after the last BN, and with none, and reports error with its
  spread over seeds. Reporting eval-mode accuracy on the training set would
  also show the mismatch directly. A model that simply ships dropout before
  its classifier would not count, and neither would a result on a
  LayerNorm network, where the mechanism does not exist.
title: 'In a batch-normalized network, put dropout after the last batch-norm layer, not upstream of one'
version: 1
tags:
- model-stability
date: '2026-09-25'
source:
- LIT-tmp68jdl
# No earlier document in or out of the record is known to state the placement
# rule. Ioffe and Szegedy (LIT-002) observed that BN can remove the need for
# dropout, which is a different instruction, and SENet adopted the arrangement
# without stating or measuring it, as this paper itself notes.
introduced_by:
- LIT-tmp68jdl
extends:
- SOTA-240
implementations:
- 'SENet (ILSVRC 2017): its one dropout layer sits before the classifier, per LIT-tmp68jdl §5'
summary: >-
  Li et al. (2018; CVPR 2019), LIT-tmp68jdl. BN freezes a moving variance
  accumulated while dropout was scaling activations. At test time dropout
  stops, the variance changes, and every later BN normalizes by the wrong
  constant. The cost is large: 77.42% → 68.55% on CIFAR-100 for DenseNet with
  dropout 0.5 in each bottleneck. The fix, one dropout layer after the last BN,
  is supported mainly as *avoiding* that cost. What it adds on its own is about
  0.2 top-1 on ImageNet, with no spread reported.
---


# SOTA-tmp0lvqr: In a batch-normalized network, put dropout after the last batch-norm layer, not upstream of one

## Source

Li, Chen, Hu and Yang (2018; CVPR 2019), LIT-tmp68jdl —
ARXIV-1801.05134.

## What to do

1. **Don't put dropout where a BN layer will normalize its output**, either
   directly or through one conv or linear layer. In training, BN's moving
   variance is accumulated while dropout scales activations by `1/p`. At test
   time dropout is the identity, so the variance BN sees is smaller, by a
   factor of `p` in the simplest case, and BN normalizes by a constant that no
   longer applies.
2. **If the network needs dropout at all** (SOTA-240 is the
   test for that), put it after the last BN. In practice that means just
   before the classifier.
3. **If dropout must sit inside BN blocks**, keep the rate low and expect the
   harm to depend on width. With a conv or linear layer between dropout and
   BN, the shift shrinks as the layer's fan-in grows. Wide ResNet (fan-in term
   about 15× that of PreResNet or DenseNet) is the case where bottleneck
   dropout helps. A narrow network copying its placement does not get its
   result.

## Why

The mechanism is derived and then checked. The derivation assumes a linear
regime and i.i.d. inputs. Four architectures on CIFAR-10 and CIFAR-100 then
show three things:

- the measured variance mismatch at each BN grows with the drop rate;
- error grows with it;
- the network misclassifies its own **training** data in eval mode, with every
  weight fixed.

The last point is why this is a train/test mismatch and not over-regularization.
A regularizer that is too strong costs training accuracy in *both* modes.

The other experiment that could have gone the other way is re-estimating BN's
statistics in eval mode, weights frozen. It recovers much of the loss: DenseNet
case (a) goes from 31.45 to 26.98 error on CIFAR-100, and PreResNet from 32.45
to 26.57. So the damage lives in the stored statistics.

## What the evidence does not show

**The size of the gain from relocating dropout.** On ImageNet, dropout 0.2
before the classifier improves ResNet-200, ResNeXt-101 and SENet by 0.21–0.23
top-1 (5 seeds, no spread reported). On CIFAR the changes are mostly under 0.3
points, in both directions depending on network and rate. ResNeXt on CIFAR-100
gets worse at every rate above 0.1. So the instruction rests on the cost it
avoids, not on what dropout-after-BN adds. For a network that is not
overfitting, SOTA-240 still says to leave dropout off.

**Recalibration does not make upstream dropout safe.** Re-estimated statistics
recover much of the loss but not all of it. Recalibrated case-(a) models stay
worse than the no-dropout network: DenseNet 6.82 against 4.72 on CIFAR-10. The
paper's "outperform their baselines" means they beat the same model *before*
recalibration.

**Anything without stored normalization statistics.** LayerNorm and RMSNorm
compute their statistics per example at test time as in training, so the
mismatch this practice avoids does not arise (SOTA-006). This
practice is about BatchNorm, and every result behind it is a convolutional
image classifier.

## Related

This is a special case of SOTA-005's warning that running
statistics are only as good as what they averaged. There the data moved. Here
the network that accumulated the statistics, with dropout active, is not the
one evaluated.

## Known implementations

- SENet's ILSVRC 2017 entry places its single dropout before the classifier.
  The source reports that the SENet paper did not measure it, and supplies
  the measurement.
