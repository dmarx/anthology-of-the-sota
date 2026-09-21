---
number: 306
status: Active
formerly:
- SOTA-tmpjm39m
consensus: converged
consensus_note: >-
  Three groups, five years apart, on three architectures and three datasets,
  with the same shape and the same interior optimum, and the two later ones
  credit the first. Raised from `emerging` when the origin was filed: two
  measurements of somebody else's recommendation is corroboration, and a
  recommendation plus two independent confirmations of it is what the field
  having settled looks like. What is *not* settled is where the optimum sits —
  16, 8 and 3 on the three — so the rule is still "shrink it and sweep".
title: "Factorize the codebook: look up in a low-dimensional normalized space, embed in a high-dimensional one, and report utilization alongside reconstruction quality"
version: 2
history:
- version: 2
  date: '2026-09-21'
  note: >-
    Filing the origin (LIT-tmpov7yl, ViT-VQGAN) corrected this in three places
    and changed its title. (1) The instruction was "make the code vectors
    low-dimensional"; the origin's is to FACTORIZE — look up in a
    low-dimensional space, project the matched code back to a high-dimensional
    embedding — which names the mechanism the descendants' framing conceals.
    (2) `ℓ₂`-normalization was carried as an unablated design detail because
    neither source ablated it; the origin does, and it is the largest single
    effect in the table. (3) The practice called utilization "the mechanism";
    the origin's dimension-4 row has 96% utilization with near-worst FID, so
    it is a necessary condition that can be met while quality collapses.
    `introduced_by` moves from LlamaGen to the origin, the source order puts
    it first, and consensus goes `emerging` -> `converged`.
tags:
- representation-and-encoding
- generative-modeling
date: '2026-09-21'
source:
- LIT-tmpov7yl
- LIT-497
- LIT-494
introduced_by:
- LIT-tmpov7yl
implementations: []
summary: >-
  Yu et al. (2021), [LIT-tmpov7yl](../literature.d/LIT-tmpov7yl.md) — project the encoder output
  down to a low-dimensional lookup space, `ℓ₂`-normalize it and the codebook,
  match there, and project the winner back up to a wide embedding. Codebook
  usage goes **4% → 95%** and FID **3.68 → 1.50** at unchanged throughput;
  removing the normalization alone drops usage to **2%**. Confirmed
  independently by [LIT-497](../literature.d/LIT-497.md) and [LIT-494](../literature.d/LIT-494.md), and in all
  three the curve turns back up, so there is an optimum to find rather than a
  direction to follow.
---

# SOTA-306: Factorize the codebook: look up in a low-dimensional normalized space, embed in a high-dimensional one, and report utilization alongside reconstruction quality

## Source

Yu, Li, Koh, Zhang, Pang, Qin, Ku, Xu, Baldridge and Wu (2021),
[LIT-tmpov7yl](../literature.d/LIT-tmpov7yl.md) — read as [NOTE-tmptxi4l](../notes.d/NOTE-tmptxi4l.md).
Confirmed independently by Sun et al. (2024), [LIT-497](../literature.d/LIT-497.md), which
credits it, and by Dong et al. (2025), [LIT-494](../literature.d/LIT-494.md), which does not
cite either.

## When this applies

You are training a vector-quantized autoencoder — an image tokenizer, an audio
one, any bottleneck that snaps a feature vector to its nearest entry in a
learned codebook. The lineage is [LIT-499](../literature.d/LIT-499.md) and
[LIT-496](../literature.d/LIT-496.md); the tunable parts are the codebook's two shapes.

## Do this

**Separate the lookup from the embedding.** This is the instruction, and it is
not the same as "use small code vectors". Project the encoder output down to a
low-dimensional *lookup* space — 768-d to 32-d or 8-d in the origin — find the
nearest entry there, then project that entry back up to a high-dimensional
embedding for the decoder. Nearest-neighbour search wants low dimension,
because at 256 or 768 dimensions distances concentrate and one entry wins
nearly every query; the embedding wants high dimension, because that is where
the capacity is. Forcing both into one space is what kills codebooks.

**`ℓ₂`-normalize both sides, and initialize the codebook from a normal
distribution.** The lookup then compares cosine similarity on a sphere. This
is the *larger* of the two effects, not a refinement on top of the first.

