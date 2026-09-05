---
status: Proposed
title: 'Widen the residual stream into several streams mixed by doubly-stochastic matrices (manifold-constrained hyper-connections)'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2025-12-01'
source:
- LIT-140
summary: >-
  Xie et al. (2025), [LIT-140](../literature.d/LIT-140.md) — hyper-connections with the residual-mixing matrix constrained to be doubly stochastic, so identity mapping survives; 6–7% overhead at 3B–27B, shipped in DeepSeek-V4.
---

# SOTA-136: Widen the residual stream into several streams mixed by doubly-stochastic matrices (manifold-constrained hyper-connections)

## Source

Xie et al. (2025), [LIT-140](../literature.d/LIT-140.md) — mHC.

<!-- inactive-ok: SOTA-137 — a Superseded practice, named as the predecessor in the chain -->
Keep the wider residual stream of hyper-connections ([SOTA-137](SOTA-137.md)) but constrain how
the streams mix: the matrix that carries them from one layer to the next is
projected onto the doubly-stochastic manifold with Sinkhorn-Knopp
iterations — entries non-negative, rows and columns summing to one — which
bounds its spectral norm and restores the identity-mapping property that
free mixing gave up. The pre- and post-mixing maps stay non-negative. The
paper reports the quality gains of hyper-connections at 6–7% training
overhead across 3B, 9B and 27B, and DeepSeek-V4 ([LIT-139](../literature.d/LIT-139.md)) ships it at 1.6T.

Why *Proposed*: one group's paper and that group's production model, the
same standing as the other replacement for the residual in the record.
Promote on an independent result.

## Sequence and siblings

<!-- inactive-ok: SOTA-137 — a Superseded practice, named as the predecessor in the chain -->
Residual connection → hyper-connections ([SOTA-137](SOTA-137.md), retired) → this. The sibling
<!-- inactive-ok: SOTA-133 — a Proposed practice, named as the sibling variation -->
variation is Attention Residuals ([SOTA-133](SOTA-133.md)): where mHC widens the stream and
constrains a fixed mixing, AttnRes keeps one stream and lets each layer
attend over its predecessors. Both are Proposed; nobody has compared them.
