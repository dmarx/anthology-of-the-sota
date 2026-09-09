---
number: 107
status: 'Active'
title: 'Keep sequence lengths multiple of 128 for best performance'
version: 1
tags:
- attention-techniques
date: '2026-08-24'
published: '2023-07-01'
source:
- LIT-106
summary: >-
  Dao et al. (2023), [LIT-106](../literature.d/LIT-106.md) — [ARXIV-2307.08691](https://arxiv.org/abs/2307.08691).
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

## What this practice is worth

Little, at the lengths language models actually train on, and the record
should say so rather than imply a tuning opportunity that is not there.
Sequence lengths are already powers of two by convention.

It bites in two real places: variable-length batches, where sequences are
packed or padded per example rather than to a global length, and evaluation
or inference on short inputs. In the first, the practice is really an
argument for padding to a block multiple rather than to the longest sequence
in the batch — which is [SOTA-108](SOTA-108.md) stated from the other end.

`LIT-106` does not state this constant. It follows from the blocked design;
the specific 128 is a property of the implementations, in the same way the
constants in [SOTA-013](SOTA-013.md) were.
