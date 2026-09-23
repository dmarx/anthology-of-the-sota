---
status: Read
paper: LIT-tmpydijh
title: 'Scaling and evaluating sparse autoencoders'
version: 1
date: '2026-09-23'
summary: >-
  TopK SAEs, a dead-latent recipe, and scaling laws, demonstrated on a
  16M-latent SAE on GPT-4. Also shows that the field's usual fidelity metric
  flatters. Sections 1–4 and 6 read. Section 5 (TopK variants, progressive
  codes) and the appendices skimmed.
---

# NOTE-tmpr5ct1: Scaling and evaluating sparse autoencoders

## Contribution

A recipe that makes very large SAEs trainable without per-run tuning of
an L1 coefficient, and without most latents dying. Scaling laws for it,
and a set of evaluation metrics beyond reconstruction.

## Key insight

**Set the sparsity you want instead of penalizing its proxy.** L1 is an
imperfect stand-in for L0, and it shrinks the latents that do fire. TopK
fixes L0 exactly, so reconstruction is the only loss, and comparisons across
sizes are at matched sparsity.

## Key results

- TopK beats ReLU and ProLU and matches Gated on the MSE–L0 frontier at 32k
  latents, and scales more steeply at fixed L0 = 128 (Figure 2). The
  downstream-loss gap is larger than the MSE gap (Figure 5a)
- Without mitigation, up to 90% of latents die. With encoder = decoderᵀ
  initialization and the auxiliary loss, 7% die in the 16M SAE
- MSE follows `L(C) = 0.09 + 0.056 C^0.084` in compute, as a fraction of
  GPT-4 pretraining (Figure 1)
- **Fidelity:** the 16M SAE's "loss recovered" against zero ablation is
  98.2%. Its language-modeling loss, substituted into GPT-4, equals that of a
  model trained on 10% of GPT-4's compute

## Limitations

- **All metrics are proxies**, as §6 says. None shows the SAE doing a task
  better than an alternative that does not use it (see [LIT-tmp57c8v](../literature.d/LIT-tmp57c8v.md))
- **TopK fixes L0 per token**, which the authors think is suboptimal.
  BatchTopK and other variants followed
- **Many GPT-4 latents are not interpretable** in random activating
  examples (§6)
- One lab's models, and mostly its own SAEs
