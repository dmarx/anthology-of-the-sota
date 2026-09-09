---
number: 107
status: Rejected
status_note: >-
  The 128 is traced and belongs to a different quantity. Every occurrence
  in the source is a head dimension or a block size; none is a sequence
  length, and "multiple of" and "divisible" appear zero times
title: 'Keep sequence lengths multiple of 128 for best performance'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Rejected on reading the source (#114). The 128 was on the record's
    ownerless-constant list; it is now traced, and it names a head
    dimension and a block size rather than a sequence length. The body's
    kernel reasoning is sound and is not the paper's.
tags:
- attention-techniques
date: '2026-08-24'
published: '2023-07-01'
source:
- LIT-106
extends:
- SOTA-086
summary: >-
  Dao et al. (2023), [LIT-106](../literature.d/LIT-106.md) — [ARXIV-2307.08691](https://arxiv.org/abs/2307.08691).
compared_against:
- SOTA-108
- SOTA-089
---

# SOTA-107: Keep sequence lengths multiple of 128 for best performance

## Source

Dao et al. (2023), [LIT-106](../literature.d/LIT-106.md) — [ARXIV-2307.08691](https://arxiv.org/abs/2307.08691).

## Where the number comes from

The kernel processes the sequence in blocks, and the block sizes are powers
of two chosen against SRAM capacity ([SOTA-086](SOTA-086.md)) — typically 64 or 128 rows. A
sequence length that is not a multiple of the block size leaves a final
partial block that is masked and computed anyway, so the cost is the same as
a full one. At 2048 tokens with a 128-row block that is invisible; at 129
tokens it is nearly half the work wasted.

The tensor-core tiles underneath want the same alignment, which is why the
figure is usually stated as 128 rather than as "whatever the kernel's block
size is".

## Why this is rejected: the number is real and the axis is wrong

`128` occurs **fifteen times** in [LIT-106](../literature.d/LIT-106.md). Every occurrence is a **head
dimension** — the paper measures at `d` of 64 or 128 — or a **block size**,
from the set `{64,128} × {64,128}` it tunes over. Not one is a sequence
length. The strings `multiple of` and `divisible` appear **zero times**.

So the constant was not invented, which distinguishes this from
<!-- inactive-ok-block: SOTA-067 — Rejected, named as the contrasting failure -->
[SOTA-067](SOTA-067.md)'s `~5000`. It was transposed: a real number about the shape of a
tile, restated as a constraint on the length of a sequence.

The reasoning below is sound and it is not this paper's. A partial block does
cost a full block; that follows from how any tiled kernel works. But the
record's rule is that a practice states what its source establishes, and
inferring a recommendation the paper does not make — however good the
inference — is the failure this practice demonstrates. It is a different
failure from a takeaway describing some other paper, and worth keeping
visible for that reason.

## What this practice is worth

Little, at the lengths language models actually train on, and the record
should say so rather than imply a tuning opportunity that is not there.
Sequence lengths are already powers of two by convention.

It bites in two real places: variable-length batches, where sequences are
packed or padded per example rather than to a global length, and evaluation
or inference on short inputs. In the first, the practice is really an
argument for padding to a block multiple rather than to the longest sequence
<!-- inactive-ok-block: SOTA-108 — Rejected in the same change, and the pair is the point -->
in the batch — which is [SOTA-108](SOTA-108.md) stated from the other end.

`LIT-106` does not state this constant. It follows from the blocked design;
the specific 128 is a property of the implementations, in the same way the
constants in [SOTA-013](SOTA-013.md) were.
