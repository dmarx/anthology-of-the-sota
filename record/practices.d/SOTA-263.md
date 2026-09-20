---
number: 263
status: Proposed
formerly:
- SOTA-tmp4jpf3
promote_when: >-
  An ablation reporting what the shift is worth — the same model finetuned at
  a new resolution with and without it — from anyone, or a second
  high-resolution training report that says it shifted for this reason. What
  would not move it: another model trained at multiple resolutions that
  happens to retune its schedule empirically, which is consistent with the
  correction and does not test the correspondence it rests on.
consensus: unreplicated
consensus_note: >-
  One group. The argument is a derivation rather than a measurement, and the
  paper demonstrates it qualitatively inside a pipeline where several things
  changed at once. It is also the kind of correction that is obvious once
  stated, which is a reason to suspect it is right and not a reason to think
  it has been checked.
title: 'Shift the timestep schedule when the resolution changes, because more pixels need more noise'
version: 1
tags:
- generative-modeling
date: '2026-09-20'
source:
- LIT-449
introduced_by:
- LIT-449
implementations:
- 'Stable Diffusion 3'
summary: >-
  Esser et al. (2024), [LIT-449](../literature.d/LIT-449.md) — a timestep is not a fixed amount of
  corruption. Destroying the signal in an image with more pixels takes more
  noise, so a timestep at one resolution must be mapped to a different one at
  another to corrupt equivalently. A schedule carried unchanged from
  low-resolution pretraining to high-resolution finetuning is wrong, and
  wrong in a predictable direction.
---

# SOTA-263: Shift the timestep schedule when the resolution changes, because more pixels need more noise

## Source

Esser et al. (2024), [LIT-449](../literature.d/LIT-449.md) — [ARXIV-2403.03206](https://arxiv.org/abs/2403.03206).

## The correction

A noise schedule is usually treated as a property of the model: chosen once,
carried across runs. But what a timestep *does* depends on how much signal
there is to destroy, and an image with more pixels has more. Add the same
noise to a 256×256 image and a 1024×1024 one and the second is less
corrupted, because the redundancy across neighbouring pixels survives.

So a timestep `t` at one resolution corresponds to a *different* timestep at
another if the two are to corrupt equivalently, and the correspondence can be
written down from the pixel count. The usual pipeline — pretrain at low
resolution, finetune at high — carries the schedule across unchanged, which
means the high-resolution stage trains against a schedule that under-corrupts
throughout.

The direction of the error is predictable, which is what makes this a
practice rather than an observation: higher resolution wants more noise at
the same nominal timestep.

## Why this is easy to miss

Nothing breaks. The model trains, the loss falls, and the samples are
plausible — the failure is that the high-resolution stage spends its budget
on a corruption range it was not supposed to be in. That is the same shape of
quiet failure the record records elsewhere for over-large batches
([SOTA-061](SOTA-061.md)) and for unadjusted preconditioning ([SOTA-188](SOTA-188.md)): the run
completes and is simply worse than it should have been, and the deficit gets
attributed to data or to scale.

## Relation to the schedule material the record holds

[THEORY-027](../theory.d/THEORY-027.md) says the continuous-time bound is indifferent to the
schedule's *shape* given its endpoints. This practice is not in tension with
that: a resolution shift changes which corruption level a given `t` produces,
which is a statement about the map from time to signal-to-noise, and the
endpoints move with it. What the invariance licenses is exactly this kind of
reparameterization — if the shape were part of the model, shifting it would
be a modelling change rather than a correction.

## Conditions, and why this is `Proposed`

**Derived, then demonstrated qualitatively.** The correspondence is argued
from signal per pixel and shown with sample comparisons inside a pipeline
that changed several things at once. There is no ablation reporting what the
shift alone is worth, which is what `promote_when:` asks for.

One group, one architecture, one resolution transition. The argument is
general and the evidence is not.

It also assumes corruption should be matched in terms of signal destroyed,
which is the natural reading and is a modelling choice rather than a
theorem. A different notion of equivalent corruption would give a different
map.

## Known implementations

- Stable Diffusion 3
