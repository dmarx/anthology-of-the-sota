---
status: Active
consensus: emerging
consensus_note: >-
  The specific pipeline is one group's, and the record has one controlled
  comparison behind it — 142M curated against 142M sampled from the same
  source. The general move is spreading: DINOv2 names text-curation
  pipelines as its inspiration, `SOTA-337`'s cluster covers the
  data-filtering side, and `#290`'s reading of `open_clip` found the
  descendant rosters (DFN, MetaCLIP, DataComp) to be curation results rather
  than architecture results. `emerging` because the direction is clear and
  the method is not standardised. Read as of 2026-09.
title: 'Curate a pretraining set by retrieving neighbours of curated seeds, rather than scaling the uncurated pool'
version: 1
tags:
- data-pipeline
- representation-and-encoding
date: '2026-09-23'
source:
- LIT-tmpfwfu3
introduced_by:
- LIT-tmpfwfu3
implementations: []
---

# SOTA-tmpj9zpp: Curate a pretraining set by retrieving neighbours of curated seeds, rather than scaling the uncurated pool

## Source

Oquab et al. (2023), [LIT-tmpfwfu3](../literature.d/LIT-tmpfwfu3.md) — [ARXIV-2304.07193](https://arxiv.org/abs/2304.07193), §3.

## The claim

Self-supervised pretraining is usually scaled by pointing it at more
uncurated data. Do the opposite: **use the curated datasets you already have
as queries, and retrieve their nearest neighbours out of the uncurated pool.**

The pipeline, as run:

1. embed the uncurated pool and several curated datasets;
2. for each curated query image, retrieve its nearest neighbours —
   **typically 4**, because larger `N` "leads to more collisions";
3. deduplicate;
4. train on the result.

It is an index job, not a training job: Faiss, 20 nodes of 8×V100-32GB, under
two days to produce a 142M-image set.

## The comparison that makes it a practice rather than a preference

Against **142M images randomly sampled from the same source**, the curated
set wins. That controls for volume, for the source distribution and for the
crawl — the three confounds that make most data claims unfalsifiable — and
leaves selection as the only difference.

Against ImageNet-22k, the curated set **matches on ImageNet-1k while
significantly outperforming it on the other benchmarks**. That is the shape
worth noticing: curation aimed at generality does not buy in-distribution
accuracy, it buys the tail. A pipeline evaluated only on its seed
distribution would have reported no gain.

## Why retrieval rather than filtering

A filter needs a quality predicate — a classifier, a heuristic, a threshold —
and every such predicate is a hypothesis about what good data looks like.
Retrieval-from-seeds needs no predicate: it inherits the judgement already
embedded in the curated datasets somebody built. The paper names its
inspiration as text-curation pipelines where a model trained on Wikipedia
scores crawled documents, which is the same trick.

## Conditions

- **It inherits the seeds' biases, all of them.** Whatever the curated
  datasets over- or under-represent, the retrieved set will amplify, because
  proximity to a seed is the only criterion. This is the cost of having no
  predicate, and it is not a small one.
- **`N` is a real hyperparameter with a stated failure.** More neighbours
  gives more collisions — images retrieved for several queries — which
  degrades diversity while appearing to add volume.
- **Retrieval quality is a function of the embedding you retrieve with**,
  which was itself trained on something. The pipeline is not
  assumption-free, it moves the assumption into the index.
- **One group, one pipeline, one domain.** The controlled comparison is
  clean and singular; nothing here has been replicated independently.
- **The distillation result is separable and is not this practice.** DINOv2
  trains a 1B-parameter ViT-g and distills it into the smaller models, which
  beat the same architectures trained from scratch on all 12 benchmarks.
  Useful, and a different claim.

## Known implementations

-
