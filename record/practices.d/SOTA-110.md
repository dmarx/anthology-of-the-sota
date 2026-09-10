---
number: 110
status: 'Active'
title: 'Consider Monarch Mixer in place of attention for very long sequence tasks'
version: 3
history:
- version: 1
  note: >-
    Titled "Consider for very long sequence tasks" — which never names its
    subject. All three practices from this source share the defect: they were
    bullets under a heading that supplied the subject, promoted one-to-one
    without it, so each reads as an instruction with no object.
- version: 2
  note: >-
    Subject restored to the title. The claim is unchanged; the source is
    LIT-115 and has always been Monarch Mixer.
- version: 3
  date: '2026-09-09'
  note: >-
    Bhardwaj → Fu in the citation line. LIT-115's first_author held a
    name belonging to no author of Monarch Mixer; corrected at that
    note's version 2 and here, where it was rendered into prose. The
    recommendation is unchanged.
tags:
- attention-techniques
date: '2026-08-24'
source:
- LIT-115
summary: >-
  Fu et al. (2023), [LIT-115](../literature.d/LIT-115.md) — [ARXIV-2310.12109](https://arxiv.org/abs/2310.12109).
---

# SOTA-110: Consider Monarch Mixer in place of attention for very long sequence tasks

## Source

Fu et al. (2023), [LIT-115](../literature.d/LIT-115.md) — [ARXIV-2310.12109](https://arxiv.org/abs/2310.12109).

## The regime where the substitution is worth considering

Long sequences are where attention's quadratic term dominates everything else,
so they are where a sub-quadratic mixer has the most to give back. That is the
whole of the recommendation, and the condition [SOTA-111](SOTA-111.md) states is the general
form of it.

Two things make "consider" the right verb rather than "use". Exactness is
given up — attention computes a data-dependent all-pairs interaction and a
structured mixer approximates the mixing, so the substitution is a modelling
decision and not an implementation one. And the ecosystem is not neutral:
attention has fused kernels, quantised inference paths and serving systems
built around its KV cache ([SOTA-105](SOTA-105.md)), none of which transfer.

## What the record cannot tell you

Where "very long" begins. [LIT-115](../literature.d/LIT-115.md) gives the architecture and its asymptotics;
this record holds no measurement of the crossover length for a given model
size, and the answer moves every time attention's constant factor improves —
which it has repeatedly ([SOTA-085](SOTA-085.md), [SOTA-106](SOTA-106.md)).

That is a real gap rather than a quibble: a practice whose condition is a
threshold nobody has measured cannot be followed except by measuring it
yourself, which is what a reader should take from this.
