---
status: Active
title: 'Understanding R1-Zero-Like Training: A Critical Perspective'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-05'
published: '2025-03-01'
arxiv: '2503.20783'
first_author: 'Liu'
keywords:
- 'grpo'
- 'reinforcement-learning'
- 'reasoning'
- 'optimization-bias'
- 'response-length'
implementations:
- Dr. GRPO
summary: >-
  Liu et al. (2025), [ARXIV-2503.20783](https://arxiv.org/abs/2503.20783). Two corrections to the R1-Zero
  story: the base model may already carry what looks like emergent reasoning,
  and GRPO has a length bias that inflates wrong answers. Dr. GRPO removes
  the bias.
---

# LIT-tmp8p6dy: Understanding R1-Zero-Like Training: A Critical Perspective

Liu et al. (2025) — [ARXIV-2503.20783](https://arxiv.org/abs/2503.20783)

## Key takeaways

- Splits R1-Zero-style training into its two components and examines each.
  On the **base model** side: DeepSeek-V3-Base already exhibits the "Aha
  moment" before any RL, and Qwen2.5 bases show strong reasoning even without
  a prompt template — which the authors read as pretraining bias. Some of
  what looked emergent under RL was already there.
- On the **RL** side: an optimization bias in GRPO that artificially inflates
  response length, and does so **especially for incorrect outputs**. That is
  a sharp finding, because "the model learned to think longer" is the usual
  reading of a length increase during RL, and here part of it is the
  objective rewarding verbosity on failures.
- **Dr. GRPO** removes the bias, improving token efficiency while holding
  reasoning performance — a cheaper model at the same accuracy rather than a
  better one.
- A minimalist R1-Zero recipe built on these findings reaches 43.3% on
  AIME 2024 with a 7B base.

## Standing in the anthology

<!-- inactive-ok: SOTA-130 — the Proposed practice this paper argues should stay Proposed -->
The corrective to [LIT-tmp6t0j4](LIT-tmp6t0j4.md), and the reason [SOTA-130](../practices.d/SOTA-130.md) should stay
*Proposed*: if part of the "emergence" is a property of the base model's
pretraining, then "run RLVR directly on the base" is a claim whose result
depends on which base, and the record has one data point per base.

It also belongs to a sequence on [LIT-127](LIT-127.md), which introduced GRPO. The
variations the record now holds each name a defect and fix it: Dr. GRPO the
length bias here, [LIT-tmp90igr](LIT-tmp90igr.md) the clipping and sampling behaviour, and
[LIT-tmprxq6c](LIT-tmprxq6c.md) the token-level importance ratio. GRPO is the practice's source
([LIT-119](LIT-119.md) runs it at 0.6B); this is the literature saying it is not the last
word.
