---
number: 154
status: Active
formerly:
- SOTA-tmpex7d9
consensus: contested
# inactive-ok-block: THEORY-tmp38myz — Proposed, and the account that
# predicts where the dissent's evidence sits; the note is the reconciliation
consensus_note: >-
  Three independent groups now report evolution strategies at or ahead of
  policy-gradient RL on models up to 8B (LIT-211, LIT-tmphm6g2, LIT-tmp4zb0l
  — the last on a recurrent architecture), and a fourth (LIT-tmp9pcfv) says
  in its own second sentence that direct ES at LLM scale is ineffective. The trunk — gradient-free search of the full
  parameter space is viable at billion scale — is agreed. The branch in
  dispute is the word "instead": whether it replaces policy-gradient RL or is
  seeded by it. The dissent's models are all at 1.5B or below, which
  THEORY-tmp38myz says is where it should be.
title: 'Fine-tune with evolution strategies instead of policy-gradient reinforcement learning'
version: 2
history:
- version: 2
  date: '2026-09-15'
  note: >-
    Promoted from `Proposed` on the condition the practice set for itself.
    Gan and Isola (LIT-tmphm6g2) ran ES against PPO and GRPO on six tasks
    outside Countdown and the conciseness objective, at matched training
    FLOPs, with the RL arm grid-searched over learning rate and batch or
    group size while ES ran one fixed configuration — an independent group,
    a harder-tuned baseline, and ES ahead in most cells. Consensus moved
    from `unreplicated` to `contested` in the same edit, which is not a
    hedge: what makes it contested is a fourth group arriving with a
    counter-argument, and that could not have been recorded while the axis
    still said nobody had replied.
tags:
- adaptation-and-tuning
date: '2026-09-07'
source:
# LIT-211 ran the comparison itself against both PPO and GRPO, which is what
# made this evidenced rather than asserted (ADR-017). LIT-tmphm6g2 is the
# independent evaluation that promoted it: a different group, six further
# tasks, and the RL arm tuned harder than the ES arm.
#
# LIT-tmp4zb0l is deliberately NOT here. Its LLM comparison is real and
# favourable, but it is on a recurrent architecture and on its own low-rank
# variant, so it is evidence about the line rather than about this
# recommendation; the lineage on the notes is where it belongs.
- LIT-211
- LIT-tmphm6g2
introduced_by:
- LIT-211
# The evidence AGAINST, required where the record claims there is some
# (ADR-016). Gu et al. argue direct ES at LLM scale is ineffective and
# replace the search space with a gradient-seeded subspace.
contested_by:
- LIT-tmp9pcfv
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
  experiment. `Active` since Gan and Isola replicated the comparison on six
  further tasks with the RL arm tuned harder; `contested`, because Gu et al.
  argue direct ES at LLM scale does not work — on models at 1.5B and below.
explained_by:
- THEORY-tmp38myz
extended_by:
- SOTA-tmpm80i3
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

## The replication, and why it counts

Gan and Isola ([LIT-tmphm6g2](../literature.d/LIT-tmphm6g2.md)) ran evolution strategies as a baseline in
a paper about something else, and that is what makes it worth more than a
friendly replication rather than less. Six tasks outside Countdown and the
conciseness objective — GSM8K, MATH-500, OlympiadBench, MBPP, ROCStories,
USPTO. Qwen2.5 at 0.5B–3B, OLMo3-7B base and instruct, Llama-3.1-8B-Instruct.
All arms matched on training FLOPs, with PPO and GRPO grid-searched over
learning rate and batch or group size while ES ran a single fixed
configuration. ES came out ahead of GRPO in most cells, and ES with test-time
majority voting took the best or runner-up cell in roughly half the table.

That is the practice's own promotion condition, met: an independent group, a
policy-gradient baseline that got at least the same tuning budget, on tasks
outside the original two. It is not weakened by having arrived as a baseline
— a group with no stake in the result, tuning the rival harder than the
method, is the *stronger* form of the evidence the condition was asking for.

<!-- inactive-ok-block: THEORY-tmp38myz — Proposed, and named as the account
     this practice acquired rather than as evidence for the recommendation -->
The practice also acquired something the condition did not ask for: an
account of why it works, in [THEORY-tmp38myz](../theory.d/THEORY-tmp38myz.md).

## What is contested, and what is not

Gu et al. ([LIT-tmp9pcfv](../literature.d/LIT-tmp9pcfv.md)) disagree, in their own second sentence:
"directly applying ES to billion-parameter LLMs is highly ineffective",
because almost all random perturbations in such a space are near-orthogonal
to a useful descent direction. Their Hyper-ES replaces the search space
rather than the optimizer — a handful of cheap GRPO runs supply LoRA descent
directions, and CMA-ES searches merging coefficients over their span. It is
gradient-seeded, and it beats GRPO-LoRA by about one point.

Two things about that dissent are worth stating precisely rather than
averaging away.

**It is a theoretical argument plus a small-model measurement, not a failed
reproduction.** The ES baseline in their table is CMA-ES over LoRA, not
full-parameter ES at the scale [LIT-211](../literature.d/LIT-211.md) reports. Nobody has run the thing
this practice recommends and reported that it did not work.

<!-- inactive-ok-block: THEORY-tmp38myz — Proposed, and this paragraph is the
     record's own reconciliation of the dispute; it rests on that account
     being what predicts the dissent's scale, which is the citation's point -->
**Every model they test is at 1.5B or below** — and [THEORY-tmp38myz](../theory.d/THEORY-tmp38myz.md) says
the density of task-improving perturbations rises with scale, with gains
appearing sharply from about 1.5B and absent beneath it. So the dissent is
measured exactly where this record's account predicts a negative result, and
their lemma about near-orthogonal perturbations is the needle-in-a-haystack
regime under another name. **That reconciliation is this record's, not either
paper's** — they do not cite each other — and it is offered as the reading to
test, not as a dismissal.

The experiment that would settle it is the one nobody has run: full-parameter
ES against a well-tuned GRPO on the same benchmarks at 7B and above.

## Conditions, and what is not established

The evidence now spans eight tasks and three model families at 0.5B–8B, with
**no frontier deployment and no released model whose post-training recipe
uses it**. That is still a long way from the post-training this record
describes, which runs multi-stage on models an order of magnitude larger.
Below about 1.5B, the practice should be expected to fail and the dissent
above is the evidence that it does.

`Active` here means the record is willing to assert the recommendation on
eight tasks at 8B and below. It does not mean the field has settled —
`consensus: contested` is carrying that, and the two axes disagreeing is the
arrangement they exist for.

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

## The line this heads

<!-- inactive-ok-block: SOTA-tmpm80i3 — Proposed, and named as the practice
     that extends this one; the lineage is what the citation is for -->
This is the first entry in what is now a line rather than a single result.
[LIT-tmp4zb0l](../literature.d/LIT-tmp4zb0l.md) (EGGROLL) makes the search affordable — rank-`r`
perturbations per worker, a high-rank population average, and a hundredfold
throughput gain at billion scale. [LIT-tmp9pcfv](../literature.d/LIT-tmp9pcfv.md) (Hyper-ES) is the dissent
above. [SOTA-tmpm80i3](SOTA-tmpm80i3.md) is the degenerate case — one round instead of many,
with an ensemble on the end — and `extends:` this practice for that reason.

## Known implementations

- None in a released model. The published results are the authors' own, and
  that absence is the half of the original promotion condition that is still
  unmet.
