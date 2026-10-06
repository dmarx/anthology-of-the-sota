---
number: 126
status: Proposed
formerly:
- THEORY-tmp1obd6
promote_when: >-
  A scaling comparison in which expressivity is the only thing varied: the
  same architecture with and without an extension known to change what it
  can express, such as negative eigenvalues in Gated DeltaNet, fitted over
  enough scales to give the data coefficient B a confidence interval. The
  account predicts that B separates and the exponents do not. Olmo Hybrid
  ran this ablation, without fitting B, and found the two scale about the
  same. That is the result to beat. A hybrid-versus-transformer gap in B
  would not count, because hybrids differ from transformers in much more
  than expressivity.
title: 'A more expressive architecture scales better by lowering the data coefficient rather than the exponent, because it can learn more of the discrete tasks in language-model data from the same tokens'
version: 1
tags:
- training-optimization
- analysis-and-evaluation
- model-architecture
date: '2026-10-06'
source:
- LIT-799
explains:
- SOTA-132
summary: >-
  Merrill et al. (2026), [LIT-799](../literature.d/LIT-799.md), §4.2 and App. E. The quantization model
  of scaling laws treats language modelling as many discrete tasks with
  power-law frequencies. If a fraction ε of tasks is inexpressible, and those
  tasks need more tokens or parameters or give less loss reduction,
  lowering ε shifts the loss curve down without changing the exponent. The
  hybrid's fitted data coefficient B is lower than the transformer's (83.7
  against 94.9, non-overlapping CIs), and the exponents overlap. But the
  instantiation that fits was chosen after the fits, and the same paper finds
  that removing negative eigenvalues barely changes the scaling.
---

# THEORY-126: A more expressive architecture scales better by lowering the data coefficient rather than the exponent, because it can learn more of the discrete tasks in language-model data from the same tokens

## Source

Merrill, Li, Romero, Svete, Costello et al. (2026), [LIT-799](../literature.d/LIT-799.md) — Olmo
Hybrid, §4.1–4.3, Theorem 4, Corollaries 4.1–4.2, App. E, Tables 5 and 18.

## The account

**Start from the quantization model.** Language modelling is a large number
of discrete tasks. Each is learned or not, each token uses one task, and the
probability of task k falls as k^−(α+1). A task becomes learnable after T
relevant tokens and costs C parameters. Loss then falls as a power law in
parameters or tokens, because tasks are acquired one by one in order of
frequency.

**Add expressivity.** Each task is expressible by a given architecture with
probability 1 − ε, independently of its frequency. An inexpressible task
can still be approximated, a lookup table rather than a compact circuit. It
needs C′ ≥ C parameters and T′ ≥ T tokens, and it gives a loss reduction
Δ′ ≤ Δ. Theorem 4 says loss still follows power laws in N and D with the
same exponents. Expressivity enters only the coefficients A_ε and B_ε and
the irreducible loss L^ε_∞. Lowering ε lowers the curve everywhere
(Corollary 4.1). It lowers the irreducible loss only if Δ′ < Δ
(Corollary 4.2).

**Matching it to the fits.** The fixed-exponent fits show a lower B for the
hybrid and no clear difference in A or E. The authors therefore pick the
instantiation in which inexpressible tasks need more tokens (T′ > T) but
the same parameters and the same final loss reduction. In that model,
expressivity makes each token worth more and does nothing else.

## What was measured

- **The coefficient** (Tables 18–20). Olmo Hybrid ([LIT-799](../literature.d/LIT-799.md)) fitted
  transformer, pure GDN and 3:1 hybrid ladders. Exponents fixed at α = β = 0.22, fit
  from 60M to 1B on identical data: B = 83.65 [79.9, 87.0] for the hybrid
  and 94.85 [89.3, 101.4] for the transformer. A and E overlap, and the
  transformer's E is the lower (1.55 against 1.58). With free exponents
  every coefficient's interval overlaps.
- **The counter-result in the same paper** (§4.3, Table 5). Gated DeltaNet
  without negative eigenvalues cannot track state, so it is the less
  expressive variant on the paper's own account. It "shows very similar
  scaling trends". At 1B the positive-eigenvalue hybrid scores 0.667 BPB
  against the selected negative-eigenvalue hybrid's 0.669. The authors say
  this is "in potential disagreement with theory" and suggest some other
  benefit of GDN may be doing the work.

## What this does not say

- **Not that hybrids are better because they are more expressive.** The
  hybrid differs from the transformer in its recurrence, its state size, its
  inductive bias toward recency, and its training stability (Olmo Hybrid
  App. A.1 shows a flatter gradient-spike profile). The B gap is consistent
  with this account and with any of those.
- **Not a prediction with numbers.** The authors warn against reading the
  model's coefficients and exponents quantitatively. The instantiation that
  fits was chosen after seeing the fits, so the fit is not evidence for that
  instantiation.
- **Not that the exponent is architecture-free in general.** It is free here
  because the account assumes expressibility is independent of task
  frequency. If the inexpressible tasks were concentrated in the tail, the
  exponent would move.

## What it would explain

Why [SOTA-132](../practices.d/SOTA-132.md)'s hybrids are more token-efficient than the transformers they
replace, if they are: in Olmo Hybrid's run, 49% fewer tokens to Olmo 3's
MMLU. Its value to the record is that it states a mechanism with a test.
The paper has already run that test once, and the result went the wrong
way.
