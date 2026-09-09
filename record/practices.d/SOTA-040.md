---
number: 40
status: 'Active'
title: 'larger models are more sample efficient'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2020-01-01'
source:
- LIT-028
summary: >-
  Kaplan et al. (2020), [LIT-028](../literature.d/LIT-028.md) — [ARXIV-2001.08361](https://arxiv.org/abs/2001.08361).
---

# SOTA-040: larger models are more sample efficient

## Source

Kaplan et al. (2020), [LIT-028](../literature.d/LIT-028.md) — [ARXIV-2001.08361](https://arxiv.org/abs/2001.08361).

## What "more sample efficient" means here

[LIT-028](../literature.d/LIT-028.md)'s power laws relate loss to model size, dataset size and compute, and
this is one of their consequences: at a fixed number of tokens seen, a larger
model reaches a lower loss. Scale substitutes for data.

The practical form is the one that changed how runs are planned — given a
compute budget, the loss-minimising split is not "train a small model for a
long time" but a specific trade between size and tokens, and Kaplan et al.
put the optimum heavily on the size side.

## Which is the part that did not survive

Chinchilla's re-derivation found the earlier analysis had held the learning
rate schedule fixed in a way that penalised longer runs, and that the
compute-optimal ratio is far more token-heavy — roughly 20 tokens per
parameter rather than the much smaller ratio implied here.

The record does not hold that correction as a source, which is worth flagging:
this practice states one side of a superseded trade-off and nothing beside it
says so. Its claim as narrowly written — *larger models are more sample
efficient* — remains true, and the planning advice people took from it does
not.

That gap is the reason this body is worth more than the practice: read alone,
SOTA-040 still points a reader toward the pre-Chinchilla allocation.
