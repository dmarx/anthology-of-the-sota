---
number: 262
status: Proposed
formerly:
- SOTA-tmp28zyj
promote_when: >-
  A second group reporting per-modality weights against a shared-weight
  backbone at matched compute, or an ablation separating the separate weights
  from the joint attention — the two arrive together here and nothing says
  which is doing the work. What would not move it: another multimodal
  transformer that happens to use separate projections, which is common and
  is not a controlled comparison.
consensus: unreplicated
consensus_note: >-
  One group, one architecture family, compared against UViT and DiT. Shipped
  in a released 8B model with weights, which is stronger than a paper claim
  and is not a replication.
title: 'Give each modality its own weights and let the streams attend jointly'
version: 1
tags:
- multimodal-learning
- model-architecture
- generative-modeling
date: '2026-09-20'
source:
- LIT-449
introduced_by:
- LIT-449
implementations:
- 'Stable Diffusion 3'
summary: >-
  Esser et al. (2024), [LIT-449](../literature.d/LIT-449.md) — MMDiT gives the text and image
  streams separate projections and MLPs, then runs attention over the
  concatenated sequence so information flows both ways. It beats UViT and
  DiT at matched budget, follows predictable scaling trends, and the gains
  land specifically on text comprehension, typography and human preference.
---

# SOTA-262: Give each modality its own weights and let the streams attend jointly

## Source

Esser et al. (2024), [LIT-449](../literature.d/LIT-449.md) — [ARXIV-2403.03206](https://arxiv.org/abs/2403.03206).

## The shape of the recommendation

Two modalities, one sequence. Text tokens and image tokens get **separate
weights** — their own projections and their own MLPs — because they are
different kinds of object and a shared parameterization has to be a
compromise between them. But attention runs over the **concatenated**
sequence, so the two streams are not merely fused at the end: information
flows in both directions at every layer.

That is the distinction worth holding. Cross-attention conditioning, the
prevailing alternative, lets image tokens read text and not the reverse. Here
the text representation is itself updated by what the image is doing.

## What it buys, and where

Against UViT and DiT backbones at matched budget, and the improvements are
not uniform: they concentrate in **text comprehension, typography and human
preference**. That is the right place for them to land if the mechanism is
what the paper claims — the tasks that fail when the text representation is
frozen partway through are exactly the ones a bidirectional design should
fix.

It also **follows predictable scaling trends**, with validation loss tracking
the downstream metrics, which is what made it safe to commit an 8B run to.

## Why this is `Proposed` despite a shipped model

**The two ingredients arrive together.** Separate weights and joint attention
are both in MMDiT and nothing here separates them. A reader could implement
one and attribute the other's benefit to it. `promote_when:` asks for exactly
that ablation.

The comparison is against shared-weight backbones — UViT and DiT — rather
than against other per-modality designs, so what is established is that this
beats *sharing*, not that this is the best way not to share.

One group, one architecture family, one modality pair. Whether the shape
generalizes beyond text-and-image is untouched.

The released 8B weights make the claim checkable, which is the main thing
raising it above a paper result.

## Known implementations

- Stable Diffusion 3
