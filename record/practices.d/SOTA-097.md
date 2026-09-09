---
number: 97
status: 'Active'
title: 'Optimal batch size scales approximately with compute budget - `B ∝ C^(1/4)`'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Source corrected from LIT-068 (Chinchilla) to LIT-028 (Kaplan et al.).
    Chinchilla fits N and D against compute and makes no batch-size claim;
    the exponent is Kaplan's equation 1.7. The recommendation is unchanged,
    and the exponent now has its derivation in the body rather than a
    rounded 1/4 on its own.
tags:
- training-optimization
date: '2026-08-24'
published: '2020-01-01'
source:
# Kaplan et al. equation 1.7, not Chinchilla. Both are compute-allocation
# papers about the same era and the citation had drifted to the more famous
# one; only Kaplan derives a batch-size exponent.
- LIT-028
implementations:
- chinchilla
- llama2
summary: >-
  Kaplan et al. (2020), [LIT-028](../literature.d/LIT-028.md) — [ARXIV-2001.08361](https://arxiv.org/abs/2001.08361). Equation 1.7 gives B ∝ C^(α_C/α_B) = C^0.24, from α_C ≈ 0.050 and α_B ≈ 0.21.
---

# SOTA-097: Optimal batch size scales approximately with compute budget - `B ∝ C^(1/4)`

## Source

Kaplan et al. (2020), [LIT-028](../literature.d/LIT-028.md) — [ARXIV-2001.08361](https://arxiv.org/abs/2001.08361).

Filed against Chinchilla ([LIT-068](../literature.d/LIT-068.md)) until version 2. Chinchilla fits model size
and token count against compute and does not derive a batch-size exponent;
Kaplan does, and this is his.

## Where the exponent comes from

Kaplan's equation 1.7 gives the compute-optimal allocation as a set of power
laws sharing one numerator:

    N ∝ C^(α_C/α_N),  B ∝ C^(α_C/α_B),  S ∝ C^(α_C/α_S)

with α_C ≈ 0.050 and α_B ≈ 0.21, so the batch exponent is **0.24** — which is
what the title rounds to 1/4. Underneath it is the *critical* batch size, the
point past which extra parallelism stops buying speed (equation 1.4):

    B_crit(L) = B* / L^(1/α_B),   B* ≈ 2×10⁸ tokens,  α_B ≈ 0.21

The property that makes this usable is in Figure 10: **B_crit depends on the
loss, not directly on the model size**, and approximately doubles for every
13% decrease in loss. Two models of different sizes at the same loss want the
same batch size.

## Conditions

The exponent is small, which matters more than its exact value: a thousand-fold
increase in compute asks for roughly a five-fold increase in batch size. Most
of a growing budget goes to model size, not to batch.

`B_crit` is a speed-against-efficiency boundary rather than a quality one.
Training below it wastes wall-clock; above it wastes compute for the same loss.
Which side to err on is a scheduling decision, not a modelling one.

And the fit is Kaplan's regime: dense decoder-only transformers on WebText2,
2020 hardware, a fixed schedule. Kaplan's model-size exponent was later shown
wrong by Chinchilla ([SOTA-096](SOTA-096.md)) — the same paper, the same fitting method, a
different exponent that did not survive. That the batch exponent has not been
re-derived by anyone since is a reason to hold it loosely, not a reason to
trust it.

## Known implementations

- chinchilla
- llama2
