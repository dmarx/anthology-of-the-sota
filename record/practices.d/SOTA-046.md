---
number: 46
status: Rejected
status_note: >-
  the '> 1MB' crossover has no owner: NCCL measures the algorithm choice
  per topology rather than publishing a constant, and LIT-051 does not
  discuss it. What survives is that a modern collectives library already
  chooses by size and topology, which is not a practice a reader acts on
title: 'Use hierarchical allreduce for tensors > 1MB'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
published: '2020-11-01'
source:
- LIT-051
summary: >-
  Jiang et al. (2020), [LIT-051](../literature.d/LIT-051.md) — https://www.usenix.org/conference/osdi20/presentation/jiang.
---

# SOTA-046: Use hierarchical allreduce for tensors > 1MB

## Source

Jiang et al. (2020), [LIT-051](../literature.d/LIT-051.md) — https://www.usenix.org/conference/osdi20/presentation/jiang.

## The threshold is not this paper's, and probably not anyone's

Hierarchical all-reduce — reduce within a node over NVLink, exchange between
nodes, broadcast back down — is a real and standard technique, and it is
NCCL's and Horovod's rather than [LIT-051](../literature.d/LIT-051.md)'s. BytePS's argument is that
all-reduce and parameter-server are two special cases of one optimal
framework, and its mechanism is the Summation Service split described under
[SOTA-047](SOTA-047.md); a size threshold for choosing an all-reduce algorithm is not in it.

The "> 1MB" is the part with no owner at all. Ring all-reduce is
bandwidth-optimal and latency-poor, so small tensors do better on a tree or a
direct exchange and large ones on a ring — but where the crossover sits
depends on the fabric, the node count and the message size, which is why NCCL
*measures* it per topology rather than publishing a constant.

## What this practice needs

Re-sourcing, and probably restating without the number: the durable claim is
that the all-reduce algorithm should be chosen by tensor size and topology,
and that a modern collectives library already does this. A record quoting 1MB
is asserting a crossover nobody has shown holds anywhere in particular.

This is the same shape as the finding in [SOTA-013](SOTA-013.md) — a plausible constant
credited to a paper that does not contain it — and the same shape as the rest
of this cluster.
