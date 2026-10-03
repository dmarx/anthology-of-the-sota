---
status: Proposed
promote_when: >-
  A group trains a latent, class- or text-conditional flow at 256 px or
  above with minibatch-OT pairing and with independent pairing, everything
  else held, and reports FID at fixed small Euler step counts (4 to 16) for
  both. The run must say how the pairing respects the condition. Every
  measurement so far is unconditional, in pixel space, at 64 px or below.
  A large model that ships with the coupling does not count unless it
  reports the independent-coupling arm.
consensus: emerging
consensus_note: >-
  Two groups reached the same construction at the same time, independently:
  OT-CFM from Mila (LIT-tmpzz36v) and Multisample Flow Matching from Meta,
  NYU and Weizmann (LIT-tmprjg3i). Both show straighter paths, and both show
  fewer steps for the same quality on images. The image evidence is mostly
  Meta's (ImageNet-32 and 64), and Mila's CIFAR-10 gain is within one run's
  noise at 100 Euler steps. No large flow model in the record uses the
  coupling: SD3 and the video reports train with independent pairs. Nothing
  in the record argues against it. Read as of 2026-10.
title: 'When a flow will be sampled with a coarse ODE solver, pair noise and data within each minibatch by exact optimal transport'
version: 1
tags:
- generative-modeling
- flows-and-transport
- training-optimization
date: '2026-10-03'
source:
- LIT-tmprjg3i
- LIT-tmpzz36v
# OT-CFM (LIT-tmpzz36v, v1 1 Feb 2023) and Multisample Flow Matching
# (LIT-tmprjg3i, v1 28 Apr 2023) are concurrent and independent; OT-CFM was
# posted first. Multisample Flow Matching is listed first in `source:`
# because it holds the image-scale evidence for the low-step claim.
introduced_by:
- LIT-tmpzz36v
implementations:
- 'torchcfm (OT-CFM)'
summary: >-
  Pooladian et al. (2023), [LIT-tmprjg3i](../literature.d/LIT-tmprjg3i.md), and Tong et al. (2023),
  [LIT-tmpzz36v](../literature.d/LIT-tmpzz36v.md). Re-pair each minibatch's noise and data by exact discrete OT
  before the flow-matching regression. The marginals stay exact, the learned
  paths straighten, and on ImageNet-64 reaching FID 20 with Euler takes 12
  steps instead of 29, at equal likelihood and 4% more time per iteration.
  It lowers the step count of an ODE sampler. It does not make one: four-step
  FID stays near 39 on ImageNet-32. Unconditional, 64 px and below.
---

<!-- inactive-ok-file: SOTA-392 — Proposed; named to say this coupling is not an alternative to its one-step students, not cited as settled advice -->

# SOTA-tmphvn35: When a flow will be sampled with a coarse ODE solver, pair noise and data within each minibatch by exact optimal transport

## Source

Pooladian, Ben-Hamu, Domingo-Enrich, Amos, Lipman and Chen (2023),
[LIT-tmprjg3i](../literature.d/LIT-tmprjg3i.md) — Multisample Flow Matching, Tables 1, 2, 6 and 9.

Tong, Fatras, Malkin, Huguet, Zhang, Rector-Brooks, Wolf and Bengio (2023),
[LIT-tmpzz36v](../literature.d/LIT-tmpzz36v.md) — OT-CFM, Table 2, Table 5 and Fig. 3.

## What to do

Flow matching usually pairs each data point with an independent noise draw.
Instead, for each training batch:

1. Draw k noise samples and k data samples.
2. Solve the exact assignment problem between them under squared Euclidean
   cost (a k × k linear assignment, the discrete OT plan).
3. Train the ordinary straight-path flow-matching loss on the matched pairs.

Use exact batch OT, not the cheaper variants. Of the couplings Multisample
Flow Matching tried, only exact BatchOT beat independent pairing on
adaptive-solver FID at both resolutions (below).

This changes nothing at sampling time. What it buys is a learned ODE that is
straighter, so a coarse Euler or midpoint solve loses less. "Coarse" here
means roughly ten to thirty steps. It is not a route to one- or two-step
sampling.

## Evidence

