---
status: Proposed
consensus: unassessed
consensus_note: >-
  One paper, one group, and no reported adoption of the measurement by
  anybody. There is nothing to assess yet.
promote_when: >-
  A run in which the measurement changed a decision and the decision paid:
  someone computes the two quantities, predicts from them that a spectral
  optimizer will or will not help on their workload, and is right — ideally
  on a workload where the answer is *no*, since a diagnostic that only ever
  agrees with the current default is not doing work. What would not settle
  it: further confirmation that transformer activations have low stable
  rank, which is already proved at initialization and measured in training.
title: "Before adopting a spectral optimizer, measure the stable rank of each block's incoming activations against its gradient's nuclear rank"
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-tmpdw28d
introduced_by:
- LIT-tmpdw28d
implementations: []
summary: >-
  Davis and Drusvyatskiy (2025), [LIT-tmpdw28d](../literature.d/LIT-tmpdw28d.md) — the spectral step's
  one-step guarantee beats the Euclidean one by the ratio of gradient
  nuclear rank to incoming activation stable rank. Both are cheap to compute
  from a run you are already doing, and the paper never uses them to route.
explained_by:
- THEORY-tmp5iwhe
---

<!-- inactive-ok-file: THEORY-tmp5iwhe — Proposed, and filed in this same contribution as the account of this measurement -->
# SOTA-tmpybkk5: Before adopting a spectral optimizer, measure the stable rank of each block's incoming activations against its gradient's nuclear rank

## Source

Davis and Drusvyatskiy (2025), [LIT-tmpdw28d](../literature.d/LIT-tmpdw28d.md) —
[ARXIV-2512.04299](https://arxiv.org/abs/2512.04299), read as [NOTE-tmprnxym](../notes.d/NOTE-tmprnxym.md).
Accounted for by [THEORY-tmp5iwhe](../theory.d/THEORY-tmp5iwhe.md).

## What to measure

For each trainable matrix `W` that acts on an incoming feature matrix `X`,
compute two numbers:

| quantity | expression | what it says |
|---|---|---|
| stable rank of the input | `‖X‖_F² / ‖X‖_op²` | how many directions the incoming features actually occupy |
| nuclear rank of the gradient | `‖∇W‖_*² / ‖∇W‖_F²` | how spread out the gradient's singular values are |

A spectral update's guaranteed one-step decrease exceeds the Euclidean one
by their ratio, so the spectral step is favoured on the blocks where the
gradient's nuclear rank is the larger number. In a transformer the incoming
matrices are the token embeddings, the RMS-normalized hidden states entering
the attention projections, and the post-activations entering the second MLP
matrix.

Both quantities are norms of tensors a training step already materializes.
Neither needs an SVD: the Frobenius and nuclear norms are traces, and the
operator norm is a few power iterations.

## Why bother, if the answer is usually yes

Because "usually" is doing load-bearing work there and nobody has checked
where it stops. The paper proves transformer activations have low stable
rank at Gaussian initialization — bounded by the inverse frequency of the
most common token, around 20 for a Zipfian corpus, and preserved through
RMSNorm, attention and the MLP independently of width and sequence length —
and measures that it holds through a NanoGPT run. That is a strong prior
that a language model is in the favourable regime.

It is also a prior derived entirely from language. A workload whose inputs
are not Zipfian, or whose activations are deliberately spread — a
well-conditioned embedding table, a heavily regularized vision encoder,
anything with an orthogonality penalty — has no such guarantee, and the
measurement is what tells you which side you are on before you pay Muon's
overhead.

## Conditions

- **This is a measurement, not a routing rule.** The paper states the rule
  of thumb and does not run the ablation that would test it: spectral
  updates on the blocks that pass, Euclidean on the blocks that fail. Using
  the condition to *select* per block goes beyond the evidence, which is why
  the practice stops at measuring. [ADR-017](../decisions.d/ADR-017.md) is the reason the line is
  drawn here.
- **It compares bounds, not outcomes.** The inequality is between guaranteed
  one-step decreases. A better guarantee is not a demonstrated speed-up.
- **The propagation results are initialization-time**, under Gaussian
  weights. That they survive training is one measured run.
- **NanoGPT scale**, plus synthetic regression. Nothing at the scale where
  [SOTA-165](../practices.d/SOTA-165.md) and [SOTA-121](../practices.d/SOTA-121.md) are evidenced.
- **It does not replace the fair comparison.** [SOTA-165](../practices.d/SOTA-165.md) rests on ten
  optimizers tuned per-optimizer at four scales. This predicts which side of
  a comparison you are on; it does not excuse you from running one.

## Known implementations

- None reported. The measurement is stated in the paper and, as far as the
  record knows, has not been used as a decision procedure by anyone.
