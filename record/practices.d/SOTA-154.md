---
number: 154
status: Proposed
formerly:
- SOTA-tmpex7d9
promote_when: >-
  An independent group running evolution strategies against a policy-gradient
  baseline that got the same tuning budget, on a task outside Countdown and
  the conciseness objective; or a post-training recipe on a released model
  above 8B that uses it. What would not move this: further results from the
  same group, or a comparison in which the RL arm was left at defaults.
consensus: unreplicated
consensus_note: >-
  One group, two tasks, models at 8B and below. The paradigm it argues
  against is what every reasoning recipe in this record runs, so the
  disagreement is real but one-sided — nobody has published a reply.
title: 'Fine-tune with evolution strategies instead of policy-gradient reinforcement learning'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-07'
published: '2025-09-01'
source:
# The paper ran the comparison itself, against both PPO and GRPO, which is
# what makes this evidenced rather than asserted (ADR-017). No adopters to
# add — that absence is what promote_when is about.
- LIT-211
# The comparison the paper actually ran: ES against GRPO, which is SOTA-145.
# Stated once here, on the practice that ran it; the fixer writes the other
# side.
compared_against:
- SOTA-145
implementations: []
summary: >-
  Qiu et al. (2025), [LIT-211](../literature.d/LIT-211.md) — evolution strategies over the full
  parameter space of a billion-scale LLM, which the field had assumed
  impossible. +36.4% over base on average against GRPO's +21.3% and PPO's
  +17.9%, with ES on one fixed hyperparameter set while RL got a sweep per
  experiment. Filed `Proposed`: two tasks, 8B and below, no deployment.
---

# SOTA-154: Fine-tune with evolution strategies instead of policy-gradient reinforcement learning

## Source

Qiu et al. (2025), [LIT-211](../literature.d/LIT-211.md) — [ARXIV-2509.24372](https://arxiv.org/abs/2509.24372).

The assumption this overturns is that searching a billion-dimensional
parameter space directly is hopeless, which is why prior ES work on LLMs
reduced the dimension — last layer only, or a low-rank subspace. This
searches the full parameter space and reports the first successful
application at that scale.

The result is backpropagation-free, and the paper's account of where the
advantage comes from follows from that: tolerance to long-horizon and delayed
rewards, robustness across different base models, reduced susceptibility to
reward hacking, and steadier training.

## Why the comparison is worth more than its headline number

It is deliberately tilted against itself. **ES ran with one fixed
hyperparameter set across every experiment.** RL got a per-experiment grid
over the KL penalty β and the learning rate α, because the authors found RL
"did not make much progress if they were not set precisely" and took the best
configuration each time.

Averaged across Qwen2.5 (0.5B–7B) and LLaMA3 (1B–8B) on Countdown, ES
improves over the base model by **36.4%**, PPO by **17.9%**, GRPO by
**21.3%** at group size 8 and **21.4%** at group size 30.

A comparison arranged to favour the baseline and won anyway is a stronger
result than a larger margin from a sweep, which is why this is the part the
practice rests on.

## Conditions, and what is not established

Two tasks — Countdown, a reasoning puzzle, and a conciseness objective — at
8B and below, with no frontier deployment. That is a long way from the
post-training this record describes, which runs multi-stage on models an
order of magnitude larger. The claim to have scaled ES is well supported; the
claim that it should replace RL in a production recipe is not made by the
paper and is not made here.

## Against the post-training spine

[SOTA-129](SOTA-129.md) makes reinforcement learning with verifiable rewards the third stage
of the reasoning recipe, [SOTA-145](SOTA-145.md) recommends the group baseline inside it,
<!-- inactive-ok: SOTA-146 — Proposed, and named as one of the three practices that assume the paradigm -->
and [SOTA-146](SOTA-146.md) corrects the objective. All three assume the paradigm; this is a
different paradigm reaching the same goal.

Be precise about what it does and does not disturb. [SOTA-145](SOTA-145.md)'s argument is
that every work which *runs or reworks GRPO* keeps the group baseline. ES
does not run GRPO, so it is not a counterexample to that — it is evidence
about whether to be in that family at all, and `compared_against:` is the
relation for a rival somebody actually measured rather than a successor.

One detail bears on [SOTA-145](SOTA-145.md) directly and mildly: raising GRPO's group size
from 8 to 30 moved the average by 0.1 points here. One task, but a data point
on what the group baseline's width buys.

## Known implementations

- None. The published results are the authors' own.
