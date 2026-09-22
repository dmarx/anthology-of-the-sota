---
number: 283
status: Read
formerly:
- NOTE-tmpp2k64
paper: LIT-539
title: 'Two novel phenomena predicted from the theory and then observed'
version: 1
date: '2026-09-22'
summary: >-
  Read as the mechanistic account with the best evidential shape in this
  cluster. From "weight decay prefers the circuit with more logit per unit
  norm, and memorisation gets less efficient as the dataset grows" it derives a
  critical dataset size, and from that derives ungrokking — a grokked network
  losing its generalization when trained on less data — and semi-grokking. Both
  were then observed. The mechanism needs weight decay, which is where the
  counterexample lands.
---

# NOTE-283: Two novel phenomena predicted from the theory and then observed

## Contribution

It states a specific, falsifiable version of "the generalising solution is
simpler", derives consequences nobody had reported, and confirms them. The
version: two circuit families both fit the training set, weight decay prefers
whichever produces a given logit at lower parameter norm, and memorisation's
efficiency degrades with dataset size while generalisation's does not. The
consequences: a critical dataset size, ungrokking, semi-grokking.

## Key insight

**Grokking is a preference, not a discovery.** Once training loss is near zero,
the only remaining gradient signal is the regularizer, and it ranks the two
circuits by logits-per-norm. Nothing needs to be *found* late; the generalising
circuit was being built all along, and what happens at the transition is that
paying for it becomes cheaper than paying for memorisation. The corollary is
that the ranking depends on dataset size, and can be reversed by changing it.

## Assumptions

- **Weight decay, or some norm-penalising pressure.** The whole argument is
  about what the regularizer prefers once cross-entropy is near zero.
- Two circuit families exist and are separable — operationalized by producing
  `C_mem`-only networks with fully random labels, and `C_gen`-only networks at
  large dataset size, verified by `> 95%` of logit norm lying in the
  trigonometric subspace.
- The efficiency argument is an *average* statement: classifier efficiency is
  monotonically non-increasing in dataset size on average, from the argument
  that a classifier trained on `D ∪ {(x, y*)}` cannot beat one trained on `D`
  at `D`'s own objective.
- 1-layer transformers, AdamW, cross-entropy, modular addition at `P = 113`
  for the headline results; nine further tasks in the appendix.
- The three ingredients are offered as **sufficient**, not necessary — the
  paper is careful about this, and it is the gap the counterexample enters
  through.

## Key results

- **(P1) Efficiency vs dataset size.** Confirmed: `C_mem`'s efficiency falls as
  the training set grows, `C_gen`'s does not. Measured by varying weight decay
  to trace logits against parameter norm, at several dataset sizes.
- **`D_crit` follows.** The two efficiencies cross at a critical dataset size.
- **(P2) Ungrokking, and it is sharp.** A network that has grokked at
  `D > D_crit`, trained on `D′ < D_crit`, regresses from high to near-random
  test accuracy, with a sharp transition in `D′` around `D_crit`. Distinct from
  ordinary catastrophic forgetting in that no new examples are introduced —
  removal alone does it.
- **(P3) Ungrokking's endpoint is independent of weight decay**, as predicted,
  because `D_crit` does not depend on it. This is the sub-prediction that is
  hardest to get right by accident.
- **(P4) Semi-grokking.** At `D ≈ D_crit`, delayed generalisation to *middling*
  test accuracy — a mixture of the two circuits rather than one winning. The
  paper is explicit that its theory permits either this or a clean winner and
  does not predict which; it reports observing semi-grokking.

## Limitations

**It needs weight decay and [ARXIV-2310.06110](https://arxiv.org/abs/2310.06110) removes it.** That paper groks on
modular arithmetic with no weight decay and a rising parameter norm. The three
ingredients here are claimed sufficient rather than necessary, so this is not
an internal contradiction — but it does mean the account is not the general
explanation of grokking, and the paper's title reads as though it were.

**Circuits are operationalized by proxy.** `C_mem`-only via random labels and
`C_gen`-only via large data with a trigonometric-subspace check are reasonable
constructions and they are constructions; the efficiency curves are measured on
these, not on the mixed networks that actually grok.

**Modular addition carries the headline.** Nine more tasks are in the appendix,
all algorithmic.

## Bearing on the record

**It is the descendant of the record's one pre-existing grokking paper.** The
paper names `LIT-085`'s Appendix E as the explanation genre it is making
precise and cites its Figures 1 and 7 for the generalising circuit and for
slow-versus-fast learning. Filing this without the trunk would have left the
record holding an account and its antecedent with the founding paper missing
between them.

**Ungrokking is the strongest single argument for `SOTA-200`'s third check.**
A capability that a model *loses* when you shrink its training set, at a sharp
threshold, with the endpoint independent of the regularization strength, is
about as direct a demonstration as exists that the discontinuity belongs to the
regime and not to the task.

## Open questions

- **Does `D_crit` exist outside algorithmic data?** The efficiency crossover is
  measured on modular addition. [ARXIV-2210.01117](https://arxiv.org/abs/2210.01117) reports a critical data size on
  MNIST, by a different argument and without the circuit decomposition; nobody
  has connected the two.
- **What explains ungrokking under the rival accounts?** Neither the LU
  mechanism nor lazy-to-rich addresses it, and this record can find no attempt.
