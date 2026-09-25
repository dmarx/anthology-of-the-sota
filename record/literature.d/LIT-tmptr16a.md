---
status: Active
title: 'Simple and Effective Masked Diffusion Language Models'
version: 1
tags:
- generative-modeling
- training-optimization
- inference-optimization
- adaptation-and-tuning
- biomolecular-modeling
date: '2026-09-25'
published: '2024-06-01'
arxiv: '2406.07524'
first_author: 'Sahoo'
compared_against:
- LIT-tmpfb0m4
- LIT-479
keywords:
- 'masked-diffusion'
- 'absorbing-state'
- 'rao-blackwellization'
- 'SUBS-parameterization'
- 'semi-autoregressive-decoding'
- 'discrete-diffusion'
implementations:
- 'kuleshov-group/mdlm'
summary: >-
  Sahoo et al. (2024), [ARXIV-2406.07524](https://arxiv.org/abs/2406.07524). MDLM: the masked-diffusion
  training objective reduces to a weighted average of BERT-style masked-LM
  losses, a continuous-time ELBO whose value is invariant to the noise
  schedule. It is the strongest discrete diffusion language model at its
  scale — beating SEDD at matched tokens — and still trails a retrained
  autoregressive baseline in-domain (LM1B 27.04 vs 22.32; OWT 23.21 vs
  17.54), which the authors state as the limitation.
---

<!-- inactive-ok-file: SOTA-157 — Proposed, and named as the practice this paper is now a corroborating source of, for the *masked* in its title and not for the *rather than autoregressively* -->
<!-- inactive-ok-file: SOTA-254 — Proposed, and named to say this paper is NOT a source of it: nothing here varies the unique-token count -->

# LIT-tmptr16a: Simple and Effective Masked Diffusion Language Models

Sahoo et al. (2024) — [ARXIV-2406.07524](https://arxiv.org/abs/2406.07524)

## Key takeaways

- **The objective is a mixture of masked-LM losses.** Restricting discrete
  diffusion to the absorbing (`[MASK]`) process and parameterizing the
  reverse step so that the mask logit is `−∞` and unmasked tokens are copied
  through ("SUBS") collapses the D3PM ELBO to
  `∫ α'_t/(1−α_t) · Σ_ℓ log⟨x_θ(z_t), x^ℓ⟩ dt` — cross-entropy on the
  masked positions, weighted by the schedule. This is the objective later
  masked-diffusion language models train with. Two concurrent papers (Shi et
  al., Ou et al.) derived the same simplification.
- **The schedule does not change the bound, only its variance.** A change of
  variables removes `α_t` from the continuous-time NELBO; four schedules give
  the same 3.30 BPD on OWT, with per-datapoint variance from 1.81 (log-linear)
  to 7.57 (linear).
- **Most of the gain over earlier masked diffusion is engineering.** The
  authors' own ranking: of SUBS, the simplified objective and a modern
  training recipe (tokenizer, DiT with RoPE, numerically stable loss,
  low-discrepancy time sampling), *"(3) has the largest contribution to
  performance."* Their re-implementation of D3PM's objective reaches 28.51 on
  LM1B where the published D3PM number is 76.90 (at 70M parameters, against
  110M here, so not all of the gap is recipe); the full MDLM objective is
  27.04. The derivation buys about 1.5 perplexity points, nearly all of it
  from carry-over unmasking; the recipe and the larger model buy the rest.
- **Against SEDD at matched training**, MDLM wins on every likelihood table:
  LM1B 27.04 vs 32.79 (33B tokens), OWT 23.21 vs 24.10 (SEDD retrained), 7/7
  zero-shot sets, and DNA 3.199 vs 3.216.
- **Against autoregression it loses in-domain.** Retrained AR with the same
  backbone: LM1B 22.32 vs 27.04 at 33B tokens and 20.86 vs 23.00 at 327B;
  OWT 17.54 vs 23.21. Zero-shot from OWT it beats AR on 3 of 7 sets (Lambada,
  Pubmed, Arxiv), which the authors explain only by hypothesis.
- **Encoders become generators cheaply.** Fine-tuning a pretrained BERT with
  the MDLM objective for 327M tokens takes its C4 perplexity bound from 78 to
  35 with no loss on GLUE (81.62 → 82.06); AR is at 22.

## The denominator the comparison uses

"Matched tokens" here counts only the *masked* tokens a diffusion model is
scored on — half of each sequence in expectation under the log-linear
schedule. So the AR baselines were trained for **half the optimizer steps**
(0.5M against 1M on OWT; 0.5M/5M against 1M/10M on LM1B), and MDLM processed
twice the raw tokens. Every "MDLM approaches AR" number carries that factor
in diffusion's favour, and AR still wins in-domain. No hyperparameter sweep
was run for either arm: constant learning rate 3e-4, the SEDD backbone,
110M parameters.

## Standing in the anthology

The leading masked-diffusion language model paper, filed because the record
recommended the family without holding it (curation entry of 2026-09-21).
It is a corroborating source of [SOTA-157](../practices.d/SOTA-157.md) **for the choice of masked
over other discrete diffusion processes** — where it is controlled and
consistent — and not for preferring diffusion to autoregression, where its
own controlled comparison goes the other way at 110M parameters. It is not a
source of [SOTA-254](../practices.d/SOTA-254.md): nothing here varies unique data, though the LM1B gap
to AR narrowing from 4.7 to 2.1 points between 33B and 327B tokens is the
direction that practice predicts. [LIT-479](LIT-479.md) measures against it and finds it
still ahead of uniform-state diffusion on likelihood.
