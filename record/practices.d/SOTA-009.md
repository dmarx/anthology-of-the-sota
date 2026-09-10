---
number: 9
status: 'Active'
title: 'warmup to a large early lr, anneal throughout training to small final lr'
version: 1
tags:
- training-optimization
date: '2026-08-24'
source:
- LIT-010
summary: >-
  Smith et al. (2017), [LIT-010](../literature.d/LIT-010.md) — [ARXIV-1708.07120](https://arxiv.org/abs/1708.07120).
compared_against:
- SOTA-100
---

# SOTA-009: warmup to a large early lr, anneal throughout training to small final lr

## Source

Smith et al. (2017), [LIT-010](../literature.d/LIT-010.md) — [ARXIV-1708.07120](https://arxiv.org/abs/1708.07120).

## The shape, and what each part is doing

Ramp to a peak, then decay to a small final value. The ramp is [SOTA-008](SOTA-008.md)'s
argument; the decay is the part this practice adds, and its justification is
different: late in training the gradient's useful component is small relative
to its noise, so a large step mostly moves the parameters around a basin
rather than into it. Shrinking the rate turns the run from exploring to
settling.

## What has moved, and it is most of this

<!-- inactive-ok-block: SOTA-039 — Superseded, named as the default this practice describes and as what replaced it -->
The record's own line has largely left this shape. [SOTA-039](SOTA-039.md) — a single cosine
cycle, the default this practice describes — is Superseded by [SOTA-140](SOTA-140.md)'s
warmup-stable-decay, and the reason is a property the cosine shape lacks:
cosine has to know the total token budget in advance, because the schedule's
endpoint is baked into its curve. Stable-then-decay leaves the budget open,
so a run can be extended without invalidating the schedule it has been
following.

<!-- inactive-ok-block: SOTA-141, SOTA-156 — Proposed, cited as how far past this shape the record's line has gone -->
[SOTA-141](SOTA-141.md) goes further and decays linearly to exactly zero, and [SOTA-156](SOTA-156.md) argues
the schedule can be dispensed with entirely by averaging iterates.

So this practice is best read as the frame those variations are stated
against — "warm up, then anneal" is still the shape, and every specific answer
about *how* has moved past it. Kept Active because the frame holds; a reader
choosing a schedule today should be reading [SOTA-140](SOTA-140.md) rather than this.
