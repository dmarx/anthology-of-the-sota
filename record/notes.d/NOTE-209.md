---
number: 209
status: Read
formerly:
- NOTE-tmprnxym
paper: LIT-457
title: 'When Spectral Updates Help'
version: 1
date: '2026-09-20'
summary: >-
  A spectral step beats a Euclidean one on a block when the gradient's
  nuclear rank exceeds the stable rank of that block's incoming activations.
  Reading it: both sides are measurable, the activation side is provably
  small in transformers, and the gap grows with dimension.
---

<!-- inactive-ok-file: THEORY-024 THEORY-032 SOTA-274 — THEORY-024 is Proposed and is named as the account this one is not; the other two are Proposed and filed here from this reading -->
# NOTE-209: When Spectral Updates Help

## Contribution

Muon is used widely and justified by geometry. This paper asks a narrower and
more answerable question — in which regimes should a spectral update beat a
Euclidean one — and answers it with a single inequality between two
quantities a training run can compute. It then does the work of showing the
inequality is not vacuous: post-activation matrices in transformers have
provably low stable rank at initialization, that property propagates through
attention and MLP sublayers, and in a real NanoGPT run both sides behave as
the theory says throughout training.

## Key insight

The reason a spectral update helps is a property of the *data flowing into a
block*, not of the norm the update descends in. When incoming activations are
degenerate — a handful of effective directions — the Euclidean view of the
landscape is badly conditioned, while an update that depends only on singular
vectors and spectral/nuclear norms is not. Low stable rank is the enabling
condition, and it is ubiquitous in transformers because token frequency is
Zipfian and RMSNorm, attention and the MLP all preserve it up to constants.

## Assumptions

- **Blockwise structure**: each trainable matrix `W` acts on an incoming
  feature matrix `X` as `W X`, and the one-step descent comparison is per
  block. Shown to extend to transformer blocks in §1.2.1.
- **Gaussian initialization** (Assumption A) for the propagation results:
  attention projections at variance `1/d`, MLP weights at the standard
  scaling, mutually independent and independent of the input.
- **Column-norm regularity** on the block input, `‖x_i‖ = Θ(√d)`.
- **Proportional asymptotics** with a spiked covariance for the random-feature
  results; ReLU activations in the accompanying experiments.
- **Scale.** Synthetic regression plus NanoGPT. Again, not frontier scale.

## Key results

- **The comparison (1.1)** — the ratio of the guaranteed one-step decreases is
  `nuclearRank(∇W) / stableRank(X)`, so spectral is favoured when
  `‖∇W‖_*² / ‖∇W‖_F² > ‖X‖_F² / ‖X‖_op²`. *Holds when:* the local curvature
  constants are controlled as in §1.2; it is a comparison of guarantees, not
  of realized progress.
- **(2.15)** — the stable rank of the token-indicator matrix is exactly
  `1/p_max`, the inverse empirical frequency of the most common token. In
  their NanoGPT run `p_max ≈ 1/20`.
- **Lemma 2.9** — embeddings and RMS-normalized embeddings have stable rank
  `O(1/p_max)` with high probability under Gaussian embedding columns.
- **Lemma 2.10 / Proposition 2.14 / Corollary 2.15** — stable rank is
  preserved through RMSNorm, attention and MLP up to constants, giving MLP
  post-activations `sr = O(1)` uniformly in depth, and everything at depth
  `l` bounded by a quadratic in `l`, **independent of width and sequence
  length**.
- **Spiked random-feature regression** — after a short burn-in the gradient's
  nuclear rank grows with dimension `d` while activation stable rank stays
  bounded, so the predicted speedup is itself dimension-dependent and linear
  in `d` in their examples.
- **NanoGPT measurement (Figure 10)** — intermediate activations stay low
  stable rank throughout training and gradients keep large
  nuclear-to-Frobenius ratios. The authors note the `1/p_max` bound is
  generally loose against the measured value.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Spectral beats Euclidean on a block when gradient nuclear rank exceeds incoming activation stable rank | strong | derived from the one-step descent bounds, §1.2; a statement about guarantees |
| C2 | Transformer post-activations have low stable rank, bounded independently of width and sequence length | strong | Lemmas 2.9, 2.10, Proposition 2.14, Corollary 2.15, at Gaussian initialization |
| C3 | That property persists through training, not just at initialization | moderate | measured in one NanoGPT run; the theorems are initialization-time |
| C4 | The advantage grows with dimension rather than decaying | moderate | proved in the spiked RF model, observed in the synthetic experiments |
| C5 | The condition explains Muon's practical success | moderate | the regime it predicts is the regime Muon is used in; no ablation applies the condition selectively |

## Concepts

- **Stable rank** — `‖X‖_F² / ‖X‖_op²`. A continuous surrogate for rank,
  small when a few directions carry the energy.
- **Nuclear rank** — `‖G‖_*² / ‖G‖_F²`, written `nr(G)`. Large when the
  gradient's singular values are spread out.
- **Incoming feature matrix** — for an MLP the previous post-activation; for a
  transformer, the RMS-normalized hidden states entering the attention
  projections or the post-activations entering the second MLP matrix.

## Connections

Builds on SpecGD (the polar-factor update) and on Muon as its momentum
variant. Explicitly positioned as *not* an analysis of Muon's practical
details, but of why the spectral update rule suits the structure that arises.
The authors note that gradient nuclear ranks already appear inside
convergence analyses of Muon and Scion; the contribution is relating that
quantity to the stable rank of the propagated data.

## Bearing on the record

- **It gives [SOTA-165](../practices.d/SOTA-165.md) an account that is not [THEORY-024](../theory.d/THEORY-024.md)'s.**
  The record's existing explanation of matrix preconditioning is the duality
  map; this is a different explanation of the same practice, from an
  unrelated group, and the two are not in conflict — one says what the update
  *is*, this says when it *wins*. Filed as [THEORY-032](../theory.d/THEORY-032.md).
- **It produces [SOTA-274](../practices.d/SOTA-274.md)**, the measurement: check the two
  quantities before assuming a spectral optimizer will pay.
- **It is the constructive half of the pair with [LIT-456](../literature.d/LIT-456.md).** That
  paper rules an explanation out; this one offers a different one. They were
  read together and neither depends on the other.
- **It does not license selective application.** The paper validates that the
  condition holds; it does not run an ablation that applies spectral updates
  only to blocks passing the test. The practice filed from it is therefore a
  measurement and not a routing rule, which is what [ADR-017](../decisions.d/ADR-017.md) asks of
  a claim's relation to its source.

## Limitations

- The comparison is between *guaranteed* one-step decreases. A bound being
  better does not establish that realized training is faster.
- The propagation theorems hold at Gaussian initialization. Persistence
  through training is measured in one run, not proved.
- One architecture, NanoGPT scale, plus synthetic regression.
- The stable-rank bound via `1/p_max` is acknowledged to be loose.
- No optimizer is proposed and no ablation of the condition as a decision
  rule is run.

## Open questions

- Does a block-selective spectral optimizer — spectral where the condition
  holds, Euclidean elsewhere — actually train faster? That is the experiment
  the paper sets up and does not run.
- Does the stable-rank structure hold at frontier width and sequence length,
  where the bounds say it should but nothing was measured?
- How does this relate to the step-size account in [LIT-456](../literature.d/LIT-456.md)? Both
  are non-geometric explanations of the same phenomenon and neither cites the
  other; whether they are one mechanism is open.
