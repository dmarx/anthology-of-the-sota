---
status: Active
title: 'Ring Attention with Blockwise Transformers for Near-Infinite Context'
version: 1
tags:
- distributed-optimization
date: '2026-09-07'
published: '2023-10-01'
arxiv: '2310.01889'
first_author: 'Liu'
keywords:
- 'context-parallelism'
- 'long-context'
- 'blockwise-attention'
- 'communication-overlap'
summary: >-
  Liu et al. (2023), [ARXIV-2310.01889](https://arxiv.org/abs/2310.01889). Compute attention and the feedforward
  blockwise, distribute the blocks across devices in a ring, and overlap the
  communication of key/value blocks with the computation of the next block.
  Sequence length scales with device count — no approximation, no extra
  communication or computation cost — which is what makes million-token
  contexts a sharding question rather than a memory ceiling.
---

# LIT-tmpu1846: Ring Attention with Blockwise Transformers for Near-Infinite Context

Liu et al., UC Berkeley (2023) — [ARXIV-2310.01889](https://arxiv.org/abs/2310.01889)

## Key takeaways

- **The constraint it removes.** A Transformer's memory demand, not its
  arithmetic, is what caps sequence length on a given device. Prior
  memory-efficient attention lowered the constant; it did not change what
  happens when one device is not enough.
- **The method.** Compute self-attention and the feedforward **blockwise**,
  distribute the blocks across devices arranged in a ring, and while a device
  computes attention on the block it holds, have it pass the key/value block
  to its neighbour. The communication of KV blocks is fully overlapped with
  the computation of blockwise attention.
- **The claim, and it is unusually clean.** Sequences up to **device count ×**
  longer than prior memory-efficient Transformers allow — "without resorting
  to approximations or incurring additional communication and computation
  overheads". No sparsity, no windowing, no loss of exactness: the same
  attention, held across more machines.
- Demonstrated on language modelling and reinforcement learning, at
  million-token context sizes.

## Standing in the anthology

The mechanism under a capability the record keeps citing and never explains,
and a multiply-cited absence from [#40](https://github.com/dmarx/anthology-of-the-sota/issues/40) — Falcon-H1 ([LIT-120](LIT-120.md)) and Kimi K3
([LIT-131](LIT-131.md)) both cite it.

The record now holds several answers to long context and they operate at
different layers, which is worth separating. [SOTA-139](../practices.d/SOTA-139.md) stages the *training
length*. [SOTA-151](../practices.d/SOTA-151.md) rescales positions so a finished model accepts a
longer one. [SOTA-132](../practices.d/SOTA-132.md) and the sparse-attention line reduce what attention
*costs* per token. This is none of those: the attention is unchanged and
exact, and what changes is that the sequence no longer has to fit on one
device. Kimi K3's "intra-device context parallelism for long-context prefill"
is this idea in its infrastructure section.

Filed as history and as vocabulary rather than as a practice: it is a
distribution strategy whose adoption is dictated by cluster shape, and the
record has no other context-parallelism material to place it against.
