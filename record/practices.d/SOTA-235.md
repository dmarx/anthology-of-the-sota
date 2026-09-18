---
number: 235
status: 'Active'
formerly:
- SOTA-tmpv9jzu
title: 'Update the weights at inference on the test instance when the task is structurally novel'
version: 2
history:
- version: 2
  date: '2026-09-18'
  note: >-
    ARC disambiguated to ARC-AGI. The record uses that acronym for two
    unrelated benchmarks; this practice's headline number is on
    Chollet's puzzle set, not the AI2 Reasoning Challenge.
tags:
- adaptation-and-tuning
consensus: unreplicated
consensus_note: >-
  One group, but measured on two benchmarks of different character — a puzzle
  benchmark built to reward search, and ordinary hard reasoning — which is
  what separates this from a single-benchmark result. Nothing in this record
  contests or replicates it.
date: '2026-09-17'
source:
- LIT-379
introduced_by:
- LIT-379
summary: >-
  Akyürek et al. (2024), [LIT-379](../literature.d/LIT-379.md) — [ARXIV-2411.07279](https://arxiv.org/abs/2411.07279). Build a loss from the
  test instance's own in-context examples, take gradient steps at inference,
  then discard the update. Up to 6x a fine-tuned baseline on ARC-AGI (53.0% at
  8B) and +7.3 points on BIG-Bench Hard at 10-shot. The examples are worth
  several times more as gradient than as context.
---

# SOTA-235: Update the weights at inference on the test instance when the task is structurally novel

<!-- inactive-ok-file: SOTA-167 — Proposed, named in the not-to-be-confused-with condition -->

## Source

Akyürek et al. (2024), [LIT-379](../literature.d/LIT-379.md) — [ARXIV-2411.07279](https://arxiv.org/abs/2411.07279).

## The method

"Temporarily updating model parameters during inference using a loss derived
from input data." Each word is load-bearing:

- **Temporarily** — the update is discarded after the instance. Nothing
  accumulates, so this is not fine-tuning and carries none of its risks.
- **During inference** — the cost is per query, not amortized over a training
  run.
- **From input data** — the loss is built from the demonstrations already in
  the prompt. No label arrives from outside, which is what keeps this from
  being supervision in disguise.

## What it buys

| benchmark | result |
|---|---|
| ARC-AGI (public validation, 8B) | **53.0%**, up to **6×** fine-tuned baselines |
| ARC-AGI, ensembled with program synthesis | **61.9%** — the paper's "average human performance" |
| BIG-Bench Hard, 10-shot | **50.5% → 57.8%** (+7.3) |

The BBH number is the one to weigh. ARC-AGI ([LIT-tmpnraor](../literature.d/LIT-tmpnraor.md)) is built to reward
search over structurally novel tasks, which is the regime this method is *defined* by, so
a large gain there is close to tautological. BBH is ordinary hard reasoning,
and the effect surviving there is what says this is not a benchmark artifact.

## The finding underneath, which is about in-context learning

The examples are identical in both conditions. As context they produce one
accuracy; as gradient, several times more. So the shortfall is not missing
information in the prompt — it is that a forward pass cannot extract what is
already there when the task is structurally unfamiliar.

That qualifies [SOTA-038](SOTA-038.md) without contradicting it. In-context learning does
permit few-shot adaptability; on novel tasks it leaves most of the value in
the examples unused.

## Conditions

**"Structurally novel" is the condition, not decoration.** The method targets
tasks outside the training distribution that few-shot prompting handles
badly. On tasks the model already does well, there is no reason to expect a
gradient step on a handful of examples to help, and every reason to expect
the extra cost.

**The cost is severe and unpriced here.** Gradient steps per query is a large
inference-time expense, and the paper reports no latency or FLOP budget this
record can cite. Anyone choosing this is trading a lot of compute per query
for accuracy on a class of task they should be able to identify in advance.

**Not to be confused with TTT layers.** `ARXIV-2407.04620` shares the
abbreviation and is a sequence architecture whose hidden state is a model
updated as tokens arrive — the linear-attention and SSM lineage ([SOTA-132](SOTA-132.md),
[SOTA-167](SOTA-167.md)), not inference-time adaptation. Different claim, same three
letters.
