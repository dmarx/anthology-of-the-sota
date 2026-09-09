---
number: 62
status: 'Active'
title: 'Scale batch size with model size but sub-linearly'
version: 1
tags:
- model-architecture
date: '2026-08-24'
published: '2021-12-01'
source:
- LIT-061
compared_against:
- SOTA-061
summary: >-
  Fedus et al. (2021), [LIT-061](../literature.d/LIT-061.md) — [ARXIV-2112.10684](https://arxiv.org/abs/2112.10684).
---

# SOTA-062: Scale batch size with model size but sub-linearly

## Source

Fedus et al. (2021), [LIT-061](../literature.d/LIT-061.md) — [ARXIV-2112.10684](https://arxiv.org/abs/2112.10684).

## Sub-linearly, and why the exponent matters more than the direction

Larger models tolerate — and want — larger batches, because the gradient noise
that sets the useful batch size falls as the model gets better at the task.
That the growth is *sub-linear* is the content: doubling parameters does not
double the batch, so the ratio of batch to model size falls as scale rises,
and a rule that scales them together over-shoots at the top end.

The practical failure is quiet. An over-large batch does not diverge; it
spends compute on samples that buy less than they cost, and the run simply
reaches a given loss later than it should have — attributed, usually, to the
data or the schedule.

## What the record has that is better

This is a heuristic from one 2021 study's setup, and the quantity it gropes
toward — critical batch size — is measurable and has since been characterised
directly. The record's own material is stronger: [SOTA-092](SOTA-092.md) and [SOTA-093](SOTA-093.md) give
the mechanism, and the ramp implied by them is what large runs actually do.

Kept because it is true and because a rule of thumb is useful when nobody is
going to measure. But a reader with a measurement should prefer it, and the
practice should not be read as licensing a fixed batch-to-parameter ratio,
which is the reading its title most invites.
