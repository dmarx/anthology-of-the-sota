---
status: Active
title: 'Replace fixed residual accumulation with learned attention over preceding layers'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2026-03-01'
source:
# The paper, and the independent evaluation that promoted this to Active
# (ADR-010).
- LIT-134
- LIT-152
summary: >-
  Kimi Team (2026), [LIT-134](../literature.d/LIT-134.md) — Attention Residuals: a per-layer pseudo-query chooses which earlier layers to read, at O(d) parameters per layer; 1.25× compute advantage on scaling laws at 48B/1.4T, adopted in Kimi K3.
---

# SOTA-133: Replace fixed residual accumulation with learned attention over preceding layers

## Source

Kimi Team (2026), [LIT-134](../literature.d/LIT-134.md) — Attention Residuals.

A residual stream adds every earlier layer's output with equal weight.
Attention Residuals give each layer one learned pseudo-query that attends
over the representations of all preceding layers, so the layer reads what
it needs and dilution along depth is contained. Block AttnRes groups layers
into compressed blocks so the cross-layer attention costs O(Nd) in memory
and communication rather than O(Ld). At 48B parameters on 1.4T tokens the
paper reports a 1.25× compute advantage on scaling laws and under 2%
inference-latency overhead, with the largest gains on multi-step reasoning
and code. Kimi K3 ([LIT-131](../literature.d/LIT-131.md)) adopts it at 2.8T.

<!-- inactive-ok: SOTA-136 — a Proposed practice, named as part of the residual chain -->
The sibling variation is [SOTA-136](SOTA-136.md): where this keeps one stream and lets a
layer attend over its predecessors, manifold-constrained hyper-connections
widen the stream and constrain a fixed mixing. Both are Proposed and
nobody has compared them.

## Promoted from *Proposed*

The condition this practice was filed under — "one group, one paper, one
production model ... promote when an independent result lands" — is met.

[LIT-152](../literature.d/LIT-152.md) is a different laboratory implementing Attention Residuals in its
own harness and measuring it against its own design. At 28 layers, Full
AttnRes reaches 1.762 training loss against 1.789 for the pre-norm residual
baseline, and lands **level with Qwen's Gated Residual**; the block-summarised
variant gives up 0.008 at S = 2 and 0.011 at S = 4. At 48 layers the ordering
holds. That is a reproduction by people with no stake in the result and their
own competing design, which is the strongest form the condition could have
asked for.

What it does *not* establish, and the practice should not claim: that
AttnRes is the best member of its family. The same evaluation finds three
designs level, so the honest reading is that *replacing fixed accumulation
with something learned* is what pays, and which learned thing is unsettled.
The conditions below say so.

Conditions: the block-summarised variant is the one that scales, and it is
the weaker one — full AttnRes attends over every preceding sublayer, which
is O(Ld) in memory and communication. Expect to pay about 0.01 of loss for
the version that is affordable at depth. And the alternatives are live:
[LIT-140](../literature.d/LIT-140.md)'s mHC and [LIT-152](../literature.d/LIT-152.md)'s Gated Residual measure the same, with the
latter cheaper at inference because it drops the mixing matrix entirely.

## Known implementations

- Kimi K3; independently evaluated by the Qwen3.8-Next design study
