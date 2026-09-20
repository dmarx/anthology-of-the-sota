---
number: 236
status: 'Active'
formerly:
- SOTA-tmpjhh4p
title: 'Predict scene geometry directly instead of solving for cameras first and triangulating'
version: 1
tags:
- vision-and-graphics
consensus: emerging
consensus_note: >-
  Two groups, two years apart, and the later one removes the optimisation the
  earlier still needed — which is the shape of a line moving toward a default
  rather than a single result. Not `converged`: the classical pipeline is
  decades of tooling and still what most production reconstruction runs on,
  and nothing in this record measures the crossover.
date: '2026-09-17'
source:
- LIT-385
- LIT-384
introduced_by:
- LIT-385
implementations:
- LIT-385
- LIT-384
summary: >-
  Wang et al. (2023), [LIT-385](../literature.d/LIT-385.md) — [ARXIV-2312.14132](https://arxiv.org/abs/2312.14132); Wang et al. (2025),
  [LIT-384](../literature.d/LIT-384.md) — [ARXIV-2503.11651](https://arxiv.org/abs/2503.11651). Given uncalibrated, unposed images, regress
  the 3D structure and let camera parameters and pixel matches fall out of it,
  rather than estimating calibration and pose first so that triangulation
  becomes possible. The quantities the classical pipeline needs as inputs are
  by-products of this one.
---

# SOTA-236: Predict scene geometry directly instead of solving for cameras first and triangulating

## Source

Wang et al. (2023), [LIT-385](../literature.d/LIT-385.md) — [ARXIV-2312.14132](https://arxiv.org/abs/2312.14132) (DUSt3R).
Wang et al. (2025), [LIT-384](../literature.d/LIT-384.md) — [ARXIV-2503.11651](https://arxiv.org/abs/2503.11651) (VGGT).

## The dependency being inverted

Classical multi-view reconstruction has a fixed order. Calibration and pose
come first, because triangulation is *defined* in terms of them — DUSt3R's own
words are that they are "mandatory to triangulate corresponding pixels in 3D
space, which is the core of all best performing MVS algorithms".

So the pipeline's stages are not a decomposition somebody chose for
convenience; each one exists because the next one cannot start without it.
That is what makes this a reframing rather than a better solver: **regress the
3D structure directly, and recover matches, relative and absolute camera from
the output.** Everything the old order required in advance is available
afterwards.

Two things fall out that the classical framing cannot express. Monocular and
multi-view reconstruction become the same problem with different amounts of
evidence, rather than different problems — a single view has no baseline to
triangulate across. And the projective camera model stops being a constraint
to satisfy and becomes a property the answer turns out to have.

## Why two papers rather than one

DUSt3R shows the inversion works and still needs an explicit global alignment
step once there are more than two images. VGGT removes it: one feed-forward
pass, one to hundreds of views, producing camera parameters, point maps, depth
maps and 3D point tracks together — **and beating methods that post-process
with geometry optimisation**, in under a second.

That last part is the strong claim. The iterative refinement that justified
the classical pipeline is not, on these benchmarks, buying what it was thought
to be buying.

## Conditions

**This is emerging, not settled.** The classical pipeline is decades of
tooling, well understood failure modes, and what most production
reconstruction still runs on. Nothing in this record measures where the
crossover is, and "a forward pass beat optimisation on these benchmarks" is
not "optimisation is obsolete".

**The guarantees are different in kind.** A triangulated point has a geometric
justification and a residual you can inspect; a regressed pointmap has neither.
Where a reconstruction has to be certified rather than merely used — survey,
metrology, anything with a tolerance — that difference is the whole question,
and neither paper addresses it.

**Scale of evidence.** Two groups. The second's backbone result — pretrained
VGGT improving downstream tracking and view synthesis — is the best available
evidence that something geometric was learned rather than four output heads
fitted, but it is still one team's finding.

## What this gives the record

The geometry half of 3D vision, which [#154](https://github.com/dmarx/anthology-of-the-sota/issues/154) found was entirely absent. The
anthology already recommends how to *represent* a reconstructed scene
([SOTA-205](SOTA-205.md), from [LIT-108](../literature.d/LIT-108.md), [LIT-086](../literature.d/LIT-086.md), [LIT-109](../literature.d/LIT-109.md), [LIT-064](../literature.d/LIT-064.md)) and said nothing about
how the scene got reconstructed — so a reader arriving with a pile of images
found four papers assuming the poses they came to ask about.

It also gives [LIT-111](../literature.d/LIT-111.md) (OnePose) its lineage. That reading builds an SfM point
cloud and matches against it with a generic network; until now this record
held that machinery only as a step inside somebody else's method, never as a
subject with papers of its own.
