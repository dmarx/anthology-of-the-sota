---
status: Active
formerly:
- SOTA-tmpslb73
consensus: emerging
consensus_note: >-
  Three laboratories, three different local mechanisms, the same layout and
  the same ratio, within ten months and without replicating each other's
  setup: Cohere (LIT-208, January 2025), NVIDIA (LIT-209, April
  2025), Kimi (LIT-133, October 2025, shipped at 2.8T in LIT-131). Not
  `converged`, because no frontier report outside those three uses it and
  nobody has compared it against a properly extended RoPE model at matched
  cost.
title: 'Drop positional encoding from the global-attention layers of a hybrid and let the cheap local layers carry position'
version: 2
history:
- version: 2
  date: '2026-09-07'
  note: >-
    LIT-131 removed from the source list. This practice was filed four days
    into the source pass and its own comment said "then the deployments" —
    a deployment named as support, before ADR-017 settled that adoption
    without a test is consensus data. K3 ships the layout at 2.8T and runs
    no ablation; Kimi Linear ran it. The consensus_note already named K3, so
    `emerging` still rests on the same three laboratories.
tags:
- attention-techniques
date: '2026-09-07'
published: '2025-01-01'
source:
# The origin, then the two designs that arrived at the layout independently.
# LIT-207 is not a hybrid paper — it is the result the
# other three rest on — but it is the source of the claim that the global
# layers lose nothing by dropping the encoding.
# LIT-131 came out. The comment below used to end "then the deployments",
# which is a deployment named as a source — written before ADR-017 said that
# adoption without a test is consensus data. K3 ships the layout at 2.8T and
# runs no ablation of its own; Kimi Linear (LIT-133) is the one that did.
- LIT-208
- LIT-209
- LIT-133
- LIT-207
implementations:
- 'RNoPE-SWA (Cohere, 8B)'
- 'SWAN-GPT (NVIDIA, 1B and 8B)'
- 'Kimi Linear 48B-A3B'
- 'Kimi K3'
compared_against:
- SOTA-063
summary: >-
  Yang et al. (2025), Puvvada et al. (2025) and the Kimi Team (2025) —
  in a model that already interleaves full attention with a cheap local
  mixer, the full-attention layers do not need a positional encoding: the
  local layers carry position and recency, and the global layers do retrieval
  better without one. Three groups, three different local mechanisms, the
  same one-global-per-three-local layout. The payoff is that extending the
  context needs no RoPE rescaling, because there is no positional parameter
  left to rescale.
---

# SOTA-153: Drop positional encoding from the global-attention layers of a hybrid and let the cheap local layers carry position

## Source

Yang et al. (2025), [LIT-208](../literature.d/LIT-208.md) — RNoPE-SWA. Puvvada et al. (2025),
[LIT-209](../literature.d/LIT-209.md) — SWAN-GPT. Kimi Team (2025), [LIT-133](../literature.d/LIT-133.md) — Kimi Linear.

## What to do

In a model whose layers alternate between full attention and something
cheaper — sliding-window attention, or a linear-attention recurrence — give
the full-attention layers **no positional encoding at all**, and leave the
encoding, or the recurrence, to the cheap layers. All three sources put one
global layer per three local ones.

## Why it works

Because the two layer types are being asked for different things, and an
encoding helps one and hurts the other.

[LIT-208](../literature.d/LIT-208.md) measured it. In a hybrid, the NoPE layers show a sharp spike of
attention mass on the tokens being retrieved and comparatively little recency
bias; the RoPE layers show strong recency and almost no retrieval. Retrieval
and locality are separable jobs, each layer type is bad at the other's, and
the positional encoding is what makes a layer local. So a layer you want to
retrieve over the whole sequence is a layer you should not make local.

[LIT-207](../literature.d/LIT-207.md) is why this costs nothing: a decoder-only transformer without a
positional encoding can represent absolute and relative position anyway, and
in a hybrid it does not even have to, because a windowed layer or a decaying
recurrence sitting beneath it already has.

## The consequence that matters most

**Context extension stops being an operation.** There is no positional
parameter in the global layers, so there is nothing to rescale: no retuned
base frequency, no interpolation, no YaRN. [LIT-131](../literature.d/LIT-131.md) reports reaching 1M tokens
this way and says so in as many words. [LIT-209](../literature.d/LIT-209.md) gets extrapolation well
past its training length with no long-context training stage at all.

This is the same problem [SOTA-151](SOTA-151.md) solves the other way, which is why the two
are filed as alternatives rather than as a sequence.

## Conditions, and what the sources disagree about

**The local layers have to be genuinely local.** [LIT-208](../literature.d/LIT-208.md)'s sharpest
negative result: widening the RoPE layers by raising the base frequency
*damages* the NoPE layers downstream, because the extra span is noise to a
layer trying to compute similarity. Needle attention mass fell from 0.0765 to
0.0369 and the needles score from 8.036 to 6.203 as θ went from 10,000 to
4 million. The fix was to confine the RoPE layers to a 4096-token window. If
you take one condition from this practice, take this one — it inverts the
reflex that longer context means a bigger base frequency.

**Whether inference-time attention scaling is required is unsettled.**
[LIT-209](../literature.d/LIT-209.md) says a dynamic scaling of attention scores is the crucial
element keeping global NoPE layers usable far past the training length, and
names [LIT-208](../literature.d/LIT-208.md) as lacking it. [LIT-208](../literature.d/LIT-208.md) reports good long-context
results without it, and [LIT-133](../literature.d/LIT-133.md) does not use it either. Two of three say it is
not needed; the one that says it is has the strongest extrapolation claim.
Nobody has run the comparison.

**The ratio is 1:3 in all three and ablated in one.** [LIT-208](../literature.d/LIT-208.md) tested
1:1, 1:3 and 1:7 and found 1:3 best; the position of the global layer within
the group did not matter. Two independent groups arriving at the same ratio is
suggestive, not a law — and the ablation is one lab's, on one architecture.

**It is not only a pretraining decision.** This is the correction
[LIT-209](../literature.d/LIT-209.md) forces on the record. An 8B RoPE model pretrained on 15T tokens
was converted by initialising from its weights, removing the encoding from
the global layers, windowing the local ones, and continuing to pretrain; it
came back at 71.55 against the original's 70.95 across GSM8k, MATH500, MBPP,
HumanEval, MT-Bench and RULER. Continued pretraining is not free and most
readers will not do it, but "an existing model cannot take this option" —
which [SOTA-063](SOTA-063.md) and [SOTA-151](SOTA-151.md) both said until now — is false.

## What would move this to `converged`

A frontier report from outside Cohere, NVIDIA and Kimi shipping the layout;
or a controlled comparison against a properly extended RoPE model — YaRN at
the same context and matched training cost — rather than against an
unextended baseline. Every comparison in the record so far is against a RoPE
model that was *not* given the rescaling treatment [SOTA-151](SOTA-151.md) recommends, which
is the weakest point in the case.

## Adjacent, and not the same practice

[SOTA-132](SOTA-132.md) recommends the 3:1 interleave of linear attention with global
attention. This practice is about what the global layers do with position,
and it applies to a windowed-attention hybrid just as well — two of the three
sources here have no linear attention in them at all. The two travel together
in Kimi's models and are separable everywhere else.
