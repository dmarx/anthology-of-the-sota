---
status: Active
title: 'Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer'
version: 1
tags:
- data-pipeline
date: '2026-09-18'
published: '2019-10-23'
arxiv: '1910.10683'
first_author: 'Raffel'
keywords:
- 'transfer-learning'
- 'text-to-text'
- 'pretraining-corpus'
- 'common-crawl'
implementations:
- 'T5'
- 'C4'
summary: >-
  Raffel et al. (2019), [ARXIV-1910.10683](https://arxiv.org/abs/1910.10683). T5's paper, and the origin of **C4** —
  the heuristically filtered Common Crawl slice that forty-six documents here
  train on. Filed for the corpus: the record cites C4 constantly and had no
  document behind it.
---

# LIT-tmplbblp: Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer

Raffel et al. (2019) — [ARXIV-1910.10683](https://arxiv.org/abs/1910.10683)

## Key takeaways

- **C4, the Colossal Clean Crawled Corpus**, is introduced here: a single
  Common Crawl snapshot put through heuristic cleaning — English-only
  detection, discarding lines that do not end in terminal punctuation,
  dropping boilerplate and placeholder text, a badwords filter, and
  deduplication of repeated spans. Roughly 750GB of English text
- **The cleaning is heuristic and English-only**, which is the property to
  carry. C4 is not "the web"; it is one crawl under one filter design, and
  what those filters keep or drop is a set of choices nobody has to agree with
- The paper's own subject is the text-to-text framework and a systematic
  ablation of transfer-learning choices. The corpus was infrastructure built
  to run that study, and it is the part this record depends on

## Standing in the anthology

**Carries no practice, deliberately** — `ADR-032`.

Forty-six documents mention C4 — thirty-nine readings, four literature notes,
two practices and one explanation — and the paper that made it was not in the
record at all. It plays two distinct roles here, and they want different
caveats.

**As a corpus with a known defect, it is load-bearing.** `SOTA-164` says to
deduplicate the pretraining corpus at both substring and document
granularity, and its headline evidence is a fact *about C4*: `LIT-202` found
one 61-word English sentence repeated thousands of times in it. That practice
is not really a claim about corpora in general — it is a claim grounded in
what survived this paper's filters, which already included a deduplication
step. The interesting reading is that C4 was deduplicated by its authors and
the repeats were still there, which is what makes the two-granularity
argument necessary rather than obvious.

<!-- inactive-ok-block: SOTA-155 — Proposed, and that is consistent with
     what this paragraph says about it: its evidence is eight workers on one
     corpus, which is why it has not been promoted. Nothing here rests on it -->
<!-- inactive-ok-block: THEORY-014 — Proposed, and named only as one of the
     documents whose comparison table uses C4 as the workload -->

**As a standard workload, it is a convention.** `SOTA-155`'s 500×
communication reduction, `LIT-212`, `LIT-252`, `LIT-276` and `THEORY-014`'s
comparison table all use C4 as the language-modelling task that distributed
and communication-efficient methods are measured on. Nothing about those
results depends on C4 specifically; it is there because everyone else used it,
which `DP-007` is the name for. `SOTA-155` already marks the narrow
part — "eight workers on C4 is a long way from the arrangement the motivation
describes".

The same shape as `LIT-424`: a dataset introduced inside a paper about
something else, which outlived the argument it was built to serve.

Unread — no `NOTE`.
