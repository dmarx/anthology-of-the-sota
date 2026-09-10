---
number: 1
status: 'Active'
consensus: universal
consensus_note: >-
  Adam as the default optimizer is what a paper departs from rather than
  argues for.
title: 'Use Adam as the default optimizer absent a reason to choose otherwise'
version: 2
history:
- version: 1
  note: >-
    Titled "Default choice for neural network training", which never named its
    subject. A practice whose title does not say what it recommends cannot be
    cited, searched for or contested — and this one is contested, by SOTA-121
    at scale and by SOTA-120 on the weight-decay half.
- version: 2
  note: >-
    Retitled to state the recommendation. The choice is unchanged and was
    always Adam: the source is LIT-001, and the consensus note already read
    "Adam as the default optimizer is what a paper departs from rather than
    argues for." Only the title changed.
tags:
- training-optimization
date: '2026-08-24'
source:
- LIT-001
summary: >-
  Kingma et al. (2014), [LIT-001](../literature.d/LIT-001.md) — [ARXIV-1412.6980](https://arxiv.org/abs/1412.6980).
---

# SOTA-001: Use Adam as the default optimizer absent a reason to choose otherwise

## Source

Kingma et al. (2014), [LIT-001](../literature.d/LIT-001.md) — [ARXIV-1412.6980](https://arxiv.org/abs/1412.6980).

## The claim

Adam is what to reach for absent a reason to do otherwise, and it is
[LIT-001](../literature.d/LIT-001.md) that the record leans on for it.

That is defensible and was more so when it was written. Adam combines
AdaGrad's per-parameter scaling with RMSProp's decaying average and corrects
the bias in both moments, which makes it insensitive to gradient scale and so
usable without the per-problem tuning SGD with momentum needs. The cost is
memory — two extra states per parameter, the 8 bytes that [SOTA-015](SOTA-015.md) keeps in
FP32 and that ZeRO exists to partition ([SOTA-028](SOTA-028.md)).

## The title, which was the reason this body was written

Until version 2 this practice was called "Default choice for neural network
training", which never says *of what*. A title that does not name its subject
cannot be cited, searched for, or contested — and this practice is contested:
[SOTA-121](SOTA-121.md) argues Muon beats the default at scale, and the weight-decay half is
[SOTA-120](SOTA-120.md). Neither disagreement could attach to the old title.

It read as a fragment of the note it was promoted from, and it is one of
several on the [#107](https://github.com/dmarx/anthology-of-the-sota/issues/107) worklist in that shape — `SOTA-036` ("gpt training
recipe") is the other clear case, still open.

## Where the default has actually moved

To AdamW rather than Adam — decoupled weight decay is now the default in every
framework and every large run in this record — and, at frontier scale, to
Muon and its relatives. This practice as written cannot express either, which
is the practical cost of the title.
