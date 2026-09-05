---
status: Active
title: 'DAPO: An Open-Source LLM Reinforcement Learning System at Scale'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-05'
published: '2025-03-01'
arxiv: '2503.14476'
first_author: 'Yu'
keywords:
- 'grpo'
- 'reinforcement-learning'
- 'clipping'
- 'dynamic-sampling'
- 'reproducibility'
implementations:
- DAPO
summary: >-
  Yu et al. (2025), [ARXIV-2503.14476](https://arxiv.org/abs/2503.14476). Decoupled Clip and Dynamic
  Sampling Policy Optimization, published with the four techniques, the code
  and the dataset — 50 points on AIME 2024 from a Qwen2.5-32B base.
---

# LIT-tmp90igr: DAPO: An Open-Source LLM Reinforcement Learning System at Scale

Yu et al. (2025) — [ARXIV-2503.14476](https://arxiv.org/abs/2503.14476)

## Key takeaways

- The stated motivation is reproducibility rather than novelty: the technical
  details of state-of-the-art reasoning models are concealed — the paper
  names the o1 blog post and the R1 report — so the community cannot
  reproduce the RL results even when the models are open.
- **DAPO** — Decoupled Clip and Dynamic Sampling Policy Optimization — is
  presented with the four techniques the authors say make large-scale LLM RL
  work, rather than as a single trick.
- 50 points on AIME 2024 from a Qwen2.5-32B base.
- Training code (on verl) and a curated dataset released with it, which is
  the part that makes the four techniques checkable.

## Standing in the anthology

One of the three GRPO variations the record now carries, each fixing a named
defect: the clipping and sampling behaviour here, the length bias in
[LIT-tmp8p6dy](LIT-tmp8p6dy.md), and the token-level importance ratio in [LIT-tmprxq6c](LIT-tmprxq6c.md).

Filed as a note rather than a practice. The record's RL practice is
[SOTA-129](../practices.d/SOTA-129.md)'s three-stage recipe, sourced to Olmo 3; whether GRPO's successors
warrant a practice of their own depends on whether the anthology wants to
carry RL algorithm choice as *practice*, and nothing does yet. What this
supplies meanwhile is the observation that "we ran GRPO" is
under-determined: three papers within a year each found a different defect
in it worth naming.
