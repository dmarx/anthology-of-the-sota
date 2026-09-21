---
number: 284
status: Proposed
formerly:
- SOTA-tmpkxz0v
promote_when: >-
  A run where the choice was made and paid off: candidate checkpoints from a
  real pre-training or mid-training run, selected by a coverage estimate and
  by validation cross-entropy, with the two selections carried through
  post-training and compared. A further demonstration that cross-entropy
  predicts downstream performance poorly is not it — that is the premise, and
  it is already established.
consensus: unreplicated
consensus_note: >-
  One paper, and a theoretical one. The premise it rests on — that a better
  next-token predictor does not guarantee a better post-trained model — is
  reported by several independent groups, and `SOTA-210` records a related
  effect on two. What nobody has done is use a coverage criterion to choose,
  so the recommendation has evidence for its motivation and none for itself.
title: 'Choose the checkpoint you post-train from by how much mass it puts on good rare responses, not by validation cross-entropy'
version: 1
tags:
- analysis-and-evaluation
- adaptation-and-tuning
date: '2026-09-21'
source:
- LIT-474
introduced_by:
- LIT-474
implementations: []
explained_by:
- THEORY-043
---

<!-- inactive-ok-file: THEORY-043 — Proposed, and the account this practice
     declares as its explanation. Both are Proposed on the same single
     theoretical source, which is the state being recorded -->

# SOTA-284: Choose the checkpoint you post-train from by how much mass it puts on good rare responses, not by validation cross-entropy

## Source

Chen, Huang, Golowich, Malladi, Block, Ash, Krishnamurthy and Foster (2025),
[LIT-474](../literature.d/LIT-474.md) — read as [NOTE-223](../notes.d/NOTE-223.md). Theory, with a
graph-reasoning task as illustration.

## The claim

When you have several candidates — training checkpoints, or hyperparameter
configurations — and you are going to post-train one of them with RL or run
Best-of-N on it, the standard criterion is validation cross-entropy. Do not
use it.

The reason is not that cross-entropy is noisy. It is that **cross-entropy and
what post-training needs are different quantities that come apart
systematically**, and the source shows them doing so during a single training
run: KL improves monotonically while the coverage profile *degrades*, and at
large `N` the coverage profile is the better predictor of Best-of-N
performance while cross-entropy can be anti-correlated with it.
[THEORY-043](../theory.d/THEORY-043.md) is why.

## What to do instead

Score candidates on **coverage**: how much probability mass each puts on
responses your downstream task would accept, weighted by how many samples you
will draw at test time. Then take the candidate that holds up worst-case
against the others — a tournament, minimizing the maximum empirical coverage
any rival achieves against it.

For a handful of candidates this is pairwise evaluation of an empirical
coverage statistic, and it comes with a guarantee maximum likelihood does not
have: it finds a good-coverage model **in the class** even when the data
distribution is not in the class. An improved variant removes an additive
penalty term at the cost of also estimating each candidate's coverage by
sampling generations from it.

If you are not going to implement a tournament, the cheap version of this
practice is the negative half: **do not let validation loss make the choice
alone**, and look at pass@k-style numbers on a downstream set instead —
which is [SOTA-210](SOTA-210.md)'s territory, and pass@k at `k = N` is an estimator
of the quantity this practice is about.

## Conditions

**Nobody has done this on a real run.** The source is a theory paper. Its
empirical content is two figures on a synthetic graph-reasoning task,
illustrating theorems. The selection procedure is proposed and analysed, not
evaluated against cross-entropy selection on anything a practitioner would
recognise.

**The quantity is not free to measure.** Coverage is not observable; what you
can compute is an empirical coverage statistic on a labelled downstream set,
and the improved tournament additionally needs generations sampled from every
candidate. Validation cross-entropy costs a forward pass. This does not.

**The theory is proved in a setting that is not language-model
pre-training.** Prompt/response formulation the authors describe as nearer to
supervised fine-tuning, realizability for the main theorem, autoregressive
linear models for the optimizer results.

**It is about Best-of-N, and RL by extension only.** Coverage is proved
necessary and sufficient for BoN. The step to RL is a cited empirical
regularity that BoN predicts post-RL performance, and the source says the
minimal conditions for RL are not known.

**Sequence-level, where reasoning wants answer-level.** For tasks that only
need the right answer, the relevant quantity is weaker than the one analysed —
so a candidate could be better than this criterion says.

## What not to take from it

Not "ignore cross-entropy". It upper-bounds coverage and it is the quantity
you can actually see. The narrower and correct reading is that its penalty for
mass the model never had is unbounded and accumulates with sequence length, so
the two criteria agree least on long-sequence tasks — which is where the
choice is being made.

Nor does any of this support a change of optimizer. The source proves that
globally normalized SGD achieves horizon-independent coverage and then
explicitly *speculates* that Adam may inherit the benefit, flagging that
Adam's per-coordinate normalization is a meaningful difference.
[SOTA-001](SOTA-001.md) is untouched.
