---
status: Active
title: 'Multisample Flow Matching: Straightening Flows with Minibatch Couplings'
version: 1
tags:
- generative-modeling
- flows-and-transport
- inference-optimization
- training-optimization
date: '2026-10-03'
published: '2023-04-28'
arxiv: '2304.14772'
first_author: 'Pooladian'
keywords:
- 'multisample-flow-matching'
- 'joint-cfm'
- 'batch-optimal-transport'
- 'stable-matching-coupling'
- 'straightness'
- 'gradient-variance'
extends:
- LIT-630
compared_against:
- LIT-630
- LIT-636
- LIT-036
- LIT-722
- LIT-tmpuz24v
summary: >-
  Pooladian et al., Meta AI, NYU and Weizmann (2023), [ARXIV-2304.14772](https://arxiv.org/abs/2304.14772).
  Flow matching with noise and data paired within each minibatch by OT
  (BatchOT) or a cheaper stable matching keeps the marginals exact. As batch
  size grows the paths straighten toward the OT map. On ImageNet-64 the
  FID-20 point drops from 29 Euler steps to 12, and adaptive FID from 13.93
  to 12.37, at equal likelihood and 4% more time per iteration. Low-NFE
  numbers stay far from one-step quality: 38.86 FID at 4 Euler steps on
  ImageNet-32. One run per row.
---

<!-- inactive-ok-file: SOTA-tmphvn35 — Proposed practices this paper is the source of, named in its standing -->
<!-- inactive-ok-file: SOTA-392 — Proposed; named to say minibatch couplings are not an alternative to its few-step students -->

# LIT-tmprjg3i: Multisample Flow Matching: Straightening Flows with Minibatch Couplings

Pooladian, Ben-Hamu, Domingo-Enrich, Amos, Lipman and Chen, Meta AI (FAIR),
NYU and Weizmann Institute (2023), ICML 2023 — [ARXIV-2304.14772](https://arxiv.org/abs/2304.14772). Read at v2
(24 May 2023), main text and Appendices A–E; v1 is 28 Apr 2023.

## Key takeaways

- **Any marginal-preserving coupling is allowed** (§3, Eq. 15, Lemma 3.1).
  The Joint CFM objective regresses onto the conditional field for pairs
  drawn from q(x₀, x₁). Its value bounds the gradient variance at fixed
  (x, t) (Lemma 3.2), so a coupling with a low optimum trains with less
  noise.
- **The multisample construction keeps marginals exact** (§4, Lemma 4.1).
  Draw k noises and k data points and pair them by a doubly stochastic
  matrix. The options are uniform (the independent CondOT baseline), exact
  BatchOT, Sinkhorn BatchEOT, Gale–Shapley Stable matching, or a heuristic.
  As k → ∞ under BatchOT, the objective's optimum, the straightness S and
  the transport cost's gap to W₂² all go to zero (Thm. 4.2). The cost falls
  monotonically in k (Thm. D.8).
- **Fewer steps for the same FID** (Table 1, Fig. 3). To reach FID 10 on
  ImageNet-32 takes 20 Euler steps with CondOT, 14 with BatchOT or Stable.
  To reach FID 20 on ImageNet-64 takes 29 with CondOT, 12 with BatchOT, 11
  with Stable. Diffusion baselines need 40 or more.
- **No loss elsewhere** (Table 6). Bits per dimension are equal: 3.58 on
  ImageNet-32 and 3.27 on ImageNet-64 for both CondOT and BatchOT. Adaptive
  FID improves, 5.04 → 4.68 and 13.93 → 12.37. Stable gets 11.82 on
  ImageNet-64. Estimated conditional-field variance falls, 594 → 507 and
  1880 → 1733.
- **Samples change less with step count** (Table 3). Inception-feature
  distance between an m-step sample and a near-exact one from the same noise
  is lower for BatchOT at every m: at m = 4, 0.101 against 0.141 on
  ImageNet-32 and 0.157 against 0.174 on ImageNet-64.
- **Cheap** (Table 9). Solving the couplings adds 0.8% per iteration on
  ImageNet-32 and 3.9% on ImageNet-64.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Reduce the required sampling cost by 30% to 60%"** (§1) is read off
  the threshold crossings of Fig. 3 (Table 1). The CondOT curves have no
  table, so fixed-NFE gaps against CondOT are figure-only. Tables 7–8 give
  Euler and midpoint numbers for BatchOT and Stable against DDPM and
  ScoreSDE only.
- **"At no degradation in performance."** The likelihoods tie to two
  decimals. Adaptive-solver FID does not. Only BatchOT beats CondOT at both
  resolutions. On ImageNet-32, Stable (5.79), Heuristic (5.29) and BatchEOT
  (6.14) are all worse than CondOT's 5.04, and BatchEOT is worse on
  ImageNet-64 too (14.92 against 13.93).
- **Few steps are still not few.** At 4 Euler steps BatchOT scores 38.86 on
  ImageNet-32 and 56.75 on ImageNet-64 (Tables 7–8). The coupling makes a
  flow cheaper to integrate. It does not make it one-step.
- **One run per row.** No seeds or intervals, and several of Table 6's FID
  gaps are under 1 point.
- **Unconditional, pixel space, 64 px and below.** No latent, conditional or
  guided experiment.

## Which comparisons are like for like

- **CondOT, BatchOT, Stable, Heuristic and BatchEOT** share architecture,
  optimizer, epochs and evaluation (Table 10, App. E.1). That is the
  controlled comparison. 438K iterations at batch 1,024 on ImageNet-32, 957K
  at 800 on ImageNet-64.
- **"Flow Matching w/ Diffusion"** is a reproduction at the same settings
  (Table 6 dagger). The path comparison is controlled, but one of its authors
  wrote the original.
- **Rectified Flow** was "trained for much longer starting from the fully
  trained CondOT model" (App. E.1). It has more compute than every other row.
- **DDPM and ScoreSDE** are reproductions too, per Table 6's dagger, at the
  same hyperparameters.

## Standing in the anthology

It carries the image-scale evidence for [SOTA-tmphvn35](../practices.d/SOTA-tmphvn35.md), minibatch OT pairing for flows sampled with a coarse solver.

It extends Flow Matching ([LIT-630](LIT-630.md)), which drew noise and data independently.
This paper keeps the conditional straight path and changes only the pairing.
Its reproduction also reruns Flow Matching's own path comparison on ImageNet.
The diffusion path scores 6.36 and 15.11 adaptive FID against CondOT's 5.04
and 13.93 at ImageNet-32 and 64, the same direction as the original Table 1.
Lipman is an author of both, so this is a replication by the same group.

Rectified Flow ([LIT-636](LIT-636.md)) is the rival way to straighten paths, and its row
here is a reflowed CondOT model trained longer: 5.55 at 111 NFE and 13.02 at
129 NFE. BatchOT reaches 4.68 and 12.37 in a single training run, at
comparable NFE (146 and 135), with no reflow. DDPM ([LIT-036](LIT-036.md)) and Score SDE
([LIT-722](LIT-722.md)) are the diffusion rows, reproduced at the same settings. They need
more NFE for worse FID (5.72 at 330, 6.84 at 198 on ImageNet-32) and fall
apart under few-step Euler: 362 and 340 FID at 4 steps (Table 7).

Concurrent with the minibatch-OT CFM paper ([LIT-tmpzz36v](LIT-tmpzz36v.md)), from a different
group. The two reach the same construction and the same k → ∞ result
independently. This one has the image-scale evidence, ImageNet-32 and 64
against CIFAR-10. That one has the dynamic-OT and Schrödinger-bridge
evaluation.

Flow map matching ([LIT-tmpuz24v](LIT-tmpuz24v.md)) quotes this paper's ImageNet-32 Euler rows
as its baseline: BatchOT's 38.86, 22.08, 15.64 and 7.71 FID at 4, 6, 8 and
20 steps, against its own teacher-free flow map's 16.90, 14.48, 12.61 and
9.68. The flow map leads only below about eight steps.

**On [SOTA-266](../practices.d/SOTA-266.md) it adds a coupling to the straight path, not a rival to it.**
The conditional path is the practice's straight line throughout. What
changes is the marginal, which [THEORY-106](../theory.d/THEORY-106.md) notes is not straight under the
independent coupling. Straightening it buys fewer Euler steps for the same
FID at ImageNet-64 and below. It has not been shown at the latent,
text-conditioned scale where the practice's evidence lives. SD3, Movie Gen
and the video reports train with the independent coupling. With a
text condition, how to pair within a batch without breaking the
conditional marginals is not addressed here.

**On [SOTA-392](../practices.d/SOTA-392.md) it is not an alternative.** Four-step FID of 38.86 on
ImageNet-32 is far from what reflow plus distillation or distribution
matching reaches in one step. Couplings lower the step count of a
many-step sampler. They do not replace a few-step student.

Filed without a NOTE: the takeaways come from one full reading of v2, main
text and Appendices A–E. Figs. 3, 4, 6, 8 and 9 are curves, quoted only
through Table 1 or the text.
