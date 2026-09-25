---
number: 69
status: Active
formerly:
- THEORY-tmpdlyut
title: 'Grokking is a regime rather than a property of algorithmic data, and at least three knobs move it'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Qualifies the first of the three knobs. Every measurement behind
    "training-set size" varies the training *fraction* of a fixed universe of
    examples, which moves size and composition with one knob. LIT-667 has
    two knobs and turns them one at a time: with the inferred/atomic ratio
    fixed, scaling the training set changes nothing. That does not overturn the
    algorithmic measurements — a ratio is not defined there — but it does mean
    the first knob is established only where the two are fused, and the
    paragraph now says which. Adds a fourth domain (knowledge-based reasoning)
    and the observation that the remaining gap in "what would change this" has
    narrowed to the data: this is grokking at a standard initialization, in a
    standard optimizer, with nothing inflated.
tags:
- capability-thresholds
- analysis-and-evaluation
- training-optimization
- model-stability
date: '2026-09-22'
source:
- LIT-538
- LIT-540
- LIT-537
- LIT-085
- LIT-667
explains:
- SOTA-200
summary: >-
  Delayed generalization is not a fact about modular arithmetic. It is produced
  and removed by moving the training regime, and three knobs have been shown to
  move it: **training-set size** (Power et al., [LIT-538](../literature.d/LIT-538.md), and the ~60%
  threshold in [LIT-085](../literature.d/LIT-085.md)), **initialization scale relative to the generalizing
  weight norm** (Liu et al., [LIT-540](../literature.d/LIT-540.md), which uses it to induce grokking on
  MNIST, IMDb and QM9 and to eliminate it on algorithmic data), and **the
  alignment between the initial neural tangent kernel and the target** (Kumar
  et al., [LIT-537](../literature.d/LIT-537.md)). The three mechanistic accounts in this record
  contradict each other; they agree on this.
---

# THEORY-069: Grokking is a regime rather than a property of algorithmic data, and at least three knobs move it

<!-- inactive-ok-file: THEORY-071 — Proposed, and named here as one of the three rival mechanisms this cluster holds; Proposed is the record's judgement on its scope, which is the point being made when it is cited. -->
<!-- inactive-ok-file: THEORY-070 — Proposed, and named here as one of the three rival mechanisms this cluster holds; Proposed is the record's judgement on its scope, which is the point being made when it is cited. -->
<!-- inactive-ok-file: THEORY-072 — Proposed, and named here as one of the three rival mechanisms this cluster holds; Proposed is the record's judgement on its scope, which is the point being made when it is cited. -->


## The account

Grokking — training accuracy saturating long before validation accuracy leaves
chance — is a *regime* a training run can be put into and taken out of. It is
not a property of algorithmic datasets, and it is not a fundamental feature of
overparameterized learning. Three separate knobs have been shown to control it,
each demonstrated in both directions.

**Training-set size — or something fused with it.** [LIT-538](../literature.d/LIT-538.md) measures it in
the paper that named the phenomenon: converged accuracy is flat across a range
of training fractions while the *time* to reach it explodes as the fraction
falls — in the vicinity of 25–30% on `S₅`, removing 1% of the data raises
median steps-to-generalize by 40–50%, while steps-to-fit stay at `10³`–`10⁴`.
[LIT-085](../literature.d/LIT-085.md) puts a threshold on it: above roughly 60% data on modular
addition, grokking is gone and generalization is immediate.

Both vary the *fraction* of a fixed universe of examples, which is one knob
moving two things — how much data there is, and what proportion of the possible
examples it covers. [LIT-667](../literature.d/LIT-667.md) has two knobs and turns them separately: on
knowledge-based reasoning, holding the inferred/atomic ratio fixed and scaling
the training set changes **nothing**, while moving the ratio at fixed size moves
grokking speed monotonically. A ratio of that kind is not defined on modular
arithmetic, so this does not overturn the measurements above; it does mean they
could not have told which of the two they were measuring. The knob is real. What
it is a knob *on* is open.

