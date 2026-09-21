---
number: 136
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
  could not express. A third group has since repaired the constraint's
  implementation rather than its geometry (LIT-513) — which does not
  resolve the dispute and does not join either side of it.
title: 'Widen the residual stream into several streams mixed by doubly-stochastic matrices (manifold-constrained hyper-connections)'
version: 3
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Sourced to LIT-152 as well as LIT-140. The body already called it "one:
    a different laboratory ran mHC in its own harness and found it
    comparable to its own design", and promote_when calls it an independent
    evaluation that arrived — while the field named only the source paper.
    DeepSeek-V4 shipping it at 1.6T stays adoption. Neither the status nor
    the recommendation moves.
- version: 3
  date: '2026-09-21'
  note: >-
    Adds LIT-513 as a source and one instruction: if you adopt the
    constraint, construct it exactly rather than approximating it with
    Sinkhorn-Knopp. The recommendation and the status are unchanged, and
    the promotion condition is unmet for the third time — LIT-139 was the
    production report, LIT-152 the independent evaluation, and this repairs
    the implementation; none of the three measures a stream statistic. The
    new source also makes the constraint EXACT, which is the condition under
    which LIT-151's objection should bite hardest, so the miss is recorded
    in the body rather than only in the note.
tags:
- model-architecture
date: '2026-09-05'
source:
# LIT-140 is mHC. LIT-152 is a different laboratory running mHC in its own
# harness and finding it comparable to its own design — an independent test,
# and evidence about the claim even though promote_when says it is not the
# *missing* evidence. LIT-139 ships mHC at 1.6T without measuring the
# contested property, so it is adoption (ADR-017); LIT-151 and LIT-181 are
# the dispute and live in contested_by.
- LIT-140
- LIT-152
- LIT-513
introduced_by:
- LIT-140
contested_by:
- LIT-151
- LIT-181
# Corrective succession (ADR-017): free mixing gives up the identity-mapping property, which is what makes hyper-connections unstable.
corrects:
- SOTA-137
compared_against:
- SOTA-133
summary: >-
  Xie et al. (2025), [LIT-140](../literature.d/LIT-140.md) — hyper-connections with the residual-mixing matrix constrained to be doubly stochastic, so identity mapping survives; 6–7% overhead at 3B–27B, shipped in DeepSeek-V4.
extends:
- SOTA-169
explained_by:
- THEORY-011
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

The V4 report was read in full for [#18](https://github.com/dmarx/anthology-of-the-sota/issues/18), because half this practice's
promotion condition asks for "a production report at depth whose streams
stay distinct" and V4 is the production report at depth. **It does not
answer the objection.** Its case for the constraint is numerical: projecting
onto the doubly-stochastic manifold bounds the spectral norm at 1, so the
residual transformation is non-expansive and both passes are more stable —
which is the property [LIT-151](../literature.d/LIT-151.md) grants and then argues cuts the other way, since
a mapping that can only contract is a mapping that can only erode what
distinguishes the streams. V4 measures no stream statistic, and the words
homogenize, diversity and distinct do not appear in it. So the condition
stands unmet by the one report that looked most likely to meet it — which is
a thing to say out loud, because a reader who knows V4 ships mHC at 1.6T
will otherwise assume the question was settled by shipping.

## Construct the constraint, do not approximate it

Yang (2026), [LIT-513](../literature.d/LIT-513.md) — read as [NOTE-258](../notes.d/NOTE-258.md) — shows the
Sinkhorn-Knopp projection does not arrive. Across SK inputs measured during
training, about **27.9%** have relative range `1/ν ≥ 10¹³`, where 20
iterations do not converge; a single residual matrix's column sum can be off
by **100%**, and the column sums of the layer-wise product `∏_l H^res_l` by
**220%** in a 24-layer network.

The replacement follows from Birkhoff-von Neumann: every doubly stochastic
matrix is a convex combination of permutation matrices, so parameterize the
convex weights with a softmax and the matrix is doubly stochastic **by
construction**. No iteration, no approximation gap, and no fused CUDA kernel —
native matrix operations, at throughput matching a naive implementation.

So the instruction inside this branch is: if you take the constraint, build it
rather than approximate it. What that does *not* settle is whether the
constraint is the right one, which is the dispute below.

**And it is the sharpest missed opportunity in that dispute.** Under
Sinkhorn-Knopp mHC the matrices are not actually doubly stochastic, so
[LIT-151](../literature.d/LIT-151.md)'s objection has an escape hatch: whatever keeps the streams
distinct might be surviving through the approximation gap. Exact construction
closes it. That makes [LIT-513](../literature.d/LIT-513.md) the cleanest available test of
whether the doubly-stochastic set homogenizes the streams — the objection
predicts it should homogenize *more* — and it reports no stream statistic at
all. One histogram, on a model already trained, with code already public.

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
