---
number: 62
status: 'Superseded'
status_note: >-
  The decoupling experiment this practice's own body invited has been run:
  holding the token budget fixed, the dependence of batch size on model size
  very nearly vanishes. What the heuristic was tracking is the data that
  scaled alongside the model. `Superseded` rather than `Rejected` because
  following it along the Chinchilla line gives roughly the right answer for
  the wrong reason — the successor is [SOTA-tmp0cq3b](SOTA-tmp0cq3b.md).
title: 'Scale batch size with model size but sub-linearly'
version: 2
history:
# inactive-ok-block: ADR-035 — Proposed, and cited for exactly the rule it
# states: a tag must not be added in order to bind a relation. Naming it is
# how this retag declares it was not
- version: 2
  date: '2026-09-20'
  note: >-
    Superseded by SOTA-tmp0cq3b, and retagged. Zhang et al. (LIT-tmphgpkf)
    ran the decoupling experiment this practice's body invited — hold the
    token budget fixed and vary model size — and the dependence very nearly
    disappears; Bergsma et al. (LIT-tmp5olz5) agree from a scaling-law fit.
    The retag from `model-architecture` to `training-optimization` is correct
    on its own terms and would be right with or without the supersession:
    `batch size` is named in the training-optimization blurb and nothing in
    the model-architecture blurb covers it. It also happens to be what lets
    the correction edge be declared, and saying so is better than not
    (ADR-035).
tags:
- training-optimization
date: '2026-08-24'
source:
- LIT-061
introduced_by:
- LIT-061
compared_against:
- SOTA-061
superseded_by:
- SOTA-tmp0cq3b
summary: >-
  Fedus et al. (2021), [LIT-061](../literature.d/LIT-061.md) — [ARXIV-2112.10684](https://arxiv.org/abs/2112.10684).
corrected_by:
- SOTA-tmp0cq3b
---

# SOTA-062: Scale batch size with model size but sub-linearly

## Source

Fedus et al. (2021), [LIT-061](../literature.d/LIT-061.md) — [ARXIV-2112.10684](https://arxiv.org/abs/2112.10684).

## Sub-linearly, and why the exponent matters more than the direction

Larger models tolerate — and want — larger batches, because the gradient noise
that sets the useful batch size falls as the model gets better at the task.
That the growth is *sub-linear* is the content: doubling parameters does not
double the batch, so the ratio of batch to model size falls as scale rises,
and a rule that scales them together over-shoots at the top end.

The practical failure is quiet. An over-large batch does not diverge; it
spends compute on samples that buy less than they cost, and the run simply
reaches a given loss later than it should have — attributed, usually, to the
data or the schedule.

## What the record has that is better

This is a heuristic from one 2021 study's setup, and the quantity it gropes
toward — critical batch size — is measurable and has since been characterised
directly. The record's own material is stronger: [SOTA-092](SOTA-092.md) and [SOTA-093](SOTA-093.md) give
the mechanism, and the ramp implied by them is what large runs actually do.

Kept because it is true and because a rule of thumb is useful when nobody is
going to measure. But a reader with a measurement should prefer it, and the
practice should not be read as licensing a fixed batch-to-parameter ratio,
which is the reading its title most invites.
