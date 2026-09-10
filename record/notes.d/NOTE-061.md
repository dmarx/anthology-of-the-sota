---
number: 61
status: Read
formerly:
- NOTE-tmpqvwzr
# inactive-ok: LIT-031 — Superseded — this document is the reading that says what survives the supersession
paper: LIT-031
title: 'Pruned Neural Networks are Surprisingly Modular'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-09'
published: '2020-03-01'
summary: >-
  Imports modularity from graph clustering — a module is neurons with strong internal and weak external connectivity — and measures it by spectral clustering on MLP weights. Trained and pruned networks are more modular than random ones, and than random networks with the same sparse weight distribution, which is the control that makes the result mean something.
---

# NOTE-061: Pruned Neural Networks are Surprisingly Modular

## Contribution

Makes "is this network modular?" a question with an answer. The definition is
borrowed from graph clustering — **a module is a set of neurons with strong
internal connectivity and weak external connectivity** — and measured by running
spectral clustering on the weight graph of an MLP and reporting the n-cut of the
resulting partition.

The finding: training plus weight pruning produces MLPs that are **more modular
than randomly initialised ones, and often significantly more modular than random
MLPs with the same (sparse) weight distribution.**

## Key insight

The second control is the whole paper. A pruned network is sparse, and sparse
graphs cluster more easily than dense ones — so "pruned networks are modular" is
uninformative unless you compare against **a random network with the same
sparsity pattern statistics.** They do, and the effect survives.

That is the methodological point worth carrying: **when a structural property
appears after an intervention, control for the intervention's incidental
statistical effects, not just against the pre-intervention baseline.**

## Assumptions

- Graph clusterability of the weight matrix is a meaningful proxy for functional
  modularity. This is the load-bearing assumption and it is a proxy — the paper
  measures connectivity structure, not behaviour.
- MLPs on small image datasets; the architecture class is narrow by design, so
  the graph is well defined.
- Spectral clustering's partition is representative; results are checked for
  consistency across cluster counts (2-way reflected in 4-way).

## Key results

- **Trained and pruned MLPs are more modular** than random initialisation and
  than sparsity-matched random baselines.
- **Networks trained with dropout are much more modular** — a training choice
  with a measurable structural consequence.
- Results reported across models trained with and without dropout (10 each in
  one comparison), with notable **spread in n-cut values on CIFAR-10**.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Modularity is measurable in a weight graph via spectral clustering | strong | the method |
| C2 | Trained+pruned MLPs are more modular than sparsity-matched random ones | strong | the controlled comparison |
| C3 | Dropout increases modularity | moderate | measured across a small set of models |
| C4 | Graph clusterability corresponds to functional modularity | **weak — assumed** | not tested here |

## Method

Train MLPs on small image datasets, with and without dropout. Prune. Build the
weight graph. Spectral-cluster it and compute the n-cut. Compare against random
initialisation and against random networks matched on the sparse weight
distribution.

## Concepts

- **Modularity as graph clusterability** — a definition that makes the question
  empirical.
- **The sparsity-matched control** — the reason the result is not trivial, and
  the transferable methodological move.
- **Dropout as a structural intervention** — usually justified as regularisation;
  here it has a measurable effect on connectivity structure.

## Connections

`LIT-085` (grokking), read in the same batch, is the other paper here that
inspects weights rather than behaviour — and it goes further, recovering the
*algorithm* rather than a structural statistic. Read together they mark the two
levels mechanistic work operates at: **structure you can measure without knowing
what the network computes, and structure you can only see once you do.**

C4 is the gap between them: this paper measures connectivity and hopes it means
function; `LIT-085` establishes function directly, for a much smaller problem.

## Recommendations

- **R1** — When an intervention produces a structural property, control against
  a random baseline matched on the intervention's incidental statistics.
  *Topic:* analysis and evaluation. *Strength:* strong, and general.
- **R2** — Treat graph clusterability as a proxy and say so; connectivity is not
  function. *Strength:* strong.
- **R3** — Regularisers may have structural effects worth measuring, not only
  generalisation effects. *Strength:* weak — C3 is one observation on small MLPs.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice**, and the
document is `Superseded` — correctly. Interpretability moved to
mechanistic circuit-level work on transformers, of which `LIT-085` is a small
example, and a connectivity statistic on pruned MLPs is not where that went.

The reading does not argue with the status. What it records is that R1 is the
part worth keeping: the sparsity-matched control is why this paper's result is
not an artefact, and it is the kind of control that structural claims about
networks routinely omit.

The document's takeaways include two that the paper does not support.
**"Feature disentanglement"** is not measured — the paper measures connectivity,
not features — and **"impact on generalization"** is not studied at all; no
generalization claim appears. That is two of four bullets asserting results the
paper does not contain.

## Limitations

- Small MLPs on small images, 2020.
- C4 is assumed throughout and is the claim everything else would need.
- C3 rests on a small number of models with a large spread on CIFAR-10.
- Spectral clustering imposes a partition whether or not one exists; the paper's
  controls address this and do not eliminate it.

## Open questions

- Does weight-graph modularity predict anything behavioural? The paper's own
  framing invites the question and does not test it, and that gap is why the
  line was superseded rather than extended.
