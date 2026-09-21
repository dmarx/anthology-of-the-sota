---
status: Active
title: 'GaussianToken: An Effective Image Tokenizer with 2D Gaussian Splatting'
version: 1
tags:
- representation-and-encoding
- generative-modeling
- vision-and-graphics
date: '2026-09-21'
published: '2025-01-26'
arxiv: '2501.15619'
first_author: 'Dong'
keywords:
- 'image-tokenizer'
- 'vector-quantization'
- '2d-gaussian-splatting'
- 'vq-vae'
- 'codebook-utilization'
- 'reconstruction-fid'
implementations: []
summary: >-
  Dong, Wang, Zheng, Chen, Lu and Tang (2025), [ARXIV-2501.15619](https://arxiv.org/abs/2501.15619). Replaces
  the fixed grid of a VQ image tokenizer with `K` 2D Gaussians whose feature
  coefficient is quantized while position, rotation and scale stay
  **continuous**. Reports rFID **1.61** on ImageNet-1K against LlamaGen's 2.19
  with a 16× smaller codebook. The paper's own word for the result is
  *semi-discrete*, and the comparison is at equal token **count** rather than
  equal rate — each token carries five floats the baselines' tokens do not.
---

# LIT-tmpjyh2c: GaussianToken: An Effective Image Tokenizer with 2D Gaussian Splatting

Dong, Wang, Zheng, Chen, Lu and Tang (2025) —
[ARXIV-2501.15619](https://arxiv.org/abs/2501.15619), read as [NOTE-tmpwtv8b](../notes.d/NOTE-tmpwtv8b.md).

## Key takeaways

- **The idea is to let the quantization units move.** A VQ tokenizer matches
  each cell of an `h × w` grid to a codebook entry. This replaces the grid
  with `K` 2D Gaussians, each carrying a position `μ ∈ R²`, a rotation `θ`, a
  scale `s ∈ R²` and a feature coefficient `ζ ∈ R^D`. Only `ζ` is quantized;
  the other five numbers stay continuous and are concatenated to the
  quantized result before splatting back to a feature map.
- **The reported numbers are strong.** ImageNet-1K rFID **1.61** against
  LlamaGen's 2.19, with embedding dimension 8 against 256, codebook 1024
  against 16384, and 20 epochs against 40. CIFAR 12.94 against a reproduced
  VQGAN's 27.00; Mini-ImageNet 12.18 against 32.31.
- **Everything is reconstruction.** There are no generation experiments, no
  multimodal experiments and no downstream task of any kind. The paper states
  this twice, in §3.4 and again under Limitations.
- **The best-supported finding is the smallest one.** rFID is non-monotonic in
  embedding dimension — 16.34 at 2, **12.94 at 3**, 13.89 at 4, 13.86 at 8 —
  and the paper ties this to codebook utilization, which rises as the
  dimension falls. Codebook size barely matters by comparison (14.56 / 13.89 /
  12.96 / 13.03 across 512 → 16384), and utilization falls below 50% at
  16,384.
- **Quality rises monotonically with the number of Gaussians**: rFID 20.09 /
  13.89 / 10.14 / **7.19** at `K` = 32 / 64 / 128 / 256 on CIFAR. Since `K`
  *is* the token count, this is the rate-quality curve, and the paper does not
  present it as one.

## Standing in the anthology

Filed as context, and **no practice rests on it**. Two reasons, both about
what the evidence can support rather than about whether the idea is good.

**The comparison is at equal token count, not equal rate.** Each GaussianToken
carries a codebook index — 10 bits at size 1024 — plus five continuous
parameters, which at fp16 is another 80 bits. The baselines' tokens carry the
index alone. "Same number of image tokens (256 tokens for a 256×256
resolution)" is the paper's own framing of the comparison and it is true; it
is not the same amount of information. Nothing in the paper computes bits per
image for either side, so how much of the rFID gap is the method and how much
is the side-channel cannot be determined from what is reported.

**The stated motivation is not met by the artifact.** The opening argument is
that images must be tokenized to *discrete* tokens to align with text and feed
an autoregressive model. The thing produced is, in the paper's own word,
"semi-discrete": a token that is an index plus five floats is not something a
language model consumes. §3.4 gives an informal argument that this is *better*
for downstream generation, and its combinatorics is written backwards — an
`h × w` index matrix over an `N`-entry codebook has `N^(h×w)` states, not the
`(h×w)^N` the paper writes — and no experiment tests it either way.

**Three internal inconsistencies**, recorded because a reader checking the
headline will hit them. §4.2 fixes the CIFAR embedding dimension at 4 and the
ImageNet-1K codebook at 2048; Table 1's CIFAR row shows dimension **3** and
its ImageNet row shows codebook **1024**, and §4.3 says 1024 as well. §4.3
gives the ImageNet result as rFID **1.67** where Table 1 says **1.61**. §4.3
says GaussianToken beats VQGAN on CIFAR "by 14.01 in rFID" at dimension 4;
Table 1's gap is 14.06 at dimension 3 and Table 2's dimension-4 row gives
13.11. Three numbers for one comparison, no two agreeing.

**The record has no trunk for this.** There is no `LIT` note for VQ-VAE,
VQGAN, MaskGIT or LlamaGen — every baseline in Table 1. A descendant filed
above an absent trunk is the gap this filing surfaces, and it is recorded
rather than quietly filled.
