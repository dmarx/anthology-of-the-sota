---
status: Active
formerly:
- SOTA-tmp8u4ld
consensus: converged
consensus_note: >-
  Every reasoning recipe in this record runs it — R1 (LIT-164), Olmo 3's RLVR
  stages (LIT-130), Falcon-H1-Tiny at 0.6B (LIT-119) — and the three papers
  that attack GRPO's objective (LIT-167, LIT-168, LIT-180) all keep the group
  baseline while changing something else. The dissent is about the objective's
  details, not about dropping the critic.
title: 'Estimate the RL baseline from a group of samples for the same prompt instead of training a critic'
version: 1
tags:
- training-optimization
date: '2026-09-07'
published: '2024-02-01'
source:
- LIT-127
- LIT-119
- LIT-168
- LIT-180
implementations: []
summary: >-
  Shao et al. (2024), [LIT-127](../literature.d/LIT-127.md) — Group Relative Policy Optimization: PPO with
  the value model dropped and the baseline taken from the scores of several
  outputs sampled for the same prompt, which removes a model-sized chunk of
  the RL memory footprint and is what every later reasoning recipe in this
  record actually runs.
extended_by:
- SOTA-146
---

# SOTA-145: Estimate the RL baseline from a group of samples for the same prompt instead of training a critic

PPO needs a value model to tell it whether an outcome was better than
expected. At LLM scale that critic is a second network of comparable size,
trained alongside the policy, and it is the largest avoidable cost in the RL
stage.

GRPO ([LIT-127](../literature.d/LIT-127.md)) removes it. Sample a group of
outputs for the same prompt, score them, and use the group's own statistics as
the baseline: an output is good relative to its siblings rather than relative
to a learned prediction. The critic disappears and the advantage estimate
becomes a within-group comparison.

## Why this is the settled part

The record holds four papers that run or rework GRPO, and **all four keep the
group baseline**:

- [LIT-119](../literature.d/LIT-119.md) runs it on a 0.6B reasoning model and reports it sensitive above
  all to the learning rate — a tuning finding, not an objection to the method.
- [LIT-167](../literature.d/LIT-167.md) identifies a length bias in the objective and publishes Dr. GRPO
  to remove it. The group baseline stays.
- [LIT-168](../literature.d/LIT-168.md) decouples the clipping range and adds dynamic sampling. The group
  baseline stays.
- [LIT-180](../literature.d/LIT-180.md) moves the importance ratio from token to sequence level. The
  group baseline stays.

Three independent groups examined this objective closely enough to publish a
correction to it, and none of them proposed bringing the critic back. That is
what `converged` is recording here: not that nobody has looked, but that
people looked hard and changed something else.

## What this does not say

<!-- inactive-ok-block: SOTA-146 — Proposed, and naming it as Proposed is
     the whole point of the sentence -->

It does not say run GRPO as published. That is
[SOTA-146](SOTA-146.md), and it is `Proposed` for a reason: the
same three papers that kept the group baseline each found a different defect
in the rest of the objective, and no two of them fixed the same one.

It also does not say *when* to run RL. [SOTA-129](SOTA-129.md) is the
<!-- inactive-ok: SOTA-130 — Proposed, named as the variation this is orthogonal to -->
three-stage recipe and [SOTA-130](SOTA-130.md) the variation that skips the SFT
stage; both name RLVR as a stage and neither names an algorithm. This is the
algorithm, and it is orthogonal to that argument — the group baseline is what
you run either way.
