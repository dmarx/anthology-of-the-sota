---
number: 36
status: 'Active'
title: 'Train a decoder-only transformer on a broad web corpus with a fixed context and a single next-token objective'
version: 2
history:
- version: 1
  note: >-
    Titled "gpt training recipe", which names a thing rather than recommending
    anything. It could not be cited, contested or checked, and it was one of
    the two clearest cases of that shape on the #107 worklist.
- version: 2
  note: >-
    Retitled to state the recipe it stands for. The subject is unchanged: the
    source is LIT-035, and the practice has always been GPT-3's pretraining
    setup read as a recommendation.
tags:
- model-architecture
date: '2026-08-24'
published: '2020-05-01'
source:
- LIT-035
summary: >-
  Brown et al. (2020), [LIT-035](../literature.d/LIT-035.md) — [ARXIV-2005.14165](https://arxiv.org/abs/2005.14165).
extended_by:
- SOTA-037
- SOTA-038
---

# SOTA-036: Train a decoder-only transformer on a broad web corpus with a fixed context and a single next-token objective

## Source

Brown et al. (2020), [LIT-035](../literature.d/LIT-035.md) — [ARXIV-2005.14165](https://arxiv.org/abs/2005.14165).

## What the recipe actually is

Stripped to what a reader can act on, [LIT-035](../literature.d/LIT-035.md)'s pretraining setup is four
choices, and their durability is the reason this is a practice at all:

- **Decoder-only**, not encoder-decoder and not a masked objective. One stack,
  causal attention, no task-specific heads.
- **A single next-token objective** on everything, with no auxiliary losses and
  no supervised task mixture during pretraining.
- **A broad, filtered web corpus** rather than a curated task collection —
  quality filtering and deduplication over scraped text, weighted toward
  higher-quality sources.
- **A fixed context window**, with documents packed and split to fill it.

Everything downstream in this record modifies one of those four rather than
<!-- inactive-ok-block: SOTA-152, SOTA-157, SOTA-166, SOTA-172, SOTA-173 — Proposed, cited as the variations on this frame; that they are open is the paragraph's claim -->
replacing the frame: the objective ([SOTA-157](SOTA-157.md)'s diffusion alternative), the
packing ([SOTA-152](SOTA-152.md)), the data proportions ([SOTA-166](SOTA-166.md)), the context (staged
extension), the corpus ([SOTA-172](SOTA-172.md), [SOTA-173](SOTA-173.md)).

## Why the title was the problem

"gpt training recipe" names an artefact and recommends nothing, so nothing
could cite it, contest it, or check it — the same defect as [SOTA-001](SOTA-001.md)'s old
title, and both were promoted one-to-one from a note's bullet.

Retitled at version 2. What the practice claims is unchanged; it can now be
disagreed with, which is the point.

## What has moved since

The frame holds and the recipe's specifics have not. Pretraining is now
followed by an alignment stage [LIT-035](../literature.d/LIT-035.md) has no equivalent of, context windows
are extended in stages rather than fixed, and the corpus is increasingly
synthetic or heavily rewritten rather than filtered-scraped.

Read as *"this is the frame everything else varies within"*, the practice is
Active and well-supported. Read as a recipe to follow in 2026, it is a
historical baseline, and the record should not let the second reading pass for
the first.
