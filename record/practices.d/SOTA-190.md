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
  direction and not of the protocol. LIT-681 is the other direction: an outside
  group tested deep-narrow at a one-GPU-day budget and found no gain. That is
  a different regime, and it bounds the claim rather than contesting it.
title: 'Increase depth before any other dimension when scaling a transformer'
version: 3
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Records an outside test. LIT-681 ran LIT-052's deep-narrow shape under a
    fixed 24-hour, one-GPU budget and found no gain: 81.39 MNLI-m against
    81.79 for its baseline, although the deep-narrow model ran faster. That
    regime is not the one this practice's promote_when asks about, so status
    and consensus are unchanged. The section added says where the claim
    stops.
- version: 3
  date: '2026-09-25'
  note: >-
    Records the depth sweep in Narang et al. (LIT-711): 6 to 24 layers at
    a fixed 223M in the T5 codebase. Final loss is non-monotone in depth, and
    step rate falls as depth rises. The paper's own sentence that deeper
    models "tend to outperform" reads the table more generously than the
    table does. Tay is an author of both papers, so this is not the outside
    group promote_when asks for. Status and consensus are unchanged.
tags:
- model-architecture
date: '2026-09-09'
source:
- LIT-052
introduced_by:
- LIT-052
implementations:
- t5
- vision_transformer
compared_against:
- SOTA-125
summary: >-
  Tay et al. (2021), [LIT-052](../literature.d/LIT-052.md) — the DeepNarrow strategy. Small 16L matches T5-Base downstream at 60% of the parameters, 63% of the FLOPs and 40% faster; the limit is parallelism rather than quality.
---

<!-- inactive-ok-file: SOTA-419 — Proposed, named as the practice for the
     small-budget regime this section bounds off; its status is not relied on -->

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

## An outside test at small budget, and what it does not reach

[LIT-681](../literature.d/LIT-681.md) (Cramming) is the first outside group in this record to
run deep-narrow directly. It is a BERT-style MLM given 24 hours on one GPU,
with every variant at the same wall-clock. Its Table 11:

| variant | MNLI-m | tokens/s |
| --- | --- | --- |
| baseline (12 layers, modified) | 81.79 | 46,431 |
| DeepNarrow, 24 layers | 81.39 | 52,558 |
| DeepNarrow, 12 layers | 80.97 | 99,717 |

"Rescaling architectures to be deep-narrow … provides no gains." The deep-narrow
model is *faster* per token and still does not win, because at a fixed time
budget per-token learning is set by parameter count and the extra tokens do
not make up the difference.

This does not contest the claim above. The claim is about *scaling* at matched
quality with fewer parameters and FLOPs, on T5 at up to XXL. Cramming holds
the budget fixed at a scale four orders of magnitude smaller and runs once
per variant. What it establishes is a boundary. At a small fixed budget,
preferring depth is not a lever, and [SOTA-419](SOTA-419.md) is the practice
that says what is.

## A same-lineage sweep at fixed parameters, and what it shows

Narang et al. ([LIT-711](../literature.d/LIT-711.md)) trade depth against feed-forward width and heads
at a fixed 223M in a T5 encoder-decoder, with hyperparameters fixed:

| layers | final loss | steps/s |
| --- | --- | --- |
| 6 | 1.857 | 3.70 |
| 8 | 1.847 | 3.69 |
| 12 (baseline) | 1.838 | 3.50 |
| 18 | **1.831** | 3.38 |
| 24 | 1.843 | 3.33 |

The paper's text says "deeper models tend to outperform shallower ones with a
fixed parameter count". Its table has a peak at 18 layers, and 24 layers is
worse than the 12-layer baseline. In its learned-position rerun, every depth
variant loses to the baseline on both early and final loss. The throughput
cost of depth does show up, and it rises steadily.

That is compatible with this practice without confirming it. The practice's
claim is about scaling at matched quality, not about reshaping at one fixed
size. And the sweep is not independent, because Tay is an author of both
papers and it ran in the same codebase. What it suggests, from one final-loss run per shape,
is that at 223M depth past about 18 layers stopped paying, before
parallelism was anywhere near binding.
