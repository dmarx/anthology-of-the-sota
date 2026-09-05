---
status: Active
title: 'The Llama 3 Herd of Models'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2024-07-01'
arxiv: '2407.21783'
first_author: 'Grattafiori'
keywords:
- 'dense-transformer'
- 'pretraining-recipe'
- 'long-context'
- 'multimodality'
- 'open-weights'
implementations:
- Llama 3
summary: >-
  Grattafiori et al. (2024), [ARXIV-2407.21783](https://arxiv.org/abs/2407.21783). The period's most-cited
  dense recipe, published at length: a 405B dense Transformer at 128K
  context, with the empirical evaluation and the compositional route to
  image, video and speech.
---

# LIT-tmprh4f9: The Llama 3 Herd of Models

Grattafiori et al., Meta (2024) — [ARXIV-2407.21783](https://arxiv.org/abs/2407.21783)

## Key takeaways

- A **dense** Transformer at 405B with a 128K context window — notable in a
  record whose recent half is entirely mixture-of-experts, and a useful
  control: this is what the same era looks like without sparsity.
- Native multilinguality, coding, reasoning and tool use, delivering quality
  comparable to the leading closed models of the time on a wide evaluation.
- Released with pre-trained and post-trained weights at 405B, plus Llama
  Guard 3 for input and output safety.
- Image, video and speech are integrated **compositionally** rather than
  natively — a contrast with the record's 2026 entries ([LIT-131](LIT-131.md), [LIT-135](LIT-135.md)),
  which build vision into the backbone.
- Its length is the point: the report is one of the few complete accounts of
  a frontier-scale dense recipe, which is why nearly every later paper in the
  corpus benchmarks against it or trains on top of it.

## Standing in the anthology

Filed as the dense baseline the record's other entries are implicitly
measured against, and as a dependency several already have: Tulu 3
([LIT-tmpg34u1](LIT-tmpg34u1.md)) post-trains Llama 3.1 bases, and Nemotron-CC ([LIT-tmpqhulf](LIT-tmpqhulf.md))
defines its long-horizon target by beating Llama 3.1 8B at 15T tokens.

No practice is drawn from it. That is deliberate rather than an omission:
the report is a recipe in the sense of a complete account, not in the sense
of a transferable recommendation with an ablation behind it, and this
anthology sources practices to the paper that isolated a change.
