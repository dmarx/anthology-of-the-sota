---
number: 192
status: Active
formerly:
- SOTA-tmp52hr5
consensus: converged
consensus_note: >-
  Standard in frontier training. DeepSeek-V4 runs Muon with QK-norm and no
  clip; the Kimi line takes the other route. The invariant is agreed, the
  instrument is not.
title: 'Normalize the queries and keys before the attention dot product'
version: 8
history:
- version: 2
  date: '2026-09-18'
  note: >-
    Adds `attention-techniques`. The practice normalizes queries and keys before the dot product; its relation to SOTA-131 joins two interventions on the same matrices (ADR-049).
- version: 3
  date: '2026-09-18'
  # inactive-ok-block: SOTA-168 — Proposed, and named only as a member of
  # the line this tag binds; nothing here rests on its standing
  note: >-
    Adds `training-optimization`. Normalizing queries and keys is a training-dynamics intervention, and it is the value shared by the line running through SOTA-121, SOTA-165 and SOTA-168 (ADR-049).
- version: 4
  date: '2026-09-20'
  note: >-
    Records an independent arrival. Esser et al. (LIT-449) adopt QK-norm
    for a high-resolution diffusion transformer after mixed-precision
    training diverged, diagnosing it through the discriminative ViT
    literature's attention-entropy result rather than through anything in the
    language-model line this practice was filed from. Neither line cites the
    other. The recommendation is unchanged; what is added is that the
    invariant now has two arrival events from two different failures.
- version: 5
  date: '2026-09-22'
  note: >-
    Adds a condition about the failure's DIAGNOSIS, not its remedy. This
    document describes near-zero attention entropy as the failure. Qi et al.
    (LIT-521) report a stable regime with near-zero entropy and argue the
    discriminator is whether the attention map is also low-rank, with the
    upstream cause being spectral energy concentration in the query-key
    product. That is one group contradicting another and is recorded as such.
    The recommendation is unchanged and so is the status: bounding the logits
    prevents both candidate modes, so nothing about what to do turns on which
    account is right. What turns on it is what a reader watching a live run
    should measure.
- version: 6
  date: '2026-09-24'
  note: >-
    Corrects `introduced_by`. This practice named LIT-088 (ViT-22B, 2023) as
    the work that first stated the recommendation. It was first stated by
    Henry et al. in 2020 (LIT-640), who named the technique; LIT-088's
    own body says the record held no source establishing it. `introduced_by`
    repoints to the origin. LIT-088 stays in `source:` because the scale
    demonstration this document is built on is entirely its, and the origin
    joins it there because it ran a controlled comparison of its own. The
    recommendation, the status and the consensus reading are unchanged --
    what changes is who the record says made the claim.
- version: 7
  date: '2026-09-24'
  note: >-
    Adds a condition about what bounding the logits costs, which nobody here
    had stated. Veličković et al. (LIT-653) prove that softmax
    coefficients are capped at `(1/n)·exp(δ/θ)`, and their Proposition 3.1
    names normalisation before the query-key mechanism as clamping the
    activation norms — this practice, by name. A smaller logit spread is the
    point of the recommendation and also tightens that cap. The
    recommendation, status and consensus are unchanged: the trade is
    unmeasured, and what it would cost is sharpness at long inputs rather than
    stability.
- version: 8
  date: '2026-09-25'
  note: >-
    Records a controlled ablation from outside the language-model scaling
    line. In LIT-tmpbukux's 20-layer attention-only decoder, removing QK-norm
    diverged at the tuned Muon rate. It was the only divergence in the study,
    and residual gates and ReZero residuals turned out neutral. It is one run
    at one rate and 24M parameters, so it is recorded in the body and not
    added as a source. The recommendation, status and consensus are
    unchanged.
tags:
- model-stability
- attention-techniques
- training-optimization
date: '2026-09-10'
source:
- LIT-640
- LIT-088
introduced_by:
- LIT-640
extends:
- SOTA-050
compared_against:
- SOTA-131
implementations:
- ViT-22B
- DeepSeek-V4
explained_by:
- THEORY-061
- THEORY-097
---
<!-- inactive-ok-file: THEORY-062 — Proposed, filed in this same
     contribution and named in a condition that says it is one group's
     unadjudicated counterexample. The condition depends on it being
     unsettled. -->

