---
number: 148
status: Proposed
formerly:
- SOTA-tmpussf5
promote_when: >-
  A group outside DeepSeek training a mixture-of-experts with the bias update
  and reporting both balance and quality against an auxiliary-loss control.
  A model that merely ships loss-free balancing without running that
  comparison is not the missing evidence — DeepSeek-V3 already did that, and
  it is why this is filed rather than deferred.
consensus: emerging
consensus_note: >-
  Two labs now. The method (LIT-171) and the 671B model that adopted it
  (LIT-160) are DeepSeek-AI's, and Kimi K3 (LIT-131) adopts it at 2.8T with
  896 experts and rewrites the update rule to hold there. Adoption and
  extension by an outside group, still with no head-to-head against an
  auxiliary-loss control from anyone but the originating lab.
title: 'Balance mixture-of-experts load with a bias on the routing scores, not an auxiliary loss'
version: 3
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Kimi K3 (LIT-131) adopts the method outside DeepSeek at 2.8T and
    replaces the fixed-step update with Quantile Balancing; DeepSeek-V4
    (LIT-139) runs a slight sequence-wise balance loss alongside the bias.
    Consensus moves from unreplicated to emerging. The recommendation is
    unchanged and the promotion condition is still unmet.
- version: 3
  date: '2026-09-07'
  note: >-
    Sourced to LIT-131 as well. K3 keeps the recommendation and replaces the
    update rule, reporting that at 896 routed experts per layer balancing
    "exceeds the regime in which existing auxiliary-loss-free bias updates
    remain effective" — a measurement of where the claim stops holding
    rather than an adoption of it, and the qualification the Variations
    section is built on. The recommendation is unchanged.
tags:
- model-architecture
date: '2026-09-07'
source:
# LIT-171 introduces the bias; LIT-160 is where it ships. LIT-131 is not an
# adopter here — it reports the size at which the fixed-step update stops
# being effective, which is a measurement of this claim's limit and the
# qualification the Variations section is built on (ADR-017). LIT-139's
# auxiliary loss alongside the bias is a deployment variation without a
# comparison, so it stays in the body.
- LIT-171
- LIT-160
- LIT-131
extends:
- SOTA-150
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

## Variations, and one qualification from the originating lab

**Kimi K3 ([LIT-131](../literature.d/LIT-131.md)) keeps the recommendation and replaces the update
rule.** At 896 routed experts per layer it reports that balancing "exceeds
the regime in which existing auxiliary-loss-free bias updates remain well
behaved": the fixed-step rule's step size trades slow adaptation against
load oscillation, and neither end of that trade is acceptable at ~900
experts. Quantile Balancing sets each expert's bias directly from the
router-score quantile matching its target load, read from a single forward
pass — Top-(k+1) selection makes the (k+1)-th entry the cutoff an expert
must beat — and estimated at scale from a per-expert histogram of margins,
one all-reduce of bin counts. The parts this practice turns on are kept: the
bias is excluded from the mixture weights, so no gradient flows through it,
and the update lands only on the next step, so no batch is routed with a
bias derived from itself.

So the *bias on the routing score* is what generalised; the *fixed step* is
what did not, and the report says at roughly what size it stopped.

**DeepSeek-V4 ([LIT-139](../literature.d/LIT-139.md)) runs a small auxiliary loss alongside the bias.**
Bias update speed 0.001, "augmented by a slight sequence-wise balance loss
that prevents extreme imbalance within individual sequences" at weight
0.0001. That is the originating lab qualifying its own result three models
on, and it is worth being exact about what it concedes. The bias regulates
load *across a batch*; nothing in the mechanism reaches imbalance *inside
one sequence*, which is the failure the 0.0001 loss is aimed at. The claim
this practice makes — that you do not need an auxiliary loss to balance
experts — survives. The stronger reading, that an auxiliary loss has no
remaining job at all, does not.

## Why `Proposed`, and why `emerging` now

The head-to-head evidence is still one lab's: [LIT-171](../literature.d/LIT-171.md)'s authors are
DeepSeek-AI and [LIT-160](../literature.d/LIT-160.md) is DeepSeek's own model. What changed is that
"nobody outside has published a result either way" stopped being true. K3 is
an outside group that adopted the method at four times the scale, hit a
limit in it, and published the fix — stronger evidence than a silent
adoption, weaker than a controlled comparison.

It still does not meet the promotion condition, and deliberately so: that
condition asks for balance *and quality* against an auxiliary-loss control,
and K3 runs no such control. The condition anticipated something like this
— "a model that merely ships loss-free balancing without running that
comparison is not the missing evidence" — and K3 does more than ship while
still not being what was asked for.

<!-- inactive-ok-block: SOTA-122, SOTA-124, SOTA-125, SOTA-144 — all
     Proposed, and that they are Proposed is precisely what is being cited -->

The record's `unreplicated` practices are all `Proposed`
([SOTA-122](SOTA-122.md), [SOTA-124](SOTA-124.md),
[SOTA-125](SOTA-125.md), [SOTA-144](SOTA-144.md)). This one has moved off
that shelf without becoming settled.

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
