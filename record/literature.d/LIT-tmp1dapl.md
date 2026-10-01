---
status: Active
title: 'Language Models are Unsupervised Multitask Learners'
version: 1
tags:
- in-context-learning
- model-architecture
- model-stability
date: '2026-10-01'
# OpenAI technical report, never posted to arXiv and with no DOI, so a url:
# under the source field group (ADR-009). The PDF carries no date; this is
# the day OpenAI released it with the GPT-2 announcement.
published: '2019-02-14'
url: 'https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf'
first_author: 'Radford'
keywords:
- 'language-models'
- 'zero-shot'
- 'webtext'
- 'pre-layer-norm'
- 'residual-scaled-initialization'
implementations:
- 'GPT-2'
summary: >-
  Radford et al. (2019) — GPT-2. Language models trained on WebText begin to
  perform tasks zero-shot when conditioned on a suitable context, and the
  performance rises log-linearly with capacity up to the 1.5B model, which
  still underfits. Its §2.3 carries two architecture changes the field kept:
  layer norm moved to the input of each sub-block, and residual-layer weights
  scaled at initialization by 1/sqrt(N), N the number of residual layers, to
  account for accumulation on the residual path with depth.
---

# LIT-tmp1dapl: Language Models are Unsupervised Multitask Learners

Radford et al. (2019) — OpenAI technical report,
https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf

## Key takeaways

- **Zero-shot task transfer from language modelling alone.** Conditioned on
  a document and questions, the largest model reaches 55 F1 on CoQA, matching
  or exceeding three of four baselines without their 127,000+ training
  examples, and sets the state of the art on 7 of 8 language-modelling
  datasets zero-shot.
- **Capacity is the lever.** Four models from 117M to 1.5B parameters
  (12 to 48 layers); performance improves log-linearly with size across
  tasks, and all four still underfit WebText.
- **Two architecture changes in §2.3, stated without ablation.** Layer
  normalization moved to the input of each sub-block, as in a pre-activation
  ResNet, with one more after the final block; and "a modified
  initialization which accounts for the accumulation on the residual path
  with model depth": residual-layer weights scaled at initialization by
  `1/sqrt(N)`, where `N` is the number of residual layers. Everything else
  "largely follows" GPT, whose own report initialises all weights from
  `N(0, 0.02)`.

## Standing in the anthology

Filed as the origin of the depth-scaled residual initialization in
[SOTA-060](../practices.d/SOTA-060.md). It is the earliest statement of it the record can name, two
months before Child et al. ([LIT-225](LIT-225.md)) wrote the same factor as `1/sqrt(2N)`
with `N` counting blocks rather than residual layers. The paper gives the
reason but no measurement of what the scaling buys.
