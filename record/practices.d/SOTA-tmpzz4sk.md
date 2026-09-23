---
status: Active
title: 'Probe language-model activations with logistic regression on the raw activations, and credit sparse-autoencoder probes only against that baseline under validation-based selection'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-tmp57c8v
introduced_by:
- LIT-tmp57c8v
consensus: unreplicated
consensus_note: >-
  One group's paper, but a large comparison across 113
  datasets, two model families, and the conditions where SAEs were expected
  to help. It overturns earlier positive results, including its authors'
  own. The case against SAE probes has not been independently re-run.
implementations: []
summary: >-
  Kantamneni et al. (2025), [LIT-tmp57c8v](../literature.d/LIT-tmp57c8v.md) — across 113 datasets, adding
  SAE-latent probes to a toolkit of raw-activation probes, choosing per task
  by validation AUC, changes test AUC by −0.003. It does not help under data
  scarcity, class imbalance, label noise or shift. Reported SAE wins came
  from baselines denied the same pooling or selection. Use logistic
  regression on activations, and hold any SAE method to it.
---

# SOTA-tmpzz4sk: Probe language-model activations with logistic regression on the raw activations, and credit sparse-autoencoder probes only against that baseline under validation-based selection

## Source

Kantamneni et al. (2025), [LIT-tmp57c8v](../literature.d/LIT-tmp57c8v.md). Read as [NOTE-tmptkt9y](../notes.d/NOTE-tmptkt9y.md).

## The practice

- **Default to logistic regression on the residual stream**, at the layer
  where it probes best (layer 20 of Gemma-2-9B's 42, in the paper). It is
  the paper's reference baseline, and SAE latents added nothing to a
  toolkit built around it
- **Do not switch to SAE probes for the hard cases.** Few examples,
  imbalanced classes and noisy labels were where the interpretable basis
  was expected to help, and it did not
- **When claiming an SAE-based result, give the baseline the same
  affordances.** Pool raw activations across tokens (attention pooling) if
  the SAE probe pools, and choose among methods on validation data, never
  on test. Both of this paper's apparent SAE wins disappeared under those
  rules

## Conditions

- **Binary probing with linear heads, on Gemma-2 and Llama-3.1.** It does
  not rule out SAEs for circuit analysis, steering or unlearning
- **Public SAEs.** A better SAE could change the result, though eight
  architectures over two years moved it less than the spread
