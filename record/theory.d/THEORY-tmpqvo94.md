---
status: Active
title: 'A lottery ticket wins by re-learning the solution its dense run already found'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
source:
- LIT-039
corrects:
- THEORY-tmp6auqn
summary: >-
  Evci et al. (2020), [LIT-039](../literature.d/LIT-039.md) — sparse networks trained from scratch do worse
  because gradient flow at initialization is poor, and a rewound ticket does
  not escape that by having found a good sparse architecture: it lands back
  in the basin the dense pruning run reached. The hypothesis survives as a
  claim about initialization, not about architecture.
---

# THEORY-tmpqvo94: A lottery ticket wins by re-learning the solution its dense run already found

## Source

Evci, Ioannou, Keskin and Dauphin (2020), [LIT-039](../literature.d/LIT-039.md).

## What was actually shown

<!-- inactive-ok: THEORY-tmp6auqn — Proposed, and this document is part of why: cited as the claim being qualified, not as a settled one. -->
The question is the one [THEORY-tmp6auqn](THEORY-tmp6auqn.md) leaves open: why does a sparse
structure trained from a random initialization do worse than the same
structure obtained by pruning a dense network? The answer offered is gradient
flow — sparse networks at initialization have poor flow, and training from
scratch has to overcome that before it can make progress on the task.

The part that bears on the ticket is the deflation. A rewound ticket is
followed and found to re-learn the solution its dense pruning run had already
reached: it lands in the same basin rather than discovering, independently,
that this sparse structure was a good one.

## What it corrects

<!-- inactive-ok: THEORY-tmp6auqn — Proposed; the sentence says exactly which part of it survives, which is what citing an unsettled claim owes. -->
Not the existence result. The measurement in [THEORY-tmp6auqn](THEORY-tmp6auqn.md) stands, and
nothing here says the ticket fails to match the dense network.

What breaks is the reading — that a search has located a sparse architecture
worth having. The claim that survives is narrower and more specific: the
initialization of the surviving weights carries information about the
solution the dense run arrived at, and the ticket's job is to get back there.
"Sparse architectures are findable" becomes "the initialization remembers",
and only the second is supported.

## What this does not say

It does not say the phenomenon is uninteresting. That initial values carry
recoverable information about a solution reached much later is a strong
statement about training dynamics, and it is the reason both of these
documents are in the record.

It does not license a recommendation, in either direction. The record holds no
pruning or sparsity practice, and neither of these two documents is the thing
that would create one — which is the state this scheme was added to be able to
file honestly rather than as a gap in the practice registry.
