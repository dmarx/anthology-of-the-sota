---
number: 400
status: Active
formerly:
- SOTA-tmpnogfc
consensus: emerging
consensus_note: >-
  The grounds are the evidence, not adoption. One paper, but a controlled
  before-and-after across three training paradigms — supervised, image-text and
  self-supervised — with nothing degrading and dense prediction improving in
  each. The only adopter this record can name is the source group, whose own
  DINOv2 line ships register checkpoints; that is the authors shipping their own
  result, which `DP-005` says to count as adoption and not as a second
  measurement. What keeps it short of `converged` is that nobody outside the
  group has reported training with registers, and one of the paper's own
  evaluations (OpenCLIP object discovery) is slightly worse with them. Read as
  of 2026-09.
title: 'Append a few register tokens to a ViT so it does not commandeer background patches for scratch space'
version: 1
tags:
- model-architecture
- vision-and-graphics
- representation-and-encoding
date: '2026-09-24'
source:
- LIT-662
introduced_by:
- LIT-662
implementations:
- DINOv2
explained_by:
- THEORY-101
---

# SOTA-400: Append a few register tokens to a ViT so it does not commandeer background patches for scratch space

## Source

Darcet, Oquab, Mairal and Bojanowski (2023), `LIT-662`.

## What to do

Append a small number of learned tokens to the input sequence that **do not
come from the image**, carry them through the transformer with everything else,
and discard them at the output. One is enough to remove the artifacts; a few
more help dense tasks slightly.

That is the whole change. No loss term, no schedule, no architectural surgery
beyond a longer sequence.

## Why

Without them, a large trained ViT takes patches whose content is redundant with
their neighbours and overwrites them with global state — `THEORY-101`.
Those patches come out as **high-norm outlier tokens**, 2.37% of them in
DINOv2 ViT-g, holding little information about their own position or pixels and
a lot about the image as a whole. Anything downstream that reads the feature
map or the attention map as a spatial signal reads them as noise.

Registers give the model somewhere to put that state which nobody downstream
is going to interpret as a patch.

## What it costs

Nothing measurable, which is unusual enough to state with the table. Linear
probing on frozen features, each model trained from scratch both ways:

| | ImageNet top-1 | ADE20k mIoU | NYUd rmse ↓ |
| --- | --: | --: | --: |
| DeiT-III | 84.7 | 38.9 | 0.511 |
| DeiT-III + reg | 84.7 | 39.1 | 0.512 |
| OpenCLIP | 78.2 | 26.6 | 0.702 |
| OpenCLIP + reg | 78.1 | 26.7 | **0.661** |
| DINOv2 | 84.3 | 46.6 | 0.378 |
| DINOv2 + reg | **84.8** | **47.9** | **0.366** |

The sequence is a handful of tokens longer, which is the only cost.

## Where the benefit actually is

Not classification. **Anything that treats the feature map as spatial.** LOST
object discovery, corloc:

| | VOC 2007 | VOC 2012 | COCO 20k |
| --- | --: | --: | --: |
| DeiT-III | 11.7 | 13.1 | 10.7 |
| DeiT-III + reg | **27.1** | **32.7** | **25.1** |
| DINOv2 | 35.3 | | |
| DINOv2 + reg | **55.4** | | |

**+20.1 corloc** for DINOv2 on VOC 2007, and DeiT-III more than doubles.

## Conditions

**It has to be done at training time.** This is not a post-hoc fix; each
comparison above is a model trained from scratch with registers. For a
checkpoint that already has artifacts, the options are to use a register
variant if one exists or to detect and mask the high-norm tokens.

**It matters at ViT-Large and above.** Tiny, Small and Base do not show the
artifacts, so below that threshold this buys nothing — the paper's sweep over
model size is what says so.

**One evaluation goes the other way.** OpenCLIP object discovery is slightly
*worse* with registers, and neither the paper nor `THEORY-101` explains
it. If the deployment is image-text pretraining for a spatial task, check
rather than assume.

**It does not recover everything the artifacts cost.** DINOv2 with registers
reaches 55.4 corloc on VOC 2007 where the original DINO reaches **61.9**.
Registers narrow that generational regression; something else about DINOv2 also
costs object discovery and nobody has named it.

## Known implementations

- DINOv2, whose released line includes register variants — the source group's
  own, so adoption rather than independent replication.
