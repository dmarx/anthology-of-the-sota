---
status: Active
title: 'Set the peak learning rate by a power law in tokens so it transfers across batch size and training length'
version: 1
tags:
- training-optimization
date: '2026-09-05'
published: '2024-08-01'
source: LIT-146
summary: >-
  Shen et al. (2024), [LIT-146](../literature.d/LIT-146.md) — under WSD the optimal learning rate is a power law in tokens and batch size; the Power scheduler applies it, and with µP the same setting carries across model sizes; adopted independently by Falcon-H1-Tiny.
---

# SOTA-142: Set the peak learning rate by a power law in tokens so it transfers across batch size and training length

## Source

Shen et al. (2024), [LIT-146](../literature.d/LIT-146.md) — the Power scheduler.

Under a warmup-stable-decay schedule ([SOTA-140](SOTA-140.md)), the optimal learning rate
follows a power law in the number of training tokens and the batch size.
The Power scheduler applies the law directly: the learning rate is a power
of the tokens seen, capped at a maximum, with the WSD decay at the end. A
value found on a short run at one batch size then holds when the run is
lengthened or the batch changed, and with µP ([SOTA-143](SOTA-143.md)) when the model is
widened, so one sweep serves the whole family.

Conditions: fitted under WSD; the exponents are the paper's and were
measured on its own model family, so a new family should re-fit them from
a few short runs. Falcon-H1-Tiny ([LIT-119](../literature.d/LIT-119.md)) is the record's independent
adoption — a square-root decay of the learning rate from 100 GT onward,
inside its WSD schedule — which is what moves this from one group's result
to a practice.

## Known implementations

- PowerLM-3B and PowerMoE-3B; Falcon-H1-Tiny
