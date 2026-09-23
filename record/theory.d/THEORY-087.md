---
number: 87
status: Deferred
formerly:
- THEORY-tmpf89jm
promote_when: >-
  An ablation that varies the candidate mechanisms independently in one
  codebase under one training recipe — predictor, stop-gradient, EMA rate,
  variance floor, decorrelation — and reports which removals collapse. The
  existing evidence is four papers each removing pieces of their own method
  under their own recipe, which cannot separate a mechanism from an
  implementation detail. A paper that merely proposes a fifth account and
  shows it fits its own method would not settle it.
title: 'Why a negative-free siamese network avoids collapse is unsettled, and the three accounts contradict each other'
version: 2
history:
- version: 2
  date: '2026-09-23'
  note: >-
    Unit D added SwAV and DINOv2 as sources. SwAV supplies a fifth account —
    an equipartition constraint, which is neither an asymmetry nor a
    regulariser on the embedding — and DINOv2 supplies the most telling
    datum in the document: rather than choose among the accounts, it stacks
    two of them. The title still says "three", which is now the count of
    accounts that contradict rather than the count of accounts.
tags:
- analysis-and-evaluation
- model-stability
- representation-and-encoding
date: '2026-09-23'
source:
- LIT-593
- LIT-594
- LIT-595
- LIT-596
- LIT-tmp6nq8y
- LIT-tmpfwfu3
explains:
- SOTA-365
---

# THEORY-087: Why a negative-free siamese network avoids collapse is unsettled, and the three accounts contradict each other

## The situation

A joint-embedding loss with no negatives has an exact trivial minimum:
output the same vector for everything. Four methods avoid it, all reach
within a couple of points of each other on ImageNet linear evaluation
(74.3 / 67.7 / 73.2 / 73.2), and **each offers a different account of why,
inconsistent with the others**.

| account | source | mechanism claimed | what it says is essential |
| --- | --- | --- | --- |
| no joint loss | [LIT-594](../literature.d/LIT-594.md) | the target's update is not a gradient of the loss, so there is no objective being jointly minimised — "similar to GANs" | predictor **and** EMA target |
| alternating optimisation | [LIT-593](../literature.d/LIT-593.md) | an EM-like alternation over two variable sets, "analogous to k-means" | stop-gradient |
| redundancy reduction | [LIT-596](../literature.d/LIT-596.md) | the off-diagonal cross-correlation penalty makes constant outputs unavailable | neither asymmetry nor negatives |
| explicit variance | [LIT-595](../literature.d/LIT-595.md) | a hinge on per-dimension standard deviation forbids collapse arithmetically | none of the above |
| equipartition | LIT-tmp6nq8y | codes are constrained so that a batch is equally divided across prototypes, so two images cannot share one | neither asymmetry nor a term on the embedding |

## Where they contradict

**On the momentum encoder, directly and numerically.** BYOL reports that
removing it gives **0.3%** accuracy and treats it as essential.
`LIT-593` *is* that removal and reports **67.7%**. Two careful groups,
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

## The two additions from unit D, and why they make it worse

**SwAV is a fifth account and it is not a variant of the other four.** Its
constraint is on the *assignment*, not on the embedding and not on the
architecture: within a batch, examples are equally partitioned across
prototypes, so "the codes for different images in a batch are distinct, thus
preventing the trivial solution where every image has the same code". Neither
the asymmetry family nor the variance family covers it.

It also has the sharpest reminder that these mechanisms are not clean. SwAV's
entropy regularisation `ε` smooths the assignment, and "a strong entropy
regularization generally leads to a trivial solution where all samples
collapse into an unique representation". **A mechanism introduced to prevent
collapse has a setting at which it causes it.**

**DINOv2 declines to choose.** Faced with five accounts, the strongest
open-source model in this lineage stacks them: a **KoLeo** regulariser
spreading features within a batch, in the spirit of the variance family,
*and* **Sinkhorn-Knopp centering borrowed from SwAV**, in the spirit of the
equipartition family, on top of DINO's teacher-student asymmetry. All three
appear as separate ablation rows.

That is the most informative datum in this document. A group with the compute
to settle the question instead assembled the mechanisms additively and
reported what each was worth — which is what you do when you have no theory,
and is a reasonable thing to do. It is not evidence for any account.

## What is *not* in dispute

- The collapse is real and reachable: removing the stop-gradient sends the
  loss to its floor of −1 within a few steps.
- Each method's own ablations replicate within its own codebase.
- All four produce useful representations.

So this document disputes the explanations, not the results — the
distinction `ADR-031` exists for. `SOTA-365` is `Active` while this is
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
