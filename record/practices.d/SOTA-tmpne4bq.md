---
status: Proposed
promote_when: >-
  A cheap estimator for the singular-value decay of a real pretraining
  context, demonstrated on one — without it the criterion names a quantity
  nobody can measure. Or a controlled comparison of two contexts whose decay
  rates were computed in advance, with the predicted one winning. And,
  separately, this record reading the source properly: the note behind it is
  `Skimmed`, and promoting a practice whose theorems nobody here has checked
  would be the wrong order.
consensus: unassessed
consensus_note: >-
  One dissertation, read at summary level. The record has not looked at
  whether the field agrees, and saying `unassessed` is more honest than
  inferring a consensus from a document nobody here has read through.
title: 'Choose a pretraining context whose association with the input is neither too strong nor too weak, and mix contexts to get there'
version: 1
tags:
- training-optimization
- representation-and-encoding
date: '2026-09-20'
source:
- LIT-tmpguznl
introduced_by:
- LIT-tmpguznl
implementations: []
summary: >-
  Zhai (2025), [LIT-tmpguznl](../literature.d/LIT-tmpguznl.md) — a pretraining objective is an association
  between the input and a context variable, and the useful contexts are the
  ones whose association is neither too strong nor too weak: the singular
  values of the expectation operator should decay neither too fast nor too
  slowly. Contexts that individually miss the range can be mixed into one
  that does not.
---

# SOTA-tmpne4bq: Choose a pretraining context whose association with the input is neither too strong nor too weak, and mix contexts to get there
<!-- inactive-ok-file: SOTA-256 — Proposed, and named as the practice whose asymptote this one locates in the context -->
<!-- inactive-ok-file: NOTE-tmpmg0fm — Skimmed, and cited precisely to record that this practice rests on a skim (ADR-025) -->

## Source

Zhai (2025), [LIT-tmpguznl](../literature.d/LIT-tmpguznl.md) — [ARXIV-2504.19792](https://arxiv.org/abs/2504.19792), a CMU dissertation.

**Read at summary level.** [NOTE-tmpmg0fm](../notes.d/NOTE-tmpmg0fm.md) is `Skimmed`, and the conditions
below say what that costs this practice.

## The claim

Treat a pretraining objective as an association between the input `X` and a
**context variable** `A`. Masking gives one context, augmentation another, a
label another; on this account the methods differ in the context and are
otherwise the same mechanism.

Then the useful contexts are the ones in the middle:

- **Association too strong** — the context nearly determines the input, so
  there is little to learn from the association.
- **Association too weak** — there is nearly no signal.
- **In between** — stated spectrally, the singular values of the expectation
  operator decay neither too fast nor too slowly.

**And the construction**: contexts that individually sit at either extreme
can be *mixed*, which the source describes as an effortless way to build
better contexts from ones you already have.

## Why the record wants this even in its weak state

Every objective practice the registry holds is filed on its own evidence —
masked diffusion, fill-in-the-middle, multi-token prediction, the
augmentation families — and nothing says what they have in common or what
would make a *new* one good. This is the first thing in the record proposing
a criterion rather than a case.

It also arrives at the scaling-ceiling question from a direction the record
has not had. [SOTA-256](SOTA-256.md) judges a recipe by its asymptote; [LIT-441](../literature.d/LIT-441.md) moves
that asymptote with regularisation and ensembling. This says the asymptote
belongs to the *context* and that model scale cannot move it — a stronger and
more falsifiable claim, and nobody has put the two side by side.

## Conditions, and why this is `Proposed` with `consensus: unassessed`

**The reading is a skim.** A 313,000-character dissertation, read at abstract,
introduction, implications and conclusions. The theorems, the statistical
learning bounds and the semi-supervised extension were not worked through.
The criterion and the mixing construction are taken from the source's own
summary of its results, not checked against proof. [ADR-025](../decisions.d/ADR-025.md) says a
`Skimmed` note is not enough to source a practice from, and this practice
exists at `Proposed` partly to record that debt rather than discharge it.

**The criterion names a quantity nobody can currently measure.** Estimating
the singular-value decay of a real pretraining context — next-token
prediction on web text, say — is not addressed in what was read, and without
it "neither too strong nor too weak" is a direction rather than a test.

**The mixing construction is the most actionable claim and has the least read
evidence behind it.** It is asserted in the summary sections; no measurement
of a mixed context outperforming its components was reached.

**And the obvious case is missing.** What *is* the context of next-token
prediction in this framework, and where does it sit on the axis? That is the
question the record most needs answered and the skim did not reach it.

## Known implementations

- None. The source introduces two objectives, SVME and KISE; no training run
  in this record chose its objective by this criterion.
