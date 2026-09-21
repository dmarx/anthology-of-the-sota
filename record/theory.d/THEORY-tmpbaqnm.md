---
status: Proposed
promote_when: >-
  The gradient-direction-error crossing measured on a model family other than
  the source's, and shown to *predict* where the switch point should go —
  rather than observed after the fact on a run whose switch point was already
  known to be robust. A further replication that dropout lowers gradient
  variance early is not it; that part is already shown across five
  model/optimizer pairs.
title: 'Dropout early in training buys a biased gradient estimate with much less directional variance, and the trade is favourable until it is not'
version: 1
tags:
- model-stability
- training-optimization
date: '2026-09-21'
source:
- LIT-tmpfdpkj
explains:
- SOTA-tmpxll55
summary: >-
  Liu et al. (2023), [LIT-tmpfdpkj](../literature.d/LIT-tmpfdpkj.md) — with dropout, mini-batch
  gradients are a *biased* estimate of the whole-dataset gradient, because
  each batch runs through a different sub-network. Their directional variance
  falls far enough that the angle to the true gradient falls too — for about
  the first thousand iterations, after which it rises and dropout goes back to
  being a regularizer.
---

<!-- inactive-ok-file: SOTA-tmpxll55 — Proposed, and the practice this account
     explains; naming it in the `explains` table is the relation, not a claim that
     either is settled -->

# THEORY-tmpbaqnm: Dropout early in training buys a biased gradient estimate with much less directional variance, and the trade is favourable until it is not

## Source

Liu, Xu, Jin, Shen and Darrell (2023), [LIT-tmpfdpkj](../literature.d/LIT-tmpfdpkj.md) §3 — read as
[NOTE-tmpbrbwv](../notes.d/NOTE-tmpbrbwv.md).

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-tmpxll55](../practices.d/SOTA-tmpxll55.md) | dropout at the start if the model underfits, at the end if it overfits | not two uses of a regularizer but two different operators, separated by whether the bias it introduces is cheaper than the variance it removes |

## The account

Start from the observation that does not fit. A model trained with dropout
produces **smaller** gradients and ends up **farther** from its
initialization than one trained without. Smaller strides, more distance.

The only way that happens is if the strides agree with each other. Two
measurements confirm it:

- The average pairwise cosine distance among mini-batch gradients — their
  **directional variance** — is lower with dropout, for roughly the first
  thousand iterations.
- The average cosine distance from mini-batch gradients to the gradient of the
  **whole training set** — the directional *error* — is lower too, over the
  same stretch.

The second is the one that matters, because the first alone would be
consistent with consistently going the wrong way.

The bias–variance reading is exact. Without dropout, a mini-batch gradient is
an unbiased estimate of the full-dataset gradient: same network, random
subset. With dropout it is **biased**, because each batch passes through a
different sub-network whose expected gradient is not the full network's. The
trade is that variance falls by more than bias costs, so the total angular
error falls.

That is why the effect is temporary. Early, the model is changing fast, any
single batch is a poor guide, and variance dominates the error. Later, the
estimate is already well aligned, there is little variance left to remove, and
the bias is all that remains — so the error curves cross, at about a thousand
iterations for the source's ViT-T, and dropout reverts to being a regularizer
that trades training fit for generalization.

One account, two regimes, and the crossing is the boundary between them.

## What is shown across settings and what is not

The **variance and error reduction** is not a one-model observation. Measured
as area under the gradient-direction-error curve over the first 1500
iterations, it appears with AdamW (−13.60%), plain SGD (−9.30%) and momentum
SGD (−6.67%) on ViT-T, and on Swin-F (−17.41%) and ConvNeXt-F with stochastic
depth (−7.62%). Five model/optimizer pairs, same sign.

The **crossing point** is one model. "About 1000 iterations" is where ViT-T's
curves meet on ImageNet-1K, and nothing predicts where it sits elsewhere.

## Why `Proposed`

Because the part that would make this an instrument is the part that has not
been tested. If the crossing predicts the right switch point, the metric is a
tool you could apply to a new setting. If it does not, the practice's wide
robustness range (1% to 50% of epochs) is doing all the work and the crossing
is a story told about a number that turned out not to matter.

The source reports both facts and does not connect them, which is the right
thing to have done and leaves the account short of established.

## What this does not say

**It does not replace the regularization account.** [THEORY-015](THEORY-015.md) and
[THEORY-016](THEORY-016.md) explain what dropout does as a regularizer — a data-dependent
penalty, and a geometric-mean ensemble at test time — and both are about the
steady state. This is about the first thousand iterations. They are the same
operator at different times, not competing explanations of one thing.

**It does not identify the sub-network bias.** That dropout makes the estimate
biased is stated and is obvious; how large the bias is, and whether it grows
or shrinks through training, is not measured. The claim that variance falls by
more than bias costs is inferred from the total error falling.

**And it says nothing about whether this is warmup by another name.**
Learning-rate warmup ([SOTA-008](../practices.d/SOTA-008.md), [SOTA-009](../practices.d/SOTA-009.md)) is the record's
other early-training intervention justified by gradient behaviour. The
directional-error metric is exactly the instrument that would tell you whether
the two are doing one job twice. Nobody has run it.
