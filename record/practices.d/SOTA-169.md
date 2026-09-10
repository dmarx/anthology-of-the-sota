---
number: 169
# inactive-ok-file: LIT-141 — the original hyper-connections paper, Superseded
# by its own successor at the practice layer and named throughout this
# document on purpose: it is the origin of the line this practice is the
# trunk of, and the paper that established the width the three constraints
# argue over.
status: Proposed
formerly:
- SOTA-tmpzajmo
promote_when: >-
  A second laboratory shipping a widened, constrained residual stream in a
  released model, or a study that isolates width-with-constrained-mixing
  against a single stream at matched parameters and reports what the width
  bought independently of which constraint was used. What would not move it:
  another paper proposing a fourth constraint, which is evidence about the
  branches and is what the record already has four of.
consensus: emerging
consensus_note: >-
  Four papers from at least three groups agree the residual stream should be
  widened and the mixing constrained, and DeepSeek-V4 ships it at 1.6T. What
  they disagree about is which constraint, which is the branch rather than
  this trunk. Not `converged`: one production deployment is not the field,
  and Llama, Qwen and Mistral ship a single residual stream.
title: 'Widen the residual stream into several streams and constrain the mixing between them'
version: 1
tags:
- model-architecture
date: '2026-09-08'
source:
# The four papers in the line plus the independent evaluation. Each reports
# gains from widening; they differ on the constraint, which is what the two
# branches below are. LIT-139 ships mHC at 1.6T without measuring the
# property, so it is adoption and lives in consensus_note (ADR-017).
- LIT-141
- LIT-140
- LIT-151
- LIT-181
- LIT-152
extended_by:
- SOTA-136
- SOTA-137
implementations: []
summary: >-
  Zhu et al. (2024) and three successors, [LIT-141](../literature.d/LIT-141.md) / [LIT-140](../literature.d/LIT-140.md) / [LIT-151](../literature.d/LIT-151.md) /
  [LIT-181](../literature.d/LIT-181.md) — replace the single residual stream with n parallel streams and
  learn the mixing. All four agree the width helps and that the mixing needs
  a constraint; they disagree about which one, and that disagreement is the
  two practices extending this rather than this itself.
---

# SOTA-169: Widen the residual stream into several streams and constrain the mixing between them

## Source

Zhu et al. (2024), [LIT-141](../literature.d/LIT-141.md) — Hyper-Connections; then [LIT-140](../literature.d/LIT-140.md) (mHC), [LIT-151](../literature.d/LIT-151.md)
(oHC) and [LIT-181](../literature.d/LIT-181.md) (spectral-sphere), each proposing a different constraint;
and [LIT-152](../literature.d/LIT-152.md), a third-party design study running mHC in its own harness.

Replace the single residual stream with **n parallel streams** (n = 2 in most
published runs) and learn the mixing between them, so the network can tune
connection strength across depth and exchange information laterally. The
motivation is the seesaw between vanishing gradients and representation
collapse that fixed residual variants cannot escape.

The original learned the mixing freely, and the three papers since all agree
that free mixing is the part that breaks: it discards the identity mapping a
residual guarantees. **What they agree on is the shape of this practice —
widen, and constrain the mixing somehow.** What they disagree about is the
constraint.

## The trunk, and why it is filed separately from its branches

<!-- inactive-ok-block: SOTA-136 — Proposed, and named as the branch this
     practice is the trunk of -->
- [SOTA-136](SOTA-136.md) — constrain to the doubly-stochastic manifold (mHC). `Proposed`
  and `contested`: two groups attacked the constraint within a month, by
  different arguments and with opposite remedies.
<!-- inactive-ok-block: SOTA-137 — Superseded, and named as the branch it is -->
- [SOTA-137](SOTA-137.md) — mix freely (the original). Superseded by the above.

Filing the branches and not the trunk left the record in an odd position: the
*disputed* part of the design had a node and the *agreed* part did not. That
is backwards, and it is why the record could recommend a layer ratio defined
in terms of a structure it had never stated.

The disagreement is genuinely about the constraint, not about the width.
[LIT-151](../literature.d/LIT-151.md) argues the doubly-stochastic set is bounded above but not below, so
mixing can only shrink what distinguishes the streams; [LIT-181](../literature.d/LIT-181.md) argues the
same set is degenerate near the identity and cannot subtract at all.
Different arguments, same verdict, opposite remedies — SO(n) rotation against
a spectral sphere. Neither disputes that widening helps.

## Conditions, and why this is Proposed rather than Active

The record has one production deployment (DeepSeek-V4, at 1.6T, using the
mHC constraint) and four research papers. Nothing isolates what the *width*
buys independently of which constraint was chosen, so the trunk's evidence is
four papers that each measured a different bundle and agreed on the sign.

This is also, deliberately, the practice that [ADR-015](../decisions.d/ADR-015.md) declined to file — on
the grounds that "converting a hedge into an assertion is an editorial act".
`Proposed` is the hedge, so filing it here converts nothing: it gives the
agreement a node that can carry a promotion condition and accumulate a
consensus reading, which prose in a note cannot do.

## Known implementations

- DeepSeek-V4 at 1.6T, via the mHC constraint.
- Against, by silence: Llama, Qwen and Mistral ship a single residual stream.
