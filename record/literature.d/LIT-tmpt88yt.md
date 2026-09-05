---
status: Active
title: 'Qwen3 Technical Report'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2025-05-01'
arxiv: '2505.09388'
first_author: 'Yang'
keywords:
- 'thinking-mode'
- 'thinking-budget'
- 'distillation'
- 'mixture-of-experts'
- 'multilingual'
implementations:
- Qwen3
summary: >-
  Yang et al. (2025), [ARXIV-2505.09388](https://arxiv.org/abs/2505.09388). Thinking and non-thinking modes
  unified in one model with a thinking budget the caller sets, plus
  flagship-to-small distillation; 0.6B to 235B, dense and MoE, 119 languages.
---

# LIT-tmpt88yt: Qwen3 Technical Report

Yang et al., Qwen Team (2025) — [ARXIV-2505.09388](https://arxiv.org/abs/2505.09388)

## Key takeaways

- Dense and MoE models from 0.6B to 235B in one family.
- The named innovation is **unifying thinking and non-thinking modes in a
  single model**, switchable by query or chat template — removing the need to
  keep a chat-optimised model and a dedicated reasoning model side by side,
  which was the standing arrangement.
- A **thinking budget**: the caller allocates inference compute per request,
  trading latency against quality by task. This is the mechanism that appears
  in the record a generation later as `reasoning_effort` on Qwen3.8-27B
  ([LIT-135](LIT-135.md)), defaulting to its deepest setting.
- Smaller models are built by **leveraging knowledge from the flagship**,
  which is presented as a substantial reduction in the compute needed to
  produce a competitive small model — the record's tiny-model half
  ([SOTA-123](../practices.d/SOTA-123.md)) argues the opposite route from scratch.
- Multilingual support from 29 to 119 languages. Apache 2.0 throughout.

## Standing in the anthology

The generation the Qwen line in the record descends from, and the missing
middle of it: [LIT-136](LIT-136.md) is Qwen3-Next's architecture, [LIT-135](LIT-135.md) is Qwen3.8-27B's
model card, [LIT-152](LIT-152.md) is the design report — and this is the report the whole
series is named after. It is also what GSPO ([LIT-tmprxq6c](LIT-tmprxq6c.md)) is credited with
improving.

Two things in it bear on practices the record holds. The thinking budget is
the origin of the control [LIT-135](LIT-135.md) documents, so the "over-thinks by default"
observation has a lineage. And flagship-to-small distillation is a direct
alternative to [SOTA-123](../practices.d/SOTA-123.md)'s claim that tiny specialists should be pretrained
from scratch on the target mixture — two roads to a small capable model,
with no comparison between them in the record.
