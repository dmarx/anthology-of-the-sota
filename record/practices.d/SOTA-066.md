---
number: 66
status: Rejected
# inactive-ok-block: SOTA-064 — Rejected for the same reason and named as the pair
status_note: >-
  The same gap as SOTA-064, restated as a width claim. The cited paper
  contains no discussion of warmup at all
title: 'Can use shorter warmup periods for wider models'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Rejected with the rest of the LIT-052 cluster.
tags:
- training-optimization
date: '2026-08-24'
source:
- LIT-052
implementations:
- vision_transformer
- bert
summary: >-
  Tay et al. (2021), [LIT-052](../literature.d/LIT-052.md) — [ARXIV-2109.10686](https://arxiv.org/abs/2109.10686). Rejected: the source contains no discussion of warmup.
---

# SOTA-066: Can use shorter warmup periods for wider models

## Source

Tay et al. (2021), [LIT-052](../literature.d/LIT-052.md) — [ARXIV-2109.10686](https://arxiv.org/abs/2109.10686).

## Why this is rejected

<!-- inactive-ok: SOTA-064 — Rejected for exactly this reason, and named as the pair -->
The reason is written out under [SOTA-064](SOTA-064.md): the source discusses model shape,
not optimisation schedules, and the string "warmup" does not appear in it.

<!-- inactive-ok-block: SOTA-064 — Rejected alongside this one; the paragraph is about the pair -->
This one is worth keeping visible separately because of what it does to the
first. [SOTA-064](SOTA-064.md) says warmup scales sub-linearly with *size*; this says it
shortens with *width*. Read together they were the record's only statement
about how warmup moves with scale, and they were two halves of a bullet list
that came from nowhere. A reader who found one and not the other would have
had no reason to doubt it.
