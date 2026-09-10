---
status: Active
consensus: emerging
consensus_note: >-
  The quantity is universally cited and the measurement is rarely performed —
  most practitioners inherit a batch size from a scaling law or a predecessor
  run rather than measuring their own.
title: 'Measure the gradient noise scale instead of sweeping batch size, and expect it to grow during the run'
version: 1
tags:
- training-optimization
date: '2026-09-10'
source:
- LIT-017
- LIT-065
extends:
- SOTA-097
implementations:
- MT-NLG
---

# SOTA-tmptd4ui: Measure the gradient noise scale instead of sweeping batch size, and expect it to grow during the run

## Source

McCandlish et al. (2018), [LIT-017](../literature.d/LIT-017.md) — the paper that defines the gradient noise
scale and, with it, critical batch size.

Smith et al. (2022), [LIT-065](../literature.d/LIT-065.md) — MT-NLG, which ramps its batch size in
production for exactly the reason `LIT-017` predicts.

## The quantity

    B_simple = tr(Σ) / |G|²

— the summed per-component gradient variance over the squared gradient norm.
It needs no Hessian, and `LIT-017` gives a way to compute it with negligible
overhead inside an ordinary data-parallel step, because the per-worker gradients
already supply the variance.

The full form is `B_noise = tr(HΣ)/(GᵀHG)`; the two differ by a small constant
factor in practice.

## What it buys

Per-step progress depends on batch size **only** through `1/(1 + B_noise/B)`.
Below the noise scale, doubling the batch nearly doubles progress; above it,
doubling buys almost nothing. **At `B = B_noise` exactly, training speed is 50%
of the maximum** — the noise scale is the knee, not the ceiling.

Verified across eight tasks in supervised learning, RL and generative modelling,
and **independent of dataset size**, which is what lets it transfer to a new
domain rather than being refitted there.

## The second half: it moves

**The noise scale rises as the loss falls.** The batch size that was right at
the start of a run is too small later, and MT-NLG acts on this: batch size
**ramped from 32 to 1920 in increments of 32 over the first 12B tokens**, at
530B parameters.

Neither paper cites the other. `LIT-065` describes the ramp as an operational
choice; `LIT-017` is the reason it works.

## Relation to the scaling-law exponent

[SOTA-097](SOTA-097.md) gives `B ∝ C^0.24` from Kaplan's equation 1.7 — a **prediction** from
compute budget. This is a **measurement** from the run in front of you. They
answer the same question with different evidence and disagreeing is
informative: the exponent is fitted on a model family, and the noise scale is
yours.

`LIT-065` also supplies the systems consequence: the batch ceiling is why data
parallelism runs out, and therefore why model parallelism exists at all. At
~4000 GPUs, pure data parallelism "would only allow for a batch size of 1 per
GPU".

## Conditions

Order-of-magnitude prediction — `LIT-017` says so plainly. It tells you whether
10³ or 10⁵ is right, not whether 8K beats 16K.

Derived under a local quadratic model the authors call unfounded, and justified
by the empirical fit; derived for SGD and applied unmodified to momentum, Adam
and RMSProp, where it still works. 2018 scales, and the preconditioned variant
(dividing by Adam's second moment) is reported as "mixed results" — awkward,
since everything is trained with Adam now.

## Known implementations

- MT-NLG's 32 → 1920 batch ramp
