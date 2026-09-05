---
status: Active
title: 'Use a warmup-stable-decay schedule: hold the learning rate, then decay it sharply over the final 10–20% of tokens'
version: 1
tags:
- training-optimization
date: '2026-09-05'
published: '2024-04-01'
source:
- LIT-144
summary: >-
  Hu et al. (2024), [LIT-144](../literature.d/LIT-144.md), with the controlled comparison in [LIT-145](../literature.d/LIT-145.md) — matches or beats cosine, leaves the token budget open, makes every stable-stage checkpoint a usable branch point; the schedule of every 2025–2026 report in the record.
---

# SOTA-140: Use a warmup-stable-decay schedule: hold the learning rate, then decay it sharply over the final 10–20% of tokens

## Source

Hu et al. (2024), [LIT-144](../literature.d/LIT-144.md) — MiniCPM; Hägele et al. (2024), [LIT-145](../literature.d/LIT-145.md), for the
comparison against cosine.

Warm up, hold the learning rate at its peak for most of training, then
decay it fast over the last stretch — about 10% of the tokens in MiniCPM,
up to about 20% in Hägele et al., who found the cooldown's length and
shape to matter and recommend a 1-sqrt shape to zero. Most of the loss
improvement arrives in the decay. Final quality matches or beats a cosine
schedule of the same length, and the schedule scales as predictably as
cosine across model sizes.

What it buys beyond quality: the total token count need not be fixed when
training starts, since the decay can be launched from any stable-stage
checkpoint; scaling laws can be fitted from one run's checkpoints instead
of a run per duration; continued pretraining is a matter of resuming the
stable stage; and high-quality or SFT-style data can be concentrated in
the decay ([LIT-144](../literature.d/LIT-144.md)), which is where [LIT-119](../literature.d/LIT-119.md)'s recipes put theirs.

Conditions: the peak learning rate must be tuned for the constant stage —
a value tuned for cosine is too high to hold. [LIT-146](../literature.d/LIT-146.md) ([SOTA-142](SOTA-142.md)) is one
way to set it. How far the decay goes is its own question: [LIT-147](../literature.d/LIT-147.md)
<!-- inactive-ok: SOTA-141 — a Proposed refinement of the decay, named as part of the schedule chain -->
([SOTA-141](SOTA-141.md)) argues for all the way to zero; production recipes in the record
decay to a floor (Falcon-H1-Tiny: ×64 exponential over 100 GT of 800 GT).

## Sequence

<!-- inactive-ok: LIT-042 — the retired warm-restarts paper, named as the start of the schedule chain -->
Warm restarts ([LIT-042](../literature.d/LIT-042.md), retired) → a single cosine cycle ([LIT-035](../literature.d/LIT-035.md),
<!-- inactive-ok: SOTA-039 — the retired cosine practice, named as the predecessor in the chain -->
[SOTA-039](SOTA-039.md), retired by this) → WSD, with its decay shape and depth still
<!-- inactive-ok: SOTA-141 — a Proposed refinement of the decay, named as part of the schedule chain -->
being settled ([SOTA-141](SOTA-141.md)) and its peak set by scaling law ([SOTA-142](SOTA-142.md)).

## Known implementations

- MiniCPM; Falcon-H1 and Falcon-H1-Tiny; the frontier reports of 2025–2026 in the record describe stable-then-decay schedules throughout
