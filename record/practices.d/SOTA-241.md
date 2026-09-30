---
number: 241
status: Proposed
formerly:
- SOTA-tmp2nprq
promote_when: >-
  A model-free selection proxy used as a screen and then validated by
  training, at a scale where the record's data practices operate — a
  candidate set ranked before training and the ranking shown to hold after
  it, at billions of parameters and hundreds of billions of tokens — or a
  training report that says it screened candidate corpora or mixtures before
  committing a run. What would not move it: a further correlational study at
  the paper's own scale, which would restate the finding rather than extend
  its range; or a proxy that requires training a model, which is the cost
  this is trying not to pay.
title: 'Rank candidate data selections with a model-free distributional proxy before spending a training run'
version: 1
consensus: unassessed
consensus_note: >-
  The paper reports the correlation and nothing in this record follows up.
  No frontier report says whether it screens candidate selections before
  training or trains on all of them, so there is no adoption to read either
  way — an absence of evidence about the field rather than evidence of
  disagreement.
tags:
- data-pipeline
- analysis-and-evaluation
date: '2026-09-17'
source:
- LIT-087
introduced_by:
- LIT-087
implementations:
- 'DSIR'
summary: >-
  Xie et al. (2023), [LIT-087](../literature.d/LIT-087.md) — KL reduction in a hashed n-gram space
  correlates with downstream performance across selection methods, including
  manual curation, which uses no n-grams at all. A selection can therefore be
  ranked against its alternatives before anything is trained on it.
---

# SOTA-241: Rank candidate data selections with a model-free distributional proxy before spending a training run

## Source

Xie et al. (2023), [LIT-087](../literature.d/LIT-087.md) — [ARXIV-2302.03169](https://arxiv.org/abs/2302.03169).

## The result this rests on is not the method

The paper's headline is a selection method. The finding that matters here is
the one it needed in order to argue for itself: **KL reduction** — how much a
selection reduces distance to the target relative to random selection,
measured in a hashed n-gram space — **correlates strongly with downstream
performance across selection methods, including methods that use no n-grams
at all, such as manual curation.**

That last clause is the whole claim. A metric that only ranked *n-gram*
selections would be the method's own objective wearing a metric's clothes.
One that also ranks a hand-curated corpus is a proxy for data selection in
general, computable with a hash and a counter, before any model exists.

## Why a bad feature space is the right feature space

Ten thousand hash buckets of unigram and bigram counts cannot represent text
and are not claimed to. What is claimed is that the space preserves the
**ordering** of candidate selections, and ordering is all a screen needs.

The general form, which is the transferable part: **when a decision only
needs candidates ranked, the proxy has to be monotone with the outcome, not
faithful to the object.** Faithfulness is the expensive property and it is
routinely bought when it was not the one required.

## What it is for

<!-- inactive-ok-block: SOTA-166 — Proposed, and named here for its COST rather than
     relied on for its claim: the point is that fitting a mixing law spends runs, which
     is true whether or not the record ends up endorsing it. -->
Every other way the record has of choosing data costs training runs.
`SOTA-166` fits a mixing law on a sample of mixtures; `SOTA-238` runs a proxy
model to convergence to produce one weighting. Both are cheaper than
training at target scale and neither is free, and both of them have to pick
which candidates to spend their budget on.

A model-free proxy is the stage before that: it does not tell you the best
mixture, it tells you which candidates are not worth a run. Used that way the
correlational weakness below matters much less than it would if the proxy
were making the final call — a screen that is right about the ordering most
of the time still removes most of the cost.

## Conditions

**The evidence is a correlation across a handful of selection methods**, at
one scale, in 2023. It is the paper's own second result rather than the thing
it set out to show, and nothing in this record re-runs it.

**It inherits the target requirement.** The proxy measures distance to a
target distribution, so it presupposes the frame filed beside it — with no
sampleable target there is nothing to compute a KL reduction against.

**Below the scale its consumers operate at.** The record's data practices are
argued at 8B parameters and 15T tokens. Whether an n-gram distance still
orders selections correctly where selection is model-based and targets are
implicit is exactly the open question, and the one the condition above names.

## Why Proposed

`DP-006`: the evidence is weak-but-honest and the instruction is real, so the
document exists and the status carries the doubt. The cheapness is what makes
it worth filing at this strength — a screen that costs a hash and is wrong
sometimes is a different proposition from a recommendation that costs a
training run and is wrong sometimes.

## Known implementations

- **DSIR** — the paper's own release; KL reduction is reported there as the
  metric used to compare selections, including ones DSIR did not produce.
