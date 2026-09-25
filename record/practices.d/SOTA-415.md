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
version: 1
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
  late in training, and it has no hyperparameter.
- **Keep the window short early.** At 204B tokens on a 1.3B/13B MoE, a 32B-token
  window was 4.6 points *below* the raw checkpoint. By about 450B tokens the
  window hardly matters.

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
