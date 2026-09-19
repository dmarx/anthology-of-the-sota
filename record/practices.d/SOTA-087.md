---
number: 87
status: 'Active'
title: 'Recompute attention during backward pass instead of storing it'
version: 4
history:
- version: 2
  date: '2026-09-13'
  note: >-
    Attribution split under ADR-029. The recommendation is Child et al.
    (2019); Dao et al. is the evidence and the argument this body makes, and
    stays the primary source. Nothing about the claim changed.
- version: 3
  date: '2026-09-18'
  note: >-
    Adds `systems-optimization`. Trading recomputation for stored activations is a memory-access decision, and it is what its line holds in common (ADR-049).
- version: 4
  date: '2026-09-19'
  note: >-
    Gains a second parent. SOTA-249 states the general activation
    memory/compute trade this is the attention case of, and the line v3
    tagged `systems-optimization` to bind now has its earliest member. The
    recommendation, the source and the ADR-029 attribution split are all
    unchanged — LIT-074 remains the evidence and LIT-225 the origin of this
    narrower rule.
tags:
- attention-techniques
- systems-optimization
date: '2026-08-24'
source:
- LIT-074
# Dao et al. is the evidence and the argument this practice makes; Child et
# al. is where the recommendation came from, three years earlier and for a
# different reason (ADR-029).
introduced_by:
- LIT-225
extends:
- SOTA-086
- SOTA-249
summary: >-
  Dao et al. (2022), [LIT-074](../literature.d/LIT-074.md) — [ARXIV-2205.14135](https://arxiv.org/abs/2205.14135).
---

<!-- inactive-ok-file: ADR-029 — Proposed. Every mention here names it as the decision that added `introduced_by:`, which is the field this document uses; the citation is to the reasoning, not a claim the decision is settled -->

# SOTA-087: Recompute attention during backward pass instead of storing it

## Source

Dao et al. (2022), [LIT-074](../literature.d/LIT-074.md) — [ARXIV-2205.14135](https://arxiv.org/abs/2205.14135).

## Why recomputation is cheaper here than storing

Standard attention materialises the N×N score matrix, writes it to HBM,
reads it back for the softmax, writes that, and reads it again for the
backward pass. The arithmetic is trivial next to the traffic, so attention is
memory-bound and the N² term is a *bandwidth* cost before it is a compute one.

FlashAttention keeps the block of scores in on-chip SRAM, consumes it
immediately, and never writes it out. The backward pass then recomputes each
block from Q, K and V — which is more FLOPs and less time, because the FLOPs
were never the bottleneck. Memory falls from quadratic to linear in sequence
length.

This is why the practice is not the usual activation-checkpointing trade. The
ordinary version buys memory with compute at a real cost in step time; here
the recomputation is close to free, because the thing it avoids is the
expensive one.

## Where the recommendation came from

Child et al. (2019) recommends it three years earlier, in [LIT-225](../literature.d/LIT-225.md) §5.4 —
*"we recompute the attention and feed-forward blocks during the backwards
pass"* — and for a different reason: ordinary activation checkpointing pays
compute for memory, and attention at long sequence length is where that trade
is best, because *"memory usage is high for these layers relative to the cost
of computing them"*. Recomputation alone is what let that paper train networks
of hundreds of layers at 16,384 context.

So the practice is older than its source, and what FlashAttention changed is
**the price**, not the instruction. That is the distinction [ADR-029](../decisions.d/ADR-029.md) adds
`introduced_by:` to hold: dropping Child et al. would not force a line of this
body to be rewritten, and would still leave the record dating a 2019
recommendation to 2022.

## Condition

It holds while the kernel is memory-bound, which is where attention lives at
the head dimensions transformers use. It also depends on the softmax being
computable blockwise — the online, running-maximum formulation — so a variant
that needs the whole row at once cannot be done this way.

The saved memory is what makes the long-context regime affordable at all;
[SOTA-086](SOTA-086.md) is the constraint on how the blocks are sized.