**Initialization scale relative to the generalizing weight norm.**
[LIT-540](../literature.d/LIT-540.md) induces grokking on **MNIST** (depth-3 MLP, 1k examples, Kaiming
weights scaled by `α > 1`), on **IMDb** with an LSTM at `α = 6`, and on **QM9**
with a GCNN at `α = 3`. At the standard initialization there is no grokking on
any of them. Run the other way, constraining the model to a small-weight-norm
sphere nearly eliminates grokking on algorithmic data.

**Initial kernel–task alignment.** [LIT-537](../literature.d/LIT-537.md) sweeps an output-scale
parameter `α` and shows it makes grokking more dramatic or removes it entirely,
and shows that worse alignment between the initial NTK's top eigenvectors and
the labels produces more intense grokking — and, because feature learning is
then necessary rather than optional, a *lower* final test loss. Alignment is
computable on any task as centered kernel alignment.

## Why this is `Active` when the mechanisms are not

The record holds three rival accounts of *why* — [THEORY-072](THEORY-072.md),
[THEORY-071](THEORY-071.md) and [THEORY-070](THEORY-070.md) — and none is settled; one of them exists
because it is an explicit counterexample to the other two. They disagree about
the mechanism and they do not disagree about this. A dataset-size condition
appears in all four of the algorithmic-data papers, including in
[LIT-537](../literature.d/LIT-537.md)'s own list of three conditions, which is the paper arguing
hardest against the others.

A claim that survives the disagreement of every account of the thing it
describes is in a different evidential position from any of them.

The fifth source is the exception that has to be stated. [LIT-667](../literature.d/LIT-667.md) does not
disagree that the regime can be moved; it disagrees about what the first knob
is, and unanimity among four papers that could not separate size from
composition is not evidence about which of the two it was.

## What it is not

**Not "grokking is an artefact".** Ungrokking ([LIT-539](../literature.d/LIT-539.md)) is a real,
sharp, reproducible behaviour, and the representations [LIT-538](../literature.d/LIT-538.md) visualizes
are real structure. The phenomenon happens; it happens in a regime.

**Not "three knobs is the list".** Three are established. Weight decay strength
changes the *timing* in two of the accounts without being one of these axes —
[LIT-667](../literature.d/LIT-667.md) measures that directly, and raising it accelerates grokking — and
[LIT-538](../literature.d/LIT-538.md) reports operations that never generalize at any data fraction,
which no knob here explains.

**Not "and now there are four".** The inferred/atomic ratio is not being added
as a fourth axis, because on the reading [THEORY-071](THEORY-071.md) now takes it is the first
axis seen properly: both are ways of making the memorising solution more
expensive. Counting it twice would claim an independence nobody has shown.

**Not a licence to read across the demonstrations.** Every result outside
algorithmic data in [LIT-540](../literature.d/LIT-540.md) changes two things at once — a much smaller
training set *and* an inflated initialization — so the axes are established
jointly rather than separately, and the paper says so.

## What would change this

A demonstration of delayed generalization at standard initialization, on a
standard-sized dataset, with no knob turned — that is, grokking arriving
unbidden in an ordinary training run. Nothing in these five papers is that, and
the one setting where it occurs unbidden is the small algorithmic dataset,
which is itself a regime choice.

[LIT-667](../literature.d/LIT-667.md) narrows what is left. An 8-layer GPT-2 at a standard
initialization, AdamW at weight decay 0.1, nothing inflated and nothing
constrained — and generalization arrives roughly **50× after** the training set
is fit. The model and the optimizer are ordinary there. What is engineered is
the *data*: a synthetic knowledge graph with a chosen ratio of derived to
atomic facts. So the remaining gap in this section is no longer "grokking needs
a doctored initialization"; it is that every setting in which anyone has watched
grokking has a data distribution somebody chose.
