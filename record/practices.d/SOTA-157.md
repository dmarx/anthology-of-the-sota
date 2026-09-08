---
status: Proposed
formerly:
- SOTA-tmp704hb
promote_when: >-
  A pretraining report on a released model above 8B trained this way, or a
  controlled comparison at matched compute against an autoregressive baseline
  that got its own hyperparameter sweep, from a group other than this one.
  What would not move it: further capability demonstrations at 8B against
  published baseline numbers, which is what the evidence already is.
consensus: unreplicated
consensus_note: >-
  One group, one model. The field has not replied — which is not the same as
  agreeing, and not the same as the dispute `contested` describes. Every
  other practice in this record assumes the paradigm this one rejects, so
  the disagreement is wide and one-sided.
title: 'Train the language model as a masked diffusion model rather than autoregressively'
version: 1
tags:
- model-architecture
date: '2026-09-07'
published: '2025-02-01'
source:
# One paper, and it is the only evidence there is. The comparison it reports
# is against its own ARM baselines plus published LLaMA3 8B numbers — which
# is what promote_when is asking somebody else to redo.
- LIT-217
implementations:
- 'LLaDA 8B'
summary: >-
  Nie et al. (2025), [LIT-217](../literature.d/LIT-217.md) — hold the paradigm fixed (pretrain, then
  SFT) and swap only the factorization: a forward masking process and a
  reverse process predicting masked tokens, optimizing a likelihood lower
  bound. Competitive with LLaMA3 8B on in-context learning; past GPT-4o on
  reversal poem completion. Filed `Proposed` — one group, one model, 8B.
---

# SOTA-157: Train the language model as a masked diffusion model rather than autoregressively

## Source

Nie et al. (2025), [LIT-217](../literature.d/LIT-217.md) — [ARXIV-2502.09992](https://arxiv.org/abs/2502.09992).

What is being challenged is an identification rather than a benchmark. The
capabilities everyone attributes to LLMs — in-context learning, instruction
following, scalability — are routinely attributed to *autoregressive*
modelling specifically. LLaDA holds the surrounding paradigm fixed and swaps
only the factorization, which is what makes the result an argument about that
identification.

A forward process masks tokens; a reverse process, parameterized by a
Transformer, predicts them; training optimizes a lower bound on the
likelihood. It is a principled generative model rather than a denoising
heuristic, and that is what gives it probabilistic inference.

## Conditions, and what is not established

Reported: LLaDA 8B is competitive with LLaMA3 8B on in-context learning, and
after SFT shows instruction-following in multi-turn dialogue. It surpasses
GPT-4o on reversal poem completion — the sharpest result here, because it is
the one place where the change in factorization predicts the change in
behaviour in advance rather than after the fact.

The comparison is against **self-constructed ARM baselines** plus published
LLaMA3 numbers, and "comparable to our self-constructed ARM baselines" is the
honest form of the claim. This is a demonstration that the paradigm scales,
not a report that it wins, and one group has made it at one size.

## What adopting this would cost, which nobody has costed

Most of this registry is advice about training an autoregressive
transformer, and none of it says so. Under this practice the registry splits,
and the split has not been checked by anyone:

- **Carries over unchanged** — the optimizer and schedule material (AdamW's
  decoupled decay, µP, the peak-LR power law), the capacity material
  (mixture-of-experts routing and granularity), data packing. These are about
  optimization and capacity, not about the factorization.
- **Does not carry over** — fill-in-the-middle training, multi-token
  prediction, speculative decoding, KV-cache compression, and context
  extension by RoPE rescaling. Each exists *because* generation is
  left-to-right and cached; under a masked-diffusion decoder some are
  unnecessary and some are incoherent.

That sort is one reader's first pass and the boundary runs through the
attention material, where a practice can be about the cache or about the
pattern. It is recorded here because a recommendation whose adoption cost is
unknown should say so rather than imply the cost is zero.

## Known implementations

- LLaDA 8B. No frontier report in this record trains this way.
