---
status: Read
paper: LIT-tmpb17dj
title: 'VQGAN: the loss that made f=16 survivable'
version: 1
date: '2026-09-21'
summary: >-
  Read as the second step of the tokenizer trunk. The architecture is
  VQ-VAE's; what is new is a perceptual loss, a patch discriminator, and an
  adaptive weight that balances them without per-dataset tuning. That loss is
  the reason a `256×256` image can become 256 tokens and still look like
  anything, and it is why this line exists at all.
---

# NOTE-tmpgjjku: VQGAN: the loss that made f=16 survivable

## Contribution

Turned a compression scheme into a usable vocabulary. VQ-VAE could discretize
images; at the compression ratios a transformer needs, its reconstructions
were blurry, because an `L2` reconstruction objective at 16× downsampling
optimizes for the mean of everything the code cannot distinguish. Replacing
that objective with a perceptual loss plus a patch-based adversarial term
changes what "good reconstruction" means — from pixel-accurate to
distributionally plausible — and at that point `f = 16` becomes survivable.

The second contribution is the pairing: a CNN for the vocabulary, a
transformer for the composition. The paper's argument is explicitly about
cost — transformers are expressive and quadratic, so shorten the sequence
first with the thing that has the right inductive bias.

## Key insight

The bottleneck is not how many bits you keep but which error you are willing
to make. Pixel-wise loss at high compression produces a blur that is optimal
under that loss and useless as a vocabulary. Perceptual plus adversarial loss
lets the decoder *invent* detail that was never in the code, which is exactly
the right trade when the code's job is to carry identity and the decoder's job
is to carry texture.

## Assumptions

- The adversarial term needs balancing against reconstruction, and the paper
  assumes the right balance is the ratio of their gradient magnitudes at the
  decoder's final layer rather than a tuned constant.
- A patch discriminator, not a whole-image one — the assumption is that
  realism at this compression is a local property.
- High-resolution synthesis assumes locality in the prior too: attention is
  applied in a sliding window rather than over the whole token field, so the
  transformer never conditions on the full image.
- Raster-scan autoregressive ordering over the token grid. Assumed, not
  argued, and rejected two years later by [LIT-tmpig8jj](../literature.d/LIT-tmpig8jj.md).

## Key results

- **The objective** adds to VQ-VAE's loss a perceptual term and
  `λ · L_GAN`, with
  `λ = ∇_{G_L}[L_rec] / (∇_{G_L}[L_GAN] + δ)`, gradients with respect to the
  decoder's last layer `G_L`.
- **Only the full `f = 16` setting synthesizes high fidelity**, per the
  paper's sweep over compression ratios — lower `f` leaves the sequence too
  long for the transformer, higher `f` loses too much to recover.
- **Sliding-window attention** yields the first semantically-guided megapixel
  synthesis with transformers.
- State of the art among autoregressive models on class-conditional ImageNet
  at the time, and conditional synthesis from both non-spatial conditions
  (class) and spatial ones (segmentation maps).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Perceptual + adversarial losses make high-compression discrete tokenization viable | strong | the compression-ratio ablation, and the entire subsequent literature runs this loss |
| C2 | The adaptive `λ` removes the need to tune the adversarial weight | moderate | stated with its formula, not ablated against a tuned constant in what I read |
| C3 | CNN vocabulary + transformer composition beats either alone at high resolution | strong | that is what the results are |
| C4 | Raster-order autoregressive modelling of the tokens is the right prior | weak | assumed, never argued, and later overturned on both speed and quality |

## Method

Encoder and decoder are convolutional; the codebook and straight-through
gradient are VQ-VAE's. Training adds an LPIPS-style perceptual term and a
patch discriminator whose weight is set adaptively per step by the gradient
ratio above. Once trained, an image becomes a grid of codebook indices, which
is flattened in raster order and modelled by an autoregressive transformer;
conditioning information is prepended or, for spatial conditions, encoded into
its own token grid. Megapixel synthesis slides an attention window over the
token field.

## Concepts

- **context-rich vocabulary** — the paper's term for what the codebook
  becomes once the loss stops demanding pixel accuracy: entries stand for
  perceptual constituents rather than for local colour statistics.
- **adaptive weight `λ`** — the gradient-ratio balance. The one number
  reimplementers most often get wrong.
- **`f`** — downsampling factor. `f = 16` on `256×256` gives the 16×16 token
  grid that is still the default in this line eight years later.

## Connections

Extends [LIT-tmpxz6hg](../literature.d/LIT-tmpxz6hg.md) directly and declares it. Extended by
[LIT-tmpig8jj](../literature.d/LIT-tmpig8jj.md), which keeps the tokenizer and discards the raster
order, and by [LIT-tmpflmiq](../literature.d/LIT-tmpflmiq.md), which keeps both and retunes the
codebook. [LIT-494](../literature.d/LIT-494.md) plugs its Gaussian module into this
architecture and compares against it.

Two of these three authors go on to latent diffusion, which is this
autoencoder with the quantization removed — the object behind
[SOTA-187](../practices.d/SOTA-187.md), which the record already held. The discrete and
continuous branches of "compress first, generate in the latent" come from the
same place, and the record now holds both roots.

## Recommendations

- **R1** — use a perceptual plus adversarial reconstruction objective when the
  compression is high enough that pixel-wise loss would blur. **Not filed as a
  practice**: it is the substrate of the whole line now rather than a choice
  anyone weighs, and no source in this record measures it against the
  alternative.
- **R2** — set the adversarial weight by the gradient ratio rather than by
  hand. *Strength:* moderate. **Not filed**, for a specific reason: I did not
  find an ablation against a tuned constant. It is a good idea that is
  universally copied, which `DP-005` says is not the same as evidence.

## Bearing on the record

Second step of the trunk [#243](https://github.com/dmarx/anthology-of-the-sota/issues/243) named, and the one that explains why
the trunk mattered — without this loss there is no 16×16 token grid, and
without that there is no image-as-sequence line to have a gap in.

The practices filed in this contribution are both about the *codebook*, which
this paper inherited from VQ-VAE and did not retune; the retuning is
[LIT-tmpflmiq](../literature.d/LIT-tmpflmiq.md)'s.

## Limitations

- **The adaptive `λ` is presented, not validated.** A formula with a `δ` in
  the denominator, no sweep against a constant weight in what I read.
- **Raster order is never justified.** It is inherited from text and it is
  wrong, by a factor of 32 in steps and 9.6 FID points, which MaskGIT
  establishes two years later.
- **Adversarial training's instability is not discussed** in what I read, and
  it is the reason tokenizer training is hard to reproduce.
- **Codebook utilization is not measured here either**, continuing VQ-VAE's
  omission. The codebook this line spent the next four years fixing is
  untouched in the paper that made the line matter.
- **`f = 16` is the right answer for a 2020 transformer's context budget.**
  The sweep that found it was run against that constraint, and the constraint
  has moved.

## Open questions

- **Does the adaptive weight beat a tuned constant?** Cheap, never published
  as far as this reading found, and everyone uses the formula.
- **What does the perceptual loss's backbone contribute?** LPIPS-style losses
  carry the biases of their feature extractor into every tokenizer trained
  with them, and no source here separates that from the adversarial term.
