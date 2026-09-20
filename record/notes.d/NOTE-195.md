---
number: 195
status: Read
formerly:
- NOTE-tmpm8s5j
paper: LIT-445
title: 'How Does Critical Batch Size Scale in Pre-training?'
version: 1
date: '2026-09-20'
summary: >-
  Decouples model size from data size — which every prior batch-size study
  had scaled together — and finds critical batch size tracks the token
  budget and is nearly flat in model size. Supported by a muP argument for
  the model half and a least-squares analysis for the data half.
---

# NOTE-195: How Does Critical Batch Size Scale in Pre-training?
<!-- inactive-ok-file: SOTA-097 — Superseded in this same change, and this reading is half the evidence -->
<!-- inactive-ok-file: SOTA-062 — Superseded in this same change, and this reading is the experiment that retires it -->

## Contribution

Identifies that the literature's claim "critical batch size grows with scale"
was measured under Chinchilla scaling, where model and data grow together, and
so could not attribute the growth to either. Holds each fixed in turn and
finds the dependence is on data. Supplies a measurement protocol that removes
the need to commit to a training duration before measuring — the practical
obstacle that had made the quantity awkward under decaying schedules — and
two theoretical arguments that predict the split it measures.

## Key insight

**Critical batch size is a property of the optimization problem's data, not of
the model solving it.** The intuition everyone carries — bigger models can
absorb bigger batches — survives as an observation and fails as a causal
claim, because bigger models in practice see more tokens. Under muP there is
a width past which more width does not raise the batch a step can usefully
absorb; the gradient signal-to-noise that sets the ceiling is determined by
how much data the model has already seen. The practical payoff is directly
useful and slightly surprising: **scaling up your token budget hands you extra
data parallelism for free**, whereas scaling up your model does not.

## Assumptions

- **Critical batch size is defined against a target validation loss**, as the
  batch size at which doubling incurs a stated overhead relative to linear
  step-count scaling. The level depends on the overhead threshold chosen; the
  scaling does not.
- **Constant learning rate plus exponential weight averaging** replaces a
  decaying schedule, on the ground that a decay schedule requires fixing the
  horizon in advance. Shown to reach comparable loss to cosine, WSD and
  schedule-free.
- **Fully synchronous data parallelism**, with wall-clock abstracted to
  optimizer-step count. Communication cost is not modelled.
- Gradient accumulation simulates large global batches, so "batch size" here
  is the effective global batch, not what fits on a device.
- **muP with a 151M proxy**; context length 512; C4; Adam.
- The theory is for mini-batch SGD on least squares under power-law source and
  capacity conditions — not for Adam on a transformer.

## Key results

- **CBS scales with data size**: fitted power law in `D` with exponent
  ≈ 0.462. *Holds when:* 85M–1.2B, C4, the stated CBS definition.
- **CBS is weakly dependent on model size at fixed data.** Curves for
  different model sizes trained on the same token count overlap
  substantially; the fitted law in `N` at fixed `D` is nearly flat.
- **Depth and width raise CBS about equally** under Chinchilla scaling —
  consistent with both being proxies for the data scaled alongside them.
- **Theorem (informal, muP)** — past a certain width, increasing width at
  fixed data size does not further increase CBS.
- **Theorem (informal, least squares)** — for mini-batch SGD under power-law
  source and capacity conditions, the CBS that reaches minimal excess risk at
  fastest serial runtime grows as `n^a`; in the variance-dominated regime `a`
  takes an explicit value, so CBS grows with sample count.
- **Constant + EWA matches cosine, WSD and schedule-free** on final loss while
  allowing training to continue past any preset horizon, and is *more* helpful
  in the large-batch regime.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Critical batch size scales primarily with data size | strong | controlled sweeps holding each of `N` and `D` fixed, 85M–1.2B, plus an independent group's matching exponent |
| C2 | Critical batch size is nearly independent of model size at fixed data | moderate | overlapping curves and a weak fitted law; "weakly dependent" is not "independent", and the range is 85M–1.2B |
| C3 | The split follows from muP for the model half and from least-squares analysis for the data half | moderate | two informal theorems under assumptions well away from the empirical setting |
| C4 | Constant learning rate plus EWA is a sound substitute for a decay schedule when the horizon must stay open | moderate | matched final loss against three schedules at this scale |

## Method

Fix a target validation loss. For each batch size, measure steps to reach it.
The point where doubling the batch stops halving the step count — within a
stated overhead — is the critical batch size for that configuration.

