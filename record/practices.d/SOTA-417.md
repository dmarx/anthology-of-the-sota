---
number: 417
status: Proposed
formerly:
- SOTA-tmphcbvi
consensus: unreplicated
consensus_note: >-
  One group, one budget, one pretraining run per cell. Heuristic filters that
  drop symbol-heavy or markup-heavy text are common in web-corpus pipelines,
  but this record holds no measurement of them other than this one. Read as
  of 2026-09.
promote_when: >-
  A second group applies a tokenizer-compression-ratio filter to a web corpus,
  compares it against the unfiltered corpus at matched tokens seen, and
  reports a downstream gain at a scale larger than one GPU-day. A result that
  names a threshold but reports no unfiltered control would not settle it.
  Neither would one that bundles this filter with a model-based quality
  classifier.
title: 'Filter pretraining text by how well the tokenizer compresses it'
version: 1
tags:
- data-pipeline
- training-optimization
date: '2026-09-25'
source:
- LIT-681
introduced_by:
- LIT-681
implementations:
- 'cramming (t = 0.25 on a WordPiece tokenizer trained on the same corpus)'
summary: >-
  Geiping and Goldstein (2023), [LIT-681](../literature.d/LIT-681.md). Drop every document whose
  token count exceeds `t` times its character count. Text a tokenizer trained
  on the corpus compresses badly is mostly markup, code fragments and debris.
  No model is needed. On C4 it lifts GLUE from **75.9 to 79.3**, and on
  already-clean bookcorpus-wikipedia from 78.1 to 78.7. The gain tracks how
  dirty the source was.
---

# SOTA-417: Filter pretraining text by how well the tokenizer compresses it

## Source

Geiping and Goldstein (ICML 2023), [LIT-681](../literature.d/LIT-681.md), §4.4 and Tables 2 and 7.

## What to do

Train the tokenizer on the corpus. For each document, compute
`tokens / characters`, and drop the documents above a threshold `t`. The
source uses `t = 0.25`, meaning at least four characters per token on
average. Do it at preprocessing time, before any training.

## Why it works, as far as the source says

A tokenizer fitted to a corpus encodes that corpus's typical text in few
tokens. What it encodes badly is text unlike the rest: "hard-to-compress
HTML", and similarly tables, code debris and non-language fragments. The
ratio is therefore a crude, model-free out-of-distribution score. The source
offers only the HTML example and does not analyse what it removes, so treat
this paragraph as the mechanism the result suggests, not one it measured.

## Evidence

GLUE after one GPU-day of MLM pretraining, one run per cell (the source's
Table 2):

| source | unfiltered | filtered |
| --- | --- | --- |
| C4 | 75.9 | **79.3** |
| Pile | 78.2 | 79.3 |
| Pile (natural sources) | 79.2 | 79.8 |
| bookcorpus-wikipedia | 78.1 | 78.7 |
| OSCAR | 79.1 | 79.2 |

The ordering is the useful part. The filter matters in proportion to how
much web debris the source has, and it is close to a no-op on curated text.
Exact-substring deduplication, run in the same study, did "not reliably
help".

## Conditions

**Small budget, encoder, English.** A day on one GPU, MLM, English text
lowercased and stripped of accents. At that budget a model sees each token
once, and a wasted token is expensive. With more compute than data the
trade-off changes. Discarding text also costs tokens, which is what
[SOTA-170](SOTA-170.md) is about. At long horizons, weigh the filter against
rephrasing what it would drop.

**The threshold is tokenizer-specific.** `t` is a ratio of tokens to
characters under *that* tokenizer. A larger vocabulary compresses everything
further and moves every document's ratio. Re-derive `t` from the ratio's
distribution on your corpus rather than copying 0.25.

**It is a floor, not a quality filter.** It removes text a tokenizer finds
unusual. That text is not necessarily bad, and code or non-English text
will be removed wholesale if the tokenizer was trained without it. If
either is wanted, fit the tokenizer on data that contains it, or apply the
filter per source.

## Known implementations

- **cramming**, the source's own pipeline.
