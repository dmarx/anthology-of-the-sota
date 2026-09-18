---
status: Active
title: 'Quantizable Transformers: Removing Outliers by Helping Attention Heads Do Nothing'
version: 1
tags:
- attention-techniques
date: '2026-09-17'
published: '2023-06-01'
arxiv: '2306.12929'
first_author: 'Bondarenko'
keywords:
- 'quantization'
- 'activation-outliers'
- 'clipped-softmax'
- 'gated-attention'
- 'no-op-attention'
implementations: []
summary: >-
  Bondarenko et al. (2023), [ARXIV-2306.12929](https://arxiv.org/abs/2306.12929), NeurIPS 2023. The diagnosis the
  attention-sink literature rests on, and two architectural fixes with the
  experiment attached. A head trying to learn a no-op must drive its softmax
  input ever larger to approximate exact zeros, which is what creates the
  outliers that break quantization. Clipped softmax and gated attention each
  remove them: BERT-base goes from 1294 W8A8 perplexity to 4.55, with max
  infinity-norm from 735 to 20. **Its gated attention is a per-head sigmoid on
  the attention output — the recommendation SOTA-134 makes, two years
  earlier**, as Qiu et al. themselves say.
---

# LIT-tmpfe659: Quantizable Transformers: Removing Outliers by Helping Attention Heads Do Nothing

Bondarenko et al., Qualcomm AI Research (2023) — [ARXIV-2306.12929](https://arxiv.org/abs/2306.12929), NeurIPS 2023

## Key takeaways

- **The diagnosis, and it is the mechanical version of the attention-sink
  account.** Strong activation outliers come from heads trying to learn a
  *no-op* — a null or partial update to the residual. Getting the exact zeros
  in the attention matrix that a no-op requires means pushing the softmax
  input larger and larger during training, and that is what produces outliers
  elsewhere in the network. Tokens such as `[SEP]`, periods and commas are
  where the no-op lands.

- **Fix one: clipped softmax.** Stretch the softmax output from `(0,1)` to
  `(γ, ζ)` with `γ ≤ 0 ≤ 1 ≤ ζ`, then clip back to `(0,1)`, so exact zeros and
  ones are reachable from a *finite* input range. Clipped values also carry no
  gradient, so the outliers stop being driven further.

- **Fix two: gated attention, and this is the one the record needs.**
  `Gated_attention(x) := sigmoid(G(x)) ⊙ softmax(QKᵀ/√d_head) V(x)`, with `G`
  defined **on a per-head basis** — "gating modules are shared between
  different token positions but not shared across attention heads" — as a
  single linear layer, costing `n_heads·(d_head+1) ≈ d_model` extra parameters
  per attention layer, under 0.009% of BERT-base.

- **The numbers, on BERT-base.** Vanilla: FP16 perplexity 4.49, max
  infinity-norm 735, average kurtosis 3076, and **W8A8 perplexity 1294±1046**
  — quantization simply breaks. With clipped softmax at `γ = −0.03`: FP16
  **4.41**, infinity-norm **20**, kurtosis **80**, W8A8 **4.55±0.01**. The
  floating-point model gets slightly *better* while INT8 goes from unusable to
  usable.

- **Scope of the evidence.** BERT-base (109M), OPT-125M, ViT-S/16 on
  ImageNet-1K. Small models by current standards, and encoder-heavy. Each
  network trained twice and each PTQ run three times, with means and standard
  deviations reported.

- **Clipped softmax is the more consistent of the two here.** On the summary
  comparison clipped softmax reaches 4.39±0.00 with outlier metrics 21.5±1.5
  and 80±6, where gated attention reaches 4.45±0.03 with 39.2±26.0 and
  201±181 — the same idea, much higher variance.

## Standing in the anthology

**It changes an attribution the record already made.**
[SOTA-134](../practices.d/SOTA-134.md) recommends gating each attention head's
output with a sigmoid after the scaled dot-product, and was filed with
`introduced_by: LIT-138` — Qiu et al. (2025). That is equation 5 of this
paper, per-head, two years earlier. Qiu et al. say so themselves:

> The work most closely related to ours is Quantizable Transformers
> (Bondarenko et al., 2023), which also finds that applying gating in softmax
> attention alleviates extreme attention concentration and outliers in hidden
> states in encoder models like BERT and ViT. While this work primarily
> leverages gating to eliminate outliers for model quantization, we provide a
> detailed analysis of various gating variants ... Building on these insights,
> we scale up gated attention models.

So the origin is here and the evidence at scale is theirs — which is exactly
the split [ADR-017](../decisions.d/ADR-017.md) draws, and the practice now
records it that way.

It is also the paper [LIT-191](LIT-191.md) gestures at when it says the same
argument had been made for quantization outliers. The record held the gesture
and not the paper.
