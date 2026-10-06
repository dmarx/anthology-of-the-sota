---
status: Proposed
promote_when: >-
  A comparison that holds everything but the block geometry: the same
  model, sparsity, selection rule and training budget, with blocks formed
  once as small 3D cubes and once as runs of the same number of
  consecutive raster-order tokens, scored on generation quality with more
  than one seed. Nobody in the record has run it. More papers that adopt
  cubes, or that compare a cube method against a raster method differing
  in selection rule or training as well, would not count. A result where
  raster runs match cubes on quality would move this toward a
  hardware-only claim, which is a different practice.
consensus: emerging
consensus_note: >-
  Five groups build block-sparse video attention on small 3D cubes laid out
  as kernel tiles: Hao AI Lab (Sliding Tile Attention, VSA), Meituan
  (LongCat-Video), Tencent Hunyuan (HunyuanVideo 1.5, Prism) and, in one
  layer in three, Kuaishou (VMoBA). The dissent is real and works:
  SpargeAttention2 (Tsinghua) reaches 95% sparsity on Wan2.1 with runs of
  consecutive tokens, and Sparse VideoGen2 replaces geometric blocks with
  content clusters. No group has measured cubes against raster runs at
  matched settings.
title: 'In block-sparse attention over video tokens, make each block a small 3D spatiotemporal cube laid out as one kernel tile, not a run of raster-order tokens'
version: 1
tags:
- attention-techniques
- systems-optimization
- generative-modeling
date: '2026-10-06'
source:
# Each ran an experiment bearing on the claim (ADR-017). STA measured
# tile-granular against token-granular 3D windows. VSA swept cube size and
# shape. Prism compared fixed cube sizes and content-chosen shapes. Sparse
# VideoGen2 measured recall of contiguous regrouped blocks against unpermuted
# raster blocks. LongCat-Video and HunyuanVideo 1.5 adopt cubes without
# testing them, so they are consensus, not source.
- LIT-tmp1yfvi
- LIT-tmp5vqlh
- LIT-tmpe78xc
- LIT-tmpucn4v
introduced_by:
# STA is the first paper in the record to make a 3D cube one FlashAttention
# block by re-indexing tokens. Neighbourhood attention did 3D windows
# earlier, but token by token, which is the layout STA measures against.
- LIT-tmp1yfvi
implementations:
- 'Sliding Tile Attention (FastVideo)'
- 'VSA (FastVideo)'
- 'LongCat-Video BSA'
- 'HunyuanVideo 1.5 SSTA'
- 'Prism'
summary: >-
  Zhang et al. (2025), [LIT-tmp1yfvi](../literature.d/LIT-tmp1yfvi.md), then [LIT-tmp5vqlh](../literature.d/LIT-tmp5vqlh.md), [LIT-tmpe78xc](../literature.d/LIT-tmpe78xc.md) and
  [LIT-tmpucn4v](../literature.d/LIT-tmpucn4v.md). Re-index video tokens so that each small 3D cube, typically
  4×4×4 = 64 tokens, is one contiguous kernel tile, and select or slide over
  whole cubes. Tiles then never need per-token masking, which is where the
  measured speed comes from: 41% against 8% MFU for the same 3D window
  computed token by token. Smaller cubes give lower loss and a slower
  kernel. Nobody has compared cubes with raster runs of the same size at
  matched settings, and one method reaches 95% sparsity with raster runs.
---

# SOTA-tmpaeox9: In block-sparse attention over video tokens, make each block a small 3D spatiotemporal cube laid out as one kernel tile, not a run of raster-order tokens

## Source

Zhang et al. (2025), [LIT-tmp1yfvi](../literature.d/LIT-tmp1yfvi.md) — Sliding Tile Attention, the first to lay
3D cubes out as kernel tiles. Zhang et al. (2025), [LIT-tmp5vqlh](../literature.d/LIT-tmp5vqlh.md) — VSA, the
cube-size sweep. Tu et al. (2026), [LIT-tmpe78xc](../literature.d/LIT-tmpe78xc.md) — Prism, fixed and
content-chosen cube shapes at 2K. Yang et al. (2025), [LIT-tmpucn4v](../literature.d/LIT-tmpucn4v.md) — Sparse
VideoGen2, the cost of unpermuted raster blocks.

## What to do

Before block-sparse attention, permute the video latent so that each small
spatiotemporal neighbourhood, a cube such as 4×4×4 latent positions, becomes
one run of consecutive positions whose length equals the kernel's tile. Then
pool, score and select whole cubes, or slide a window one cube at a time.
Undo the permutation after attention. The cost is a gather and scatter per
layer. Prism measures its own version, with shape assignment, at 1.5% of
inference time.

## What the evidence shows

**The tile layout is a hardware result, and a large one.** Sliding Tile
Attention ([LIT-tmp1yfvi](../literature.d/LIT-tmp1yfvi.md)) compares a 3D window that slides one tile at a time
with the same window computed token by token. With tiles, every block is
either fully attended or skipped, so no block needs a mask inside the
kernel. Analytically, the token-wise window leaves 7.17% of blocks mixed for
a 48³ video. In the same framework (FlexAttention) at about 90% sparsity, the
tiled window reaches 41.03% MFU and 7.30× over FA3, against 8.20% and 1.27×
token by token. That comparison is between sliding granularities, both 3D.
It is not a comparison of 3D cubes with raster runs.

