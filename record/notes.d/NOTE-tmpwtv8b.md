---
status: Read
paper: LIT-tmpjyh2c
title: 'GaussianToken and the cost of the continuous half'
version: 1
date: '2026-09-21'
summary: >-
  Read from the [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) worklist and filed without a practice. The idea —
  let the quantization units move and size themselves instead of sitting on a
  grid — is a good one, and the evidence for it cannot be separated from the
  five continuous parameters each token carries alongside its index. The
  comparison is at equal token count, and nobody computed bits.
---

# NOTE-tmpwtv8b: GaussianToken and the cost of the continuous half

## Contribution

Takes the quantization unit of a VQ image tokenizer off the grid. In VQ-VAE
and its descendants, the encoder produces an `h × w` feature map and every
cell is independently snapped to its nearest codebook entry, so the spatial
extent of a token is fixed by the downsampling ratio and identical everywhere.
Here the units are `K` 2D Gaussians that learn where to sit, which way to
point and how far to spread, and the feature map is reconstructed by splatting
them. Detail-dense regions can be covered by several narrow Gaussians and flat
regions by one wide one. That reallocation is the contribution, and as far as
I can tell it is new for a *learned, generalizing* tokenizer — the prior 2D
Gaussian work (GaussianImage, Image-GS) fits Gaussians per image and does not
generalize.

## Key insight

A quantizer has two jobs that VQ conflates: deciding *what* a region looks
like and deciding *which region* it is. The codebook does the first well and
the grid does the second by fiat. Separating them — keep the codebook for the
appearance, learn the support — is a real decomposition, and it is also why
this paper is hard to evaluate: the learned support is continuous, so the
moment you separate the jobs you have stopped producing discrete tokens.

## Assumptions

- The Gaussian covariance is factorized as `Σ = (RS)(RS)ᵀ` from a rotation
  angle `θ ∈ [0, π]` and scales `s ∈ R²`, which keeps it positive
  semi-definite by construction.
- Positions `μ` are refined residually (`μ + Δμ`) while `θ`, `s` and `ζ` are
  *replaced* each refinement step. The paper's reason is stability: replacing
  `μ` moves the region every other parameter was fitted to.
- Deformable attention stands in for full attention over the feature
  sequence, so the cost argument depends on a sparse attention pattern rather
  than on the Gaussian idea.
- The splatting is a CUDA kernel; "ultra-fast rendering" is asserted and no
  wall-clock or FLOP comparison against a VQ lookup appears anywhere.

## Key results

- **Table 1, ImageNet-1K 256×256.** GaussianToken: 256 tokens, ratio 16,
  embedding dimension 8, codebook 1024, 20 epochs → rFID **1.61**, PSNR 20.68,
  SSIM 0.58. LlamaGen: 256 tokens, dimension 256, codebook 16384, 40 epochs →
  2.19, PSNR 20.79. MaskGIT 2.28; VQGAN 7.94; SD-VQGAN 5.15. *Holds when:*
  reconstruction only, on a 5,000-image test split.
- **Table 1, CIFAR 32×32, ratio 4.** GaussianToken 64 tokens, dimension 3,
  codebook 1024, 30 epochs → 12.94 / 25.84 / 0.90. Reproduced VQGAN at the
  same token count and epochs → 27.00 / 23.59 / 0.81. The 500-epoch
  comparisons (VQ-VAE 39.67, SQ-VAE 37.92, CVQ-VAE 24.73) use embedding
  dimension 256.
- **Table 1, Mini-ImageNet.** 12.18 / 19.84 / 0.57 against a reproduced VQGAN's
  32.31 / 18.71 / 0.50, matched on tokens, codebook, dimension and epochs.
- **Table 2, embedding dimension (CIFAR).** 2 → 16.34; **3 → 12.94**;
  4 → 13.89; 8 → 13.86. Non-monotonic, with a stated mechanism: smaller
  dimension gives higher codebook utilization (Figure 4).
