---
status: Proposed
formerly:
- SOTA-tmpussf5
promote_when: >-
  A group outside DeepSeek training a mixture-of-experts with the bias update
  and reporting both balance and quality against an auxiliary-loss control.
  A model that merely ships loss-free balancing without running that
  comparison is not the missing evidence — DeepSeek-V3 already did that, and
  it is why this is filed rather than deferred.
consensus: unreplicated
consensus_note: >-
  One lab. The method (LIT-171) and the 671B model that adopted it (LIT-160)
  are both DeepSeek-AI, and no group outside it has published a result either
  way. That is not the same as contested: nobody has looked and disagreed,
  nobody has looked and confirmed.
title: 'Balance mixture-of-experts load with a bias on the routing scores, not an auxiliary loss'
version: 1
tags:
- model-architecture
date: '2026-09-07'
published: '2024-08-01'
source:
- LIT-171
- LIT-160
implementations:
- DeepSeek-V3
summary: >-
  Wang et al. (2024), [LIT-171](../literature.d/LIT-171.md) — add a per-expert bias to the routing scores
  before the top-K decision and update it from that expert's recent load, so
  balancing changes which experts are chosen without adding a gradient to the
  loss. Better balance *and* better quality than an auxiliary-loss control,
  and what DeepSeek-V3 runs at 671B.
---

# SOTA-148: Balance mixture-of-experts load with a bias on the routing scores, not an auxiliary loss

A mixture-of-experts needs its experts used evenly: an unbalanced load either
collapses routing onto a few experts or wastes the capacity of the rest. The
standard remedy is an auxiliary loss that penalises imbalance, added to the
training objective with a coefficient.

That coefficient is a trade, and it is the problem. Large enough to balance
the load, the auxiliary term injects **interference gradients** — updates that
serve balance rather than the objective you actually care about. Balance and
quality get traded against each other through a number nobody can set
correctly.

**Loss-Free Balancing takes the balancing out of the gradient entirely.**
Before the top-K decision, add a per-expert bias to the routing scores, and
update each bias from that expert's recent load: overloaded experts get their
bias lowered, idle ones raised. Routing changes. The loss does not.

Because no interference gradient exists, this is not a better point on the
balance/quality trade — it removes the trade. [LIT-171](../literature.d/LIT-171.md) reports better
performance *and* better balance than an auxiliary-loss control at 3B
parameters and 200B tokens, and [LIT-160](../literature.d/LIT-160.md) is DeepSeek-V3 running it at 671B.

## What this presumes, and does not argue

It presumes you are training a mixture-of-experts. **It is not a
recommendation to train one** — the record has no practice saying "use a
mixture of experts", the question is open as
[#17](https://github.com/dmarx/anthology-of-the-sota/issues/17), and this
document does not settle it.

That separation is what makes this fileable on its own.
[LIT-171](../literature.d/LIT-171.md)'s own standing section worried the opposite way — that a
load-balancing practice "would arrive without the context that makes it
meaningful" because the record carries no MoE practices at all. The
resolution is that architecture choice and technique are different kinds of
claim. Whether to build a sparse model is an editorial judgement about where
the field is going; how to keep its experts evenly loaded once you have is a
technique with a mechanism and an ablation, and it is answerable without the
other question being settled.

## Why `Proposed` and `unreplicated`

The evidence is good and it is all from one lab. [LIT-171](../literature.d/LIT-171.md)'s authors are
DeepSeek-AI and [LIT-160](../literature.d/LIT-160.md) is DeepSeek's own model; nobody outside has
published a result either way. That is `unreplicated` rather than
`contested` — people have not looked and disagreed, they have not looked.

<!-- inactive-ok-block: SOTA-122, SOTA-124, SOTA-125, SOTA-144 — all
     Proposed, and that they are Proposed is precisely what is being cited -->

The record's four other `unreplicated` practices are all `Proposed`
([SOTA-122](SOTA-122.md), [SOTA-124](SOTA-124.md),
[SOTA-125](SOTA-125.md), [SOTA-144](SOTA-144.md)), and this is the same
shape: a clean mechanism, one group, real scale.

## The MoE material now in the record

Three practices' worth, and this is the first of them filed:

- [LIT-170](../literature.d/LIT-170.md) — fine-grained plus shared experts, the architecture itself. Not
  filed; that is the open question.
- [LIT-171](../literature.d/LIT-171.md) — this.
- [LIT-180](../literature.d/LIT-180.md) — the RL objective is unstable on mixture-of-experts
  specifically.

<!-- inactive-ok-block: SOTA-146 — Proposed, named as the caveat it carries -->

That last one is already in the registry: [SOTA-146](SOTA-146.md) carries the
instability as a caveat on an architecture the record has never recommended.
