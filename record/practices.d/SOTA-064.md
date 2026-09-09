---
number: 64
status: Rejected
status_note: >-
  The cited paper does not contain the word "warmup". Its subject is model
  shape for downstream fine-tuning; this claim came from a takeaway that
  belonged to no identifiable source, and no paper in the record supports it
title: 'Warmup needed scales sub-linearly with model size'
version: 2
history:
- version: 2
  date: '2026-09-09'
  # inactive-ok-block: SOTA-065, SOTA-066, SOTA-067, SOTA-068 — retired in this
  # same change; the note exists to say they went together
  note: >-
    Rejected. Retired together with SOTA-065, SOTA-066, SOTA-067 and
    SOTA-068 — the five practices drawn from LIT-052's replaced takeaways.
tags:
- training-optimization
date: '2026-08-24'
published: '2021-09-01'
source:
- LIT-052
implementations:
- vision_transformer
- bert
summary: >-
  Tay et al. (2021), [LIT-052](../literature.d/LIT-052.md) — [ARXIV-2109.10686](https://arxiv.org/abs/2109.10686). Rejected: the source contains no discussion of warmup.
---

# SOTA-064: Warmup needed scales sub-linearly with model size

## Source

Tay et al. (2021), [LIT-052](../literature.d/LIT-052.md) — [ARXIV-2109.10686](https://arxiv.org/abs/2109.10686).

## Why this is rejected

The paper at that identifier is *Scale Efficiently: Insights from Pre-training
and Fine-tuning Transformers*. Its subject is model shape — depth against
width — and its finding is the DeepNarrow strategy. Searched in full, it
contains the string "warmup" **zero times**.

The claim came from [LIT-052](../literature.d/LIT-052.md)'s first key takeaway, "as model size increases,
required warmup period becomes shorter relative to total training time",
which was replaced at that note's version 2 along with five others. Whatever
those bullets were drawn from, it was not this paper.

## What is left of the claim

Something in this neighbourhood may well be true, and the record should not
pretend otherwise: warmup length is usually set as a fraction of the run or as
a fixed step count, and both conventions imply *something* about how it should
move with scale. But the anthology's rule is that a recommendation names the
paper that established it ([ADR-001](../decisions.d/ADR-001.md)), and no paper in the record establishes
this one. Restating it would need a source found first, not a source assumed.

<!-- inactive-ok-block: SOTA-065, SOTA-066, SOTA-067, SOTA-068 — Rejected or Superseded in the same change, and the point is that all five went together -->
Retired alongside [SOTA-065](SOTA-065.md), [SOTA-066](SOTA-066.md), [SOTA-067](SOTA-067.md) and [SOTA-068](SOTA-068.md). All five
came from the same six bullets, which is why this is one finding about a note
rather than five findings about practices.
