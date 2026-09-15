---
status: Proposed
promote_when: >-
  A group reporting the drift-versus-population trade directly — same task
  accuracy reached at higher N and lower T, with prior-task retention
  measured — or an ES post-training run that reports its stopping rule and
  the held-out capability it preserved. What would not satisfy this: another
  demonstration that ES forgets, which is the problem rather than evidence
  the remedy works.
consensus: emerging
consensus_note: >-
  Two groups supply the two halves. LIT-tmppbfp5 shows the forgetting
  accumulating in the stretch after the target task has converged, and
  LIT-tmp4w505 gives the scaling that says why and reports ES staying
  competitive in continual learning "when its iteration budget is
  controlled". Neither states the rule as an instruction; the record is
  joining them, and says so.
title: 'Stop evolution-strategies post-training when the target task converges, and buy accuracy with population size rather than more steps'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-15'
source:
# LIT-tmp4w505 is primary: it supplies the mechanism and the knob. LIT-tmppbfp5
# is the measurement of what happens when nobody turns it.
- LIT-tmp4w505
- LIT-tmppbfp5
# Neither paper states this as a recommendation — LIT-tmp4w505 states the
# scaling and the qualifier "when its iteration budget is controlled", which
# is the nearest thing to it and is where the instruction comes from.
introduced_by:
- LIT-tmp4w505
extends:
- SOTA-154
implementations: []
summary: >-
  Hoy et al. and Abdi et al. (2026), [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md) and [LIT-tmppbfp5](../literature.d/LIT-tmppbfp5.md) — an ES
  run's off-manifold displacement grows as sigma^2 d T / N, so every step past
  convergence buys drift and nothing else. Countdown peaks at about 200
  iterations and held-out HellaSwag keeps falling to 500; across four
  sequential tasks the ES update norm grows 87 to 173 where GRPO's grows 1.0
  to 1.8. Raise the population, cap the steps, and stop when the target task
  stops moving.
explained_by:
- THEORY-tmpt76ks
---

# SOTA-tmpdcmgg: Stop evolution-strategies post-training when the target task converges, and buy accuracy with population size rather than more steps

## Source

Hoy et al. (2026), [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md) — [ARXIV-2604.01499](https://arxiv.org/abs/2604.01499); Abdi et al.
(2026), [LIT-tmppbfp5](../literature.d/LIT-tmppbfp5.md) — [ARXIV-2601.20861](https://arxiv.org/abs/2601.20861).

## Why a stopping rule matters more here than for gradient methods

<!-- inactive-ok-block: THEORY-tmpt76ks — Proposed, filed in this same change
     and named as the account this instruction is derived from -->
[THEORY-tmpt76ks](../theory.d/THEORY-tmpt76ks.md) is the reason. An ES update splits into a component that
changes the loss and one that cannot; the second is a random walk whose
squared norm grows as `σ²dT/N`. Two consequences follow directly, and they
are the whole practice:

- **Drift is linear in steps.** Every additional iteration adds displacement
  whether or not it adds accuracy. Once the target task has converged, further
  steps buy drift and nothing else.
- **Drift is inversely proportional to population size.** The same amount of
  on-manifold progress reached with a larger population and fewer steps costs
  less off-manifold displacement.

A gradient method has neither problem in this form — gradient descent freezes
on flat directions where ES diffuses — which is why this practice has no
analogue in the RL recipe and why an ES run needs a stopping rule that a GRPO
run does not.

## What it costs to ignore

[LIT-tmppbfp5](../literature.d/LIT-tmppbfp5.md) ran Countdown to 500 iterations on Qwen2.5-1.5B-Instruct.
Countdown accuracy reaches near-maximum by about **200**. Held-out HellaSwag
declines steadily across the whole run, tracing a convex Pareto front — and
the decline continues through the 300 iterations that bought no task
performance at all. The Frobenius drift after 500 iterations is roughly
**1000×** GRPO's on the same task.

In the sequential setting, [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md) reports the ES update norm growing
from 87.28 to 173.00 across four tasks where GRPO's grows from 1.00 to 1.84 —
a ratio of 87–107× — and states that ES "remains competitive sequentially
**when its iteration budget is controlled**". That qualifier is the closest
either paper comes to stating this practice, and it is where the instruction
comes from.

## How to act on it

1. **Track the target metric and a held-out capability on the same axis.** The
   Pareto front is the artifact worth producing; the convex shape is the
   warning.
2. **Stop when the target task stops improving**, not when the budget runs
   out. The gap between those two points is pure capability loss.
3. **Spend a larger budget on population, not iterations**, where the cluster
   allows it. `N` divides the drift; `T` multiplies it. This also aligns with
   [LIT-230](../literature.d/LIT-230.md)'s finding that the population needed for stable ES *falls* as
   models grow — so at larger scale the same `N` is buying more.
4. **Expect the perturbation scale to be two-sided.** `σ²` is in the numerator
   of the drift, and [LIT-230](../literature.d/LIT-230.md) reports too-small `σ` overfitting the sampled
   rewards. Reducing it is not a free way to cut drift.

## Conditions, and what is not established

**Both sources are at 4B and below**, on four and three tasks respectively.
The scaling is theoretical and general; the demonstrations are not.

**Nobody has run the remedy.** This is the record joining a mechanism to a
measurement, and both papers are named so a reader can see the join rather
than take it on trust. The promotion condition asks for the trade to be
reported directly — same accuracy at higher `N` and lower `T`, with retention
measured — because that is the experiment neither paper ran.

<!-- inactive-ok-block: SOTA-212 — Proposed, and named as the practice this
     failure mode cannot reach; that is what the citation is for -->
**It does not apply to [SOTA-212](SOTA-212.md).** That practice's whole form is a single
parallel round, so `T = 1` and there is no stretch past convergence for drift
to accumulate over. Whether one round at large `N` is a *general* answer to
this problem is an interesting question and not one anybody has asked.

**It does not resolve whether the drift is otherwise harmful.**
[LIT-230](../literature.d/LIT-230.md) finds no broad forgetting at a single-task horizon and
[LIT-tmppbfp5](../literature.d/LIT-tmppbfp5.md) finds plenty past convergence. This practice is what both
results are consistent with; it is not a finding that either paper made.

## Known implementations

- None. Neither source paper adopts a stopping rule; both report what happens
  without one.
