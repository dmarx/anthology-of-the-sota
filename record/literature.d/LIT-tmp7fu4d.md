---
status: Active
title: 'Scaling Data-Constrained Language Models'
version: 1
tags:
- data-pipeline
date: '2026-09-05'
published: '2023-05-01'
arxiv: '2305.16264'
first_author: 'Muennighoff'
keywords:
- 'data-repetition'
- 'scaling-laws'
- 'epochs'
- 'data-constrained'
- 'compute-optimality'
summary: >-
  Muennighoff et al. (2023), [ARXIV-2305.16264](https://arxiv.org/abs/2305.16264). Up to four epochs of
  repeated data cost almost nothing against unique data at fixed compute;
  past that the value of added compute decays to zero. 400 runs, up to 900B
  tokens and 9B parameters.
---

# LIT-tmp7fu4d: Scaling Data-Constrained Language Models

Muennighoff et al. (2023) — [ARXIV-2305.16264](https://arxiv.org/abs/2305.16264)

## Key takeaways

- Sets up the regime the field has since entered: extrapolating the
  parameters-and-tokens trend runs into the amount of text that exists, so
  the interesting question becomes what happens when data, not compute, is
  the binding constraint.
- The headline result, from a sweep over repetition and compute budget up to
  900B tokens and 9B parameters: **with constrained data at fixed compute,
  training on up to four epochs of repeated data changes the loss negligibly
  against having that much unique data.** Repetition is close to free, up to
  a point.
- Past that point it is not: with more repetition, the value of adding
  compute decays toward zero. Both halves matter — the first licenses
  repetition, the second bounds it.
- A scaling law for compute optimality that prices in the decreasing value of
  repeated tokens *and* of excess parameters, validated empirically.
- Mitigations for data scarcity are tested too: adding code data to the
  mixture, and removing commonly used filters.
- 400 training runs, with models and datasets released.

## Standing in the anthology

The counter-evidence to [SOTA-124](../practices.d/SOTA-124.md), and filed to make that disagreement
legible rather than to settle it.

[SOTA-124](../practices.d/SOTA-124.md) says the quantity that governs safe repetition is not epoch
*count* but epoch *size* relative to the model's memorization window, and on
that basis Falcon-H1-Tiny repeated SFT sources a hundred times or more. This
paper says four epochs, and it has 400 runs behind it where [SOTA-124](../practices.d/SOTA-124.md) has one
figure and an argument its own authors call early.

The two are not quite measuring the same thing, which is the interesting
part: this sweep repeats a *whole corpus* under a fixed compute budget, while
the memorization-window claim is about one high-quality *source inside a
mixture*, where a small share means a large delay between repeats. That is a
real distinction and it may dissolve the conflict — or it may be the
mechanism by which a 100× repetition is quietly costing something nobody
measured. Nobody has run the experiment that would tell them apart, and
[SOTA-124](../practices.d/SOTA-124.md) stays *Proposed* partly for that reason.
