---
status: Active
title: 'STARFlow: Scaling Latent Normalizing Flows for High-resolution Image Synthesis'
version: 1
tags:
- generative-modeling
- flows-and-transport
- model-architecture
- representation-and-encoding
date: '2026-10-03'
published: '2025-06-06'
arxiv: '2506.06276'
first_author: 'Gu'
keywords:
- 'starflow'
- 'latent-normalizing-flow'
- 'deep-shallow-architecture'
- 'autoregressive-flow-universality'
- 'decoder-finetuning-on-noisy-latents'
- 'gaussian-cfg-for-flows'
implementations: []
extends:
- LIT-tmpvcmj8
compared_against:
- LIT-448
- LIT-447
- LIT-497
- LIT-714
- LIT-566
- LIT-449
- LIT-073
summary: >-
  Gu et al., Apple (2025), [ARXIV-2506.06276](https://arxiv.org/abs/2506.06276). TarFlow moved into a VAE latent
  with a deep-shallow split: one deep Transformer flow block and five 2-layer
  ones. It adds a decoder fine-tuned on noisy latents in place of score
  denoising, and a guidance rule derived from the Gaussian score. ImageNet
  256 FID 2.40 at 1.4B against a retrained pixel TarFlow's 5.56, with SiT's
  quoted 2.06 and MAR's 1.55 still ahead. ImageNet 512 3.00 against EDM2's
  1.25; COCO zero-shot 9.1; GenEval 0.56. The only head-to-head against
  diffusion is a plot against an in-house 2.1B DiT trained on 200M images
  (STARFlow's schedule is 400M) with a stock decoder. Sampling is about 2.2 s per 256×256 image with guidance.
---

<!-- inactive-ok-file: THEORY-tmpx14qc — Proposed; the account filed from this paper's Prop. 1, named in its standing -->

# LIT-tmpnm3dm: STARFlow: Scaling Latent Normalizing Flows for High-resolution Image Synthesis

Gu, Chen, Berthelot, Zheng, Wang, Zhang, Dinh, Bautista, Susskind and Zhai,
Apple (2025) — [ARXIV-2506.06276](https://arxiv.org/abs/2506.06276). Read at v1 (6 Jun 2025), the only version.

## Key takeaways

- **Two blocks are almost universal, three are** (§3.1, Prop. 1, App. A.1).
  One affine autoregressive block makes every conditional a single
  Gaussian. Two blocks in opposite orders make every coordinate but the
  last an infinite Gaussian mixture. A third restores the last. The
  argument is a sketch resting on the density of Gaussian mixtures "with the
  expressive power of neural networks". The ablation agrees: performance
  drops sharply below two blocks and is flat above (Fig. 10e).
- **Put the depth in the first block** (§3.2, App. B.1, Table 5). Guiding
  only the top three of TarFlow's eight blocks already gives the full
  effect (Fig. 3), so STARFlow uses one deep l-layer block (18 or 24) and
  T − 1 two-layer blocks. Only the deep block is conditioned and guided. A
  batch of 16 guided 256×256 samples takes 35 s against 72 s for an
  equal-sized TarFlow of matched parameters (Table 5).
- **Learn in the latent and fix the noise in the decoder** (§3.3, Eqs. 6–7,
  App. C.3, Table 6). The flow models SD-VAE latents with Gaussian noise
  σ = 0.3 added. The decoder is fine-tuned to reconstruct from noisy
  latents with L2, LPIPS and GAN losses. ImageNet 256 FID: decoder
  fine-tuning 2.40, a 30-step DiT denoiser 2.53, TarFlow's single-step
  score denoising 2.96 ("blurry").
- **Guidance from the Gaussian score** (§3.4, Prop. 2, Eq. 9). With
  Gaussian conditional and unconditional predictions, the guided
  distribution is Gaussian with a closed-form mean and variance. Clipping
  the variance ratio to [0, 1] keeps it mode-seeking and stable. TarFlow's
  rule has the same best FID but degrades quickly away from it (Fig. 10b).
- **The numbers.** Class-conditional ImageNet 256: 2.40 at 1.4B (Table 1).
  ImageNet 512: 3.00 (Table 2). Zero-shot COCO FID-30K: 9.1 for a 3.8B
  model on about 700M text-image pairs, 10.3 on CC12M alone (Table 3).
  GenEval overall 0.56 (Table 4).
- **Training needs guards** (App. B.2). The −log σ term is unbounded, so
  outputs are soft-clipped with a tanh, the scale goes through a softplus,
  and intermediate latents carry a 10⁻⁴ norm penalty.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Sample quality approaching that of state-of-the-art diffusion
  models"** (abstract). Against the rows the paper itself prints:
  - ImageNet 256: **2.40** against SiT 2.06 and DiT 2.27 among diffusion
    models, VAR 1.73 and MAR 1.55 among autoregressive ones (Table 1);
  - ImageNet 512: **3.00** against EDM2-XXL's 1.25 (Table 2);
  - COCO: **9.1** against Imagen's 7.3 and eDiff-I's 7.0 (Table 3);
  - GenEval: **0.56** against SD3's 0.74 (Table 4).

  "Approaching" is fair at 256, where 2.40 is within 0.34 of SiT. The rest
  are not close.
- **The 2.40 is above the decoder's own reconstruction FID** (App. B.3).
  Reconstructing 50K real images through σ = 0.3 noise and the fine-tuned
  decoder gives rFID about 2.73, worse than the generated 2.40. The authors
  read this as a ceiling. It also means that at 256 the GAN-trained
  decoder, not the flow, sets the FID.
- **"STARFlow consistently achieves the lowest FID at every training
  checkpoint"** (§4.2, Fig. 10a). Only with 50,000 samples; with 4,096 the
  gap is "smaller". The values are plotted, not tabulated. The authors'
  reading, that STARFlow is more diverse, is untested: no precision,
  recall or diversity metric is reported.
- **Speed.** App. C.1 credits "single-pass inference" with "substantial
  latency advantages over diffusion models". App. C.2 says "the sampling
  speed is still relatively slow", and §6 lists unoptimized inference as a
  limitation. Fig. 10a's diffusion baseline runs 250 steps.
- **One run per setting, no seeds**, and the 1.4B and 3.8B models take
  about two weeks on 32 and 64 H100s (App. B.2).

## Which comparisons are like for like

- **Table 1's normalizing-flow rows are the controlled part.** TarFlow is
  retrained from its official code at 1.3B in pixels (5.56). The same model
  with the deep-shallow split, still in pixels with patch size 8, gives
  4.69. STARFlow, at 1.4B in latents, gives 2.40. The last step changes the
  input space, the patch size and the decoder together.
- **The in-house DiT and LlamaGen (Fig. 10a, App. B.4) are near-matched,
  not matched.**
  - The DiT is 2.1B (28 layers, width 2048), trained on 200M samples at
    batch 256, sampled with 250 steps at guidance 1.5.
  - The LlamaGen is 1.4B, on 200M samples at batch 512.
  - STARFlow is 1.4B and was pretrained on 400M images at batch 512 (§4.1).
    The figure does not say where on that schedule its points sit.
  - The DiT decodes with the stock VAE decoder. STARFlow decodes with one
    fine-tuned for 200K further updates with a GAN loss (App. B.3). Table 6
    puts that decoder 0.56 FID ahead of TarFlow's score denoising; no run
    isolates what it is worth against the stock decoder.
- **Every other row in Tables 1–4 is quoted** from its paper.

## Standing in the anthology

It extends TarFlow ([LIT-tmpvcmj8](LIT-tmpvcmj8.md)). The block is TarFlow's causal-Transformer
affine flow, the noise-augmented training is TarFlow's, and so is the
guidance it starts from. STARFlow retrains TarFlow from the official code as
its baseline. It changes three things, each with an ablation: where depth
goes, which space is modelled, and how guidance is computed.

Its Prop. 1 is filed as [THEORY-tmpx14qc](../theory.d/THEORY-tmpx14qc.md): one affine autoregressive block
cannot represent a multimodal conditional, which is proved and matches
TarFlow's one-block failure, while the claim that three blocks are
universal rests on this paper's sketch.

**On whether exact-likelihood flows have caught up.** With TarFlow, this is
the record's answer, and it is "close at one resolution, not at matched
compute". DiT ([LIT-448](LIT-448.md)) and LlamaGen ([LIT-497](LIT-497.md)) are the two architectures it
retrained as near-matched baselines. Against them STARFlow plots the lowest
50K-sample FID at every checkpoint, but with fewer parameters than the DiT,
an unstated position on its own longer schedule, and a better decoder. On
the published tables it trails SiT ([LIT-447](LIT-447.md)), 2.40 against 2.06 at 256,
and is far behind EDM2 ([LIT-714](LIT-714.md)), 3.00 against 1.25 at 512. In text-to-image
it trails Imagen ([LIT-073](LIT-073.md)) on COCO FID and SD3 ([LIT-449](LIT-449.md)) on GenEval, and
edges SDXL ([LIT-566](LIT-566.md)) on GenEval, 0.56 against 0.55. The likelihood, which is
the reason to want a flow, is plotted (Fig. 10c) but never reported as a
number against anything.

It is evidence for [SOTA-187](../practices.d/SOTA-187.md) from outside diffusion. Moving the same
deep-shallow flow from pixels to latents takes ImageNet 256 FID from 4.69 to
2.40 (Table 1), confounded with the decoder change. It also shows that
practice's stated cost: the decoder bounds the generator, here visibly,
with reconstruction FID above the generated one.

Filed without a `NOTE`: the takeaways come from one full reading of v1,
appendices included, done for this filing. Fig. 10's curves are read only
where the text states values.
