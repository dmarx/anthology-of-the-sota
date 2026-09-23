---
status: Proposed
promote_when: >-
  The key and value analyses repeated on current gated-FFN models at scale,
  with automated rather than hand annotation of key patterns, finding
  value-key agreement in upper layers well above the 3.5% in the source.
  Or a causal test: editing one value vector shifts the model's next-token
  distribution in the direction its vocabulary projection predicts, on
  inputs that trigger its key.
title: 'A transformer''s feed-forward layers work as key-value memories: each hidden unit''s input weights match input patterns, and its output weights promote the tokens that follow them'
version: 1
tags:
- analysis-and-evaluation
- model-architecture
date: '2026-09-23'
source:
- LIT-tmp96ozs
summary: >-
  Geva et al. (2021), [LIT-tmp96ozs](../literature.d/LIT-tmp96ozs.md) — read FF(x) = f(xK)V as a memory. Keys
  fire on recognizable prefix patterns, shallow in lower layers and semantic
  in upper ones. Values, projected to the vocabulary, favor the tokens that
  follow those patterns. The evidence is 160 keys of one 16-layer model,
  with value-key agreement of at most 3.5%, and outputs are mostly
  compositions. This reading is behind ROME, MEMIT and tools that list
  features by what they "hear" and "predict".
---

# THEORY-tmp03ct6: A transformer's feed-forward layers work as key-value memories: each hidden unit's input weights match input patterns, and its output weights promote the tokens that follow them

## Source

Geva et al. (2021), [LIT-tmp96ozs](../literature.d/LIT-tmp96ozs.md). Read as [NOTE-tmpah4r2](../notes.d/NOTE-tmpah4r2.md).

## The account

The FFN sublayer has the algebraic shape of a key-value memory without the
softmax. The account says it also behaves like one. Each hidden unit is a
slot, its activation measures how well the current prefix matches a
pattern, and its output row writes a vote for what comes next into the
residual stream. The stream accumulates and refines those votes.

## What it explains

- Why FFN units can be labeled by their triggering contexts and their
  vocabulary projections, the basis of FFN-feature browsers
- Why ROME and MEMIT can write facts into MLP weights as associative
  key-value pairs ([LIT-tmpvij69](../literature.d/LIT-tmpvij69.md), [LIT-tmpmnwn4](../literature.d/LIT-tmpmnwn4.md))

## Where it is weak

- **The value half is a tendency.** At most 3.5% top-token agreement
- **Composition dominates.** The layer's output is rarely one memory's
  vote, so a per-unit reading describes ingredients, not the layer
- **One small model**, with ReLU FFNs, where modern models use gated ones
