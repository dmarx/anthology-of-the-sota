---
status: 'Active'
title: 'Large Batch Optimization for Deep Learning: Training BERT in 76 minutes'
version: 1
tags:
- training-optimization
date: '2026-09-15'
published: '2019-04-01'
arxiv: '1904.00962'
first_author: 'You'
keywords:
- 'large-batch'
- 'layerwise-adaptation'
- 'lamb'
- 'bert'
implementations: []
summary: >-
  You et al. (2019), [ARXIV-1904.00962](https://arxiv.org/abs/1904.00962). LAMB: normalize each layer's update by
  the ratio of weight norm to update norm, which lets BERT train at batch size
  32k without per-batch-size retuning.
---
# LIT-tmp75er0: Large Batch Optimization for Deep Learning: Training BERT in 76 minutes

You et al. (2019) — [ARXIV-1904.00962](https://arxiv.org/abs/1904.00962)

## Key takeaways

The paper proposes LAMB (Layer-wise Adaptive Moments optimizer for Batch
training), a layerwise adaptive large-batch optimizer that combines per-
dimension Adam normalization with per-layer learning rate scaling. LAMB
enables scaling BERT pre-training batch size to 32K–64K without accuracy
loss, reducing training time from 3 days to 76 minutes.

- **Nonconvex convergence of simplified LAMB (Theorem 1).** For simplified
  LAMB (beta1=0, lambda=0) with appropriate step size, the algorithm
  converges to an epsilon-stationary point at rate O(1/sqrt(T)) with
  complexity depending on Lavg (average layer smoothness) rather than L_inf
  (global smoothness), which can be significantly smaller for networks with
  heterogeneous curvature.
  *Holds when:* L-smooth nonconvex objective; bounded gradient variance;
  beta1=0, lambda=0; step size chosen per theorem conditions.
- **Large-batch accuracy preservation (empirical).** LAMB maintains BERT
  SQuAD F1 >= 90.4 at batch sizes up to 32,768 (64x baseline), while AdamW
  degrades at batch size > 16K; LARS fails entirely on BERT at all batch
  sizes.
  *Holds when:* BERT-Large on SQuAD v1.1; TPUv3 hardware; mixed-batch
  training schedule.

## What the evidence does not cover

- Convergence theory only covers simplified LAMB (beta1=0, lambda=0); the
  general case with momentum and weight decay is left unproven.
- Scaling efficiency drops to ~76.7% at 64x hardware due to gradient
  communication overhead for BERT's 300M parameters.
- Mixed-batch training requires careful re-warmup tuning; decreasing batch
  size between phases risks optimization instability.
- Results are demonstrated primarily on TPUv3 hardware; behavior on GPU
  clusters with different interconnects may differ.

## Standing in the anthology

Read — the reading is [NOTE-tmpm5eod](../notes.d/NOTE-tmpm5eod.md). Arrived in the imported batch, which
brought in the batch-size line — how large a batch buys speed, and what it
costs.
