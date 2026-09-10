---
number: 35
# inactive-ok: LIT-094 — Rejected, and this document is the reading that says why the paper is in the attic and what survives it
paper: LIT-094
status: Read
formerly:
- NOTE-tmpccocu
title: 'Neural Scene Graphs for Dynamic Scenes'
version: 1
tags:
- vision-and-graphics
date: '2026-09-09'
published: '2020-11-01'
summary: >-
  The first neural rendering method to decompose a dynamic scene into a scene graph — objects with learned transformations and radiance, described by a single implicit function plus a per-object latent — so novel arrangements can be rendered, not just novel views. Learned from a video alone.
---

# NOTE-035: Neural Scene Graphs for Dynamic Scenes

## Contribution

Implicit neural rendering at the time encoded an entire static scene into **one**
network, which meant it could render new *views* and nothing else. This paper
decomposes a dynamic scene into a **learned scene graph**: nodes are objects with
their own transformation and radiance, and the graph is what gets rendered.

The consequence is compositional: **novel arrangements and unseen sets of
objects at unseen poses**, not merely novel viewpoints of a fixed configuration.
Learned "only by observing a video of this scene".

## Key insight

Rendering a new viewpoint and rendering a new *arrangement* are different
capabilities, and the second requires that objects be separable entities in the
representation. Baking a scene into one network makes the first easy and the
second impossible.

The economical part: rather than one implicit function per object, **one shared
implicit function plus a per-object latent** describes them all. Objects share
what they have in common — how surfaces and radiance work — and differ in a
code, which is what allows *unseen* objects to be placed.

## Assumptions

- Objects are separable from a video with the supervision available (RGB plus,
  in the automotive setting, tracking).
- A single implicit function with a latent spans the object variation present —
  reasonable for a domain like vehicles, and the reason automotive data is the
  demonstration.
- Rigid-body object transformations.

## Key results

- **The first neural rendering method decomposing dynamic scenes into scene
  graphs.**
- Learned from video alone, on synthetic and real automotive data.
- Renders **novel scene compositions with unseen sets of objects at unseen
  poses.**

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A dynamic scene can be decomposed into a learned scene graph from video | strong | the demonstration |
| C2 | One implicit function plus per-object latents suffices | moderate | works for the object classes shown |
| C3 | Novel compositions render photo-realistically | moderate | shown on automotive data |

## Method

Learn a scene graph whose nodes carry object transformations and a latent code,
with a shared implicit function for radiance and density. Render by composing
node contributions along rays.

## Concepts

- **Structure as a capability enabler** — the graph is not a compression or an
  efficiency device; it is what makes recomposition possible at all.
- **Shared function plus per-instance code** — the same economy as a class
  embedding, applied to implicit geometry.

## Connections

The ancestor of the dynamic and compositional radiance-field work that followed,
including the dynamic extensions of `LIT-108`'s Gaussian primitives that this
batch's other papers stop short of.

C2's shape — one model, one latent per instance — is the same idea as
`LIT-118`'s stacked ID embedding and `LIT-078`'s pseudo-word: **put the shared
mechanism in the parameters and the identity in a code.** Three instances in this
pass, in three domains.

## Recommendations

- **R1** — If a capability requires manipulating parts, the representation must
  have parts; no amount of capacity in a monolithic model supplies them.
  *Topic:* vision and graphics; the form is general. *Strength:* strong.
- **R2** — Share the mechanism and vary a per-instance code. *Strength:*
  moderate.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice**, and the
document is `Superseded`. The reading does not argue with that: neural scene
graphs were overtaken by faster representations, and 2020 automotive NeRF is not
a line the anthology tracks.

R1 is the durable statement: **a capability that requires manipulating parts
cannot be obtained from a representation without parts.** That is an argument
about representation design rather than about capacity, and it is the same
argument `LIT-070`'s attribute-binding failure makes from the other direction —
there, a representation *without* the needed structure could not carry it no
matter how good the decoder was.

The document's takeaways — "dynamic scene representation", "object
relationships", "temporal coherence", "hierarchical structure" — name plausible
adjacent topics. **"Temporal coherence" is not a claim this paper makes**; the
dynamics come from object transformations in a graph, not from a coherence
constraint over time.

## Limitations

- 2020, automotive data, rigid objects.
- C2 holds for object classes with a shared shape prior.
- Superseded on speed and quality by the explicit-representation line.

## Open questions

- What supervision is minimally required to get the decomposition? "Only by
  observing a video" is doing some work in a setting with tracking available.
