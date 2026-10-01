---
number: 52
status: 'Active'
title: 'Use smaller variance for deep networks'
version: 1
tags:
- model-stability
date: '2026-08-24'
source:
- LIT-084
introduced_by:
- LIT-084
summary: >-
  Wang et al. (2022), [LIT-084](../literature.d/LIT-084.md) — [ARXIV-2203.00555](https://arxiv.org/abs/2203.00555).
---

# SOTA-052: Use smaller variance for deep networks

## Source

Wang et al. (2022), [LIT-084](../literature.d/LIT-084.md) — [ARXIV-2203.00555](https://arxiv.org/abs/2203.00555).

## The dependence the title leaves out

Initialising weights with the usual fan-in-scaled variance keeps activations
stable through one layer, and a deep stack compounds whatever error remains:
a variance slightly above unity per layer grows exponentially in depth, and
slightly below shrinks to nothing. So the correction depth requires is a
scaling *by depth*, not merely "smaller".

The practice comes from [LIT-084](../literature.d/LIT-084.md) (DeepNet), which derives that scaling from a
bound on the size of the model update rather than sweeping for it. Its
residual is `LayerNorm(x·α + f(x))`, and the feed-forward, value and output
projections are Xavier-initialised with gain `β`, which for a decoder-only
model is `(8M)^(−1/4)` while `α = (2M)^(1/4)` grows. The query and key
projections are deliberately left at gain 1, which "smaller variance" does not
say. With it the paper trained 1,000 layers, and a 200-layer 3.2B model beat a
48-layer 12B model by 5 BLEU on translation.

The record holds the specific forms elsewhere — [SOTA-060](SOTA-060.md)'s depth-scaled output
projections, [SOTA-051](SOTA-051.md)'s exactly-zero residual scalar — and this practice is the
general statement they instantiate.

## Why the general statement is worth keeping anyway

Because the specific forms are architecture-dependent and the principle is
not. A new block design gets the same question — how much of this branch
should reach the residual stream at initialisation — and the answer is always
some function of depth.

What the practice cannot supply is the function. "Smaller variance for deep
networks" gives a direction and no rate, and the record's own instances differ
in theirs. A reader with a residual architecture should take the depth-scaled
form from [SOTA-060](SOTA-060.md) or [SOTA-051](SOTA-051.md); a reader with something else has a principle
and a measurement to make.