# SOTA-192: Normalize the queries and keys before the attention dot product

## Source

Henry, Dachapally, Pawar and Chen (2020), `LIT-640` — the paper that
named the technique and first made the recommendation.

Dehghani et al. (2023), [LIT-088](../literature.d/LIT-088.md) — ViT-22B, where the mechanism is diagnosed
rather than only fixed, and the demonstration this document is built on.

## Two papers, one recommendation, three years apart

This practice was filed naming `LIT-088` as both its source and its origin.
<!-- inactive-ok-block: ADR-029 — Superseded by ADR-030, which is cited beside
     it. The pair is the point: ADR-029 drew the origin/evidence distinction
     and ADR-030 refined it, so naming only the successor would hide where the
     rule this correction applies came from. -->
The origin was wrong, and `LIT-088`'s own body said so — it records that
nothing in the record read a source establishing QK-norm, and calls itself
*one of the earliest at scale*. That is an adoption claim, correctly hedged;
what it could not do was fill the slot `introduced_by` asks for, which is the
work that **first made the recommendation** rather than the work that
evidenced it ([ADR-029](../decisions.d/ADR-029.md), refined by [ADR-030](../decisions.d/ADR-030.md)).

Henry et al. made it in 2020, and the two arrivals differ in every respect
except the intervention:

| | `LIT-640` (2020) | [LIT-088](../literature.d/LIT-088.md) (2023) |
| --- | --- | --- |
| failure addressed | softmax saturation costing expressivity | divergence at ~8B parameters |
| scale | low-resource translation | 22B-parameter vision encoder |
| the scale factor | `1/√d` **replaced** by a learnable parameter | `1/√d` retained |
| evidence | +0.928 BLEU over five pairs | one model diverging, then converging |

The third row is the one that gets lost. Henry et al. do not add a
normalization in front of the existing scaling — they normalize the queries
and keys and then **scale by a trained scalar instead of a constant**, which
makes the softmax temperature a learned quantity. The record's later usage,
and `LIT-088`'s, keeps `1/√d`. Both bound the logits; only one turns the
temperature into a parameter, and that difference is what `LIT-641`
measures.

So the two are not a citation chain but two independent arrivals — a third
sits below in diffusion transformers ([LIT-449](../literature.d/LIT-449.md)). What this correction adds
is that the earliest of the three is now held, and that the record can stop
reading a 22B vision encoder as the place a translation technique began.

## The failure it prevents

Attention logits grow without bound as the query and key weights grow. Past some
point the softmax saturates and the failure is total: ViT-22B observed

> divergent training loss after a few thousand steps … caused by extremely large
> values in attention logits, which lead to (almost one-hot) attention weights
> with near-zero entropy

An almost-one-hot softmax has almost no gradient, so the layer stops learning
and the run diverges. The instability appeared at around **8B parameters** — it
is a scale phenomenon, absent below and fatal above.

## The fix

Apply a normalization to the queries and keys **before** the dot product:

    softmax[ (1/√d) · LN(XW_Q)(LN(XW_K))ᵀ ]

Bounding the norms of the two vectors bounds their inner product, so the logits
cannot grow with the weights. ViT-22B shows an 8B model diverging without it and
converging with it, everything else equal.

## Why `1/√d` is not enough

[SOTA-050](SOTA-050.md) already divides by `√d_head`, and that is the right correction for a
different problem: the dot product's variance grows with the **dimension**, so
the scale factor removes the dimension's contribution. It does nothing about the
**weights** growing during training. `1/√d` is a fix at initialisation;
QK-normalization is a fix that holds throughout.

## The other route to the same invariant

[SOTA-131](SOTA-131.md) (QK-Clip) rescales the query and key weights whenever the logits
exceed a threshold — the same invariant, enforced reactively on the weights
rather than structurally on the activations. The Kimi line uses the clip;
DeepSeek-V4 runs Muon with QK-norm and reports not needing it.

**Nobody has compared them.** The record now carries both, and which is
preferable — or whether the clip is only necessary when the normalization is
absent — is unresolved.

## A third arrival, from generative modelling

