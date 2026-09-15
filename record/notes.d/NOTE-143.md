---
number: 143
status: Read
formerly:
- NOTE-tmprv9sv
paper: LIT-312
title: 'Exact Solution for On-Line Learning in Multilayer Neural Networks'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  The closed-form solution is: R(t) = R_∞ - (R_∞ - R_0) exp(-t / τ_sp) with
  specialization timescale τ_sp ∝ 1/η. Generalization error follows: ε_gen(t)
  ∝ (1 - R(t))² = C_∞ + A · exp(-t/τ_sp) + B · exp(-2t/τ_sp) This is a SUM OF
  EXPONENTIALS in ε, not a single exponential, because of the square.
---
# NOTE-143: Exact Solution for On-Line Learning in Multilayer Neural Networks

## Contribution

Solves in closed form the coupled ODEs for Q and R derived in the companion
PRE paper, demonstrating that the student-teacher overlap R(t) follows a
characteristic S-shaped trajectory: extended plateau at low R, sharp
transition, exponential approach to R_∞. The generalization error inherits
this shape as ε(t) ∝ (1 - R(t))². Learning rate η controls the overall
timescale (τ_sp ∝ 1/η) but not the fundamental shape. This is the paper that
establishes the S-curve as the universal learning curve for two-layer
teacher-student networks.

## Key insight

The closed-form solution is: R(t) = R_∞ - (R_∞ - R_0) exp(-t / τ_sp) with
specialization timescale τ_sp ∝ 1/η. Generalization error follows: ε_gen(t)
∝ (1 - R(t))² = C_∞ + A · exp(-t/τ_sp) + B · exp(-2t/τ_sp) This is a SUM OF
EXPONENTIALS in ε, not a single exponential, because of the square. The
curve has three regimes: (1) plateau: ε ≈ const for t << τ_sp (2)
transition: steep drop over ~3τ_sp (3) floor: ε → ε_∞ = C(1 - R_∞)²
exponentially η controls τ_sp (and therefore the speed of all three phases)
but not their relative durations — the shape is fixed by architecture and
data.

## Assumptions

- Thermodynamic limit d → ∞
- Online SGD (batch size 1)
- IID Gaussian inputs; erf activation (exact); smooth activations
  (approximate)
- Fixed teacher; constant learning rate η

## Key results

- **Closed-form solution for R(t).** R(t) = R_∞ - (R_∞ - R_0) · exp(-t /
  τ_sp) where τ_sp = 1 / (η · |F'(R*)|) and R* is the unstable fixed point
  of the ODE F(R) = dR/dt. For the realizable case R_∞ = 1; for unrealizable
  R_∞ < 1.
  *Holds when:* Symmetric subspace (all R_{jn} equal); erf activation
- **S-curve in generalization error.** ε_gen(t) = C(1 - R(t))² = C(1 - R_∞)²
  + 2C(1 - R_∞)(R_∞ - R_0) exp(-t/τ_sp) + C(R_∞ - R_0)² exp(-2t/τ_sp) This
  is a sum of two decaying exponentials plus a constant floor. It is NOT a
  single exponential. The ratio of the two rates is exactly 2 (from the
  square).
  *Holds when:* Realizable case; symmetric subspace
- **Learning rate controls timescale, not shape.** Doubling η halves τ_sp,
  uniformly compressing the time axis. The ratio (plateau duration) /
  (specialization duration) is invariant to η. To change the shape, one must
  change d, K, M, or the activation.
  *Holds when:* Moderate η range
- **Capability threshold.** Realizable (K ≥ M): R_∞ = 1, ε_gen → 0.
  Unrealizable (K < M): R_∞ < 1, persistent floor. Over-complete (K >> M):
  plateau is shorter because redundant students break symmetry faster.
  *Holds when:* General K, M

## Concepts

- **Specialization timescale τ_sp** — τ_sp ∝ 1/η; the characteristic time
  for the plateau-to-specialization transition. Most learning occurs within
  ~3τ_sp of this transition.
- **S-curve** — Three-phase MSE trajectory: plateau (nearly flat), steep
  drop (specialization), asymptote (floor). Cannot be fit by a single
  exponential or power law.
- **Sum-of-exponentials MSE** — Because ε ∝ (1-R)² and R decays
  exponentially, ε = C₀ + C₁·e^{-t/τ} + C₂·e^{-2t/τ} — two rates in fixed
  1:2 ratio. This is a key identifiable constraint.
- **Realizable vs unrealizable** — K ≥ M (student has capacity ≥ teacher):
  R_∞ = 1, perfect learning possible. K < M: irreducible residual error.

## Connections

**Builds on.**

- On-line learning in soft committee machines (Saad & Solla PRE 1995) —
  Solves the ODEs derived in that paper.

**Related.**

- Goldt et al. 2020 ([LIT-340](../literature.d/LIT-340.md)) — Extends S-curve analysis to ReLU and
  hidden manifold model; directly applicable to our setup.

## Recommendations

- **R1** — Fit experimental MSE curves to the sum-of-exponentials form: ε(t)
  = C_∞ + A · exp(-t/τ) + B · exp(-2t/τ) with the constraint B/A = (R_∞ -
  R_0) / (2(1 - R_∞)) — only 3 free parameters (C_∞, A, τ) if you impose the
  theoretical 1:2 rate ratio. If the 1:2 constraint fits poorly, the
  symmetric-subspace assumption is breaking down.
  *Topic:* curve fitting · *Strength:* strong · *When:* Two-layer teacher-
  student networks in realizable regime
- **R2** — The gossip penalty should be decomposed into: Δτ_sp — delay in
  specialization timescale (gossip averaging re-merges students, extending
  the plateau or restarting it) ΔC_∞ — increase in asymptotic floor (gossip
  introduces residual misalignment) These are separable in the S-curve fit
  and have distinct physical interpretations. **[not filed as a practice:
  specific to the project these readings were made for]**
  *Topic:* gossip penalty characterization · *Strength:* strong · *When:* MSE
  trajectories fit to the Saad-Solla curve family

## Bearing on the record

The Letter companion. Filed with it.

## Limitations

- Symmetric subspace solution (all R_{jn} equal); general case requires
  numerical ODE integration.
- Thermodynamic limit only.
- Erf activation; ReLU requires numerical ODE solution.
- Online SGD; minibatch introduces additional terms.

## Open questions

- Does the 1:2 rate ratio in the sum-of-exponentials hold approximately for
  ReLU and finite d?
- Can the gossip step be modeled as a perturbation to R that shifts the
  plateau start time?
- Is ΔC_∞ or Δτ the dominant term in the gossip penalty?
