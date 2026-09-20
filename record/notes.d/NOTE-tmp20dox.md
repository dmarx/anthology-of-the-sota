---
status: Read
paper: LIT-tmp5olz5
title: 'Power Lines'
version: 1
date: '2026-09-20'
summary: >-
  Scales the AdamW timescale rather than the weight decay, and finds it
  follows a power law in tokens-per-parameter with exponent about -0.52 over
  three orders of magnitude of compute. Optimal and critical batch size both
  scale as power laws in the token budget, not in compute.
---

# NOTE-tmp20dox: Power Lines
<!-- inactive-ok-file: SOTA-097 — Superseded in this same change, and this reading is the evidence -->
<!-- inactive-ok-file: SOTA-062 — Superseded in this same change, and named as contradicted by implication -->
<!-- inactive-ok-file: SOTA-255 — Proposed, and named because this reading says why the two do NOT compose -->

## Contribution

Turns three hyperparameters that are set by convention — weight decay,
optimal batch size, critical batch size — into quantities with fitted laws
and a stated independent variable. The weight-decay result works by scaling a
*derived* quantity, the AdamW timescale, rather than `λ` itself, and shows
that the quantity prior work proposed holding constant instead obeys a clean
power law in tokens-per-parameter. The batch-size results replace compute
with the token budget as the scaling variable, which is a change of the
question rather than a better answer to it, and they agree to within about 2%
with an independent measurement made under almost entirely different
conditions.

## Key insight

**The number everyone copies is a ratio with an implicit denominator.**
Weight decay only has meaning against a learning rate and a step count,
because what those three jointly determine is how much of training survives
into the final weights: `τ̃ = 1/(η λ S)` is the fraction of past updates
effectively averaged in. Setting `λ = 0.1` across scales is not holding a
policy fixed, it is letting the policy drift with whatever `η` and `S` happen
to be. Once the derived quantity is named, it turns out to scale — and to
scale smoothly enough to predict from small runs. The same shape of argument
recurs for batch size: `B ∝ C^0.24` is a real fit that describes a
projection, because `C` and `D` move together along the Chinchilla line and
only one of them is doing the work.

## Assumptions

- **muP throughout.** Base hyperparameters are tuned on a small proxy and
  transferred. The claim that `λ` rather than `η` is the thing to tune is
  stated *given* muP; without it the learning rate is not already handled.
- **Single-epoch pretraining.** The normalization `τ̃ = τ/S` is introduced on
  the explicit ground that "LLM pre-training only uses one epoch of data".
  Nothing here covers repeated data.
- **`τ̃` is computed at peak learning rate**, since it varies during decay.
  Two runs sharing a schedule shape and peak-LR `τ̃` end with matching EMA
  contributions even at different `S`.
- **TPP from 20 to 1280.** Below Chinchilla-optimal is outside the fit.
- GPT-2-like decoder with ALiBi and SwiGLU, SlimPajama, linear schedule with
  10% warmup decaying to zero, AdamW. Held-out evaluation on 1.1B tokens.
- The `C ≈ 6ND` approximation is used when converting between data and
  compute.

## Key results

- **Optimal normalized timescale**: `τ̃_opt ∝ TPP^(−0.52)`, `R² = 0.975`,
  bootstrapped 10th/90th percentiles on the exponent (−0.529, −0.507).
  Roughly 1.0 at 1 TPP, 0.01 at 1000 TPP. *Holds when:* muP, single epoch,
  within and somewhat beyond the fitted TPP range.
- **Generalization across compute**: four held-out points, including a
  3.3B-30TPP run requiring ~1000× the FLOPs of the nearest fitted point, sit
  on the law. Three orders of magnitude.
- **Tuning `λ` beats tuning `η`** — strictly better in 6 of 8 comparisons
  against a default `λ = 0.1` with swept learning rate. On a 111M 200TPP
  model: 2.810 default, 2.808 tuning `η`, 2.805 tuning `λ`. Small margins;
  the reported point is that tuning `λ` alone is sufficient.
- **`B_opt ∝ D^0.38`**, `R² = 0.984`, percentiles (0.367, 0.391).
- **`B_crit ∝ D^0.47`**, `R² = 0.940`, percentiles over all points
  (0.491, 0.526); against Zhang et al.'s independently measured 0.462.
- **The compute and loss power laws for `B` do not fit across the board.**
  Points at equal `D`, or equal TPP, fall on parallel lines — the signature of
  an underlying `D` dependence viewed through a confound.
- **Pareto frontier over time and compute**: with time modelled as
  `D/B` steps plus per-step cost, over-trained models sit on the frontier;
  under-trained models (below 20 TPP) are dominated in both time and FLOPs.
  Fitted optimal TPP of 20.6 at loss target 2.6.
- A `B_crit` estimation method that does not require fixing the training
  duration in advance, and so works under any schedule or optimizer.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The optimal AdamW timescale obeys a power law in tokens-per-parameter rather than staying constant | strong | hundreds of runs, `R²=0.975`, four held-out points at up to 1000× the fitting compute |
| C2 | Optimal batch size scales as a power law in the token budget, not in compute | strong | `R²=0.984`; the compute fit is shown to be a projection |
| C3 | Critical batch size scales as a power law in the token budget | strong | `R²=0.940`, and an independent group's exponent agrees to ~2% |
| C4 | Given muP, tuning weight decay is a better use of one sweep than tuning the learning rate | moderate | 6 of 8 cases, with margins of a few thousandths of a nat |
| C5 | Small over-trained models sit on the time-versus-compute Pareto frontier | moderate | derived from the fitted laws under one model of training time, at one loss target |

## Method

