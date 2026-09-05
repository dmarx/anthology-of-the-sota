---
status: Active
title: 'The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale'
version: 1
tags:
- data-pipeline
date: '2026-09-05'
published: '2024-06-01'
arxiv: '2406.17557'
first_author: 'Penedo'
keywords:
- 'pretraining-data'
- 'deduplication'
- 'filtering'
- 'common-crawl'
- 'ablation'
implementations:
- FineWeb
- FineWeb-Edu
summary: >-
  Penedo et al. (2024), [ARXIV-2406.17557](https://arxiv.org/abs/2406.17557). 15T tokens from 96 Common Crawl
  snapshots, with every design choice documented and ablated — and
  FineWeb-Edu, the 1.3T educational filter that moves MMLU and ARC sharply.
---

# LIT-tmpw2sm1: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale

Penedo et al., Hugging Face (2024) — [ARXIV-2406.17557](https://arxiv.org/abs/2406.17557)

## Key takeaways

- The gap it fills is documentary: the pretraining corpora behind the best
  open-weight models of the period are not public and almost nothing is known
  about how they were built, so nobody outside those labs could reason about
  the choices.
- FineWeb is 15T tokens from 96 Common Crawl snapshots, and outperforms other
  open pretraining datasets — but the contribution the paper leads with is
  that **every design choice is documented and ablated**, deduplication and
  filtering strategies in particular.
- **FineWeb-Edu** is 1.3T tokens filtered from it for educational content,
  and models pretrained on it do dramatically better on knowledge- and
  reasoning-heavy benchmarks — MMLU and ARC are named.
- The curation codebase and every ablation model are released, which is what
  makes the ablations usable rather than merely reported.

## Standing in the anthology

The dataset half of the record's data practices, and the thing several notes
have been referring to without a citation: [LIT-119](LIT-119.md)'s tiny models mix
FineWeb and FineWeb-EDU by name in their web allocation, and its 20%-web
ablation is a decision taken *inside* the trade-off this paper maps.

Filed as a note. The record has no practice recommending a corpus, and
should not: a dataset is not a technique, and the transferable content here
is the ablation methodology — that filtering and deduplication choices are
worth measuring individually rather than adopting as a bundle. Read against
[LIT-tmpqhulf](LIT-tmpqhulf.md), which argues this filtering is too aggressive for long token
horizons.
