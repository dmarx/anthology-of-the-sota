---
status: Proposed
promote_when: >-
  A group outside NVIDIA, training something other than an ADM-style image
  U-Net — a diffusion transformer, a video or audio model, a language model —
  sweeps the averaging length post hoc and reports that the best length moves
  with a variable it would otherwise have fixed in advance (guidance weight,
  evaluation metric, learning-rate schedule) by enough to change a reported
  comparison. A second paper confirming that the reconstruction is accurate is
  not it: the mechanism is a least-squares fit and was never in doubt; what is
  unreplicated is that the choice it frees you to make matters.
title: 'Choose the EMA length after training: store two power-function averages at snapshots and reconstruct any length by least squares'
version: 1
tags:
- training-optimization
- generative-modeling
- analysis-and-evaluation
date: '2026-09-25'
source:
- LIT-tmpzn7w1
introduced_by:
- LIT-tmpzn7w1
implementations:
- 'NVlabs/edm2'
summary: >-
  Karras et al. (2023), [LIT-tmpzn7w1](../literature.d/LIT-tmpzn7w1.md) — EDM2. Track two power-function
  averages of the weights (`σ_rel` 0.05 and 0.10), save both every few
  thousand steps, and synthesize any EMA length after the run from a small
  linear solve. Then choose it per configuration, per guidance weight and per
  metric, because on ImageNet-512 the best length moves with all three — at
  guidance 1.4, FID wants 2% and FD_DINOv2 wants 14%.
---

<!-- inactive-ok-file: SOTA-156, SOTA-408 — Proposed; named as neighbouring averaging practices this one does not rest on -->

# SOTA-tmp9x33t: Choose the EMA length after training: store two power-function averages at snapshots and reconstruct any length by least squares

## Source

Karras et al. (2023), [LIT-tmpzn7w1](../literature.d/LIT-tmpzn7w1.md) — [ARXIV-2312.02696](https://arxiv.org/abs/2312.02696), §3, §4 and Appendix
C; read as [NOTE-tmpod74g](../notes.d/NOTE-tmpod74g.md).

## What to do

**During training**, keep two running averages of the weights with a
**power-function** profile rather than an exponential one:

    θ̂_γ(t) ← β_γ(t) · θ̂_γ(t−1) + (1 − β_γ(t)) · θ(t),   β_γ(t) = (1 − 1/t)^(γ+1)

It is an EMA whose decay depends on the step. Two properties make it the
right profile to store: the initial random weights get **zero** weight, and
the profile **stretches with training length**, so "10%" means the same
thing at every point in the run. Use `σ_rel` = 0.05 and 0.10
(`γ` ≈ 16.97 and 6.94). Snapshot both every ~4k steps; fp16 is enough. The
paper's runs stored 160–512 snapshots.

**After training**, pick any target profile — any `σ_rel` in about
[0.015, 0.25], at any point in the run — and solve `Ax = b` for the linear
combination of stored snapshots whose averaging profile best matches it
(closed-form inner products; Algorithm 3 in the paper is a dozen lines).
Reconstruction error falls roughly as the fourth power of the snapshot count.

**Then actually use the freedom**: sweep the length, and choose it
separately for each thing you report.

## Why the length has to be chosen late

The mechanism is not the point; what it revealed is. With the length sweepable
densely for the first time, on ImageNet-512:

- **It depends on the architecture.** The optimum moves across every step of
  the paper's ablation ladder, and a comparison of two architectures at one
  shared EMA length is a comparison at one of them's wrong setting.
- **It depends on the learning rate.** With the EMA re-chosen post hoc, a
  learning-rate decay anywhere in a 5× bracket stays within 10% of the best
  FID; with the EMA fixed at the overall optimum of 13%, the same bracket
  costs up to **72%**. Much of what looks like learning-rate sensitivity is
  EMA mismatch.
- **It depends on guidance** — "very strongly". Guided sampling typically wants
  a much shorter average. A model tuned unguided and then sampled guided, or
  the reverse, is off-optimum in one of them; the authors suspect part of
  the guided/unguided gap reported by earlier work is this.
- **It depends on the metric.** Unguided, FID's optimum is 13% and
  FD_DINOv2's is 19%. At guidance 1.4 it is **2% against 14%**, and each metric
  rates the other's choice as terrible. There is no length that is best; there
  is a length that is best *for the number you are about to report*.

So the instruction is not "use a longer EMA" or any particular value. The
paper's own values for its own models run from 2% to 19%.

## Conditions

- **Evidence is one group, one architecture family, image diffusion only.**
  ADM-style U-Nets on ImageNet-512 latents and ImageNet-64 pixels. Nothing
  here shows the length matters as much for a transformer denoiser or outside
  diffusion, which is what `promote_when` waits on.
- **The sensitivity is itself architecture-dependent.** In the paper's
  baseline, individual weight tensors disagree about the best length, so the
  global optimum is broad and forgiving; in its final architecture they agree
  and the optimum is sharp. A reader with a well-conditioned architecture needs
  this *more*, not less.
- **Three of its observations are anecdotal by the authors' own label** —
  that the optimal length scales as `1/(α_ref² t_ref)`, shortens with model
  capacity, and shortens on simpler data. Use them as starting points for the
  sweep, not as a rule.
- **Choosing per metric is not choosing per taste.** Reporting FID at FID's
  optimum and FD_DINOv2 at its own is the honest protocol, and it means two
  "models" from one run. Say so when reporting — the same discipline as fixing
  the guidance weight before comparing ([SOTA-424](SOTA-424.md)), and a close cousin of
  [SOTA-337](SOTA-337.md)'s reason for reporting a second Fréchet distance at all.
- **Storage is the cost.** Two copies of the weights per snapshot. At
  hundreds of snapshots that is real disk for a large model; the paper
  leaves the snapshot count/accuracy trade unstudied beyond "a few dozen is
  more than sufficient" for the profile fit.

## What this does not cover

**Whether to average weights at all.** This practice is a knob on
evaluating from an average of the weights, and the record holds no practice
for that trunk: EDM2 calls model averaging "indispensable" in image synthesis
and runs no arm without it. The neighbours that do exist average for other
reasons — [SOTA-408](SOTA-408.md) averages the tail of a cyclical-LR run for flatter optima,
[SOTA-156](SOTA-156.md) averages iterates to remove the schedule — and the post-hoc machinery
would apply to their profiles too, which the paper states and does not test.

## Known implementations

- `NVlabs/edm2`, the reference implementation.
