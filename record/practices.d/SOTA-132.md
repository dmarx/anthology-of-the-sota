---
status: Active
title: 'Interleave linear-attention layers with global attention at about 3:1 instead of using full attention throughout'
version: 1
tags:
- attention-techniques
date: '2026-09-05'
published: '2025-10-01'
source:
# Primary: the controlled comparison against full attention. The rest is
# what corroborates it — the shipped 3:1 layouts and the module they use
# (ADR-010). Falcon-H1's parallel-head layout (LIT-120, LIT-119) is the
# contrast, not support, so it stays in Variations rather than here.
- LIT-133
- LIT-136
- LIT-135
- LIT-131
- LIT-137
- LIT-183
summary: >-
  Kimi Team (2025), [LIT-133](../literature.d/LIT-133.md) — three Kimi Delta Attention layers per gated-MLA layer beat full MLA at 48B/1.4T while cutting KV cache 75%; the layout [LIT-131](../literature.d/LIT-131.md) ships at 2.8T with 69 KDA and 24 MLA layers.
---

# SOTA-132: Interleave linear-attention layers with global attention at about 3:1 instead of using full attention throughout

## Source

Kimi Team (2025), [LIT-133](../literature.d/LIT-133.md) — Kimi Linear.

Most layers carry a linear-attention module with a finite-state memory —
here Kimi Delta Attention, a gated delta rule with a channel-wise forgetting
gate — and one layer in about four keeps global attention, implemented as
Multi-Head Latent Attention so its KV cache is compressed too. On a
48B-total, 3B-active model trained for 1.4T tokens, this hybrid outperformed
full MLA under matched conditions on short-context, long-context and RL
evaluations, with up to 75% less KV cache and up to 6.3× the decoding
throughput at 1M tokens. Kimi K3 ([LIT-131](../literature.d/LIT-131.md)) ships the layout at 2.8T
parameters with 69 KDA layers and 24 gated-MLA layers.

There is a second benefit the practice was filed without, and it only shows
up in the report rather than the abstract. Kimi K3 applies **no positional
encoding at all** to its global-attention layers, letting the interleaved
KDA layers supply position sensitivity and recency instead. The consequence
the report names: extending the context stops requiring a retuned RoPE
frequency base or YaRN, because the global layers hold no positional
parameter to retune. So the hybrid is not only cheaper per token — it makes
[SOTA-139](SOTA-139.md)'s staged context extension a smaller operation. Whether that
survives without a recurrence that is itself position-sensitive is untested.

Conditions: the controlled comparison is one group's at one mid scale. The
layout has two independent adopters in the record with different linear
modules — Kimi's KDA at 2.8T ([LIT-131](../literature.d/LIT-131.md)) and Alibaba's Gated DeltaNet
([SOTA-135](SOTA-135.md)) from Qwen3-Next's 80B-A3B ([LIT-136](../literature.d/LIT-136.md)) to the dense Qwen3.8-27B
([LIT-135](../literature.d/LIT-135.md)) — which is adoption evidence, not a second controlled comparison. The ratio
is a knob — the paper's ablations settled on 3:1 — and the global layers
are what keep exact retrieval intact, so they should not be removed to
chase the throughput number.

## Sequence

The Gated DeltaNet paper's own H1 and H2 hybrids ([LIT-137](../literature.d/LIT-137.md), 2024) → Qwen3-Next
ships 3:1 Gated DeltaNet to gated attention in production ([LIT-136](../literature.d/LIT-136.md),
September 2025) → Kimi Linear's fair comparison against full attention
([LIT-133](../literature.d/LIT-133.md), October 2025, this practice's source) → Qwen3.5, 3.6 and 3.8
([LIT-135](../literature.d/LIT-135.md)) and Kimi K3 ([LIT-131](../literature.d/LIT-131.md)) at dense and frontier scale.

## Variations

A third laboratory has since adopted the layout independently:
[LIT-183](../literature.d/LIT-183.md)'s Nemotron 3 Nano is a MoE hybrid Mamba-Transformer at 30B-A3B,
using Mamba rather than a linear attention as the cheap layer. That widens
what the practice can claim — from "the 3:1 interleave works" toward "a
hybrid of a fixed-state mixer with periodic global attention works, and the
mixer's family is a second-order choice".

A third *layout* also exists now. [LIT-176](../literature.d/LIT-176.md)'s Native Hybrid Attention
puts the mixture inside one uniform layer — a linear RNN maintains long-term
KV slots, a sliding window supplies short-term tokens, and a single softmax
attends over both — so the ratio becomes a continuous hyperparameter instead
of a layer schedule. The practical argument for it is that an interleave
makes every fourth layer different, which every cache manager and pipeline
schedule then has to know about; the infrastructure sections of [LIT-131](../literature.d/LIT-131.md) and
[LIT-152](../literature.d/LIT-152.md) are largely about managing that. It has no frontier deployment, so
the practice does not move.

The other hybrid layout in the record is Falcon-H1's ([LIT-120](../literature.d/LIT-120.md)): SSM heads
and attention heads in parallel within every block, with the split a
per-block channel allocation rather than a layer schedule. [LIT-119](../literature.d/LIT-119.md)'s tiny
<!-- inactive-ok: SOTA-125 — a Proposed practice, named as the other layout's finding -->
ablations ([SOTA-125](SOTA-125.md)) found SSM capacity worth more than MLP width under that
layout; no source in the record compares the two layouts against each
other.

## Known implementations

- Kimi Linear 48B-A3B, Kimi K3; Qwen3-Next, Qwen3.5, Qwen3.6-27B, Qwen3.8-27B
