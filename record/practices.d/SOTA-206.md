---
number: 206
status: Active
formerly:
- SOTA-tmpo7on7
consensus: emerging
consensus_note: >-
  The few-step generative line has settled on models that expose a step count
  rather than on strictly one-step models, and the record's own fast-sampling
  holdings all keep the dial. It is one paper's argument made explicitly,
  corroborated by what shipped rather than by a second ablation.
title: 'Keep a multi-step sampling option in a few-step generative model'
version: 1
tags:
- generative-modeling
date: '2026-09-10'
published: '2023-03-01'
source:
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

## The other route

[SOTA-203](SOTA-203.md) gets a low step count from a better solver and costs no
training at all. This one costs a training run and reaches step counts a solver
cannot. Nothing in the record compares them, and the choice is currently made
by which asset you have rather than by evidence.