- **Table 3, codebook size (CIFAR).** 512 → 14.56; 1024 → 13.89; 2048 →
  **12.96**; 16384 → 13.03, with utilization below 50% at 16,384. A 32× range
  of codebook size moves rFID by 1.6.
- **Table 4, Gaussian number (CIFAR).** 32 → 20.09; 64 → 13.89; 128 → 10.14;
  256 → **7.19** / 28.23 / 0.95. Monotone, with diminishing returns.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Learning the position and extent of quantization units beats a fixed grid at matched token count | moderate | Tables 1 and 4, three datasets — but confounded, see below |
| C2 | It reaches rFID 1.61 on ImageNet-1K, better than LlamaGen's 2.19 | weak | one run, no seeds, 5,000-image test split, and §4.3 gives the same number as 1.67 |
| C3 | It needs a smaller codebook and fewer epochs than the baselines | moderate | Table 1, consistently, across three datasets |
| C4 | rFID is non-monotonic in embedding dimension, optimized around 3, via codebook utilization | moderate | Table 2 plus Figure 4, one dataset, one architecture |
| C5 | The representation is better suited to downstream generation | weak | an informal argument in §3.4 with no experiment, and its combinatorics is written backwards |
| C6 | Effective image tokenization requires alignment with discrete text | — | the paper's motivating premise, asserted, and not what the method delivers |

## Method

Encoder features are flattened and lifted; `K` Gaussian anchors are randomly
initialized and lifted through an MLP into queries. `B = 3` blocks each run
self-attention over features and over queries, deformable cross-attention from
anchors into features, and a refinement MLP that emits `Δμ, Δθ, Δs, Δζ`.
Afterwards the feature coefficients `ζ` are quantized by nearest neighbour
against a standard codebook, the five spatial parameters are **concatenated
unquantized**, and a CUDA splatting kernel renders the set back to an `h × w`
feature map for the VQGAN decoder. Loss is VQGAN's: reconstruction, commitment
and GAN terms. The whole thing is described as a drop-in replacement for
VQGAN's quantization step, which it is.

## Concepts

- **featured 2D Gaussian / GaussianToken** — the unit `g = (μ, θ, s, ζ)`, of
  dimension `5 + D`. The name is doing work: five of those numbers are not
  tokens in any sense a language model would recognize.
- **semi-discrete** — the paper's own term for the resulting latent space,
  used once in §3.4. It is the accurate description and it does not reach the
  abstract.
- **contribution `c_ki`** — a Gaussian's influence at grid position `i`, the
  Gaussian density times the quantized feature coefficient. Feature values are
  sums of contributions, so a cell's value is not any single codebook entry.
- **valid coverage region `Ω_k`** — where a unit's contribution is non-zero;
  the basis of the paper's convergence argument, that gradients to a unit
  aggregate over a region rather than a cell.

## Connections

The quantization side descends from VQ-VAE and VQGAN, and the paper compares
against VQGAN, MaskGIT and LlamaGen. The Gaussian side descends from 3D
Gaussian Splatting and its 2D image-fitting descendants, GaussianImage and
Image-GS, which the related-work section correctly distinguishes: those fit
one image at a time and do not generalize.

No machine-readable relation is declared, and this is a case where one is
genuinely missing rather than absent by choice — `compared_against` would be
right for VQGAN, MaskGIT and LlamaGen if the record held them. It does not:
there is no `LIT` note for VQ-VAE, VQGAN, MaskGIT or LlamaGen. That gap is
the most useful thing this reading found.

## Recommendations

- **R1** — let quantization units learn their own position and extent rather
  than tiling a fixed grid. *Topic:* image tokenization. *Status:*
  experimental. *Strength:* weak **as evidenced here**, because the same
  change that frees the support also adds a continuous side-channel and the
  two are never separated. **Not filed.** What would make it fileable is
  below, under Open questions.
