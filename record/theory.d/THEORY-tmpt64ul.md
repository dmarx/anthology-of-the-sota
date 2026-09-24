---
status: Proposed
promote_when: >-
  An independent group reproducing the block ablation at a scale where Muon is
  actually deployed — VO+FFN against full Muon on a model above 1B — or a
  direct test of the causal claim: intervene on the isotropy of the weight
  spectrum without changing the optimizer, and show the tail-class gap moves
  with it. What would NOT meet it: further measurements that Muon-trained
  weights are more isotropic, which is the observation rather than the
  mechanism, or another demonstration that Muon beats Adam overall.
title: 'Muon''s update matches the outer-product structure of associative memories, which is why it learns tail classes that Adam under-trains'
version: 1
tags:
- training-optimization
- signal-structure
date: '2026-09-24'
source:
- LIT-tmpaqpf2
explains:
- SOTA-121
summary: >-
  Wang et al. (2025), [LIT-tmpaqpf2](../literature.d/LIT-tmpaqpf2.md). A linear associative memory is a sum of
  outer products; orthogonalising the update treats every outer-product
  direction alike. So Muon produces more isotropic weight spectra than Adam,
  and on heavy-tailed data that shows up as **tail classes being learned**
  where Adam under-trains them. The ablation localises the effect: Muon on
  value-output weights and the FFN nearly recovers full Muon, and Muon on
  query-key contributes little.
---

<!-- inactive-ok-file: THEORY-032, THEORY-024, THEORY-033, THEORY-081 — all Proposed.
     The first three are named as the record's existing accounts of spectral
     updates, to say how this one differs from each; nothing here rests on any
     being settled, and THEORY-032's being open is what the comparison is
     about. THEORY-081 is named as the Proposed premise this account inherits,
     which the document states as a reason for its own status. -->

# THEORY-tmpt64ul: Muon's update matches the outer-product structure of associative memories, which is why it learns tail classes that Adam under-trains

## Source

Wang, Zhang, Li, Du, Du, Pang, Yang, Hong and Tan (2025), `LIT-tmpaqpf2`.

## The account, in three steps

**One.** The transformer blocks that behave as associative memories are the
value-output attention weights and the FFN (`THEORY-081` for the FFN half). A
linear associative memory over key-value pairs has the algebraic form
`W = Σ_i e_o_i e_s_i^T` — a sum of outer products, one per stored fact.

**Two.** Muon orthogonalises the gradient: it replaces the singular values of
the update with equal ones. Against a sum of outer products that is the
operation which **allocates the same step to every stored direction**,
irrespective of how much gradient signal each one carries. Adam scales
entrywise, so directions with more signal move further.

**Three.** Gradient signal per direction is proportional to how often the
corresponding fact appears, and real corpora are heavy-tailed. So the
directions Adam under-serves are exactly the rare ones. The prediction is that
Muon should match Adam on frequent classes and beat it on rare ones — which is
what the source measures, and the head–tail gap narrows accordingly.

The compressed version: **Adam's balance across facts depends on the geometry
of the embeddings; Muon's does not.** The one-layer theorem makes that precise
— for any embeddings satisfying their assumption, one step of Muon gives a
balance measure `ϱ ≥ 1 − ε(1 + O(log K / K))`, while plain gradient descent
gives `O(ε^{−r}K^{r−1})` with `r < 1`, which degrades as the number of facts
grows.

## What it predicts that the record can check

**Which parameters carry the gain.** VO and FFN, not QK, and within those `W_O`
over `W_V` and `W_out` over `W_in`. This is a claim about where a spectral
optimizer is worth its cost, and it is the first such claim in this record that
names blocks rather than conditions.

**That the gain is data-distribution-dependent.** On a balanced corpus the
account predicts the advantage should shrink. Nobody has run that, and it is
the cleanest falsification available.

## Why `Proposed`

**One group, one paper**, with ablations at small scale and a 0.7B check, and
a theorem about a one-layer model with momentum disabled and zero
initialisation.

**The isotropy is measured as a correlate.** The source shows Muon-trained
weights have higher SVD entropy and effective rank than Adam-trained ones,
consistently. It does not intervene on isotropy while holding the optimizer
fixed, so the step from *isotropic spectra* to *tail-class learning* rests on
the one-layer theorem rather than on an experiment.

**One observation cuts against the tidy version.** The source also reports
that Muon learns more isotropic **QK** weights than Adam — and QK is the block
that contributes little. So isotropy is general and the benefit is not, which
means isotropy alone cannot be the whole mechanism. The associative-memory
structure is doing work that isotropy does not do by itself.

**It inherits a `Proposed` premise.** The FFN-as-associative-memory reading is
`THEORY-081` here, itself `Proposed` on 160 hand-annotated keys of one
16-layer model. This account is downstream of it.

## Where it sits among the record's spectral-update accounts

Three documents here already say something about why spectral updates work,
and all three are about the *update rule* in the abstract:

- `THEORY-024` — orthogonalising is dualising, and muP and Shampoo are partial
  approximations of it.
- `THEORY-032` — the spectral step's one-step bound beats the Euclidean one by
  the ratio of the gradient's nuclear rank to the incoming activations' stable
  rank.
- `THEORY-033` — what it buys is a step size that stays optimal.

This one is about **which matrices and which data**, and it is the first that
makes a prediction a practitioner could act on when deciding where to spend a
spectral optimizer.

It is also close enough to `THEORY-032` to be worth saying how they differ.
That account's condition is a property of the *incoming activations*; this
one's is a property of the *block's role and the data's tail*. They could
coincide — an associative-memory block may be exactly the one whose incoming
activations are low stable rank — and nobody has checked. `THEORY-032`'s
`promote_when` now names that as the discriminating measurement.
