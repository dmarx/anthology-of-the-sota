---
number: 231
status: 'Active'
formerly:
- SOTA-tmpdf5n5
title: 'Put an adapter on every linear layer, not just the attention query and value projections'
version: 1
tags:
- adaptation-and-tuning
consensus: unreplicated
consensus_note: >-
  One group, one sweep. Nobody in this record has agreed or disagreed, and
  the claim contradicts a default that a great deal of published fine-tuning
  still uses — which is a reason to watch it rather than a reason to
  discount it.
date: '2026-09-17'
source:
- LIT-378
introduced_by:
- LIT-378
summary: >-
  Dettmers et al. (2023), [LIT-378](../literature.d/LIT-378.md) — [ARXIV-2305.14314](https://arxiv.org/abs/2305.14314). Adapters on the query
  and value projections alone — the default inherited from the LoRA paper —
  do not reach full fine-tuning on large base models. The number of adapted
  matrices is the hyperparameter that decides it; the projection rank `r`,
  which is the one people tune, does not affect performance across the
  paper's sweep.
---

# SOTA-231: Put an adapter on every linear layer, not just the attention query and value projections

## Source

Dettmers et al. (2023), [LIT-378](../literature.d/LIT-378.md) — [ARXIV-2305.14314](https://arxiv.org/abs/2305.14314).

## The claim

Applying LoRA to the query and value attention projections is the standard
practice, and it comes from the LoRA paper's own experiments ([LIT-046](../literature.d/LIT-046.md),
[SOTA-184](SOTA-184.md)). On large base models it does not replicate full fine-tuning.

What closes the gap is **how many matrices carry an adapter**, and the answer
the paper reaches is all the linear layers in the transformer block — not
attention alone, and not attention plus a chosen few. In their words, LoRA on
all linear transformer block layers is *required* to match full fine-tuning.

## The knob that is inert, and the knob that is not

The same sweep reports that the projection rank `r` does not affect
performance. So the two hyperparameters trade places against the usual habit:

| | usually tuned | what the evidence says |
|---|---|---|
| rank `r` | yes, extensively | no effect across the sweep |
| which matrices are adapted | left at the default | decides whether the method works |

Anyone who searched `r` and left placement at query/value was searching the
dimension the measurements say is flat.

## Why this is believable, which is a separate question

Because they re-tuned the *baseline* too. The paper states that default
hyperparameters for fully fine-tuned baselines are undertuned and searches
learning rate 1e-6 to 5e-5 and batch size 8 to 128 to get a fair comparison.
A weak baseline is how a placement default survives unexamined — it makes
query/value look adequate by making the thing it is measured against worse.
That the finding survived a strengthened baseline is most of its weight.

## Conditions

Stated for **large base models**; the LoRA paper's own tasks were smaller and
its query/value result was not wrong about them. So this is a scale
condition, not a refutation — the failure appears where the base is big
enough that a low-rank update over two matrices per block cannot carry the
adaptation.

It costs trainable parameters and optimizer state, in proportion to how many
more matrices are adapted. That is a real cost against the whole argument for
adapters, and the paper's answer is that `r` is free to be small, so the
product of (many matrices × small rank) stays cheap.

Independent of quantization. It applies to ordinary 16-bit LoRA, and a reader
who will never quantize anything should still take it.
