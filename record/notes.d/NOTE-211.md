---
number: 211
status: Read
formerly:
- NOTE-tmpepjgm
paper: LIT-462
title: 'Spectral muP under Width-Depth Scaling'
version: 1
date: '2026-09-20'
summary: >-
  Derives the muP spectral condition for joint width-depth scaling and shows
  the rule is indexed by residual-branch depth. Reading it: Depth-muP and
  CompleteP are `k = 1` and `k ≥ 2` of one family, Transformers are the
  second, and for preconditioned optimizers the whole depth correction is a
  `1/L` residual multiplier.
---

<!-- inactive-ok-file: SOTA-144 SOTA-275 SOTA-276 THEORY-024 — SOTA-144 is Proposed and this reading is the assessment of its promote_when; the two SOTA-tmp practices are Proposed and filed here from this reading; THEORY-024 is Proposed and is named as an adjacent frame this derivation does not need -->
# NOTE-211: Spectral muP under Width-Depth Scaling

## Contribution

Width-depth muP existed in several incompatible forms, each tied to a
particular architecture and optimizer and each derived with heavy machinery —
Tensor Programs or dynamical mean-field theory. This paper derives them all
from one spectral condition using elementary linear algebra, and in doing so
explains *why* they differ: the rule is set by how many transformations sit
inside a residual branch. What is true afterwards that was not before is that
Depth-muP and CompleteP are not rivals, they are `k = 1` and `k ≥ 2` of one
family, and which one an architecture needs is a structural fact about that
architecture rather than an empirical question.

## Key insight

Expand the one-step change in a residual block's output. With one
transformation in the branch, only terms where a single weight moved appear.
With two, there is also a term where *both* moved in the same step — the
product `ΔW⁽²⁾ΔW⁽¹⁾`. That cross term is second order and would ordinarily be
dismissed as negligible; under the maximal-update principle it is not,
because muP deliberately makes every update as large as stability allows.
Constraining it is what tightens the residual multiplier from `Θ(1/√L)` to
`Θ(1/L)`. The whole difference between the two published depth
parameterizations is one term in a product expansion.

## Assumptions

- **Deep linear residual MLP, one gradient step, one data point.** The main
  derivation is in the same simplified setting Yang et al. use for the
  width-scaling condition. Appendix G states and verifies assumptions under
  which it extends to finitely many steps, nonlinearities and finitely many
  examples; the extension is argued, not proved in general.
- **Scale estimates, not equalities.** The norm tracking uses subadditivity
  and submultiplicativity, and the tightness depends on "standard
  non-cancellation and alignment behavior". Appendix F justifies this the way
  the width-scaling treatment does. If cancellation were typical the
  estimates would be loose in the direction that matters.
- **`k = Θ(1)`**: residual branch depth is fixed as width and depth grow.
- **Gaussian initialization**, layerwise learning rates, block multipliers
  `α_l`.
- **Scale.** GPT-2 style models on OpenWebText, widths to 4096, depths to
  256, 300M tokens per run at batch size 240. Deep, not long: the depth
  sweep is the contribution and the token budget is small.

## Key results

- **Condition 3.1** — for a two-layer residual block, `α_l ‖W⁽²⁾‖_R ‖W⁽¹⁾‖_R =
  Θ(1/L)` at initialization, with the same `Θ(1/L)` imposed on the two
  first-order update products (C2.2) *and* on the second-order product
  `α_l ‖ΔW⁽²⁾‖_R ‖ΔW⁽¹⁾‖_R` (C2.3). Input and output weights keep the
  width-scaling `Θ(1)`. *Holds when:* the simplified setup above.
- **Condition B.1 (`k = 1`)** — no second-order term exists, the constraint
  set is looser, and `α_l = Θ(1/√L)` follows. Recovers Depth-muP.
- **Condition B.2 (`k ≥ 2`)** — all orders 1 through `k` constrained to
  `Θ(1/L)`; the resulting parameterization is the same as `k = 2`. So `k = 2`
  is the minimal setting that captures practical architectures, and there is
  no third regime.
- **Takeaway 2** — for every modern optimizer treated except SGD,
  implementing Condition 3.1 is width-scaling muP plus `α_l = Θ(1/L)`.
  Normalized and preconditioned updates have norms that do not depend on
  `α_l`, so the depth factor the raw gradient inherits is removed. SGD's
  update is proportional to the raw gradient and needs an extra `α_l`-
  dependent learning-rate rescaling.
- **Empirical, Figure 1** — under SP the final-block feature RMS grows
  rapidly with both width and depth and the optimal base learning rate
  shifts; under the Condition 3.1 muP it stays flat and the optimum barely
  moves, across widths 128–4096 and depths 4–256.
- **Empirical, Figure 2** — the head-to-head. Condition B.1 (`k = 1`) shifts
  the optimal learning rate as depth grows; Condition 3.1 (`k ≥ 2`) does not.
  Shown for Muon-Kimi-AdamW and Muon-AdamW, repeated for Shampoo-AdamW and
  Sophia in the appendix.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Residual-branch depth `k` determines which depth-muP rule applies, via the highest-order update term | strong | derivation in §3.3, and the `k=1` vs `k≥2` head-to-head in Figure 2 is a direct test of the prediction |
