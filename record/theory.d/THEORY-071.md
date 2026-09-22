---
number: 71
status: Proposed
formerly:
- THEORY-tmpmiiyl
title: 'A memorising and a generalising circuit compete on logits per unit norm, and which one wins flips at a critical dataset size'
version: 1
tags:
- analysis-and-evaluation
- model-stability
- training-optimization
date: '2026-09-22'
source:
- LIT-539
- LIT-085
promote_when: >-
  The efficiency crossover is demonstrated outside algorithmic data — a
  measured `D_crit`, or an ungrokking transition, on a task where the
  generalising circuit is not a known trigonometric construction. That is
  what stands between this account and being the record's explanation of
  grokking, not more evidence in the setting it already covers.
summary: >-
  Varma et al. ([LIT-539](../literature.d/LIT-539.md)), making precise the "simpler solution" genre
  [LIT-085](../literature.d/LIT-085.md) proposed. Two circuit families fit the training set; once
  cross-entropy is near zero the only remaining pressure is weight decay, which
  prefers whichever produces a given logit at lower parameter norm.
  Memorisation gets less efficient as the dataset grows and generalisation does
  not, so they cross at a critical dataset size `D_crit`. From that the paper
  derived **ungrokking** and **semi-grokking** and then observed both.
  `Proposed`, on scope rather than on evidence: it needs weight decay, and
  [LIT-537](../literature.d/LIT-537.md) groks without any.
corrected_by:
- THEORY-070
---

# THEORY-071: A memorising and a generalising circuit compete on logits per unit norm, and which one wins flips at a critical dataset size

<!-- inactive-ok-file: THEORY-070 — Proposed, and named here as one of the three rival mechanisms this cluster holds; Proposed is the record's judgement on its scope, which is the point being made when it is cited. -->

## The account

Three ingredients, claimed sufficient:

1. `C_gen` generalises and `C_mem` does not;
2. `C_gen` is more **efficient** — it produces equivalent cross-entropy at
   lower parameter norm;
3. `C_gen` is learned more slowly.

Then the story is short. Early on, `C_mem` is built fast and training loss goes
to near zero. After that the cross-entropy term has almost nothing left to say
and the regularizer does the talking: gradient descent keeps reducing total
loss by moving parameter norm from `C_mem` to `C_gen`, and when enough has
moved, test accuracy transitions. **Nothing is discovered late.** The
generalising circuit was being built all along; what changes is which circuit
is cheaper to keep.

**The dataset-size argument.** A classifier trained on `D ∪ {(x, y*)}` cannot
be more efficient than one trained on `D`, so efficiency is non-increasing in
dataset size on average. If the model already generalises to the new point,
nothing changes — so `C_gen`'s efficiency is flat in `D`. If it does not, the
memorising circuit must spend more norm — so `C_mem`'s efficiency falls. They
cross at **`D_crit`**.

## Why the evidence is the strongest in this cluster

The crossover implies two behaviours nobody had reported, and the paper went
and found them.

**Ungrokking.** Take a network that grokked at `D > D_crit` and keep training
it on `D′ < D_crit`. `C_mem` is now the cheaper circuit, so norm should move
back and test accuracy should *fall*. It does — with a **sharp** transition in
`D′` around `D_crit`, on removal of examples alone rather than the introduction
of new ones, and with a final test accuracy **independent of weight decay**,
because `D_crit` is. That last sub-prediction is the one hardest to hit by
accident.

**Semi-grokking.** At `D ≈ D_crit` the circuits are similarly efficient, so a
mixture is possible and delayed generalisation should arrive at *middling*
accuracy. The paper states that its theory permits either this or a clean
winner and does not predict which, then reports observing semi-grokking.

All four predictions confirmed on 1-layer transformers with AdamW on modular
addition at `P = 113`, with nine further algorithmic tasks in the appendix.

## Why it is `Proposed` anyway

**It needs weight decay, and [LIT-537](../literature.d/LIT-537.md) exhibits grokking without any** — on
modular arithmetic, with a two-layer MLP, and with the parameter norm *rising*
through the transition. The three ingredients are claimed sufficient rather
than necessary, so this is not an internal contradiction; it does mean the
account cannot be the general explanation, which is what its title reads as.

**And the circuits are constructions.** `C_mem`-only networks come from
training on random labels, `C_gen`-only from large datasets with a check that
`> 95%` of logit norm lies in the trigonometric subspace. The efficiency curves
are measured on these, not on the mixed networks that actually grok. Outside
modular addition there is no known generalising circuit to check against, which
is exactly what the `promote_when` asks somebody to supply.

The status is about scope. On evidential shape — risky predictions, made
first, confirmed after — this is the best-supported account here, and
[THEORY-070](THEORY-070.md), which contradicts it, leaves both of its novel phenomena
unexplained.
