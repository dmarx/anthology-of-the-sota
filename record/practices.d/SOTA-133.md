---
status: Proposed
title: 'Replace fixed residual accumulation with learned attention over preceding layers'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2026-03-01'
source: LIT-134
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

Why *Proposed*: one group, one paper, one production model. The residual
connection is the most-replicated component in the field, and a replacement
for it should collect an independent result before the record calls it
practice. Promote when one lands.

## Known implementations

- Kimi K3
