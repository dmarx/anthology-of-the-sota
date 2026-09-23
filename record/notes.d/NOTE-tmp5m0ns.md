---
status: Read
paper: LIT-tmpcemc9
title: 'The Role of ImageNet Classes in FID'
version: 1
date: '2026-09-23'
summary: >-
  FID can be lowered by two-thirds without changing a generator, by
  resampling its outputs to match ImageNet-class statistics. Non-ImageNet
  feature spaces barely move. An ImageNet-pretrained discriminator gets the
  same effect by accident. Read §1–5; the appendices were skimmed.
---

<!-- inactive-ok-file: SOTA-tmptfakt — Proposed, filed in this same contribution; named because this paper contests it -->

# NOTE-tmp5m0ns: The Role of ImageNet Classes in FID

## Contribution

A demonstration, with a mechanism, that FID contains a large perceptual
null space tied to ImageNet classes, and a practical case where a training
method falls into it.

## Key insight

**FID's features are ImageNet class evidence.** The pool3 features are one
affine map from the logits. So FID rewards matching the distribution of
whatever ImageNet classes the images happen to trigger, whether or not those
matter for the dataset.

## Assumptions

- **Standard FID:** Inception-V3 pool3, 50k generated against the training
  set
- **StyleGAN2 generators** on FFHQ, LSUN Cat, Car and Places, and AFHQ Dog
- **Alternative spaces:** ResNet-50 (ImageNet), SwAV (self-supervised on
  ImageNet), CLIP ViT-B/32

## Key results

- **Table 1 (Top-1 matching):** FID −8.5% to −11.3%. CLIP-FD −0.3% to −2.1%
- **Table 2 (fringe-feature matching):** FID −63% to −72% on four
  datasets. CLIP-FD −4% to −11%
- **§4:** Projected FastGAN against StyleGAN2 on FFHQ: FID 5.28 / 5.30,
  recall 0.45 / 0.46, CLIP-FD 4.67 / 2.76. Humans prefer StyleGAN2

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | FID can be substantially lowered without perceptible change | strong | resampling experiments, five datasets, alternative spaces as controls |
| C2 | The null space is tied to ImageNet classes | strong | the size of the drop tracks how much ImageNet each feature space saw |
| C3 | ImageNet-pretrained discriminators exploit it | moderate | one model on one dataset, with human evaluation |
| C4 | FID is reliable within a setup | weak | the authors' judgment |

## Connections

It contests Projected GAN ([LIT-tmpbzwal](../literature.d/LIT-tmpbzwal.md)). It complements the FID Lottery
([LIT-501](../literature.d/LIT-501.md)), which is about seed variance.

## Recommendations

- **R1** — When ImageNet-pretrained networks take part in training,
  confirm FID gains in a non-ImageNet feature space. Filed as [SOTA-tmprzpgu](../practices.d/SOTA-tmprzpgu.md)

## Bearing on the record

- **[SOTA-tmptfakt](../practices.d/SOTA-tmptfakt.md)** is contested by it
- **[SOTA-307](../practices.d/SOTA-307.md)** addresses variance, and this addresses bias. Both apply

## Limitations

- **CLIP is not neutral either.** It is trained on web image-text data, and
  the authors propose it as a partial check, not a fix
- **One worked example** of the accidental case

## Open questions

- Which feature space, if any, is free of the training data of the models
  being compared
