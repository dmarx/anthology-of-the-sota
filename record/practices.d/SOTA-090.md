---
number: 90
status: 'Active'
title: 'Use hardware-specific memory layouts'
version: 1
tags:
- systems-optimization
date: '2026-08-24'
published: '2020-06-01'
source:
- LIT-066
summary: >-
  Ivanov et al. (2020), [LIT-066](../literature.d/LIT-066.md) — [ARXIV-2007.00072](https://arxiv.org/abs/2007.00072).
---

# SOTA-090: Use hardware-specific memory layouts

## Source

Ivanov et al. (2020), [LIT-066](../literature.d/LIT-066.md) — [ARXIV-2007.00072](https://arxiv.org/abs/2007.00072).

## The same finding as [SOTA-082](SOTA-082.md), from the other side

TVM's claim is that a compiler should choose layouts; [LIT-066](../literature.d/LIT-066.md)'s is that the
layouts frameworks choose by default are **suboptimal** — a statement about
defaults rather than about a missing capability, which is what makes it
actionable without new tooling.

Both matter to a reader for different reasons. [SOTA-082](SOTA-082.md) says the choice is
being made for you and the symptom of a bad one is a transpose in the profile.
This says the default is worth doubting: the layout a framework picks was
tuned for some hardware, and it may not be yours.

## What a reader can actually do

Not much by hand, and the practice should say so rather than implying a knob.
The available moves are choosing among the layouts a framework exposes
(channels-last, for instance), keeping a model in one layout end to end so no
conversion is inserted, and — where it matters enough — letting a compiler
retune ([SOTA-084](SOTA-084.md)).

The cost of getting it wrong is not a crash but a steady tax that looks like
the model simply being that expensive. That is why it belongs beside
[SOTA-091](SOTA-091.md): the layout question is invisible until something is measuring
bytes moved rather than time elapsed.
