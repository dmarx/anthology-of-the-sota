---
status: Active
title: 'An update smaller than the lattice spacing is not merely rounded away — it is cancelled exactly, and carrying the remainder makes the discrete path shadow the continuous one within half a grid cell'
version: 1
tags:
- numerics-and-precision
- training-optimization
date: '2026-09-21'
source:
- LIT-tmp14peb
explains:
- SOTA-tmpjdocv
summary: >-
  Xu et al. (2026), [LIT-tmp14peb](../literature.d/LIT-tmp14peb.md) §5 — decompose rounding as identity
  plus error and expand the trajectory: when every step falls short of the
  grid, the accumulated quantization loss cancels the accumulated ideal update
  term for term and the weights never move. Stochastic rounding replaces
  stagnation with a random walk whose variance grows in `T`. Carrying the
  remainder bounds the deviation from the ideal path at `Δ/2` for all `T`.
---

<!-- inactive-ok-file: SOTA-tmpjdocv — Proposed, and the practice this account
     explains; the document's point is that a sound explanation does not promote
     the practice, so its unsettled status is the thing being said -->

<!-- inactive-ok-file: ADR-031 — Proposed, cited for the practice/explanation
     split that lets this account be Active while the practice stays Proposed -->

# THEORY-tmp8xhjh: An update smaller than the lattice spacing is not merely rounded away — it is cancelled exactly, and carrying the remainder makes the discrete path shadow the continuous one within half a grid cell

## Source

Xu, Miikkulainen and Qiu (2026), [LIT-tmp14peb](../literature.d/LIT-tmp14peb.md) §5 — read as
[NOTE-tmp4sz3x](../notes.d/NOTE-tmp4sz3x.md).

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-tmpjdocv](../practices.d/SOTA-tmpjdocv.md) | bank the sub-lattice part of each update | not a refinement but the difference between moving and not moving, with a bound on how far the discrete path can drift |

## The account

Write the quantizer as identity plus an error term, `Q(x) = x + ε(x)`, and
expand a `T`-step trajectory of `w ← Q(w + η ĝ)`. The result splits into the
ideal continuous update summed over `T` steps and an accumulated quantization
loss summed over the same steps.

**Deterministic rounding gives exact cancellation.** If `‖η ĝ‖ < Δ/2` at every
step — the ordinary case in fine-tuning, where updates are small by design —
then `Q(w + η ĝ) = w`, so `ε` equals `−η ĝ` exactly. The two sums annihilate
term for term and `w_T = w_0`. This is stronger than "the update is lost to
rounding": there is no slow drift, no eventual accumulation, no threshold
that is eventually crossed. The optimizer is stationary.

**Stochastic rounding trades stagnation for a random walk.** Round
probabilistically and the estimator becomes unbiased, which is what a
zeroth-order method wants. But `ε` is now a zero-mean noise term whose scale
is set by `Δ`, and it accumulates as a random walk: deviation grows like
`√T`, producing a noise floor proportional to the grid spacing. Unbiasedness
is necessary and is not sufficient — the failure has moved from the estimator
to the *application* of the estimate.

**Carrying the remainder converts both into a bound.** Define virtual
continuous parameters `w̃ = w + e`, where `e` is the retained residual. The
update rules make `w̃` evolve by exactly the unconstrained high-precision
ascent — the discretization has been moved out of the dynamics and into the
readout. The physical weights are then the rounding of that path, so

    ‖w − w̃‖ ≤ Δ/2

for every `T`. Not growing in `T`, not scaled by the number of steps: one
final residual, bounded by the grid. The quantized model tracks the
high-precision trajectory it would have followed, lagging by less than one
grid cell and discharging that lag whenever the accumulated signal crosses a
boundary.

## Why `Active`

Because it is a derivation rather than a conjecture, and the device it
describes is not new evidence — error feedback on a coarse channel has
carried 1-bit SGD and communication-efficient training for years. What this
adds is the observation that a model's *parameter lattice* is the same kind
of coarse channel as a gradient wire, with the same failure and the same fix.
That transfer is argued, checkable, and does not depend on the source's
experiments.

The status is about the account, not about the size of the practical win.
[SOTA-tmpjdocv](../practices.d/SOTA-tmpjdocv.md) is `Proposed` and `unreplicated`, and stays there: an
explanation being sound is not evidence that the method is worth adopting,
which is the split [ADR-031](../decisions.d/ADR-031.md) exists to keep visible.

## What this does not say

**It does not say the empirical gap is caused by this.** The source infers
from the mechanism to its numbers — QES beats a stateless quantized
zeroth-order baseline, therefore the accumulator is why. No ablation removes
the accumulator while holding everything else fixed, so the attribution is an
inference and the derivation does not supply it.

**It says nothing specific to evolution strategies.** The cancellation is
about rounding an update, not about how the update was estimated. The same
argument covers a first-order optimizer stepping on a quantized lattice, and
the record holds no result either way for that case — which is the most
obvious test this account invites.

**The `Δ/2` bound is per-parameter and instantaneous.** It bounds the distance
from the ideal trajectory at each step. It does not bound the difference in
final *loss*, and it does not say the ideal trajectory was any good.

**The bound assumes the residual is kept exactly.** [SOTA-tmpjdocv](../practices.d/SOTA-tmpjdocv.md)'s
memory-saving form rebuilds it from a truncated history, so the guarantee
holds for the oracle variant and approximately for the practical one — and
the source's own decay ablation shows the approximation failing loudly when
the decay is made aggressive.
