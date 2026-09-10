---
number: 65
status: Rejected
status_note: >-
  The cited paper contains no discussion of layer normalization. The claim is
  also doubtful on its own terms: LayerNorm's gain initialises to exactly 1
  by convention at every scale, so "closer to 1 for larger models" names no
  adjustable quantity
title: 'Initialize layer norm weights closer to 1 for larger models'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Rejected with the rest of the LIT-052 cluster.
tags:
- training-optimization
date: '2026-08-24'
source:
- LIT-052
implementations:
- vision_transformer
- bert
summary: >-
  Tay et al. (2021), [LIT-052](../literature.d/LIT-052.md) — [ARXIV-2109.10686](https://arxiv.org/abs/2109.10686). Rejected: the source contains no discussion of layer normalization, and the claim names no adjustable quantity.
---

# SOTA-065: Initialize layer norm weights closer to 1 for larger models

## Source

Tay et al. (2021), [LIT-052](../literature.d/LIT-052.md) — [ARXIV-2109.10686](https://arxiv.org/abs/2109.10686).

## Why this is rejected

Two reasons, and the second is the one worth reading.

**The source does not say it.** Searched in full, the paper contains "layer
norm" zero times. The claim came from [LIT-052](../literature.d/LIT-052.md)'s fourth replaced takeaway,
"layer normalization plays crucial role in stabilizing early training" —
itself a general statement that this practice then sharpened into a specific
initialisation rule nobody wrote.

**The instruction does not describe an action.** LayerNorm's learnable gain is
initialised to exactly 1, and its bias to 0, in every implementation the record
knows of. "Closer to 1" from 1 is not a direction. Read charitably it might
mean *scale the residual branch down at init* — which is a real technique with
real sources ([SOTA-051](SOTA-051.md)'s neighbourhood) — but that is a different practice
about a different parameter, and inferring it here would be inventing a claim
to save a citation.

That combination is what makes this the clearest member of the cluster. A
fabricated attribution can still name a true practice; this one names an
operation that cannot be performed.
