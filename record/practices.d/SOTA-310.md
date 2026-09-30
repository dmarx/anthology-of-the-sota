---
number: 310
status: Active
formerly:
- SOTA-tmp2f1hx
consensus: unreplicated
consensus_note: >-
  One group, one paper. It is filed `Active` on that because the result is a
  demonstration rather than an estimate — exhaustive enumeration cannot be
  underpowered — and because the counts are lower bounds, so the direction of
  any error is known. What has not been shown is the size of the problem in
  transformers at scale, and the paper says so. Against it, the prevailing
  practice of reporting one circuit is not a competing measurement; nobody had
  counted.
title: 'Treat a mechanistic explanation that passes circuit error or causal alignment as one of many, and report what you did to rule the others out'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-504
introduced_by:
- LIT-504
implementations: []
summary: >-
  Méloux, Maniu, Portet and Peyrard (2025), [LIT-504](../literature.d/LIT-504.md) — by
  exhaustive enumeration on small MLPs, **no network** had exactly one circuit
  interpretation and **under 2%** had exactly one valid minimal mapping. The
  median number of explanations satisfying the criteria rises from **38 to
  910,000** as width goes 2 → 5, and both counts are lower bounds. Passing
  circuit error or IIA establishes that an explanation is admissible, not that
  it is the explanation.
---

<!-- inactive-ok-file: SOTA-286 — Proposed, cited as one of the two existing
     practices this one completes a set with. The citation is about what the
     three are severally about, which does not wait on any of them being
     settled -->

# SOTA-310: Treat a mechanistic explanation that passes circuit error or causal alignment as one of many, and report what you did to rule the others out

## Source

Méloux, Maniu, Portet and Peyrard (2025), [LIT-504](../literature.d/LIT-504.md) —
read as [NOTE-251](../notes.d/NOTE-251.md).

## When this applies

You have found a circuit, a feature interpretation, or an algorithm causally
aligned with a network's internals, and it passes the field's criteria — low
circuit error, or interchange-intervention accuracy of one. You are about to
describe it as *the* mechanism.

## Do this

**Say what else would have passed.** The criteria are satisfiability tests,
not selection rules, and the satisfying set is large:

| | median explanations found |
|---|---|
| circuit-first, width 2 → 5 | **38 → 910,000** |
| algorithm-first, width 2 → 5 | **8 → 3,700** |

Under **2%** of trained networks had exactly one valid minimal mapping. **No
network** had exactly one circuit interpretation. Both figures are lower
bounds: circuit enumeration was capped at sparsity above 0.3 and to
two-input/one-output circuits, and interpretations were counted only for the
sparser circuits.

Concretely, report at least one of: how many alternatives you enumerated and
rejected; which criterion beyond the passing one you applied; or — the honest
minimum — that you did not count, so the reader knows the claim is
"an explanation" and not "the explanation".

**Do not reach for sparsity as the tiebreak.** The source considers and
rejects it, in a sentence worth carrying: "Should we dismiss an entirely
different candidate explanation simply because it involves one additional node
than another?" In their experiments simplicity did not single anything out.

**Say which epistemic goal the explanation is serving.** This is the source's
own constructive recommendation and it costs nothing. If predictivity and
manipulability are what you need, non-unicity may not matter at all and you
can say so. If you are making a claim about *the* mechanism — because
something downstream depends on it being the mechanism — then unicity is load
bearing and unestablished.

## What does reduce the count

One lever, reported and modest: the number of valid abstractions **decreases
significantly with the number of tasks** a network is trained on (`p = 0.05`),
up to four tasks, past which the variation stops being significant. Adding
input noise decreases circuits while *increasing* interpretations in the
circuit-first method, and tightening the loss cutoff moves the counts without
closing the gap. Training dynamics narrow the space; they do not collapse it.

## Why `Active` on one paper

Because the claim is a demonstration, not an estimate. Exhaustive enumeration
over a space small enough to enumerate cannot be underpowered, and the
reported counts are lower bounds by construction — so if the numbers are
wrong, they are wrong in the direction that makes the problem worse. The
recommendation that follows is also free: it asks for a sentence about what
was not ruled out.

## Conditions

**Toy models for the enumeration.** MLPs of shape `(2, k, k, n)` trained on
two-input logic gates. Transformers, real tasks and scale are a different
regime, and the source is explicit that it has not tested them.

**One demonstration at scale, and it is a partial one.** A regression MLP on
MNIST digits 0 and 1, split so that the `(3, 3, 3, 1)` tail could be
enumerated against the head's partial computations: **3,209 valid circuits**
in the tail. The argument that the whole network has at least that many is
sound — any valid circuit in the head extends through one of them — and it is
still one network, one task, one architecture.

**The burden-shifting argument is the paper's, and it is fair.** If the
problem vanishes at scale, "why the problems would disappear at larger scales
must be demonstrated". That is an argument about where the burden sits rather
than evidence about large models, and this practice should not be read as
having measured them.

**Non-unicity may not be a defect.** §5.1 takes the pragmatic position
seriously: an explanation that predicts and supports intervention may be
everything that is owed, and the interpretability-illusion debate the paper
cites was resolved that way. This practice asks for the count and the stated
goal, not for the count to be one.

## Related

[SOTA-278](../practices.d/SOTA-278.md) says to rule out the evaluation before reporting that a
model cannot do something. [SOTA-286](../practices.d/SOTA-286.md) says to measure how much of
parameter space behaves the way your sample does. This is the same discipline
at the explanation end: what you found passing a criterion is one member of a
set nobody has counted, and the criterion does not know which member it is.
