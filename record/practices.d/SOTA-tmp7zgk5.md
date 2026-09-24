---
status: Active
title: 'Train a plain ViT on ImageNet-1k with average pooling, fixed 2D sin-cos positions, a 1024 batch and light augmentation'
version: 1
tags:
- vision-and-graphics
- training-optimization
- analysis-and-evaluation
date: '2026-09-24'
source:
- LIT-tmp5t7v1
introduced_by:
- LIT-tmp5t7v1
consensus: converged
consensus_note: >-
  One group for the ablation, and the paper positions itself against two
  concurrent efforts reaching similar numbers by other routes (DeiT III and
  the ResNet-strikes-back setup), which it cites as evidence the level is
  real rather than that its own recipe is uniquely good. The parts have been
  separately adopted — average pooling and sin-cos positions came from the
  MoCo-v3 ViT study, and this paper takes them rather than inventing them —
  and `big_vision` is the reference implementation the ViT line was developed
  in. `converged` on the *level being reachable*; the specific combination is
  one group's.
implementations:
- big_vision
summary: >-
  Beyer et al. (2022), [LIT-tmp5t7v1](../literature.d/LIT-tmp5t7v1.md) — five changes, none novel, take ViT-S/16
  on ImageNet-1k from **66.8% to 76.5%** at 90 epochs and **80.0%** at 300.
  Global average pooling, fixed 2D sin-cos position embeddings, batch 1024,
  RandAugment at level 10 and Mixup at p = 0.2. **6h30 on a TPUv3-8** for the
  90-epoch run.
---

# SOTA-tmp7zgk5: Train a plain ViT on ImageNet-1k with average pooling, fixed 2D sin-cos positions, a 1024 batch and light augmentation

## Source

Beyer, Zhai and Kolesnikov (2022), [LIT-tmp5t7v1](../literature.d/LIT-tmp5t7v1.md).

## When this applies

You are training a vision transformer on ImageNet-1k or a dataset of that
order, from scratch, and you want a baseline rather than a result — the number
another change will be measured against.

## Do this

Five changes to the original ViT recipe, in descending order of what the
ablation attributes to each at 300 epochs:

| change | worth |
| --- | --- |
| RandAugment (level 10) + Mixup (p = 0.2) | **6.3 points** |
| global average pooling instead of a `[cls]` token | 1.8 |
| batch size 1024 instead of 4096 | 1.4 |
| fixed 2D sin-cos position embeddings instead of learned | 0.4 |
| — linear versus MLP classification head | **nothing** |

Keep the architecture. Inception-style crop at 224², random horizontal flip.

**Do not add the things that look like the next step.** The paper names them:
dropout, stochastic depth, SAM, CutMix, repeated augmentation, blurring,
high-resolution fine-tuning, checkpoint averaging, distillation. None is in
the baseline and it reaches 80%.

## The part worth understanding rather than copying

**Augmentation is not buying accuracy, it is buying the right to train
longer.** Without RandAugment and Mixup the improved recipe goes 73.6 → 73.7
→ 73.7 across 90 / 150 / 300 epochs — flat. With them, 76.5 → 78.5 → 80.0.
The original recipe behaves the same way: 66.8 → 67.2 → 67.1.

So the four structural changes set the level and the augmentation sets whether
the schedule does anything. A practitioner who adopts the structural changes
and skips the augmentation because it "only adds a little" gets a model that
is done at 90 epochs and will conclude that longer training does not help.

## Limitations

- **ViT-S/16 at 224², ImageNet-1k.** The authors recommend ViT-B/32 or
  ViT-B/16 when more compute and data are available, and note that increasing
  patch size is nearly equivalent to reducing resolution — but the ablation
  numbers are for S/16 and are not claimed to transfer.
- **The batch-size result is a batch-size-*reduction* result**, which is the
  opposite of the usual direction and is not explained. 1024 beats 4096 by
  1.4 points at fixed epochs. Whether that is an optimisation effect, an
  interaction with the augmentation, or a learning-rate artefact is untested
  here, and [SOTA-258](SOTA-258.md) and [SOTA-097](SOTA-097.md) both concern batch-size scaling from
  different angles.
- **`converged` refers to the reachable level, not this recipe.** Two
  concurrent efforts reach comparable accuracy by other routes; that is what
  makes 80% credible and what makes "these five changes specifically" one
  group's finding.
