---
number: 27
paper: LIT-072
status: Read
formerly:
- NOTE-tmp2fa8m
title: 'Simple Open-Vocabulary Object Detection with Vision Transformers'
version: 1
tags:
- vision-and-graphics
date: '2026-09-09'
summary: >-
  Transfers a contrastively pretrained image-text model to open-vocabulary detection with minimal architectural change. Its transferable finding is about fine-tuning: the text encoder needs a learning rate about 100× lower than the image encoder, freezing it entirely is also wrong, and the recipe that maximises zero-shot transfer is *not* the one that maximises in-distribution performance.
---

# NOTE-027: Simple Open-Vocabulary Object Detection with Vision Transformers

## Contribution

Open-vocabulary detection — detect categories named in text, including ones
never seen in detection training — with a deliberately minimal recipe: take a
contrastively pretrained image-text ViT, attach lightweight detection heads,
fine-tune. Evaluated on **LVIS v1.0 val**, chosen because "this dataset has a
long tail of rare categories and is therefore well-suited to measure
open-vocabulary performance."

## Key insight

**Two encoders fine-tuned at one learning rate is the wrong recipe, and the
right one is asymmetric.** From Table 3:

- Using the same learning rate for image and text encoders is "clearly
  sub-optimal" and causes a large drop in `AP_rare^LVIS`, the zero-shot measure.
- The text encoder needs a rate **about 100× lower**, which the authors suggest
  "may help to prevent catastrophic forgetting of the wide knowledge the model
  acquired during the contrastive pre-training stage."
- **Freezing it completely (learning rate 0) also does not work well.** There is
  an interior optimum, not a corner.

And the part worth the whole reading:

> the optimal recipe for zero-shot transfer does not necessarily maximize
> in-distribution performance

`AP^OI`, the in-distribution measure, moves in the **opposite** direction: the
same-learning-rate setting that destroys zero-shot transfer *improves*
in-distribution accuracy. Two metrics, opposite gradients, one hyperparameter.

## Assumptions

- The pretrained text encoder's knowledge is the thing that carries zero-shot
  transfer, so preserving it is the objective. This is the explanation offered
  for the asymmetry and it is a hypothesis.
- LVIS's rare categories are a fair proxy for open-vocabulary generality.

## Key results

- Open-vocabulary detection from a contrastively pretrained backbone with
  minimal architectural addition.
- **The ~100× learning-rate asymmetry**, with an interior optimum.
- **The zero-shot / in-distribution metric conflict**, measured on the same
  sweep.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A pretrained image-text model transfers to detection with minimal change | strong | the results |
| C2 | The text encoder needs a much lower learning rate than the image encoder | strong | swept, Table 3 |
| C3 | Freezing it entirely is also wrong | strong | the LR=0 point |
| C4 | Preventing catastrophic forgetting is why | **moderate — offered as an explanation** | plausible and not isolated |
| C5 | Zero-shot and in-distribution optima diverge | strong | opposite trends on the same sweep |

## Method

Contrastively pretrain image and text encoders. Add detection heads. Fine-tune
end-to-end with a much lower learning rate on the text side. Evaluate on LVIS
rare categories for zero-shot and on an in-distribution set separately.

## Concepts

- **Per-component learning rates as a knowledge-preservation mechanism** — the
  transferable idea, and a cheaper instrument than freezing or than an explicit
  regulariser.
- **Metric conflict on one hyperparameter** — C5, and the reason a single
  reported number can hide a real decision.

## Connections

C2 is the same instrument as `LIT-079`'s prior-preservation loss and as
KL-to-reference in post-training, at a different price point: instead of adding
a term to the objective, **turn the learning rate down on the part you do not
want to move.** Three ways to say "protect the pretrained behaviour", and the
record carries one of them.

C5 belongs with `LIT-077`'s brittle-metrics finding and `LIT-073`'s DrawBench:
a fourth instance in this pass of the measurement determining the conclusion —
here, two metrics that a single sweep optimises in opposite directions.

## Recommendations

- **R1** — Give each pretrained component its own learning rate when fine-tuning
  a multi-encoder model; a shared rate is a default, not a choice. *Topic:*
  adaptation and tuning. *Strength:* strong.
- **R2** — Look for an interior optimum between "fine-tune freely" and "freeze".
  *Strength:* strong — C3.
- **R3** — Report zero-shot and in-distribution metrics separately when tuning;
  they can have opposite optima. *Topic:* analysis and evaluation.
  *Strength:* strong.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**
Open-vocabulary detection is not a line the anthology tracks.

R1 is the finding with reach. The record's adaptation practices treat a
fine-tune as one operation with one learning rate; this is a clean measurement
that a **component-wise** rate is the actual decision, with a factor of 100
between components and a non-monotone response. Together with `LIT-079`'s prior
preservation it makes a pair: two different ways to keep a pretrained component
from being destroyed, neither of which the record states.

The document's takeaways include **"zero-shot capabilities"**, which is the
third bullet in this batch to use that phrase as a substitute for saying what a
paper does — and here the paper's actual finding is that zero-shot capability is
in *tension* with in-distribution accuracy, which is more interesting than the
bullet.

## Limitations

- Detection, 2022, one dataset family for the open-vocabulary measure.
- C4 is an explanation, not an isolated result.
- The 100× factor is specific to this model pair and is not derived.
- No study of whether the asymmetry generalises to other multi-encoder models.

## Open questions

- Is there a principle setting the ratio? A factor of 100 between two encoders'
  learning rates is the kind of number µP-style reasoning exists to derive, and
  nobody appears to have tried.
