---
number: 178
status: Proposed
formerly:
- SOTA-tmpr2k8m
promote_when: >-
  A released model above 3B built on this recurrence, or a demonstration that
  the state-tracking advantage shows up on a language task at a scale where
  the record's hybrids operate. The complexity result is a claim about what
  the architecture *can* represent; what would promote this is evidence that
  the capability is reached by training and matters for language.
consensus: unreplicated
consensus_note: >-
  One group and one line, reaching vector-valued gating independently of the
  gated-delta line the record recommends. Nothing disputes it; nothing at
  frontier scale runs it either, and the largest released model is 2.9B.
title: 'Give the recurrence vector-valued gating and in-context learning rates so it can track state a softmax layer provably cannot'
version: 1
tags:
- model-architecture
date: '2026-09-08'
published: '2025-03-01'
source:
- LIT-173
implementations:
- 'RWKV-7 Goose (0.19B–2.9B)'
summary: >-
  Peng et al. (2025), [LIT-173](../literature.d/LIT-173.md) — a generalised delta rule with vector-valued
  gating and in-context learning rates, at constant memory and constant time
  per token. A 2.9B model sets the 3B state of the art on multilingual tasks
  on dramatically fewer training tokens. The expressivity claim is the sharp
  one: it can recognise all regular languages, which under standard
  conjectures exceeds what a softmax stack in TC⁰ can do.
---

# SOTA-178: Give the recurrence vector-valued gating and in-context learning rates so it can track state a softmax layer provably cannot

## Source

Peng et al. (2025), [LIT-173](../literature.d/LIT-173.md) — [ARXIV-2503.14456](https://arxiv.org/abs/2503.14456).

A generalised delta rule with **vector-valued gating** and **in-context
learning rates**, plus a relaxed value-replacement rule. Constant memory and
constant inference time per token. Released Apache 2.0 with a 3.1T-token
multilingual corpus and four models from 0.19B to 2.9B.

The vector-valued gate is the same move Kimi Delta Attention makes, arrived
at independently and from a different tradition — recurrent networks rather
than linear attention. Two lines converging on per-channel gating is worth
holding as two data points rather than one.

## Why this is not just another module

The reported result is efficiency-flavoured: a 2.9B model setting the 3B
state of the art on multilingual tasks and matching it in English, **while
trained on dramatically fewer tokens** than what it is compared against.

The expressivity result is the one that cuts against an assumption the rest
of the record makes. RWKV-7 can perform **state tracking and recognise all
regular languages** while remaining parallelisable to train — which, under
standard complexity conjectures, **exceeds what a softmax stack can do**,
since those are limited to TC⁰.

That inverts the usual justification. [SOTA-132](SOTA-132.md) interleaves linear layers
with global attention because the linear layers are *cheaper* and the
attention supplies capability they lack. This says the capability gap runs
the other way for state tracking: the recurrence can do something attention
provably cannot.

**The record should hold that claim without leaning on it.** A complexity
result is about what an architecture can represent, not about what training
finds, and whether it matters for language modelling at scale is not settled
by a 2.9B model. But a hybrid practice justified by "linear is cheap,
attention is capable" is resting on half of a picture, and this is the other
half.

## Conditions, and why this is Proposed

One group, one line, nothing above 2.9B, and no frontier deployment. The
comparison the record would most want — this recurrence against the gated
delta rule it recommends, at matched scale — has not been run by anyone.

## Known implementations

- RWKV-7 "Goose", 0.19B to 2.9B. Nothing else in the record.
