---
number: 45
paper: LIT-108
status: Read
formerly:
- NOTE-tmphj2no
title: '3D Gaussian Splatting for Real-Time Radiance Field Rendering'
version: 1
tags:
- vision-and-graphics
date: '2026-09-09'
published: '2023-08-01'
summary: >-
  Represents a scene as anisotropic 3D Gaussians initialised from structure-from-motion points, optimised with interleaved density control, and rendered by projecting to 2D and α-blending. Differentiable like a volumetric field, rasterizable like geometry — the first real-time (≥30 fps) radiance-field rendering at 1080p. Static scenes.
---

# NOTE-045: 3D Gaussian Splatting for Real-Time Radiance Field Rendering

## Contribution

Real-time novel-view synthesis at quality matching the expensive methods.
Three elements, and the paper is explicit that all three are needed:

- **3D Gaussians initialised from the sparse points produced by camera
  calibration (SfM)** — a representation that "preserves desirable properties of
  continuous volumetric radiance fields for scene optimization while avoiding
  unnecessary computation in empty space".
- **Interleaved optimization and density control**, including **anisotropic
  covariance** so a Gaussian can be shaped to the surface it represents.
- **A fast visibility-aware rendering algorithm** supporting anisotropic
  splatting, which accelerates training as well as rendering.

## Key insight

**A 3D Gaussian is differentiable as a volume and cheap as a primitive.** The
paper's own statement: they "are a differentiable volumetric representation, but
they can also be rasterized very efficiently by projecting them to 2D, and
applying standard α-blending, using an equivalent image formation model as
NeRF."

That equivalence is the whole argument. Prior work chose between a volumetric
model you can optimise and a rasterizable one you can render fast; Gaussians are
both, so nothing is traded.

The second decision is **initialisation from SfM points** — the sparse geometry
you already computed to get the camera poses. The scene starts where there is
evidence of structure, rather than in a uniform grid, and the ablation lists it
first among the contributions tested.

## Assumptions

- SfM calibration is available and its sparse points are a good starting
  distribution. This is free in the intended pipeline and is a real dependency.
- **Static scenes.** The optimisation is over a fixed scene; dynamic extensions
  came later and are not in this paper.
- Anisotropy is necessary, not a refinement — it is ablated as such.

## Key results

- **Real-time, ≥30 fps, at 1080p, for unbounded and complete scenes** — the first
  method to do so, where "no current method can achieve real-time display rates".
- **State-of-the-art visual quality with competitive training times.**
- **Ablations on:** SfM initialisation, the densification strategies, anisotropic
  covariance, and allowing an unlimited number of splats to receive gradients.
  Four separately tested choices, which is more discipline than most systems
  papers.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | 3D Gaussians are both differentiable-volumetric and efficiently rasterizable | strong | the equivalent image-formation argument, and the implementation |
| C2 | SfM initialisation matters | strong | ablated |
| C3 | Anisotropic covariance is necessary for accurate representation | strong | ablated |
| C4 | Real-time 1080p rendering at matching quality | strong | measured on established datasets |
| C5 | Unlimited splats receiving gradients matters | moderate | ablated, less discussed |

## Method

Initialise Gaussians at SfM points. Optimise position, anisotropic covariance,
opacity and colour, interleaved with density control that splits, clones and
prunes. Render by projecting to 2D and α-blending, front to back, with
visibility awareness.

## Concepts

- **A primitive that is both differentiable and rasterizable** — the design
  criterion, and the reason a long-standing trade evaporated.
- **Initialising from evidence you already have** — SfM points, free from the
  calibration step.
- **Density control as part of optimisation**, not a preprocessing step.

## Connections

With `LIT-064` (instant-ngp) and `LIT-086` (K-Planes) this is the third paper in
this batch replacing "query a large network per point" with a compact explicit
structure. `LIT-113` builds directly on Gaussian primitives for human
generation, and `LIT-109` is the same speedup pressure applied to implicit
surfaces.

C1's shape — find a representation where two desirable properties stop being
exclusive, rather than trading them — is the most transferable thing here, and
`LIT-071`'s decoder split is the same move in a different field.

## Recommendations

- **R1** — When two required properties appear to trade, look for a
  representation that has both rather than tuning the trade. *Topic:* vision and
  graphics; the form is general. *Strength:* strong.
- **R2** — Initialise from structure you already computed. *Strength:* strong.
- **R3** — Ablate each element of a systems contribution separately.
  *Strength:* strong, and this paper is a good model of it.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**
Radiance-field rendering is not a line the anthology tracks.

The document's takeaway **"dynamic scene optimization" is wrong.** This paper is
about **static** scenes: the abstract's scope is "unbounded and complete scenes
(rather than isolated objects)", and the optimisation referred to is *density
control* of Gaussians during fitting. Dynamic 3D Gaussian work came afterwards
and is not this paper. A reader taking that bullet at face value would cite this
for something it does not do.

## Limitations

- Static scenes; the dynamic extension is other work.
- Requires SfM calibration, so it inherits that pipeline's failure modes.
- Memory grows with the number of Gaussians, and C5's "unlimited splats with
  gradients" is a cost as well as a benefit.
- 2023, and the field moved quickly afterwards.

## Open questions

- What sets the right number of Gaussians? Density control is adaptive and its
  stopping behaviour is a heuristic.
