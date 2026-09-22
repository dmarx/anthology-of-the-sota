---
number: 262
status: Read
formerly:
- NOTE-tmpptsb7
paper: LIT-519
title: 'Eleven checkpoints agree on where the spectrum concentrates, and imitating it does not help'
version: 1
date: '2026-09-22'
summary: >-
  Read for breadth rather than depth of claim. Eleven GPT-2-style checkpoints
  differing in size, language, tokenizer and corpus share a depth profile in
  effective-rank entropy, which is the right instrument for a claim about
  where a matrix's magnitude sits. The paper's own headline — that you can
  initialize from that profile — is a negative result, reported as one.
---
<!-- inactive-ok-file: THEORY-059 — Proposed, named as the question this
     reading supplies the breadth leg of. -->

# NOTE-262: Eleven checkpoints agree on where the spectrum concentrates, and imitating it does not help

## Contribution

Two halves. A survey: measure Frobenius norm and effective-rank entropy across
layers and components of eleven pretrained GPT-2-style checkpoints, and see
what they share. Then an intervention: build initializers that imitate those
profiles and see whether pretraining improves.

## Key results

**The instrument.** Entropy effective rank, `erank(W) = exp(−Σᵢ pᵢ log pᵢ)`
with `pᵢ = σᵢ/Σⱼσⱼ`, counts how many singular directions carry substantial
mass. Frobenius norm gives total scale; erank gives its concentration. For a
claim about whether subtracting a few directions removes a lot of magnitude,
this is the quantity, not the rank.

**The shared profile.** Across the eleven checkpoints — English GPT-2 small
and medium, Russian small and large, and Vietnamese, Chinese, Portuguese,
Japanese, Turkish, poem and story models — effective-rank entropy drops in the
final few blocks. The drop is sharpest for `W_O` and `W_down`, the two
matrices that write into the residual stream, and weaker but present for
`W_QKV` and `W_up`.

**Norm and concentration move in opposite directions.** `W_O` and `W_down`
Frobenius norms rise almost linearly with depth while their effective spectra
narrow: more weight mass, carried by fewer directions, the deeper you go.

**The shape is structural, not a scale artifact.** The common trend is clear
in z-scored plots and not in raw metric values, which is the authors' own
argument that they are seeing shared structure rather than shared magnitude.

**The intervention fails, and is reported as failing.** Initializers matched
to pretrained component-wise magnitudes and singular-value shapes visibly
change the model's structural spectra and produce no corresponding performance
advantage. Reusing actual pretrained weights stays competitive. The conclusion
offered is that effective reuse needs more than component-wise scale and
singular-value shape.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Spectral concentration rises with depth, peaking in the last blocks | strong for this family | eleven checkpoints, consistent after normalization |
| C2 | Residual-writing matrices concentrate most | moderate | the plots; the authors call the component reading qualitative |
| C3 | Matching the spectral profile at init does not help | strong as a negative result | their own comparison, reported against their hypothesis |

## Limitations

**One architecture family.** GPT-2-style throughout, deliberately — the design
varies everything except the architecture. So it is breadth in data, language
and tokenizer, and none in architecture.

**`W_QKV` is analysed fused.** Query, key and value share one matrix here, and
the paper flags this as a limitation itself, noting that `W_V` belongs
functionally with `W_O` rather than with `W_Q` and `W_K`. That is exactly the
distinction the two neighbouring papers in this cluster disagree about, so
this measurement cannot arbitrate it.

**The component-level interpretation is qualitative.** The key-value memory
reading of the depth trends is offered as an interpretation of plots, which
the authors say in those words.

**Small models.** GPT-2 small through large; nothing at the scale where
compression decisions are usually made.

## Bearing on the record

**It is the breadth leg of the answer to [THEORY-059](../theory.d/THEORY-059.md)'s question.**
[LIT-517](../literature.d/LIT-517.md) goes deep on three models and
[LIT-516](../literature.d/LIT-516.md) on three more; this holds the architecture fixed
and varies everything else, which is what rules out "one tokenizer" or "one
corpus" as the source of the spectral shape.

**It agrees with the depth half of the non-uniformity finding and complicates
the component half.** [LIT-516](../literature.d/LIT-516.md) finds the first and last blocks
compression-friendly and the middle resistant; this finds entropy dropping at
the end, which is the same direction. But it finds `W_down` among the *most*
concentrated matrices, where the other paper classes MLP Down as
non-low-rank. The measurements are not the same quantity — entropy across all
directions against the presence of a heavy tail — and the record is not
treating that as a settled contradiction.

**The negative result earns its place.** A spectral profile that recurs across
eleven models and cannot be transplanted into a twelfth is evidence that the
profile is produced by training rather than a setting that produces good
training. [DP-005](../../docs/design-principles.md#dp-5) is the principle, and here the authors apply it to
themselves.

## Open questions

- **Does the depth profile hold at billions of parameters?** Every model here
  is GPT-2-sized, and the compression decisions that would use it are made at
  7B and up.
- **Split `W_QKV`.** The one measurement that would let this dataset speak to
  the Value question the cluster is stuck on, and it is a re-run rather than
  a new experiment.
