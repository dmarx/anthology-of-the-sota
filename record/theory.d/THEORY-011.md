---
number: 11
status: Active
formerly:
- THEORY-tmp3jmjc
title: 'Skip connections make a deep network trainable by smoothing the loss surface, not by making it more expressive'
version: 1
tags:
- model-stability
date: '2026-09-15'
source:
- LIT-014
explains:
- SOTA-032
- SOTA-051
- SOTA-060
- SOTA-136
- SOTA-169
summary: >-
  Li et al. (2017), [LIT-014](../literature.d/LIT-014.md) — the same deep network plotted with and without
  skip connections gives a chaotic surface with visible barriers between
  nearby points, and a smooth near-convex one. The claim is about
  *trainability* rather than capacity: the residual network is not a larger
  function class, it is a reachable one. It is the reason depth stopped being
  the barrier it had been, and the reason every practice in this record about
  residual streams is about what to do with them rather than whether to have
  them.
---

# THEORY-011: Skip connections make a deep network trainable by smoothing the loss surface, not by making it more expressive

## The claim

Plot the loss of a deep network over a two-dimensional slice of parameter
space, once with skip connections and once without, with everything else held
fixed. Without them the surface is chaotic — non-convex, with visible barriers
between points that are near each other. With them it is smooth and close to
convex over the region plotted.

The consequence is the part that matters, and it is a claim about
**trainability rather than capacity**. A residual network is not a richer
function class than the same network without the identity path; it is one
whose minima gradient descent can reach. Depth stopped being the barrier it
had been not because deeper networks could suddenly represent more, but
because the surface between initialization and a minimum stopped having walls
in it.

## What rests on it

This is the account under every practice in the record about residual streams,
and it is why none of them is about *whether* to have one:

- Where to normalise relative to the identity path — [SOTA-032](../practices.d/SOTA-032.md).
- How weakly to initialise the branch that joins it — [SOTA-051](../practices.d/SOTA-051.md), [SOTA-060](../practices.d/SOTA-060.md).
<!-- inactive-ok-block: SOTA-136, SOTA-169 — Proposed, and named as the open
     question this account underwrites rather than settles -->
- How many streams to run, and how to mix them — [SOTA-136](../practices.d/SOTA-136.md), [SOTA-169](../practices.d/SOTA-169.md), both
  `Proposed`, and both open questions of the form *how far does the smoothing
  argument stretch?*

That the identity path itself goes unfiled is [DP-007](../../docs/design-principles.md#dp-7) working as intended: a
recommendation every model already follows has no author to cite and nobody to
tell.

## Why it is `Active`

It is the best explanation this record holds for the thing, it is the one the
field reaches for, and nothing here contradicts it. The status is about the
account's standing, not about the strength of the figure — which is the next
section's business, and is weaker than the status suggests.

## What the evidence does not cover

**The visualisation is a two-dimensional slice through a very high-dimensional
surface**, along random filter-normalised directions. It is evidence about the
geometry, not a measurement of it, and the paper is careful about this in a
way summaries of it usually are not. What survives is the qualitative
contrast, which is large and reproduces.

**Smoothness in a slice is not convexity in the space.** The claim as this
record holds it is comparative — *smoother than the same network without* —
and nothing here licenses the stronger reading that the residual loss surface
is well-behaved in absolute terms.

**It says nothing about how far the argument stretches.** If skip connections
<!-- inactive-ok-block: SOTA-136, SOTA-169 — Proposed, and the open question
     this account raises without answering -->
help because they smooth, do two residual streams smooth more? [SOTA-136](../practices.d/SOTA-136.md) and
[SOTA-169](../practices.d/SOTA-169.md) are that question, filed as practices and unresolved, and this
account does not answer them — it is why the question is worth asking.
