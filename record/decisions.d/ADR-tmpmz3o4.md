---
status: Active
title: 'The practice vocabulary cannot express a claim about how to evaluate'
version: 1
tags:
- taxonomy
date: '2026-09-10'
issue: '#123'
summary: >-
  Reading the generic-bullet corpus produced four recommendations about
  measurement, and the practice vocabulary has nowhere to file them. The LIT
  side has `analysis-and-evaluation`; the practice side does not, and unlike the
  other two topics missing from it, this one is a kind of claim rather than a
  domain. Adds it, making eleven.
---

# ADR-tmpmz3o4: The practice vocabulary cannot express a claim about how to evaluate

## Context

The practice vocabulary has ten topics. The literature vocabulary has thirteen.
The three the practice side lacks are `generative-modeling`,
`vision-and-graphics` and `analysis-and-evaluation`, and the first two are
absent **on purpose**: [ADR-020](ADR-020.md) scopes this anthology by the *kind of claim*
rather than the domain a technique came from, so a vision paper's
recommendation files under whichever of the ten topics expresses it. A `LIT`
document is about a paper and takes the paper's subject; a `SOTA` document is
about an action and takes the action's kind. The asymmetry is correct.

`analysis-and-evaluation` is not like the other two. Its blurb on the
literature side is "theory, interpretability, benchmarks, measurement,
debugging", and **none of that is a domain** — it is a kind of claim, and the
ten cannot express it.

The gap was invisible until something needed it. Reading the 50 generic-bullet
`LIT` documents ([#123](https://github.com/dmarx/anthology-of-the-sota/issues/123)) produced four recommendations whose subject is
measurement:

| finding | source |
|---|---|
| Check whether an apparently emergent capability is a metric artefact before believing it | `LIT-077`, `LIT-085` |
| Report zero-shot and in-distribution metrics separately; one hyperparameter can optimise them in opposite directions | `LIT-072` |
| Account for test/train document proximity when evaluating, and say what your contamination exposure is | `LIT-060`, `LIT-077` |
| When an objective arrives with its own dataset, state the composition before attributing the effect to the objective | `LIT-080`, `LIT-099` |

None of these is about training, stability, data pipelines, architecture,
attention, inference, adaptation, distribution, systems or representation. They
are about **how you find out whether something worked**, which every one of the
other ten topics presupposes and none of them states.

## Decision

**Add `analysis-and-evaluation` to `record/practices.d/tags.yaml`.** Eleven
topics.

The blurb is narrowed from the literature side's. There, it covers a paper's
subject and reasonably includes theory and interpretability. Here it should
cover an action, so:

> how to find out whether something worked — what to measure, what a
> measurement cannot tell you, and which comparisons are unsound

## Consequences

**The four practices this ADR exists for become fileable**, and are filed in the
same contribution.

<!-- inactive-ok-block: ADR-024 — Proposed, and this whole section is about the relationship to that open decision -->
**It is a fourth vocabulary decision in a row**, which [ADR-021](ADR-021.md) predicted and
[ADR-024](ADR-024.md) is separately about. That is worth stating precisely, because the two
are easy to confuse and are not the same problem:

<!-- inactive-ok-block: ADR-024 — Proposed, and this passage is about the relationship to that open decision -->
- **[ADR-024](ADR-024.md)'s seams are between topics that exist.** Twenty-five unbound
  relations, eighteen of them in four pairs — attention against architecture,
  distributed against architecture, and so on. Every one of those practices has
  a topic; the complaint is that it has *two*.
- **This is a topic that does not exist.** The four practices below have no
  topic at all, and no relaxation of `exactly-one` would give them one.

<!-- inactive-ok-block: ADR-024 — Proposed, and this passage is about the relationship to that open decision -->
So this does **not** preempt [ADR-024](ADR-024.md), and none of its four options addresses
this case. If dmarx settles [ADR-024](ADR-024.md) in a direction that also reorganises the
vocabulary, these four practices retag with everything else.

**The record now has practices about its own epistemics**, which is new and
worth watching. A practice saying "this comparison is unsound" is a different
kind of thing from one saying "use this optimizer", and it is closer to what
`DP` documents do. The distinction held here is that a design principle governs
**how this record is kept**, and these four govern **how the field's claims
should be read** — they are recommendations to a practitioner, with sources, and
that is what a `SOTA` is.

## Alternatives considered

**File them under `training-optimization`.** Three of the four concern training
runs, so it is available. Rejected: it makes the topic mean "anything to do with
training", and the fourth (contamination) is not about training at all. The
whole value of `exactly-one` ([ADR-003](ADR-003.md)) is that the topic is a claim about the
claim, and a topic that absorbs anything is not one.

<!-- inactive-ok-block: ADR-024 — Proposed, and named as the open decision this alternative would wait for -->
**Hold them until [ADR-024](ADR-024.md) is settled.** Rejected: they are evidence *for* a
vocabulary decision, and holding evidence until the decision is made is
backwards. `ADR-021` added three topics on the same reasoning — the corpus grew
past what the vocabulary was written for — and this is the fifth seam, from a
direction that ADR's own "expect a fourth" did not anticipate.

**Widen the practice vocabulary to match the literature one.** Rejected: it
would import `generative-modeling` and `vision-and-graphics`, which
[ADR-020](ADR-020.md) deliberately excludes. The asymmetry between the two vocabularies is
load-bearing and this ADR narrows the gap by one topic rather than closing it.
