---
status: Active
title: 'Ghost in the Transformer: Detecting Model Reuse with Invariant Spectral Signatures'
version: 1
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-22'
published: '2025-11-09'
arxiv: '2511.06390'
first_author: 'Wang'
keywords:
- 'model provenance'
- 'fingerprinting'
- 'singular value spectra'
- 'intellectual property'
- 'model lineage'
implementations:
- GhostSpec
summary: >-
  Wang, Ma, Xinyi and Li (2025), [ARXIV-2511.06390](https://arxiv.org/abs/2511.06390) — take the
  singular spectra of `W_q W_k^T` and `W_v W_o` per layer. Those products are
  invariant to the permutation and scaling transforms that hide derivation
  while preserving function, so the spectra fingerprint the model. **F1
  0.9867** over 55 model pairs, data-free, against 0.9610 for the best prior
  method. Read as [NOTE-tmp42huo](../notes.d/NOTE-tmp42huo.md).
---
<!-- inactive-ok-file: THEORY-061 THEORY-062 — both Proposed,
     filed earlier in this same contribution. Named to record that the same
     matrix product appears in two literatures with no citation between them,
     which is an observation about the coincidence rather than a claim
     resting on either account. -->

# LIT-tmp81ryb: Ghost in the Transformer: Detecting Model Reuse with Invariant Spectral Signatures

Wang, Ma, Xinyi and Li (2025) —
[ARXIV-2511.06390](https://arxiv.org/abs/2511.06390), AAAI 2026. Read as
[NOTE-tmp42huo](../notes.d/NOTE-tmp42huo.md).

## Key takeaways

- **The invariant is the whole idea.** Comparing `W_q`, `W_k`, `W_v`, `W_o`
  directly is defeated by permutation and scaling, which change the weights
  and not the function. The products `M_qk = W_q W_k^T` and `M_vo = W_v W_o`
  are not, so their singular spectra survive the obfuscation.
- **Data-free and non-invasive.** No training data, no queries, no
  modification of the model. It reads weights.
- **Two metrics.** GhostSpec-mse compares truncated spectra directly;
  GhostSpec-corr compares the *trend* of the top-K normalized singular values
  across layers, aligned by dynamic sequence alignment and scored by distance
  correlation.
- **55 model pairs**, Llama-2-7b and Mistral-7B as base models, covering
  fine-tuning, pruning, merging, expansion and adversarial transforms. F1:
  GhostSpec-mse **0.9867**, GhostSpec-corr 0.9730, REEF 0.9610, Logits 0.9268,
  QueRE 0.9157, PCS 0.9014.

## Standing in the anthology

**It opens a subject the record does not hold at all.** Grepping the practices
for watermarking, fingerprinting or provenance returns nothing. The corpus has
three hundred recommendations about building and serving models and none about
establishing where a model came from — which is a question that has already
had public instances, and one the `deployment-and-society` topic exists for.

**It is the same invariant the stability cluster is about, used for a
different purpose.** `W_q W_k^T` is the matrix whose spectral energy
[THEORY-062](../theory.d/THEORY-062.md) says predicts a crash and whose spectral norm
[THEORY-061](../theory.d/THEORY-061.md) bounds attention entropy by. Here its spectrum
is a serial number. Nobody in either literature cites the other, and the
coincidence is worth noticing: the quantity that governs whether training
survives is also the quantity that identifies the model afterwards.

**Its limits are about adversaries, not accuracy.** The evaluation covers
transformations someone might apply innocently or to hide provenance, and the
method is offered as evidence rather than proof. A determined adversary who
knows the fingerprint is a different threat model and the paper does not claim
to cover it.
