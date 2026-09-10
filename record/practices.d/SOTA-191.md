---
number: 191
status: Proposed
formerly:
- SOTA-tmpqpw9i
promote_when: >-
  A decoder-only language model at contemporary scale trained with the
  normalization gain removed, reporting quality against the same model with
  it. The source's evidence is on 2019-era sequence models, and the axis
  that matters is whether the finding survives the architecture and scale
  the record's other practices assume.
consensus: contested
consensus_note: >-
  One group, and the field went the other way: every model in this record
  keeps a learnable gain, and RMSNorm — the near-universal choice (SOTA-182)
  — keeps the gain while dropping the centering, which is the opposite
  half from the one this paper says is expendable. LIT-088 adds a second
  data point at 22B on the same side, and a qualification: ViT-22B drops
  the QKV and LayerNorm biases for 3% accelerator utilisation with no
  quality loss, and deliberately KEEPS the MLP dense-layer biases.
title: "Consider removing LayerNorm's learnable gain and bias rather than tuning them"
version: 2
history:
- version: 2
  date: '2026-09-10'
  note: >-
    Enriched from the #123 readings. The recommendation is unchanged;
    the source list, the numbers or the neighbourhood are.
tags:
- model-stability
date: '2026-09-09'
published: '2019-11-01'
source:
- LIT-025
# RMSNorm keeps the gain and drops the centering — the opposite half from
# the one this paper calls expendable, and the reason `contested`.
contested_by:
- LIT-023
compared_against:
- SOTA-182
summary: >-
  Xu et al. (2019), [LIT-025](../literature.d/LIT-025.md) — the bias and gain increase overfitting risk and "do not work in most cases"; LayerNorm-simple, with both removed, beats LayerNorm on four datasets and reaches state of the art on En-Vi.
---

# SOTA-191: Consider removing LayerNorm's learnable gain and bias rather than tuning them

## Source

Xu et al. (2019), [LIT-025](../literature.d/LIT-025.md) — [ARXIV-1911.07013](https://arxiv.org/abs/1911.07013).

## The finding

The paper sets out to explain why LayerNorm works and arrives somewhere its
authors did not expect. The received account is forward normalization —
controlling the distribution of a layer's inputs. Their analysis says the
benefit is in the **backward** pass instead: the derivatives of the mean and
variance re-center and re-scale the gradients, and that is what buys the
smoother training.

The consequence for the learnable parameters is the part that becomes a
practice. If the forward normalization is not doing the work, the bias and
gain that adjust it are not either — and worse, they **increase the risk of
over-fitting**. `LayerNorm-simple`, with both removed, outperforms LayerNorm
on four of the datasets tried and reaches state of the art on En-Vi machine
translation. The paper's own proposal, AdaNorm, replaces them with an
input-dependent transformation and beats LayerNorm on seven of eight.

## Why this is Proposed, and why it is filed at all

The field went the other way. Every model in this record keeps a learnable
gain, and RMSNorm ([SOTA-182](SOTA-182.md)) — now effectively universal — keeps the gain
while dropping the *centering*, which is the opposite half from the one this
paper calls expendable. Two papers, one conclusion each, pointing in
different directions about which part of LayerNorm is load-bearing.

The evidence here is 2019-era sequence models and machine translation, not
decoder-only language models at scale, and no adopter in the record has
tested the removal. That is enough to file it and not enough to recommend it.

<!-- inactive-ok-block: SOTA-027 — Rejected in the same change; this paragraph is about the three practices that cited this paper -->
It is filed rather than dropped for a specific reason. Three practices —
[SOTA-025](SOTA-025.md), [SOTA-026](SOTA-026.md) and [SOTA-027](SOTA-027.md) — cited this paper for a decade of the
record's life while recommending how to *set* the two parameters it argues
should be deleted. Leaving the note with no practice would leave the record
with no statement of what it actually says, which is how that inversion
survived being read.

## A second data point at scale, on the other side

[LIT-088](../literature.d/LIT-088.md) (ViT-22B) applies its LayerNorms "without bias and centering",
citing RMSNorm — so it **keeps the gain and drops the centering**, the opposite
half from the one this practice calls expendable. That is one more model at 22B
taking [SOTA-182](SOTA-182.md)'s side rather than this one, and it does not meet the
`promote_when` above, which asks for a decoder-only language model with the
*gain* removed.

It does carry a qualification worth having. ViT-22B drops the biases from the
QKV projections and the LayerNorms for a measured **3% accelerator utilisation**
gain with no quality loss — and **keeps the biases on the MLP dense layers**,
explicitly departing from PaLM, having "observed improved quality and no speed
reduction".

So bias removal is not uniform even inside one model, and two groups disagree
about the MLP biases with neither showing the experiment. Whatever settles this
practice will need to be more specific than "remove the learnable parameters".

## Known implementations

- None in this record. The paper's own LayerNorm-simple and AdaNorm are the only reported uses.
