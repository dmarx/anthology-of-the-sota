---
status: Read
paper: LIT-tmpnu5sc
title: 'Talagrand Meets Talagrand'
version: 1
date: '2026-09-26'
summary: >-
  Take a centered Gaussian process on a finite set T with max variance σ²
  and minimum separation a. The expected softmax-weighted average g(β) =
  E[Σ_t X_t e^{βX_t}/Z] satisfies g(β) ≤ √(2σ²·E D(ν_β‖ν₀)) for every β
  (Thm 1, D = KL from uniform). For β ≥ β*, g(β) ≥ c·a·√(E D(ν_β‖ν₀)),
  with c the Sudakov constant (1/17 via Marcus–Rosen) (Thm 2). For i.i.d.
  N(0,σ²) logits there is an exact identity, g(β) = βσ²(1 − E‖ν_β‖²₂)
  (Lemma 2). The quenched free energy is bounded above by √(2σ²·E
  D_{1/2}(ν_β‖ν₀)), with an i.i.d. lower bound of (cσ/2)√(E D_{1/2}) (Thms
  4–5).
---

<!-- inactive-ok-file: THEORY-061 — Proposed; named in Bearing on the record as the neighbouring account -->

# NOTE-tmp1ybcq: Talagrand Meets Talagrand

## Contribution

The classical two-sided bound a√log|T| ≲ E max_t X_t ≲ Δ√log|T| (Eq. 1) is extended to finite inverse temperature β. For the two smooth proxies of the maximum, the paper identifies which quantity plays the role of log|T| at finite β:
- for the Gibbs average g(β), the expected KL divergence of the Gibbs measure from uniform, E D(ν_β‖ν₀) = log|T| − E H(ν_β);
- for the quenched free energy φ(β), the expected Rényi-½ divergence E D_{1/2}(ν_β‖ν₀).

Both reduce to √log|T| as β → ∞. The authors believe the finite-β bounds are new (§1.1). They differ from Liu (2022, 2023), who bounds log-integral relaxations of convex-body widths for non-Gaussian linear processes.

## Key insight

Two tools, one for each direction.
- **Upper bound.** By the Gibbs variational principle, the softmax average ⟨X⟩_β is a Legendre dual of the log-partition function. So ⟨X⟩_β ≤ (1/λ)·D(ν_β‖ν₀) + φ(λ) for any λ, and the Gaussian moment generating function bounds φ(λ) ≤ λσ²/2. Optimising over λ gives √(2σ²·D).
- **Lower bound.** By Gaussian integration by parts, g(β) is an exact function of the replica overlap. It equals (β/2)·Σ_{s,t} d²(s,t)·E[ν_β(s)ν_β(t)]. At low temperature this lets Sudakov minoration at β = ∞ be propagated backwards to finite β by a monotonicity argument.

The one thing to remember: **for i.i.d. Gaussian logits, the expected softmax-weighted logit is exactly βσ² times one minus the expected collision probability** (Lemma 2, Eq. 12).

## Assumptions

- X = (X_t)_{t∈T} is a **centered Gaussian process on a finite index set T**.
- d(s,t) = (E|X_s − X_t|²)^{1/2} is a metric, not a pseudometric: E|X_s − X_t|² > 0 for s ≠ t (p. 2). So all X_t are a.s. distinct and ν_β tends to a Dirac mass as β → ∞.
- σ² = max_t Var X_t. a = min separation. Δ = diameter.
- Theorems 3 and 5 additionally assume that the X_t are **i.i.d. N(0, σ²)**. Then a² = Δ² = 2σ².
- Theorem 6 needs a 4σ-packing S of (T, d).
- Nothing about the logits being produced by a network, or about the values being averaged differing from the logits. The averaged quantity in g is the logit X_t itself.

## Key results

- **Eqs. 2, 4.** max X_t ≤ (1/β) log Σ e^{βX_t} ≤ max X_t + log|T|/β, and max X_t − log|T|/β ≤ g(X;β) ≤ max X_t.
- **Eqs. 8–10.**
  - D(ν_β‖ν₀) = log|T| − H(ν_β) = log|T| + β⟨X⟩_β − Λ(β), with Λ = log Z.
  - D_α(ν_β‖ν₀) = log|T| + (Λ(αβ) − αΛ(β))/(α−1).
  - D_{1/2}(ν_β‖ν₀) = log|T| + log‖ν_{β/2}‖²₂.
