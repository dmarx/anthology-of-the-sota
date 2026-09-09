---
status: Active
title: 'Train With Mixed Precision — NVIDIA deep learning performance guide'
version: 1
tags:
- training-optimization
date: '2026-09-09'
published: '2018-01-01'
url: 'https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html'
first_author: 'NVIDIA'
keywords:
- 'mixed-precision'
- 'loss-scaling'
- 'implementation'
summary: >-
  NVIDIA, the *Train With Mixed Precision* user guide. Where the dynamic loss
  scaling constants everyone runs actually come from: "we successfully trained
  networks with N = 2000, increasing scaling factor by 2, decreasing scaling
  factor by 0.5" — reported as one tested configuration, with "many other
  settings are valid as well."
---

# LIT-tmpsalf8: Train With Mixed Precision — NVIDIA deep learning performance guide

NVIDIA — <https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html>

`published:` is the guide's first year rather than a fixed date. It is living
documentation, continuously revised alongside the hardware, and the record
should not imply a precision the source does not have.

## Why a vendor guide is in the reading list

Because three numbers in the record came from here and were credited to a
paper that does not contain them. [SOTA-013](../practices.d/SOTA-013.md) recommends dynamic loss scaling
that "doubles every 2000 successful steps" and cited only [LIT-011](LIT-011.md) — which
introduces the *mechanism* and prescribes no schedule.

The guide's dynamic-scaling section gives the recipe:

> We successfully trained networks with **N = 2000**, increasing scaling
> factor by **2**, decreasing scaling factor by **0.5**

All three constants, in one sentence, from the organisation that also employed
[LIT-011](LIT-011.md)'s authors. From there they became defaults rather than
recommendations: PyTorch's `torch.amp.GradScaler` ships
`growth_interval=2000`, `growth_factor=2.0`, `backoff_factor=0.5` and
`init_scale=65536.0`, and NVIDIA's own Apex carried them before that.

[ADR-009](../decisions.d/ADR-009.md) admits a source with no arXiv identifier or DOI under a `url:`, which
is what makes this filable.

## The qualifier is the most useful part

The same passage says these are an example and **"many other settings are
valid as well."** So the guide is evidence for *what was tried and worked*,
not for 2000 being optimal, and nothing in the chain from here to
`GradScaler`'s default argues that it is.

That distinction is what the record was missing. A practice quoting 2000 as
though a paper had established it claims more than anyone has shown; quoting
it as the widely-run, once-validated default is exactly right, and is a
weaker and more useful claim.

## Standing in the anthology

The second source of [SOTA-013](../practices.d/SOTA-013.md), alongside [LIT-011](LIT-011.md), which supplies the reason
loss scaling is needed at all. The division of labour is the point: the paper
says why, this says what everyone actually runs and how firmly.
