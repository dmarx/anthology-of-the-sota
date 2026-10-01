---
status: Active
title: 'Perceiver: General Perception with Iterative Attention'
version: 1
tags:
- model-architecture
- attention-techniques
- multimodal-learning
- representation-and-encoding
- vision-and-graphics
date: '2026-10-01'
published: '2021-03-04'
arxiv: '2103.03206'
first_author: 'Jaegle'
# The paper reran ViT-B-16 with its own Fourier-feature inputs and on
# permuted ImageNet (Tables 1, 2, 4), so the comparison is one it ran.
compared_against:
- LIT-587
keywords:
- 'perceiver'
- 'transformer'
- 'cross-attention'
- 'latent-bottleneck'
- 'iterative-attention'
- 'fourier-features'
- 'multimodal'
- 'permuted-imagenet'
- 'audioset'
- 'modelnet40'
summary: >-
  Jaegle et al. (2021), [ARXIV-2103.03206](https://arxiv.org/abs/2103.03206) — the Perceiver. A learned latent
  array of N=512 queries cross-attends to the raw input (50,176 ImageNet
  pixels), so attention costs O(MN) rather than O(M²), and a deep latent
  transformer then runs at O(N²) per layer, independent of input size. With
  2D Fourier-feature positions and no convolution it reaches 78.0% top-1 on
  ImageNet without pretraining, unchanged when the pixels are permuted, while
  ViT-B-16 and ResNet-50 given the same features fall to 61.7 and 39.4. The
  same architecture runs on audio, video and point clouds.
---
<!-- inactive-ok-file: SOTA-tmp34072 — Proposed, filed from this paper in the same contribution -->
<!-- inactive-ok-file: SOTA-403 — Proposed; named as neighbours this paper informs or tests, with their standing stated where they are cited -->

# LIT-tmp7rvm6: Perceiver: General Perception with Iterative Attention

Jaegle et al., DeepMind (2021) — [ARXIV-2103.03206](https://arxiv.org/abs/2103.03206)

## Key takeaways

- **The mechanism: an asymmetric attention bottleneck.** Keys and values are
  projections of the input byte array (size M); queries are projections of a
  learned latent array (size N ≪ M, 512 on ImageNet). That cross-attention
  costs O(MN). A GPT-2-style latent transformer then runs on the N latents at
  O(N²) per layer, so the whole model is O(MN + LN²) and depth is decoupled
  from input size: the best ImageNet model has 48 latent self-attention
  blocks. Cross-attends can be repeated (iterative attention), re-querying the
  input with what the latents already hold; all attention is unmasked.
- **ImageNet, no 2D convolution and no pretraining (Table 1).** 78.0% top-1
  with Fourier-feature positions, against ResNet-50 at 77.6 and ViT-B-16 at
  77.9 from the literature, and 73.5 and 76.7 for the authors' runs of those
  baselines given the same Fourier-feature inputs. A full transformer on
  64×64 downsampled inputs gets 57.0. The model is ~45M parameters, trained
  with LAMB for 120 epochs. The paper notes the no-pretraining state of the
  art at submission was 86.5%, so this is competitiveness with standard
  baselines, not a new best.
- **Permuted ImageNet (Table 2) is the paper's real argument.** One fixed
  permutation of pixels, applied after the position features are computed:
  the Perceiver and the plain transformer are unaffected (78.0, 57.0), while
  ViT-B-16 drops 76.7 → 61.7 and ResNet-50 73.5 → 39.4. With a fully learned
  128-d position encoding instead of Fourier features, so the model has no
  knowledge of 2D structure at all, the Perceiver still gets 70.9 (with one
  cross-attend; eight were unstable with learned positions).
- **Interleaving cross-attends matters, and was ablated (Table 6).** With
  eight cross-attends spread through the network: 78.0. The same eight all
  placed at the start: 73.7. A stack of cross-attention with no latent
  transformer reaches only 45.3 with eight layers (Table 5).
- **Weight sharing is regularisation here (Table 7).** Sharing all
  cross-attends after the first and the corresponding latent blocks cuts
  parameters from 326.2M to 44.9M at the same 707.2B FLOPs, and moves
  validation from 72.9 to 78.0 while training accuracy falls from 87.7 to
  79.5: the unshared model overfits. Sharing the first cross-attend as well
  made training unstable.
- **Position encoding details that carried weight.** Fourier features
  linearly spaced up to a Nyquist-style maximum frequency, concatenated (not
  added) to the input. The NeRF power-of-two bands were numerically unstable
  beyond about k=15 bands. More bands and a higher maximum frequency helped
  (Fig. 6). Coordinates had to be crop-relative rather than image-relative,
  or the model overfit by latching onto a few (RGB, position) pairs.
- **Other modalities, same architecture.** AudioSet (Table 3): 38.4 mAP on
  raw audio, 25.8 on video, 43.5 on audio+video fused at input (44.2 tuned),
  below a late-fusion model at 46.2. Video dropout during training was worth
  more than 3 points (39.7 → 43.5 on raw audio + video). ModelNet40 (Table 4):
  85.7% against 82.1 for a transformer and 78.9 for the best ViT, but below
  the specialised PointNet++ at 91.9, which uses extra geometric features and
  augmentation.
- **What v2 corrected.** The first arXiv version's AudioSet mAPs were wrong,
  and higher, because the class-score matrix was passed to sklearn
  transposed (Appendix F). The numbers above are the corrected ones.

## Standing in the anthology

The primitive is older than this paper. The Set Transformer ([LIT-tmpt8znm](LIT-tmpt8znm.md))
already had learned arrays cross-attend to a large input, and the Perceiver
names it as the most closely related work; what it changes is the
composition. The Set Transformer's induced block maps back to the input size,
so a stack of them pays for the input at every layer, where the Perceiver
keeps the latent array through depth. The record holds no Perceiver IO and
no learned-query resampler. The claim this paper adds (attention through a
small learned array removes the input-size term from depth) is filed as a
practice, [SOTA-tmp34072](../practices.d/SOTA-tmp34072.md).

The comparison it ran is with ViT ([LIT-587](LIT-587.md)), which the authors reimplemented
with the Perceiver's own Fourier-feature inputs. On unpermuted ImageNet the
two are within a point (78.0 against 76.7 for that reimplementation), and the
paper does not claim otherwise. Where it separates them is on permuted
pixels, where ViT's single patch convolution, a 256-pixel receptive field,
costs it 15 points and the Perceiver nothing. That bears on [SOTA-358](../practices.d/SOTA-358.md) from an
unusual side. [SOTA-358](../practices.d/SOTA-358.md) says to drop the domain prior once data is large
enough; the Perceiver drops it entirely on ImageNet-1k alone, which is below
the threshold that practice describes, and lands at ResNet-50's level rather
than above it. It is consistent with the practice's caution rather than a
counterexample: removing the prior was affordable, not profitable, at that
scale.

Two smaller contacts. The Fourier position features are the encoding of
Tancik et al. ([LIT-550](LIT-550.md)), reparameterised with linear rather than random or
power-of-two frequencies; the k=15 instability with NeRF's bands is a
data point for [SOTA-331](../practices.d/SOTA-331.md)'s warning that frequency scale must be tuned. And the
weight-sharing result touches [SOTA-403](../practices.d/SOTA-403.md), which recommends sharing attention but
not feed-forward parameters across depth: the Perceiver shares both and gains
five points, but its unshared baseline was overfitting badly and the paper
does not separate the attention half from the feed-forward half, so it does
not test that practice's distinction.

Unread — no NOTE.