Train hundreds of muP models over a grid of model size `N`, token budget `D`,
batch size `B` and weight decay `λ`, at tokens-per-parameter ratios from 20 to
1280. For each `(N, D)` cell, compute the optimal `τ̃` over the `λ × B` grid,
then fit `τ̃_opt = a · TPP^b`. Recover `λ` from `τ̃`, the muP-adjusted learning
rate and the step count.

For batch size, fit `B`-specific power laws relating steps to a target loss,
derive the transition point where doubling `B` stops paying at the chosen
overhead threshold, and collect `(D, B_crit)` pairs across model sizes and
loss targets. Fit `B_crit = c · D^d`, and separately `B_opt` over the same
grid.

For the Pareto analysis, generate iso-loss contours in `(N, D)`, convert each
to a compute cost and a wall-clock estimate as a function of `B`, extend each
contour using the fitted `B_crit` law, and take the non-dominated points.

## Concepts

- **AdamW timescale `τ`** — `1/(η λ)` in steps; the horizon over which
  AdamW's weights average past updates, following from reading AdamW's weight
  sequence as an EMA of updates.
- **Normalized timescale `τ̃`** — `τ/S`, the *fraction* of training averaged
  into the final weights. The quantity that scales.
- **Tokens-per-parameter (TPP)** — `D/N`. Chinchilla-optimal is about 20; this
  study runs to 1280.
- **Optimal batch size `B_opt`** — the `B` minimizing loss at a given `(N, D)`.
- **Critical batch size `B_crit`** — the `B` past which reaching a target loss
  costs more than proportionally more data; a speed-against-efficiency
  boundary, not a quality one.

## Connections

Corrects Kaplan et al. ([LIT-028](../literature.d/LIT-028.md)) on the batch-size exponent, and inherits
the critical-batch-size quantity from the gradient-noise-scale line
([LIT-017](../literature.d/LIT-017.md)) while replacing its measurement procedure with one that
survives a decaying schedule.

Against Wang and Aitchison, whose proposal it takes up and then contradicts:
they showed the timescale measured in *epochs* is stable as batch or dataset
size change, on image tasks with multi-epoch training; here, in single-epoch
language-model pretraining across TPP, the normalized timescale is not
constant but power-law.

Downstream, the fitted law reproduces two previously published
hyperparameter-scaling relations as special cases, which is the kind of
consistency check a scaling law rarely gets.

## Recommendations

- **R1** — Set weight decay by targeting a normalized AdamW timescale from
  the fitted power law in tokens-per-parameter, rather than by inheriting a
  constant. *Topic:* regularization. *Status:* experimental. *Strength:*
  strong. *Applies when:* muP, single-epoch pretraining, TPP roughly 20–1280.
- **R2** — With muP already handling the learning rate, spend the available
  sweep on weight decay. *Topic:* hyperparameter tuning. *Status:*
  experimental. *Strength:* moderate. *Applies when:* the base learning rate
  was transferred from a proxy.
- **R3** — Scale batch size with the token budget, not with compute or model
  size. *Topic:* batch size. *Status:* experimental. *Strength:* strong.
  *Applies when:* any pretraining run where `B` is a free choice.
- **R4** — When trading training time against compute, prefer small
  over-trained models; they are faster per step and admit more parallelism
  because `B_crit` grows with `D`. *Topic:* budget allocation. *Status:*
  experimental. *Strength:* moderate. *Applies when:* wall-clock is a
  first-class objective alongside FLOPs.

## Bearing on the record

- **Retires [SOTA-097](../practices.d/SOTA-097.md).** `B ∝ C^0.24` is a fit to a projection. That
  practice's own body already flagged that the exponent had never been
  re-derived; it now has been, twice, and the variable is wrong.
- **Contradicts [SOTA-062](../practices.d/SOTA-062.md)** by implication and [LIT-tmphgpkf](../literature.d/LIT-tmphgpkf.md) directly:
  batch size does not track model size once the token budget is held fixed.
- **Should produce practices** for R1 and R3, and R4 is worth filing as the
  Pareto claim it is.
- **Does not compose with [SOTA-255](../practices.d/SOTA-255.md), and the record must say so.** That
  practice's conditions name exactly this gap — no rule for predicting
  optimal weight decay from the parameter-to-token ratio — and this supplies
  one, but in a disjoint regime: single-epoch, TPP ≥ 20, where Kim et al.
  epoch a fixed corpus at TPP well below 1. Composing them is unchecked.
- **Leaves [SOTA-198](../practices.d/SOTA-198.md) standing.** The gradient-noise-scale instrument is not
  disputed; what changes is the variable the quantity is claimed to track.

## Limitations

- One architecture family, one corpus, one schedule shape, one optimizer.
  The exponents are fitted; the paper does not claim they are universal
  constants.
- The largest trained model is 3.3B, and the compute-generalization evidence
  is four held-out points, not a second full sweep.
- The `λ`-versus-`η` result has margins of a few thousandths of a nat in the
  reported examples, which is a thin basis for "strictly superior" even at 6
  of 8.
- `B_crit` depends on the overhead threshold chosen to define it; the
  exponent is more robust than the level.
- The time model in the Pareto analysis is a specific one, and the paper shows
  that a different notion of time (pure step count) yields a visibly different
  frontier.
- Single-epoch only, which excludes the entire data-constrained regime the
  record has been filing into.

## Open questions

- Does the timescale law extrapolate below 20 TPP, and does it survive
  repeated data? That is the conversion that would let this and [SOTA-255](../practices.d/SOTA-255.md)
  be the same statement.
- Are the exponents architecture-dependent? The agreement with Zhang et al.
  on `B_crit` suggests not, for that one; nothing tests it for `τ̃`.
- What sets the level rather than the slope? Every law here is fitted with two
  free parameters and only the exponent has been checked across groups.
