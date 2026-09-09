---
number: 78
status: 'Active'
title: 'Buffer size should be 2-3x batch size'
version: 1
tags:
- data-pipeline
date: '2026-08-24'
published: '2020-01-01'
source:
- LIT-053
summary: >-
  Aizman et al. (2020), [LIT-053](../literature.d/LIT-053.md) — [ARXIV-2001.01858](https://arxiv.org/abs/2001.01858).
---

# SOTA-078: Buffer size should be 2-3x batch size

## Source

Aizman et al. (2020), [LIT-053](../literature.d/LIT-053.md) — [ARXIV-2001.01858](https://arxiv.org/abs/2001.01858).

## What the buffer is for

Reading tar shards sequentially ([SOTA-077](SOTA-077.md)) gives up random access, so the
shuffle has to be reconstructed. The sample buffer is half of that: fill it
from the stream, yield a random element, refill from the stream. The larger
it is, the further apart in the archive two samples in the same batch can be.

That is the quantity to reason about — how much of the archive the buffer
spans — and it is why a rule stated relative to *batch size* is the wrong
shape. What matters is the buffer against the shard's internal correlation:
an archive whose adjacent records are one video's frames or one document's
chunks needs a far larger buffer than one written in random order, at the
same batch size.

## The constant is not this paper's

"2-3x batch size" is not stated in [LIT-053](../literature.d/LIT-053.md), and the record cannot say who it
belongs to. It is also small for the purpose: implementations in this family
default to buffers of thousands of samples, which at ordinary batch sizes is
one to two orders of magnitude above what this practice says.

Flagged rather than retired, because the underlying recommendation — hold a
shuffle buffer, size it deliberately — is real. What it needs is restatement
against shard correlation rather than against batch size, and either a source
for a number or no number.
