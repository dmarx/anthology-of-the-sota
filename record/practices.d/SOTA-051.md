---
number: 51
status: 'Active'
title: 'Initialize final layer weights near zero'
version: 1
tags:
- model-stability
date: '2026-08-24'
published: '2020-03-01'
source:
- LIT-047
summary: >-
  Bachlechner et al. (2020), [LIT-047](../literature.d/LIT-047.md) — [ARXIV-2003.04887](https://arxiv.org/abs/2003.04887).
---

# SOTA-051: Initialize final layer weights near zero

## Source

Bachlechner et al. (2020), [LIT-047](../literature.d/LIT-047.md) — [ARXIV-2003.04887](https://arxiv.org/abs/2003.04887).

## Zero, not small

[LIT-047](../literature.d/LIT-047.md)'s intervention is one scalar per layer multiplying the residual
branch, initialised to **zero** — so at initialisation every block is exactly
the identity and the signal passes through an arbitrarily deep stack with no
attenuation and no amplification. Training then raises the scalars from zero
as the blocks earn their contribution.

That is stronger than "near zero" and the difference is the point: an exact
identity at initialisation means depth costs nothing at step one, so the
warmup and careful initialisation that deep stacks otherwise need become
unnecessary rather than merely easier.

## The same instinct, three places in this record

Start the residual branches quiet and let training turn them up:
[SOTA-060](SOTA-060.md)'s depth-scaled output projections, [SOTA-025](SOTA-025.md)'s slightly-shrunk
LayerNorm scale, and this. ReZero is the limiting case — the branch starts at
exactly nothing.

The cost is a slower start: a block contributing zero learns only through the
gradient that reaches its scalar, so the early steps do less than they
otherwise would. In practice this is small against the depth it buys, and it
is the reason the technique is usually described as trading a little early
progress for the ability to train deeper at all.

Modern large models mostly use the scaled-initialisation form rather than a
learned gate, so this practice is best read as the clearest statement of a
principle the record applies in weaker versions elsewhere.
