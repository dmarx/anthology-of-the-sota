---
number: 314
status: Active
formerly:
- SOTA-tmp0iki2
consensus: unreplicated
consensus_note: >-
  One group, one paper, three model families inside it. The mechanism is
  proved rather than only measured, which is why this is `Active` on a single
  source, but nobody outside this group has run it and nobody has run it
  outside diffusion. The 4-bit weight-and-activation setting it targets is
  also young enough that there is no field position to report.
title: 'Absorb quantization outliers into a high-precision low-rank branch taken from the weights, and fuse its kernels into the low-bit ones'
version: 2
history:
- version: 2
  date: '2026-09-22'
  note: >-
    Two conditions added, no change to the recommendation or the status. The
    rank is global — 32 at 4 bits, 16 at 8 — and in language transformers a
    global rank is now measurably the wrong choice (SOTA-318); nobody
    has checked whether diffusion transformers share that non-uniformity.
    Separately, the residual this hands its quantizer contains the bottom of
    the spectrum, which in non-square language-transformer matrices is not
    the negligible part (SOTA-317). Both are open questions about a
    practice whose reported results stand, recorded here because a reader
    porting this to a language model would otherwise meet them unwarned.
tags:
- numerics-and-precision
- inference-optimization
- systems-optimization
date: '2026-09-21'
source:
- LIT-512
introduced_by:
- LIT-512
implementations: []
summary: >-
  Li et al. (2024), [LIT-512](../literature.d/LIT-512.md) — at 4 bits on both weights and
  activations, smoothing alone is not enough. Shift outliers from activations
  into weights, peel the dominant singular values into a 16-bit rank-32
  branch, quantize the residual. Then fuse: run naïvely the branch costs
  **57%** latency and cancels the win; fused it gives **3.0×** over W4A16 and
  **3.5×** memory on 12B FLUX.1.
explained_by:
- THEORY-059
---

<!-- inactive-ok-file: THEORY-059 — Proposed, filed in this same
     contribution. This practice declares `explained_by:` on it, so the
     citation is the relation itself, and the sentence citing it says the
     spectral premise is what remains unsettled. -->

# SOTA-314: Absorb quantization outliers into a high-precision low-rank branch taken from the weights, and fuse its kernels into the low-bit ones

## Source

Li, Lin, Zhang, Cai, Li, Guo, Xie, Meng, Zhu and Han (2024),
[LIT-512](../literature.d/LIT-512.md) — read as [NOTE-257](../notes.d/NOTE-257.md).

## When this applies

You are quantizing **both** weights and activations to about 4 bits for
inference, and you want the arithmetic speedup rather than only the memory
saving. At 8 bits, or weight-only, the problem this solves does not bite hard
enough to be worth the machinery.

## Do this

**Shift the outliers out of the activations first.** Smoothing moves them into
the weights, which is where the next step can reach them. On its own it is not
enough at 4 bits — the paper's ablation has it only slightly ahead of naïve
quantization — but it makes the weights the single place outliers live.

**Take the low-rank branch off the weights, not off the quantization error.**
Compute the SVD of the smoothed weight `Ŵ`, keep the top `r` singular
directions in 16 bits, and quantize only the residual `R = Ŵ − L₁L₂`. The
ordering is the whole thing, and [THEORY-059](../theory.d/THEORY-059.md) is why: a weight
matrix has a steep spectrum so rank 32 removes a lot of magnitude, while a
quantization error has a flat one so the same rank removes almost nothing.
Doing it the other way round is a published method that underperforms.

**Rank 32 at 4 bits, rank 16 at 8 bits**, per-group symmetric quantization on
both sides, group size 64 with 16-bit scales for INT4, group size 16 with FP8
scales for NVFP4.

**Fuse the branch into the low-bit kernels, or do not add it.** This is the
half that is usually left to the reader and it is not optional:

| | latency |
|---|---|
| rank-32 branch run independently | **+57%** |
| fused | the reported speedups |

