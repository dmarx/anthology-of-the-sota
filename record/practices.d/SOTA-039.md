---
number: 39
status: Superseded
superseded_by: SOTA-140
status_note: warmup-stable-decay matches it and leaves the token budget open; every report since 2024 in the record uses a stable-then-decay schedule
title: 'single cycle of cosine decay is sufficient lr schedule'
version: 1
tags:
- model-architecture
date: '2026-08-24'
source:
- LIT-035
introduced_by:
- LIT-035
summary: >-
  Brown et al. (2020), [LIT-035](../literature.d/LIT-035.md) — [ARXIV-2005.14165](https://arxiv.org/abs/2005.14165).
---

# SOTA-039: single cycle of cosine decay is sufficient lr schedule

## Source

Brown et al. (2020), [LIT-035](../literature.d/LIT-035.md) — [ARXIV-2005.14165](https://arxiv.org/abs/2005.14165).

## Why this is superseded

<!-- inactive-ok: LIT-042 — the retired warm-restarts paper this practice itself retired -->
A single cosine cycle retired warm restarts ([LIT-042](../literature.d/LIT-042.md)) by showing they were not
needed at scale, and was the default from GPT-3 through 2023. It ties the
result to a token budget fixed in advance, so every duration is its own run
and no intermediate checkpoint is a finished model. Warmup-stable-decay
([SOTA-140](SOTA-140.md)) matches or beats it while removing that constraint, and by 2025
every frontier report in the record uses a stable-then-decay shape. The
claim here was right that one cycle beats several; what moved is the shape
of the one cycle.

What [LIT-035](../literature.d/LIT-035.md) reports is the recipe, not a comparison. All eight GPT-3 models,
125M to 175B, were trained with a linear warmup over the first 375 million
tokens and a single cosine decay to 10% of the peak rate over 260 billion
tokens, held at 10% for the rest of the 300 billion. No other schedule is run
against it, so the paper's evidence for "sufficient" is that the one cycle
trained every size; that it showed warm restarts unnecessary is the record's
reading, not a result in the paper.
