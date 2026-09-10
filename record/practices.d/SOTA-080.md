---
number: 80
status: 'Active'
title: 'Use multiple worker processes (num_workers = 4 * num_gpus)'
version: 1
tags:
- data-pipeline
date: '2026-08-24'
source:
- LIT-053
summary: >-
  Aizman et al. (2020), [LIT-053](../literature.d/LIT-053.md) — [ARXIV-2001.01858](https://arxiv.org/abs/2001.01858).
---

# SOTA-080: Use multiple worker processes (num_workers = 4 * num_gpus)

## Source

Aizman et al. (2020), [LIT-053](../literature.d/LIT-053.md) — [ARXIV-2001.01858](https://arxiv.org/abs/2001.01858).

## What the workers are for, and why a formula is the wrong shape

Decode and augmentation are CPU work, and a single process cannot keep a
modern accelerator fed. Multiple worker processes parallelise it, which is
the practice, and it is right.

The formula is not. What sets the number is the ratio of per-sample CPU work
to per-sample GPU work, and the CPU cores available — a JPEG-decoding vision
pipeline and a pre-tokenised text pipeline differ by orders of magnitude at
the same GPU count. "4 × num_gpus" encodes one workload's answer as though it
were arithmetic, and it will be wrong in both directions: too few for heavy
decode, and wasteful for a pipeline reading tensors that need no work at all.

## Where the number comes from, as far as the record can tell

Not [LIT-053](../literature.d/LIT-053.md), which is about the storage format and the access pattern rather
than loader concurrency. It reads as PyTorch `DataLoader` folklore, and
unlike [SOTA-013](SOTA-013.md)'s constants — which turned out to be NVIDIA's, documented, and
attributable — this one has no owner the record can find.

Contention makes over-provisioning actively harmful, not merely wasteful:
workers compete for the same cores as the main process, and each holds its
own prefetch buffers ([SOTA-079](SOTA-079.md)), so more workers can lower throughput while
raising memory.

Flagged for restatement: the practice is "parallelise the CPU stages and size
the pool by measurement ([SOTA-045](SOTA-045.md))", and the record should say that instead
of a constant it cannot source.
