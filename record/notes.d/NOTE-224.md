---
number: 224
status: Read
formerly:
- NOTE-tmpbrbwv
paper: LIT-475
title: 'Dropout Reduces Underfitting'
version: 1
date: '2026-09-21'
summary: >-
  Reading it: the persuasive number is the training loss, not the accuracy.
  Early dropout lowers ViT-T's training loss from 3.443 to 3.394 while
  standard dropout raises it to 3.885 — so the same operator is doing two
  opposite things depending only on when it runs, and one of them is not
  regularization.
---

# NOTE-224: Dropout Reduces Underfitting

## Contribution

Dropout as an optimization intervention rather than a regularizer. Before
this, dropout was a device with one job — trade training fit for
generalization — and the question was how much. Here the same device, applied
only at the start, **improves training fit**, which no amount of tuning the
rate can do.

What is true afterwards that was not before: the schedule is a separate axis
from the rate, and the operator's sign depends on it.

## Key insight

The paradox that opens §3 is what makes the rest credible. Dropout produces
**smaller gradient norms** and the model travels **farther** from
initialization. Small steps, more ground covered.

The resolution is that the steps agree with each other. Dropout lowers the
pairwise angular spread of mini-batch gradients, and — the part that matters
— lowers their angle to the *whole-dataset* gradient. A biased estimator with
enough variance reduction beats an unbiased one with none.

That framing is worth keeping separately from the dropout result: the quantity
the authors invent, angle to the full-dataset gradient, is a general way to
ask whether an intervention is helping early optimization, and it is cheap to
measure.

## Assumptions

- **The regime is defined by the outcome.** "Overfitting" means standard
  dropout helps; "underfitting" means it hurts. Honest, circular, and means the
  precondition costs a training run.
- **The whole-dataset gradient is computable** with dropout in inference mode,
  which is what the error metric is measured against.
- **One of dropout or stochastic depth per experiment**, never both.
- **Dropout is off during downstream fine-tuning**, so transfer results measure
  the representation.
- **ConvNeXt recipe** as the basic setting, with a stronger variant that
  doubles epochs and weakens mixup and cutmix.

## Key results

- ViT-T on ImageNet-1K: 73.9 baseline, **67.9** with standard dropout, **74.3**
  with early dropout, 74.4 with early stochastic depth.
- Training loss, same order: 3.443 → 3.885 (standard) → 3.394 (early).
- Swin-F 74.3 → 74.7 / 75.2; Mixer-S 71.0 → 71.3 / 71.7; ConvNeXt-F 76.1 →
  76.3 (s.d. only).
- Improved recipe raises ViT-T's baseline to 76.3 — above the literature
  numbers — and early dropout still adds 0.4.
- Late stochastic depth: ViT-B 81.6 → **82.3**, beating linear-increasing
  (82.1) and curriculum (82.0) schedules at their own best settings; Mixer-B
  78.0 → 78.6.
- Gradient direction error falls early and rises after ~1000 iterations.
  AUC reduction over the first 1500 iterations: AdamW 13.60%, SGD 9.30%,
  momentum SGD 6.67%, Swin-F 17.41%, ConvNeXt-F s.d. 7.62%.
- 3 seeds, average standard deviation **0.142%**.
- Transfer with dropout off: COCO, ADE20K (39.2 → 40.0 mIoU on ViT-T; 44.3 →
  45.7 on ViT-B with late s.d.), and five classification sets.

## Claims

**Strong and well measured:** that early dropout lowers training loss. This is
the claim that cannot be explained as regularization, it is reported for every
model, and it moves in the opposite direction from standard dropout on the
same models.

**Well measured, modest:** the accuracy gains. +0.4 to +0.9 against a 0.142%
standard deviation is real; +0.2 is not, and the paper gives you the number to
work that out.

**Supported and one-model:** the mechanism. The gradient-direction-error
crossing is measured on ViT-T; the AUC reduction is replicated across five
model/optimizer combinations, but the *crossing point* — the thing that would
tell you when to switch — is not.

## Method

Two arms per model on ImageNet-1K, three seeds, with training loss reported
alongside accuracy; a separate measurement study defining and tracking two
gradient-direction statistics; transfer to COCO, ADE20K and five
classification sets with the intervention disabled.

## Concepts

*Early dropout* and *late dropout*; *gradient direction variance* (pairwise
cosine distance among mini-batch gradients); *gradient direction error* (cosine
distance to the whole-dataset gradient); the operational regime test.

## Connections

- [SOTA-240](../practices.d/SOTA-240.md) — apply dropout where the model can memorize, not where it
  cannot. This **confirms** it on the strongest evidence in the record (six
  points of ImageNet accuracy) and then finds the boundary the practice did
  not have: the verdict is about dropout *throughout* training, and the same
  operator on a prefix does the opposite thing.
- [SOTA-008](../practices.d/SOTA-008.md) and [SOTA-009](../practices.d/SOTA-009.md) — learning-rate warmup — are the record's
  other "do something different at the start" practices, and warmup's usual
  rationale is also about early-training instability. Nobody has asked whether
  early dropout and warmup are doing the same job twice; the
  gradient-direction-error metric is exactly the instrument that would answer
  it.
- [THEORY-015](../theory.d/THEORY-015.md) and [THEORY-016](../theory.d/THEORY-016.md) explain dropout as a regularizer — a
  data-dependent penalty, and a geometric-mean ensemble at test time. Neither
  covers this, because neither is about *when* dropout runs.

## Bearing on the record

One practice and one account, plus a boundary on `SOTA-240` that is worth
adding to it: a reader following `SOTA-240` on an underfitting model would
conclude "no dropout", and the correct conclusion is "no dropout after the
first stretch".

## Limitations

**All vision.** ImageNet-1K and vision transfer, 5–86M parameters. The record's
interest is mostly language models, and the underfitting regime here — a small
model on a fixed 1.2M-image set — is not obviously the same object as a large
model under-trained on a large corpus. `ADR-026` says a claim takes its kind
rather than its domain, which is why this is filed; it does not make the
evidence broader than it is.

**The precondition is a run.** You learn your regime by comparing with and
without standard dropout, which is the experiment the practice is supposed to
save you from having to think about.

**The switch point has no theory.** "About 1000 iterations" is where ViT-T's
gradient-direction-error curves cross. The robustness result (1% to 50% of
epochs) is what makes this liveable, and it is an empirical range on the same
family of models.

**Stochastic depth carries much of the result** — often more than dropout
proper — and the two are treated as interchangeable instances of the idea.
That is reasonable and it is not shown.

## Open questions

- Does it hold for language-model pretraining, where the underfitting regime
  is the normal one? This is the obvious test and the paper does not attempt
  it.
- Is early dropout doing the same work as warmup? Both are early-training
  interventions justified by gradient behaviour, and no experiment in the
  record separates them.
- Does the gradient-direction-error crossing predict the right switch point,
  or is the 1%–50% robustness doing the work? If the former, the metric is a
  tool; if the latter, the choice barely matters and the metric is a story.
