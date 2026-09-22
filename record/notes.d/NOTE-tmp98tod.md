---
status: Read
paper: LIT-tmp7xt7l
title: 'MatFormer'
version: 1
date: '2026-09-22'
summary: >-
  One Transformer with four nested FFN widths, trained one width per step,
  gives four sizes plus Mix'n'Match sizes nobody trained. At the compute of
  training the four separately, it matches the largest and beats the
  smaller ones, which see up to 4× the data through shared weights. Read
  §1–5 and Appendices B, D.1, E.1 and F.
---

<!-- inactive-ok-file: SOTA-tmpgvgkf — Proposed, filed in this same contribution from this paper; new, not retired, and cited as the practice this document sources -->

# NOTE-tmp98tod: MatFormer

## Contribution

A way to get a model *family* from one training run without distillation
or pruning afterwards. The nesting is simple: the first `m` FFN neurons. The
contribution is the training rule (sample one size per step, not all four)
and the observation that sizes never trained, assembled layer by layer, fall
on the curve between the trained ones.

## Key insight

**Order the neurons by importance during training, and truncation becomes a
model.** A smaller granularity's neurons are shared by every larger one, so
they receive gradient from every step and become the most important.
Removing the tail of each FFN then degrades the model gracefully. The same
idea applied to a representation vector is Matryoshka Representation
Learning.

## Assumptions

- **Decoder LMs from 78M to 850M, 16 layers**, trained at a fixed
  tokens-to-parameters ratio (10B–80B tokens per granularity), 1024 context,
  256k SentencePiece vocabulary, 1M-token batches
- **Only FFN width is nested** in the main results. Depth, attention and
  `d_model` are fixed across granularities
- **Uniform sampling of granularities.** Appendix F.3 finds that tuning the
  distribution gives stronger submodels
- **The comparison budget is the family's.** MatLM uses `4X` tokens, the
  same total as four baselines at `X` each

## Key results

- **850M MatLM (Figure 2):** every trained granularity has lower
  validation loss and higher 1-shot accuracy (25 tasks) than its baseline.
  Appendix B.4 says the larger granularity "match[es] in performance" and
  the smaller ones "outperform Baseline by a large margin"
- **Mix'n'Match:** at 55% of XL's compute, a Mix'n'Match model loses about
  1% accuracy against XL. The trained M granularity loses about 2%
- **DynaBERT** (joint loss over all sizes each step) is 0.01 log-perplexity
  worse at 850M, and still behind with 15% more compute. **OFA** (random
  per-layer sampling) gives a bell-shaped loss curve, weak at both ends
- **Consistency with XL:** up to 11.5% more matching tokens than baselines
- **Speculative decoding** (393M draft, 850M verifier): 1.14× / 1.11× on
  LAMBADA / TriviaQA, against 1.10× / 1.08× for baselines. 1.16× / 1.14×
  with a shared attention cache
- **Scaling (Table 3):** `Loss = a·(ND)^b + c`, with baseline
  `a = 14.08, b = −0.10, c = 0.89` and MatFormer
  `a = 21.60, b = −0.13, c = 1.33`
- **MatViT:** B/16 matches, L/16 is up to 0.35% better. The L/16 175M
  Mix'n'Match query encoder costs 40% less than XL at under 0.5% 1-NN loss,
  where separately trained small encoders are near 0

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | At family-matched compute, nested training matches the largest size and beats the smaller ones | moderate | Figures 2–3, 78M–850M, one group; the smaller sizes' advantage is explained by extra effective tokens |
| C2 | Sampling one granularity per step beats averaging all per step | moderate | DynaBERT comparison at 850M |
| C3 | Per-layer mixed widths land on the trained sizes' trade-off curve | moderate | Figure 2, and ViT Figure 4 |
| C4 | Non-decreasing width with depth is the right Mix'n'Match rule | weak | "empirically found … to perform the best", with some NAS support in Appendix D.1 |
| C5 | MatFormer scales like a standard Transformer | weak | the fitted exponents and offsets differ, and the text calls them "extremely similar" |
| C6 | Nested submodels are more consistent with the full model, which helps speculative decoding | moderate | consistency is measured, and the speed-up is 4 points on one model pair |

## Method

For FFN weights `W₁, W₂ ∈ ℝ^{d_ff × d_model}`, granularity `i` computes
`σ(x · W₁[0:mᵢ]ᵀ) · W₂[0:mᵢ]`. Each step samples `i ~ p` and takes one
optimizer step on `L(Mᵢ(x), y)`. At inference, choose `mᵢ` per layer.

## Concepts

- **Granularity** — one of the `g` explicitly trained FFN widths
- **Mix'n'Match** — assembling a model from different granularities per
  layer, none of which combination was trained
- **Consistency** — the fraction of tokens a submodel generates that match
  the universal model's for the same prefix, or the KL between their outputs

## Connections

It carries Matryoshka Representation Learning's nesting from the output
embedding to the weights. It builds on Slimmable Networks and DynaBERT (fixed
widths trained jointly) and on Once-for-All (random subnetworks plus NAS),
and differs from both in sampling one of a few preset nested sizes per step.
Flextron extends it to attention heads with a router. Gemma 3n
([LIT-tmp5bcs0](../literature.d/LIT-tmp5bcs0.md)) ships it.

## Recommendations

- **R1** — If you will deploy several sizes, train one nested model rather
  than several separate ones, and sample one size per step. *Topic:*
  model-architecture. *Status:* experimental. *Strength:* moderate. *Applies
  when:* you would otherwise train the whole family. Filed as [SOTA-tmpgvgkf](../practices.d/SOTA-tmpgvgkf.md)
- **R2** — For an intermediate budget, widen FFNs monotonically with depth
  rather than mixing extremes. *Strength:* weak. Folded into [SOTA-tmpgvgkf](../practices.d/SOTA-tmpgvgkf.md)

## Bearing on the record

- **[SOTA-tmpgvgkf](../practices.d/SOTA-tmpgvgkf.md)** is new and sourced here
- **[SOTA-227](../practices.d/SOTA-227.md)** (speculative decoding) gets a small corroborating result: a
  draft that shares weights with the verifier is more consistent with it, and
  that is worth a few points of speed-up. Not enough to change that practice

## Limitations

- **850M is the largest model.** Gemma 3n is the only published use at
  larger scale, and Google published no ablation for it
- **If you would only have trained the largest model, this costs more.** The
  budget is four models' worth of tokens. Appendix E.1 puts one MatFormer run
  at 2.58× the FLOPs per token of a single Transformer of the same size
- **The Mix'n'Match rule is a heuristic**, chosen by looking at results
- **Nesting only `d_ff`** leaves the attention and the residual width, and so
  the KV cache, the same size across granularities

## Open questions

- Whether the XL-matches-baseline result holds at billions of parameters and
  over-trained token ratios
- Whether nesting attention heads or `d_model` keeps the same trade-off,
  since that is where serving memory goes
