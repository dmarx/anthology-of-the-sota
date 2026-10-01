---
number: 436
status: 'Proposed'
formerly:
- SOTA-tmp34072
promote_when: >-
  A comparison at matched FLOPs between a latent-bottleneck model and a
  patch- or grid-based transformer, run at two or more input sizes, showing
  that the bottleneck's accuracy per FLOP improves as the input grows. That is
  the claim this practice rests on, and the source states it from asymptotics
  without measuring it: it reports no FLOPs for its baselines. A second group
  showing the same architecture holding up on an input that a grid model cannot
  take natively, such as point clouds or several modalities fused at the input,
  would also move it. A later model that uses a learned-query resampler counts
  as adoption, not evidence.
consensus: unassessed
consensus_note: >-
  Learned-query cross-attention into a small latent array has been widely
  adopted since, but the record holds none of the papers that did so, and this
  reading did not survey them. The evidence here is one group, one paper
  (LIT-747). Read as of 2026-10.
title: 'Route a very large or non-grid input through cross-attention into a small learned latent array, so that depth no longer scales with input size'
version: 1
tags:
- model-architecture
- attention-techniques
- multimodal-learning
date: '2026-10-01'
source:
- LIT-747
# The source credits the cross-attention primitive to the Set Transformer
# (Lee et al. 2019, arXiv 1810.00825), whose ISAB and PMA blocks map a large
# set to a small array. It argues that a stack of ISABs still scales with the
# input at every layer, and that decoupling depth from input size with a
# task-independent latent array is its own contribution. The Set Transformer is
# now held (LIT-760) and was read for this: ISAB returns to the input size
# after every block and PMA's output size is set by the task, so neither takes
# the input out of depth. It is the origin of the primitive, not of the
# recommendation, which is stated first by the source.
introduced_by:
- LIT-747
implementations:
- 'Perceiver'
summary: >-
  Jaegle et al. (2021), [LIT-747](../literature.d/LIT-747.md) — the Perceiver. A learned array of 512
  latents cross-attends to all 50,176 ImageNet pixels, at a cost of O(MN)
  rather than O(M²), and a 48-block latent transformer then runs at a cost
  independent of input size. It matched ResNet-50 and ViT-B/16 at 78.0% top-1
  without convolutions, did not beat them, and ran unchanged on audio, video
  and point clouds. The case for doing it is cost and modality-independence,
  not accuracy, and the cost advantage is argued from complexity, not
  measured against a baseline.
---

# SOTA-436: Route a very large or non-grid input through cross-attention into a small learned latent array, so that depth no longer scales with input size

## Source

Jaegle et al. (2021), [LIT-747](../literature.d/LIT-747.md) — the Perceiver, §2–3 and Appendix Tables 5–7.

## What to do

When the input has too many elements for self-attention over all of them, or
has no grid that a patch convolution could exploit:

- **Learn a small latent array** of `N` elements, independent of the input
  and of the task (`N = 512` on ImageNet).
- **Cross-attend from the latents to the input.** Queries come from the
  latents and keys and values from the input, so this layer costs `O(MN)` in
  the input size `M`.
- **Put the depth in a transformer over the latents.** Each layer costs
  `O(N²)`, which does not grow with `M`. The whole model is `O(MN + LN²)`
  where a transformer over the raw input would be `O(LM²)`.
- **Re-query the input a few times, spread through the depth.** Do not place
  all the cross-attends at the start.
- **Carry position in the input features.** The architecture is
  permutation-invariant, so whatever spatial or temporal structure matters has
  to be concatenated onto the input as a position encoding.

## Evidence

[LIT-747](../literature.d/LIT-747.md) introduced the design and measured it on ImageNet with no
convolutions and no pretraining. It reached 78.0% top-1, against 77.6 for
ResNet-50 and 77.9 for ViT-B/16 as published, and 73.5 and 76.7 for the
authors' own runs of those two given the same Fourier-feature inputs. A plain
transformer, which had to be fed 64×64 downsampled images to fit, got 57.0.
**This is a match, not a win.** The paper notes the best result without
pretraining at the time was 86.5%.

The paper's own ablations support three parts of the instruction:

