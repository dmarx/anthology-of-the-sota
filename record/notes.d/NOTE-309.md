---
number: 309
status: Read
formerly:
- NOTE-tmptkt9y
paper: LIT-568
title: 'Are Sparse Autoencoders Useful? A Case Study in Sparse Probing'
version: 1
date: '2026-09-23'
summary: >-
  On 113 datasets and five regimes, probes on SAE latents do not beat, or
  usefully add to, probes on raw activations once method selection is
  honest. Earlier wins, including the authors' own, came from weaker
  baselines. Main text read, appendices skimmed.
---

# NOTE-309: Are Sparse Autoencoders Useful? A Case Study in Sparse Probing

## Contribution

A downstream test of SAEs with a fair comparison: a practitioner's
toolkit with and without SAE probes, with the choice made on validation
data. This is where interpretable latents were most expected to help.

## Key insight

**An interpretability method's benefit is only as real as the baseline it
beat.** Every positive result for SAE probes the authors found, their own
included, shrank or vanished when the baseline got the same affordance
(pooling across tokens, method selection).

## Key results

- Standard conditions, Gemma-2-9B layer 20: SAE probes chosen for 14 of
  113 tasks. Mean change from adding them, −0.003 ± 0.002 AUC (Figure 4)
- Data scarcity (2–1024 examples), class imbalance (5–95% positive), label
  noise (0–50%): no average gain at any setting (Figure 6)
- Covariate shift: SAE probes generalize worse
- Multi-token: 19.6% win rate against a last-token baseline, 8.7% against
  an attention-pooled one (Figure 11)
- Eight SAE architectures (ReLU through Matryoshka, Gemma-2-2B): a slight
  upward trend, smaller than the spread (Figure 12)
- Replicated on Llama-3.1-8B with Llama Scope TopK SAEs

## Limitations

- **Probing is one proxy**, as the authors say. SAEs may help elsewhere:
  circuit discovery, steering, unlearning
- **Binary classification with linear heads.** A task where the concept is
  not linearly available in raw activations might differ
- **Public SAEs only** (Gemma Scope, Llama Scope)
