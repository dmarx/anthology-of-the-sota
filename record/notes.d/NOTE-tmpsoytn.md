---
status: Read
paper: LIT-tmpebkg3
title: 'Tuned Lens'
version: 1
date: '2026-09-23'
summary: >-
  The logit lens decodes intermediate layers with the final unembedding, and
  fails or misleads on many models. A per-layer affine translator,
  distilled toward the final logits, fixes this across every family
  tested. Sections 1–5 read, appendices skimmed.
---

# NOTE-tmpsoytn: Tuned Lens

## Contribution

A cheap, general way to read a pretrained transformer's intermediate
predictions that does not depend on the model happening to keep its
intermediate layers in the unembedding's basis.

## Key insight

**The logit lens fails for two nameable reasons, and each has a fix.**
Later layers add residuals that are far from zero on average, which a
learned bias corrects. And the hidden-state covariance drifts with depth,
with outlier dimensions that appear partway, which a learned change of
basis corrects. Distilling toward the model's own final distribution, not
toward labels, keeps the probe from knowing more than the model.

## Key results

- Logit lens bias on GPT-Neo-2.7B: 4–5 bits KL at most layers (Figure 3).
  The tuned lens's is far lower
- Lower perplexity than the logit lens at every layer, Pythia 70M–12B and
  NeoX-20B, with lower spread across models (Figure 5). Same on BLOOM, with
  or without the last block (Figure 4)
- Causal basis extraction, Pythia-410M layer 18: influence on the lens and
  on the model correlate at Spearman 0.89. No direction matters to the lens
  and not to the model (Figure 8)
- Prompt-injection detection, Pythia-12B (Table 1): AUROC 1.00 on five of
  nine tasks. The SRM baseline also scores 1.00 on those five and is better
  on MC-TACO and SciQ. The lens wins only on ARC-Challenge (0.81 against
  0.57)
- Secret-word elicitation (§5.1): mixed against the logit lens, and the
  best layer cannot be chosen without the answer

## Limitations

- **The lenses in the paper are undertrained, by its own later account.**
  Version 6 reports that Muon reaches much lower KL than the SGD used for
  every experiment, and that the experiments were not re-run
- **Pre-LN transformers.** Both lenses assume the iterative residual form
- **A lens needs training per model**, though it transfers to fine-tunes
  (at most 0.3 bits per byte, LLaMA-13B to Vicuna-13B) and to nearby layers
- **The applications do not beat strong baselines.** The case for the
  tuned lens is as a better *reading* tool than the logit lens, not as a
  detector
