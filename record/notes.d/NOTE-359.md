---
number: 359
status: Read
formerly:
- NOTE-tmpf0zmh
paper: LIT-700
title: 'Non-Euclidean Edge of Stability'
version: 1
date: '2026-09-25'
summary: >-
  Steepest descent under the ℓ∞, block and spectral norms, and SignGD and
  normalized Spectral GD, sharpen to `2/η` and train there — measured in the
  update's own norm, where the ordinary top Hessian eigenvalue stays far below
  the threshold. Reading it: the identity is exact and the empirics are
  consistent, but the sharpness is a Frank-Wolfe estimate, the divergence
  theorem covers one line of initializations, and everything is full-batch.
---

<!-- inactive-ok-file: THEORY-024 THEORY-030 THEORY-033 SOTA-272 — all Proposed, and named to say what this reading does not reach, not relied on -->

# NOTE-359: Non-Euclidean Edge of Stability

## Contribution

Before this paper the edge of stability had been characterized for gradient
descent ([LIT-461](../literature.d/LIT-461.md)), for adaptive preconditioned methods (Cohen et al. 2022,
not in the record) and for SAM, each with its own notion of sharpness. This
gives one definition that covers all of them and extends to the optimizers
that had not been studied: steepest descent under an arbitrary norm, which
includes Spectral GD (the update underneath Muon), ℓ∞-descent, block
coordinate descent, and their normalized versions SignGD and normalized
Spectral GD. It then shows empirically that each of them sharpens to `2/η`
and trains there, in that definition.

## Key insight

Stability is a statement about curvature *in the geometry the step is
taken in*. Take a step of size `η` along the steepest-descent direction for a
norm, and whether the loss goes down is decided by the curvature along that
step measured in that norm. So the sharpness that equilibrates at `2/η` is
`max_{‖d‖=1} dᵀ∇²L d` for the update's norm — which is `λ_max` only when the
norm is Euclidean. Measure a spectral or sign optimizer with the Euclidean
eigenvalue and the regime is invisible.

## Assumptions

- **Full-batch, deterministic updates, no momentum.** Every experiment. The
  conclusion names stochastic, momentum and adaptive extensions as future
  work "to clarify how geometry-aware EoS diagnostics should be used in
  practical large-scale training".
- **The step is a pure steepest-descent step under a fixed norm**:
  `w_{t+1} = w_t − η‖∇L‖_*(∇L)^*` (Definition 1.1) or its normalized form
  `w_{t+1} = w_t − η(∇L)^*` (Definition 1.2). For the spectral case the norm
  is `max_ℓ ‖W^ℓ‖_2` across layers, following Bernstein and Newhouse's *Old
  optimizer, new norm* (not in the record), and the update is computed with
  5 Polar Express steps. This is Spectral GD, not Muon: no momentum, no
  AdamW for non-matrix parameters, no per-layer shape scaling.
- **The Hessian is roughly constant along the step.** Generalized sharpness
  (Definition 2.2) is obtained from the exact directional smoothness by this
  assumption; it is a motivation, not a bound in the other direction.
- **Twice continuously differentiable loss**, for the Taylor step (eq. 8).
- **Quadratic results** (Theorems 5.1, 5.2) assume `L(w) = ½wᵀHw` with
  `H ≻ 0`.
- **Setting.** MLPs and small CNNs on a 5k subset of CIFAR-10 and on full
  CIFAR-10, ResNet20 and VGG11 on CIFAR-10, all with MSE loss; a Transformer
  on Tiny Shakespeare with cross-entropy. Nothing near the decoder-only,
  large-batch, stochastic setting this record's practices assume.

## Key results

- **Loss-change identity (eq. 6–7).** With `D(w_t, w_{t+1})` the exact
  directional smoothness along the step, one step of non-Euclidean GD gives
  `ΔL_t = −η(1 − (η/2)D)‖∇L(w_t)‖²_*`, so whenever `‖∇L‖_* > 0`,
  `ΔL_t ≤ 0 ⟺ D ≤ 2/η`. *Holds:* exactly, for any norm and any
  differentiable loss.
- **Normalized form (eq. 20–21).** For `w_{t+1} = w_t − η(∇L)^*`,
  `ΔL_t ≤ 0 ⟺ D ≤ 2‖∇L‖_*/η`. *Holds:* exactly.
- **Theorem 5.1.** On a positive-definite quadratic, non-Euclidean GD with
  `η < 2/S` converges linearly from any start. *Holds when:* quadratic,
  `H ≻ 0`.
- **Theorem 5.2 / Lemma 5.3.** For `η > 2/S` there exists an initialization
  (on the line spanned by the sharpness maximizer) and a valid dual-gradient
  selection from which it diverges, as `w_t = (1 − ηS)^t w_0`. *Holds when:*
  the same; the authors note this is weaker than Euclidean GD, which diverges
  from all but a measure-zero set.
- **Theorem J.5.** Divergence from every nonzero start when `η > 2/μ`, where
  `μ = inf_{‖v‖=1} vᵀHv` — a much larger step.
