---
status: Active
consensus: converged
consensus_note: >-
  The rare case where the introducing paper supplied the replication itself:
  multi-crop was transplanted into SimCLR, DeepCluster and DeepCluster-v2 in
  the same paper and gained 2-4 points in every one. It then propagated —
  DINO and DINOv2 (LIT-tmpfwfu3) both carry a local-crop stage, and the
  `#304` reading found no joint-embedding method after 2020 that went back
  to two full-resolution views. Read as of 2026-09.
title: 'Add many low-resolution views alongside the two full ones, because view count is what helps and resolution is what costs'
version: 1
tags:
- data-pipeline
- representation-and-encoding
date: '2026-09-23'
source:
- LIT-tmp6nq8y
introduced_by:
- LIT-tmp6nq8y
implementations: []
---

# SOTA-tmpoe0zb: Add many low-resolution views alongside the two full ones, because view count is what helps and resolution is what costs

## Source

Caron et al. (2020), [LIT-tmp6nq8y](../literature.d/LIT-tmp6nq8y.md) — [ARXIV-2006.09882](https://arxiv.org/abs/2006.09882).

## The claim

A joint-embedding method compares two augmented views. More views would help
and two is what the budget allows — but only because everyone assumed the
views must be the same size.

**Use a mix of resolutions.** Two standard-resolution crops plus several
smaller ones. The number of comparisons rises; the compute and memory do
not, because the extra views are small. Nothing else about the method
changes.

## Why this is unusually well-evidenced for its size

The paper that introduced it **did not keep it**. Multi-crop was applied to
**SimCLR, DeepCluster and DeepCluster-v2** — three methods with three
different objectives, one of them contrastive with negatives and two
clustering-based — and "consistently improves the performance for all the
considered methods by a significant margin of 2–4% top-1".

That is the transplant test the record usually has to wait for, performed in
the introducing paper. Compare [SOTA-367](SOTA-367.md)'s variance term, the only other
component in this cluster with evidence of working outside its own method.

## What it says about the mechanism, which is more than it looks

If view count is what matters and view *resolution* is mostly what costs,
then the thing a joint-embedding loss is learning from is **the number of
independent comparisons**, not the fidelity of each one. That is consistent
with [SOTA-361](SOTA-361.md) — the augmentation set specifies the task — and it
sharpens it: the task is specified by the *distribution of views*, and you
can sample it more densely for free.

## Conditions

- **The small crops are not free of assumptions.** A low-resolution crop of
  an image is still recognisable as the same object; a low-resolution crop of
  a text span, a spectrogram or a point cloud may not be. The
  resolution/semantics trade is domain-specific and the paper only tests it
  on natural images.
- **Measured on ImageNet, on four methods.** Broad for a component result,
  narrow in domain.
- **It compounds with the augmentation policy rather than replacing it**
  ([SOTA-361](SOTA-361.md)). The crops still need the colour distortion.
- **The asymmetry it introduces is real**: with views of different sizes the
  two branches no longer see the same distribution, which interacts with
  whatever anti-collapse mechanism is in use. SwAV's own is the equipartition
  constraint, not an architectural asymmetry, so the interaction is untested
  for the predictor-and-stop-gradient family ([SOTA-365](SOTA-365.md)).

## Known implementations

-
