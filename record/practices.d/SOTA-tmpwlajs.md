---
status: Proposed
promote_when: >-
  The trade run at language-model pretraining scale with throughput reported:
  a decoder-only model at a billion parameters or more, rebuilt with more
  heads and fewer layers at matched training compute, reporting loss,
  downstream metrics AND wall-clock or tokens per second. Throughput is not
  optional here — the competing practice's own source names parallelism as
  the binding constraint, so a parameter saving that costs latency settles
  nothing. What would NOT meet it: another vision architecture at 300 epochs
  on ImageNet, which is the evidence already held.
consensus: unreplicated
consensus_note: >-
  One group, twelve architectures inside the paper, and no adoption this
  record can find. The direction contradicts SOTA-190, which is itself
  `unreplicated` on a different axis, so the record now holds two
  single-group shape recommendations pointing opposite ways with no
  experiment between them.
title: 'Trade attention heads for depth: more heads conditions the attention block, and the layers you drop cost nothing'
version: 1
tags:
- model-architecture
- attention-techniques
date: '2026-09-22'
source:
- LIT-tmpqux2k
introduced_by:
- LIT-tmpqux2k
implementations: []
summary: >-
  Saratchandran, Teney and Lucey (2025), [LIT-tmpqux2k](../literature.d/LIT-tmpqux2k.md) — more
  heads lower the condition number of the attention block, which is part of
  what depth was buying. In the five configurations where the MLP width is
  held fixed, raising head count and cutting layers holds or improves accuracy
  at **29–53% fewer parameters** — TNT-B goes 65.4M → 30.9M at identical
  Top-1.
---
<!-- inactive-ok-file: SOTA-190 — Proposed, and the practice this one pulls
     against. The consensus_note and the Why-Proposed section both say the
     two point opposite ways with no experiment between them, which requires
     it to be unsettled. -->

# SOTA-tmpwlajs: Trade attention heads for depth: more heads conditions the attention block, and the layers you drop cost nothing

## Source

Saratchandran, Teney and Lucey (2025), [LIT-tmpqux2k](../literature.d/LIT-tmpqux2k.md) — read as
[NOTE-tmph5061](../notes.d/NOTE-tmph5061.md).

## Do this

When choosing a transformer's shape, **raise the head count and lower the
depth** rather than accepting the published configuration. Keep `d_model`
fixed, so head dimension falls as head count rises, and keep the MLP width
fixed so you know what you are trading.

Reference points, taking only the configurations where the MLP width does not
also move:

| model | depth, heads | Top-1 | params |
|---|---|---|---|
| XCiT-M | 24, 8 → 12, 16 | 81.4 → 81.7 | 84.4M → 59.0M |
| TNT-B | 12, 10 → 8, 16 | 82.3 → 82.3 | 65.4M → **30.9M** |
| DaViT-B | 9 → 5 blocks in stage 3 | 83.3 → 83.5 | 88.0M → 62.0M |
| XCiT-L | 24, 16 → 12, 24 | 82.1 → 82.4 | 189.1M → 103.8M |
| DaViT-L | 9 → 5 blocks in stage 3 | 83.6 → 83.6 | 196.8M → 140.0M |

On language, Crammed BERT goes from 16 layers and 12 heads at 119M to 10
layers and 24 heads at **84M**, with the GLUE average identical at 78.6.

## Why it should work

The condition number of a matrix is `σ₁/σ_k`, and a high one slows gradient
descent. Theorem 3.2 shows the attention block's condition number falls as the
number of heads rises. So heads are doing optimization work and not only
representational work — and if some of what depth was buying was
easier optimization, heads can buy it more cheaply, because a head costs a
fraction of a layer.

## Why `Proposed`

**The mechanism is proved and the trade is not derived from it.** The paper
says so itself: "while we lack a full theoretical explanation for this
trade-off". Conditioning improves with heads; whether that is *why* the
dropped layers are free is a hypothesis with a suggestive experiment behind
it.

**It contradicts [SOTA-190](SOTA-190.md) and nothing arbitrates.** That practice says to
increase depth before any other dimension. The axes are not the same — depth
against width there, depth against head count here — and neither paper cites
the other. The record carries both.

**No throughput anywhere.** Parameters and training memory fall by up to half.
Latency, tokens per second and behaviour under model parallelism are not
reported, and [SOTA-190](SOTA-190.md)'s source names parallelism as the reason its own
recommendation has a ceiling. A shape recommendation without a throughput
column is half a recommendation.

**One group, one seed per configuration, 300 epochs on ImageNet-1k.**

## Conditions

**Half the paper's configurations also shrink the MLP.** ViT, DeiT and VOLO
rows change three things at once and their parameter savings should not be
quoted for this practice. The five rows above are the ones that isolate it.

**More heads at fixed width means smaller heads**, and no experiment here
finds where that breaks. XCiT-L runs 24 heads of dimension 128; nothing says
what happens at 48 heads of 64.

**Untested against [SOTA-109](SOTA-109.md).** Grouped-query attention reduces distinct
key-value heads to save memory bandwidth; this raises head count for
conditioning. They are not contradictory — GQA keeps query heads separate —
but nobody has built a model that does both, and this practice gives no
guidance on the interaction.

**The language evidence is 119M and below.** Crammed BERT and a GPT-2 on
TinyStories. Everything at scale here is vision.

## Known implementations

None. The paper rebuilds published architectures; no released model is known
to use the resulting shapes.