**On quality, the tile cost a little where it was measured.** At a matched
58% sparsity without training, token-wise sliding scores VBench 82.69 and
tile-wise 82.46 ([LIT-tmp1yfvi](../literature.d/LIT-tmp1yfvi.md), Table 4). The tile buys speed, not quality.

**Smaller cubes are better and slower.** VSA ([LIT-tmp5vqlh](../literature.d/LIT-tmp5vqlh.md), Table 1c–d)
trains the same model with cubes of 256, 128, 64 and 16 tokens. Loss falls
from 0.13375 to 0.13244 to 0.13162 to 0.13155. Kernel throughput falls with
them, and the 16-token cube runs 2.26× slower than the 64-token one. Every
arm is a 3D cube, and the differences are in the third and fourth decimal of
one run each. 64 tokens is where the curve flattens and the kernel is still
fast. Prism ([LIT-tmpe78xc](../literature.d/LIT-tmpe78xc.md), Table 9) points the same way at 2K: a fixed 4×4×4
cube scores aesthetic quality 0.55 and MotionQ 0.77, and a fixed 8×8×8 cube
0.43 and 0.51. LongCat-Video ([LIT-tmpid6gf](../literature.d/LIT-tmpid6gf.md)) reports the opposite for its
refinement stage, "no significant differences" across block sizes of 64 to
1,024 key tokens, with no table.

**Raster blocks do lose something, measured once.** Sparse VideoGen2
([LIT-tmpucn4v](../literature.d/LIT-tmpucn4v.md), Fig. 8) compares blocks of consecutive raster-order tokens
with the same tokens regrouped into contiguous content clusters, at the same
cluster size and pooling. The regrouped blocks recover more attention mass at
every density. That supports regrouping before pooling. It shows nothing
about geometric cubes in particular, because its regrouping is by k-means
on the features, not by position. It is shown as a curve, without values.

## What it does not establish

**The deciding comparison has not been run.** No paper in the record trains
or evaluates the same method with cubes and with raster runs of equal size
at matched sparsity and selection. VSA names the gap itself: every block in
its sweep is a cube. So the claim that cubes beat raster runs on quality
rests on the plausible argument that a cube's tokens are more alike than a
run that wraps across rows, on Sparse VideoGen2's evidence that regrouping
helps, and on adoption.

**Raster runs work in at least one strong method.** SpargeAttention2
([LIT-tmpbgw07](../literature.d/LIT-tmpbgw07.md)) uses runs of 128 query and 64 key tokens in raster order. It
reaches 95% sparsity on Wan2.1 at 1.3B and 14B with quality level with the
dense model, after fine-tuning against a dense teacher. Training may be what
makes the geometry matter less. That is untested.

**VMoBA's evidence is confounded.** VMoBA ([LIT-tmpmuiol](../literature.d/LIT-tmpmuiol.md)) attributes the
collapse of vanilla MoBA's motion (Dynamic Degree 5.80%) to MoBA's 1D
partition. But that comparison also changes the selection rule, and VMoBA's
ablation never trains a cube-only arm.

## Variations

- **Shape chosen from content.** Prism ([LIT-tmpe78xc](../literature.d/LIT-tmpe78xc.md)) keeps the cube volume
  in {64, 128, 256} tokens and picks each 8×8×8 zone's shape per head and
  layer, giving short edges along axes where features or audio coupling vary
  fast. Inside its own pipeline this beats fixed 4×4×4 (0.61 against 0.55
  aesthetic, 0.89 against 0.77 MotionQ). It is one run per arm, from a
  method whose competitors were trained differently. Filed here as a
  variation, not a practice.
- **Shape cycled by layer.** VMoBA ([LIT-tmpmuiol](../literature.d/LIT-tmpmuiol.md)) alternates temporal slabs,
  spatial columns and cubes across layers. T3 ([LIT-tmpva88i](../literature.d/LIT-tmpva88i.md)) cycles five
  window shapes, from whole frames to tall thin tubes.
- **Membership chosen from content.** Sparse VideoGen2 ([LIT-tmpucn4v](../literature.d/LIT-tmpucn4v.md)) drops
  geometry altogether and blocks tokens by k-means, with variable block
  sizes and a custom kernel. It is training-free and runs on dense models.
  It is the main alternative to this practice, not a variant of it.

## Conditions

- It is about attention over video latents with a regular (T, H, W) grid.
  Nothing here tests it on images, audio or text, and Prism leaves its audio
  tokens dense.
- The cube's token count should match the kernel's tile. Most of the speed
  argument depends on that alignment, and a cube that straddles tiles
  reintroduces the mixed blocks STA removed.
- It is compatible with any selection rule: a fixed sliding window (STA),
  top-k of pooled scores (VSA, LongCat-Video), top-k with a redundancy
  penalty (HunyuanVideo 1.5) or a top-k ∪ top-p union (Prism). The geometry
  and the rule are separate choices.

## Known implementations

- Sliding Tile Attention and VSA (FastVideo kernels; ThunderKittens and
  Triton)
- LongCat-Video's block sparse attention, 4×4×4 (Triton)
- HunyuanVideo 1.5's selective and sliding tile attention ([LIT-tmp1ecle](../literature.d/LIT-tmp1ecle.md))
- Prism (Triton, 64-token tiles)