- **Block ℓ1,2 closed form (Lemma I.8).** If the Hessian is PSD, generalized
  sharpness is the largest diagonal-block eigenvalue, `max_ℓ λ_max(∇²_{w_ℓ}L)`.
- **Empirical (Figures 1–5, E.1–E.3, G.1–G.5).** Directional smoothness and
  generalized sharpness rise to `2/η` and hover at or slightly above it, for
  GD, ℓ∞-descent, Block CD and Spectral GD; the normalized ratios do the same
  for SignGD and normalized Spectral GD. On ResNet20 and VGG11 with ℓ∞-descent
  and with Spectral GD, `λ_max(∇²L)` stays far below `2/η` while generalized
  sharpness sits at it.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | For steepest descent under any norm, the loss decreases on a step iff the directional smoothness along it is at most `2/η` | strong | eq. 6–7; an identity, no assumptions beyond differentiability |
| C2 | Non-Euclidean GD (ℓ∞, block ℓ1,2, spectral) sharpens to `2/η` in generalized sharpness and hovers there | moderate | Figures 2–4, E.1, G.1, E.3, G.5 — consistent across MLP, CNN, ResNet20, VGG11 and one small Transformer, full-batch only; the sharpness for ℓ∞ and spectral is a multi-restart Frank-Wolfe *lower* estimate of an NP-hard maximum |
| C3 | For Spectral GD and ℓ∞-descent the ordinary top Hessian eigenvalue stays well below `2/η`, so Euclidean sharpness does not capture the regime | moderate | Figures E.3 and G.5, two architectures on CIFAR-10; a direct measurement |
| C4 | SignGD and normalized Spectral GD sit at the gradient-scaled threshold, `S/‖∇L‖_* ≈ 2/η` | moderate | Figure 5, one setting each; follows algebraically from C1 once C2 holds |
| C5 | The generalized sharpness is the right quantity because the local quadratic model diverges above it | weak | Theorem 5.2 covers one line of initializations; Figure 6 and G.4 show generic divergence on one CNN; the authors call the explanation "still incomplete" |
| C6 | Cohen et al.'s adaptive-EoS characterization of RMSprop fails for small `β₂` | moderate | Figure H.1, one MLP, `β₂` swept |
| C7 | Under ℓ∞ and spectral norms there is a pre-EoS oscillatory regime that Euclidean GD does not have | weak | Appendix B, one ℓ∞ run plus Figure B.2; reported, not explained |
| C8 | Generalized sharpness slightly above `2/η` reflects several unstable directions, as for Euclidean GD | weak | Appendix C: an analogy to Cohen et al. (2025) plus Figure C.1 on one run; the authors say extending the argument "is nontrivial" |

## Method

*Estimating generalized sharpness.* `max_{‖d‖≤1} dᵀHd` is NP-hard in general
(for ℓ∞ it is an Ising ground-state problem). The paper runs Frank-Wolfe on
the relaxed ball, `K = 50` iterations with step `γ_k = 2/(2+k)`, from `M`
random Gaussian restarts, projects the final iterate onto the unit sphere,
and keeps the maximum over restarts (Algorithm 1). Each Frank-Wolfe step
needs one Hessian-vector product and one linear-minimization oracle for the
norm — for the spectral norm, a polar factor. Defaults `M = 5`, `K = 50`.

The estimate is a lower bound on the true value. It is sensitive to `M` for
ℓ∞ and block norms (one restart underestimates; Figures E.2, F.1) and
insensitive for the spectral norm (Figure G.2). For block ℓ1,2 with a PSD
Hessian the closed form is available and was used as the reference.

## Concepts

- **non-Euclidean GD** — `w_{t+1} = w_t − η‖∇L‖_*(∇L)^*`, the minimizer of
  the linearization plus `(1/2η)‖y − w‖²`. Its normalized form drops the
  dual-norm factor.
- **directional smoothness** `D(w, y)` — the curvature along the chord,
  `(L(y) − L(w) − ⟨∇L(w), y − w⟩)/(½‖y − w‖²)`, chosen so the descent
  inequality holds with equality. May be negative.
- **generalized sharpness** `S_‖·‖(w)` — `max_{‖d‖=1} dᵀ∇²L(w)d`. Reduces to
  `λ_max` under ℓ2 and to `λ_max(P^{-1/2}∇²L P^{-1/2})` under a
  preconditioner norm.
- **Spectral GD** — steepest descent under `max_ℓ ‖W^ℓ‖_2`; the update is the
  polar factor of each layer's gradient scaled by the sum of nuclear norms
  across layers.

## Connections

It extends [LIT-461](../literature.d/LIT-461.md) directly: the same phenomenon, the same threshold, the
same Taylor-approximation test (their Figure 6 is Cohen et al.'s Appendix E
run under a different norm), on Cohen et al.'s code, with Cohen as an
author. It borrows [LIT-453](../literature.d/LIT-453.md)'s picture of oscillation in a multi-dimensional
unstable subspace to explain the gap above `2/η`, by analogy. Its update
family is the steepest-descent-under-a-norm frame of the modular-duality line
([LIT-438](../literature.d/LIT-438.md) and its predecessors); it cites *Old optimizer, new norm* for the
spectral block norm, not the modular-duality paper itself. Directional
smoothness comes from Mishkin et al. (2024), not in the record. [LIT-456](../literature.d/LIT-456.md)
cites it as the paper joining the local-expansion analysis to the edge of
stability.

