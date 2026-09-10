---
status: Active
consensus: emerging
consensus_note: >-
  That some emergence is a metric artefact is well evidenced and widely cited.
  What share of it is remains open — no one has put a number on it, and this
  practice deliberately recommends the check rather than the conclusion.
title: 'Check whether an emergent capability is a metric artefact before believing it'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-10'
source:
- LIT-077
- LIT-085
implementations: []
---

# SOTA-tmpwccgh: Check whether an emergent capability is a metric artefact before believing it

## Source

Srivastava et al. (2022), [LIT-077](../literature.d/LIT-077.md) — BIG-bench, 204 tasks across three
model families from millions to hundreds of billions of parameters, with expert
human raters.

Nanda et al. (2023), [LIT-085](../literature.d/LIT-085.md) — the grokking analysis, which reverse-engineers
one network and recovers the continuous progress underneath its discontinuity.

## The claim

A capability that appears suddenly at some scale may be appearing suddenly in
your **measurement** rather than in the model. Before treating a jump as a
finding about learning, check two things:

**Is the metric all-or-nothing over multiple steps?** BIG-bench's
categorisation is direct: tasks that improve gradually "commonly involve a large
knowledge or memorization component, whereas tasks that exhibit *breakthrough*
behavior at a critical scale often involve multiple steps or components, **or
brittle metrics**." A task scored only when every step is right improves
invisibly until the last step lands, and then appears to jump. Nothing about the
model was discontinuous.

**Is the discontinuity a property of the regime?** Grokking — delayed
generalization long after memorization — is the most-cited mysterious training
phenomenon of its period, and `LIT-085` finds it **disappears above roughly 60%
data**. At sufficiently large data fractions generalization is immediate.
Smaller fractions grok more slowly. The phenomenon is real and it is a
data-starved-regime phenomenon, not a fundamental one.

## What a positive check looks like

`LIT-085` is also the demonstration that the underlying quantity can be found,
and the honest caveat about what that costs. Its progress measures — restricted
loss and excluded loss — are computed by projecting onto or removing the five
key frequencies the network was **reverse-engineered** to be using. They are
meaningless without that reverse-engineering, and they show continuous progress
through the transition.

So "find the continuous measure underneath" is not cheap advice. What is cheap
is the negative check: **look at whether your metric can express partial
progress**, and whether the effect survives a change in data fraction.

## Conditions

`LIT-077` is a categorisation across 204 heterogeneous tasks, not a controlled
experiment, and it puts no number on what share of observed emergence is
artefactual. `LIT-085` is one modular-addition task on a one-layer transformer
with weight decay `λ = 1` — the authors call the generalisation to emergence "a
proof of concept" and it is nonetheless how the paper is usually cited.

Neither source licenses "emergence is not real". They license **asking**, and
they name two specific things to ask about.

## Known implementations

- BIG-bench's *linearity vs breakthroughness* axis is the categorisation itself
