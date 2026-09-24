---
number: 337
status: Read
formerly:
- NOTE-tmp77r8c
paper: LIT-636
title: 'Rectified Flow'
version: 1
date: '2026-09-24'
summary: >-
  Regressing a velocity onto x1 − x0 along the straight interpolation gives
  an ODE that preserves the marginals and does not increase any convex
  transport cost, and retraining on its own couplings ("reflow") provably
  straightens it at O(1/K). On CIFAR-10 the single-pass model scores FID
  2.58 against 3.93 for the VP probability-flow ODE at the same
  architecture, with training budget unstated. Most of the one-step result
  comes from distillation (378 → 6.18 with no reflow), and reflow adds
  6.18 → 4.85.
---

<!-- inactive-ok-file: SOTA-333 SOTA-386 SOTA-389 SOTA-390 — Proposed, and cited here to weigh the evidence for them; this document is part of that evidence, not an endorsement -->

# NOTE-337: Rectified Flow

Read in full from arXiv v1 (7 Sep 2022), which is the only version in the
scratchpad: §§1–5, the proofs in §3, and Appendix A with Algorithms 2–4 and
Figs. 16–21. Figures were read from captions. Fig. 8, the FID and recall
curves against step count, gives no values in the text. So this note uses
the text's "N ⪅ 80" and no other numbers from it.

## Contribution

A single least-squares objective for learning an ODE between any two
distributions π0 and π1. It serves noise-to-data generation and unpaired
domain transfer without change. Two results come with it. The first is a
theory of **rectification**, which turns any coupling into a deterministic
one with no larger convex transport cost. The second is **reflow**, which
repeats the procedure on the model's own couplings and provably straightens
the paths. The paper also shows that probability-flow ODEs and DDIM are
"nonlinear rectified flows" with curved interpolants.

## Key insight

**Linear interpolation paths cross, and an ODE's paths cannot.** Fitting
v(x, t) to the average direction x1 − x0 through each point "rewires" the
crossing lines into non-crossing ones with the same marginals (Fig. 2).
Because this rewiring never lengthens a path, transport cost falls. A
coupling whose interpolation paths never cross is a fixed point, and its
flow is exactly straight. A straight flow can be simulated in one Euler
step.

## Assumptions

- **Rectifiability** (Def. 3.2): v^X is locally bounded, and the ODE
  dZ_t = v^X(Z_t, t)dt has a unique solution. §2.2 notes this can fail when
  X0 | X1 has no conditional density, and suggests adding Gaussian noise to
  X0.
- **Exact minimizers.** Every theorem is about v^X(x, t) = E[X1 − X0 |
  X_t = x], the conditional expectation, not a fitted network.
- **Linear interpolation** for Theorems 3.5–3.7. Theorem 3.5 extends to
  straight paths at non-constant speed only for convex costs that are
  m-homogeneous with m ∈ (0, 1] (§3.2).
- **E‖X1 − X0‖² < ∞** for the O(1/K) rate (Thm. 3.7).
- **Optimality only in one dimension.** Straight and c-optimal coincide on
  ℝ (Thm. 3.10). For d ≥ 2 a straight coupling need not be optimal for any
  given c (§3.4).

## Key results

- **Marginal preservation** (Thm. 3.3): Law(Z_t) = Law(X_t) for all t. This
  holds for any differentiable interpolation, linear or not.
- **Convex cost** (Thm. 3.5): E[c(Z1 − Z0)] ≤ E[c(X1 − X0)] for every
  convex c.
- **Straightening rate** (Thm. 3.7): with straightness
  S(Z) = ∫₀¹ E‖(Z1 − Z0) − Ż_t‖² dt (Eq. 3) and V the non-intersection
  measure (Eq. 12),
  Σ_{k=0}^{K} [S(Z^{k+1}) + V((Z^k_0, Z^k_1))] ≤ E‖X1 − X0‖²,
  so min_{k≤K} of that sum is O(1/K). §2.2 states the looser form
  min_k S(Z^k) ≤ E‖X1 − X0‖² / K.
- **PF-ODEs as nonlinear rectified flows** (Prop. 3.11): the VE, VP and
  sub-VP objectives are instances of Eq. 6 with X_t = α_t X1 + β_t ξ.
  §2.3 argues, and Fig. 4 shows in a 2-D toy, that reflow does not
  straighten them because their interpolants are curved.
