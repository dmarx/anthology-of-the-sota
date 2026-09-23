---
status: Deferred
promote_when: >-
  An ablation that varies the candidate mechanisms independently in one
  codebase under one training recipe — predictor, stop-gradient, EMA rate,
  variance floor, decorrelation — and reports which removals collapse. The
  existing evidence is four papers each removing pieces of their own method
  under their own recipe, which cannot separate a mechanism from an
  implementation detail. A paper that merely proposes a fifth account and
  shows it fits its own method would not settle it.
title: 'Why a negative-free siamese network avoids collapse is unsettled, and the three accounts contradict each other'
version: 1
tags:
- analysis-and-evaluation
- model-stability
- representation-and-encoding
date: '2026-09-23'
source:
- LIT-tmp3roys
- LIT-tmpawe8p
- LIT-tmpipfcy
- LIT-tmpovcux
explains:
- SOTA-tmp1kmsu
---

# THEORY-tmpf89jm: Why a negative-free siamese network avoids collapse is unsettled, and the three accounts contradict each other

## The situation

A joint-embedding loss with no negatives has an exact trivial minimum:
output the same vector for everything. Four methods avoid it, all reach
within a couple of points of each other on ImageNet linear evaluation
(74.3 / 67.7 / 73.2 / 73.2), and **each offers a different account of why,
inconsistent with the others**.

| account | source | mechanism claimed | what it says is essential |
| --- | --- | --- | --- |
| no joint loss | [LIT-tmpawe8p](../literature.d/LIT-tmpawe8p.md) | the target's update is not a gradient of the loss, so there is no objective being jointly minimised — "similar to GANs" | predictor **and** EMA target |
| alternating optimisation | [LIT-tmp3roys](../literature.d/LIT-tmp3roys.md) | an EM-like alternation over two variable sets, "analogous to k-means" | stop-gradient |
| redundancy reduction | [LIT-tmpovcux](../literature.d/LIT-tmpovcux.md) | the off-diagonal cross-correlation penalty makes constant outputs unavailable | neither asymmetry nor negatives |
| explicit variance | [LIT-tmpipfcy](../literature.d/LIT-tmpipfcy.md) | a hinge on per-dimension standard deviation forbids collapse arithmetically | none of the above |

## Where they contradict

**On the momentum encoder, directly and numerically.** BYOL reports that
removing it gives **0.3%** accuracy and treats it as essential.
`LIT-tmp3roys` *is* that removal and reports **67.7%**. Two careful groups,
the same ablation, results three orders of magnitude apart. Neither paper
resolves it, and the difference must lie in something neither isolated.

**On whether asymmetry is the mechanism at all.** SimSiam argues the
momentum encoder's apparent importance was a confound, because it "is always
accompanied with stop-gradient". But Barlow Twins and VICReg then remove the
stop-gradient too, and do not collapse. If the account is about asymmetry,
it does not cover half the field.

**On what a fix is a fix for.** BYOL's own ablation shows the target network
can be dropped when the predictor is kept near-optimal (52.5% by closed-form
solution, 66.5% by raising only its learning rate, ≈25% by raising both the
projector's and the predictor's). That is not obviously the same phenomenon
as a variance hinge, and no account covers both.

## What is *not* in dispute

- The collapse is real and reachable: removing the stop-gradient sends the
  loss to its floor of −1 within a few steps.
- Each method's own ablations replicate within its own codebase.
- All four produce useful representations.

So this document disputes the explanations, not the results — the
distinction `ADR-031` exists for. `SOTA-tmp1kmsu` is `Active` while this is
`Deferred`, and that pairing is deliberate.

The status is `Deferred` rather than `Proposed` on the vocabulary's own
terms: `Proposed` is for an account "stated and plausible, on evidence that
is suggestive rather than settling", and this document proposes no account at
all. `Deferred` is "filed because the question is real; no position taken on
the answer", which is exactly what this is. The four accounts below are
reported, not endorsed.

## Why the record should keep the dispute open rather than pick

Because the obvious tiebreak is unavailable. Every piece of evidence is a
paper removing components of **its own** method under **its own** training
recipe — its own learning rate, weight decay, projector width, augmentation
set. BYOL itself notes that removing weight decay makes both BYOL and SimCLR
diverge, which is a reminder of how much of the recipe is load-bearing for
reasons unrelated to collapse. A 0.3%-versus-67.7% discrepancy on nominally
the same ablation is the signature of exactly that confound, and no amount of
reading the four papers against each other resolves it.

`promote_when` therefore asks for the experiment nobody in this cluster ran:
one codebase, one recipe, the candidate mechanisms varied independently.
