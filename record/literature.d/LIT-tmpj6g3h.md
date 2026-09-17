---
status: 'Active'
title: 'Scaling Diffusion Language Models via Adaptation from Autoregressive Models'
version: 1
tags:
- generative-modeling
- adaptation-and-tuning
date: '2026-09-17'
published: '2024-10-23'
arxiv: '2410.17891'
first_author: 'Gong'
keywords:
- 'diffusion-language-models'
- 'continual-pretraining'
- 'model-conversion'
- 'infilling'
implementations:
- 'DiffuGPT'
- 'DiffuLLaMA'
summary: >-
  Gong et al. (2024), [ARXIV-2410.17891](https://arxiv.org/abs/2410.17891). Diffusion language models are hard
  to train from scratch at scale and there are a great many trained
  autoregressive ones, so convert instead: continual pretraining on under
  200B tokens turns GPT2 and LLaMA at 127M–7B into DiffuGPT and DiffuLLaMA.
  The conversion rests on a stated connection between the AR and diffusion
  objectives rather than on the two being retrained independently.
---

# LIT-tmpj6g3h: Scaling Diffusion Language Models via Adaptation from Autoregressive Models

<!-- inactive-ok-file: SOTA-157 — Proposed, and named as the OTHER branch of this same decision; the pairing is the content -->
<!-- inactive-ok-file: SOTA-tmp5nzpk — Proposed, and filed in this same contribution as the practice this note sources -->

Gong et al. (2024) — [ARXIV-2410.17891](https://arxiv.org/abs/2410.17891)

## Key takeaways

- **The premise is an asymmetry of supply.** Diffusion language models have
  been studied at smaller scale than autoregressive ones and training them
  from scratch at scale is hard; open-weight AR models are abundant. So adapt
  what exists.
- **Continual pretraining, under 200B tokens**, converting GPT2 and LLaMA
  across 127M–7B into DiffuGPT and DiffuLLaMA.
- The method rests on **connections between the AR and diffusion objectives**,
  which is what makes this a conversion rather than a re-initialisation with
  extra steps.
- Resulting models outperform earlier diffusion language models and are
  **competitive with their AR counterparts**, on language modeling, reasoning
  and commonsense benchmarks.
- The capability that justifies the exercise: **filling in the middle without
  prompt re-ordering**, plus in-context learning and instruction following.
  Infilling is the thing an AR model structurally cannot do well, so it is
  the payoff for changing paradigm rather than a bonus.

## Standing in the anthology

Sources [SOTA-tmp5nzpk](../practices.d/SOTA-tmp5nzpk.md), and pairs with something the record already
holds. [SOTA-157](../practices.d/SOTA-157.md) records the other route — train as a masked diffusion model
from the start, from [LIT-217](LIT-217.md) (LLaDA). This is the same choice met from the
other side: keep the autoregressive pretraining and convert afterwards.

That pairing is an instance of a shape this record meets repeatedly: **build
it that way from scratch, or adapt an artifact you already have.**
Quantization has it — [SOTA-163](../practices.d/SOTA-163.md) and [SOTA-185](../practices.d/SOTA-185.md) compress a finished model,
and the ternary line trains in the target format instead. Adaptation has it —
[SOTA-123](../practices.d/SOTA-123.md) pretrains a tiny model from scratch on the target distribution
rather than fine-tuning one. The record has no document naming that shape,
which is what [DP-007](../principles.d/DP-007.md) predicts of a pattern everybody uses and nobody
introduced.
