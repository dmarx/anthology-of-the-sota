---
status: Read
paper: LIT-tmphmfch
title: 'Modular Duality in Deep Learning'
version: 1
date: '2026-09-19'
summary: >-
  Gradients live in the dual space and weights live in the primal one, so
  subtracting one from the other is a type error that ordinary gradient
  descent commits every step. Fix it with a duality map built recursively from
  per-layer operator norms. Two consequences the record cares about: muP and
  Shampoo turn out to be partial approximations of one such map, and the map
  for Linear layers is a Newton-Schulz iteration — which is Muon.
---

# NOTE-tmpq1cy8: Modular Duality in Deep Learning

## Contribution

A construction, and a unification that falls out of it. The construction is
**modular dualization**: assign each layer an operator norm chosen from its
input-output semantics, derive that layer's duality map, and recurse over the
architecture to get a map on the whole weight space. The unification is that
two methods nobody had connected turn out to be the same map, approximated
differently.

## Key insight

The complaint is old and the paper says so — duality maps are routine in
physics and applied maths, and central to mirror descent, natural gradient
descent and steepest descent on a normed space. What had not happened is
anyone taking the objection seriously *for general architectures*. Prior work
(spectral descent, duality structure gradient descent) derived maps for single
linear layers and then extended them heuristically to all-layer updates.

The move that makes it work is **choosing the norm from the layer's
semantics** rather than from mathematical convenience. An `Embed` layer, a
`Linear` layer and a `Conv2D` layer are doing different things to different
kinds of object, so they get different operator norms, and the recursion
composes them.

## Concepts

- **Duality map** — takes a dual vector (the gradient) to the primal space
  (where weights live), given a norm
- **Modular dualization** — the three-step recursive construction
- **RMS–RMS operator norm** — the norm whose duality map both muP and Shampoo
  approximate
- **Rectangular Newton-Schulz iteration** — the GPU-friendly algorithm for the
  `Linear` and `Conv2D` maps, from Kovarik (1970) and Björck & Bowie (1971)

## Assumptions

- **The architecture decomposes into modules with nameable semantics.** The
  whole construction is recursive over that decomposition
- **The operator norm assignment is the right one.** This is the paper's
  substantive modelling choice and it is argued from semantics rather than
  derived
- **The Newton-Schulz approximation is close enough.** The exact map is a
  polar factor; the iteration approximates it in a few matmuls
- **Duality is the right frame at all** — that steepest descent under a
  well-chosen norm is what a good optimizer is doing

## Key results

- **muP and Shampoo are partial approximations to one duality map**, the one
  induced by the RMS–RMS operator norm (§4.1). *Holds when:* the derivation's
  norm assignment; both are described as partial.
- **Duality maps for `Embed`, `Linear` and `Conv2D`**, with GPU-friendly
  algorithms — the last two by rectangular Newton-Schulz.
- **A variant set NanoGPT speed records.** This is the empirical claim and it
  is reported rather than benchmarked here.
- **The update rule is one line**: `weight - LR * dualize(weight.grad)`.

## Limitations

- **The speed-record claim is secondhand within the paper** — "a variant of
  our methods". It is not a controlled comparison and this paper does not
  attempt one
- **No large-scale experiments of its own.** This is a theory paper; the
  evidence for the resulting optimizer is elsewhere, in the record at
  `LIT-122`, `LIT-132` and `LIT-131`
- **The norm assignment is a modelling choice**, and a different assignment
  gives a different optimizer. The theory says what follows *from* a choice
  rather than fixing the choice
- **"Partial approximations" is doing work.** The paper does not claim muP and
  Shampoo are *equal* to the duality map, and how much is lost is not
  quantified here

## Connections

`LIT-tmp1tday` is the parent: the modular norm is the object this dualizes
against. `LIT-tmpee0q4` is the grandparent and the reason the spectral norm is
the quantity in play. `LIT-159` is the blog post that introduced Muon and is
the record's only source for ten practices; `LIT-122`, `LIT-132` and `LIT-131`
are the production and scaling evidence.

## Bearing on the record

Sources `THEORY-tmpm3lav`, which is the account those ten practices have
lacked. The record could say *use Muon* and *use SOAP* and *use muP* and had
no way to say that the first is a duality map, and the other two are
approximations of the same one.

The honest limit: this explains **why the shape is right**, not why the
constants are. `SOTA-121`'s decoupled weight decay and AdamW-matched update
RMS, and `SOTA-131`'s QK-Clip, are engineering the theory does not reach.
