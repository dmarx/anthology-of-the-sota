---
number: 85
status: 'Active'
title: 'Use flash attention for all attention computations when hardware supports it'
version: 4
history:
- version: 2
  date: '2026-09-18'
  note: >-
    The edge to SOTA-083 moves from `compared_against` to `extends`. Flash attention is a custom kernel for a critical op — an instance of that rule rather than a comparison anyone ran (ADR-011, ADR-047). The tag crossing this edge makes visible is untouched and still wants an answer.
- version: 3
  date: '2026-09-18'
  note: >-
    Adds `systems-optimization`. This document's body is about kernels, on-chip memory per SM and tile sizes, which is that blurb almost word for word — and flash attention being an instance of SOTA-083's custom-kernel rule is what the `extends` edge asserts. The frontmatter comment below asked that this crossing keep showing up until someone answered it; ADR-049 is the answer, and an unbound relation is never the resting state.
- version: 4
  date: '2026-09-24'
  note: >-
    Splits the memory claim from the speed claim, which this document had been
    carrying as one. Rabe and Staats (LIT-tmp2jjuh), six months before
    FlashAttention, get the same exactness and a 59x memory reduction at
    length 16,384 from the same algorithm — and measure it on TPU as "within a
    few percent of the runtime of the standard implementation", because
    standard self-attention already balances FLOPs against memory bandwidth
    there. So the memory saving is algorithmic and the speedup is a property
    of a memory hierarchy where HBM traffic is the bottleneck. The
    recommendation and status are unchanged; the condition in the title now
    covers hardware CLASS as well as kernel availability. `introduced_by`
    deliberately unchanged — see the Source section.
tags:
# `flash-attention` removed. #101 added it to both this practice and its
# counterpart to bind them under an invariant that then read `tags`, which
# luria.yaml records as satisfying the check rather than answering it. With
# the invariant back on `tags` (ADR-035) it would do that again, so it
# goes: the edge is real, it crosses a fault line in the vocabulary, and it
# should keep showing up until someone answers it.
- attention-techniques
- systems-optimization
date: '2026-08-24'
source:
- LIT-074
introduced_by:
- LIT-074
summary: >-
  Dao et al. (2022), [LIT-074](../literature.d/LIT-074.md) — [ARXIV-2205.14135](https://arxiv.org/abs/2205.14135).
extended_by:
- SOTA-161
- SOTA-106
extends:
- SOTA-083
---

# SOTA-085: Use flash attention for all attention computations when hardware supports it

## Source

Dao et al. (2022), [LIT-074](../literature.d/LIT-074.md) — [ARXIV-2205.14135](https://arxiv.org/abs/2205.14135).

**`introduced_by` stays with `LIT-074`, and the reason is worth stating**
because a predecessor now sits in the record. `#342` flagged this as a likely
repeat of `SOTA-192`'s origin defect and asked for it to be verified first; it
is not one. That practice's title was a generic technique credited to a paper
that adopted it. This one names an **artifact** — *flash attention* is Dao et
al.'s system, and the recommendation to run that kernel was first made by
them. The antecedent is `LIT-tmp2jjuh`, which carries the memory-complexity
result and the condition below, and which is a source rather than an origin.

## What "when hardware supports it" is carrying

The recommendation is easy because the result is exact. FlashAttention
computes the same attention as the unfused implementation — not an
approximation, not a sparsity pattern — so adopting it changes throughput and
memory and nothing else about the model. That is unusual among the
efficiency practices in this record and is why the title can be so
unconditional.

The condition in the title is doing real work, though. The kernel depends on
enough on-chip memory per SM to hold a tile ([SOTA-086](SOTA-086.md)), and on the head
dimension and dtype being ones a compiled path exists for. Off that path the
fallback is the unfused implementation, silently.

## The memory saving and the speedup are different claims

Everything above is about whether the kernel **runs**. There is a second
condition, about whether the benefit **transfers**, and it is measured in the
work this line descends from.

Rabe and Staats (`LIT-tmp2jjuh`) published the same algorithmic idea — exact
attention without materialising the `N × N` matrix — six months earlier, with
a JAX implementation on TPU. They get the memory result: **59× less overhead
at sequence length 16,384**, 32× during differentiation. They do not get the
speedup:

> is **within a few percent of the runtime of the standard implementation** of
> attention

and they say why: *"standard self-attention already balances the available
FLOPs and memory bandwidth of TPUs."*

So the two halves separate, and on **hardware class** rather than on kernel
availability:

| | what it depends on | where it holds |
| --- | --- | --- |
| less memory | the algorithm | anywhere it runs |
| more speed | HBM traffic being the bottleneck | measured on GPUs; near zero on TPU |

`LIT-074`'s 3× on GPT-2 is a GPU number, and Theorem 2's HBM-access bound is
explicitly a claim about a memory hierarchy rather than about attention. Both
still hold. What does not follow, and what this practice implied by carrying
the two together, is that the speedup travels with the algorithm.

For a reader on GPUs nothing changes. For a reader choosing an accelerator, or
reading `SOTA-086`'s tile-size rule as general advice, it changes what to
expect.

## Where the line goes from here

[SOTA-106](SOTA-106.md) supersedes the version of the kernel rather than the practice:
FlashAttention-2 rebalances the work partitioning for the same exact result.

The one thing adopting it changes numerically is the *order* of accumulation,
and that is not nothing at scale — [SOTA-161](SOTA-161.md) exists because the rounding bias
of the fused reduction compounds rather than cancelling over a long run, and
it is filed under stability rather than attention for exactly that reason.
