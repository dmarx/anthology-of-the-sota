---
status: Active
title: 'Explaining grokking through circuit efficiency'
version: 1
tags:
- analysis-and-evaluation
- model-stability
- training-optimization
date: '2026-09-22'
published: '2023-09-05'
arxiv: '2309.02390'
first_author: 'Varma'
keywords:
- 'grokking'
- 'circuit efficiency'
- 'critical dataset size'
- 'ungrokking'
- 'weight decay'
implementations: []
summary: >-
  Varma, Shah, Kenton, Kramár and Kumar (2023), [ARXIV-2309.02390](https://arxiv.org/abs/2309.02390), DeepMind —
  the account that earns its place by predicting things nobody had seen.
  Memorising and generalising circuits both fit the training set; weight decay
  prefers whichever produces more logit per unit parameter norm; memorisation
  gets less efficient as the dataset grows and generalisation does not, so
  there is a critical dataset size `D_crit` where the preference flips. From
  that the paper predicts **ungrokking** and **semi-grokking**, and then
  observes both. Read as [NOTE-tmpp2k64](../notes.d/NOTE-tmpp2k64.md).
---

# LIT-tmp9xrey: Explaining grokking through circuit efficiency

Varma, Shah, Kenton, Kramár and Kumar (2023) — [ARXIV-2309.02390](https://arxiv.org/abs/2309.02390). Read as
[NOTE-tmpp2k64](../notes.d/NOTE-tmpp2k64.md).

## Key takeaways

- **Three ingredients are claimed sufficient for grokking:** `C_gen`
  generalises and `C_mem` does not; `C_gen` is more *efficient*, producing
  equivalent logits at lower parameter norm; and `C_gen` is learned more
  slowly. Weight decay then keeps reducing an already-near-zero training loss
  by moving norm from `C_mem` to `C_gen`, and test accuracy transitions.
- **The dataset-size argument.** Adding a point a classifier already
  generalises to changes nothing; adding one it gets wrong forces memorisation
  to spend more norm. So `C_mem`'s efficiency falls with dataset size while
  `C_gen`'s does not, and they cross at a **critical dataset size `D_crit`**.
- **Ungrokking.** Take a network that has grokked at `D > D_crit` and continue
  training it on `D′ < D_crit`: `C_mem` is now the more efficient circuit, so
  gradient descent should move norm back and test accuracy should *fall*. Three
  sharper sub-predictions: a **sharp** transition in `D′` around `D_crit`;
  it happens on removal alone, unlike ordinary catastrophic forgetting; and
  the final test accuracy is **independent of weight decay**, because `D_crit`
  is.
- **Semi-grokking.** At `D ≈ D_crit` the two circuits are similarly efficient,
  so a mixture is possible: delayed generalisation to *middling* rather than
  perfect test accuracy.
- **All four predictions (P1–P4) confirmed**, on 1-layer transformers with
  AdamW on modular addition (`P = 113`), with nine further tasks in the
  appendix. `C_mem`-only networks are produced with random labels, `C_gen`-only
  by large datasets with `> 95%` of logit norm in the trigonometric subspace.

## Standing in the anthology

**`Active` as a note, and the strongest evidential shape in this cluster.**
Ungrokking and semi-grokking were not observed and then explained; they were
derived and then looked for. That is the form of support the record most
wants and least often finds.

**It is explicitly built on `LIT-085`.** The paper names Nanda et al.'s
Appendix E as the explanation genre it is making precise, and cites that
paper's Figures 1 and 7 for the generalising circuit and for slow-versus-fast
learning. So the record's one pre-existing grokking paper turns out to be this
account's antecedent.

**Its mechanism is contested and its predictions are not.** [ARXIV-2310.06110](https://arxiv.org/abs/2310.06110)
exhibits grokking with no weight decay and a rising weight norm, which the
efficiency argument needs weight decay to explain; it says nothing about
ungrokking or semi-grokking, which remain unexplained by any rival.
