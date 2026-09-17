---
number: 51
status: 'Active'
title: 'Initialize a residual or adapter branch to exactly zero, not merely near zero'
version: 4
history:
- version: 2
  date: '2026-09-10'
  note: >-
    Enriched from the #123 readings. The recommendation is unchanged;
    the source list, the numbers or the neighbourhood are.
- version: 3
  date: '2026-09-10'
  note: >-
    Gained ControlNet (LIT-089) as a second source and the section on
    branches attached to an already-trained model. This entry was left
    truncated at the word "The" and is completed here from the source
    comments and the diff it describes.
- version: 4
  date: '2026-09-17'
  note: >-
    Retitled. The title said "near zero" while the body's whole argument is
    that zero is not near zero — it stated the weaker claim its own content
    refutes, and a reader who searched the registry for the exact-identity
    rule would not have found it. The recommendation is unchanged; what
    changes is that the title now says it.
tags:
- model-stability
date: '2026-08-24'
source:
# LIT-047 is the origin: near-zero final-layer init for depth.
# LIT-089 is what sharpens it. The body's 'zero is not near zero'
# distinction is ControlNet's zero convolutions, and under ADR-017's
# retraction test that section does not survive without it (#121).
- LIT-047
- LIT-089
introduced_by:
- LIT-047
compared_against:
- SOTA-060
- SOTA-025
summary: >-
  Bachlechner et al. (2020), [LIT-047](../literature.d/LIT-047.md) — [ARXIV-2003.04887](https://arxiv.org/abs/2003.04887). Start an added branch at
  exactly zero so it is the identity at initialisation, and let training
  raise it. Exact zero rather than small-random is the claim: a small random
  branch is PROBABLY harmless, a zero one is PROVABLY the identity — which is
  what matters when the thing being protected is a residual stack deep enough
  to attenuate, or a pretrained model expensive enough that adapter noise
  is not worth risking.
explained_by:
- THEORY-011
---

# SOTA-051: Initialize a residual or adapter branch to exactly zero, not merely near zero

## Source

Bachlechner et al. (2020), [LIT-047](../literature.d/LIT-047.md) — [ARXIV-2003.04887](https://arxiv.org/abs/2003.04887).

## Zero, not small

[LIT-047](../literature.d/LIT-047.md)'s intervention is one scalar per layer multiplying the residual
branch, initialised to **zero** — so at initialisation every block is exactly
the identity and the signal passes through an arbitrarily deep stack with no
attenuation and no amplification. Training then raises the scalars from zero
as the blocks earn their contribution.

That is stronger than "near zero" and the difference is the point: an exact
identity at initialisation means depth costs nothing at step one, so the
warmup and careful initialisation that deep stacks otherwise need become
unnecessary rather than merely easier.

## The same instinct, three places in this record

Start the residual branches quiet and let training turn them up:
[SOTA-060](SOTA-060.md)'s depth-scaled output projections, [SOTA-025](SOTA-025.md)'s slightly-shrunk
LayerNorm scale, and this. ReZero is the limiting case — the branch starts at
exactly nothing.

## The same instrument, for a branch added to a model that is already trained

The three above are about **initialising a network you are about to train**.
The identical argument governs a branch **attached to a frozen pretrained
model**, where the stakes are higher: noise from an untrained adapter is being
added to representations built from billions of examples.

[LIT-089](../literature.d/LIT-089.md) (ControlNet) connects its trainable branch to the locked backbone
through **zero convolutions** — convolution layers initialised to zero — so the
adapter is an *exact* no-op at initialisation and its parameters "progressively
grow from zero", ensuring "no harmful noise could affect the finetuning".
[SOTA-184](SOTA-184.md)'s LoRA does the same thing for the same reason: its `B` matrix starts
at zero, so the update is exactly nothing until training makes it something.

The distinction worth holding, and the one this practice's own title stated
backwards until version 4: **zero is not "near zero".** A small random initialisation makes the branch
*probably* harmless; an exact zero makes it *provably* the identity. When the
thing you are protecting is expensive and already trained, the difference
between those two is the whole point.

The cost is a slower start: a block contributing zero learns only through the
gradient that reaches its scalar, so the early steps do less than they
otherwise would. In practice this is small against the depth it buys, and it
is the reason the technique is usually described as trading a little early
progress for the ability to train deeper at all.

Modern large models mostly use the scaled-initialisation form rather than a
learned gate, so this practice is best read as the clearest statement of a
principle the record applies in weaker versions elsewhere.
