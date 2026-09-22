---
number: 263
status: Read
formerly:
- NOTE-tmpsv1p1
paper: LIT-517
title: 'An MP bulk plus outliers at both ends, and why magnitude order is not importance order'
version: 1
date: '2026-09-22'
summary: >-
  Read to answer [THEORY-059](../theory.d/THEORY-059.md)'s open question. It answers it and complicates it:
  language-transformer weight spectra are steep at the top, as the account
  needs, but the bottom of the spectrum in non-square matrices holds
  directions whose removal is catastrophic. Frobenius magnitude and functional
  importance are ordered differently, and a method that peels the top and
  quantizes the rest is keeping exactly the part this paper says is fragile.
---
<!-- inactive-ok-file: THEORY-059 — Proposed, and this reading is about what
     its premise does and does not survive. The citations are the subject of
     the note, not a recommendation resting on it. -->

<!-- inactive-ok-file: SOTA-274 — Proposed, named once in a DP-009 counting
     paragraph as the same shape one floor over. Cited as a comparison, and
     the sentence citing it says two is not several. -->

# NOTE-263: An MP bulk plus outliers at both ends, and why magnitude order is not importance order

## Contribution

Use Random Matrix Theory as a null hypothesis for a trained weight matrix. At
initialization the singular values of `W` follow the Marchenko-Pastur law
exactly; whatever departs from it after training is where learning went. Then
ask what the departing directions do.

## Key results

**The spectrum's shape.** Trained matrices are an MP bulk plus outliers, on
BERT, Pythia-410M and Llama-3.1-8B. For a **square** matrix the MP support
starts at zero, so outliers can only appear above the bulk. For a
**rectangular** matrix the lower edge `ν₋ = σ̃(1 − √(1/q))` is strictly
positive, so singular values can fall *below* the bulk too — and they do.

**The bottom outliers are not noise.** Their right singular vectors overlap
the eigenvectors of the activation covariance matrix far above the 3σ band
expected from random vectors. Present in Up/Down/Gate projections of Pythia
and Llama; absent in the Attention-Output matrix of all three models.

**The ablation, which is the part that bites.** Zero one decile of the
rank-ordered singular values of one matrix type across all blocks, measure
the damage:

| Llama-3 8B, GSM8K 3-shot (43.2% baseline) | smallest decile | largest decile |
|---|---|---|
| Down-Projection (non-square) | **2.0%** | 0.0% |
| Gate-Projection (non-square) | 34.1% | 0.0% |
| Attention-Output (square) | 40.0% | 0.0% |
| Query (square) | 40.3% | 0.0% |

For square matrices, importance decreases monotonically from large to small.
For non-square matrices it does not: the smallest decile always outranks some
larger ones, and for the Down-Projection it is the *second* most damaging
decile in the matrix. On RULER at 8192 context, removing decile 1 from all
layers scores 0.0 on all five tasks — the same as removing decile 10.

**The reconciliation.** Two published results disagreed about whether small
singular values matter. Varying only the order of operations reproduces both:
prune-then-fine-tune recovers the loss (BoolQ fully, RTE and SST2 nearly),
fine-tune-then-prune does not (all three degrade significantly against a 3σ
band from six runs). So fine-tuning *writes into* the small directions.

**A mechanism, in a solvable model.** Write `W = W₀ + X`, a low-rank rule plus
noise. Under the usual white-noise assumption `Cov(X) = 1`, a singular value
of `W₀` can only surface as an outlier *above* the bulk — the BBP threshold.
Give the noise non-trivial covariance and outliers below the bulk become
possible, with the information in the outlier's singular vector related to its
distance from the bulk.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Trained transformer spectra are MP bulk plus outliers | strong | three model families, exact agreement at init |
| C2 | Non-square matrices carry informative small outliers | strong | 3σ overlap plus the ablation, agreeing |
| C3 | Magnitude order ≠ importance order | strong for non-square; the square case is the opposite | Table 1, Table 2, Figure 5 |
| C4 | Fine-tuning is what loads the small directions | moderate | one model (BERT), three datasets, order swapped |
| C5 | Non-trivial noise covariance explains small outliers | suggestive | a two-layer linear teacher-student model, not the real network |

## Limitations

**Zeroing a decile is not quantizing it.** The ablation removes directions
outright. Every compression method this bears on instead represents them at
lower precision, and the paper does not interpolate between the two.

**Three models, and the matrix-type findings are not identical across them.**
Llama's Down-Projection shows no increased overlap while Pythia's does; the
authors offer a speculation about the GLU placement and leave it there.

**The minimal model is linear and two-layer.** It shows small outliers *can*
arise from correlated noise; it does not show that is what produced them in
Llama.

## Bearing on the record

**It answers most of [THEORY-059](../theory.d/THEORY-059.md)'s open question.** That account was
`Proposed` because its spectral premise was plotted only on diffusion
transformers. Here it is plotted on three language models, and the premise
holds in the form the account needs: a few directions carry a large share of
the Frobenius magnitude, so a rank-32 subtraction removes a lot of it.

**It also names the account's other half without measuring it.** [THEORY-059](../theory.d/THEORY-059.md)
says a quantization error is flat because rounding is near-independent across
entries. That is precisely the i.i.d. hypothesis whose singular values are
Marchenko-Pastur. So the two cases in the theory are "MP plus outliers" and
"MP", which is a sharper statement than the theory currently makes — and the
spectrum of `W − Q(W)` is still not plotted anywhere.

**And it raises a question about [SOTA-314](../practices.d/SOTA-314.md) that the practice does not
contain.** SVDQuant peels the top 32 singular directions into 16 bits and
quantizes the residual. The residual is where the bottom outliers live. In
language transformers those are, for the MLP projections, the directions whose
loss costs 41 points of GSM8K. Whether 4-bit quantization damages them the way
zeroing does is unmeasured, and whether diffusion transformers have them at all
is unmeasured. Both are in the open questions below rather than in the
practice, because neither has been checked.

**Counted, not generalized.** This is the second document in this cluster
where a quantity's rank order and its functional importance come apart —
[SOTA-274](../practices.d/SOTA-274.md) already says to measure a block's stable rank rather than
assume it. Different mechanisms, and two is not several.
[DP-009](../../docs/design-principles.md#dp-9).

## Open questions

- **What does 4-bit quantization do to a bottom outlier?** The ablation zeroes;
  every method that matters quantizes. One curve — damage against bits — on a
  Down-Projection would settle whether this is a warning or a curiosity.
- **Do diffusion transformers have bottom outliers?** The same overlap plot on
  the model [LIT-512](../literature.d/LIT-512.md) quantizes. If they do, the residual SVDQuant hands
  its quantizer is not the benign part.
- **Why does the Attention-Output matrix never overlap the activation
  covariance?** Systematic across BERT, Pythia and Llama, and unexplained.
