---
number: 135
status: Active
title: 'Give linear-attention layers a gated delta rule: a decay gate for erasure plus a delta update for targeted writes'
version: 2
history:
- version: 2
  date: '2026-10-06'
  note: >-
    Adds Olmo Hybrid (LIT-tmpax1wi) to `source:`. It is an independent
    test, from Ai2, of the gated delta rule against Mamba-2's decay-only
    update under one recipe from 60M to 1B, pure and in a 3:1 hybrid, and
    the gated delta rule wins at every scale. It does not test the delta
    update without the gate, so it supports half of the original comparison.
    Gated DeltaNet-2 (LIT-tmpsiw5k) joins the "where it is incomplete"
    section as a channel-wise split of β that stacks with KDA's channel-wise
    decay. The recommendation is unchanged.
tags:
- attention-techniques
date: '2026-09-05'
source:
# LIT-tmpax1wi joined at v2: an independent comparison of the gated delta
# rule against Mamba-2 at seven scales, pure and hybrid (its Table 5). It
# does not run DeltaNet without the gate.
- LIT-137
- LIT-tmpax1wi
introduced_by:
- LIT-137
summary: >-
  Yang et al. (2024), [LIT-137](../literature.d/LIT-137.md) — beats Mamba2 and DeltaNet across language modelling, retrieval and long context at 1.3B/100B; the recurrence the Qwen hybrids use for three layers in four, and the one Kimi Delta Attention extends.
extended_by:
- SOTA-177
---

# SOTA-135: Give linear-attention layers a gated delta rule: a decay gate for erasure plus a delta update for targeted writes

## Source

Yang et al. (2024), [LIT-137](../literature.d/LIT-137.md) — Gated DeltaNet.

A linear-attention layer keeps a fixed-size state and has to manage it. A
decay gate, as in Mamba2, lets the state forget fast; the delta rule, as in
DeltaNet, overwrites one key's association without disturbing the others.
The gated delta rule does both in one recurrence, and a chunkwise parallel
algorithm keeps it hardware-efficient. At 1.3B parameters on 100B tokens
it consistently beat both parents on language modelling, commonsense
reasoning, in-context retrieval, length extrapolation and long-context
understanding, and the paper's own hybrids with sliding-window attention or
Mamba2 layers did better still.

The gated delta rule is [LIT-137](../literature.d/LIT-137.md)'s own proposal: it takes Mamba2's
data-dependent decay and DeltaNet's delta update with its WY-based chunkwise
algorithm, extends that algorithm to carry the gate, and attributes the
parents' failures in its single-needle tests to forgetting too fast (Mamba2
past 2K tokens) and clearing memory poorly (DeltaNet at longer lengths).

**An independent test, at small scale.** Olmo
Hybrid ([LIT-tmpax1wi](../literature.d/LIT-tmpax1wi.md)) compared Gated DeltaNet with Mamba-2 as the recurrent
layer under one recipe at seven sizes from 60M to 1B. Gated DeltaNet won
every one of them, as a pure model (0.677 against 0.718 BPB at 1B) and in a
3:1 hybrid (0.669 against 0.698). Pure Gated DeltaNet was also slightly
ahead of the transformer (0.682). It then trained the hybrid to 7B and 6T
tokens, with the negative-eigenvalue extension that lets the state
transition take an eigenvalue of −1. Whether that extension matters for language modelling is open:
the same ablations find positive eigenvalues scale about as well. The paper
did not test the delta update without the gate, which is the other half of
what this practice says.

Conditions: on its own the layer still trails full attention on exact
retrieval, which is why every production use interleaves it with global
attention ([SOTA-132](SOTA-132.md)). The paper's evidence is at 1.3B; the production
evidence is the Qwen line from Qwen3-Next's 80B-A3B ([LIT-136](../literature.d/LIT-136.md)) to the dense
Qwen3.8-27B ([LIT-135](../literature.d/LIT-135.md)).

## Sequence

DeltaNet and Mamba2 → the gated delta rule (this practice) → Kimi Delta
Attention ([LIT-133](../literature.d/LIT-133.md)), which replaces the scalar decay with a channel-wise
one and is what Kimi K3 uses. Each keeps the delta update; the variation is
in how the state forgets.

Two things now hang off it, and only one is a descendant. The decoupled erase
is filed as a `Proposed` practice extending this one — same recurrence, a
cleanup path added beside the corrective write. RWKV-7 ([LIT-173](../literature.d/LIT-173.md)) is not: it
reaches vector-valued gating from the recurrent-network tradition rather than
from linear attention, independently and a year earlier than the
channel-wise gate here, and it carries an expressivity argument this line
does not make. Two traditions converging on per-channel gating is two data
points; treating the other line as a step in this one would make it look like
one.

## Where it is incomplete

[LIT-177](../literature.d/LIT-177.md) names an asymmetry in the pairing this practice recommends.
The delta update is active and targeted — it corrects what is stored at the
address being written — while the decay gate is passive and global. So stale
content at a *different* address can never be actively removed, only left to
decay. Decoupling the erase address from the write address fixes it, and the
gain persists through 80B tokens of long-context midtraining.

[LIT-133](../literature.d/LIT-133.md)'s channel-wise forgetting gate is the other answer to the same
pressure: finer *passive* decay rather than active removal. Nobody has
compared them directly.

Gated DeltaNet-2 ([LIT-tmpsiw5k](../literature.d/LIT-tmpsiw5k.md)) comes closest, from the group that made this
recurrence. It keeps KDA's channel-wise decay and splits β into a
channel-wise erase gate on the key and a channel-wise write gate on the
value. The erased read then runs along a reweighted key rather than the key
itself, which is a restricted form of the decoupled erase. At 1.3B / 100B
tokens and matched state it averages 53.11 against 52.28 for KDA and 52.07
for this practice's Gated DeltaNet. Most of the gain comes from the erase
gate. That says the two remedies stack, in one run at one scale.

## Known implementations

- Qwen3-Next, Qwen3.5, Qwen3.6-27B, Qwen3.8-27B (Gated DeltaNet); Kimi Linear, Kimi K3 (as KDA)
- Olmo Hybrid 7B (Gated DeltaNet with negative eigenvalues)