- **Lemma 1.** β ↦ ‖ν_β‖²₂ (the participation ratio, i.e. e^{−H₂(ν_β)}) is nondecreasing. Its derivative is 2‖ν_β‖²₂(Λ′(2β) − Λ′(β)) ≥ 0.
- **Lemma 2 (replica-symmetric representation).** g(β) = (β/2)·Σ_{s,t} d²(s,t)·E[ν_β(s)ν_β(t)] = (β/2)·E⟨d²(τ¹,τ²)⟩_β.
  - For i.i.d. N(0,σ²) logits: **g(β) = βσ²(1 − r(β))**, with r(β) = E‖ν_β‖²₂ nondecreasing.
- **Theorem 1.** g(β) ≤ √(2σ²·E D(ν_β‖ν₀)) for all β ≥ 0.
  - Corollary 1 writes this as √(2σ²(log|T| − E H(ν_β))), which recovers E max ≤ √(2σ² log|T|) as β → ∞.
- **Theorem 2.** There exists 0 < β* < ∞, depending on the covariance, with g(β) ≥ c·a·√(E D(ν_β‖ν₀)) for all β ≥ β*. The constant c is Sudakov's (Eq. 14).
- **Theorem 3 (i.i.d.).** As stated: g(β) ≥ cσ√(E D) for all β ≥ 0. As proved: that constant holds for β > β*, and cσ/√2 holds for β ≤ β* (see corrections).
- **Theorem 4.** φ(β) ≤ √(2σ²·E D_{1/2}(ν_β‖ν₀)).
  - Proof: integrate Theorem 1 through ψ(β) = βφ(β), with ψ′ = g, and use Jensen and the convexity of ψ.
- **Theorem 5 (i.i.d.).** φ(β) ≥ (cσ/2)·√(E D_{1/2}(ν_β‖ν₀)) for all β ≥ 0 (as stated; see corrections).
- **Theorem 6 (no independence).** If S is a 4σ-packing, then E Φ_β(X; ∪_s B(s,σ)) ≥ σ·E Φ_{βσ}(G; S) + (1/|S|)·Σ_s E Φ_β(X; B(s,σ)), with G i.i.d. N(0,1).
  - As β → ∞ this recovers Talagrand's (1992) minoration for finite T.
- **Theorem 7 (REM).** Energies are i.i.d. N(0, N/2) on {±1}^N. There are explicit piecewise functions Q̲_N ≤ P_N(β) ≤ inf_{β₀} Q̄_N(β; β₀) for each finite N, with a threshold β*_N.
  - Each bound is quadratic in β below its breakpoint. Above it, the lower bound is linear in β, and the upper bound is linear up to the slowly varying factor √(E D(ν_{N,β}‖ν_{N,0})/N) ≤ √log 2 (Remark 2). The constants are not sharp.
  - Choosing β₀ = β_c = 2√log 2 in the upper bound gives log 2 + β²/4 below β_c and ≤ β√log 2 above it, the correct upper bound at every N (Remark 2).
  - The limit law with the phase transition at β_c is cited to Giardinà–Starr. It is not proved here.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | g(β) ≤ √(2σ²·E D(ν_β‖ν₀)) for every β, with a sharp constant at β = ∞ | strong | proof, Thm 1 (Gibbs variational principle + Gaussian MGF) |
