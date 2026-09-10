---
number: 56
status: Read
formerly:
- NOTE-tmpoe21j
paper: LIT-032
title: 'PowerNorm: Rethinking Batch Normalization in Transformers'
version: 1
tags:
- model-stability
date: '2026-09-09'
summary: >-
  Diagnoses why batch normalization underperforms layer normalization in NLP — the batch mean and variance fluctuate far more than in vision — and fixes it by dropping the zero-mean step and normalizing by a running quadratic mean instead of a batch variance. Beats LN by 0.4/0.6 BLEU and 5.6/3.0 perplexity with no hyperparameter changes.
---

# NOTE-056: PowerNorm: Rethinking Batch Normalization in Transformers

## Contribution

Two halves, and the diagnosis is worth more than the method. **Why does BN
fail in NLP?** Everyone knew it did; the paper instruments training and finds
the answer is *statistical instability of the batch statistics themselves* —
the per-batch mean and variance in a transformer swing far more, run to run,
than in a ConvNet, so the running estimates used at inference are a poor match
for what training saw.

From that: **Power Normalization**, which makes two changes to BN.

1. **Relax zero-mean.** Do not subtract the batch mean at all.
2. **Normalize by the quadratic mean `ψ` (root mean square), not the
   variance** — and use **running statistics** for it rather than per-batch
   ones.

## Key insight

The zero-mean step is the expensive one. The paper's measurements show the
batch *mean* has the large variation, and that the gradient contribution
routed through `σ_B` carries many more outliers than the one through `ψ_B`.
So BN's two operations are not equally to blame: centring is what breaks in
NLP, and scaling is salvageable if you scale by something better behaved.

That reframes normalization from "which axis do you normalize over"
(LN vs BN, the usual question) to **"which statistic is stable enough to
normalize by"** — a different and more portable question. It is also the same
observation `LIT-025` makes from the other side when it argues LayerNorm's
gain and bias can be dropped.

## Assumptions

- **Running statistics are usable if the statistic is stable.** The whole
  method is that `ψ` is stable enough for running estimates where `σ` is not.
- The instability is a property of NLP data and transformer activations rather
  than of any particular task — supported across translation and language
  modelling, not proved.
- Transformer encoder/decoder architectures at 2020 scale.

## Key results

- **vs LayerNorm:** +0.4 BLEU on IWSLT14, +0.6 on WMT14; −5.6 PPL on PTB,
  −3.0 on WikiText-103. **With no change of hyperparameters**, which the
  authors emphasise and which matters — a normalization swap that needs a
  re-sweep is not a drop-in.
- **vs BatchNorm:** +1.5/+2.0 BLEU and −7.7/−3.4 PPL, i.e. most of the gap
  BN had to close was closed by the running-`ψ` change.
- **The diagnostic measurements** are the paper's backbone: batch statistics
  vs running statistics distance during the forward pass, and gradient-norm
  outliers through `σ²` vs `ψ²` during the backward pass. `ψ_B` is visibly
  better behaved on both.
- A singular-value analysis comparing PN and LN representations.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | BN fails in NLP because batch statistics fluctuate, not for an architectural reason | strong | directly measured, forward and backward |
| C2 | The zero-mean step is the problematic half | strong | the mean is where the variation is |
| C3 | A running quadratic mean is stable enough to normalize by | strong | the method works, and the stability is measured |
| C4 | PN beats LN across translation and language modelling | moderate | four datasets, consistent direction, modest margins |
| C5 | The gain needs no re-tuning | moderate | asserted and demonstrated on these setups |

## Method

Replace LayerNorm with: no mean subtraction; divide by a **running** estimate
of `ψ = √(E[x²])`; keep the learnable affine. Everything else — optimizer,
schedule, hyperparameters — unchanged.

## Concepts

- **Statistical stability as the normalization criterion** — the reframing,
  and the transferable part.
- **Quadratic mean vs variance** — normalizing by RMS rather than by a
  centred second moment. RMSNorm makes the same move on the layer axis; this
  paper makes it on the batch axis and gives the measurement for why.

## Connections

Directly parallel to RMSNorm (`LIT-023`), which also drops centring and
normalizes by a root-mean-square — but along the feature axis, and argued as a
hypothesis rather than measured. **PowerNorm supplies the measurement RMSNorm
states as a suspicion**, which is a genuinely useful pairing the record did not
previously connect. Also related to `LIT-025` on removing LayerNorm's learned
parameters: three papers converging on "LayerNorm does more than it needs to".

## Recommendations

- **R1** — Before choosing a normalization axis, ask which statistic along it
  is stable. *Topic:* model stability. *Strength:* moderate.
- **R2** — Centring is the fragile half of a normalizer; scaling by RMS is the
  robust one. *Strength:* moderate — this paper and RMSNorm agree, from
  different directions.
- **R3** — Report whether a swap needed re-tuning. *Topic:* analysis and
  evaluation. *Strength:* strong.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**
PowerNorm itself did not displace LayerNorm or RMSNorm, and a 0.4-BLEU
improvement at 2020 scale is not a reason to revisit that.

The value of the reading is the connection: this is the measurement behind a
claim `LIT-023` makes as a hypothesis and `LIT-025` acts on. Recorded in
Connections so the next person reading about normalization finds all three.

The document's takeaways were vague and one was wrong in emphasis — **"better
numerical stability"** describes the wrong thing. PowerNorm is not about
numerics; it is about the *statistical* variability of batch estimates, which
is a different failure and the one the paper measures.

## Limitations

- Modest margins over LN, on 2020-scale translation and language modelling.
- No decoder-only LLM evidence, which is where every normalization decision in
  this record now gets made.
- C1 is established for these models and datasets; "NLP" is doing some work.
- Dropping centring means the representation's mean is unconstrained, and the
  consequences are not explored.

## Open questions

- Does the diagnosis survive at scale? If batch-statistic instability is what
  kills BN, very large batches should mitigate it — and nobody has checked.
- PowerNorm and RMSNorm make the same move on different axes. Is there a
  statement covering both, and is centring ever worth its cost?
