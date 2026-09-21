---
status: Read
paper: LIT-tmpledv1
title: 'Late-phase weights'
version: 1
date: '2026-09-21'
summary: >-
  Reading it: three ablations constrain the recommendation more than the
  headline does. Starting at initialization fails outright, the fanciest
  variant is worse than doing nothing, and replicating every weight instead
  of a few is worse than replicating a few. All three are reported.
---

<!-- inactive-ok-file: SOTA-285 — Proposed, named in Connections as one of the
     record's two dropout practices because dropout is a baseline here that loses
     to doing nothing; nothing in this reading rests on it -->

<!-- inactive-ok-file: THEORY-045 — Proposed, and the connection to it is stated
     in the text as a reading rather than a result, which is why its unsettled
     status is not a problem for the sentence that names it -->

# NOTE-tmpdgwy1: Late-phase weights

## Contribution

An ensemble you never pay for at inference. Train `K` variants that differ
only in a handful of weights, share everything else, and average the handful
at the end. The cost during training is small because the replicated set is
small; the cost at test time is zero because there is one model again.

What is true afterwards that was not before: ensembling's generalization
benefit is at least partly available without ensembling's inference cost, and
the subset that carries it can be as small as BatchNorm's scale and shift.

## Key insight

**The replicated set is a knob, and smaller is better.** This is the
counterintuitive part and the paper tests it directly: a late-phase *full*
deep ensemble — same schedule, every weight replicated — performs worse than
replicating only BatchNorm parameters.

The reason offered is data efficiency: low-dimensional late-phase ensembles
"can be trained with as little data as a single model". Each copy sees the
same data and has few enough free parameters that it does not need more.

**And it has to be late.** The whole construction depends on the `K` copies
staying in one basin, because otherwise averaging them is meaningless. The
paper is explicit that mode coverage — normally the point of an ensemble —
"would preclude us from taking the averaged model". Perturbing at
initialization gives mode coverage, which is why `T₀ = 0` fails.

## Assumptions

- **A locally flat, connected solution region.** Cited to the dense-cluster
  and low-curvature-eigenspectrum literature. If this is false the averaging
  step is unjustified.
- **BatchNorm present**, for the default and best variant.
- **Layerwise-scaled perturbation noise** so one `σ` governs the network —
  though the CIFAR experiments set it to **zero**.
- **Base gradients accumulated across copies**, with a scale factor; the paper
  finds a large factor is tolerated and speeds learning.
- `K = 10` throughout the CIFAR work, with `T₀` and the schedule tuned once on
  CIFAR-100 and then held fixed.

## Key results

- CIFAR-10 WRN 28-10, 5 seeds: base 96.16, late-phase 96.46; under SWA 96.48 →
  **96.81**. Deep ensemble 96.91 at `K` times the cost.
- CIFAR-100 WRN 28-10: 81.35 → **82.87** (SGD), 82.46 → **83.06** (SWA).
  Deep ensemble 84.09.
- Hypernetwork variant on CIFAR-100: 81.55 (SGD) and 82.01 (SWA) — the second
  is below the base model's 82.46.
- `T₀ = 0` fails to reach the base model on both datasets.
- ImageNet fine-tuning, 5 seeds: ResNet-50 76.62 → 76.87, ResNet-152 78.37 →
  78.77, DenseNet-161 78.17 → 78.31, at standard deviations of 0.01–0.06.
- enwik8 LSTM, BPC: 1.695 base, 1.663 with rank-1 parameters alone, 1.633 with
  late-phase. Under SWA: 1.626, 1.616, **1.615**.
- Dropout is *below* the base model on CIFAR-10 WRN (96.02 vs 96.16).

## Claims

**Well supported:** that the method improves generalization on CIFAR and on
ImageNet fine-tuning, with five seeds and small standard deviations, and that
inference cost is unchanged.

**Supported and self-limiting:** the three ablations above. Each one narrows
what the method is, and the paper ran and reported all three rather than
letting the headline stand alone.

**Weaker than it looks in one place:** the LSTM result. Under SWA the gap
between base and late-phase is 0.011 BPC, against 0.062 without SWA. The
paper reports this as SWA "substantially improving all scores, with smaller
gains on the models with multiplicative weights", which is accurate and is
easy to read past.

## Method

Two-phase training with a shared base and `K` low-dimensional replicas,
averaged at the end; compared against SGD, SWA, dropout, MC-dropout,
BatchEnsemble and — as an explicit upper bound at unmatched cost — deep
ensembles. Five seeds on CIFAR and ImageNet.

## Concepts

*Base* and *late-phase* weights; the weight interaction function; perturbative
initialization within one basin; late-phase BatchNorm, rank-1, and
hypernetwork-embedding models; the base-gradient scale factor.

## Connections

- [SOTA-012](../practices.d/SOTA-012.md) — sharpness correlates with test error — is the record's
  existing version of the geometry this method *assumes*. Here flatness is not
  being measured, it is being relied on: `K` perturbed copies must stay in one
  basin or the average is meaningless.
- [THEORY-045](../theory.d/THEORY-045.md) measures how much of parameter space behaves like a trained
  network. This exploits the same region from the other end — it moves within
  it on purpose. Neither paper cites the other and the connection is a reading
  rather than a result.
- [SOTA-240](../practices.d/SOTA-240.md) and [SOTA-285](../practices.d/SOTA-285.md) are the record's dropout practices, and
  dropout is a baseline here that **loses to doing nothing** on CIFAR-10 WRN
  (96.02 vs 96.16). Consistent with `SOTA-240`'s conditional rather than
  against it: a WRN 28-10 on CIFAR-10 with standard augmentation is not
  obviously in the regime where dropout pays.
- SWA is named as the strong simple baseline and is **not in the record**,
  which this reading makes visible rather than fixes.

## Bearing on the record

One practice, `Proposed`, opening a family the anthology had no entry in.
The honest framing is comparative rather than absolute: this beats dropout and
BatchEnsemble, roughly matches or exceeds SWA depending on the problem, and
loses to a deep ensemble that costs `K` times more.

## Limitations

**2020, and vision-heavy.** WRN, PyramidNet, ResNet, DenseNet, plus one
1.56M-parameter LSTM sized so as not to overfit. Nothing at transformer scale
and nothing since.

**SWA is the comparison that matters and the answer depends on the problem.**
0.33–0.60 points of benefit over SWA on CIFAR; 0.011 BPC on enwik8. A reader
should try SWA first because it is simpler, and this note should not be read
as saying otherwise.

**Half the LSTM gain is a parameterization change**, not the ensemble: adding
rank-1 multiplicative parameters with no replication gets 1.695 → 1.663.

**BatchNorm dependence.** The best variant needs it; the variants for
architectures without it did worse.

**The flat-basin assumption is assumed, not checked.** No measurement confirms
the `K` copies stayed in one mode; the `T₀ = 0` failure is consistent with
them not doing so, which is evidence for the assumption's importance rather
than for its truth in the working case.

## Open questions

- Does it work on transformers, where BatchNorm is absent and LayerNorm's gain
  and bias are the obvious analogue? Nobody has tried it in the record's
  reach, and the natural substitute is exactly the kind of low-dimensional
  multiplicative parameter the method wants.
- Is this SWA with extra steps? The two overlap heavily on the LSTM and not on
  CIFAR, and no experiment isolates why.
- What sets `T₀`? Tuned once on CIFAR-100 and held fixed; the `T₀ = 0`
  failure says the choice matters and nothing says how to make it.
