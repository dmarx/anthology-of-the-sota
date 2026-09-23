---
number: 312
status: Read
formerly:
- NOTE-tmpah4r2
paper: LIT-575
title: 'FFN layers as key-value memories'
version: 1
date: '2026-09-23'
summary: >-
  Keys fire on input patterns, and values project to next-token
  preferences. The reading is interpretable in upper layers of one small
  WikiText model, with weak key-value agreement and mostly compositional
  outputs.
---

# NOTE-312: FFN layers as key-value memories

## Contribution

A reading of the feed-forward sublayer that makes its hidden units
inspectable: what makes one fire, and what it pushes the output toward.

## Key insight

**An FFN is an unnormalized key-value memory.** The activation is how
strongly the input matches a key, and the output adds the matching values.
Projecting values through the output embedding makes them legible as token
preferences.

## Key results

- Patterns identified for most of 160 sampled keys. Shallow in layers 1–9,
  semantic in 10–16
- Value-key top-token agreement: near 0 in lower layers, rising to 3.5% in
  upper layers, against 0.0004% at random
- Layer outputs are mostly compositions, not any one memory's prediction

## Limitations

- **One 16-layer model on WikiText-103**, with 10 keys per layer, and
  patterns judged by human annotators
- **Weak agreement.** The value reading is a tendency, not a lookup
- **Before gated FFNs.** The paper's ReLU FFN has one input matrix, where
  SwiGLU models have gate and up projections