| C2 | Transformers are the `k ≥ 2` case and need CompleteP-style scaling | moderate | structural observation plus Figure 2 on GPT-2-style models at 300M tokens |
| C3 | Width-depth muP = width muP + `α_l = Θ(1/L)` for normalized/preconditioned optimizers | moderate | derived per optimizer in §4 and Appendix C; the experiments implement it rather than testing the simplification against a non-simplified alternative |
| C4 | The condition yields correct muP for nine named optimizers | moderate | derivations for all nine; experiments run four |
| C5 | The elementary derivation recovers prior width-depth muP results as special cases | strong | shown for Depth-muP and CompleteP explicitly |

## Method

Write a residual network with `k`-transformation branches and explicit block
multipliers. Require scale-invariant features and maximal feature change
(Principle 2.1). Track RMS operator norms through initialization and through
a one-step update, expanding the feature change by update order. Read off the
constraints. Then, per optimizer, map the constraint on `‖ΔW‖_R` to a
concrete learning-rate and initialization rule using that optimizer's update
form.

## Concepts

- **RMS operator norm** `‖A‖_R = max_v ‖Av‖_R / ‖v‖_R = √(n/m) ‖A‖₂` — the
  spectral norm rescaled so that the conditions read as `Θ(1)`.
- **Block multiplier `α_l`** — the scalar in front of each residual branch,
  the quantity the depth rule actually sets.
- **`k`** — the number of linear transformations inside one residual branch.
- **Depth-muP-style / CompleteP-style** — the paper's own hedged names for
  the `k = 1` and `k ≥ 2` formulations. It says it *recovers* these, not that
  it implements them.

## Connections

Extends the width-scaling spectral condition of Yang et al. ([LIT-437](../literature.d/LIT-437.md))
to joint width-depth scaling, which is the move the whole paper is. Recovers
CompleteP ([LIT-150](../literature.d/LIT-150.md)) as the `k ≥ 2` case and Depth-muP as `k = 1`.
Sits beside [LIT-436](../literature.d/LIT-436.md), the modular norm, which also gets learning-rate
transfer across width and depth — by defining a norm recursively alongside
the architecture rather than by indexing a condition on branch depth.

## Bearing on the record

- **[SOTA-144](../practices.d/SOTA-144.md)'s `promote_when` is nearly met, and the gap is worth
  being exact about.** It asks for "an independent group training under
  CompleteP itself and reporting depth transfer." This group is independent
  (Renmin University and ByteDance Seed, no overlap with the CompleteP
  authors) and it does report depth transfer to `L = 256`. But it trains
  Muon-Kimi-AdamW, Muon-AdamW, Shampoo-AdamW and Sophia — explicitly *not*
  AdamW, on the grounds that prior work covered it — and the parameterization
  is its own Condition 3.1, which the paper says "recovers CompleteP-style
  results", the hedge being the paper's own word. So this is corroboration of
  the route by an independent derivation and a wider set of optimizers, and
  it is not the literal test the field was asked for. `SOTA-144` moves from
  `unreplicated` to `emerging` and stays `Proposed`; validation at production
  scale is still missing, which is what `Proposed` means here.
- **It produces [SOTA-275](../practices.d/SOTA-275.md)** — pick the depth rule from the
  residual branch — which is a recommendation `SOTA-144` does not make.
  `SOTA-144` says use CompleteP; this says which architectures need it and
  why, and that the alternative demonstrably fails on Transformers.
- **It produces [SOTA-276](../practices.d/SOTA-276.md)** — the one-multiplier
  implementation rule, with SGD named as the exception.
- **It bears on [SOTA-121](../practices.d/SOTA-121.md) and [SOTA-165](../practices.d/SOTA-165.md).** The record
  recommends Muon and matrix preconditioning and says nothing about how to
  muP either. This derives both, and Takeaway 2 says the answer is the same
  as AdamW's plus one multiplier — which is why the omission was survivable.
- **It is adjacent to [THEORY-024](../theory.d/THEORY-024.md) without depending on it.** That account
  says muP and Shampoo are partial approximations of one duality map. This
  derives muP for Shampoo, Muon and six others from a spectral condition, and
  needs no duality anywhere. Two frames, same objects.

## Limitations

- The derivation is a deep **linear** residual MLP with a **one-step** update
  on a **single** example. The generalization is in an appendix under stated
  assumptions.
- The norm tracking gives scale estimates whose tightness rests on
  non-cancellation and alignment behaviour, argued rather than proved.
- 300M tokens per run. Nothing here is a long-horizon result, and muP's
  known failure modes at long horizons are not probed.
- Nine optimizers derived, four run.
- The `k ≥ 2` advantage over `k = 1` is measured as learning-rate transfer
  stability, not as final loss at matched compute.
- **The authors flag a confound themselves.** For Muon-Kimi-AdamW, SP appears
  to transfer across depth reasonably well in Figure 1(d). They attribute it
  to moderate depths and to LayerNorm and QKNorm masking the pathology, and
  they remove LayerNorm to show SP then breaks. That is honest, and it also
  means the practical margin at realistic depths with modern normalization is
  smaller than the theory's margin.

## Open questions

- Does the `k ≥ 2` rule still beat `k = 1` at a realistic token budget, where
  the 300M-token runs cannot say?
- What does `k` mean for an architecture whose residual branch depth is not
  constant across blocks, or for one with parallel attention and FFN?
- Is the one-multiplier simplification exact for every preconditioned
  optimizer, or an artifact of the nine chosen? The argument is that update
  norms do not depend on `α_l`, which is a property to check rather than a
  theorem about the class.