| lookup dim | `ℓ₂` | IS ↑ | FID ↓ | usage |
|---|---|---|---|---|
| 256 | ✓ | 160.1 | 3.68 | **4%** |
| 128 | ✓ | 173.9 | 2.77 | 14% |
| 64 | ✓ | 179.5 | 2.50 | 37% |
| **16** | ✓ | **191.2** | **1.50** | 95% |
| 8 | ✓ | 189.5 | 1.52 | 96% |
| 4 | ✓ | 143.8 | 3.68 | **96%** |
| 32 | **✗** | 123.6 | **5.44** | **2%** |

*(ViT-VQGAN, ImageNet, codebook 8192. Throughput is 954–960 across every row,
so none of this costs anything.)*

Dropping the normalization is worse than any dimension choice in the table —
worse than leaving the lookup at 256.

**Measure utilization, and do not stop there.** It is the diagnostic, and the
dimension-4 row is why it is not the target: **96% usage, 3.68 FID**, tied for
worst among the normalized rows. Every code gets used and none of them can say
enough. A tokenizer reconstructing acceptably at 20% usage has a codebook that
is mostly decoration and will not be helped by a larger `K`; a tokenizer at
96% usage may simply have too little room per code.

**Sweep for the optimum rather than following the direction.** All three
sources turn back up, at different places:

- ViT-VQGAN: best at lookup dimension **16**; dimension 4 loses 40 IS points.
- LlamaGen: 256 → 9.21 rFID at 0.29% usage, **8 → 2.19** at 97%, 4 → 9.88 at
  82%.
- GaussianToken: 16.34 at 2, **12.94 at 3**, 13.89 at 4, 13.86 at 8.

Sixteen, eight and three, on three architectures. Nothing in the three
predicts where it sits on a fourth.

**Codebook size is the weaker lever and also non-monotone.** LlamaGen:
4096 → 3.02 (100% used), 8192 → 2.91 (75%), **16384 → 2.19** (97%),
32768 → 2.26 (85%). GaussianToken's sweep moves rFID by 1.6 across a 32× range
of `K`, with utilization below 50% at 16,384. Fix the lookup first; size buys
little on its own and nothing past the point where utilization falls.

## Why `Active`, and why `converged`

Three groups, five years apart, on three architectures (ViT, CNN and a
Gaussian-splatting quantizer), three datasets and three metric sets, reporting
the same shape and the same mechanism — with the two later ones crediting the
first and one of them arriving at it without citing anybody. The instruction
is cheap to follow, free at inference by the origin's own throughput column,
and cheap to check.

The consensus was `emerging` while the record held only the two descendants,
because two measurements of somebody else's recommendation is corroboration
rather than agreement. Filing the origin is what changed it.

## Conditions

**The descendants state the monotone half in their captions and leave the
reversal in the table.** LlamaGen's caption reads "Lower vector dimension
(from 256 to 8) improves both", bounded exactly to exclude dimension 4. Its
codebook-size caption is bounded the same way. GaussianToken, to its credit,
describes its own curve as rising then falling, and the origin's table simply
prints the reversal without a caption claiming otherwise. Anyone taking the
descendants' captions rather than the tables gets "smaller is better", which
is false at the end.

**The optimum is not transferable.** 16, 8 and 3 on three models, and no
source offers an account of what sets it.

**The two mechanisms are not separated from each other.** In the origin's
table every normalized row is also factorized and the single un-normalized row
sits at one dimension, so there is no un-normalized, un-factorized control and
the interaction is unmeasured.

**Factorization versus a plainly narrow codebook is untested.** The origin
factorizes and keeps a wide embedding; LlamaGen makes the whole codebook
8-dimensional and reports a comparable effect. Nobody has run the comparison,
so this practice states the mechanism the origin names while acknowledging
that the simpler implementation appears to work too.

**The utilization metric is not standardized, and the three sources differ.**
The origin counts codes used over a batch of 256 test images averaged across
the test set; LlamaGen counts over a queue of 65,536 samples and deliberately
omits the entropy loss that MaskGIT and the MAGVIT line use in codebook
learning. A per-batch definition reads higher than a per-queue one. None of
the three flags this, and utilization numbers should not be compared across
them.

**The origin's ablation rides alongside architecture changes.** ViT-versus-CNN
and StyleGAN-versus-PatchGAN sit in the same table as the codebook rows and
are not crossed with them, so the headline FID cannot be apportioned. The
codebook rows themselves are internally controlled, which is what this
practice rests on.
