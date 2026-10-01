---
status: Proposed
promote_when: >-
  A comparison in which the supervision source is the only thing that
  changes — the same reconstructor, the same compute, trained once on a
  video model's renderings and once on captured multi-view data — scored
  against real held-out views of captured scenes, not against the teacher's
  own frames. The most informative version scores both on RealEstate10K or
  DL3DV, where captured training data has the home advantage; the practice
  survives if the generated supervision is not worse there and better out of
  domain. A second group, or a different video model as teacher, would also
  count. What would NOT meet it: another system that trains this way and
  tops a benchmark table of numbers copied from other papers, which changes
  the generator, the decoder and the data at once and isolates none of them.
consensus: unreplicated
consensus_note: >-
  One group, one teacher (GEN3C on Cosmos), and the only arm that isolates
  the supervision source is scored on the teacher's own distribution. The
  benchmark wins in the source are real but compare whole systems, with the
  baselines' numbers taken from their papers. Read as of 2026-10.
title: "Supervise a feed-forward 3D reconstructor with a frozen camera-controlled video model's renderings instead of captured multi-view data"
version: 1
tags:
- vision-and-graphics
- data-pipeline
- generative-modeling
date: '2026-10-01'
source:
- LIT-tmp5yash
# The source claims the idea as its own contribution ("eliminating the need
# for captured multi-view real-world data") and names Wonderland as the
# closest prior work, which uses a camera-controlled video model to generate
# Gaussians feed-forward but is not described as dropping captured data.
# Wonderland is not in the record either way.
introduced_by:
- LIT-tmp5yash
implementations:
- 'Lyra'
summary: >-
  Bahmani et al. (2025), [LIT-tmp5yash](../literature.d/LIT-tmp5yash.md) — Lyra trains a 3D Gaussian Splatting
  decoder only on a frozen video model's RGB decodings along six camera paths
  per image, with no captured multi-view data. In its one controlled arm,
  training on real RealEstate10K + DL3DV instead scores PSNR **19.08 against
  24.77**, and adding the real data to the generated data gives **24.74**, no
  better. Both are scored against the teacher's own renderings on its own
  prompts, which is the distribution the generated supervision was drawn
  from — so the arm shows the generated data is sufficient there, not that
  it beats captured data on real scenes.
---

# SOTA-tmpqmoen: Supervise a feed-forward 3D reconstructor with a frozen camera-controlled video model's renderings instead of captured multi-view data

## Source

Bahmani et al. (2025), [LIT-tmp5yash](../literature.d/LIT-tmp5yash.md) — Lyra, §3, §6 (Tables 1 and 2) and
Appendix C.

## The claim

Captured multi-view scenes are scarce and narrow; RealEstate10K and DL3DV are
what scene-level reconstructors train on, and they generalize poorly outside
them. A camera-controlled video diffusion model trained on internet video can
render any image along any camera path. So generate the multi-view data
instead: sample camera trajectories for each input image, let the frozen
video model produce the views, and train the reconstructor to match them.

[LIT-tmp5yash](../literature.d/LIT-tmp5yash.md) does this with GEN3C as teacher: 59,031 generated images, six
trajectories of 121 frames each, 354,186 videos, and no captured multi-view
data at all. The student is a 3DGS decoder that reads the video model's
latents, and its renderings are trained against the RGB decoder's frames with
MSE and LPIPS, plus a depth loss against ViPE video depth and an opacity
penalty.

## The evidence, and what each part can show

**The arm that isolates the supervision source** (Table 2), scored by PSNR /
SSIM / LPIPS against the video model's own renderings on out-of-distribution
prompts:

| supervision | PSNR | SSIM | LPIPS |
|---|---|---|---|
| generated only (Lyra) | **24.77** | **0.837** | **0.224** |
| captured only (RealEstate10K + DL3DV) | 19.08 | 0.659 | 0.413 |
| generated + captured | 24.74 | 0.823 | 0.236 |

The paper reads the third row as confirming "that self-distillation is diverse
and consistent enough to learn a reconstruction model". That is the
supportable half. The large gap to the second row is not evidence that
generated supervision beats captured supervision: the test targets are the
teacher's frames, so a student trained on the teacher is being scored on its
training distribution and a student trained on real scenes is being scored
on how well it reproduces the teacher's hallucinations. The captured-only
model is never scored on RealEstate10K or DL3DV, the benchmarks where it
would have the advantage.

**The benchmark comparison** (Table 1), single image to 3D on RealEstate10K,
DL3DV and Tanks-and-Temples, scored against real held-out views: Lyra leads on
every metric — RealEstate10K PSNR 21.79 against Bolt3D's 21.54, DL3DV 20.09
against Wonderland's 16.64, Tanks-and-Temples 19.24 against 15.90. This is
the real-scene test, but it compares whole systems: the baselines differ in
generator, decoder and training data at once, and their numbers are taken
from their papers because "no source code is available". It shows the
recipe produces a strong system; it does not say how much of that is the
supervision.

**The authors' own limit:** "the scale and consistency of our generated
scenes are bounded by the capacity of our camera-controlled video diffusion
model". A student trained only on a teacher's frames inherits every 3D
inconsistency in them; the depth loss exists because RGB supervision alone
produced flat geometry.

## Conditions

- **The student decodes the teacher's latents.** At inference Lyra still runs
  the video model and replaces only its RGB decoder. Whether generated views
  are as good a supervisor for a reconstructor that takes images directly is
  untested here; the pixel-space version of this student ran out of memory on
  726 views per scene, which is why the design reads latents.
- **The teacher has to be 3D-consistent first.** The source chose GEN3C
  because it builds an explicit 3D cache to keep views consistent, and still
  had to refine its masks; a video model without that would supply
  inconsistent targets, and nothing here measures how much inconsistency the
  student tolerates. Fusing across the six trajectories is learned for this
  reason; without it PSNR falls to 17.73, the largest drop in Table 2.
- **One teacher and one group**, with no variance reported for any cell.

## Known implementations

- Lyra (NVIDIA)