Do this in three arrangements: Chinchilla scaling with `N` and `D` growing
together; `D` fixed while `N` varies; `N` fixed while `D` varies. Fit scaling
laws in each, which decouples the two dependences that the first arrangement
confounds.

Replace the learning-rate schedule with a constant rate plus an exponential
weight average, evaluating the averaged weights. This allows a run to be
resumed from a checkpoint until the target loss is reached, rather than
requiring the total duration to be chosen before the run that measures it.

## Concepts

- **Critical batch size (CBS)** — here, the batch size at which the step-count
  reduction from doubling falls below linear by a stated overhead, measured
  against a target loss. Distinct from optimal batch size, which minimizes
  loss rather than time.
- **Decoupling** — measuring the dependence on one of `N`, `D` while holding
  the other fixed, as against the Chinchilla-scaled sweep where they move
  together.
- **Exponential weight averaging (EWA)** — a running average of weights used
  for evaluation, `Polyak`-style, standing in for learning-rate decay.

## Connections

Corrects Kaplan et al. ([LIT-028](../literature.d/LIT-028.md)), whose `B_crit(L)` is a function of loss and
whose compute exponent the record carries, and departs from the
gradient-noise-scale framing of [LIT-017](../literature.d/LIT-017.md) by making the token budget rather
than the run's internal statistics the reported variable.

Converges with [LIT-443](../literature.d/LIT-443.md), which reaches `0.47` where this reaches
`0.462`, from a different architecture, dataset, context length,
parameterization, schedule and tuning strategy. Neither is a replication of
the other's protocol; the agreement is between two independent ways of asking.

The EWA substitution connects to the weight-averaging literature, and the
paper notes it trades memory for optimization efficiency most usefully exactly
where this study needs it — the large-batch regime.

## Recommendations

- **R1** — Expect available data parallelism to grow with the token budget,
  not with model size; plan the parallelism strategy from `D`. *Topic:*
  batch size. *Status:* experimental. *Strength:* strong. *Applies when:*
  synchronous data-parallel pretraining.
- **R2** — When measuring anything defined against a target loss, use a
  constant learning rate with weight averaging rather than a decay schedule,
  so the horizon does not have to be guessed in advance. *Topic:*
  experimental method. *Status:* experimental. *Strength:* moderate.
  *Applies when:* the quantity of interest is steps-to-loss.
- **R3** — Do not infer a batch-size rule from a sweep in which model and data
  scaled together. *Topic:* evaluation. *Status:* standard. *Strength:*
  strong. *Applies when:* reading any scaling result along the Chinchilla
  line.

## Bearing on the record

- **Retires [SOTA-062](../practices.d/SOTA-062.md)**, whose claim is that batch size scales with model
  size sub-linearly. That practice's body says a reader with a measurement
  should prefer it; this is the measurement, and the model-size dependence
  very nearly disappears.
- **Half of the evidence retiring [SOTA-097](../practices.d/SOTA-097.md)**, jointly with [LIT-443](../literature.d/LIT-443.md).
- **Should produce a theory document.** The muP argument plus the
  least-squares result is an account of *why* the split falls where it does,
  which is separable from the recommendation and is what `THEORY` is for.
- **Does not dispute [SOTA-198](../practices.d/SOTA-198.md)'s instrument.** Gradient noise scale growing
  through a run is consistent with CBS growing in tokens seen; what this
  changes is the reported variable, not the measurement.
- **R3 is a methodological warning the record has no home for** and is worth
  remembering next time a scaling claim arrives from a Chinchilla-line sweep.

## Limitations

- 85M to 1.2B parameters, context length 512, one corpus. "Weakly dependent
  on model size" is a statement about that range.
- The theory is for SGD on least squares; the experiments are Adam on
  transformers. The two are offered as consistent, not as one deriving the
  other.
- CBS is defined against an overhead threshold, so the absolute numbers are
  convention-dependent even though the exponent is not.
- Wall-clock is abstracted to step count and communication cost is not
  modelled — which is exactly where the practical value of extra parallelism
  would be spent.
- No frontier-scale check.

## Open questions

- Does the near-independence from model size survive past 1.2B, or is there a
  width at which it reappears?
- What happens under repeated data? Every result here is single-pass, and the
  record's data-constrained cluster is not.
- Does the exponent depend on the data distribution? Two groups on two corpora
  agree, which is suggestive and is two points.
