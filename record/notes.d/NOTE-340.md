---
number: 340
status: Read
formerly:
- NOTE-tmpa4mlk
paper: LIT-630
title: 'Flow Matching'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    ADM is now held, LIT-tmpcq7qo, read in full. Its Table 11 confirms the
    run this note audits against (ImageNet 128×128, 4360K iterations, batch 256,
    422M parameters) and adds that it is class-conditional, while Flow Matching's
    ImageNet-128 model is unconditional. C7's "not a controlled one" gains a
    second reason; its strength is unchanged.
date: '2026-09-24'
summary: >-
  Regressing onto a per-sample conditional vector field trains a continuous
  normalizing flow without simulation, with the same gradient as the
  intractable marginal objective. With the U-Net, hyperparameters and epochs
  held fixed, the straight "OT" path beats the VP diffusion path under that
  objective at CIFAR-10 and ImageNet 32/64 with uniform timesteps (FID 6.35
  against 8.06 on CIFAR-10). The objective's own advantage over score
  matching is mixed, and the likelihood gains at ImageNet scale are 0.01 bpd.
---

<!-- inactive-ok-file: SOTA-333 SOTA-386 SOTA-389 SOTA-390 — Proposed, and cited here to weigh the evidence for them; this document is part of that evidence, not an endorsement -->

# NOTE-340: Flow Matching

Read in full from arXiv v2 (8 Feb 2023): the main text, and Appendices A–F,
including the proofs of Theorems 1–3, the probability-flow derivations
(App. D), the hyperparameters (Table 3) and the likelihood estimates
(Table 4). Figures were read from their captions and axis labels. Figures 5,
7 and 10 give no values in the text, so this note quotes no numbers from
them except where the text states one.

## Contribution

A training objective for continuous normalizing flows that needs no ODE
solve in the loop. Conditional Flow Matching (CFM) regresses the network
onto a vector field defined for one data sample at a time. The paper proves
that this has the same gradient as regressing onto the marginal field, which
cannot be computed. Diffusion paths become one choice of conditional path
among many. The paper singles out a linear path, which it calls "OT", and
compares it with the VP path under the same objective.

## Key insight

**Pick the path, not the process.** Once the objective is per-sample, the
thing a modeller chooses is a family of conditional Gaussians
p_t(x|x1) = N(μ_t(x1), σ_t(x1)²I), and the vector field follows in closed
form. A diffusion SDE is one way to pick μ_t and σ_t. Setting both linear in
t gives straight conditional trajectories whose direction does not change
over time, which the paper argues is "arguably" an easier regression target
(§4.1, Fig. 2).

## Assumptions

- **p_t(x) > 0 for all x and t** (Thm. 2). Theorem 1 also needs the
  integrands to satisfy the Leibniz rule. The proof of Theorem 2 assumes q
  and p_t(x|x1) decay fast enough for Fubini, and that u_t, v_t and ∇θv_t
  are bounded (App. A).
- **Gaussian conditional paths** with μ_0 = 0, σ_0 = 1, μ_1 = x1 and
  σ_1 = σ_min (Eq. 10). The conditional flow is fixed to the affine map
  ψ_t(x) = σ_t(x1)·x + μ_t(x1). Infinitely many vector fields generate the
  same path, and this is a choice (§4).
- **Timesteps uniform:** t ~ U[0, 1] (Eq. 5).
- **Pixel space and unconditional images** at 32–128 px, plus one
  64→256 super-resolution task.

## Key results

- **Theorem 1.** The marginal field u_t(x) = ∫ u_t(x|x1) p_t(x|x1) q(x1) /
  p_t(x) dx1 (Eq. 8) generates the marginal path p_t(x) (Eq. 6).
- **Theorem 2.** L_CFM and L_FM differ by a constant independent of θ, so
  ∇θL_FM = ∇θL_CFM.