The fusion is two pairings, each justified by shared operands: Down Projection
with Quantize, because they read the same input; Up Projection with the 4-bit
compute, because they write the same output. Without it the extra 16-bit reads
and writes cost more than the 4-bit arithmetic saves.

**Keep the layers where 4 bits is not worth it in 16.** For FLUX.1 the linear
layers inside adaptive normalization stay W4A16; elsewhere cross-attention key
and value projections stay 16-bit, on the stated grounds that they are under
5% of runtime.

**Compose it with the error-compensation practice.** The residual weights are
quantized with GPTQ rather than round-to-nearest, which improves quality in
most of the paper's settings. [SOTA-185](SOTA-185.md) and this act on different terms
of the same bound.

## What it buys

- **3.5×** memory reduction on the 12B FLUX.1 models.
- **3.0×** over the W4A16 baseline on a 16GB laptop 4090 with INT4.
- **3.1×** over W4A16 on an RTX 5090 with NVFP4.
- On FLUX.1-dev with NVFP4, PSNR **21.5** against the 16-bit model.

## Why `Active` on one source

Because the reason is proved, not only measured. Proposition 4.1 bounds the
output error by the magnitudes of weights and activations as well as their
rounding errors, and Proposition 4.2 bounds a matrix's rounding error by its
magnitude; Eckart-Young then makes the truncated SVD the optimal rank-`r`
reduction of that magnitude. The recommendation follows from the bound, and
the ablation ordering matches what the bound predicts.

What one source cannot settle is whether the spectral premise holds outside
diffusion transformers, which is what [THEORY-059](../theory.d/THEORY-059.md) carries as
`Proposed`.

## Conditions

**The speedups are a co-design, not a quantization result.** They are measured
with the authors' own engine against a W4A16 baseline, and a reader who
implements the quantization without the fusion gets the 57% instead. Quoting
"3× faster" for the decomposition alone would be wrong.

**One result should be read sceptically, and the paper's own framing invites
it.** On FLUX.1-dev the 4-bit model **exceeds the original BF16 model** on
Image Reward, which the source reads as "suggesting stronger human
preference". A 4-bit model preferred over the model it approximates is more
economically explained by the metric — Image Reward is a learned preference
model with its own biases — than by quantization improving generation. The
PSNR and LPIPS columns do not show the same inversion.

**Not all of it is uniform gain.** On PixArt-Σ the INT4 variant degrades
slightly and only NVFP4 matches FP16, which the paper attributes to the 600M
model benefiting from the smaller microscaling group size.

**Diffusion only.** Three model families — SDXL, PixArt-Σ, FLUX.1 — all
diffusion, all image. Nothing here is measured on a language model, where the
activation outlier structure is the thing most of the quantization literature
is about.

**Hardware-shaped.** NVFP4's advantage rests on Blackwell's native support for
group size 16. The ordering of formats is a fact about the GPUs tested.

**The rank is global, and outside diffusion that is known to be the wrong
shape.** Rank 32 at 4 bits and 16 at 8, applied to every matrix. In language
transformers how nearly low-rank a matrix is varies systematically by
component and by depth, and picking one rank for all of them costs ~6.4× in
perplexity against picking per matrix at the same compression
([SOTA-318](SOTA-318.md)). Whether diffusion transformers have the same
non-uniformity is unmeasured. This is not a defect in the reported results —
the numbers are what they are — but a global rank is a choice the source does
not defend, and the first thing to sweep when porting this.

**What is handed to the quantizer is the bottom of the spectrum, and that may
not be the negligible part.** Peeling the top 32 directions into 16 bits
leaves everything else, including the smallest singular directions. In
non-square language-transformer matrices those carry data directions and
removing them is catastrophic ([SOTA-317](SOTA-317.md)). Quantizing is
not removing, and no measurement here or there connects the two, so this is
flagged and not claimed: the damage curve against bit-width for the smallest
directions has not been drawn by anyone.

## Known implementations

- Nunchaku, the inference engine published with the paper, which also loads
  off-the-shelf LoRA adapters without re-quantization.
