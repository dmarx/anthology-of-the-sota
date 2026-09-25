---
number: 71
status: Proposed
formerly:
- THEORY-tmpmiiyl
title: 'A memorising and a generalising circuit compete on logits per unit norm, and which one wins flips when the data makes memorising more expensive'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    The title said the flip happens "at a critical dataset size". LIT-667
    is a named correction of exactly that: with the inferred/atomic ratio held
    fixed, scaling the training set changes nothing about the transition, and
    the paper proposes critical data *distribution* in its place. The crossover
    survives and is now stated by what it is indexed on — whatever makes
    memorising more expensive while leaving generalising alone — which is
    dataset size in the algorithmic setting and the ratio in the knowledge
    setting. The `promote_when` is rewritten too, because it asked for "a
    measured `D_crit`" outside algorithmic data, and the paper that went
    outside algorithmic data showed there is no `D_crit` to measure there.
tags:
- analysis-and-evaluation
- model-stability
- training-optimization
- capability-thresholds
date: '2026-09-22'
source:
- LIT-539
- LIT-085
- LIT-667
promote_when: >-
  The efficiency ordering is **measured** — parameter norm per unit logit, on
  the mixed networks that actually grok rather than on constructed
  `C_mem`-only and `C_gen`-only ones — and something accounts for the grokking
  LIT-537 reports with no weight decay at all. A third domain in which the
  crossover's *consequences* show up is explicitly not it: LIT-667
  supplied one, and what it established was that the quantity the previous
  version of this field asked to be measured does not exist there.
summary: >-
  Varma et al. ([LIT-539](../literature.d/LIT-539.md)), making precise the "simpler solution" genre
  [LIT-085](../literature.d/LIT-085.md) proposed. Two circuit families fit the training set; once
  cross-entropy is near zero the only remaining pressure is weight decay, which
  prefers whichever produces a given logit at lower parameter norm.
  Memorisation gets less efficient as the dataset grows and generalisation does
  not, so they cross at a critical dataset size `D_crit`. From that the paper
  derived **ungrokking** and **semi-grokking** and then observed both. What
  crosses is not indexed on dataset size, though: LIT-667 holds the
  inferred/atomic ratio fixed, scales the data, and nothing happens.
  `Proposed`, on scope rather than on evidence: it needs weight decay, and
  LIT-537 groks without any.
corrected_by:
- THEORY-070
explains:
- SOTA-402
---

# THEORY-071: A memorising and a generalising circuit compete on logits per unit norm, and which one wins flips when the data makes memorising more expensive

<!-- inactive-ok-file: THEORY-070 — Proposed, and named here as one of the three rival mechanisms this cluster holds; Proposed is the record's judgement on its scope, which is the point being made when it is cited. -->
<!-- inactive-ok-file: THEORY-032 — Proposed, and cited only for the shape of its v3 amendment: how its promotion condition failed, which is a fact about this record's editing rather than about the account. -->

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

## The index is not dataset size

That argument is about *examples*, and it is the part [LIT-667](../literature.d/LIT-667.md) corrects by
name. Wang et al. train on a mixture of atomic facts and facts deduced from
them, and separate two knobs the algorithmic setting fuses:

- **Hold the inferred/atomic ratio `φ` and scale the data.** Nothing happens —
  not the gap between the train and test curves, not the level reached. There
  is no `D_crit` in this setting to measure.
- **Hold the size and raise `φ`.** Grokking accelerates monotonically, and at
  `φ = 18.0` it is gone.

The efficiency argument survives this, and in fact the paper runs it: `C_mem`
must store the inferred facts as well as the atomic ones, while `C_gen` stores
the atomic facts twice at most, so `N_mem` grows with `φ` and `N_gen` is
bounded. Scaling the data at fixed `φ` scales both, and the *ratio* of the two
is what the regularizer sees. The crossover is real; **dataset size was a proxy
for it** in a setting where every example is an inferred fact and there is
nothing else to trade against.

So this document's claim is now stated by what the crossover is indexed on —
whatever makes memorising dearer while leaving generalising alone — which is
the training fraction in modular addition and the derived-fact ratio in a
knowledge graph. Both are the same quantity seen through different data.

One caution, because it cuts the other way too: the reverse inference is not
available. Modular addition has no atomic/inferred split, so `φ` is not defined
there, and nothing here shows that the size dependence [LIT-538](../literature.d/LIT-538.md) and [LIT-085](../literature.d/LIT-085.md)
measured was secretly a distribution effect. What it shows is that those
experiments could not have told the difference, because they moved size and
composition with one knob.

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
are measured on these, not on the mixed networks that actually grok.

[LIT-667](../literature.d/LIT-667.md) does not close that. It traces a generalising circuit in a
non-algorithmic setting, which the previous version of the `promote_when` asked
for, and then argues the efficiency ordering by **counting facts** — how many
each circuit must store — rather than by measuring norm per unit logit. A
counting argument over a traced circuit is a better thing to have than a
counting argument over a hypothesised one, and it is still not the
measurement. That is what the rewritten `promote_when` asks for, and it now
asks for it in the setting the account was built in rather than somewhere else.

The status is about scope. On evidential shape — risky predictions, made
first, confirmed after — this is the best-supported account here, and
[THEORY-070](THEORY-070.md), which contradicts it, leaves both of its novel phenomena
unexplained. [LIT-667](../literature.d/LIT-667.md) adds a second domain and a third confirmed
prediction of the same shape (raising weight decay accelerates grokking, which
the efficiency story implies and the paper then measured), which is why the
correction above is an amendment and not a demotion.

**A note on what this cost.** The previous `promote_when` asked for "a measured
`D_crit` ... outside algorithmic data". The paper that went outside algorithmic
data reported that there is no `D_crit` there to measure. A promotion condition
can be met in spirit and refuted in letter at the same time, and the honest
response is to fix the condition rather than to read the paper as satisfying
it — the same call as [THEORY-032](THEORY-032.md) v3, for a different reason: there the result
was the right shape and the wrong measurement, here the condition named a
quantity that does not exist in the setting it demanded.
