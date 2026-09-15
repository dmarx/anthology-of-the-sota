---
status: Active
title: 'Sparse Upcycling: Training Mixture-of-Experts from Dense Checkpoints'
version: 1
tags:
- model-architecture
date: '2026-09-15'
published: '2022-12-09'
arxiv: '2212.05055'
first_author: 'Komatsuzaki'
keywords:
- 'mixture-of-experts'
- 'initialization'
- 'transfer'
- 'training-efficiency'
summary: >-
  Komatsuzaki et al. (2022), [ARXIV-2212.05055](https://arxiv.org/abs/2212.05055). Initialize a
  mixture-of-experts model from a dense checkpoint instead of from scratch.
  Upcycled T5 and ViT models beat their dense counterparts using ~50% of the
  dense pretraining sunk cost, and beat MoE models trained from scratch on
  100% of it.
---

# LIT-tmpolljg: Sparse Upcycling: Training Mixture-of-Experts from Dense Checkpoints

Komatsuzaki, Puigcerver, Lee-Thorp, Riquelme Ruiz et al. (2022) — [ARXIV-2212.05055](https://arxiv.org/abs/2212.05055)

## Key takeaways

- The problem: sparsely activated models decouple size from per-token cost,
  but "remain data-hungry and costly to train from scratch in the large scale
  regime". The dense checkpoints everyone already has are sunk cost.
- **Sparse upcycling** initializes an MoE from a dense checkpoint — the dense
  FFN's weights seed the experts — rather than starting over.
- The two comparisons, and the second is the one that matters:
  - Upcycled T5 Base/Large/XL and ViT Base/Large **beat their dense
    counterparts** on SuperGLUE and ImageNet using **~50%** of the initial
    dense pretraining sunk cost.
  - They also **beat sparse models trained from scratch on 100%** of that
    same budget. Same architecture, same compute, different initialization.

## Key takeaways — what this does not say

- The scales are T5 and ViT, 2022. It is not a frontier-scale result, and it
  does not report where the advantage goes as the post-upcycling budget grows
  — which is the question a lab deciding between the two would actually ask.
- It does not explain *why* the dense initialization helps. The paper offers a
  procedure and a comparison; the account is somebody else's to give.
