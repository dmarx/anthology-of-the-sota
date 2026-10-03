---
status: Active
title: 'Improving and generalizing flow-based generative models with minibatch optimal transport'
version: 1
tags:
- generative-modeling
- flows-and-transport
- training-optimization
date: '2026-10-03'
published: '2023-02-01'
arxiv: '2302.00482'
first_author: 'Tong'
keywords:
- 'conditional-flow-matching'
- 'minibatch-optimal-transport'
- 'ot-cfm'
- 'schrodinger-bridge'
- 'arbitrary-source-distribution'
- 'single-cell-dynamics'
implementations:
- 'torchcfm'
extends:
- LIT-630
compared_against:
- LIT-630
- LIT-644
- LIT-636
summary: >-
  Tong et al., Mila (2023), [ARXIV-2302.00482](https://arxiv.org/abs/2302.00482). Flow matching trains on any
  coupling of source and target samples. Pairing each minibatch by exact
  optimal transport (OT-CFM) gives near-OT paths in 2-D (normalized path
  energy 0.02–0.09 against 0.2–2.7 for the independent coupling, five seeds)
  at under 1% overhead. On CIFAR-10 its gain is small: adaptive-solver FID
  3.58 against 3.66 at 134 against 146 NFE, and the independent coupling is
  better at 1,000 Euler steps. Its rerun of the path comparison, at a recipe
  that beats Flow Matching's own, has the straight path ahead of VP at
  100 Euler steps (4.64 against 7.77).
---

# LIT-tmpzz36v: Improving and generalizing flow-based generative models with minibatch optimal transport

Tong, Fatras, Malkin, Huguet, Zhang, Rector-Brooks, Wolf and Bengio, Mila
(2023), TMLR 03/2024 — [ARXIV-2302.00482](https://arxiv.org/abs/2302.00482). Read at v4 (11 Mar 2024), main text
and Appendices A–E; v1 is 1 Feb 2023.

## Key takeaways

- **The coupling is a free choice** (§3.1–3.2, Table 1). Conditioning on a
  pair z = (x₀, x₁) drawn from any joint with the right marginals keeps the
  conditional flow-matching gradient equal to the marginal one (Thms.
  3.1–3.2). With the independent coupling and σ = 0 it is rectified flow's
  objective (I-CFM, §3.2.2). The source need not be Gaussian.
- **An OT coupling gives OT dynamics** (§3.2.3, Prop. 3.4). With the exact
  static OT plan and σ → 0, the learned field solves the dynamic OT problem.
  On data too large for exact OT, each minibatch is re-paired by exact
  discrete OT (Alg. 3). An entropic plan with a Brownian-bridge path gives
  the Schrödinger-bridge probability flow (SB-CFM, Prop. 3.5).
- **In 2-D the paths become near-optimal** (Table 2, five seeds). Normalized
  path energy is 0.018–0.087 for OT-CFM, against 0.222–2.738 for I-CFM and
  0.069–0.149 for 2-rectified flow, at similar 2-Wasserstein fit. The OT
  batch can be small: path energy plateaus at about 64 samples, under 0.5%
  of a 10K-point dataset (Fig. D.2).
- **On CIFAR-10 the gain is small** (§5.3, Table 5, one run each). FID at
  100 Euler steps / 1,000 Euler steps / adaptive dopri5: OT-CFM 4.443 /
  3.741 / 3.577 (133.94 NFE), I-CFM 4.461 / 3.643 / 3.659 (146.42 NFE).
  Fig. 3 shows OT-CFM ahead at low Euler NFE after 400K steps, as curves
  only. The OT solve costs under 1% per iteration.
- **The path comparison, rerun.** Under the same improved recipe, the straight
  path (OT-FM) scores 4.640 / 3.822 / 3.655 at 143 adaptive NFE, and the VP
  path (VP-FM) 7.772 / 4.048 / 4.335 at 526 (Table 5).
- **Beyond images** (§5.2, §5.4, App. D.2). On single-cell interpolation
  OT-CFM has the lowest average EMD on all three datasets (Table 4). In
  CelebA latent translation it has the lowest MMD (Table 6). It also fits an
  energy-defined funnel target, and is better than I-CFM and FM with
  10-step Euler (Table D.2).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"OT-CFM … lead[s] to faster inference"** (abstract). At 100 Euler steps
  the CIFAR-10 margin over I-CFM is 0.018 FID, and at 1,000 steps I-CFM is
  ahead by 0.098 (Table 5). The low-NFE advantage on images exists only in
  Fig. 3's curves. Each CIFAR number is one run.
- **"More efficient training."** Fig. 2 shows faster convergence per step on
  2-D validation error. Table D.1's wall-clock time to convergence on the
  same tasks is longer for OT-CFM (1.48 × 10³ s) than for I-CFM (1.05) or FM
  (1.01).
- **Flow Matching's CIFAR-10 number did not reproduce.** Following Lipman et
  al.'s stated procedure gave adaptive FID 11.53, against the reported 6.35
  (Table 5). The authors list what the paper leaves unspecified: FID sample
  count, σ_min, augmentation, source standard deviation, evaluation batch
  size, and conflicting epoch counts (footnote 3). Their own recipe is
  constant learning rate, gradient clipping, EMA, 128 channels and dropout
  0.1 (§5.3, App. E.8).
- **Minibatch OT is an approximation whose error grows with dimension**
  (§6). Prop. 3.4 is about the exact plan. No result here bounds the
  minibatch error on images.
- **Unconditional only.** No image experiment pairs samples under a class
  or text condition.

## Which comparisons are like for like

- **Table 5's "(ours)" rows** share architecture, optimizer, 400K steps and
  evaluation and differ only in path or coupling. The rows marked
  "reported" are other papers' numbers on other recipes.
- **Table 2** shares a 3×64 MLP and training protocol across CFM variants,
  but the CNF, regularized-CNF and ICNN baselines ran on a GPU while the CFM
  models ran on one CPU core. That matters for the timing columns, not the
  metrics.
- **2-RF and 3-RF in Table 2** are Rectified Flow's procedure run here on the
  same 2-D tasks.

## Standing in the anthology

It extends Flow Matching ([LIT-630](LIT-630.md)). The conditional objective becomes a
statement about any coupling of the two endpoints, so the source can be data
and the pairing can be chosen. It is also the record's evidence that Flow
Matching's CIFAR-10 FID of 6.35 cannot be reproduced from that paper's text.
It took a different recipe to beat it (3.66 with Flow Matching's own path),
and the comparison here is against that rerun.

Its rerun of the stochastic interpolant ([LIT-644](LIT-644.md)) under the same recipe
scores 4.009, against 10.27 as originally reported. Under one recipe the
interpolant's trigonometric path trails the straight one by 0.35 adaptive
FID, where the two papers' reported numbers differ by 3.92.

Rectified Flow ([LIT-636](LIT-636.md)) is the other way to straighten a flow, and in 2-D
it is compared directly. Two and three rounds of reflow give path energies
of 0.069–0.149 and 0.055–0.129. Minibatch OT reaches 0.018–0.087 in one
simulation-free training run.

**On [SOTA-266](../practices.d/SOTA-266.md) it is independent support for the straight half.** The group
is not the Meta, Stability or UT Austin authors of that practice's sources.
At a recipe that beats Flow Matching's own and with uniform timesteps, the
straight path beats the VP path on CIFAR-10: 4.640 against 7.772 at 100
Euler steps and 3.655 against 4.335 adaptive, at 143 against 526 NFE. The
gap is largest at few steps, as the practice says. It does not touch the
logit-normal half.

It also bears on [SOTA-266](../practices.d/SOTA-266.md)'s open question of mechanism, and it supports
[THEORY-106](../theory.d/THEORY-106.md)'s point that "straight" describes the conditional path, not the
marginal ODE. §3.2.1 says so directly: the straight conditional path "is not
in general an OT path" for the marginal. The coupling is the lever that
straightens the marginal, with the conditional path held fixed. In 2-D that
lever moves path energy by an order of magnitude. On CIFAR-10 it moves FID by
less than the path choice does. So a straighter marginal is not, by itself,
what [SOTA-266](../practices.d/SOTA-266.md)'s image results measure.

Filed without a NOTE: the takeaways come from one full reading of v4, main
text and Appendices A–E. Figs. 2, 3, D.2–D.8 are curves, and only values
stated in the text are quoted.
