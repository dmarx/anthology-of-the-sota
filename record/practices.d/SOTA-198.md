---
number: 198
status: Active
formerly:
- SOTA-tmptd4ui
consensus: emerging
consensus_note: >-
  The quantity is universally cited and the measurement is rarely performed —
  most practitioners inherit a batch size from a scaling law or a predecessor
  run rather than measuring their own.
title: 'Measure the gradient noise scale instead of sweeping batch size, and expect it to grow during the run'
version: 2
history:
# inactive-ok: SOTA-097 — Superseded in this same change; this entry says so
# inactive-ok: THEORY-026 — Proposed, and filed in this same contribution as the account of the correction
- version: 2
  date: '2026-09-20'
  note: >-
    SOTA-097, the prediction this practice was set against, is now
    Superseded: the batch-size scaling variable is the token budget, not
    compute (SOTA-258, THEORY-026). The section naming that
    disagreement now says it was resolved, and says why the instrument
    survives the resolution — a noise scale rising through a run is what
    growth in tokens seen looks like from inside it. The recommendation is
    unchanged.
tags:
- training-optimization
date: '2026-09-10'
source:
- LIT-017
- LIT-065
introduced_by:
- LIT-017
extends:
- SOTA-097
implementations:
- MT-NLG
---

<!-- inactive-ok-file: THEORY-013 — Rejected, and cited as what this
     practice does NOT rest on: the other thing called a noise scale, and
     why the record does not hold it. -->

# SOTA-198: Measure the gradient noise scale instead of sweeping batch size, and expect it to grow during the run
<!-- inactive-ok-file: THEORY-026 — Proposed, and filed in this same contribution as the account of why the exponent this practice was set against was wrong -->

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

## The other thing called a noise scale

[LIT-305](../literature.d/LIT-305.md) identifies an "SGD noise scale" `g = eps*N/B` two months before
[LIT-017](../literature.d/LIT-017.md), and this record briefly held the two as the same statistic reached by
two routes. They are not, and [LIT-017](../literature.d/LIT-017.md) says so: it cites [LIT-305](../literature.d/LIT-305.md) as predicting
"a dependence on dataset size", and adds *"which we do not observe"*.

[LIT-305](../literature.d/LIT-305.md)'s `g` is a property of the **configuration**
— learning rate, training set size, batch size — and you *set* it. `B_simple`
is a property of the **gradient distribution**, and you *measure* it. Holding
`g` fixed while `B` doubles means doubling the learning rate, so that quantity
is linear scaling with a derivation attached; this one tells you where the
batch stops buying speed. [THEORY-013](../theory.d/THEORY-013.md) is why the record does not hold the
first.

## Relation to the scaling-law exponent

<!-- inactive-ok-block: SOTA-097 — Superseded in this same change; this section exists to say what replaced it and why the instrument survives -->
[SOTA-097](SOTA-097.md) gave `B ∝ C^0.24` from Kaplan's equation 1.7 — a **prediction** from
compute budget, against this practice's **measurement** from the run in front
of you. It is now `Superseded`, and by the better outcome: the disagreement
was resolved rather than left open. The successor is [SOTA-258](SOTA-258.md), and the
scaling variable is the **token budget**, not compute — `B_crit ∝ D^0.46` from
two groups who did not coordinate.

**That vindicates the instrument rather than threatening it.** A gradient
noise scale rising through a run is precisely what "critical batch size grows
with tokens seen" looks like from inside the run, so the thing this practice
tells you to measure and the thing the new law predicts are the same
quantity, observed two ways. What was wrong was the *prediction* from
compute, not the measurement, and the reason to measure rather than predict
stands: the exponent is fitted on somebody's model family and the noise scale
is yours. [THEORY-026](../theory.d/THEORY-026.md) is the account.

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
