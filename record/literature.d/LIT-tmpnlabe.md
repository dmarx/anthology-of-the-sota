---
status: Active
title: 'Large Language Diffusion Models'
version: 1
tags:
- generative-modeling
date: '2026-09-07'
published: '2025-02-01'
arxiv: '2502.09992'
first_author: 'Nie'
keywords:
- 'diffusion-language-model'
- 'masked-diffusion'
- 'autoregressive'
- 'reversal-curse'
- 'likelihood-lower-bound'
implementations:
- 'LLaDA 8B'
summary: >-
  Nie et al. (2025), [ARXIV-2502.09992](https://arxiv.org/abs/2502.09992). LLaDA: an 8B language model
  trained from scratch under the ordinary pretrain-then-SFT paradigm, with
  the autoregressive factorization replaced by masked diffusion — a forward
  masking process and a reverse process that predicts masked tokens,
  optimizing a likelihood lower bound. Competitive with LLaMA3 8B on
  in-context learning, and beats GPT-4o on reversal poem completion.
---

# LIT-tmpnlabe: Large Language Diffusion Models

Nie et al. (2025) — [ARXIV-2502.09992](https://arxiv.org/abs/2502.09992)

## Key takeaways

**What is being challenged is an identification, not a benchmark.** The
capabilities everyone attributes to LLMs — in-context learning, instruction
following, scalability — are routinely attributed to *autoregressive*
modelling specifically. LLaDA holds the paradigm fixed (pretrain, then SFT)
and swaps only the factorization, which is what makes the comparison an
argument about that identification rather than about a model.

**The mechanism.** A forward process masks tokens; a reverse process,
parameterized by a Transformer, predicts them. Training optimizes a lower
bound on the likelihood, so it is a principled generative model rather than
a denoising heuristic — the paper is explicit that this is what gives it
probabilistic inference.

**The reversal-curse result is the sharpest one.** Autoregressive models
trained on "A is B" notoriously fail at "B is A". LLaDA surpasses GPT-4o on
reversal poem completion. That is a small task, and it is the one place where
the difference in factorization predicts the difference in behaviour in
advance — which makes it evidence about the mechanism rather than about
scale.

**The comparison is against self-constructed ARM baselines**, plus published
LLaMA3 8B numbers. "Comparable to our self-constructed ARM baselines" is the
honest form of the claim and should be read as written: this is a
demonstration that the paradigm scales, not a report that it wins.

## Standing in the anthology

**It is the assumption under the whole registry, named.** Every practice in
this record — schedules, optimizers, sparsity, attention variants, context
extension, the RL post-training spine — is advice about training an
autoregressive transformer. None of them says so, because nothing in the
record has ever needed the qualifier. LLaDA is why the qualifier now exists
to be written.

Some of the registry would survive the swap untouched: AdamW and its
decoupled decay, µP, warmup-stable-decay, mixture-of-experts routing and data
packing are about optimization and capacity, not about the factorization.
Others are load-bearing on it — fill-in-the-middle training, multi-token
prediction, speculative decoding and KV-cache compression all exist because
generation is left-to-right and cached. Which practices sit on which side is
a real question the record has never had to answer.

**Not a practice, and it is not close.** No frontier report in this record
trains a diffusion language model, and LLaDA at 8B against 8B baselines does
not establish that one should. What would change it: a frontier-scale
diffusion language model with a disclosed recipe, or a controlled comparison
at matched compute with both arms tuned — the same standard the schedule
material is held to.