The two routes above are both from language-model training. A third arrives
from image synthesis and does not cite either: Esser et al., [LIT-449](../literature.d/LIT-449.md),
found that mixed-precision training of an 8B diffusion transformer **diverged
when moving to high resolution**, took the diagnosis from the discriminative
ViT literature — attention entropy growing without bound — and fixed it with
RMSNorm on Q and K in both streams of their architecture.

Same intervention, same invariant, a failure mode the language-model line
never reports, and no citation in either direction.

[DP-007](../principles.d/DP-007.md) says agreement has no author and therefore no arrival event.
This is the interesting variant: there are two arrival events, in different
literatures, and the record can see both only because it files by the kind of
claim rather than by the domain the claim was found in ([ADR-026](../decisions.d/ADR-026.md)).

## Conditions

**Entropy alone may be the wrong instrument for diagnosis.** Qi et al.
([LIT-521](../literature.d/LIT-521.md), read as [NOTE-266](../notes.d/NOTE-266.md)) report attention
maps that are sparse but **not** low-rank — near-identity, near-zero entropy —
in runs that train perfectly well, and present that as a counterexample to the
entropy criterion. On their account the fatal state is sparse *and* low-rank,
and the predictor is spectral energy concentration in `W_q^T W_k`, which in
crashed runs falls into fewer than ten directions. That is one group against
another, at 50M–307M, and nobody has adjudicated it — see
[THEORY-062](../theory.d/THEORY-062.md).

It changes nothing about this recommendation, because bounding the logits
suppresses both modes. It changes what to look at when deciding whether a run
in progress is in trouble.

**Bounding the logits is what this practice is for, and it is not free.**
Veličković et al. ([LIT-653](../literature.d/LIT-653.md)) prove that a softmax over `n` items
caps every coefficient at `(1/n)·exp(δ/θ)`, where `δ` is the logit spread — so
how sharp a head can be at a given input size is governed by exactly the
quantity this recommendation exists to shrink. Their Proposition 3.1 names the
intervention directly:

> there is a common practice of leveraging operators such as layer
> normalisation… which clamps `‖x_i‖` and `‖y‖` if applied right before the
> query-key mechanism, **accentuating the impact of Q and K's singular
> values**.

Two things follow, and they point in opposite directions. Sharpness in a
Transformer is only reachable by growing weights — `δ ≤ 2·σ_max(Q)·σ_max(K)·
‖y‖·max‖x‖` — which is the same weight growth this practice treats as the
failure. And a normalised `Q` and `K` leave `δ` to the singular values alone,
which is also `THEORY-062`'s crash predictor.

**Nothing here changes the recommendation**, and the reason is that the two
failures live at different input sizes: entropy collapse is a training
pathology at whatever length you train on, and dispersion is an
out-of-distribution one. Nobody has measured whether QK-normalised models
disperse sooner than unnormalised ones, and until somebody does this is a
consequence of two bounds rather than a cost anyone has paid. It is recorded
because a reader who bounds the logits should know what the bound also does.

`LIT-088` is a **vision encoder**. The mechanism — logit growth, entropy
collapse, vanishing gradient — is architecture-independent and is the reason the
practice transfers, but the demonstration is not a decoder-only language model.
The corroboration on that side is [SOTA-131](SOTA-131.md)'s own body, which records DeepSeek-V4
using QK-norm in place of the clip.

Adds two normalization operations per attention layer. ViT-22B does not report
the cost separately.

## An ablation from a model with no feed-forward layers

LIT-tmpbukux trains attention-only decoders, with every feed-forward layer
deleted, to 48 layers and 105B tokens. It tested which component keeps them
trainable. The authors expected residual gating. The answer was QK-norm.
Removing it from the 20-layer, 24M-parameter model **diverged at the tuned
learning rate** (validation loss 8.28), the only divergence in the study.
Removing the gates, or swapping in a ReZero residual, changed loss by less
than 0.004 nats.

It is one run at one rate under Muon, in an architecture nobody ships, and the
authors scope the claim to that rate. It is not another arrival like the
ones above, because the paper cites LIT-640 and LIT-088 and adopted QK-norm
from them. It is a test. It took the component out of an otherwise fixed
model, and the model failed. It does not say which of the failure modes
above occurred, since the run reports no entropy or logit measurements.

## Known implementations

- ViT-22B; DeepSeek-V4 (with Muon, no clip)