## Recommendations

- **R1** — When checking whether a run with a non-Euclidean optimizer is at
  the edge of stability, measure curvature in the update's norm, not the
  Hessian's top eigenvalue; for normalized updates compare `S/‖∇L‖_*` to
  `2/η`. *Topic:* analysis-and-evaluation. *Status:* experimental.
  *Strength:* moderate for the negative half (the Euclidean eigenvalue
  misses it, C3), weak for the positive half at any practical setting
  (full-batch only, estimator is a heuristic lower bound). *Applies when:*
  full-batch or near-full-batch diagnostics; not shown for stochastic,
  momentum or Muon-as-deployed.

Not filed as a practice. The instruction is a diagnostic that nobody in the
record's setting runs — sharpness is expensive even in the Euclidean case,
and here it needs repeated Frank-Wolfe with Hessian-vector products — and its
evidence stops at full-batch CIFAR-10. `DP-006` sets a low bar for filing,
but it asks for an instruction a reader can act on in the regime the record
covers, and the authors themselves name that regime as future work.

## Bearing on the record

- **[THEORY-035](../theory.d/THEORY-035.md)** — supported and refined. The account's two forces and one
  equilibrium hold for every non-Euclidean optimizer tested, which is an
  outside replication of the regime in a new class of optimizers. But its
  quantity, "the maximum eigenvalue of the training-loss Hessian", is the
  right one only for Euclidean GD; for the spectral and sign updates it is
  the generalized sharpness in the update's norm, and the Euclidean
  eigenvalue is well below `2/η`. Recorded there at v2. The identity (C1)
  does not fill that document's "does not explain progressive sharpening"
  gap: it shows the *directional smoothness* must rise if the loss goes from
  decreasing to oscillating, which is a consequence of the oscillation, not a
  mechanism for Hessian curvature rising.
- **[THEORY-024](../theory.d/THEORY-024.md)** — not reached. The paper takes the steepest-descent-under-a-
  norm frame as its object and shows the frame is the right one for
  *describing where the stability threshold sits*. It does not compare
  optimizers on loss or test whether the geometry is what makes spectral
  updates train well, which is what [LIT-456](../literature.d/LIT-456.md)'s control contests. A reader
  should not count this as evidence for the duality account's explanatory
  claim.
- **[THEORY-033](../theory.d/THEORY-033.md)** — not reached. Normalized Spectral GD's threshold is
  `2‖∇L‖_*/η`, an effective-step relation, but nothing here measures the
  optimal step size or its constancy.
- **[THEORY-030](../theory.d/THEORY-030.md)** — neighbouring, not tested. That document asks whether its
  curvature-shaping account and the duality account are one mechanism or two;
  this paper puts both kinds of optimizer under one stability condition but
  does not examine implicit curvature penalties or central flows for
  non-Euclidean methods.
- **[SOTA-121](../practices.d/SOTA-121.md)** (Muon) and **[SOTA-272](../practices.d/SOTA-272.md)** — untouched. Nothing here compares
  optimizers or step-size rules. The warning in R1 would apply to anyone who
  tried to use [SOTA-272](../practices.d/SOTA-272.md)'s reasoning to monitor a Muon run by the Euclidean
  sharpness, but the record does not currently say to.

## Limitations

- Full-batch and without momentum; no weight decay or mixed per-parameter
  optimizers are described. The
  optimizers are idealizations of Muon and Adam-family methods, not the
  deployed versions.
- Small networks and datasets: CIFAR-10 (often 5k examples), MSE loss for all
  vision runs, one small Transformer on Tiny Shakespeare.
- For ℓ∞ and spectral norms the reported sharpness is a heuristic
  Frank-Wolfe estimate of an NP-hard maximum and can only undershoot the true
  value; "hovers slightly above `2/η`" is therefore a statement about the
  estimate.
- The divergence theory (Theorem 5.2) is for a specific initialization and
  dual-gradient selection; the authors say it "does not yet establish generic
  divergence".
- No claim is made about generalization, final loss, or which optimizer is
  better.

## Open questions

- Does generalized sharpness equilibrate at a predictable value under
  stochastic gradients and momentum — i.e. for Muon as run? [LIT-461](../literature.d/LIT-461.md) found
  Euclidean sharpness does not under SGD, so the answer is not obvious.
- Why does the pre-EoS oscillatory regime (C7) exist for ℓ∞ and spectral
  norms and not for ℓ2?
- Is there a non-Euclidean analogue of multiple eigenvalues at the edge
  (C8)?
- Does the quadratic model diverge generically above `2/S` for general
  norms, as Figure 6 suggests?
