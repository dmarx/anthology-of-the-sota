---
number: 183
status: Active
formerly:
- SOTA-tmpp9gpf
title: 'Generate the harmlessness preference labels with the model itself, against a written set of principles'
version: 1
tags:
- data-pipeline
consensus: emerging
date: '2026-09-08'
published: '2022-12-15'
source:
- LIT-082
summary: >-
  Bai et al. (2022), [LIT-082](../literature.d/LIT-082.md) — [ARXIV-2212.08073](https://arxiv.org/abs/2212.08073). Replace the human
  harmlessness comparisons with model-generated ones: the model critiques and
  revises its own responses against an explicit list of principles, and the
  preference model trains on that.
---

# SOTA-183: Generate the harmlessness preference labels with the model itself, against a written set of principles

## Source

Bai et al. (2022), [LIT-082](../literature.d/LIT-082.md) — [ARXIV-2212.08073](https://arxiv.org/abs/2212.08073).

## The method

Two stages. First supervised: sample responses to harmful prompts, have the
model critique each one against a principle drawn from a written list, revise
it, and fine-tune on the revisions. Then reinforcement: have the model choose
between response pairs using those same principles, train a preference model
on the resulting comparisons, and optimize against it. Human labels remain in
the loop for *helpfulness*; the harmlessness half is model-generated.

## Why this is a training-data practice, not an alignment philosophy

The
expensive, slow, unpleasant input to preference training is the human
harm-comparison label, and this replaces it with generated data at the cost
of writing down the criteria. The criteria being written down is the part
that transfers — the supervision is now an artifact you can read, version and
argue with, instead of a distribution implicit in a labeling contract.

## Why `emerging`

The general move — AI feedback in
place of human preference labels — is now widespread and appears in most
open post-training pipelines. The specific apparatus of a principle list
consulted per-critique is much less so; several groups get the same effect
from a reward model or a rubric without the constitution framing. What is
agreed is that the labels can be synthetic. What is not agreed is what the
model should be asked to consult.

## The condition worth carrying

This shifts the failure mode rather than
removing it. A gap or an ambiguity in the written principles propagates
silently into every generated comparison, where a human labeler would have
produced visible disagreement instead.

## Known implementations

- Claude, and the RLAIF stage in most open post-training recipes
