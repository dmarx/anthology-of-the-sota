---
status: Read
paper: LIT-623
title: 'MAGVIT-v2'
version: 1
date: '2026-09-24'
summary: >-
  A causal 3D-CNN video tokenizer with lookup-free quantization (sign-binary
  latents plus an entropy penalty) improves a fixed ~307M masked token model
  on Kinetics-600 frame prediction from FVD 9.9 to 5.2 at equal decoding
  steps. The claim that LFQ, unlike VQ, keeps improving generation as the
  vocabulary grows rests on a figure with no numbers. "Beats diffusion" holds
  only with guidance (1.78 against MDT's 1.79 at 256, 1.91 against VDM++'s
  2.65 at 512), and the strongest diffusion baselines at 512 are about 6×
  its size.
---

# NOTE-tmpesnac: MAGVIT-v2

Read in full from arXiv 2310.05737v3 (29 Mar 2024, ICLR 2024): main text
and Appendices A–B, including Tables 6–8 and Figs. 7–9. Plotted values in
Figs. 1, 6 and 9 are not in the extracted text, so only the direction of
those curves is used below. The project page's samples were not viewed.

## Contribution

A video tokenizer, MAGVIT-v2, with two changes over MAGVIT. **Lookup-free
quantization (LFQ)** replaces the codebook: each of log₂K latent dimensions
is sign-quantized to {−1, 1}, and the token index is the resulting binary
number (Eqs. 3–4). An entropy penalty encourages codebook use (Eq. 5). A
**temporally causal 3D CNN** encoder lets the first frame be tokenized
alone, so a still image is a valid one-frame video (§3.2). There are smaller
architecture changes (strided-conv downsamplers, depth-to-space upsamplers,
late temporal downsampling, adaptive GroupNorm, 3D blur pooling), and a
token factorization so that a ~300M transformer can predict over 2^18
entries (§3.2).

## Key insight

**The vocabulary is where reconstruction and generation diverge.** A larger
VQ codebook reconstructs better, but past a point the generator does worse
on it. The paper's reading is that per-token capacity has to shrink as the
vocabulary grows. LFQ takes that to the limit of zero embedding dimension
(§3.1, crediting the ViT-VQGAN trick). The second insight is structural:
**causal padding makes frame 0 independent**, and with stride s mapping
1 + s·t frames to 1 + t latents, images and video share one latent layout.

## Assumptions

- **A masked, non-autoregressive LM** (MaskGIT/MAGVIT style) is the
  generator throughout the main results, decoded in 12–64 steps (§4.2). The
  one AR-LM result is in App. B (Table 8).
- **Independent binary dimensions.** The paper studies "the simplest form"
  of LFQ and leaves other variants to future work (§3.1).
- **Separate tokenizers per task.** Image tokenizers are trained on ImageNet
  at 16× and 32× downsampling. The video tokenizer is inflated from a
  128×128 image tokenizer and trained on Kinetics-600 for 190 epochs
  (App. A.1).
- **Comparability with diffusion baselines** is asserted as "the same
  training data, with a comparable model size and training budget" (§4.2)
  and never quantified.

## Key results

- **Video generation** (Table 1, MLM, ~307M). Kinetics-600 frame prediction
  FVD: MAGVIT 9.9 ± 0.3 at 12 steps, non-causal LFQ baseline 11.6 ± 0.6 at
  12, MAGVIT-v2 5.2 ± 0.2 at 12 and 4.3 ± 0.1 at 24. UCF-101: MAGVIT 76 ± 2 at
  12 steps, MAGVIT-v2 58 ± 3 **at 24 steps**. No 12-step UCF number is given
  for MAGVIT-v2. The diffusion baselines are VDM (16.2, 1.1B) and RIN
  (10.8, 411M), both on K600 only.
- **ImageNet 512** (Table 2). Unguided: 4.61 at 12 steps and 3.07 at 64,
  against VDM++ 2.99 and simple diffusion 3.54 (both 2B). Guided: 1.91
  against VDM++ 2.65. MAGVIT-v2 has 307M parameters.
- **ImageNet 256** (Table 7). Unguided 3.65 against VDM++ 2.40. Guided 1.78
  against MDT 1.79 (676M) and VDM++ 2.12.
- **Tokenizer ablations, cumulative.** ImageNet 128 reconstruction FID:
  MAGVIT 2.65, +LFQ 2.48, +large vocabulary 1.34, +up/downsampler 1.21,
  +deeper 1.20, +adaptive norm 1.15 (Table 5b). UCF-101 video FVD: 24.55 →
  16.12 (LFQ and large vocabulary) → 15.37 → 11.11 (late temporal
  downsampling) → 8.90 → 8.62 (Table 5c).
- **Causal architectures on UCF-101** (Table 5a, FVD, with first-frame
  FID): MAGVIT 107.15 (39M, no FID possible), C-ViViT 437.54 / 28.02 (90M),
  C-ViViT + MAGVIT 316.70 / 13.52 (67M), causal 3D CNN 96.33 / 7.06 (58M).
