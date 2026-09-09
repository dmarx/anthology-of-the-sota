---
number: 77
status: 'Active'
title: 'Use tar archives for dataset storage'
version: 1
tags:
- data-pipeline
date: '2026-08-24'
published: '2020-01-01'
source:
- LIT-053
summary: >-
  Aizman et al. (2020), [LIT-053](../literature.d/LIT-053.md) — [ARXIV-2001.01858](https://arxiv.org/abs/2001.01858).
extended_by:
- SOTA-078
- SOTA-079
---

# SOTA-077: Use tar archives for dataset storage

## Source

Aizman et al. (2020), [LIT-053](../literature.d/LIT-053.md) — [ARXIV-2001.01858](https://arxiv.org/abs/2001.01858).

## The access pattern, not the file format

The argument in [LIT-053](../literature.d/LIT-053.md) is that distributed filesystems were built for
directory trees and random access to files, and a training job does neither:
it reads an enormous number of small objects in shuffled order. That is close
to the worst case for the metadata path, and no amount of tuning the
filesystem changes what the job is asking for.

Sharded tar archives change the request instead. The job streams large files
sequentially, which is what storage is good at, and the shuffle is recovered
in two places — across shards, and within a buffer of samples read from the
current shard. Tar specifically because it needs no special reader and no
index: a standards-based container the pipeline can consume anywhere.

## Conditions and cost

Random access to an individual sample is gone. That is fine for training,
which wants a stream in a different order each epoch, and it is a genuine
loss for anything that wants to fetch example 4,213 — evaluation on a fixed
subset, debugging a specific item, any curriculum that selects by index.

The shuffle is also only as good as the buffer ([SOTA-078](SOTA-078.md)) and the shard
count. Too few shards and the epoch order is nearly fixed; a buffer too small
and samples that were adjacent in the archive stay adjacent in the batch,
which correlates the gradient in a way that is hard to see and easy to
attribute to something else.
