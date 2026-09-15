---
status: Active
title: 'MoEfication: Transformer Feed-forward Layers are Mixtures of Experts'
version: 1
tags:
- model-architecture
date: '2026-09-15'
published: '2021-10-05'
arxiv: '2110.01786'
first_author: 'Zhang'
keywords:
- 'mixture-of-experts'
- 'sparsity'
- 'feed-forward'
- 'interpretability'
summary: >-
  Zhang et al. (2021), [ARXIV-2110.01786](https://arxiv.org/abs/2110.01786). Most inputs activate only a tiny
  fraction of an FFN's neurons, and the neurons that fire together can be
  partitioned into experts with a router bolted on afterwards — the same
  parameters, conditionally used. 10–30% of FFN parameters per input retains
  over 95% of performance.
---

# LIT-tmpf6e0b: MoEfication: Transformer Feed-forward Layers are Mixtures of Experts

Zhang, Lin, Liu, Li et al. (2021) — [ARXIV-2110.01786](https://arxiv.org/abs/2110.01786)

## Key takeaways

- The observation the paper starts from: in a pre-trained transformer, **most
  inputs activate only a tiny ratio of an FFN's neurons.** The dense layer is
  dense in storage and sparse in use.
- MoEfication converts a trained dense model into a mixture-of-experts version
  **with the same parameters**, in two phases — split the FFN's parameters
  into functional partitions, then train routers to pick which partitions an
  input needs. No retraining of the parameters themselves.
- The result: conditionally using **10–30% of FFN parameters** retains **over
  95%** of original performance across models and downstream tasks, with a
  reported 2× inference speedup at 25%.
- The partition is not imposed. It is recovered from which neurons co-activate,
  which is what makes the title a claim rather than a method name: the
  mixture-of-experts structure was already in the dense layer.

## Key takeaways — what this does not say

- It is a post-hoc conversion of a trained model, evaluated on inference cost.
  Nothing here is a claim about training a sparse model from scratch, and the
  paper does not compare against one.
- The models are of their moment (2021, BERT- and T5-scale). The
  10–30% figure should be read as evidence that the structure exists, not as
  a number to expect at frontier scale.
