---
status: Proposed
promote_when: >-
  A result that answers the Birkhoff-polytope objection: a measurement of
  stream homogenization with depth under the doubly-stochastic constraint
  that finds it does not happen, or a production report at depth whose
  streams stay distinct. A further independent evaluation that does not test
  the constraint is not the missing evidence — one already arrived.
consensus: contested
consensus_note: >-
  Two independent groups attacked the doubly-stochastic constraint within a
  month of each other, by different arguments and with opposite remedies
  (LIT-151, LIT-181), while it ships at 1.6T in DeepSeek-V4. Production
  adoption and public dispute at once, which is the state `status:` alone
  could not express.
title: 'Widen the residual stream into several streams mixed by doubly-stochastic matrices (manifold-constrained hyper-connections)'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2025-12-01'
source:
- LIT-140
contested_by:
- LIT-151
- LIT-181
extends:
- SOTA-137
compared_against:
- SOTA-133
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

Why *Proposed*: **the condition this was filed under has been met, and is
not being applied.** That is worth explaining rather than quietly leaving
the status alone.

The condition was "promote on an independent result". [LIT-152](../literature.d/LIT-152.md) is one: a
different laboratory ran mHC in its own harness and found it comparable to
its own design. By the letter of the rule this should now be *Active*.

It is not, because two other independent results arrived at the same time
and both attack the specific thing this practice recommends — the
doubly-stochastic constraint. [LIT-151](../literature.d/LIT-151.md) proves the Birkhoff polytope is
bounded above but not below, so the mixing can only shrink what
distinguishes the streams and they homogenize with depth. [LIT-181](../literature.d/LIT-181.md) names
three further defects: identity degeneration, an expressivity bottleneck
from non-negativity forbidding subtractive interactions, and unstable
Sinkhorn projection. Different arguments, opposite remedies, same verdict on
the constraint.

So the honest position is that the practice's *claim* has independent
support and its *mechanism* has independent opposition, and a condition
phrased as "an independent result" cannot tell those apart. The condition
was the wrong condition.

What the five papers in this chain agree on is narrower and better attested
than what this document currently says: **widen the residual stream into
several streams and constrain the mixing** — with mHC's doubly stochastic
matrices, oHC's rotations, sHC's spectral sphere, or Qwen's gate that drops
the mixing matrix altogether all counting as instances. Restating the
practice at that level is the right move and is deliberately not made here:
it changes what the document claims rather than its status, and that is a
curation decision rather than a backlog pass.

The alternative to promoting is restating the practice at the level its
literature agrees on — widen the residual stream and constrain the mixing —
which all four papers hold and none of them disputes.

## Sequence and siblings

<!-- inactive-ok: SOTA-137 — a Superseded practice, named as the predecessor in the chain -->
Residual connection → hyper-connections ([SOTA-137](SOTA-137.md), retired) → this. The sibling
variation is Attention Residuals ([SOTA-133](SOTA-133.md), now Active): where mHC widens the stream and
constrains a fixed mixing, AttnRes keeps one stream and lets each layer
attend over its predecessors. Both are Proposed; nobody has compared them.
