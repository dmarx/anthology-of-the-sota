---
status: Proposed
promote_when: >-
  The false-positive case measured: two models trained independently on
  similar public corpora with similar recipes and no derivation between them,
  scored by this fingerprint, with the separation reported against the
  derived-model scores. A provenance claim is only as good as its false
  positives, and every result held here is about correctly detecting
  derivation. What would NOT meet it: more derivative-model pairs, or another
  fingerprinting method beaten on the same benchmark.
consensus: unassessed
consensus_note: >-
  One group, one benchmark, and no field position to report because the
  record holds no other document on model provenance. The subject is new
  here, not contested.
title: 'Verify a model''s lineage from the singular spectra of its attention products, which survive permutation and rescaling'
version: 1
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-22'
source:
- LIT-tmp81ryb
introduced_by:
- LIT-tmp81ryb
implementations:
- GhostSpec
summary: >-
  Wang et al. (2025), [LIT-tmp81ryb](../literature.d/LIT-tmp81ryb.md) — compare the per-layer
  singular spectra of `W_q W_k^T` and `W_v W_o`. Those products absorb the
  permutation and rescaling that change weights without changing the
  function, so the spectra identify a model through fine-tuning, pruning,
  merging and expansion. F1 **0.9867** over 55 model pairs, using no data and
  no queries.
---
<!-- inactive-ok-file: SOTA-319 — Proposed, named in a condition
     flagging an unexamined interaction. The condition depends on it being
     untested. -->

# SOTA-tmp3ot5z: Verify a model's lineage from the singular spectra of its attention products, which survive permutation and rescaling

## Source

Wang, Ma, Xinyi and Li (2025), [LIT-tmp81ryb](../literature.d/LIT-tmp81ryb.md) — read as
[NOTE-tmp42huo](../notes.d/NOTE-tmp42huo.md). AAAI 2026.

## When this applies

You have weights for two models and want evidence about whether one derives
from the other — a licence question, a release you are asked to vouch for, or
an audit. It needs weight access to both, so it does not apply to an API-only
model.

## Do this

**Compare the products, not the matrices.** For each layer `i`:

    M_qk = W_q⁽ⁱ⁾ (W_k⁽ⁱ⁾)ᵀ        M_vo = W_v⁽ⁱ⁾ W_o⁽ⁱ⁾

Take the singular spectrum of each. The fingerprint is those spectra across
all layers.

**The reason this and not the raw weights** is the whole method. A model can
be permuted or rescaled so that `W_q`, `W_k`, `W_v` and `W_o` all look
different and the function is unchanged. Those transforms cancel inside the
products, so the products' spectra do not move.

**Two ways to score a pair.** Compare truncated spectra directly, truncating
at each spectrum's effective rank; or reduce each layer to the mean of its
top-K normalized singular values, align the resulting per-layer sequences when
depths differ, and score by distance correlation. The second is cheaper and
handles a derived model whose depth has changed.

**It needs no data.** No training set, no queries, no modification of either
model.

## What it buys

Over 55 model pairs built from Llama-2-7b and Mistral-7B, spanning
fine-tuning, 50%- and 70%-unstructured pruning, merging, expansion, and
scaled and permuted adversarial transforms:

| method | F1 |
|---|---|
| **this, direct spectra** | **0.9867** |
| this, trend correlation | 0.9730 |
| REEF | 0.9610 |
| logit-based | 0.9268 |
| QueRE | 0.9157 |
| PCS | 0.9014 |

## Why `Proposed`

**Nothing here measures false positives against convergent similarity.** Every
result is about correctly recognizing a model that *is* derived. The case that
decides whether this can support a claim about a person or an organization is
two models that are similar because they were trained the same way and are not
derived, and it is not in the paper.

**The benchmark and the baselines are the authors' own**, which is ordinary
for a young subproblem and means the ranking is not independent.

**Two base models**, both 7B, both from the Llama-adjacent family.

**The thresholds are fitted where they are evaluated.** Both scores use an
empirical discrimination threshold tuned on this benchmark, so the reported F1
carries that advantage.

## Conditions

**It is evidence, not proof, and the distinction matters more here than
usual.** The transforms considered are permutation and rescaling — what
someone might do casually or to obscure provenance without thinking hard. An
adversary who has read this paper and specifically wants to break the
fingerprint is a different threat model and is not addressed. Anything said
publicly on the strength of this should say which of the two it rests on.

**Weights for both models are required.** This cannot answer a question about
a model served only through an API, which is where many of the disputes are.

**It reads only attention projections.** A derivation that replaced the
attention blocks and kept everything else is outside what it measures.

**Unknown interaction with spectral training methods.** A model trained under
[SOTA-319](SOTA-319.md) or a spectrum-preserving optimizer has a spectrum
shaped by the optimizer rather than by its data and history. Whether that
makes two unrelated models look related is unexamined, and it is the same
matrix product in both literatures.

## Known implementations

- `GhostSpec`, released by the authors.
