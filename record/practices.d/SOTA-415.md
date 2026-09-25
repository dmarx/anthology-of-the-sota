---
number: 415
status: Proposed
formerly:
- SOTA-tmpc94s8
consensus: emerging
consensus_note: >-
  Hägele et al. (LIT-145) and Li et al. (LIT-684) report the effect
  independently, at ≤1B and up to 20B/200B MoE and 70B dense respectively.
  LIT-445 uses the same instrument. No one reports a contradiction. What is
  *not* established is using the average as a replacement for the anneal. Read
  as of 2026-09.
promote_when: >-
  A second group compares constant LR plus a checkpoint average against a real
  anneal *from the same fork, at a matched token budget*, with seeds or a
  stated evaluation-noise band, at 1B or more active parameters, and reports
  how far the proxy sits from the annealed score. A report that merging helps
  against an unannealed checkpoint does not count, because that is the
  premise, not the claim.
title: 'During a warmup-stable-decay run, estimate the annealed score from a uniform average of recent stable-phase checkpoints instead of launching a decay branch'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Qualifies one of the two reasons given for uniform averaging. "It has no
    hyperparameter" was true as a description of uniform averaging and false as an
    argument for it: LIT-tmp7nrwv shows the averaging length can be swept after
    the run from stored snapshots, so the hyperparameter is avoidable rather than
    unaffordable — and this practice's own next bullet is a heuristic for tuning a
    window, which is the hyperparameter it said there was not one of.
    Recommendation, status and consensus unchanged.
tags:
- training-optimization
- analysis-and-evaluation
date: '2026-09-25'
source:
- LIT-684
- LIT-145
# LIT-684 is the large-scale measurement and the one fork against a
# real anneal. LIT-145 is the earlier, independent result at smaller scale
# (ADR-030).
introduced_by:
- LIT-145
implementations: []
summary: >-
  Li et al. (2025), [LIT-684](../literature.d/LIT-684.md), extending Hägele et al. (2024), [LIT-145](../literature.d/LIT-145.md).
  To see where a WSD run would land if annealed now, evaluate the simple
  average of its last ~10 stable-phase checkpoints. On the one fork measured,
  that proxy sits within about 1.5 points of a real 250B-token anneal on each
  benchmark. It costs no training. **Still anneal the model you ship**: on that
  fork the anneal is ahead on MMLU at the end.
---

<!-- inactive-ok-file: SOTA-156 — Proposed; named as the rival practice for dropping the
     decay, which this one explicitly does not recommend -->

# SOTA-415: During a warmup-stable-decay run, estimate the annealed score from a uniform average of recent stable-phase checkpoints instead of launching a decay branch

## Source

Li et al. (2025), [LIT-684](../literature.d/LIT-684.md). The practice's idea is earlier,
in Hägele et al. (2024), [LIT-145](../literature.d/LIT-145.md): averaging along a constant-LR
trajectory improves the model at no training cost.

## What to do

In the stable phase of a warmup-stable-decay run ([SOTA-140](SOTA-140.md)), take a
uniform average (SMA) of the last ~10 checkpoints and evaluate it. Treat the
result as an estimate of where an anneal from here would land, for decisions
such as when to stop, whether to change data, or how to fit a scaling
curve. Launch the actual decay for the model you release.

- **Use a uniform average.** Weighted and exponential schemes converge with it
  late in training. It is also the cheapest thing to get right, which is not the
  same as having nothing to get right — see below.
- **Keep the window short early.** At 204B tokens on a 1.3B/13B MoE, a 32B-token
  window was 4.6 points *below* the raw checkpoint. By about 450B tokens the
  window hardly matters.
- **The window is a hyperparameter, and it does not have to be guessed.** The
  bullet above is a heuristic for tuning one, so "uniform averaging has no
  hyperparameter" — this practice's v1 wording — was describing the *scheme*
  rather than the choice. [SOTA-tmp0s2gj](SOTA-tmp0s2gj.md) is the alternative: keep two
  power-function averages during the run and reconstruct any window afterwards by
  least squares, which works retroactively from stored snapshots at reduced
  accuracy. That makes the window measurable on runs already finished instead of
  guessed, and it is how the "by about 450B tokens the window hardly matters"
  claim could be checked at other scales rather than carried.

## Why

Averaging checkpoints along a noisy constant-LR trajectory cancels much of the
noise that a decay would anneal away. That is the effect both sources
measure. Why it works is not established in the record. The source's Taylor
argument is algebra that holds for any average near a minimum and measures
nothing.

## Conditions

- **One fork against a real anneal.** The "matches annealing" evidence is one
  1.3B/13B MoE, four plotted benchmarks, no seeds. At the end the anneal led
  by about 1.5 MMLU, tied on BBH and GSM8K, and trailed on HumanEval.
- **Private data and architecture**, and a composite metric with unstated
  weights.
- **The learning rate is not swept.** The average's value depends on the
  stable-phase LR, which the source held at its scaling-law setting.
- **Not a replacement for the decay.** Nothing here supports skipping it for a
  model you will use. [SOTA-156](SOTA-156.md) is the practice that argues for no
  decay at all, by a different mechanism.

## Known implementations

- None recorded.