| C2 | For i.i.d. N(0,σ²) logits, g(β) = βσ²(1 − E‖ν_β‖²₂) exactly | strong | proof, Lemma 2 (Gaussian integration by parts) |
| C3 | A Sudakov-type lower bound g(β) ≥ c·a·√(E D) holds above some threshold β* | strong (existence only) | proof, Thm 2. β* is non-constructive. |
| C4 | For i.i.d. logits the lower bound holds at all β with constant cσ | moderate | proof, Thm 3. The proof gives cσ/√2 for β ≤ β*, so the printed constant is off by √2 there. |
| C5 | φ(β) ≲ σ√(E D_{1/2}) in general, and ≍ for i.i.d. | strong (upper) / moderate (i.i.d. lower, inherits C4's constant) | proofs, Thms 4–5 |
| C6 | Without independence, the β-softmax obeys a Talagrand-type minoration | strong | proof, Thm 6 (Chatterjee's Gaussian interpolation + Jensen) |
| C7 | The finite-β bounds are new | weak | assertion, §1.1 ("to the best of our knowledge") |
| C8 | The REM finite-N bounds pinpoint quadratic vs linear scaling in β | moderate | proof of Thm 7; constants not sharp, by the authors' own statement |

## Method

This is a proof paper and there is no algorithm. It uses four techniques:
- the Gibbs variational principle (Donsker–Varadhan duality) for the upper bounds;
- Gaussian integration by parts, giving the replica-symmetric representation;
- Sudakov minoration at β = ∞, propagated to finite β by showing that g(β) − ca√(E D) is nonincreasing beyond β*;
- the fundamental theorem of calculus through ψ(β) = βφ(β), with ψ′ = g, to move from Gibbs averages to free energies.

## Concepts

- **β-softmax** — Φ_β(X; A) = (1/β) log Σ_{t∈A} e^{βX_t} (log-sum-exp at inverse temperature β; §4.3).
- **Gibbs average g(X;β)** — Σ_t X_t e^{βX_t}/Z(β). This is the softmax-weighted mean of the logits themselves. It runs from the sample mean (β=0) to the max (β→∞).
- **Quenched** — the expectation over the disorder X is taken after the Gibbs average: g(β) = E g(X;β), and φ(β) = (1/β)·E log((1/|T|)·Σ e^{βX_t}).
- **Gibbs measure ν_β** — softmax(βX) as a random measure on T. ν₀ is uniform.
- **Participation ratio** — ‖ν_β‖²₂ = Z(2β)/Z(β)² = e^{−H₂(ν_β)}. It is the collision probability of two independent softmax draws.
- **Replicas** — τ¹, τ² drawn i.i.d. from ν_β for a fixed X.

## Connections

- The proofs rely on standard sources: Talagrand (2011, 2014) for generic chaining and Sudakov minoration, Panchenko (2013) and Talagrand (2011, Lemma 1.3.11) for replica-symmetric representations in the SK model, Chatterjee (2014) for superconcentration and Gaussian interpolation, Bovier (2006) and Mézard–Montanari (2009) for the REM.
- The closest prior work is Liu (2022, 2023). Liu bounds E log ∫ e^{⟨t,Y⟩}µ(dt) over convex bodies, with Y not necessarily Gaussian.
- The Rényi–free-energy link is cited to Baez (2022).
- It was read first in the catchall record, nucleation, where it was filed under information theory for its KL/Rényi characterisation; the owner moved it here on 2026-09-26.

## Bearing on the record

It supports or contradicts no document here directly. It carries no instruction and no ML claim. "Attention" and "transformer" never appear, "softmax" names only the log-sum-exp (Eq. 2, §4.3), and "neural" occurs only in the grant titles of the acknowledgments. But it does contain something an ML theory document could use, which is why it is filed here:
- **Attention with Gaussian scores.** g(X;β) is exactly the expected attended *score* under softmax attention whose scores are Gaussian, for example at initialization with random queries and keys. It is not the attended *value*, which weights separate V vectors. So the direct transfer is limited to "how large is the logit the softmax lands on".
  - Lemma 2 gives, for i.i.d. N(0,σ²) scores, E[Σ p_t s_t] = βσ²(1 − E Σ p_t²) exactly. That is an exact link between attention sharpness (Rényi-2 collision probability) and score scale.
  - Theorem 1 gives, for any Gaussian scores, E[Σ p_t s_t] ≤ √(2σ²(log n − E H(p))). A given expected attended score therefore forces an entropy deficit from uniform of at least g²/(2σ²).
- **Length and temperature.** The REM section (restated, not proved here) implies a condensation threshold. With energy variance N/2 over n = 2^N items, condensation sets in at β_c = 2√log 2, i.e. at βσ = √(2 ln n) in the paper's scaling (my translation). So softmax over i.i.d. Gaussian scores stays diffuse unless inverse temperature × score scale grows like √(2 ln n).
  - That is a mathematically clean version of why attention needs a temperature that grows with sequence length. It is the Gaussian counterpart of the bounded-logit dispersion argument in [THEORY-098](../theory.d/THEORY-098.md) (Veličković et al., [LIT-653](../literature.d/LIT-653.md)).
  - It sits beside [THEORY-061](../theory.d/THEORY-061.md) (attention entropy lower-bounded via the spectral norm of the QK product) and the practices [SOTA-050](../practices.d/SOTA-050.md) (1/√d scaling) and [SOTA-192](../practices.d/SOTA-192.md) (QK normalization).
- **How to cite it.** As supporting mathematics for an account of softmax temperature against the number of items — not as evidence that any temperature schedule works. The reading that placed it recommended naming it in prose rather than filing it alone; it is filed alone at the owner's request, and the recommendation stands for how it is used. The phase-transition fact itself is Derrida's REM, not this paper's result.

## Limitations

- The index set must be finite and the process exactly Gaussian. There is no heavy-tail or sub-Gaussian version and no infinite-T version (generic chaining at finite β is not attempted).
- The low-temperature lower bound needs a non-constructive threshold β*. So Theorem 2 gives no usable bound at any specified β outside the i.i.d. case.
- Theorem 3's printed constant exceeds the proved one by √2 for β ≤ β*. Theorem 5 inherits this.
- The i.i.d. matching bounds do not extend to correlated processes. Only the free-energy minoration (Thm 6) goes beyond independence.
- The REM bounds are explicitly not sharp. The phase-transition limit is quoted, not derived.
- The abstract's "learning theory" motivation is not developed anywhere in the text.

## Open questions

- Can β* be made explicit in terms of the covariance, for example via a, Δ and |T|? That would turn Theorem 2 into a usable finite-temperature bound.
- Does g(β) ≍ σ√(E D(ν_β‖ν₀)) hold for weakly correlated or equicorrelated logits? A chaining argument at finite β would settle it.
- Is there a generic-chaining analogue at finite β, i.e. a finite-temperature γ₂ functional?
- For ML use: does the same KL-from-uniform characterisation hold when the averaged vector (values) differs from the scores? That is the attention-output case, and the paper does not treat it.

## Corrections to the seeded skim

- The dossier gives the headline bounds only up to ≲/≳. The constants are explicit, and one matters. Theorem 1 is g(β) ≤ √(2σ²·E D(ν_β‖ν₀)), with the sharp √2 that recovers E max ≤ √(2σ² log|T|) (Eq. 13). Theorem 2's constant is exactly the Sudakov constant c of Eq. 14. The paper quotes c = 1/17 from Marcus–Rosen Lemma 5.5.6.
- The threshold β* in Theorem 2 is **not constructive**. The proof (p. 9) only shows that some β* exists. It is the point beyond which 1 − r(β) ≤ c²a²/(2Δ²), where r(β) = E‖ν_β‖²₂ and Δ is the diameter. Existence follows because r is nondecreasing (Lemma 1) and tends to 1. The paper gives no expression or estimate for β*. The dossier asked "how it depends on covariance". The answer is: only through this implicit condition on r, a and Δ.
- Theorem 3 (i.i.d. lower bound "for all β ≥ 0") has a constant slip that the dossier could not see. The theorem states g(β) ≥ cσ√(E D). The proof's high-temperature branch (p. 10) delivers g(β) ≥ cσ√(½·E D), i.e. constant c/√2. Remark 1 calls this "the worse constant c/2", which is c/2 in units of a = √2σ. So the statement as printed overstates the proved constant for β ≤ β* by a factor √2. Theorem 5 inherits the statement's constant (ψ ≥ βg/2 ≥ (cβσ/2)√(E D)). Its proved constant is therefore cσ/(2√2), not cσ/2. The orders of magnitude and the ≍ claims are unaffected.
- The dossier's question "whether the i.i.d. matching extends to weakly correlated logits" is not addressed anywhere in the paper. Its only result without independence (Theorem 6, §4.3) is a Talagrand-type lower bound on the β-softmax (1/β)·E log Σ e^{βX_t}, i.e. on the free energy. It is not a bound on g(β).
- The dossier's summary says the free energy "scales likewise with the Rényi-½ divergence". Only the upper bound is general (Thm 4). The matching lower bound is i.i.d.-only (Thm 5).
