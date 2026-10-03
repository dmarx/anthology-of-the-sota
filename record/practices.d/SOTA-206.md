---
number: 206
status: Active
formerly:
- SOTA-tmpo7on7
consensus: converged
consensus_note: >-
  The few-step generative line has settled on models that expose a step count
  rather than on strictly one-step models, and the record's own fast-sampling
  holdings all keep the dial. It was one paper's argument made explicitly,
  corroborated by what shipped. Since 2026-10 the record also holds measured
  cases of one model serving several step counts from three groups outside
  the source's: Shortcut Models (LIT-tmpo7np5), Inductive Moment Matching
  (LIT-tmp7ppws) and rCM (LIT-tmpkegvh), besides iCT and sCM from the
  source's own line (LIT-tmpnrsms, LIT-tmpt5h4h). Converged since v3, on the
  owner's reading of that evidence: three groups unconnected to the source
  now measure the property. Read as of 2026-10.
title: 'Keep a multi-step sampling option in a few-step generative model'
version: 3
history:
- version: 3
  date: '2026-10-03'
  note: >-
    Consensus moved from emerging to converged, on the owner's decision,
    on the grounds v2 gave: Shortcut Models, Inductive Moment Matching and
    rCM, three groups outside the source's line, each serve one model at
    several step counts. Status and recommendation unchanged.
- version: 2
  date: '2026-10-03'
  note: >-
    Adds iCT, sCM, Shortcut Models, Inductive Moment Matching and rCM as
    sources: each samples one trained model at several step counts and
    reports the quality at each. Adds a condition that the dial is not free
    (Shortcut's Table 1, IMM's Table 7, rCM's one-step video). Consensus is
    left at emerging; a move to converged is proposed for the owner to
    decide, since three groups unconnected to the source now measure the
    property. Status unchanged.
tags:
- generative-modeling
- few-step-generation
date: '2026-09-10'
source:
- LIT-093
- LIT-tmpo7np5
- LIT-tmp7ppws
- LIT-tmpnrsms
- LIT-tmpt5h4h
- LIT-tmpkegvh
introduced_by:
- LIT-093
summary: >-
  Song et al. (2023), [LIT-093](../literature.d/LIT-093.md). A one-step model that cannot spend more
  compute has no quality dial: whatever it produces is what you get. Consistency
  models trade compute for quality at inference without retraining, and that
  property is worth preserving by design.
---

# SOTA-206: Keep a multi-step sampling option in a few-step generative model

## Source

Song et al. (2023), [LIT-093](../literature.d/LIT-093.md) — Consistency Models.

## The claim

Fast generative sampling is usually presented as a race to one step. The
property worth keeping is not the low number; it is that the number is a
**knob**. Consistency models sample in one step and also support multistep
sampling that trades compute for quality — **without retraining**, because the
model learns a map to the trajectory's endpoint rather than a fixed-length
procedure.

A strictly one-step model gives up the ability to spend more compute when a
particular sample matters. That is a capability loss that does not show up in
an FID table, because the table reports one operating point.

## Why the framing matters

[LIT-093](../literature.d/LIT-093.md) is usually cited as a distillation result, and the paper is at pains to
say distillation is **not required**: consistency models can be trained in
isolation and, so trained, beat existing one-step non-adversarial models on
CIFAR-10, ImageNet-64 and LSUN-256. Reading it as "a way to distil a diffusion
model" loses the part that makes it a model family.

## Evidence

- **One-step FID 3.55 on CIFAR-10, 6.20 on ImageNet-64** — state of the art for
  one-step generation at the time.
- Multistep sampling improves quality with no change to the weights.
- Zero-shot inpainting, colorization and super-resolution, no task-specific
  training — capabilities that need somewhere to put extra compute.

Later papers measure the dial directly, each with one set of weights:

- **Shortcut Models** ([LIT-tmpo7np5](../literature.d/LIT-tmpo7np5.md)), from a different group, condition a
  flow-matching network on step size and train it in one run. On DiT-B at
  matched compute it scores 6.9 / 13.8 / 20.5 FID at 128 / 4 / 1 steps on
  CelebA-HQ-256 and 15.5 / 28.3 / 40.3 on ImageNet-256, and many-step
  quality is not lost against plain flow matching (6.9 against 7.3).
- **Inductive Moment Matching** ([LIT-tmp7ppws](../literature.d/LIT-tmp7ppws.md)), also from outside the
  source's group, runs one ImageNet-256 model at 1, 2, 4 and 8 steps for FID
  8.05, 3.99, 2.51 and 1.99, saturating near 16 steps (1.90). Guidance
  doubles each step's evaluations.
- **iCT** ([LIT-tmpnrsms](../literature.d/LIT-tmpnrsms.md)), the source's own line, finds two steps better
  than one in every row, by 0.27 to 0.82 FID: 3.25 to 2.77 on ImageNet-64
  for iCT-deep.
- **sCM** ([LIT-tmpt5h4h](../literature.d/LIT-tmpt5h4h.md)), also that line, samples at one or two steps, and
  the second step closes most of the gap to the teacher at every model size:
  2.28 to 1.88 on ImageNet-512 at 1.5B, against a teacher at 1.73.
- **rCM** ([LIT-tmpkegvh](../literature.d/LIT-tmpkegvh.md)), from a third group, serves 1, 2 and 4 steps from
  one 14B student on text-to-image and text-to-video. Images hold at one
  step (GenEval 0.82 at 14B, 0.83 at four).

## Conditions

**The dial is not free.** Three of the papers above show its price.

- A fixed one-step model can beat it at one step. In Shortcut Models' own
  matched Table 1 ([LIT-tmpo7np5](../literature.d/LIT-tmpo7np5.md)), progressive distillation, which has no
  many-step mode, scores 14.8 against the shortcut model's 20.5 on
  CelebA-HQ and 35.6 against 40.3 on ImageNet. Keeping the dial cost 5.7
  and 4.7 FID at one step there.
- The operating points compete in training. In Inductive Moment Matching's
  Table 7 ([LIT-tmp7ppws](../literature.d/LIT-tmp7ppws.md)), the loss weighting that gives the best eight-step
  FID (2.01) gives a slightly worse one-step FID, 8.28 against 7.97.
- The low end can be unusable in some modalities. rCM's one-step video is
  blurry and its 1.3B VBench falls to 82.65 from 84.43 at four steps
  ([LIT-tmpkegvh](../literature.d/LIT-tmpkegvh.md), §5.2); video needs two steps where images hold at one.

So keep the dial when a sample may be worth more compute, and expect to pay
a little at the lowest step count for it.

## The other route

[SOTA-203](SOTA-203.md) gets a low step count from a better solver and costs no
training at all. This one costs a training run and reaches step counts a solver
cannot. Nothing in the record compares them, and the choice is currently made
by which asset you have rather than by evidence.
