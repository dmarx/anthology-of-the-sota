---
status: Active
formerly:
- SOTA-tmpq6ehk
consensus: emerging
consensus_note: >-
  Cited by two frontier reports in this record — Falcon-H1 and Kimi K3, whose
  "intra-device context parallelism for long-context prefill" is this idea in
  its infrastructure section. Not `converged`: the record has no other
  context-parallelism material to compare it against, and adoption is
  partly dictated by cluster shape rather than by the argument.
title: 'Shard the sequence across devices in a ring and overlap the key-value exchange with the attention it feeds'
version: 1
tags:
- distributed-optimization
date: '2026-09-08'
published: '2023-10-01'
source:
- LIT-206
implementations: []
summary: >-
  Liu et al. (2023), [LIT-206](../literature.d/LIT-206.md) — compute attention and the feedforward
  blockwise, distribute the blocks across devices in a ring, and pass each
  key/value block to the neighbour while computing on the one you hold. The
  communication is fully overlapped with the computation, so sequences scale
  with device count — exactly, with no approximation and no added overhead.
---

# SOTA-181: Shard the sequence across devices in a ring and overlap the key-value exchange with the attention it feeds

## Source

Liu et al. (2023), [LIT-206](../literature.d/LIT-206.md) — [ARXIV-2310.01889](https://arxiv.org/abs/2310.01889).

The constraint being removed is memory, not arithmetic: a transformer's
memory demand is what caps sequence length on a given device. Memory-efficient
attention lowered the constant. It did not change what happens when one
device is not enough.

Compute self-attention and the feedforward **blockwise**, distribute the
blocks across devices arranged in a **ring**, and while a device computes
attention on the block it holds, have it pass its key/value block to its
neighbour. The communication of KV blocks is fully overlapped with the
computation of blockwise attention.

**The claim is unusually clean.** Sequences up to *device count ×* longer
than prior memory-efficient transformers allow, "without resorting to
approximations or incurring additional communication and computation
overheads". No sparsity, no windowing, no loss of exactness — the same
attention, held across more machines. Demonstrated on language modelling and
reinforcement learning at million-token context.

## Which long-context problem this solves, which is not the others

The record holds four answers to long context and they operate at different
layers. Keeping them apart is most of the value of filing this one:

<!-- inactive-ok-block: SOTA-153 — Proposed, named as one of the four layers
     the long-context answers operate at -->
- [SOTA-139](SOTA-139.md) stages the *training length*.
- [SOTA-151](SOTA-151.md) rescales positions so a finished model accepts a longer one, and
  [SOTA-153](SOTA-153.md) removes the positional encoding from the layers that carry
  distance.
- [SOTA-132](SOTA-132.md) and the sparse-attention line reduce what attention *costs* per
  token.
- **This is none of those.** The attention is unchanged and exact; what
  changes is that the sequence no longer has to fit on one device.

A reader hitting a context limit should know which of the four they are
actually hitting, because three of them cost accuracy or a training run and
this one costs machines.

## Conditions

Adoption is partly dictated by cluster shape rather than by the argument —
the ring is only free if the interconnect makes it so, and the overlap claim
assumes communication fits inside the compute it hides behind. The record has
no other context-parallelism material to compare it against, which is why
this is `emerging` rather than settled.

## Known implementations

- Cited by Falcon-H1 and Kimi K3; K3's "intra-device context parallelism for
  long-context prefill" is this idea in its infrastructure section.
