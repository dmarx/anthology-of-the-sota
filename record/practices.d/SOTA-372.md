---
number: 372
status: Active
formerly:
- SOTA-tmpvf6yn
consensus: converged
consensus_note: >-
  The design outlived the objective that motivated it. `SOTA-250`, which
  argues against MAE's reconstruction target, describes an architecture with
  the same asymmetry — a context encoder that never sees the masked regions
  and a separate predictor — and `LIT-216` reports a ViT-H/14 in under 1200
  GPU-hours on the strength of it. `#304`'s remaining units are where a
  counterexample would show up; none has so far. Read as of 2026-09.
title: 'Run the encoder on visible tokens only and push the mask tokens into a small decoder you discard'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    `training-optimization` added. The practice's measured result is a
    training-cost one — 3× or more faster pretraining at lower memory — and
    SOTA-359 took the same topic on the same grounds. Written now because
    SOTA-429 extends both this practice and SOTA-359, joining their
    lines, and this was the one member not carrying the topic the rest share
    (ADR-049). Recommendation unchanged.
tags:
- systems-optimization
- representation-and-encoding
- training-optimization
date: '2026-09-23'
source:
- LIT-601
introduced_by:
- LIT-601
implementations: []
extended_by:
- SOTA-429
---

<!-- inactive-ok-file: SOTA-429 — Proposed; named in the history as the practice whose relation prompted the retag -->
# SOTA-372: Run the encoder on visible tokens only and push the mask tokens into a small decoder you discard

## Source

He et al. (2021), [LIT-601](../literature.d/LIT-601.md) — [ARXIV-2111.06377](https://arxiv.org/abs/2111.06377).

## The claim

In a masked-prediction objective, the obvious implementation feeds the full
sequence to the encoder with masked positions replaced by a mask token. Do
not. **Give the encoder only the visible tokens**, and introduce the mask
tokens afterwards, to a small decoder that you throw away after pretraining.

Two asymmetries, and both matter:

- **The encoder never sees a mask token.** At a 75% ratio it processes a
  quarter of the sequence, so its cost falls by roughly that factor — and it
  is also never trained on an input distribution that does not occur at
  inference time, since real images have no mask tokens.
- **The decoder is lightweight and disposable.** Its job is to get from a
  latent to the target, which is a lower-level task than recognition, so it
  does not need to be large and its weights are not what you keep.

The measured result is **3× or more** faster pretraining and reduced memory,
"without any specialized sparse operations".

## Why it generalises past this paper's objective

Because it says nothing about the target. `SOTA-250` argues the opposite of
MAE on *what* to predict — representations rather than pixels — and arrives
at the same structural asymmetry: an encoder on the context only, a separate
predictor for the masked regions. Two objectives that disagree, one
architecture.

That is the mark of a design that is about the *computation* rather than the
*claim*, and it is why this is filed as a practice separate from the paper's
argument.

## Conditions

- **It requires an architecture that can drop tokens**, which is why this
  arrived after ViT ([LIT-587](../literature.d/LIT-587.md)) and not before. A convolution over a regular
  grid cannot simply omit a quarter of its input.
- **The saving scales with the masking ratio**, so it compounds with
  [SOTA-373](SOTA-373.md) and is worth much less at a low ratio. On a signal that
  cannot tolerate heavy masking this practice mostly evaporates.
- **Decoder depth is not free to choose** — see the conditions on
  [SOTA-373](SOTA-373.md) and the note's ablation. "Lightweight" is a claim about
  parameters, not about depth being irrelevant: a single block already gives
  84.8% fine-tuned, but linear probing wants more.
- **The encoder's positional embeddings still carry the layout**, so the
  visible tokens are not an unordered set. Dropping tokens is not the same as
  dropping the geometry.

## Known implementations

-
