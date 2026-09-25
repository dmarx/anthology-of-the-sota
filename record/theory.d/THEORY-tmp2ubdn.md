---
status: Active
title: 'A diffusion loss whose weighting falls monotonically with signal-to-noise is maximum likelihood on noise-augmented data; a non-monotone one is not a likelihood objective'
version: 1
tags:
- generative-modeling
- training-optimization
date: '2026-09-25'
source:
- LIT-tmpqjbx0
extends:
- THEORY-027
promote_when: >-
  Active for the identity, which is a theorem with a checkable proof. It would
  be narrowed by a demonstration that the noise-augmented ELBO a monotone
  objective optimizes ranks models differently from the clean-data ELBO on
  held-out data. That is the use the source proposes and does not test.
summary: >-
  Kingma and Gao (NeurIPS 2023), [LIT-tmpqjbx0](../literature.d/LIT-tmpqjbx0.md). Every standard diffusion loss
  is `½∫ w(λ) E‖ε̂ − ε‖² dλ` for an implied weighting. Integration by parts
  turns it into an expectation, over `p_w = dw/dt`, of the KL of the reverse
  process from time `t`. That is a distribution exactly when `w` decreases in
  log-SNR. The loss is then the expected ELBO of Gaussian-noise-augmented
  data, with the model told the noise level. v-MSE with a cosine schedule,
  flow matching on the OT path with uniform `t`, and InDI are monotone.
  ε-MSE with a cosine schedule, EDM, P2 and Min-SNR are not.
---

# THEORY-tmp2ubdn: A diffusion loss whose weighting falls monotonically with signal-to-noise is maximum likelihood on noise-augmented data; a non-monotone one is not a likelihood objective

## Source

Kingma and Gao (2023), [LIT-tmpqjbx0](../literature.d/LIT-tmpqjbx0.md), §4 and Appendix C.

## The account

Write the loss as `L_w = ½∫ w(λ) E‖ε̂ − ε‖² dλ`. The derivative in `t` of the
reverse-process KL from `t` is `½(dλ/dt)E‖ε − ε̂‖²`. Integrate by parts and,
with `w` normalized to 1 at the noisy end:

`L_w = E_{t ∼ p_w}[L(t; x)] + const`, with `p_w(t) = dw(λ_t)/dt`,

plus a point mass `w(λ_max)` at `t = 0`. `L(t; x)` is the expected negative ELBO
of `z_t`, the data with Gaussian noise added at level `t`. So:

- **If `w` is monotone** (decreasing in λ), `p_w` is a distribution. The
  objective is maximum likelihood on a noise-augmented family, with the model
  conditioned on the augmentation: DistAug.
- **If not**, `p_w` changes sign. The objective is a signed mixture of ELBOs and
  is not a likelihood objective.

## What it does and does not say

- **It is the ELBO of augmented data, not of the data.** Clean data gets only the
  small mass `w(λ_max)`.
- **It does not say monotone weightings sample better.** The source's own 64×64
  table shows parity: EDM-monotonic 1.43 against EDM 1.43. SD3's non-monotone
  logit-normal won its 61-way sweep at scale. What the theorem gives is an
  interpretation, not a ranking.
- **It carries [THEORY-027](THEORY-027.md) into the weighted case.** Given `w`, the loss
  depends on the schedule only through its endpoints, and the schedule's shape
  sets only the Monte Carlo variance. [THEORY-027](THEORY-027.md) is the unweighted special
  case, and it remains scoped to scalar schedules.
- **No practice is explained by it.** Plain rectified flow is monotone and SD3's
  logit-normal is not. Neither is recommended *because* of this, so `explains:`
  is empty on purpose.
