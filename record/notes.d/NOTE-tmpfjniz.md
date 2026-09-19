---
status: Read
paper: LIT-tmpkbyen
title: 'NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis'
version: 1
date: '2026-09-19'
summary: >-
  Store the scene in the weights of an MLP that maps a 5D coordinate to
  density and view-dependent colour, and render it with classical volume
  rendering, which is differentiable — so posed images are the only
  supervision. Two additions do the work everybody remembers: positional
  encoding, without which the result is oversmoothed, and hierarchical
  sampling, without which it is unaffordable.
---

# NOTE-tmpfjniz: NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis

## Contribution

A scene representation and a way to fit it. The representation is a
continuous 5D function — position and viewing direction to density and colour
— parameterised by a fully-connected network. The fitting procedure is
classical volume rendering made differentiable, so the whole thing optimizes
against photometric error on a set of posed images.

## Key insight

Two, and they are separable. **A scene can be the weights of a network**
rather than a data structure the network consumes. And **the rendering
operator can carry the gradient**, which removes the need for any 3D
supervision at all — no meshes, no depth, no voxel grids, just images and
their cameras.

## Concepts

- **Radiance field** — density at a point plus the colour that point emits in
  a given direction
- **Positional encoding** — mapping the input coordinate to a higher
  dimensional space so the MLP can express high-frequency variation
- **Hierarchical sampling** — a coarse pass to find where content is, a fine
  pass to spend samples there

## Assumptions

- **Camera poses are known.** This is the load-bearing input assumption and
  it is the reason the record's geometry practices sit upstream of this one:
  `SOTA-236` and `SOTA-237` are about getting the poses this paper requires
- **One scene, one network.** Nothing here generalises across scenes; the fit
  is the artifact
- **Static scene, consistent lighting** across the captured views
- **Enough views, well distributed.** "Sparse" in the abstract means sparse
  relative to classical multi-view stereo, not few

## Key results

- **State-of-the-art novel view synthesis** on complex scenes with
  complicated geometry and appearance, against prior neural rendering and
  view-synthesis work. *Holds when:* per-scene optimization, known poses.
- **Positional encoding is necessary, not a refinement.** The ablation
  without it is oversmoothed; the paper states the basic implementation does
  not reach a sufficiently high-resolution representation.
- **Hierarchical sampling reduces the queries needed** to sample a
  high-frequency representation adequately — the difference between the idea
  and something that runs.
- **The view-dependence split is what keeps it multiview-consistent**:
  density from position only, colour from position and direction.

## Limitations

- **Per-scene optimization**, and slow — which is the entire reason the four
  papers `SOTA-205` sources exist
- **Requires known poses**, so it is not a reconstruction method on its own
- **Static scenes.** Dynamic and deformable extensions are all later work
- **The positional-encoding frequency band is hand-set**, and the record's
  own successor practice replaces the encoding scheme wholesale rather than
  tuning it

## Connections

`SOTA-205` is the record's position on this design and recommends against it:
a compact explicit structure with a small decoder, sourced to Instant-NGP,
K-Planes, 3D Gaussian Splatting and NeuS2 — every one of them a response to
this paper's cost. `SOTA-236` and `SOTA-237` supply the poses it assumes.

The positional-encoding result is the one part that travels outside vision:
it is a claim about what a coordinate-input MLP can represent, and the
record's `representation-and-encoding` topic is where that kind of claim
lives.

## Bearing on the record

No practice, deliberately — see `LIT-tmpkbyen`'s standing. The reading's
value is that `SOTA-205`'s recommendation now has a legible object: "a large
coordinate network" was a description of something the record did not hold,
and four of its sources were arguing with a paper that was not there.
