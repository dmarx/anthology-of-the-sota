---
status: Proposed
promote_when: >-
  A comparison by another group, on a quantitative metric beyond Cityscapes
  FCN scores, between cycle consistency and alternative content-preservation
  constraints for unpaired translation, showing cycle consistency is not
  dominated on appearance tasks. The source compares it only with GAN-only
  and one-directional variants of itself.
title: 'For unpaired image-to-image translation of appearance, constrain both mappings with a cycle-consistency loss'
version: 1
tags:
- generative-modeling
- vision-and-graphics
date: '2026-09-23'
source:
- LIT-tmpm6lfm
introduced_by:
- LIT-tmpm6lfm
consensus: unassessed
consensus_note: >-
  CycleGAN is a standard baseline for unpaired translation. The record holds
  none of the later work that might keep or replace the cycle constraint,
  so where the field stands on it has not been assessed here.
implementations:
- CycleGAN
summary: >-
  Zhu et al. (2017), [LIT-tmpm6lfm](../literature.d/LIT-tmpm6lfm.md) — learn X → Y and Y → X together, and
  penalize ‖F(G(x)) − x‖₁ and ‖G(F(y)) − y‖₁ alongside the two adversarial
  losses. With GAN losses alone the mapping may ignore its input. With the
  cycle it keeps content and changes appearance. It is scoped to colour and
  texture changes, and the authors report failure on geometric ones.
---

# SOTA-tmpw7xk8: For unpaired image-to-image translation of appearance, constrain both mappings with a cycle-consistency loss

## Source

Zhu et al. (2017), [LIT-tmpm6lfm](../literature.d/LIT-tmpm6lfm.md) — CycleGAN. Read as [NOTE-tmp36vxd](../notes.d/NOTE-tmp36vxd.md).

## The practice

When translating between two image domains **without paired examples**,
and the change is in **appearance** (style, colour, texture, season):

- **Train both directions**, `G: X → Y` and `F: Y → X`, each with its own
  discriminator
- **Add the cycle loss**, `λ(‖F(G(x)) − x‖₁ + ‖G(F(y)) − y‖₁)` with
  `λ = 10`, so a translation must keep what is needed to undo it

## What was measured

On Cityscapes labels → photo, GAN-only scores 0.51 / 0.11 / 0.08 (per-pixel
/ per-class / IoU) and the full model 0.52 / 0.17 / 0.11. On photo →
labels, 0.53 / 0.11 / 0.07 against 0.58 / 0.22 / 0.16. A cycle loss alone,
with no adversarial term, is far worse in both directions.

## Conditions

- **Appearance, not geometry.** Where the shape must change (dog → cat) the
  model makes minimal edits instead
- **One direction can suffice.** On labels → photo, GAN + forward cycle
  scored higher than both directions. The case for bidirectional is the
  instability and mode collapse the authors saw in the dropped direction
- **If pairs exist, use them.** The paired method is better
