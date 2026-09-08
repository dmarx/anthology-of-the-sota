---
status: Active
formerly:
- SOTA-tmpjwfcn
consensus: emerging
consensus_note: >-
  One originating laboratory and one outside adopter at frontier scale — Kimi
  K3 at 2.8T calls its expert layer "Stable LatentMoE" and credits this
  paper; NVIDIA's own Nemotron-3 Super and Ultra use it too, which is the
  same group. Not `converged`: two adopters is not the field, and the
  bandwidth-bound premise the design rests on is a claim about serving
  regimes that other labs may not share.
title: "Keep the routed experts' weights in a down-projected latent space and spend the saved bandwidth on more of them"
version: 1
tags:
- model-architecture
date: '2026-09-08'
published: '2026-01-01'
source:
- LIT-196
extends:
- SOTA-150
implementations:
- 'Kimi K3'
- 'Nemotron-3 Super'
- 'Nemotron-3 Ultra'
summary: >-
  Elango et al. (2026), [LIT-196](../literature.d/LIT-196.md) — down-project the token before the routed
  experts and keep their weights in that latent space, dispatching and
  aggregating there too, while routing and the shared experts stay at full
  width. Communication volume and weight-loading bandwidth both fall by
  d/d_l, and the saved budget buys more experts and more active per token.
---

# SOTA-180: Keep the routed experts' weights in a down-projected latent space and spend the saved bandwidth on more of them

## Source

Elango et al. (2026), [LIT-196](../literature.d/LIT-196.md) — [ARXIV-2601.18089](https://arxiv.org/abs/2601.18089).

[SOTA-150](SOTA-150.md) answers *whether* the feed-forward layers should be sparse. This
answers *where the width should be*, and the premise underneath it is the
part worth arguing about first.

**Judge a sparse design on two axes, not one.** Accuracy per FLOP is the
usual one. Accuracy per *parameter* is the second, standing in for memory
footprint, bandwidth, routing communication and sharding overhead — and a
roofline analysis of serving a 235B-A22B model shows why it is the binding
one: at latency-critical batch sizes the per-expert token count is small, so
arithmetic intensity is low and expert computation sits in the
**bandwidth-bound** regime. Adding FLOPs there is free. Moving weights is
not. Optimising accuracy per FLOP alone optimises for the case that is not
the constraint.

## What to build

- **Down-project the token** into a latent space of width d_l before the
  routed experts, and keep the routed experts' weights in that space.
  Dispatch and aggregation happen there too.
- **Leave routing and the shared experts at the full hidden width d.** Those
  are not where the bottlenecks are, and shrinking them costs quality for no
  bandwidth.
- Communication volume and weight-loading bandwidth both fall by **d/d_l**.

**And then spend the saving, which is the part that is not obvious.** This is
not "make the experts smaller". The freed budget buys *more* experts and more
active per token, on the design principle that scaling the pool and the
active count together raises expert diversity faster than it raises cost in
the latent space — so quality per parameter goes up rather than down.

## What it is under, in this record

Kimi K3 calls its expert layer "Stable LatentMoE" and credits this paper.
That is what makes **896 routed experts with 16 active** affordable at 2.8T,
and K3's three additions — an RMSNorm before the up-projection, SiTU-GLU,
Quantile Balancing — are all repairs to failure modes the resulting 56×
sparsity brings on. Read the K3 material without this practice and the base
those repairs are stabilising is missing.

## Conditions

Design-space exploration to 95B parameters over a 1T-token horizon, with
ablations, scaling studies and a projected trillion-parameter serving
analysis — but the deployments are one originating lab plus one outside
adopter, and the argument turns on a serving regime. A throughput-oriented
deployment at large batch is the case the paper says the field was already
optimising for, and there the second axis binds less.

## Known implementations

- Kimi K3 at 2.8T (as "Stable LatentMoE"); NVIDIA's Nemotron-3 Super and
  Ultra.
