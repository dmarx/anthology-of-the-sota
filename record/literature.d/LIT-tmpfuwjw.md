---
status: Active
title: 'Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2024-08-01'
arxiv: '2408.15664'
first_author: 'Wang'
keywords:
- 'mixture-of-experts'
- 'load-balancing'
- 'routing'
- 'auxiliary-loss'
- 'expert-bias'
implementations:
- Loss-Free Balancing
summary: >-
  Wang et al. (2024), [ARXIV-2408.15664](https://arxiv.org/abs/2408.15664). Balance expert load with a bias
  added to the routing scores and updated from recent load, instead of with
  an auxiliary loss whose gradients interfere with the objective you care
  about.
---

# LIT-tmpfuwjw: Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts

Wang et al., DeepSeek-AI (2024) — [ARXIV-2408.15664](https://arxiv.org/abs/2408.15664)

## Key takeaways

- The bind: an unbalanced expert load causes routing collapse or wasted
  compute, so everyone adds an auxiliary loss to encourage balance — and a
  large enough auxiliary loss injects **interference gradients** that damage
  the model. Balance and quality are traded against each other through a
  coefficient nobody can set correctly.
- **Loss-Free Balancing** takes the balancing out of the gradient entirely:
  before the top-K decision, add a per-expert **bias** to the routing scores,
  and update each bias dynamically from that expert's recent load. Routing
  changes; the loss does not.
- Because no interference gradient is produced, it raises the ceiling on what
  MoE training can reach, rather than merely trading less quality for more
  balance.
- Validated up to 3B parameters and 200B tokens: better performance *and*
  better balance than auxiliary-loss control.

## Standing in the anthology

A candidate practice the record has not drawn, and worth flagging as such.
This is a clean, transferable recommendation — control load with a bias, not
a loss — with a mechanism, an ablation and adoption at 671B ([LIT-tmp0brdl](LIT-tmp0brdl.md))
and beyond. What stops it becoming a `SOTA` document is that the anthology
carries no MoE practices at all, so it would arrive without the context that
makes it meaningful.

That is the open question [#17](https://github.com/dmarx/anthology-of-the-sota/issues/17) names and this note is the sharpest case for
resolving it: the corpus now holds the fine-grained-plus-shared architecture
([LIT-tmpe49t1](LIT-tmpe49t1.md)), the load-balancing fix here, and RL that is unstable on MoE
specifically ([LIT-tmprxq6c](LIT-tmprxq6c.md)) — three practices' worth of material with nowhere
to sit.
