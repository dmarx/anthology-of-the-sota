---
number: 281
status: Read
formerly:
- NOTE-tmphxkj0
paper: LIT-538
title: 'The founding paper already measured the regime dependence'
version: 1
date: '2026-09-22'
summary: >-
  Read because the record staked a claim on grokking being a data-starved-regime
  phenomenon while holding only the paper that put a number on it. The founding
  paper measured the dependence too, and reported it as a headline: converged
  accuracy is flat across a range of training-set sizes while time-to-generalize
  explodes as the set shrinks. It also names weight decay as the strongest
  intervention it found, which is the thread every later mechanism pulls on.
---

# NOTE-281: The founding paper already measured the regime dependence

## Contribution

It names a phenomenon and builds the testbed for studying it. Binary operation
tables `a ∘ b = c` over abstract symbols, a small transformer, one GPU: a
setting where memorization, generalization, data efficiency and speed of
learning can be varied independently and the curves read off directly. The
phenomenon is that validation accuracy can go from chance to perfect a
thousand-fold more optimization steps after training accuracy saturates.

## Key insight

**Withhold enough of a small structured dataset and generalization stops being
something that accompanies fitting and becomes something that happens
afterwards, if at all.** The gap is not a fixed property of the task — it is a
function of how much you withheld, and the paper's own Figure 1 puts the
dramatic curve and the data-fraction curve side by side.

## Assumptions

- **Small algorithmically generated datasets.** Binary operation tables with
  every element a distinct abstract token; the network sees no internal
  structure of the operands — no decimal notation, no permutation line
  notation.
- A small transformer throughout; architecture and hyperparameters in the
  appendix.
- Optimization budget `10⁵` steps for the comparison experiments, `10⁶` for
  the headline run.
- Results averaged over three seeds where reported.

## Key results

- **The headline run.** Division mod 97, 50% training data: training accuracy
  near-perfect at `< 10³` steps; validation accuracy reaching that level near
  `10⁶`; very little generalization before `10⁵`. Validation loss
  double-descends.
- **Learning-time curves.** For the product in `S₅`, median steps to 99%
  validation accuracy rises sharply as the training fraction falls — **in the
  vicinity of 25–30% data, a 1% decrease raises it by 40–50%**. Steps to 99%
  *training* accuracy trends *down* as data shrinks and stays in `10³`–`10⁴`.
  The same exponential-looking rise appeared on every algorithmic task where
  the networks generalized at all.
- **Weight decay.** More than halves the samples needed relative to most other
  interventions. Decay toward the initialization also works but less well than
  toward the origin — which the authors read as the zero-weight prior
  explaining part, not all, of the effect. Gradient and weight noise help,
  consistent with flatter minima. Learning rate must be within about one order
  of magnitude.
- **Task dependence.** `x³ + xy² + y (mod 97)` never generalized at any
  fraction up to 95%; to that model the data was effectively random. Symmetric
  operations (`x+y`, `x*y`, `x²+y²`) need less data than their asymmetric
  counterparts, possibly because a transformer can ignore positional
  embeddings. A deliberately mixed operation — `x/y` if `y` is odd, else
  `x−y` — still generalized, so grokking is not confined to clean group or
  ring operations.
- **Embeddings.** t-SNE of the output layer sometimes recovers the object's
  structure, including a circular number line for modular addition.

## Limitations

**One architecture family and one kind of data.** Whether any of it transfers
is the question [ARXIV-2210.01117](https://arxiv.org/abs/2210.01117) was written to answer, and it is not asked
here.

**No mechanism.** The paper is explicit that it is proposing a testbed, and
its explanatory content is a set of ablations rather than an account. Every
theory the record now files is downstream of this and none of it is here.

**"Sometimes".** The abstract says validation accuracy "sometimes suddenly
begins to increase"; the paper reports operations where it never does, and
notes that at larger dataset sizes training and validation curves track each
other closely. The reputation of the phenomenon is more universal than the
paper's own claim.

## Bearing on the record

**It changes who is owed what in `SOTA-200`.** That practice's third check
cites `LIT-085`'s ~60%-data finding. Reading this, the data-fraction dependence
is not a later discovery that deflated the phenomenon — it is a headline
result of the paper that introduced it, and `LIT-085` sharpened an existing
measurement into a threshold. The practice's prose reads as though the
deflation arrived from outside, and it did not.

**Weight decay is the thread.** It is the strongest intervention here, and
both [ARXIV-2210.01117](https://arxiv.org/abs/2210.01117) and [ARXIV-2309.02390](https://arxiv.org/abs/2309.02390) build mechanisms around what weight
decay does to the norm — which is precisely what [ARXIV-2310.06110](https://arxiv.org/abs/2310.06110) later
removes to produce a counterexample. All three arguments start in this
paper's ablation table.

## Open questions

- **What distinguishes the operations that never grok?** `x³ + xy² + y` failed
  at every fraction up to 95%, and this record can find no account of why some
  binary operations are learnable in this setting and others are not.
- **Does weight decay toward the origin beat decay toward initialization for
  the reason given?** The paper offers a zero-weight prior as a partial
  explanation and says so; nothing here or downstream tests it.
