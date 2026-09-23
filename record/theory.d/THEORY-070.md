---
number: 70
status: Proposed
formerly:
- THEORY-tmplnntp
title: 'Grokking is the transition from lazy to rich training dynamics'
version: 1
tags:
- training-optimization
- analysis-and-evaluation
- model-stability
- capability-thresholds
date: '2026-09-22'
source:
- LIT-537
corrects:
- THEORY-072
- THEORY-071
promote_when: >-
  The account is extended to cover ungrokking — a grokked network regressing
  to near-random test accuracy at a sharp threshold in dataset size, with an
  endpoint independent of weight decay. Until something in the lazy-to-rich
  picture produces that, this corrects the weight-norm accounts without
  replacing them, and the record holds three partial explanations rather than
  one.
summary: >-
  Kumar, Bordelon, Gershman and Pehlevan ([LIT-537](../literature.d/LIT-537.md)). The memorising phase
  is early *lazy* training: the network fits the training set in its initial
  feature basis, which the linearised approximation describes, so training loss
  falls with no test improvement. Grokking is the late breakdown of that
  approximation as feature learning begins. Two knobs control it — an
  output-scale laziness parameter and the alignment between the initial neural
  tangent kernel and the target — and neither is weight norm. Filed with
  `corrects` on both weight-norm accounts, because the paper's §3 is an
  explicit counterexample to them.
---

# THEORY-070: Grokking is the transition from lazy to rich training dynamics

<!-- inactive-ok-file: THEORY-071 — Proposed, and named here as one of the three rival mechanisms this cluster holds; Proposed is the record's judgement on its scope, which is the point being made when it is cited. -->
<!-- inactive-ok-file: THEORY-072 — Proposed, and named here as one of the three rival mechanisms this cluster holds; Proposed is the record's judgement on its scope, which is the point being made when it is cited. -->

## The account

In the lazy regime a network is well approximated by its linearisation around
initialization: it fits the training data by reweighting the features it
started with, and learns no new ones. That is enough to drive training loss to
near zero on a small dataset, and it generalises only as well as the initial
neural tangent kernel does — which, if the kernel's top eigenvectors are
misaligned with the labels, is badly.

Grokking is what happens when the linear approximation breaks down and feature
learning starts. The "memorising solution" of the other accounts and the lazy
solution look the same from outside: both fit fast, both generalise poorly,
both are followed by a long plateau. The difference is whether the network is
storing examples or fitting them in a basis it has not yet updated.

Two knobs follow, and neither is a norm:

- **Laziness `α`**, an output-scale parameter (also reachable by label
  rescaling). Sweeping it makes grokking more dramatic or removes it entirely.
- **Initial kernel–task alignment**, `ε` in the toy model and **centered kernel
  alignment** in general — computable on any task, before training.

Three conditions are stated for grokking to appear: the top NTK eigenvectors
are misaligned with `y(x)`; the dataset is large enough that generalisation is
eventually possible but not so large that training loss tracks test loss
throughout; and the network starts lazy.

## The counterexample it is built on

§3 is the load-bearing part. **Modular arithmetic, two-layer MLP, no weight
decay: the model groks, and the parameter weight norm rises through the
transition.** The polynomial-regression task behaves the same way.

Both [THEORY-072](THEORY-072.md) and [THEORY-071](THEORY-071.md) explain grokking by a late *decrease*
in weight norm — one as a walk down to the generalizing shell, the other as
norm moving from the memorising circuit to the more efficient one. Neither can
produce a run with no regularizer and a rising norm. That is why `corrects` is
declared on both, and why the declaration is about the mechanism rather than
about the experiments either paper reports.

## What it also gets

- Worse initial alignment gives **more intense grokking and a lower final test
  loss**, because poor alignment is where feature learning is necessary rather
  than optional. "Lazy, misaligned networks grok the most intensely."
- Consistency across architectures, optimizers and datasets, carried from the
  analysable two-layer polynomial-regression setting to MNIST, one-layer
  transformers and student–teacher networks.
- A methodological point the record keeps: the analysis is in **loss, not
  accuracy**, on the grounds that loss drives the dynamics and that accuracy
  curves on regression tasks can be gamed by the choice of metric.

## Why it is `Proposed`

**It leaves its predecessor's two confirmed novel predictions unexplained.**
[THEORY-071](THEORY-071.md) derived ungrokking and semi-grokking before anybody had seen
them, and this account says nothing about a grokked network regressing at a
sharp threshold in dataset size with a weight-decay-independent endpoint. A
correction that cannot reproduce what it corrects has narrowed the earlier
account's scope rather than replaced it, and the record files it that way.

**The analysable setting is a two-layer network on polynomial regression**; the
transformer and MNIST results are reported as consistent rather than derived.

**And its second condition is a dataset-size window** — so the paper attacking
the others hardest still agrees with all of them, and with [LIT-085](../literature.d/LIT-085.md) and
[LIT-538](../literature.d/LIT-538.md), about the regime. That agreement is [THEORY-069](THEORY-069.md) and it is the
only `Active` account here.
