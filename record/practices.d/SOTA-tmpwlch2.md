---
status: Proposed
consensus: unreplicated
consensus_note: >-
  One group, one sweep. The convention it displaces is `universal` in the
  adoption sense — 15% is in every MLM codebase and nobody justifies it — and
  that is exactly what `DP-005` says not to count as evidence, which cuts
  against the incumbent here rather than for it. Nobody has re-run the sweep,
  and the field largely stopped training encoder MLMs before it could.
  Read as of 2026-09.
promote_when: >-
  A second group sweeps the rate at more than one model size and reports the
  optimum, on any MLM. Not a single run at a higher rate: the claim is that the
  optimum *moves with capacity*, so a paper reporting that 40% worked for its
  one model would be consistent with a fixed optimum of 40% and would not
  settle it.
title: 'Scale the masked-language-modelling rate with model size rather than holding it at 15%'
version: 1
tags:
- representation-and-encoding
- training-optimization
date: '2026-09-25'
source:
- LIT-tmpqkx1z
# Same code as `source:`. Wettig et al. ran the sweep and drew the
# recommendation from it; the 15% it displaces was never a recommendation
# anybody argued for, only one everybody copied (ADR-030).
introduced_by:
- LIT-tmpqkx1z
implementations: []
summary: >-
  Wettig et al. (2022), [LIT-tmpqkx1z](../literature.d/LIT-tmpqkx1z.md). The masking rate has been held at 15%
  "regardless of model sizes or masking strategies" since 2018, and the number
  was never swept. Swept, the optimum moves with capacity: **40% at 354M, 20%
  at 124M, 15% at 51M**. At 354M, 40% wins seven of nine GLUE-plus-SQuAD tasks
  and reaches the 15% model's QNLI and QQP scores **in half the training
  time** — under an efficient recipe, with the advantage shrinking on longer
  schedules.
---

# SOTA-tmpwlch2: Scale the masked-language-modelling rate with model size rather than holding it at 15%

<!-- inactive-ok-file: THEORY-088 — Proposed, named as the account this practice's evidence corrects:
     the rate moves with capacity while the signal is fixed. Open is the point. -->

## Source

Wettig, Gao, Zhong and Chen (2022), [LIT-tmpqkx1z](../literature.d/LIT-tmpqkx1z.md) —
[ARXIV-2202.08005](https://arxiv.org/abs/2202.08005).

## What to do

Treat the masking rate as a hyperparameter of the model, not a constant of the
objective. The measured optima, averaged over GLUE and SQuAD under an efficient
pre-training recipe:

| model | parameters | rate |
| --- | --- | --- |
| medium | 51M | 15% |
| base | 124M | 20% |
| large | 354M | 40% |

At 354M the 40% run beats 15% on seven of nine tasks — SQuAD +1.8, RTE +2.0,
MRPC +1.0 — and loses on SST-2 (−0.2) and CoLA (−1.1). The efficiency number is
the one to plan around: on QNLI and QQP, 40% reaches the 15% model's score in
**half the training steps**.

If you use a structured masking strategy, expect a *lower* optimum than these.
Span masking and PMI masking make the task harder at a given rate, so uniform
masking admits the higher rate; the prior comparisons between strategies were
all run at a fixed 15% and their conclusions do not transfer unexamined to a
higher one.

## Conditions

**The advantage is largest where the compute is smallest.** The sweep uses an
efficient recipe with relatively few steps. Under a longer schedule and under
RoBERTa's more expensive recipe, the authors report 40% "achieving similar
performance to the 15% masking rate". So this buys a faster path to a given
quality more reliably than it buys a better endpoint, and a reader on a long
schedule should expect the gap to close.

**Two tasks prefer the old number**, at the end of training: SST-2 and CoLA. The
optimum is task-dependent as well as size-dependent, and a single-task target
deserves its own check.

**Encoder MLM only, 51M to 354M.** Nothing here is measured on a decoder or on
next-token prediction, and nothing here is above 354M — so "larger models want
higher rates" is a trend over three points, not a law with a slope you can
extrapolate.

**It is not a claim about redundancy.** The rate moves with *capacity* here
while the signal is held fixed, which is what corrects [THEORY-088](../theory.d/THEORY-088.md) — and
at an 80% rate, where validation perplexity exceeds 1,000 and nothing can be
reconstructed, 95% of fine-tuning performance survives. Whatever sets the useful
rate, it is not whether the masked content is recoverable.

## Known implementations

- None known at the time of filing. 15% remains the default in the MLM
  codebases this record can name, which is a fact about inertia rather than
  about evidence (`DP-005`).