The marginals are untouched by construction. Any coupling whose marginals
are the noise and data distributions leaves the flow-matching gradient
equal to the marginal one ([LIT-tmprjg3i](../literature.d/LIT-tmprjg3i.md), Lemma 3.1 and §4; [LIT-tmpzz36v](../literature.d/LIT-tmpzz36v.md),
Thms. 3.1–3.2). As the batch grows, the batch-OT objective's optimum and the
paths' straightness go to the OT values ([LIT-tmprjg3i](../literature.d/LIT-tmprjg3i.md), Thm. 4.2;
[LIT-tmpzz36v](../literature.d/LIT-tmpzz36v.md), Prop. 3.4).

**Multisample Flow Matching** ([LIT-tmprjg3i](../literature.d/LIT-tmprjg3i.md)). Pixel-space, unconditional
ImageNet. Architecture, optimizer, epochs and evaluation are shared across
couplings (App. E.1).

- Euler steps needed to reach a target FID (Table 1, read off Fig. 3's
  curves):

  | | ImageNet-32, FID 10 | ImageNet-64, FID 20 |
  |---|--:|--:|
  | Independent (CondOT) | 20 | 29 |
  | BatchOT | 14 | 12 |
  | Diffusion baselines | ≥ 40 | ≥ 40 |

- Likelihood is unchanged: 3.58 and 3.27 bits per dimension for both
  couplings. Adaptive-solver FID improves, 5.04 → 4.68 on ImageNet-32 and
  13.93 → 12.37 on ImageNet-64 (Table 6).
- Samples from the same noise change less as the step count drops (Table 3).
- The pairing costs 0.8% more time per iteration on ImageNet-32 and 3.9% on
  ImageNet-64 (Table 9).

**OT-CFM** ([LIT-tmpzz36v](../literature.d/LIT-tmpzz36v.md)), from a different group. In 2-D, normalized path
energy is 0.018–0.087 with minibatch OT against 0.222–2.738 with independent
pairs, over five seeds. Two and three rounds of reflow reach 0.069–0.149
and 0.055–0.129, so one OT-CFM training run does about as well as several
rounds of reflow or better (Table 2). The OT batch can be small, and path energy plateaus near 64
samples (Fig. D.2). On CIFAR-10, Fig. 3 shows OT-CFM ahead of independent
pairing at low Euler step counts after 400K steps, as curves only.

## Conditions

- **The image gain is modest, and the numbers are one run each.** OT-CFM's
  CIFAR-10 table ([LIT-tmpzz36v](../literature.d/LIT-tmpzz36v.md), Table 5) has 4.443 against 4.461 at 100
  Euler steps. Independent pairing is ahead at 1,000 steps (3.643 against
  3.741). Its "more efficient training" is per step: wall-clock time to
  convergence in 2-D is longer with OT (Table D.1). In Multisample Flow
  Matching, the cheaper couplings lose to independent pairing on
  ImageNet-32 adaptive FID: Stable 5.79, Heuristic 5.29 and BatchEOT 6.14
  against 5.04 (Table 6). Several gaps there are under one FID point.
- **Unconditional, pixel space, 64 px and below.** Neither paper pairs under
  a class or text condition. Pairing across a batch makes each noise depend
  on the other images in that batch, so the noise given a condition is no
  longer the source distribution, and neither paper shows the conditional
  marginals survive. Pairing within each condition is the obvious repair
  and is untested.
- **The minibatch plan is an approximation whose error grows with
  dimension** ([LIT-tmpzz36v](../literature.d/LIT-tmpzz36v.md), §6). The theorems are about the exact plan or
  the limit of large batches. Nothing bounds the error at image dimension
  and realistic batch size.
- **It does not replace a few-step student.** Four-step Euler FID with
  BatchOT is 38.86 on ImageNet-32 and 56.75 on ImageNet-64 ([LIT-tmprjg3i](../literature.d/LIT-tmprjg3i.md),
  Tables 7–8). For one to four steps, distillation or a consistency-type
  model is the route. [SOTA-392](SOTA-392.md) is about that case.
- **What it straightens is the marginal, not the conditional path.**
  [SOTA-266](SOTA-266.md) already says to use the straight conditional path. [THEORY-106](../theory.d/THEORY-106.md)
  notes that a straight conditional path does not give a straight marginal
  ODE. The coupling is the lever that straightens the marginal with the
  conditional path held fixed. In OT-CFM's CIFAR-10 runs that lever moves FID
  less than the choice of path does ([LIT-tmpzz36v](../literature.d/LIT-tmpzz36v.md), Table 5). Use this on top
  of [SOTA-266](SOTA-266.md), not instead of it.

## Known implementations

- torchcfm, the OT-CFM authors' library.
