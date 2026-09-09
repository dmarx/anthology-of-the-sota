---
paper: LIT-086
status: Read
title: 'K-Planes: Explicit Radiance Fields in Space, Time, and Appearance'
version: 1
tags:
- vision-and-graphics
date: '2026-09-09'
summary: >-
  Represents a d-dimensional scene with "d choose 2" planes, so static (d=3) and dynamic (d=4) scenes are the same model at different d. The factorisation makes dimension-specific priors easy to attach and separates static from dynamic components naturally; a linear decoder with a learned colour basis matches a nonlinear MLP.
---

# NOTE-tmpcovu6: K-Planes: Explicit Radiance Fields in Space, Time, and Appearance

## Contribution

A **white-box** radiance-field model in arbitrary dimensions: represent a
`d`-dimensional scene with **`C(d,2)` planes** — every pair of axes gets one.
Static scenes are `d = 3` (three planes), dynamic are `d = 4` (six), and moving
between them changes a number rather than a design.

**1000× compression** over a full 4D grid, competitive or state-of-the-art
reconstruction fidelity, fast optimisation, in **pure PyTorch**.

## Key insight

The planar factorisation is chosen for what it makes *easy*, not just for what
it compresses. Because each plane spans a named pair of axes:

- **Dimension-specific priors attach naturally** — temporal smoothness goes on
  the planes involving time, multi-resolution spatial structure on the spatial
  ones. In an entangled representation there is nowhere to put such a prior.
- **Static and dynamic components decompose by construction** — the planes not
  involving time describe what does not move.

That is the general lesson: **a factorisation indexed by the axes you care about
lets you state assumptions about each axis separately.**

Second finding, quietly against the grain: **a linear feature decoder with a
learned colour basis performs about as well as a nonlinear black-box MLP
decoder.** Once the representation carries the structure, the decoder does not
need to.

## Assumptions

- Pairwise-plane factorisation captures enough of the signal. This is a strong
  structural assumption and the compression figure is its payoff.
- Priors of interest are axis-aligned — temporal smoothness, spatial
  multi-resolution — which is what makes the factorisation's index useful.

## Key results

- **`C(d,2)` planes for a `d`-dimensional scene**; `d = 3` static, `d = 4`
  dynamic, same model.
- **1000× compression over a full 4D grid**, with low memory use.
- **Competitive and often state-of-the-art fidelity** across synthetic and real,
  static and dynamic, fixed and varying-appearance scenes.
- **A linear decoder with a learned colour basis matches a nonlinear MLP.**
- Fast optimisation in **pure PyTorch** — no custom kernels, unlike much of this
  neighbourhood.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Pairwise planes suffice to represent `d`-dimensional radiance fields | strong | fidelity across scene types |
| C2 | The factorisation makes axis-specific priors easy to state | strong | demonstrated for time and space |
| C3 | Static/dynamic decomposition falls out of the factorisation | strong | structural |
| C4 | A linear decoder suffices | strong | measured against the MLP |
| C5 | 1000× compression over a 4D grid | strong | arithmetic plus results |

## Method

Allocate one feature plane per pair of dimensions. For a point, project onto each
plane, look up and multiply the features, decode linearly against a learned
colour basis. Add per-axis regularisers where they belong.

## Concepts

- **Factorisation indexed by axes** — the transferable idea: it buys a place to
  put each assumption.
- **White-box representation** — the paper's own word, and the property C2 and
  C3 depend on.
- **Capacity in the representation rather than the decoder** — C4.

## Connections

With `LIT-064` and `LIT-108`, the third explicit-structure replacement for a
large coordinate network in this batch, and the one that needs no custom
kernels.

C4 — put the structure in the representation and the decoder can be linear — is
the same trade `LIT-091` makes for adapters (**the capability is already there;
the adapter only aligns to it**) and the opposite of the usual instinct to add
capacity where the output is produced.

## Recommendations

- **R1** — Factorise along the axes you have assumptions about, so each
  assumption has somewhere to live. *Topic:* vision and graphics; the form is
  general. *Strength:* strong.
- **R2** — Check whether a nonlinear decoder is still needed once the
  representation carries the structure. *Strength:* moderate.
- **R3** — Report whether a method needs custom kernels; "pure PyTorch" is a
  real property. *Strength:* moderate.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**

R1 is the observation that leaves the domain. The record's architecture
practices reason about capacity and connectivity, and this is about **where an
assumption can be attached** — a representation that makes a prior expressible
is doing something a more general one cannot, even at equal capacity.

The document's takeaways — "hybrid representation scheme", "temporal
coherence", "efficient rendering", "appearance modeling" — name four topics and
not the mechanism, which is one line: `C(d,2)` planes for `d` dimensions.

## Limitations

- 2023, radiance fields, and the field moved to Gaussian primitives quickly.
- C1's sufficiency is empirical; pairwise planes cannot express arbitrary
  higher-order structure.
- Axis-aligned priors are the ones this helps with, and not all priors are.

## Open questions

- Where does pairwise factorisation break? The paper reports it working and does
  not characterise the signals it cannot represent.
