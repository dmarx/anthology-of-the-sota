---
number: 377
status: Active
formerly:
- SOTA-tmptiobf
consensus: unreplicated
consensus_note: >-
  One group, one measurement, and the measurement is the only one of its kind
  — the paper itself notes that existing studies "stop at 64k", so nobody
  else has looked past the ceiling to confirm it. That makes this
  `unreplicated` rather than `emerging`: what is measured is real, what is
  missing is a second group going as far. `DP-005` keeps those apart. The
  adjacent arguments in `THEORY-085` and `LIT-591` are independent of it and
  do not replicate it. Read as of 2026-09.
title: 'Stop scaling the contrastive batch past about 32k, because the benefit saturates there'
version: 1
tags:
- training-optimization
- multimodal-learning
date: '2026-09-23'
source:
- LIT-605
introduced_by:
- LIT-605
implementations: []
---

# SOTA-377: Stop scaling the contrastive batch past about 32k, because the benefit saturates there

## Source

Zhai et al. (2023), [LIT-605](../literature.d/LIT-605.md) — [ARXIV-2303.15343](https://arxiv.org/abs/2303.15343), §4.

## The claim

Contrastive pretraining is widely believed to want the largest batch you can
afford, because the batch is the negative set. There is a ceiling, and it is
lower than the belief implies.

Trained from 512 up to **one million**, image-text contrastive performance
**saturates around 32k** — and it saturates for the **softmax** loss as well
as the sigmoid, so this is a property of the objective family rather than of
either loss.

## Why nobody had seen it

The paper says it plainly: existing studies "stop at 64k". The ceiling sits
just below the point where everyone stopped looking, so every study was run
inside the regime where the belief holds and none was run where it breaks.

That is worth generalising past this result. **A consensus formed entirely
inside a range is a claim about the range, and the cost of testing outside it
is exactly why nobody does.** Going four and a half doublings past the
convention is what this paper spent its compute on, and the finding is
negative.

## Where it sits among the record's other reasons

Three arguments now say the negative count is not a quality dial, and **none
of them is downstream of the others**:

| argument | source | form |
| --- | --- | --- |
| the InfoNCE bound cannot certify more than `log N` | `THEORY-085` | information-theoretic |
| batch-size gaps "decrease or disappear" with longer training | `LIT-591` | training-budget |
| performance saturates at 32k, measured to 1M | this | direct empirical |

The first says the certificate saturates, the second says the advantage is
convergence speed rather than quality, and the third says the curve flattens.
They could all have been false together; that they agree is the strongest
corroboration this cluster produces.

## Conditions

- **32k is a number for image-text pretraining with these encoders**, on
  this data, at these training durations. What transfers is that a ceiling
  exists and is findable — and that it may sit below the convention.
- **Saturation is not a cliff.** Larger batches are not *worse*; they stop
  paying, which matters because the cost is real and rises.
- **Interacts with training length** (`LIT-591`): a saturation point measured
  at one budget need not hold at another, and the two papers vary different
  things.
- **One group.** The consensus reading says `unreplicated` for a reason, and
  a second measurement past 64k is what would settle it.

## Known implementations

-
