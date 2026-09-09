---
number: 190
status: Proposed
formerly:
- SOTA-tmp7pn5v
promote_when: >-
  A depth-preferential shape comparison from another group at a scale where
  model parallelism binds, reporting wall-clock as well as quality. The
  source states its own limit as a hardware limit, so a result that does not
  report throughput under parallelism cannot settle it.
consensus: unreplicated
# inactive-ok-block: SOTA-125 — Proposed; cited as the corroborating measurement,
# and its status is why this one stays Proposed too
consensus_note: >-
  One group, on T5 configurations up to XXL, with a vision check in the same
  paper. SOTA-125 reaches the same conclusion at 90M from a different group
  and a different architecture family, which is corroboration of the
  direction and not of the protocol.
title: 'Increase depth before any other dimension when scaling a transformer'
version: 1
tags:
- model-architecture
date: '2026-09-09'
published: '2021-09-01'
source:
- LIT-052
implementations:
- t5
- vision_transformer
compared_against:
- SOTA-125
summary: >-
  Tay et al. (2021), [LIT-052](../literature.d/LIT-052.md) — the DeepNarrow strategy. Small 16L matches T5-Base downstream at 60% of the parameters, 63% of the FLOPs and 40% faster; the limit is parallelism rather than quality.
---

# SOTA-190: Increase depth before any other dimension when scaling a transformer

## Source

Tay et al. (2021), [LIT-052](../literature.d/LIT-052.md) — [ARXIV-2109.10686](https://arxiv.org/abs/2109.10686).

## The claim, and the numbers under it

Kaplan et al. ([LIT-028](../literature.d/LIT-028.md)) found that shape barely matters — depth, width and
head count have "minimal effects within a wide range" once parameter count is
fixed. That was measured on upstream pretraining loss. Measured instead on
downstream fine-tuning quality, shape matters, and depth is the axis that
matters most.

The recommendation the paper gives is to increase depth preferentially, before
any uniform scaling of the other dimensions. Its Table 4:

| model | params | FLOPs vs. baseline | quality |
|---|---|---|---|
| Small 16L vs. Base | 134M vs. 223M | 63.1% | comparable, 40% faster |
| Base 36L vs. Large | 16% saving | lower | outperforms |
| XL 32L vs. XXL | ~33% | ~44% | outperforms, ~3× faster |

## What it trades, which is the reason it is not universal

Depth is serial. Every layer waits for the one before it, so depth cannot be
split across devices the way width can, and the paper is explicit that its
protocol holds "within a certain hardware limit" — its own experiments cap at
64 workers with model parallelism of 32, and it puts extreme width-parallel
scaling out of scope.

That is the whole condition. A deep-narrow model is more efficient per FLOP and
harder to parallelise, so the strategy is right up to the point where the
parallelism you can actually buy becomes the binding constraint, and the paper
does not say where that point is. This is why the practice is *Proposed*: what
it needs is not another quality comparison but a throughput one, at a scale
where the trade bites.

## Where it sits against the rest of the record

<!-- inactive-ok-block: SOTA-125 — Proposed; this paragraph is about what it does and does not corroborate -->
[SOTA-125](SOTA-125.md) reaches the same conclusion from the other end — a 90M hybrid
Mamba/attention model where the 27-layer configuration beat the shallow one,
and the 50-layer one gained further on MMLU but cost 2× in throughput and was
not chosen. Different group, different architecture, different scale, same
finding *and the same trade*: depth wins on quality per parameter and loses on
throughput. Two independent arrivals at a shape rule, both of which stop at
the same wall.

They are declared as a comparison rather than a lineage because neither builds
on the other; they are separate measurements of one question.

## Known implementations

- T5 (the released DeepNarrow configurations: Small 16L, Small 20L, Small 24L, Base 36L, XL 32L)
- Vision Transformer (the paper's own cross-domain check)
