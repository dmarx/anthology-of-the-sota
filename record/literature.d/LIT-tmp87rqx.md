---
status: Active
title: 'Non-Euclidean Gradient Descent Operates at the Edge of Stability'
version: 1
tags:
- training-optimization
- model-stability
- analysis-and-evaluation
date: '2026-09-25'
published: '2026-03-05'
arxiv: '2603.05002'
first_author: 'Islamov'
keywords:
- 'edge-of-stability'
- 'directional-smoothness'
- 'generalized-sharpness'
- 'non-euclidean-gradient-descent'
- 'spectral-gradient-descent'
- 'signgd'
- 'frank-wolfe'
extends:
- LIT-461
implementations: []
summary: >-
  Islamov, Crawshaw, Cohen and Gower (ICML 2026), [ARXIV-2603.05002](https://arxiv.org/abs/2603.05002). Steepest
  descent under any norm — Spectral GD, ℓ∞-descent, Block CD, and the
  normalized forms SignGD and normalized Spectral GD — also sharpens to `2/η`
  and trains there, **if sharpness is measured in the update's own norm**:
  `max_{‖d‖=1} dᵀ∇²L d`. The ordinary top Hessian eigenvalue stays well below
  `2/η` for Spectral GD and ℓ∞-descent, so the Euclidean diagnostic misses the
  regime entirely. Full-batch, CIFAR-10 and Tiny Shakespeare scale; the
  non-Euclidean sharpness is a multi-restart Frank-Wolfe estimate, not an
  exact value.
---

<!-- inactive-ok-file: THEORY-024 THEORY-030 THEORY-033 — all Proposed, and named to say what this paper does not reach, not relied on -->

# LIT-tmp87rqx: Non-Euclidean Gradient Descent Operates at the Edge of Stability

Islamov, Crawshaw, Cohen and Gower (2026; ICML 2026, oral) — [ARXIV-2603.05002](https://arxiv.org/abs/2603.05002)

## Key takeaways

- **The edge of stability is a property of the update's norm, not of the
  Hessian's top eigenvalue.** For steepest descent under a norm `‖·‖` the
  quantity that sharpens to `2/η` and hovers there is the *generalized
  sharpness* `S_‖·‖(w) = max_{‖d‖=1} dᵀ∇²L(w)d`. Under ℓ2 it is `λ_max`, which
  is Cohen et al.'s sharpness; under a preconditioner norm it is the
  preconditioned-Hessian sharpness of the adaptive-EoS work. Under the
  spectral and ℓ∞ norms it is something new.
- **The Euclidean diagnostic fails for the optimizers people use.** On
  ResNet20 and VGG11 trained on CIFAR-10 with Spectral GD and with ℓ∞-descent,
  generalized sharpness stabilizes at `2/η` while `λ_max(∇²L)` "stays well
  below this threshold" throughout (Figures E.3, G.5). A practitioner
  monitoring the ordinary sharpness under a Muon-like update would conclude
  the run is not at the edge of stability when it is.
- **The identity that does the work is one line.** With directional
  smoothness defined as the exact second-order remainder along the step,
  `ΔL_t = −η(1 − (η/2)·D(w_t, w_{t+1}))·‖∇L‖²_*`, so the loss falls iff
  `D ≤ 2/η`. A loss that decreases and then oscillates forces `D` to rise to
  `2/η` and oscillate around it — "almost by definition", in the authors'
  own words. Generalized sharpness is motivated from this by assuming the
  Hessian is roughly constant along the step.
- **Normalized methods sit at a gradient-scaled threshold.** SignGD and
  normalized Spectral GD are the unnormalized updates at effective step
  `η/‖∇L‖_*`, so the ratio `S/‖∇L‖_*` hovers at `2/η` (Figure 5). Cohen et
  al.'s adaptive-EoS characterization of RMSprop, by contrast, holds only
  for `β₂` near 1 and breaks down as `β₂ → 0`, where RMSprop becomes SignGD
  (Figure H.1).
- **The quadratic theory is only half there.** On a quadratic, non-Euclidean
  GD converges linearly when `S < 2/η` (Theorem 5.1). Above it the authors
  prove divergence only from one line of initializations with a chosen
  dual-gradient selection (Theorem 5.2) — weaker than the Euclidean case, and
  they say so. Empirically the quadratic Taylor model does diverge at EoS
  (Figure 6).
- **A regime Euclidean GD does not have.** Under ℓ∞ and spectral norms the
  directional smoothness starts climbing and the network's outputs start
  oscillating *before* generalized sharpness reaches `2/η`, without the
  quadratic model diverging (Appendix B). The authors leave it unexplained.

## Standing in the anthology

**It is the paper that joins the record's two optimizer clusters.** One half
is the edge of stability — LIT-461, which this extends and whose code
it is built on, and LIT-453, whose account of multiple unstable
eigenvalues it borrows to explain why its own sharpness sits slightly above
`2/η`. The other half is steepest descent under a non-Euclidean norm — the
frame of LIT-438 and of THEORY-024, contested by LIT-456, which
cites this paper. It was named in the curation journal on 2026-09-20 as the
link between them and carried as unfiled through five entries.

**What it adds to the record's account of the edge of stability** is the
statement that THEORY-035's "maximum eigenvalue of the training-loss
Hessian" is the right quantity for Euclidean gradient descent only. For the
spectral update the record recommends (SOTA-121), the equilibrium
is at `2/η` in the spectral geometry and the Euclidean eigenvalue is far from
it. That is a refinement, not a correction: LIT-461 never claimed more
than gradient descent.

**What it does not do** is bear on why spectral optimizers work. It measures
where their stability threshold sits, not whether the geometry is what pays;
no optimizer is compared with another on loss, and nothing here tests the
`Kaon` result. It does not reach THEORY-024 or THEORY-033
in either direction. See NOTE-tmpf0zmh.

**Scope.** Full-batch, deterministic, no momentum; MLPs, small CNNs, ResNet20
and VGG11 on CIFAR-10 (often a 5k subset) with MSE loss, and a Transformer on
Tiny Shakespeare. The authors name stochastic, momentum-based and adaptive
optimizers as the extension that would make the diagnostic usable in
practical training — which is the same gap THEORY-035 and
THEORY-030 already name.
