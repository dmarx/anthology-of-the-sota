---
status: Read
paper: LIT-tmpnvhj9
title: 'Broken Neural Scaling Laws'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  A single power law ε(t) = C_∞ + b·t^{-c} fails when the curve has two
  regimes (steep early, shallow late — or vice versa).
---
# NOTE-tmpzzq0c: Broken Neural Scaling Laws

## Contribution

Identifies and formalizes the empirical observation that neural network
learning curves often exhibit two distinct scaling regimes separated by a
kink or inflection point, causing single power laws (Kaplan et al.) to fail.
Proposes the Broken Neural Scaling Law (BNSL) functional form, a smooth
composite that interpolates between two power-law regimes and reduces to the
standard power law + floor when the break is absent. Demonstrates improved
fits across vision, language, and RL benchmarks. Directly relevant to
training runs where warm-start conditions (e.g. gossip-initialized weights)
produce kinks in the MSE trajectory.

## Key insight

A single power law ε(t) = C_∞ + b·t^{-c} fails when the curve has two
regimes (steep early, shallow late — or vice versa). BNSL uses a smooth
break:

ε(t) = C_∞ + b · t^{-c₀} · (1 + (t/d₁)^{1/f₁})^{-c₁·f₁}

Parameters: C_∞ — irreducible floor (same as Kaplan L_∞) b — amplitude of
the decay c₀ — early-regime exponent (before the break) d₁ — break point
(step count where regime transition occurs) f₁ — sharpness of the break (f₁
→ 0 gives an abrupt step; f₁ large = smooth) c₁ — late-regime exponent
adjustment (net late exponent ≈ c₀ + c₁)

Limiting cases: - If (t/d₁) → 0 for all t: reduces to ε(t) = C_∞ + b·t^{-c₀}
(standard power law) - If (t/d₁) → ∞ for all t: reduces to ε(t) = C_∞ +
b·d₁^{c₁}·t^{-(c₀+c₁)} - Smooth crossover between the two exponents at t ≈
d₁

The kink location d₁ is interpretable: it marks the exhaustion of the "easy"
structure in the data (e.g., the transition from curriculum learning to hard
examples, or from warm-start benefit to diminishing returns).

## Assumptions

- Empirical curve-fitting framework; not derived from first principles
- Assumes the learning curve is monotonically non-increasing in t
- Fits are over a scalar metric (loss, accuracy, MSE) vs a scalar resource
  (steps, samples, compute)
- Break is assumed to be a single-kink; multiple kinks require chaining BNSL
  segments

## Key results

- **BNSL functional form.** ε(t) = C_∞ + b · t^{-c₀} · (1 +
  (t/d₁)^{1/f₁})^{-c₁·f₁} For t << d₁: ε(t) ≈ C_∞ + b·t^{-c₀} (early
  exponent c₀) For t >> d₁: ε(t) ≈ C_∞ + b·d₁^{c₁}·t^{-(c₀+c₁)} (late
  exponent c₀+c₁) At t = d₁: smooth crossover; f₁ controls how sharp the
  kink is. Six free parameters: {C_∞, b, c₀, d₁, f₁, c₁}.
  *Holds when:* Six parameters; reduces to 3 when d₁ → ∞ (single power law)
- **Reduction to Kaplan power-law + floor.** When d₁ → ∞ (break point beyond
  observed range), the BNSL term (1 + (t/d₁)^{1/f₁})^{-c₁·f₁} → 1, and: ε(t)
  = C_∞ + b·t^{-c₀} which is exactly Kaplan et al.'s L(S) = L_∞ + (S_c/S)^α
  with c₀ = α and b = S_c^α.
  *Holds when:* Single-regime limit
- **Chained BNSL for multiple breaks.** For K kinks, the BNSL can be
  chained: the output of one BNSL segment feeds as the input resource to the
  next. This handles staircase-like learning curves (e.g., emergent
  abilities in large LMs that appear as discontinuous jumps).
  *Holds when:* K-break generalization
- **Better fit than single power law on benchmark tasks.** BNSL achieves
  significantly lower residuals than Kaplan power law + floor across vision
  transformers (ImageNet), language models, and RL benchmarks, particularly
  for runs that exhibit early rapid improvement followed by slower scaling.
  *Holds when:* Empirical; no theoretical guarantee

## Concepts

- **Break point d₁** — The step count at which the dominant scaling regime
  transitions from early exponent c₀ to late exponent c₀+c₁. Interpretable
  as the exhaustion of easy structure or a phase transition in the loss
  landscape.
