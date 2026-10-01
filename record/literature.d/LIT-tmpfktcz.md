---
status: Active
title: 'Reducing Activation Recomputation in Large Transformer Models'
version: 1
tags:
- distributed-optimization
- systems-optimization
date: '2026-10-01'
published: '2022-05-10'
arxiv: '2205.05198'
first_author: 'Korthikanti'
keywords:
- 'sequence-parallelism'
- 'tensor-parallelism'
- 'selective-activation-recomputation'
- 'activation-memory'
- 'large-language-models'
implementations:
- 'Megatron-LM'
- 'NeMo-Megatron'
summary: >-
  Korthikanti et al. (2022), [ARXIV-2205.05198](https://arxiv.org/abs/2205.05198). Introduces sequence
  parallelism: the layer norms and dropouts that tensor parallelism leaves
  replicated are split along the sequence dimension, and the tensor-parallel
  all-reduces become an all-gather and a reduce-scatter that move the same
  bytes, so activation memory per layer falls by the tensor-parallel degree at
  no extra communication. With selective recomputation of the attention core
  it cuts activation memory about 5x, and over full recomputation lifts
  end-to-end throughput 29.0-32.1% on models from 22B to 1T parameters.
---

# LIT-tmpfktcz: Reducing Activation Recomputation in Large Transformer Models

Korthikanti et al. (2022) — [ARXIV-2205.05198](https://arxiv.org/abs/2205.05198)

## Key takeaways

- **Tensor parallelism leaves part of every layer replicated.** The layer
  norms and the dropouts after attention and the MLP are not split, so each
  rank stores them whole; in the paper's activation-memory formula that is
  the `10sbh` term that does not divide by the tensor-parallel size (§4.2.2).
- **Sequence parallelism splits those regions along the sequence
  dimension**, which they can be because the operations are independent
  across positions. The converters between the sequence-parallel and
  tensor-parallel regions are an all-gather and a reduce-scatter. A ring
  all-reduce *is* a reduce-scatter followed by an all-gather, so four
  all-gathers and four reduce-scatters per layer, forward and backward, use
  the same bandwidth as tensor parallelism's four all-reduces. Activation
  memory per layer becomes the unparallelised figure divided by the
  tensor-parallel size.
- **Measured, not only derived.** Sequence parallelism and selective
  recomputation each cut activation memory roughly in half; together about
  5x, to under 20% of the tensor-parallel baseline (§6.1). On one layer of a
  22B model, sequence parallelism alone takes the forward pass from 7.7 to
  7.2 ms, a 6% speedup, though reduce-scatter plus all-gather executes
  slower than one all-reduce despite moving the same data (§6.2).
- **Selective activation recomputation** stores everything except the
  attention core (`QK^T`, softmax, softmax dropout, attention over `V`),
  whose activations are large and whose FLOPs are few. Overhead falls from
  39% for full recomputation to 4% with both techniques on the 22B layer,
  and end-to-end throughput rises 29.0% (22B) to 32.1% (1T). The 530B model
  on 2240 A100s reaches 54.2% MFU against 42.1% with full recomputation.
- One training-side communication overlap is in the method itself: the
  sequence-split input to the first linear layer is all-gathered again in the
  backward pass, and that all-gather is overlapped with the weight-gradient
  computation.

## Standing in the anthology

Filed as the source and origin of [SOTA-058](../practices.d/SOTA-058.md), which had pointed at
[LIT-043](LIT-043.md), a paper that never mentions sequence parallelism. The paper
credits an earlier, different "sequence parallelism" (Li et al., 2021) that
partitions activations along the sequence throughout the network but
replicates parameters and optimizer state on every device; the scheme that
interlocks with tensor parallelism is this one.
