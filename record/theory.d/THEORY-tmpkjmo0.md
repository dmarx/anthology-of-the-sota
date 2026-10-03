---
status: Proposed
promote_when: >-
  An experiment that separates the two reasons TarFlow offers and that its
  ablation cannot tell apart. One is support: the inverse is trained only near
  a nearly discrete set and must generalize to the whole Gaussian. The
  other is conditioning: a narrow noise forces a low-entropy distribution
  onto an ambient Gaussian. Measuring the inverse's Jacobian conditioning,
  or its reconstruction error on held-out latents, against the training
  noise level would test the second. Holding the noise level fixed and
  varying only its shape, uniform against Gaussian at equal variance, would
  test what the Gaussian tail adds. A second architecture family, coupling
  or continuous-time, showing the same failure on dequantization noise would
  show the effect is about likelihood-trained flows rather than TarFlow. A
  further flow that samples well with noise augmentation would not count.
title: "A likelihood-trained normalizing flow samples well only when its training data carry Gaussian noise well above the quantization width, because its inverse must be well conditioned over the whole Gaussian latent"
version: 1
tags:
- generative-modeling
- flows-and-transport
date: '2026-10-03'
source:
- LIT-tmpvcmj8
- LIT-tmpnm3dm
summary: >-
  Zhai et al. (2024), [LIT-tmpvcmj8](../literature.d/LIT-tmpvcmj8.md), §2.4 and §3.3. Trained on the uniform
  dequantization noise that likelihood evaluation uses, TarFlow could not
  sample: "constant numerical issues" and nothing sensible. Gaussian noise
  of standard deviation about 0.05, against the dequantization noise's
  0.002, gave its best samples. The authors offer two reasons and a
  hypothesis, and test none of them apart. STARFlow ([LIT-tmpnm3dm](../literature.d/LIT-tmpnm3dm.md)) keeps the
  noise, at 0.3 in latent space, on TarFlow's word. One ablation from one
  group, and an account that is the authors' own guess.
---

# THEORY-tmpkjmo0: A likelihood-trained normalizing flow samples well only when its training data carry Gaussian noise well above the quantization width, because its inverse must be well conditioned over the whole Gaussian latent

## Source

Zhai, Zhang, Nakkiran, Berthelot, Gu, Zheng, Chen, Bautista, Jaitly and
Susskind (2024), [LIT-tmpvcmj8](../literature.d/LIT-tmpvcmj8.md), §2.4–2.5, §3.3 and Fig. 4. Gu, Chen,
Berthelot et al. (2025), [LIT-tmpnm3dm](../literature.d/LIT-tmpnm3dm.md), §3.3.

## What was shown

**The observation.** TarFlow ([LIT-tmpvcmj8](../literature.d/LIT-tmpvcmj8.md)) is trained by exact maximum
likelihood. Trained on uniform noise one quantization bin wide, the
convention for reporting likelihood, "sampling experiences constant
numerical issues and was not able to produce sensible outputs" (§3.3).
Trained on Gaussian noise, it samples. With pixels in [−1, 1], the best σ
for sample quality is about 0.05, while the dequantization noise's standard
deviation is 0.002 (§2.4). Raw-sample FID favours the smallest σ, and after
denoising a moderate one wins (Fig. 4). The likelihood headline, 2.99
bits/dim, comes from a uniform-noise model that the paper says cannot
sample, so the paper's best likelihood and best samples come from
different models.

**The reasons offered.** §2.4 asks "Why is this the case?" and gives "two
factors which could be important". First, support. Without noise the
inverse is trained on a set the size of the training set, and at sampling
time it must generalize to a dense Gaussian input, "an out-of-distribution
problem". Second, shape. A Gaussian "stretches the support of the training
distribution to the ambient input space, with the mode of the density
placed at the original data points", which a narrow uniform box does not.
§3.3 adds a hypothesis for the uniform failure: "a narrow uniform noise
makes the flow transformation ill-conditioned, as it forces a model to map
a low entropy distribution to an ambient Gaussian distribution."

**What it costs, and how it is paid.** A model of noisy data samples noisy
images. TarFlow removes the noise with Tweedie's formula, using the flow's
own score (§2.5). STARFlow ([LIT-tmpnm3dm](../literature.d/LIT-tmpnm3dm.md), §3.3) cites TarFlow that a
"proper amount of Gaussian noise … is crucial for stable training and high
quality sampling", adds σ = 0.3 noise to its autoencoder latents, chosen
by a preliminary search, and fine-tunes the decoder to read noisy latents
instead of denoising. STARFlow tests the denoiser, not the noise.

## What this does not say

- **Which of the reasons is right.** The account in the title is the
  conditioning reading, chosen because it alone explains why *uniform*
  noise fails outright rather than merely sampling worse. TarFlow states it
  as a hypothesis, and no experiment in either paper measures conditioning.
  The support reading predicts a graded loss of quality, not numerical
  failure, and the sweep in Fig. 4 cannot distinguish them.
- **That the noise level is principled.** Both papers chose σ by search,
  0.05 in pixels and 0.3 in a latent space, and the ablation models trained
  100 epochs against 320 for the reported runs.
- **Anything about flows other than TarFlow's.** The failure is reported
  for one causal-Transformer affine flow. Glow ([LIT-tmp086g1](../literature.d/LIT-tmp086g1.md)) trained on
  uniform dequantization noise and did produce samples, but chose to sample
  at temperature 0.7, shrinking the latent toward its centre, and reads the
  noisy high-temperature samples as the model overestimating the data's
  entropy (§6). That is consistent with an inverse that is poor far out in
  the latent, and it is not a test of it. Neither paper here runs a
  coupling flow.
- **That this makes a flow a diffusion model.** The resemblance is real.
  The model is fitted by likelihood to Gaussian-noised data at one noise
  level, and denoised by the score. [THEORY-107](THEORY-107.md) shows a diffusion loss with
  a monotone weighting is likelihood on noise-augmented data over a whole
  range of levels. Here there is one level and an exact likelihood, and
  nothing in the sources connects the two accounts.