- **The latent transformer carries the result.** A stack of cross-attends
  with no latent self-attention reaches 39.4% with four layers and 45.3% with
  eight. Twelve ran out of memory on 64 TPUs (Table 5).
- **Interleave the cross-attends.** Eight cross-attends spread through the
  network give 78.0%. The same eight all at the start give 73.7%, at the same
  707.2B FLOPs (Table 6).
- **It does not need the grid.** On ImageNet with one fixed pixel
  permutation, applied after the position features are computed, the
  Perceiver stays at 78.0. The authors' ViT-B/16 drops from 76.7 to 61.7 and
  ResNet-50 from 73.5 to 39.4 (Table 2). With a learned position encoding
  instead of Fourier features, so the model knows nothing of 2D structure, it
  still gets 70.9.

Across modalities the same architecture gets 38.4 mAP on raw AudioSet audio
and 43.5 with video fused at the input, below a late-fusion model at 46.2. On
ModelNet40 point clouds it gets 85.7%, against 82.1 for a transformer and 91.9
for the specialised PointNet++, which uses extra geometric features and
augmentation. These show it runs everywhere. They do not show it is best
anywhere.

## Conditions and limits

- **The cost advantage is asymptotic, and the paper does not measure it
  against a baseline.** It reports FLOPs for its own variants only. The best
  ImageNet model costs 707.2B FLOPs (unfused multiply-adds). A single
  cross-attend gets 76.7% at 404.3B, which matches the authors' ViT-B/16 run.
  Whether either is cheaper than ViT-B/16 at 224×224 is not shown. What the
  design buys for certain is that the input-size term enters only at the
  cross-attends, so the advantage grows with `M`. At ImageNet's `M` it was not
  measured.
- **Weight sharing was needed to stop overfitting.** Unshared, the ImageNet
  model has 326.2M parameters and gets 72.9% validation against 87.7% train.
  Shared across all cross-attends after the first and the corresponding latent
  blocks, it has 44.9M and gets 78.0% (Table 7). Sharing the first
  cross-attend as well made training unstable.
- **Stability is fragile in places.** Eight cross-attends were unstable with
  learned position encodings, so that result uses one. NeRF-style
  power-of-two Fourier bands became unstable beyond about 15 bands.
  Coordinates had to be crop-relative or the model overfit.
- **Classification only.** Every result pools the latents into one output. The
  paper does not cover dense or structured outputs.
- **The original AudioSet numbers were wrong.** The first arXiv version
  reported higher mAPs because of a transposed score matrix (Appendix F). The
  numbers above are the corrected ones.

## Where the primitive came from

The cross-attention from a small learned array to a large input is older
than the source. The Set Transformer ([LIT-760](../literature.d/LIT-760.md)) introduced it in two forms: an
induced set attention block, in which `m` learned inducing points (16 in
most of its runs) attend to an input set of `n` elements and the elements
attend back, at `O(nm)` per block, and pooling by multihead attention, in which `k` learned
seeds attend to the set to produce `k` outputs. With 16 inducing points it
matched or beat full self-attention on amortized clustering, and on
ModelNet40 it ran at 5,000 points where full attention was too slow. But
neither block does what this practice asks. The induced block maps back to
the input size, so a stack of them still pays for the whole input at every
layer, and the pooling block's output size is fixed by the task, one seed
for classification. The encoders it sets out are two blocks deep. The source makes the
same comparison in its Appendix A and puts its contribution in the
composition: a single large, task-independent latent array, and the depth
placed behind it. So the Set Transformer supplies the mechanism and the
Perceiver the recommendation, and `introduced_by` stays with the Perceiver.

## Beside the record's other practices

[SOTA-358](SOTA-358.md) says to drop a domain's inductive bias once pre-training data is
large enough and to keep it when it is not. This practice drops the grid
prior entirely on ImageNet-1k, below the threshold [SOTA-358](SOTA-358.md) describes, and
lands at ResNet-50's level rather than above it. It is consistent with
[SOTA-358](SOTA-358.md) rather than a counterexample. Removing the prior was affordable at
that scale, not profitable. What the Perceiver adds is a reason to remove the
prior that [SOTA-358](SOTA-358.md) does not consider: an input with no grid, or several
inputs with different grids, where there is no prior to keep.

## Known implementations

- Perceiver, the source's model (DeepMind).
