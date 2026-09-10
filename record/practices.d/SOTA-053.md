---
number: 53
status: 'Active'
title: 'Special handling for gated architectures'
version: 1
tags:
- model-stability
date: '2026-08-24'
source:
- LIT-047
summary: >-
  Bachlechner et al. (2020), [LIT-047](../literature.d/LIT-047.md) — [ARXIV-2003.04887](https://arxiv.org/abs/2003.04887).
---

# SOTA-053: Special handling for gated architectures

## Source

Bachlechner et al. (2020), [LIT-047](../literature.d/LIT-047.md) — [ARXIV-2003.04887](https://arxiv.org/abs/2003.04887).

## What is special about a gate

A gated architecture already has a multiplicative path — a sigmoid or SiLU
factor deciding how much of a branch passes — so adding ReZero's scalar
([SOTA-051](SOTA-051.md)) on top puts two multiplicative controls in series on the same
signal. Initialising both toward closed means the branch is doubly suppressed
and its gradient is the product of two small numbers, which is slower than
either alone.

The handling the title asks for is therefore about not stacking the
suppressions: initialise the gate's bias so it starts open, or drop the extra
scalar and let the gate itself be the thing that starts near zero.

## What the record cannot say

Which of those two, or by how much. [LIT-047](../literature.d/LIT-047.md)'s contribution is the scalar and
its analysis in plain residual stacks; the gated case is a caveat rather than
a result, and this practice inherits the caveat without the answer.

That matters more now than it did, because the gated architectures in this
<!-- inactive-ok-block: SOTA-177, SOTA-178 — Proposed, cited as the gated architectures this caveat now applies to -->
record — the delta-rule recurrences of [SOTA-177](SOTA-177.md) and [SOTA-178](SOTA-178.md), the gated linear
attention families — are exactly the case. The practice flags a real
interaction and leaves the reader to resolve it.

Flagged for restatement: what it can honestly say is *"do not stack a
zero-initialised residual scalar on top of a closed gate"*, which is
narrower than "special handling" and is actually actionable.
