---
number: 270
status: Read
formerly:
- NOTE-tmpruk19
paper: LIT-526
title: 'Concepts live in the quiet directions, and the paper labels its own claims robust or partial'
version: 1
date: '2026-09-22'
summary: >-
  Read last of the batch and the easiest call to make, for a reason that has
  little to do with the finding: it arrives with a table grading its own six
  claims, a robust null against the hypothesis it set out to confirm, and
  partial results labelled partial. The finding itself is that contextual
  concept directions sit at the bottom of the unembedding spectrum and static
  vocabulary contrasts sit at the top.
---
<!-- inactive-ok-file: THEORY-034 — Proposed, named in a paragraph saying
     the two answer different questions and the record has not joined them. -->

# NOTE-270: Concepts live in the quiet directions, and the paper labels its own claims robust or partial

## Contribution

Ask where in the spectrum of the unembedding second moment a concept
direction lives. The answer is the low-variance tail for contextual
directions and the high-variance head for static vocabulary contrasts, which
the paper calls a dual geometry.

## Key results

**The measurement.** Form the regularized uncentered second moment of the
unembedding rows, `Σ_L = (1/|L|)Σ_w γ(w)γ(w)ᵀ + τI`. Project a candidate
concept direction onto its eigenbasis and ask where the mass sits. **Spectral
Center of Mass** is the fraction of eigendirections at which half the mass has
accumulated; SCM near 1 means the direction is encoded in low-eigenvalue
directions. Partitioned tests use `k = ⌊0.1d⌋` with robustness checked at 5%,
10% and 20%.

**Anti-concentration, three ways.** Residual-stream difference-of-means
vectors across 22 semantic categories: 17 of 17 models negative against the
uniform baseline (model-level `p = 3.8×10⁻⁹`), 13 of 17 against a
norm-matched random-direction null. Sparse-autoencoder features replicate
(`p = 4.5×10⁻¹⁹` across concepts within a model), and so do linear probes on
Llama and Qwen.

**The dual geometry.** Static unembedding-row contrasts *concentrate* in high
variance (`p < 10⁻⁴`, 4 models) while activation-space concept directions
anti-concentrate. The paper's reading is that transformers rotate semantic
content into spectrally quiet regions during contextualized processing.

**Independence from the background spectrum.** Correlation between random-
direction SCM and concept SCM is `r = 0.019` (`p = 0.94`), so the effect is
not a property of the ambient spectrum. The paper marks this *suggestive* at
`n = 17`.

**The null.** The investigation began by testing whether a published causal
inner product helps transport concepts across languages. Matched-spectrum
randomization across 17 models and four language pairs: `p = 0.95`. No
benefit over spectral regularization alone. Marked *robust (null)*.

**Two results marked partial, in the paper's own table.** The steering
interference asymmetry holds in 4 of 5 models — 7 of 13 configurations, sweep
`p` uncorrected, one model undetermined, and the magnitude depends on steering
strength. Syntax in the high-variance subspace holds in 6 of 8 models on
English, with Qwen 2.5 reversing, as do both models tested on Chinese.

## Claims

| id | claim | the paper's own grade |
|---|---|---|
| C1 | Activation-space concept directions anti-concentrate | robust (13/17 vs matched null) |
| C2 | Independent of the background spectrum | suggestive (n=17) |
| C3 | Dual geometry: vocabulary contrasts concentrate | robust |
| C4 | Whitened Causal Alignment adds no benefit | robust (null) |
| C5 | Steering interference asymmetry | partial |
| C6 | Syntax preferentially in the high-variance subspace | partial |

This record has nothing to add to that grading, which is the unusual part.

## Limitations

**Correlational throughout.** Where a direction sits and what it does are
different questions; C5 is the only intervention and it is the weakest result.

**The uncentered second moment is a choice**, defended in an appendix showing
centering leaves the effect intact or slightly stronger. Worth knowing the
choice exists.

**The partial results are genuinely partial**, and the paper's framing is
careful enough that a reader skimming the abstract gets the hedges. Qwen 2.5
reversing on C6 and both Chinese models reversing is not a detail — it means
the syntax claim may be about English.

**17 models is breadth in checkpoints, not in architecture families.**

## Bearing on the record

**It stands beside [THEORY-034](../theory.d/THEORY-034.md) without subsuming or being subsumed.**
That account says concepts sit in embedding space as intersections of
half-spaces — a claim about the shape of a concept region. This says where in
the covariance spectrum the direction lies, and that the answer inverts
between static and contextual representations. Different questions about the
same object, no citation in either direction.

**It is the third instance of a shape and the count stops there.** The
smallest singular directions of a weight matrix carry disproportionate
information ([NOTE-263](NOTE-263.md)); the residual a low-rank branch
hands its quantizer is not the negligible part ([SOTA-314](../practices.d/SOTA-314.md)); and
now the quiet end of the unembedding covariance is where concepts live. Three
different matrices, three unrelated literatures, and no mechanism this record
could write down that would connect them. Counted, not generalized.
[DP-009](../../docs/design-principles.md#dp-9).

**The reporting is a reason to file it and worth saying plainly.** A paper
that starts from a hypothesis, fails to confirm it, reports the null as a
headline result, grades its own six claims and marks two partial is doing what
[DP-010](../../docs/design-principles.md#dp-10) asks of everybody. The record has spent this week finding
abstracts that outran their appendices; this is the other case.

## Open questions

- **Does anti-concentration have a consequence?** The steering result is the
  only attempt and it is partial. If concepts really are in the quiet
  directions, an intervention that exploits it should beat one that does not.
- **Is C6 about English?** Qwen 2.5 reverses and both Chinese models reverse.
  The syntax claim is either language-dependent or tokenizer-dependent, and
  distinguishing those is one more experiment.
- **Why would contextual and static geometry invert?** The paper observes the
  duality and offers a reading; nothing tests it.