- **Compression at 0.0384 bpp** (Table 3). LPIPS 0.104 against VVC 0.153,
  but PSNR 26.18 against 32.65 and MS-SSIM 0.894 against 0.966. Raters
  prefer MAGVIT-v2 by Elo: 16 raters, 30 MCL-JCV videos, about 800 pairs
  each (Fig. 6, App. A.3).
- **Action recognition** (Table 4). As input, 75.34 on K400 against raw
  pixels 76.13. As SSv2 targets, 67.38 against MAGVIT 67.22.
- **AR-LM on UCF-101** (Table 8): FVD 109 (840M, 1280 steps) against
  MAGVIT's 265 (306M, 1024 steps).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | With the same MLM backbone, the new tokenizer improves video generation | strong | K600 9.9 → 5.2 at equal steps, with ± bands (Table 1) |
| C2 | With LFQ, generation keeps improving as vocabulary grows, while with VQ it turns worse | weak | Fig. 1 only, with no numbers in text, at 128×128 with a 306–372M MLM |
| C3 | Causality in the tokenizer helps generation | moderate | 11.6 → 5.2 against a "non-causal baseline" on frame prediction, which is not described further (Table 1) |
| C4 | The causal 3D CNN is the best causal tokenizer architecture | moderate | Table 5a. Parameter counts differ (58M against 90M and 67M), and the table does not say whether its FVD is reconstruction or generation |
| C5 | A masked LM beats diffusion on ImageNet at the same data, comparable size and budget | weak | holds only with guidance. The 512 baselines are 2B against 307M, and budget is not quantified. At 256 the margin is 0.01 FID |
| C6 | The architecture changes (up/downsamplers, late temporal downsampling, adaptive norm, depth) improve the tokenizer | moderate | cumulative ablation, reconstruction only (Tables 5b, 5c). Not shown on generation |
| C7 | As a codec it is comparable to or better than VVC | weak | holds on LPIPS and rater Elo. Clearly worse on PSNR and MS-SSIM, and runs on TPU, not CPU |
| C8 | Images and video share one tokenizer and vocabulary | weak | an architectural property. No experiment generates images with the video tokenizer. Closest is first-frame FID (Table 5a) |

## Method

LFQ: encoder output z ∈ R^{log₂K}. Quantize q(z_i) = sign(z_i) and take
index Σ 2^{i−1}·1[z_i > 0]. Train with reconstruction, GAN, perceptual and
commitment losses, the entropy penalty E[H(q(z))] − H[E(q(z))] (weight 0.1,
annealed from 3× over 2k steps), and LeCAM. There is no codebook loss.
Causal 3D conv: pad k_t − 1 frames before and none after. 17×128×128 clips
become 5×16×16 tokens at vocabulary 2^18 (App. A.2). The generator is
MAGVIT's MLM with the 2^18 vocabulary factorized into two 2^9 heads and
weight-tied embeddings (§3.2, §4.2).

## Concepts

- **Lookup-free quantization.** Quantization with no codebook embeddings.
  The code is the sign pattern of the latent. K = 2^d for d latent
  dimensions.
- **Causal tokenizer.** Each latent frame depends only on current and past
  input frames, so frame 0 is tokenized as an image.
- **Token factorization.** One 18-bit token is predicted as two 9-bit
  sub-tokens with separate heads, so that a small LM can model a 262K
  vocabulary.
- **"Language model."** In this paper it mostly means a bidirectional
  masked token model, not an autoregressive LLM.

## Connections

It extends MAGVIT (same group) and takes its motivation from ViT-VQGAN's
low-dimensional codes ([LIT-500](../literature.d/LIT-500.md)). It compares against VDM ([LIT-627](../literature.d/LIT-627.md)) and RIN
on video and against LDM ([LIT-062](../literature.d/LIT-062.md)), DiT, MDT and VDM++ on images. Its causal
first-frame design is what later continuous video VAEs adopt with a KL
bottleneck instead of LFQ (Wan, CogVideoX, HunyuanVideo, per the LIT note).

## Recommendations

- **R1. Make a video tokenizer temporally causal with frame 0 encoded
  alone**, so that images and videos share a latent format. *Topic:*
  representation-and-encoding. *Status:* standard. *Strength:* moderate.
  *Conditions:* the generation evidence is on frame prediction, where a
  causal tokenizer respects the conditioning boundary by construction. Gains
  on unconditional generation are not isolated.
- **R2. When scaling a discrete tokenizer's vocabulary, check generation,
  not only reconstruction**, because the two can move in opposite
  directions. *Topic:* analysis-and-evaluation. *Status:* standard.
  *Strength:* moderate. It is argued, and supported qualitatively by Fig. 1.
- **R3. Consider LFQ (sign-binary codes plus an entropy penalty) for large
  vocabularies.** *Topic:* representation-and-encoding. *Status:*
  experimental. *Strength:* weak on generation (C2), moderate on
  reconstruction (Table 5b).
- **R4. Delay temporal downsampling to the later encoder blocks.** *Topic:*
  model-architecture. *Status:* experimental. *Strength:* moderate on
  reconstruction (15.37 → 11.11 FVD, Table 5c). Not shown on generation.

