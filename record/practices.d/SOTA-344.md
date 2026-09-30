---
number: 344
status: Proposed
formerly:
- SOTA-tmpmnhef
promote_when: >-
  An independent comparison at scale, not from the TopK authors, of TopK
  against the current alternatives (JumpReLU, BatchTopK and Gated),
  showing TopK's reconstruction and downstream-loss advantage over L1-ReLU
  holds with dead-latent mitigation applied to every arm. The source's
  comparisons are one lab's, and later architectures have moved on.
title: 'Train sparse autoencoders with a TopK activation instead of an L1 penalty, and prevent dead latents with transposed-decoder initialization and an auxiliary loss'
version: 1
tags:
- analysis-and-evaluation
- concept-geometry
date: '2026-09-23'
source:
- LIT-571
introduced_by:
- LIT-571
consensus: unassessed
consensus_note: >-
  TopK and its batch variant are used in public SAE suites (Llama Scope is
  TopK). JumpReLU (Gemma Scope) is the main alternative. Which is preferred
  now has not been assessed here.
implementations:
- openai/sparse_autoencoder
summary: >-
  Gao et al. (2024), [LIT-571](../literature.d/LIT-571.md) — keep the k largest pre-activations and
  zero the rest, and train on reconstruction alone. L0 is then set, not
  tuned through an L1 coefficient that also shrinks the latents that fire.
  It beats ReLU SAEs on the MSE–L0 frontier by more as SAEs grow. Initialize
  the encoder as the decoder's transpose and add a loss reconstructing the
  residual from dead latents: 7% dead at 16M latents, against up to 90%.
---

# SOTA-344: Train sparse autoencoders with a TopK activation instead of an L1 penalty, and prevent dead latents with transposed-decoder initialization and an auxiliary loss

## Source

Gao et al. (2024), [LIT-571](../literature.d/LIT-571.md). Read as [NOTE-307](../notes.d/NOTE-307.md).

## The practice

If you train an SAE on a model's activations:

- **Use TopK for sparsity.** `z = TopK(W_enc(x − b_pre))`, loss = MSE.
  Choose k as the L0 you want. There is no L1 coefficient to sweep, and
  runs at different sizes compare at identical sparsity
- **Initialize the encoder to the decoder's transpose**
- **Add the auxiliary dead-latent loss:** reconstruct the current error from
  the top-k_aux latents that have not fired recently. Together with the
  initialization, this is what took dead latents from up to 90% to 7%
- **Scale the learning rate as 1/√(latents)**, the largest that converged
  in the paper

## Conditions

- **This says how to train an SAE, not whether to use one.** On probing,
  SAE latents do not beat raw activations ([LIT-568](../literature.d/LIT-568.md), [SOTA-345](SOTA-345.md))
- **Fixed per-token L0 is a known weakness.** The authors suggest
  constraining the expected L0 instead, which BatchTopK does
