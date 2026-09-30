---
number: 364
status: Active
formerly:
- SOTA-tmpw2bcy
consensus: converged
consensus_note: >-
  Two independent groups hit it within three months and shipped two different
  fixes — MoCo shuffles the batch across devices, SimCLR aggregates the
  statistics globally — which is stronger evidence than either paper alone
  and is why this carries two sources (`ADR-010`). A third contemporary
  approach named in both papers avoids the problem by using layer norm.
  Converged in the sense that the failure is known and handled, not in the
  sense that one fix won. Read as of 2026-09.
title: "Break batch normalization's cross-sample leak before it solves your contrastive task for you"
version: 1
tags:
- model-stability
- distributed-optimization
date: '2026-09-23'
source:
- LIT-590
- LIT-591
introduced_by:
- LIT-590
implementations: []
---

# SOTA-364: Break batch normalization's cross-sample leak before it solves your contrastive task for you

## Source

He et al. (2019), [LIT-590](../literature.d/LIT-590.md) — [ARXIV-1911.05722](https://arxiv.org/abs/1911.05722), §3.3, and Chen et al.
(2020), [LIT-591](../literature.d/LIT-591.md) — [ARXIV-2002.05709](https://arxiv.org/abs/2002.05709), §2.2. Two groups, three months
apart, the same bug and two different fixes.

## The claim

Batch normalization makes each sample's activations depend on the other
samples in its batch. In a contrastive objective **the other samples in the
batch are the answer**, so BN hands the model a channel through which the
positive can be identified without learning anything.

The symptom is diagnostic and easy to misread as success: **the pretext task
gets solved quickly and the representation stays bad.** MoCo's words are that
the model "appears to 'cheat' the pretext task and easily finds a low-loss
solution"; SimCLR's are that it "can exploit the local information leakage to
improve prediction accuracy without improving representations".

MoCo's appendix names the mechanism exactly: with per-device BN, the
sub-batch statistics act as **a signature telling the model which sub-batch
the positive key is in**. It does not need to compare content at all.

## The two fixes

- **Shuffle (MoCo).** Permute the mini-batch order across devices before
  encoding with the **key encoder only**, then unshuffle. A query and its
  positive key then land in different device sub-batches, so their statistics
  come from different subsets and the signature is destroyed. The query
  encoder's order is untouched.
- **Aggregate (SimCLR).** Compute BN mean and variance across **all** devices,
  so there is no per-device signature to read. Simpler, and it costs a
  synchronisation per BN layer.

A third option both papers name is to avoid the normalization that causes it
— layer norm has no cross-sample dependence, which is why this failure does
not appear in transformer-based contrastive models.

## Why it is worth its own document

Because the failure is silent in the only place people look. Training loss
drops *faster* with the bug than without it. Nothing in the loop reports it,
and the pretext-task accuracy — the natural thing to monitor — moves in the
wrong direction, so the metric that should catch it endorses it instead. Both
papers found it by noticing that a good-looking run produced a bad
representation.

MoCo's Figure A.1 is the shape to recognise: the pretext-task curve tracking
high while a kNN monitor on real classification stalls, and "training longer
without shuffling BN overfits more".

## Conditions

- **This is specific to normalization that mixes samples.** BN and its
  relatives; not layer norm, RMSNorm or group norm.
- **The memory-bank mechanism is immune** and the papers say so: its positive
  keys come from earlier mini-batches, so there is no shared batch to leak
  through. Immunity here is a property of the negative-sampling mechanism, not
  a virtue of memory banks.
- **It generalises past contrastive learning to any objective whose label is
  a function of batch membership** — in-batch ranking, batch-wise
  discrimination, some retrieval losses. The test is whether a sample's
  target can be inferred from which batch it is in.
- **The two fixes are not equivalent in cost.** Global aggregation adds
  communication at every BN layer; shuffling adds a permutation and its
  inverse once per key-encoder forward pass.

## Known implementations

-
