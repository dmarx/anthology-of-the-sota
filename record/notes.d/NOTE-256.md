---
number: 256
status: Read
formerly:
- NOTE-tmpl6noj
paper: LIT-511
title: 'Image-GS: the rate accounting GaussianToken skipped, and an ablation that inverts its own headline'
version: 1
date: '2026-09-21'
summary: >-
  Read from the [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) worklist for its adjacency to the tokenizer trunk. Two
  things worth keeping: a comparison run the way this record keeps asking for
  — six baselines at matched model size, bitrate on the axis — and an ablation
  in which the two unglamorous optimizer choices outweigh the content-adaptive
  allocation the paper is named for.
---

<!-- inactive-ok-file: SOTA-304 — Proposed, and named only as the first of a
     pair of ablations that invert their own headline. The citation is a tally
     entry that this note explicitly declines to promote, not a recommendation
     being leaned on. -->

# NOTE-256: Image-GS: the rate accounting GaussianToken skipped, and an ablation that inverts its own headline

## Contribution

An explicit image representation: a set of anisotropic, colored 2D Gaussians,
each with a mean, a covariance and a color vector, fitted per image by a custom
differentiable renderer. Positions are sampled at initialization from a
weighted mix of local image-gradient magnitude and a uniform constant, so more
primitives land on high-frequency regions while the whole image stays covered.
More Gaussians are added every 0.5K steps into regions with persistent error,
starting from half the budget.

## Key results

**The comparison is run the way this record keeps asking for.** Six neural
image representations — ReLU-F, SIREN, FFN, WIRE, I-NGP and GI — plus JPEG,
using the baselines' official implementations with only model size changed to
reach the target range. At 2K×2K the model sizes are **164, 166, 161, 154,
159, 164 and 160 KB** for ReLU-F, I-NGP, SIREN, FFN, WIRE, GI and Image-GS.
Bitrate is on the axis throughout, in bpp and bits per pixel per channel.

Image-GS outperforms all six across the evaluated bitrate range and passes
JPEG below **0.244 bpp**. The paper immediately qualifies its own win: JPEG
and GI use entropy coding, which Image-GS does not, and entropy coding breaks
the data locality that the random-access claim depends on. Naming what the
baselines have that you lack, in the sentence announcing the win, is rarer
than it should be.

**Quality against rate**, 45-image evaluation set:

| bitrate | PSNR | MS-SSIM | LPIPS | FLIP |
|---|---|---|---|---|
| 0.366 bpp | 32.99 ± 4.49 | 0.966 ± 0.020 | 0.083 ± 0.057 | 0.078 ± 0.029 |
| 0.122 bpp | 29.20 ± 4.57 | 0.924 ± 0.042 | 0.173 ± … | — |

**Decode cost is the number that carries the practice.** 0.3K multiply-
accumulates per pixel, against C3's **3K MACs at 0.31 bpp** — an order of
magnitude — with hardware-friendly random access and a level-of-detail stack
that falls out of the error-guided growth order.

**The ablation inverts the headline.** Table 1, on the same evaluation set:

| variant | PSNR | MS-SSIM | LPIPS | cost against Full |
|---|---|---|---|---|
| **Full** | **31.77 ± 4.73** | 0.960 | 0.102 | — |
| No color init | 30.40 ± 4.73 | 0.951 | 0.110 | −1.37 |
| No position init | 29.88 ± 4.18 | 0.954 | 0.135 | −1.89 |
| Random init (both off) | 29.54 ± 4.15 | 0.948 | 0.149 | −2.23 |
| No top-K normalization | 29.35 ± 4.43 | 0.944 | 0.182 | **−2.42** |
| No inverse scale | 29.11 ± 4.58 | 0.933 | 0.152 | **−2.66** |

The content-adaptive allocation the paper is named for is worth **2.23 dB**
with both components removed. Optimizing `1/s` instead of the raw Gaussian
scale — a reparameterization justified in one sentence, because the natural
range is `[5,10]` and the inverse lands in `[0,1]` where gradients are
smoother — is worth **2.66**. Top-K normalization is worth **2.42**. Two
implementation choices each outweigh the idea in the title.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | An explicit primitive set beats implicit coordinate networks for single images at low bitrate | strong | six baselines, official implementations, matched KB, bitrate axis |
| C2 | Decode cost is an order of magnitude below a comparable neural codec | strong | 0.3K vs 3K MACs/pixel at comparable bpp |
| C3 | Content-adaptive allocation is what makes it work | **overstated** | worth 2.23 dB; two optimizer details are worth more, by the paper's own Table 1 |
| C4 | The level-of-detail hierarchy is free | moderate | falls out of the growth order; no separate cost reported, and no comparison against a purpose-built LOD scheme |

