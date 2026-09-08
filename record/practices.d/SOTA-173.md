---
status: Proposed
formerly:
- SOTA-tmprblvs
promote_when: >-
  An independent group running one of the three augmentation families against
  an un-augmented baseline in a data-constrained multi-epoch setting and
  reporting where the overfitting point moved; or a pretraining report that
  says it augmented for this reason. What would not move it: a paper adding
  an auxiliary objective and reporting a better final loss without the
  multi-epoch, data-constrained framing — the claim here is specifically
  about *delaying* the overfitting these settings produce.
consensus: unreplicated
consensus_note: >-
  One group, one paper, and the newest position in a three-way disagreement
  about repetition that nobody has yet run the decisive experiment on.
title: 'Augment the objective to make multi-epoch pretraining productive on a fixed corpus'
version: 1
tags:
- data-pipeline
date: '2026-09-08'
published: '2026-06-01'
source:
- LIT-175
implementations: []
summary: >-
  Chen et al. (2026), [LIT-175](../literature.d/LIT-175.md) — standard autoregressive pretraining overfits
  severely on a fixed corpus, reaching its optimum early and deteriorating
  continuously. Three orthogonal augmentation families each delay that and
  lower validation loss; combining them lowers the minimum further. The claim
  is hundreds of productive epochs on the same data.
---

# SOTA-173: Augment the objective to make multi-epoch pretraining productive on a fixed corpus

## Source

Chen et al. (2026), [LIT-175](../literature.d/LIT-175.md) — [ARXIV-2606.16246](https://arxiv.org/abs/2606.16246).

The premise is the regime: compute capacity is outrunning the rate at which
new high-quality text is produced, so pretraining is moving to a
data-constrained, compute-abundant setting where multi-epoch training on a
fixed corpus has to be made *productive*.

The failure it starts from is unambiguous. Standard autoregressive
pretraining **overfits severely** in this setting — it reaches its optimum
early and then deteriorates continuously. Not a plateau; a decline.

## The three families, which are orthogonal

- **Token-level noise** — masking, random replacement. Random token
  replacement is the best single method.
- **Sequence permutations** — right-to-left prediction, fill-in-the-middle.
- **Target offset prediction** — predict x_{t+i} for i > 1.

Each individually delays overfitting and lowers validation loss against the
baseline; combining categories lowers the minimum further. The claim is
hundreds of productive epochs on the same data.

## The reframing is worth more than the recipe

The record now holds three positions on repetition and this is the third.
<!-- inactive-ok-block: SOTA-124 — Proposed, and named as one of the three
     positions this reframes -->
[SOTA-124](SOTA-124.md) says heavy repetition is safe when epoch size exceeds the
memorization window; [SOTA-171](SOTA-171.md) says four epochs and then diminishing
returns; this says repetition overfits severely **and the overfitting is a
property of the objective rather than of repetition**, removable with
augmentation.

That framing is the useful one, because it makes the other two falsifiable in
the same terms: if augmentation is what buys productive multi-epoch training,
then a recipe repeating a source a hundred times is either augmenting
implicitly or paying a cost nobody measured.

## Same transformation, three purposes

Fill-in-the-middle appears here as a *sequence-permutation augmentation*
valued for regularisation. [SOTA-174](SOTA-174.md) records it as a capability to be
trained for. And [LIT-119](../literature.d/LIT-119.md) reached for dropout when heavy repetition of a small
FIM corpus hurt HumanEval-FIM — the same corpus, the same transformation, and
a regularisation problem solved by a third mechanism. Three purposes for one
transformation, which is worth knowing before treating any one of them as the
reason it is in your pipeline.

## Conditions, and why this is Proposed

One group, one paper, published this year, and nothing in the record trains
under it. The augmentation families are also evaluated as delays to
overfitting rather than as end-of-training quality at a fixed budget, which
is the comparison a reader choosing between "augment" and "get more data"
would want.

## Known implementations

- None in the record.
