---
status: Active
title: 'Interleave linear-attention layers with global attention at about 3:1 instead of using full attention throughout'
version: 1
tags:
- attention-techniques
date: '2026-09-05'
published: '2025-10-01'
source: LIT-133
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

Conditions: the evidence is one group's fair comparison at one mid scale
plus one production adoption at frontier scale; independent replication
with a different linear-attention module is not in the record. The ratio
is a knob — the paper's ablations settled on 3:1 — and the global layers
are what keep exact retrieval intact, so they should not be removed to
chase the throughput number.

## Variations

The other hybrid layout in the record is Falcon-H1's ([LIT-120](../literature.d/LIT-120.md)): SSM heads
and attention heads in parallel within every block, with the split a
per-block channel allocation rather than a layer schedule. [LIT-119](../literature.d/LIT-119.md)'s tiny
<!-- inactive-ok: SOTA-125 — a Proposed practice, named as the other layout's finding -->
ablations ([SOTA-125](SOTA-125.md)) found SSM capacity worth more than MLP width under that
layout; no source in the record compares the two layouts against each
other.

## Known implementations

- Kimi Linear 48B-A3B, Kimi K3