## Limitations

**Per-image fitting, not a learned codec.** Every image is an optimization run
— 5K Adam steps. Against autoencoder codecs trained across a dataset this is a
different product with a different cost model, and the paper is comparing
against overfit-per-image baselines, which is the right comparison for its
claim and not the one someone shipping a general codec wants.

**No seeds anywhere.** Means and standard deviations are across the 45-image
evaluation set, not across optimization runs. The ablation gaps are 1.4–2.7 dB
against a per-image spread of ±4.5, so the image-to-image variance dominates
and the run-to-run variance is unreported.

**The ablation is one budget.** Whether the ordering of those five choices
holds at 0.122 bpp as well as at the ablation's operating point is untested,
and the interesting question — does the content-adaptive allocation matter
*more* as the budget tightens, which is the regime the paper claims — is
exactly the one the table does not answer.

**Entropy coding is left on the table and acknowledged.** The paper declines
it for locality, which is a real engineering reason, and it means the reported
bitrates are not the best this representation could do.

## Bearing on the record

**[SOTA-205](../practices.d/SOTA-205.md) gains a fifth source and its first outside 3D.** Four
radiance-field papers argued that capacity should move out of the network into
a structure that is addressed rather than evaluated. This is the same claim
for a single image, and 0.3K against 3K MACs per pixel is the cleanest
statement of what "addressed rather than evaluated" buys.

**The constructive contrast with [LIT-494](../literature.d/LIT-494.md).** GaussianToken landed two
units earlier with comparisons matched on token count while each token carried
an index plus five continuous floats, and [NOTE-243](NOTE-243.md) recorded that nothing
ruled out the rival explanation that it simply had more channel. Image-GS is
the same primitives in the same year with bits per pixel on the axis and
model sizes matched in kilobytes. The two are not compared by anybody and no
relation is declared — [ADR-011](../decisions.d/ADR-011.md) — but holding both is what makes the
criticism of the first precise rather than general, and it is the answer to
the open question [NOTE-243](NOTE-243.md) left.

**Second instance of an ablation inverting its own headline, counted not
promoted.** [SOTA-304](../practices.d/SOTA-304.md) records the first: in Genesys, removing the symbolic
checker costs 62 points of validity and removing the clever unit-wise
decomposition costs 19, so the boring half is three times the lever. Here the
reparameterization and the normalization each outweigh the content-adaptive
allocation. Two instances from unrelated fields is a count. What would make it
more is a mechanism, and "papers name themselves after the interesting half"
is a sociological observation rather than one — [DP-009](../../docs/design-principles.md#dp-9).

**No new practice.** Content-adaptive densification is what [LIT-108](../literature.d/LIT-108.md)
already does in 3D and what [SOTA-205](../practices.d/SOTA-205.md) already covers at the level that
matters; a 2D instance adds a source, not a recommendation. The `1/s`
reparameterization is the most surprising number here and rests on one
sentence in one paper about one parameter — an open question below rather than
a practice.

## Open questions

- **Does the `1/s` reparameterization generalize?** It is worth more than the
  paper's headline idea and is justified in a single sentence: optimize the
  inverse when the natural range sits away from zero, because `[0,1]` gives
  smoother gradients. If that holds for other bounded-away-from-zero
  parameters — scales, temperatures, bandwidths — it is a practice; here it is
  one measurement on one parameter.
- **Does content-adaptive allocation matter more as the budget tightens?** The
  paper's claim is about low-bitrate regimes and its ablation is at one
  operating point.
- **What does the rate curve look like against GaussianToken's task?** Nobody
  has run a Gaussian image representation and a Gaussian image *tokenizer*
  against each other at matched bits. Both exist, both are public, and the
  comparison is the one [NOTE-243](NOTE-243.md) asked for.