- **CIFAR-10, DDPM++ architecture** (Table 1a), FID (distilled in
  parentheses):

  | model | 1 Euler step | RK45 (NFE) |
  |---|---|---|
  | 1-rectified flow | 378 (6.18) | 2.58 (127) |
  | 2-rectified flow | 12.21 (4.85) | 3.36 (110) |
  | 3-rectified flow | 8.15 (5.21) | 3.96 (104) |
  | VP ODE | 451 (16.23) | 3.93 (140) |
  | sub-VP ODE | 451 (14.32) | 3.16 (146) |

  VP SDE and sub-VP SDE at 2,000 Euler steps score 2.55 and 2.61. Recall
  for 1-rectified flow under RK45 is 0.57.
- **Domain adaptation** (Table 2): OfficeHome 69.2 ± 0.5 against Deep
  CORAL's 68.7 ± 0.3. DomainNet 41.4 ± 0.1 against CORAL's 41.5 ± 0.2.
- **Reflow cost** (App. A): each reflow simulates 4 million (z0, z1) pairs
  from the previous flow and fine-tunes for 300,000 steps. The solver used
  to generate the pairs is not stated.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The rectified flow preserves the marginals and never increases a convex transport cost | strong | Thms. 3.3 and 3.5, for exact minimizers under rectifiability |
| C2 | Reflow straightens the flow at O(1/K) | strong | Thm. 3.7, for exact minimizers. Empirically Figs. 3, 9 and 10 |
| C3 | The linear interpolation "should be recommended as a default choice" | moderate | Theorems plus one CIFAR-10 table at one architecture. Budget parity with the VP rows is not stated |
| C4 | 1-rectified flow beats VP and sub-VP PF-ODEs at full simulation | moderate | Table 1a: 2.58 against 3.93 and 3.16 at the same architecture. It does not beat the 2,000-step VP SDE (2.55) |
| C5 | Reflow improves few-step sampling | moderate | Table 1a at N = 1: 378 → 12.21 → 8.15. Fig. 8 for N ⪅ 80 |
| C6 | Reflow degrades full-simulation quality | moderate | Table 1a: 2.58 → 3.36 → 3.96. The paper attributes this to accumulated estimation error, which is asserted |
| C7 | One-step FID 4.85 is state of the art for one-step models | weak | True only against diffusion/flow and "U-Net" GANs (Table 1b, literature numbers). StyleGAN2+ADA (2.92) and StyleGAN-XL (1.85) are lower |
| C8 | Rectified flow is state of the art on domain adaptation | weak | Table 2: first on OfficeHome by 0.5, second on DomainNet by 0.1 |
| C9 | VP/sub-VP ODE paths have non-uniform speed, and a linear α_t removes it with the same trajectories | weak | Fig. 5 last column, a 2-D toy, qualitative |

## Method

Draw (X0, X1) from any coupling, usually independent. Sample t ~ U[0, 1] and
regress v(tX1 + (1 − t)X0, t) onto X1 − X0 (Alg. 1, Alg. 2). Sample by Euler
with step 1/N or by RK45 at Song et al.'s tolerances. For reflow, simulate
the trained flow from fresh X0 to get a new coupling (Z0, Z1) and train
again on it (Alg. 4). To distil to k steps, fine-tune with t drawn from
{0, 1/k, …, (k − 1)/k}. For k = 1 the loss is LPIPS rather than L2
(App. A). CIFAR-10 training used Adam at 2e-4, dropout 0.15 and EMA 0.999999.
The number of iterations for the 1-rectified flow is not stated.

## Concepts

- **Rectify / rectified coupling:** the map from a coupling (X0, X1) to the
  endpoints (Z0, Z1) of its rectified flow.
- **k-rectified flow:** the flow after k − 1 reflows. The "1-rectified flow"
  is what later work simply calls rectified flow.
- **Straight coupling:** a fixed point of Rectify. Equivalently, its linear
  interpolation paths do not intersect (Thm. 3.6).
- **Straightness S(Z):** the mean squared deviation of the velocity from
  the chord (Eq. 3). Zero means one Euler step is exact.

## Connections

It is concurrent with Flow Matching ([LIT-630](../literature.d/LIT-630.md)), whose OT path at σ_min = 0
gives the same target, and with stochastic interpolants. It reframes the
DDIM and probability-flow ODE line as curved special cases (§2.3.1, §3.5).
It also argues, in prose, that ODEs should be preferred to SDEs (§4). SD3
([LIT-449](../literature.d/LIT-449.md)) takes its name and its single-pass objective. InstaFlow later used
the reflow-then-distil pipeline for text-to-image.

## Recommendations

- **R1.** Use the linear interpolation with a velocity target as the
  default single-pass objective. *Topic:* generative-modeling. *Status:*
  standard. *Strength:* moderate (C3, C4). *Conditions:* one pixel-space
  CIFAR-10 comparison, budget parity unstated.
