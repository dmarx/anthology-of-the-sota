---
number: 108
status: Rejected
status_note: >-
  Not in the cited paper. "padding", "padded", "pad", "block boundar" and
  "divisible" appear zero times each; the body's reasoning about skipping
  fully-masked blocks is correct and is not the source's
title: 'Pad attention masks to block boundaries for better hardware utilization'
version: 2
history:
- version: 2
  date: '2026-09-09'
  # inactive-ok-block: SOTA-107 — Rejected in this same change; the pair is
  # the point of the note
  note: >-
    Rejected on reading the source (#114), with SOTA-107. Neither the
    recommendation nor its vocabulary is in the paper.
tags:
- attention-techniques
date: '2026-08-24'
published: '2023-07-01'
source:
- LIT-106
compared_against:
- SOTA-107
summary: >-
  Dao et al. (2023), [LIT-106](../literature.d/LIT-106.md) — [ARXIV-2307.08691](https://arxiv.org/abs/2307.08691).
---

# SOTA-108: Pad attention masks to block boundaries for better hardware utilization

## Source

Dao et al. (2023), [LIT-106](../literature.d/LIT-106.md) — [ARXIV-2307.08691](https://arxiv.org/abs/2307.08691).

## The same block boundary, from the mask's side

<!-- inactive-ok-block: SOTA-107 — Rejected in the same change; this practice is its other half -->
[SOTA-107](SOTA-107.md) says the sequence should be a multiple of the block size; this says
what to do when it cannot be. A mask expressed at token granularity still has
to be applied blockwise, so a block that is partly masked is computed in full
and then discarded — the kernel's unit of work is the tile, not the token.

Rounding the mask out to block boundaries does not save that work. What it
does is let the kernel *skip* blocks that are entirely masked, which is where
the saving actually is: in causal attention roughly half the blocks are fully
above the diagonal, and a block-aligned mask lets them be dropped rather than
computed and zeroed.

## Why this is rejected

The paper does not say it. `padding`, `padded`, `pad`, `block boundar` and
`divisible` all appear **zero times** in [LIT-106](../literature.d/LIT-106.md).

What is written above is a correct account of how a blockwise kernel handles
a mask, and it is an inference rather than a citation. Retired with
<!-- inactive-ok-block: SOTA-107 — Rejected in the same change, and the pair is the point -->
[SOTA-107](SOTA-107.md), which fails the same way from the other end: two practices about
block alignment, both technically defensible, neither attributable.

The durable claim — express a structured mask so a kernel can skip fully
masked blocks — is real, and needs a source that makes it before the record
can recommend it.

## Condition, and the cost that is easy to miss

Rounding a mask outward makes it *less* restrictive at the edges. That is
fine for a causal mask, whose block-aligned form is still causal at block
granularity and is handled exactly by the kernel's own diagonal logic. It is
not fine for an arbitrary mask where the difference between token- and
block-alignment changes which positions attend to which — there the practice
would silently alter the model.

So this is a recommendation about how to *express* a structured mask so the
kernel can exploit it, not a licence to round any mask. Document-packing
masks, the common case where it matters, are structured in exactly the way
that makes it safe.

<!-- inactive-ok-block: SOTA-107 — Rejected alongside this one for the same reason -->
Like [SOTA-107](SOTA-107.md), this is a property of blocked implementations rather than
something `LIT-106` states — which both bodies said before either was read
against the paper, and which is now the reason both are retired.