- **Theorem 3.** For a Gaussian path the unique field defining ψ_t is
  u_t(x|x1) = (σ'_t(x1)/σ_t(x1))·(x − μ_t(x1)) + μ'_t(x1) (Eq. 15).
- **The OT path** is μ_t = t·x1 and σ_t = 1 − (1 − σ_min)t (Eq. 20). Its
  regression target is x1 − (1 − σ_min)·x0 (Eq. 23). With σ_min = 0 this is
  Rectified Flow's x1 − x0. The VP path is trained on t ∈ [0, 1 − ε] with
  ε = 10⁻⁵ (App. E.1). The OT field is defined on all of [0, 1].
- **Table 1**, same model trained with each method (FID / NLL in bpd /
  NFE for dopri5 at tolerance 1e-5):

  | method | CIFAR-10 | ImageNet-32 | ImageNet-64 |
  |---|---|---|---|
  | DDPM | 7.48 / 3.12 / 274 | 6.99 / 3.54 / 262 | 17.36 / 3.32 / 264 |
  | Score Matching | 19.94 / 3.16 / 242 | 5.68 / 3.56 / 178 | 19.74 / 3.40 / 441 |
  | ScoreFlow | 20.78 / 3.09 / 428 | 14.14 / 3.55 / 195 | 24.95 / 3.36 / 601 |
  | FM w/ Diffusion | 8.06 / 3.10 / 183 | 6.37 / 3.54 / 193 | 16.88 / 3.33 / 187 |
  | FM w/ OT | 6.35 / 2.99 / 142 | 5.02 / 3.53 / 122 | 14.45 / 3.31 / 138 |

- **ImageNet-128:** FID 20.9 and NLL 2.90, compared only against GANs
  (Table 1, right). The model is 25% larger than ADM's, trained for 500k
  iterations at batch 1,536 (Table 3). The paper calls that "33% less image
  throughput" than ADM's 4.36M iterations at batch 256 (§6.1). That ADM run
  (LIT-tmpcq7qo, Table 11: 422M parameters) is **class-conditional**; this
  model is not.
- **Sampling cost:** at a fixed ODE error, FM-OT needs "roughly only 60% of
  the NFEs" of the diffusion-path models (§6.2, Fig. 7). That is measured on
  ImageNet-32 with the midpoint solver against 1,000-NFE references on 256
  seeds.
- **Super-resolution 64→256** (Table 2): FID 3.4 against SR3's 5.2, IS 200.8
  against 180.1. PSNR is lower at 24.7 against 26.4, and SSIM at 0.747
  against 0.762. The text calls these "similar".

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | CFM has the same gradient as the marginal FM objective | strong | Theorem 2, proved under the stated regularity |
| C2 | VE and VP diffusion are special cases, and the diffusion conditional field coincides with the probability-flow ODE field | strong | Eqs. 16–19 and App. D derivation |
| C3 | At fixed architecture, hyperparameters and epochs, the OT path gives lower FID than the VP path under FM | strong | Table 1, three datasets, both FM rows. App. E fixes epochs for exactly these two |
| C4 | FM with the diffusion path trains better than score matching on the same path | weak | Table 1 is mixed. FM-Dif beats Score Matching on FID at CIFAR-10 and ImageNet-64 and loses at ImageNet-32 (6.37 against 5.68). It loses to DDPM at CIFAR-10 (8.06 against 7.48). Baseline budget is unclear (see Limitations) |
| C5 | FM-OT has "consistently better" likelihood | weak | 0.01 bpd over the nearest competitor at ImageNet-32 and 64 (Table 1). At K = 1 on ImageNet-32 it ties DDPM at 3.62 (Table 4). CIFAR-10 is 0.10 |
| C6 | The OT path samples with fewer function evaluations | moderate | Adaptive NFE lower on all three datasets (Table 1). The "60%" is one figure, one dataset, one solver (Fig. 7) |
| C7 | FM converges faster in training | weak | Fig. 5 curves on ImageNet-64 with no values in text. The ImageNet-128 throughput comparison is against ADM's published run, not a controlled one, and that run is class-conditional while FM's is not (LIT-tmpcq7qo, Table 11) |
| C8 | Sampling cost stays constant during FM training and drifts under score matching | weak | Fig. 10, CIFAR-10, figure only |

## Method

Choose μ_t and σ_t. Sample t ~ U[0, 1], a data point x1 and noise x0. Form
x = ψ_t(x0) = σ_t·x0 + μ_t, and regress v_t(x; θ) onto dψ_t/dt with a plain
squared error (Eq. 14). For the OT path the target is x1 − (1 − σ_min)x0.
Sample by integrating dx/dt = v_t from t = 0 to 1 with an off-the-shelf
solver (dopri5 by default). The network is the Dhariwal & Nichol U-Net with
minimal changes, trained with Adam and polynomial-decay or constant learning
rates (Table 3). Likelihood uses the instantaneous change of variables with
a Hutchinson trace estimator and uniform dequantization (App. C, E.2).

## Concepts

- **Conditional probability path:** a path defined for one data point x1,
  from N(0, I) at t = 0 to N(x1, σ_min²I) at t = 1. Its mixture over the
  data is the marginal path the model learns.
- **OT path:** named for the conditional map, which is the McCann
  displacement interpolant between two Gaussians. The paper warns that "this
  by no means imply that the marginal VF is an optimal transport solution"
  (§4.1).
- **Simulation-free:** training draws x from p_t(x|x1) directly and never
  integrates the ODE.

## Connections

It generalizes denoising score matching (Vincent) from scores to vector
fields, and Theorem 1 can also be derived from Peluchetti's diffusion
mixture representation, as the paper says (§3.1). It is concurrent with
Rectified Flow ([LIT-636](../literature.d/LIT-636.md), same target at σ_min = 0) and Albergo
and Vanden-Eijnden's stochastic interpolants (§5). Its OT path is the
objective that SD3 and the video reports now train with.

## Recommendations

- **R1.** When training a flow or diffusion model with a Gaussian path,
  prefer the linear (OT) path to the VP path. *Topic:* generative-modeling.
  *Status:* standard. *Strength:* strong at the scales tested (C3).
  *Conditions:* pixel space, unconditional, 32–64 px, uniform timesteps.
  Evidence above 64 px here is not controlled.
- **R2.** Do not expect the FM objective alone, on a diffusion path, to beat
  a tuned ε-prediction baseline. *Topic:* generative-modeling. *Status:*
  experimental. *Strength:* weak (C4). *Conditions:* the gain in Table 1 is
  carried by the path, not the objective.
- **R3.** Quote likelihood gains in bpd with the dequantization estimator
  and K. *Topic:* analysis-and-evaluation. *Status:* standard. *Strength:*
  moderate. *Conditions:* Table 4 shows K changes rankings at the 0.01 level.

## Bearing on the record

| practice | disposition |
|---|---|
| [SOTA-266](../practices.d/SOTA-266.md) straight path plus logit-normal timesteps | **confirmed** for the straight-path half, with a sharpening below |
| [SOTA-203](../practices.d/SOTA-203.md) higher-order solver on trained weights | consistent: Fig. 7 runs Euler, midpoint and RK4 on the same weights, figure only |
| [SOTA-195](../practices.d/SOTA-195.md) predict v rather than ε | consistent, not tested. FM's target is a velocity, and the VP path must stop at 1 − ε |
| [SOTA-188](../practices.d/SOTA-188.md) | no bearing. The timesteps are uniform and nothing about unit variance is tested |
| [SOTA-386](../practices.d/SOTA-386.md), [SOTA-333](../practices.d/SOTA-333.md), [SOTA-187](../practices.d/SOTA-187.md), [SOTA-390](../practices.d/SOTA-390.md), [SOTA-389](../practices.d/SOTA-389.md) | no bearing. Pixel-space images only, no latent, no video, no captions |

[SOTA-266](../practices.d/SOTA-266.md) v2 cites Table 1 as "the same U-Net, hyperparameters and epochs
give CIFAR-10 FID 6.35 on the straight path against 8.06 on the diffusion
path". That is correct. The epoch parity comes from App. E, which names
FM-OT and FM-Diffusion among the three methods trained for the same number
of epochs. So the path comparison is untouched by the budget inconsistency
below, which bears only on the objective comparison against DDPM, Score
Matching and ScoreFlow. The ImageNet-32 (5.02 against 6.37) and ImageNet-64
(14.45 against 16.88) pairs could be added to [SOTA-266](../practices.d/SOTA-266.md) as replication
within the paper.

## Limitations

- **The budget statement conflicts with itself.** §6.1 says "All models are
  trained using the same architecture, hyperparameter values and number of
  training iterations, where baselines are allowed more iterations for
  better convergence." That one sentence says both "same" and "more". App. E
  and E.2 say "the same number of Epochs" for three methods: FM-OT,
  FM-Diffusion and SM-Diffusion. DDPM and ScoreFlow are not named. A
  consistent reading is that those two got more iterations and the three
  named ones were matched. Score Matching is both a named method and a
  baseline, so the conflict holds there. Table 3 gives one iteration count
  per dataset. Either way, the budget was equal or favoured the baselines.
- **σ_min is never given a value**, although the OT target depends on it.
- **CIFAR-10 FIDs are high** (6.35 at best). The authors attribute this to
  an architecture "not optimized for CIFAR-10" (§6.1).
- **ImageNet-128 is not a controlled comparison.** It is against GANs from
  the literature, and IC-GAN is excluded because it is conditional.
- **No seeds or variance** anywhere. Every Table 1 cell is one run.
- **The straight-path story is about conditional paths.** The marginal
  trajectories are not measured for straightness. Fig. 6 shows noise
  removed "roughly linearly", which is qualitative.

## Open questions

- Is the OT advantage from straightness or from the weighting over t that
  the linear schedule implies? No experiment separates them. Rectified
  Flow's Fig. 5 toy is the closest ([LIT-636](../literature.d/LIT-636.md)).
- Does the gap hold with logit-normal timesteps on both paths? SD3 suggests
  the ranking depends on the timestep distribution at scale.
- What σ_min was used, and does it matter?

## Corrections to the LIT note

- **"App. E.2 says all methods trained 'for the same number of Epochs'…
  the two sentences cannot both be true."** App. E.2 says "All methods we
  trained (i.e., FM-OT, FM-Diffusion, SM-Diffusion)". It names three of the
  five Table 1 rows. Fix: "§6.1 contradicts itself in one sentence ('same
  number of training iterations, where baselines are allowed more
  iterations'). App. E fixes epochs for FM-OT, FM-Diffusion and Score
  Matching and says nothing about DDPM or ScoreFlow. The two statements
  conflict only for Score Matching. The OT-against-diffusion path comparison
  is matched under every reading."
- **"Either way the comparison favours the baselines."** Fix: "Either way
  the budget was equal to or favoured the baselines."
- **"'Consistently better likelihood' is 0.01–0.02 bpd at ImageNet-32 and
  64."** The margin over the nearest competitor is 0.01 at both. 0.02 is the
  margin over FM-Diffusion at ImageNet-64 only. At K = 1 on ImageNet-32,
  FM-OT ties DDPM at 3.62 (Table 4). Fix: "0.01 bpd over the next-best model
  at ImageNet-32 and 64, and a tie with DDPM at K = 1 on ImageNet-32."
