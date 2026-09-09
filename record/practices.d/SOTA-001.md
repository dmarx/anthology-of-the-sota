---
number: 1
status: 'Active'
consensus: universal
consensus_note: >-
  Adam as the default optimizer is what a paper departs from rather than
  argues for.
title: 'Default choice for neural network training'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2014-12-01'
source:
- LIT-001
summary: >-
  Kingma et al. (2014), [LIT-001](../literature.d/LIT-001.md) — [ARXIV-1412.6980](https://arxiv.org/abs/1412.6980).
---

# SOTA-001: Default choice for neural network training

## Source

Kingma et al. (2014), [LIT-001](../literature.d/LIT-001.md) — [ARXIV-1412.6980](https://arxiv.org/abs/1412.6980).

## What the practice is, once the title is read charitably

"Default choice for neural network training" does not say what the default
*is*. It is SOTA-001 in a registry whose first source is [LIT-001](../literature.d/LIT-001.md), so the
subject is Adam, and the claim is that Adam is what to reach for absent a
reason to do otherwise.

That claim is defensible and was more so when it was written. Adam combines
AdaGrad's per-parameter scaling with RMSProp's decaying average and corrects
the bias in both moments, which makes it insensitive to gradient scale and so
usable without the per-problem tuning SGD with momentum needs. The cost is
memory — two extra states per parameter, the 8 bytes that [SOTA-015](SOTA-015.md) keeps in
FP32 and that ZeRO exists to partition ([SOTA-028](SOTA-028.md)).

## The title is a finding, not just a style complaint

A practice whose title does not name its subject cannot be cited, searched
for, or checked. It reads as a fragment of the note it was promoted from, and
it is one of several on the [#107](https://github.com/dmarx/anthology-of-the-sota/issues/107) worklist in that shape — `SOTA-036` ("gpt
training recipe") is the other clear case.

Retitling changes what the practice asserts, so it is not done here. The
version worth having is roughly *"use Adam or AdamW as the default optimizer
absent a reason to choose otherwise"*, which is checkable and which the record
would then be able to contest: [SOTA-121](SOTA-121.md) argues Muon beats it at scale, and the
<!-- inactive-ok: SOTA-120 — Deferred, named as the half of the default this practice cannot express -->
weight-decay half is [SOTA-120](SOTA-120.md), already `Deferred`.

## Where the default has actually moved

To AdamW rather than Adam — decoupled weight decay is now the default in every
framework and every large run in this record — and, at frontier scale, to
Muon and its relatives. This practice as written cannot express either, which
is the practical cost of the title.
