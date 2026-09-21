---
number: 205
status: Active
formerly:
- SOTA-tmpjpcc8
consensus: converged
consensus_note: >-
  Four papers in the record, three different explicit structures — a hash
  grid, planar factorisations, anisotropic Gaussians — reaching the same
  conclusion independently within eighteen months, each getting orders of
  magnitude from it. The readings name the convergence themselves: K-Planes
  is recorded as "the third explicit-structure replacement for a large
  coordinate network", and NeuS2 as inheriting the line.
title: 'Replace a large coordinate network with a compact explicit structure and a small decoder'
version: 2
history:
- version: 2
  date: '2026-09-21'
  note: >-
    Adds LIT-tmpuxbgc as a fifth source and the practice's first outside 3D.
    v1 rested on four radiance-field papers, so the claim was stated generally
    and evidenced in one setting. Image-GS carries it to single-image
    representation and supplies the decode-cost number the practice wanted:
    0.3K multiply-accumulates per pixel against a comparable neural codec's
    3K. No change to the recommendation.
tags:
- vision-and-graphics
date: '2026-09-10'
source:
- LIT-064
- LIT-108
- LIT-086
- LIT-109
- LIT-tmpuxbgc
introduced_by:
- LIT-064
implementations:
- Instant-NGP
- 3D Gaussian Splatting
- K-Planes
- NeuS2
summary: >-
  Four independent groups, three structures. Where a field is queried
  pointwise and the signal is spatially sparse, the capacity belongs in an
  addressable structure that training optimises directly, not in a network
  evaluated per point.
---

# SOTA-205: Replace a large coordinate network with a compact explicit structure and a small decoder

## Source

Four papers, converging from different directions:

- Müller et al. (2022), [LIT-064](../literature.d/LIT-064.md) — a **multiresolution hash grid**;
  training in seconds, rendering in tens of milliseconds.
- Kerbl et al. (2023), [LIT-108](../literature.d/LIT-108.md) — **anisotropic 3D Gaussians**; the first
  real-time (>=30 fps) radiance-field rendering at 1080p.
- Fridovich-Keil et al. (2023), [LIT-086](../literature.d/LIT-086.md) — **planar factorisation**, and
  the one that needs no custom kernels.
- Wang et al. (2023), [LIT-109](../literature.d/LIT-109.md) — the hash-encoding line applied to
  implicit **surfaces** rather than radiance fields.
- Zhang et al. (2024), [LIT-tmpuxbgc](../literature.d/LIT-tmpuxbgc.md) — read as [NOTE-tmpl6noj](../notes.d/NOTE-tmpl6noj.md) —
  **2D Gaussians for a single image**, and the first source here outside 3D.

## What it costs to decode, measured

The four 3D sources argue the case from rendering speed, which entangles the
representation with a rasterizer. [LIT-tmpuxbgc](../literature.d/LIT-tmpuxbgc.md) gives the number in
the units the claim is actually about: **0.3K multiply-accumulates per pixel**
to decode, against **3K MACs at 0.31 bpp** for C3, a neural codec in the same
quality range. An order of magnitude, from moving the capacity out of the
network.

It also shows the claim is not confined to scenes. A single image has no
viewpoint, no occlusion and no geometry to exploit, so it is close to the
weakest case for an explicit structure — and the explicit structure still wins
against six implicit baselines held at matched model size, across the bitrate
range.

## The claim

The instinct when a coordinate-queried field is too slow is to make the network
smaller or the sampling cheaper. These four do something else: they move the
capacity out of the network entirely, into a structure that can be **addressed
rather than evaluated** — a hash table, a set of planes, a set of primitives —
and leave a small decoder behind it.

The decoder can then be small because the structure already carries the
variation. K-Planes states the strong form: put the structure in the
representation and **the decoder can be linear**. That is the opposite of the
usual instinct to add capacity where the output is produced.

## Why this is one practice and not four

The three structures are not variants of one method — a hash grid, a plane
factorisation and a cloud of Gaussians have almost nothing in common
mechanically. What they share is the *decision*: that for a spatially sparse
signal, lookup beats evaluation. Three groups arriving there by different
routes within eighteen months is stronger evidence for the decision than any of
them is for its own structure.

## Conditions

- **The signal must be spatially sparse** — that is what makes an addressable
  structure smaller than the network it replaces, and what makes hash collisions
  survivable: [LIT-064](../literature.d/LIT-064.md) accepts collisions and lets training absorb them
  rather than building a mechanism to resolve them.
- **Something must place the structure.** [LIT-108](../literature.d/LIT-108.md) initialises its
  Gaussians from the sparse points that camera calibration already produced, and
  ablates that choice as load-bearing. The general form — initialise from
  structure you already computed — is the practice's most portable corollary and
  the record holds one ablation of it.
- **Custom kernels are a real cost.** [LIT-086](../literature.d/LIT-086.md) makes the point by not
  needing them; whether a method requires them belongs in its report.
- The quality/cost trade should be exposed as one number. [LIT-064](../literature.d/LIT-064.md)'s is
  hash table size.

## Scope

This takes a domain topic under [ADR-026](../decisions.d/ADR-026.md) because it is a claim about
neural graphics primitives as such: the sparsity it depends on is a property of
3D scenes, and there is no version of it that survives the domain changing. The
generalised form — "prefer lookup to evaluation where the signal is sparse" —
would be an aphorism, not a practice, and the record does not hold it.

## Known implementations

- Instant-NGP, 3D Gaussian Splatting, K-Planes, NeuS2 — and the tooling built on
  the first two is where most practitioners meet this.