- **Break sharpness f₁** — Controls how abrupt the regime transition is. f₁
  → 0 gives a step-function break (two distinct power laws). f₁ large gives
  a smooth crossover. In practice, f₁ is fit from data.
- **Early exponent c₀ / Late exponent c₀+c₁** — The two scaling exponents.
  c₀ governs early training; c₀+c₁ governs late training. c₁ > 0 means
  learning slows down; c₁ < 0 means it speeds up (rare).
- **Warm-start kink** — In our gossip setting: when a node is re-initialized
  or averaged with neighbors, the MSE trajectory may show a kink — rapid
  initial adjustment followed by a slower convergence phase. This is a BNSL
  break with d₁ near the gossip event time.

## Connections

**Builds on.**

- Kaplan et al. 2020 ([LIT-028](../literature.d/LIT-028.md)) — BNSL generalizes Kaplan's power-law + floor
  by adding a smooth break between two power-law regimes. Kaplan is the d₁ →
  ∞ special case of BNSL.

**Related.**

- Bordelon, Canatar, Pehlevan 2020 ([LIT-tmpq3y0z](../literature.d/LIT-tmpq3y0z.md)) — Bordelon et al. provide
  the spectral theory for each BNSL segment: each regime has a different
  effective β (eigenvalue decay), giving different α = β/(1+β). A kink in
  the learning curve may signal a change in the effective spectrum seen by
  the optimizer.
- Saad & Solla 1995 — The Saad-Solla S-curve (plateau + steep drop + floor)
  is a different type of kink — exponential, not power-law. In regimes where
  both apply, the BNSL break at d₁ may correspond to the Saad-Solla
  specialization transition.

## Recommendations

- **R1** — When fitting MSE curves from gossip experiments that show visible
  kinks (e.g., after a gossip averaging event or after warm-start
  initialization), use BNSL rather than a single power law: ε(t) = C_∞ + b ·
  t^{-c₀} · (1 + (t/d₁)^{1/f₁})^{-c₁·f₁} Fix d₁ at the known gossip event
  time if applicable (reduces free parameters from 6 to 5). Compare AIC/BIC
  against the 3-parameter Kaplan fit. **[not filed as a practice: specific
  to the project these readings were made for]**
  *Topic:* curve fitting · *Strength:* strong · *When:* When empirical curves
  show a visible kink or two-regime behavior
- **R2** — The gossip penalty can be characterized by changes in BNSL
  parameters: - ΔC_∞: floor lift (fundamental, non-recoverable) - Δc₀:
  change in early exponent (recovery rate) - Δd₁: shift in kink location
  (how quickly the hard regime sets in) - Δ(c₀+c₁): change in late exponent
  (asymptotic rate) This four-dimensional decomposition is richer than the
  Kaplan two-parameter (floor + rate) decomposition and may reveal gossip
  effects invisible to single-power-law fits. **[not filed as a practice:
  specific to the project these readings were made for]**
  *Topic:* gossip penalty characterization · *Strength:* strong · *When:*
  Requires sufficient training steps to observe both regimes
- **R3** — Use the break point d₁ as a diagnostic for gossip overhead.
  Hypothesis: d₁ decreases as gossip period T decreases (more frequent
  averaging → earlier onset of the slow-scaling regime). Measuring d₁(T)
  gives a scalar summary of gossip cost that is comparable across
  experiments. **[not filed as a practice: specific to the project these
  readings were made for]**
  *Topic:* gossip diagnostic · *Strength:* moderate · *When:* Requires BNSL fits
  to converge reliably; needs T scan experiments

## Bearing on the record

Broken neural scaling laws fit the curves a single power law cannot,
including the non-monotone ones. The record holds practices fitted to power
laws and no statement of when that form fails.

## Limitations

- Purely empirical functional form; no mechanistic derivation.
- Six free parameters can overfit short curves; need sufficient range of t.
- Break sharpness f₁ is often poorly identifiable from noisy data.
- Chained BNSL adds parameters rapidly; model selection becomes critical.
- Does not address the Saad-Solla S-curve (exponential) regime — BNSL
  assumes power-law dynamics throughout.

## Open questions

- Can we derive the BNSL form from the Bordelon spectral theory by allowing
  β to shift at a transition point?
- Does fixing d₁ to the gossip event time give a well-identified 5-parameter
  fit?
- Is c₁ positive or negative for gossip-averaged curves relative to isolated
  training?
