---
number: 149
status: Active
formerly:
- SOTA-tmpa982c
consensus: emerging
consensus_note: >-
  Two labs taking the same shape further. DeepSeek has run fine-grained plus
  shared experts since LIT-170 and through LIT-160 and LIT-139; Kimi K3's
  "Stable LatentMoE" (LIT-131) is 16 routed of 896, which is the same design
  pushed past what the original paper tried. Qwen and NVIDIA build sparse
  models (LIT-182, LIT-183) without the record knowing whether they segment
  this finely, so this is spreading rather than settled.
title: 'Build the sparse layers from many small experts plus an always-on shared one, not a few large ones'
version: 1
tags:
- model-architecture
date: '2026-09-07'
source:
- LIT-170
extends:
- SOTA-150
implementations:
- DeepSeekMoE
- DeepSeek-V3
- DeepSeek-V4
- Kimi K3
summary: >-
  Dai et al. (2024), [LIT-170](../literature.d/LIT-170.md) — split into mN smaller experts and activate mK
  of them so the router chooses from a far larger combination space at the
  same compute, and isolate a few always-on shared experts to hold the common
  knowledge every routed expert would otherwise learn separately.
---

<!-- inactive-ok-file: SOTA-148 — Proposed, named as the third member of the
     family this document is about -->

# SOTA-149: Build the sparse layers from many small experts plus an always-on shared one, not a few large ones

[SOTA-150](SOTA-150.md) says make the layer sparse. This says how to
cut it up, and the diagnosis behind it is the interesting part.

Conventional top-K-of-N routing does not actually deliver **expert
specialisation**. Experts end up holding overlapping knowledge rather than
focused knowledge, which wastes the parameters sparsity was supposed to buy —
you pay for capacity and get redundancy.

[LIT-170](../literature.d/LIT-170.md) attributes that to the granularity of the choice and changes it
in two ways:

- **Fine segmentation.** Split into `mN` smaller experts and activate `mK` of
  them. Same compute, but the router now picks from a combinatorially larger
  space, so a token can be served by a combination rather than by whichever
  single large expert is least wrong.
- **Shared experts.** Isolate `K_s` experts that always fire. Knowledge every
  token needs stops being replicated across routed experts, which is what
  those experts were spending capacity on.

The measurement that matters most is the last one in the paper: DeepSeekMoE 2B
nearly reaches its **dense counterpart at equal total parameters**. That is
the ceiling a mixture of experts is trying to approach and normally does not,
and approaching it is the specialisation claim being cashed out.

## Where the rest of the family sits

Three practices' worth of MoE material, which is what
[LIT-171](../literature.d/LIT-171.md) predicted:

- [SOTA-150](SOTA-150.md) — make the layer sparse at all.
- This one — how to cut it up.
- [SOTA-148](SOTA-148.md) — how to keep the experts evenly loaded, with a
  bias rather than an auxiliary loss.

They are separable claims: you can accept sparsity and reject fine
segmentation, or adopt fine segmentation and still balance with an auxiliary
loss. The record files them apart so that a reader can.
