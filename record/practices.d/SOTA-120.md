---
number: 120
status: Active
consensus: converged
consensus_note: >-
  AdamW is the default optimizer, so decoupled decay is what nearly everyone
  runs — deliberately or not. The gap between that and this practice's
  `Deferred` status is the point of having two axes.
title: 'Prefer AdamW''s decoupled weight decay to L2 regularization added to the loss'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Deferred -> Active. The promote_when condition asked for a survey or
    a frontier training report that states which of the two it uses;
    LIT-156 is that survey and benchmarks ten optimizers against a well-
    tuned AdamW, and LIT-122 adds decoupled decay to Muon as a stated
    design decision. LIT-132, LIT-139 and LIT-159 name AdamW as the
    incumbent. The deferral's doubt -- that everyone still runs vanilla
    Adam -- is refuted by documents the record acquired after it was
    written. The recommendation is unchanged.
tags:
- training-optimization
date: '2026-08-24'
source:
- LIT-012
summary: >-
  Loshchilov et al. (2017), [LIT-012](../literature.d/LIT-012.md) — [ARXIV-1711.05101](https://arxiv.org/abs/1711.05101).
---

# SOTA-120: Prefer AdamW's decoupled weight decay to L2 regularization added to the loss

## Source

Loshchilov et al. (2017), [LIT-012](../literature.d/LIT-012.md) — [ARXIV-1711.05101](https://arxiv.org/abs/1711.05101).

## How this stopped being deferred

This practice was `Deferred` for sixteen days on a doubt carried over
verbatim from the old `sota_maybe` field:

> I feel like everyone still uses vanilla Adam though...
>
> llama2 used - β₁=0.9, β₂=0.95

The result was never in question — only whether anybody acts on it. The
`promote_when:` condition asked for **a survey or a frontier training report
that states which of the two it uses**, rather than leaving the choice
implicit in a config. The record has since acquired both, and neither had to
be gone looking for:

- **[LIT-156](../literature.d/LIT-156.md)** is the survey exactly: ten optimizers across four scales,
  each tuned rather than handed the baseline's hyperparameters, measured at
  the end of training. The baseline everything is judged against is **a
  well-tuned AdamW** — not Adam.
- **[LIT-122](../literature.d/LIT-122.md)** is the stronger evidence, because there decoupling is a
  *stated design decision* rather than a default. Muon had results at small
  scale and none above it; the two changes that carried it to a 3B/16B model
  on 5.7T tokens were applying weight decay and matching AdamW's update RMS.
  Someone had to decide to decouple, and wrote it down.
- **[LIT-132](../literature.d/LIT-132.md)**, **[LIT-139](../literature.d/LIT-139.md)** and **[LIT-159](../literature.d/LIT-159.md)** all name AdamW as the incumbent
  whose hyperparameters a challenger must transfer — [LIT-139](../literature.d/LIT-139.md) keeps AdamW
  for the embeddings while moving the matrices elsewhere, which is a choice
  only statable if the optimizer is named.

So the doubt is answered against itself: the frontier reports say AdamW, and
the survey benchmarks against AdamW. This is the case the pending-decisions
report describes as "a decision the codebase has already made and hasn't
written down".

The `consensus: converged` axis was already recording this. The gap between
that and a `Deferred` status was the point of having two axes — and it is now
closed from the status side, which is where it should have been all along.
