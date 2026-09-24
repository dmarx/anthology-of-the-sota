---
status: Proposed
promote_when: >-
  The decay measured in a trained model rather than derived under
  independence: per-layer `|xˡⁿ_{k+1} − xˡⁿ_k|` plotted against `k` for a real
  Pre-LN network at two depths, with the fitted exponent compared against
  `−1/2`. The cheapest version is a forward pass over any held checkpoint.
  What would NOT meet it: another paper deriving a decay under the same
  Gaussian-independence assumption, which is the assumption being questioned
  rather than evidence about it.
title: 'A Pre-LN residual stream''s per-layer change decays as one over root k, so deep blocks cannot refine the representation'
version: 1
tags:
- model-stability
- model-architecture
date: '2026-09-24'
source:
- LIT-tmpeqjkq
explains:
- SOTA-032
summary: >-
  Xie et al. (2023), [LIT-tmpeqjkq](../literature.d/LIT-tmpeqjkq.md) — in a Pre-LN transformer the residual
  stream accumulates unnormalised, so by block `k` it has variance `~k` and a
  single block's contribution is a `1/√k` share of it. The change in the
  normalised input between consecutive blocks decays as `O(1/√k)`, and adding
  a block to an `N−1` block model moves the output `O(1/√N)`. **The
  architecture's benefit and its cost are the same mechanism.**
---

# THEORY-tmpt3lzt: A Pre-LN residual stream's per-layer change decays as one over root k, so deep blocks cannot refine the representation

## Source

Xie et al. (2023), [LIT-tmpeqjkq](../literature.d/LIT-tmpeqjkq.md), §3.2.

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-032](../practices.d/SOTA-032.md) | put the normalisation inside the residual block, before the sublayer | the unnormalised residual stream is what bounds the gradients, and it is the same thing that makes later blocks' contributions a vanishing share of it |

## The account

In Pre-LN the stream accumulates without renormalisation: `xᵃ_{k+1} = xᵃ_k +
f_k(LN(xᵃ_k))`, so the model output is `y = LN(Σₖ xᶠ_k)`. Each block's output
is normalised exactly once, on the way out — which is precisely why nothing
is blocked in the forward or backward pass, and why the gradient problem
Post-LN has does not arise.

**The cost falls out of the same sum.** If the block outputs are independent
with variance `σ²`, then `xᵃ_k` has variance `(k−1)σ²`, so the normalisation
divides by `√(k−1)σ`. A single new block contributes `σ` to a quantity of
size `√k σ`. Writing the difference of consecutive normalised states,

    xˡⁿ_{k+1} − xˡⁿ_k ~ N(0, ω_k² I),   ω_k² = 2 / (√k (√(k−1) + √k))

and per coordinate `E[|·|] ~ O(1/√k)`. The same argument at the output gives
`O(1/√N)` for the effect of adding a block to an `N−1` block model.

So the inputs the later blocks see become increasingly alike, and **the
capacity of those blocks is not that it is unusable but that there is
progressively less for it to act on.**

## Why this is the interesting shape

**The benefit and the cost are not a trade-off between two mechanisms — they
are one mechanism described twice.** What makes Pre-LN trainable is that the
residual path is never renormalised, so gradients reach the early blocks
undamped. What makes deep Pre-LN blocks idle is that the residual path is
never renormalised, so the stream outgrows any single block's contribution.

That is why the fixes in the literature are rearrangements rather than
removals — sandwich and peri-layernorm placements, and this paper's own two
streams — and why `SOTA-032` is right to be a placement recommendation rather
than a law.

## Limitations, and they are the reason this is `Proposed`

- **The independence assumption is doing the work and is not tested.** The
  derivation assumes `xᶠ_k ~ N(0, σ²I)` independently across all `k`. In a
  trained network block outputs are neither Gaussian nor independent — later
  blocks read the stream the earlier ones wrote, which is the correlation
  most likely to change the exponent. The theorem is exact given the
  assumption; nothing here establishes the assumption.
- **It describes initialisation better than training.** Nothing in the
  argument involves learned weights, so it says what the architecture does to
  a freshly initialised network. Whether training reduces, preserves or
  amplifies the decay is open, and a model could in principle learn to
  compensate by scaling later blocks' outputs up.
- **`O(1/√k)` is slow.** At `k = 24` the per-layer change is about a fifth of
  its value at `k = 1`, not a thousandth. "Collapse" names the direction and
  overstates the speed, and the practical question — the depth at which it
  starts to cost accuracy — is not answered here.
- **The measurement that would settle it is cheap and nobody has published
  it**, which is what the `promote_when` asks for.