- **R2** — shrink the codebook's embedding dimension until utilization stops
  rising. *Strength:* moderate; one dataset, one architecture. **Not filed**,
  and it should be attached to a VQ trunk the record does not yet have rather
  than hung off this paper alone.

## Bearing on the record

Mostly it shows what is missing. The corpus has `SOTA-187` — train the
generative model in a learned compressed latent — and that latent is
continuous. It has nothing on discrete image tokenization at all: no VQ-VAE,
no VQGAN, no MaskGIT, no LlamaGen, and so no place for this paper's claim to
attach or be contradicted. Filing a 2025 descendant into that space produces a
document with no lineage, which is why the `LIT` note carries the gap
explicitly.

Nothing here contradicts an existing practice.

## Limitations

- **The comparison is at equal token count, not equal rate.** Each token is
  one index — 10 bits at codebook 1024 — plus five continuous parameters,
  which at fp16 is 80 bits more. The baselines' tokens carry the index alone.
  Bits per image is never computed for either side, so the share of the rFID
  gap attributable to the moving support versus the side-channel is not
  identified. This is the single reason no practice is filed.
- **The motivation is not met by the artifact.** The paper opens on aligning
  images with discrete text for autoregressive models, and produces a
  representation it calls semi-discrete. A token that is an index plus five
  floats cannot be fed to a language model as a token.
- **No downstream experiments of any kind.** The paper says so in §3.4 and
  under Limitations, which is honest, and it means every claim about
  generation diversity is argument.
- **The diversity argument has an algebra error.** §3.4 puts the number of
  index matrices at `(h × w)^N` for a codebook of size `N`; it is `N^(h×w)`.
  With `h × w = 256` and `N = 1024` the two differ by a factor of `2^5632`.
  Nothing rests on it, because nothing was measured.
- **Three internal inconsistencies on the headline.** §4.2 states CIFAR
  embedding dimension 4 and ImageNet codebook 2048; Table 1 shows 3 and 1024,
  and §4.3 says 1024. §4.3 gives ImageNet rFID as 1.67, Table 1 as 1.61. §4.3
  claims a 14.01 rFID advantage on CIFAR at dimension 4, where Table 1's gap
  is 14.06 at dimension 3 and Table 2's dimension-4 row implies 13.11. The
  CIFAR headline row appears to be the best cell of the ablation rather than
  the configuration §4.2 describes as the setting.
- **The ablation table references are wrong** — §4.4 points at "Table 4" for
  the embedding-dimension and codebook-size studies, which are Tables 2 and 3
  — and the Gaussian-number text says "from 16 to 128" where the table runs 32
  to 256. Sloppiness rather than error, and it costs a checking reader time.
- **Single runs throughout.** No seeds, no repeats, no error bars, and the
  ImageNet rFID is on a 5,000-image test split where the convention for this
  metric is the 50,000-image validation set. I could not verify what the
  baselines' quoted rFIDs were computed on.
- **No cost comparison.** Deformable attention over the feature map plus three
  refinement blocks plus a splatting kernel is strictly more work than a
  nearest-neighbour lookup, and no wall-clock, FLOP or memory number appears.

## Open questions

- **What is the rate-distortion curve?** The measurement that would turn R1
  into a practice: plot rFID against *bits per image* for both methods, where
  the Gaussian side counts its five parameters at whatever precision it
  actually needs. Table 4 is most of the experiment already — it sweeps `K`,
  which is the token count — and needs only the bit accounting and a matched
  VQ sweep beside it.
- **How much precision do the spatial parameters need?** If position, rotation
  and scale survive quantization to a few bits each, the side-channel
  objection shrinks and the representation becomes genuinely discrete, which
  would answer the motivation as well as the evidence problem. The paper does
  not try.
- **Does any of it survive a generation task?** The whole argument for a
  discrete tokenizer is what an autoregressive prior can do with it, and an
  unordered set of indices with continuous attributes is a harder object to
  model, not an easier one. The paper defers this and does not say how it
  would work.