## Bearing on the record

| practice | disposition |
|---|---|
| [SOTA-305](../practices.d/SOTA-305.md) compare tokenizers only at equal rate | **the paper's ablation does not do this** |
| [SOTA-306](../practices.d/SOTA-306.md) factorize the codebook, low lookup dimension | extended: LFQ is the zero-dimension limit, argued from the same intuition |
| [SOTA-307](../practices.d/SOTA-307.md) FID over training seeds | C5 at 256 (1.78 against 1.79) is far inside its noise floor |
| [SOTA-187](../practices.d/SOTA-187.md) train in a learned latent | consistent. Discrete rather than continuous |
| [SOTA-386](../practices.d/SOTA-386.md), [SOTA-390](../practices.d/SOTA-390.md), [SOTA-389](../practices.d/SOTA-389.md), [SOTA-266](../practices.d/SOTA-266.md), [SOTA-333](../practices.d/SOTA-333.md) | no bearing |

**[SOTA-305](../practices.d/SOTA-305.md).** Table 5b's largest step, "+ large vocabulary" (2.48 → 1.34
rFID), raises bits per token at a fixed token count. It is a rate increase
reported alongside rate-neutral changes. The compression comparison
(Table 3) *is* at equal bpp, and it is the one place the paper controls for
rate. This is a worked example for [SOTA-305](../practices.d/SOTA-305.md), not a contradiction of it.

**[SOTA-306](../practices.d/SOTA-306.md).** That practice finds an interior optimum in lookup dimension
(16, 8 and 3 across its sources). LFQ goes to one bit per dimension with no
embedding, and claims monotone improvement with vocabulary. The two do not
conflict, because LFQ changes the construction (no nearest-neighbour search)
rather than moving along [SOTA-306](../practices.d/SOTA-306.md)'s axis. But C2 is too weak to add LFQ to
that practice as a source.

**[SOTA-307](../practices.d/SOTA-307.md).** "Beats diffusion" at 256 is a 0.01 FID gap from one run. By
that practice's threshold it is inconclusive. The 512 margin (1.91 against
2.65) is large enough to survive it.

**Should produce:** R1 as a practice, sourced here. The LIT note's claim
that later video VAEs share the design is adoption ([DP-005](../../docs/design-principles.md#dp-5)) and belongs in
`consensus:`.

## Limitations

- **C2, the paper's central LFQ claim, is a curve without numbers.** Table 5b
  shows LFQ plus a larger vocabulary improving *reconstruction*. Nothing
  numeric shows generation.
- **Architecture changes are validated on reconstruction only** (Tables 5b,
  5c).
- **"Comparable model size"** does not match its own Table 2, where the
  strongest diffusion baselines at 512 are 2B against 307M. Tokenizer
  parameters are not counted in #Params.
- **No text conditioning.** App. B says text-to-video results were "not
  available at the moment".
- **The ± in Table 1 is not defined.** It may be sampling variation, not
  training seeds.

## Open questions

- What are the numeric Fig. 1 curves, and does LFQ generation still improve
  past 2^16?
- Does causality help unconditional video generation, or only frame
  prediction where it matches the conditioning boundary?
- Is the UCF gain (76 → 58) still there at equal decoding steps?

## Corrections to the LIT note

- **[LIT-623](../literature.d/LIT-623.md) says:** "With the MLM backbone unchanged, Kinetics-600 FVD goes
  from 9.9 to 5.2 and UCF-101 FVD from 76 to 58 (Table 1)." **Fix:** "K600
  goes 9.9 → 5.2 at 12 decoding steps each. UCF-101 goes 76 (MAGVIT, 12
  steps) → 58 (MAGVIT-v2, 24 steps). Table 1 reports no 12-step UCF number
  for MAGVIT-v2. The backbone also changes slightly: the 2^18 vocabulary is
  factorized into two 2^9 heads with weight tying (§3.2, §4.2)."
- **[LIT-623](../literature.d/LIT-623.md) says:** "With LFQ, reconstruction and generation both keep
  improving up to about 2^18 (Fig. 1, a controlled sweep on ImageNet 128)."
  **Fix:** "Fig. 1's vocabulary axis is labelled 10–16 (2^10–2^16) in the
  extracted text. 2^18 is the vocabulary used in the experiments (§4.1), not
  a point the sweep is shown to reach. The figure gives no numbers." This
  should be checked against the rendered figure.
- **[LIT-623](../literature.d/LIT-623.md) says:** "It beats C-ViViT variants on reconstruction FVD, 96
  against 437 and 317 (Table 5a)." **Fix:** "Table 5a does not say whether
  its FVD is reconstruction or generation. Its MAGVIT row (107.15) does not
  match MAGVIT's reconstruction FVD in Table 5c (24.55). Parameter counts
  differ (58M, 90M, 67M)."
- **[LIT-623](../literature.d/LIT-623.md) says:** "The causal design lets images and video share one
  tokenizer". This is true of the architecture. **Add:** "No experiment
  uses the video tokenizer for images. ImageNet results use separate
  ImageNet-trained image tokenizers (App. A.1)."