- **R2.** If one-step sampling is the goal, distil first and measure
  whether reflow adds enough to pay for itself. *Topic:*
  inference-optimization. *Status:* experimental. *Strength:* moderate.
  *Conditions:* on CIFAR-10, distillation alone takes one-step FID from 378
  to 6.18. One reflow before distilling takes it to 4.85, at the cost of 4M
  simulated pairs and 300k steps.
- **R3.** Do not reflow a model that will be sampled with many steps.
  *Topic:* generative-modeling. *Status:* experimental. *Strength:*
  moderate (C6). *Conditions:* each reflow raised full-simulation FID in
  Table 1a.

## Bearing on the record

| practice | disposition |
|---|---|
| [SOTA-266](../practices.d/SOTA-266.md) straight path plus logit-normal timesteps | **confirmed** for the single-pass straight path with uniform t. The wording about this paper's comparison should be softened (below) |
| [SOTA-206](../practices.d/SOTA-206.md) keep a multi-step option in a few-step model | supporting evidence on the cost side. Reflow buys few-step quality and loses many-step quality (C6), and a k-step distilled model is fixed at k |
| [SOTA-203](../practices.d/SOTA-203.md) higher-order solver on trained weights | weakly consistent. RK45 needs 127 NFE for 1-RF against 140 for the VP ODE |
| [SOTA-195](../practices.d/SOTA-195.md) predict v rather than ε | consistent. The target is a velocity |
| [SOTA-386](../practices.d/SOTA-386.md), [SOTA-333](../practices.d/SOTA-333.md), [SOTA-187](../practices.d/SOTA-187.md), [SOTA-390](../practices.d/SOTA-390.md), [SOTA-389](../practices.d/SOTA-389.md) | no bearing. Pixel-space images only |

[SOTA-266](../practices.d/SOTA-266.md) v2 says both originating papers "won their controlled comparisons
against VP diffusion in pixel space ([LIT-636](../literature.d/LIT-636.md) Table 1a)". Two sharpenings.
First, Table 1a is at most partly controlled. The architecture is shared,
but the training budget is not stated, and the text does not say whether
the VP rows were retrained. Second, the win is against the VP
*probability-flow ODE* (3.93) and sub-VP ODE (3.16). The 2,000-step VP SDE
(2.55) is level with the 1-rectified flow (2.58). A practice citing this
table should say "beats the VP probability-flow ODE at equal architecture".

A practice candidate the record lacks is R2, the separation of reflow from
distillation. [LIT-636](../literature.d/LIT-636.md) currently reads the one-step result as reflow's.

## Limitations

- **The theory is about exact minimizers.** How much a fitted network
  departs from v^X, and whether that departure is what hurts reflowed
  models at many steps, is not measured.
- **Straightness is shown for the reflowed model.** The 1-rectified flow is
  not straight (Fig. 10). The first reflow is the one that makes 1-step
  sampling usable.
- **One quantitative image benchmark.** 256 px generation (Fig. 11) and
  image-to-image translation (Figs. 13–15) are qualitative. The translation
  experiments use a classifier-weighted loss (Eq. 20), not the plain
  objective.
- **No seeds or variance** for CIFAR-10. Table 2 reports ± values, and the
  DomainNet gap is inside them.
- **The GAN comparisons are literature numbers** at different
  architectures (Table 1b).

## Open questions

- How much of reflow's one-step gain survives when distillation is strong?
  6.18 against 4.85 is one comparison.
- Why does reflow cost quality at many steps? Accumulated estimation error
  is the stated guess.
- Does the straight-path advantage come from path shape or from path speed?
  Fig. 5's constant-speed VP column separates them in 2-D only.

## Corrections to the LIT note

- **Summary: "The 'fast' in the title needs 'reflow'. Without it, one-step
  FID is 378. After one reflow it is 12.2."** Table 1a's parenthesized
  column gives 6.18 for the 1-rectified flow distilled with no reflow. Fix:
  "Without reflow or distillation one-step FID is 378. Distillation alone
  gives 6.18. One reflow gives 12.21 undistilled and 4.85 distilled."
- **Key takeaways, "Few steps need reflow."** Same issue. Few steps need
  reflow *or distillation*, and distillation does most of the work in Table
  1a.
- **"Probability-flow ODEs and DDIM are nonlinear rectified flows, and
  reflow does not straighten them (Prop. 3.11, Fig. 4)."** Prop. 3.11
  proves only the equivalence. The non-straightening is argued in §2.3 and
  shown in a 2-D toy (Fig. 4). Fix: "(Prop. 3.11 for the equivalence; §2.3
  and a 2-D toy in Fig. 4 for the non-straightening)".
- **"At full simulation the straight path beats VP."** Add: "the VP
  probability-flow ODE. The 2,000-step VP SDE scores 2.55."
