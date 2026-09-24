---
status: Active
title: 'Transformers without Tears: Improving the Normalization of Self-Attention'
version: 1
tags:
- model-stability
- training-optimization
- model-architecture
date: '2026-09-24'
published: '2019-10-14'
arxiv: '1910.05895'
first_author: 'Nguyen'
keywords:
- 'pre-norm'
- 'scalenorm'
- 'warmup'
- 'normalization'
- 'low-resource-translation'
implementations: []
summary: >-
  Nguyen and Salazar (2019), [ARXIV-1910.05895](https://arxiv.org/abs/1910.05895). The first systematic evaluation
  of pre-norm in the base Transformer regime — and it reports a result the
  record's `universal` pre-norm practice does not carry: **on high-resource
  WMT'14 English-German, post-norm wins, 27.58 to 26.83.** Also introduces
  ScaleNorm, the `ℓ₂`-normalization-with-one-learned-scalar that `LIT-640`'s
  QK-norm is an application of.
compared_against:
- LIT-640
---

# LIT-tmprikl1: Transformers without Tears: Improving the Normalization of Self-Attention

Nguyen and Salazar (2019) — [ARXIV-1910.05895](https://arxiv.org/abs/1910.05895)

## What it is not

**This paper did not introduce pre-norm, and says so in its own
introduction.** It is worth stating first because the abstract — *"we show
that pre-norm residual connections (PreNorm) and smaller initializations
enable warmup-free… training"* — reads like origination, and the record was
about to treat it that way.

Their attribution, in the second paragraph:

> Chen et al. (2018) found that pre-norm residual units (PreNorm)… were
> instrumental to their model's performance. Wang et al. (2019) compare the
> two, showing that PreNorm makes backpropagation more efficient over depth…

and, a page later:

> This is cited as a stabilizer for Transformer training (Chen et al. 2018;
> Wang et al. 2019) and is **already implemented in popular toolkits**
> (Vaswani et al. 2018; Ott et al. 2019; Hieber et al. 2018), **though not
> necessarily used by their default recipes.**

Their own framing is *"Our work demonstrates **additional consequences** in
the base (≤6-layer encoder) Transformer regime."* That is a `source:` claim,
not an `introduced_by:` one, and `SOTA-032` is corrected accordingly in this
same contribution — to **empty**, not to this paper.

## The result the record did not have

Everything above is low-resource. Section 3.4 asks whether the claims hold at
high resource: base Transformer, WMT'14 English-German, `newstest2014`,
tokenized BLEU.

| | BLEU |
| --- | --: |
| PostNorm + LayerNorm (published, Vaswani et al.) | 27.3 |
| **PreNorm** + LayerNorm | **26.83** |
| PreNorm + FixNorm + ScaleNorm | 27.07 |
| **PostNorm** + LayerNorm | **27.58** |
| PostNorm + FixNorm + ScaleNorm | 27.57 |

**Post-norm beats pre-norm by 0.75 BLEU**, and the paper calls it out:
*"Surprisingly, in this task PostNorm works notably better than PreNorm; one
observes similar behavior in Wang et al. (2019)."* Their closing summary is
the careful version — *"while PostNorm performs better for high-resource NMT
in the original base Transformer regime, PreNorm is both more stable and more
competent in low-resource settings."*

Their speculation about why is **a different mechanism from the one the
record holds**: identity residual networks acting like shallow ensembles
(Veit et al. 2016), *"thus undermining the learning of the longest path"*. The
record's account of pre-norm's cost is representation collapse — the residual
stream outgrowing any single block's contribution. These are not the same
claim, and the paper is explicit that *"further study is required"*.

## Pre-norm's advantage, and how much of it is really initialization

The low-resource case is strong, and the qualification inside it is the
interesting part. On en→vi development BLEU with Xavier normal
initialization:

| warm-up steps | 4k | 8k | 16k |
| --- | --: | --: | --: |
| PostNorm, default init | fail | fail | 5.76 |
| PreNorm, default init | 28.52 | 28.73 | 28.32 |
| PostNorm, **SmallInit** | 28.17 | 28.20 | 28.62 |
| PreNorm, **SmallInit** | 28.26 | 28.44 | 28.33 |

Reducing the attention layers' initialization takes post-norm from *failing*
to within 0.5 BLEU of pre-norm. **So a large part of what looks like a
placement problem is an initialization problem**, and the paper says so:
they *"partly reclaim PostNorm's stability via smaller initializations,
although PreNorm is less sensitive to this magnitude."* Less sensitive is the
honest form of the advantage.

Without warm-up, the placement difference reasserts itself with depth
(en→vi development BLEU):

| encoder/decoder layers | 4 | 5 | 6 |
| --- | --: | --: | --: |
| PostNorm | 18.31 | fails | fails |
| PreNorm | 28.33 | 28.13 | 28.32 |

And `NoWarmup` is competitive with the inverse-square-root schedule on four of
five pairs, failing only on the smallest — *"one can do without warmup, though
it remains useful in the lowest resource settings."*

## ScaleNorm, and the loop it closes

The paper's own contribution is **ScaleNorm**: replace LayerNorm with `ℓ₂`
normalization to a single learned length `g`. Motivated by Santurkar et al.
(2018) — batch normalization works by smoothing the loss landscape, not by
reducing internal covariate shift — so a non-variance-based normalization
should do as well. Their `g` is initialized to `√d`.

Two things follow that the record should hold together.

**ScaleNorm is what `LIT-640`'s QK-norm applies to queries and keys.** Henry
et al. build directly on this paper — same five benchmarks, same repository as
a starting point — and their own description is that ScaleNorm *"replaces
layer normalization with `ℓ₂` normalization along the embedding dimension,
multiplied by a learnable scalar parameter"*, while QKNorm *"complements
LayerNorm rather than replacing it"*. The technique `SOTA-192` recommends is
this paper's normalization, moved from the residual stream onto `Q` and `K`.

**The learned `g` grows with depth.** Positive correlation between depth and
`g` for every sublayer type except decoder-encoder attention, *"clearest in
the decoder, where `g` linearly scales up to the output layer"*. That is a
measurement of the residual stream's magnitude growing with depth — the same
quantity the record's collapse account is about — taken by a different method
and three and a half years earlier. Recorded rather than filed: it is a
correlation over sublayers of trained models, not the derivation the record
already holds.

## Standing in the anthology

Unit 1 of `#342`, and `#290`'s promotion [#23](https://github.com/dmarx/anthology-of-the-sota/issues/23). Filed as a **defect repair on
two documents**:

`SOTA-032` is `Active` and `universal` and recommends pre-norm. Its
`introduced_by` named Xiong et al. (2020), a paper published **four months
after this one** and about a different regime. The repair is not to repoint it
here, because this paper disowns the origin; it is to say the record looked
and found no origin document, which `ADR-053` provides for.

`LIT-640`'s evidence line said QK-norm's +0.928 BLEU was measured *"against
state-of-the-art bilingual benchmarks"*. The baseline is **this paper's own
system**, and the comparison swaps two things at once. Corrected here.

Two antecedents this paper names are unheld and are the natural next
candidates for the pre-norm line: **Chen et al. (2018)**, `1804.09849`, whom
it credits with finding pre-norm instrumental, and **Wang et al. (2019)**,
`1906.01787`, who first compared the two placements at depth and who report
the same high-resource result. Neither is in `#290`'s queue, so neither is
ranked yet.
