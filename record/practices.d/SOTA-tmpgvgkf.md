---
status: Proposed
promote_when: >-
  A group outside Google trains a nested model at several billion
  parameters, against separately trained sizes at the same total compute,
  and reports that the largest granularity still matches its own baseline,
  with downstream evaluations and not loss alone. Gemma 3n shipping it does
  not count: it is the authors' own organization and published no
  comparison.
title: 'Train one nested model instead of a family of separately trained sizes, and extract the sizes you need from it'
version: 1
tags:
- model-architecture
- inference-optimization
- training-optimization
date: '2026-09-22'
source:
- LIT-tmp7xt7l
introduced_by:
- LIT-tmp7xt7l
consensus: unreplicated
consensus_note: >-
  One group reports the comparisons. Gemma 3n ships the architecture: E4B
  contains a jointly trained E2B, and Mix'n'Match sizes between them are
  offered (LIT-tmp5bcs0). That is production adoption by the authors' own
  organization with no published ablation, so it counts as adoption and not
  evidence (DP-005).
implementations:
- Gemma 3n
summary: >-
  Devvrit, Kudugunta, Kusupati et al. (2023), [LIT-tmp7xt7l](../literature.d/LIT-tmp7xt7l.md) — nest four FFN
  widths in one Transformer, train one width per step, and extract any size
  in between by choosing widths per layer. Up to 850M parameters, at the
  compute of training the four sizes separately, the largest matches its
  baseline and the smaller ones beat theirs. It pays only if you were going
  to train the family. Gemma 3n ships it.
---

# SOTA-tmpgvgkf: Train one nested model instead of a family of separately trained sizes, and extract the sizes you need from it

## Source

Devvrit, Kudugunta, Kusupati et al. (2023), [LIT-tmp7xt7l](../literature.d/LIT-tmp7xt7l.md) — MatFormer. Read
as [NOTE-tmp98tod](../notes.d/NOTE-tmp98tod.md).

## The practice

If you are going to serve several model sizes, **do not train them
separately. Train one model whose FFNs are nested**, so that granularity
`i` uses the first `mᵢ` hidden neurons of every FFN. Four granularities,
at FFN ratios {0.5, 1, 2, 4}, is what was tested.

- **Sample one granularity per step**, uniformly unless tuned, and take an
  ordinary optimizer step on that submodel's loss. Do not average all
  granularities' losses in one step. That is DynaBERT's rule, and it gives a
  quarter of the gradient updates for the same data and ends up 0.01
  log-perplexity worse at 850M
- **At deployment, choose each layer's width independently** to hit any
  budget between the trained sizes. Keep widths non-decreasing with depth,
  with the smallest steps you can. The paper found this beats mixing
  extremes and matches evolutionary NAS
- **Use the nesting for inference tricks.** A small granularity drafting
  for the full model is more consistent with it than a separately trained
  draft (up to 11.5% more matching tokens), which is worth 1.14× against
  1.10× in speculative decoding ([SOTA-227](SOTA-227.md)) at 850M. The smaller encoders of
  a nested ViT can query a corpus the full encoder embedded

## What the evidence is, exactly

The comparison is **one nested run on `4X` tokens against four separate
models on `X` tokens each**, so the total compute is the same. Inside the
nested model, the smallest submodel's weights are updated at every step and
effectively see `4X` tokens, while the largest sees `X`. So:

- **The largest granularity matches its separately trained baseline.** It
  does not beat it (Appendix B.4)
- **The smaller granularities beat theirs**, and the obvious reason is that
  they trained on more data
- **Sizes nobody trained sit on the curve between the trained ones.** At
  55% of XL's compute, a Mix'n'Match model loses about 1% accuracy against
  XL, while the trained M loses about 2%

The practice therefore **pays only when you would otherwise train the
family.** If you want one model, a nested run is dearer. Appendix E.1 puts
it at 2.58× the FLOPs per token of a single Transformer of the largest
size. What you get for that is every size in between.

## Conditions

- **78M–850M decoder LMs and ViT-B/L.** Nothing larger is published with a
  comparison
- **FFN width only.** Attention, `d_model` and depth are shared across
  sizes, so the KV cache and the attention cost do not shrink with the
  granularity. Nesting attention heads is in the paper's appendix, and
  nesting them with a per-token router is later work (Flextron), which is
  not in the record
- **The scaling fit is not identical.** The paper calls MatFormer's
  `Loss(N, D)` "extremely similar" to a Transformer's, but the fitted
  exponent is −0.13 against −0.10 and the offset 1.33 against 0.89. Over
  78M–850M the curves overlap. How they extrapolate is not established

## Known implementations

- Gemma 3n (E2B nested in E4B, Mix'n'Match sizes between)
