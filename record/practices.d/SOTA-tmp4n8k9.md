---
status: 'Active'
title: 'Set domain weights with a small proxy model under group DRO on excess loss, then transfer them'
version: 1
tags:
- data-pipeline
consensus: converged
consensus_note: >-
  The baseline the data-mixing literature measures itself against, and the
  method later work cites when it wants a non-heuristic comparison. Not
  `universal`: most published corpora still ship heuristic weights, and the
  record's own [SOTA-166](SOTA-166.md) is a different instrument for the same decision
  rather than an endorsement of this one.
date: '2026-09-17'
source:
- LIT-tmpovhsh
introduced_by:
- LIT-tmpovhsh
implementations:
- 'DoReMi'
summary: >-
  Xie et al. (2023), [LIT-tmpovhsh](../literature.d/LIT-tmpovhsh.md) — [ARXIV-2305.10429](https://arxiv.org/abs/2305.10429). Train a small proxy under
  group DRO to produce domain weights, then resample and train the real model
  with them. Optimise worst-case EXCESS loss against a reference model, not
  worst-case loss — the naive form upweights whichever domain is noisiest,
  because every domain has a different irreducible entropy.
---

# SOTA-tmp4n8k9: Set domain weights with a small proxy model under group DRO on excess loss, then transfer them

<!-- inactive-ok-file: SOTA-166 — Proposed, and this practice's counterpart; naming it is how the record holds the choice -->

## Source

Xie et al. (2023), [LIT-tmpovhsh](../literature.d/LIT-tmpovhsh.md) — [ARXIV-2305.10429](https://arxiv.org/abs/2305.10429).

## The method

Three steps. Train a small **reference** model on the default mixture. Train a
small **proxy** under Group DRO over domains. Resample the corpus with the
resulting weights and train the model you actually wanted.

In the paper, a 280M proxy sets the weights for an 8B run — a 30x transfer —
for **+6.5 points** average few-shot downstream accuracy over The Pile's
default weights, and baseline accuracy in **2.6x fewer steps**.

## Optimise excess loss, not loss

This is the part to get right, and the naive version fails in a way that looks
like success:

> a naive worst-case approach would upweight the domains with the most noisy
> data, as every domain has a different optimal loss (aka, the entropy)

Worst-case *loss* selects for whichever domain is hardest, and the hardest
domain is usually the one with the most irreducible noise. So optimise the
**gap against a pretrained reference model** instead. That turns "which domain
is hard" into "which domain has headroom", which is the quantity a mixture
should be chasing.

**The reference model earns its step by supplying that subtraction.** Skipping
it is not a saving; it changes what is being optimised.

The general form is worth carrying past data mixing: *a worst-case objective
over heterogeneous groups selects for irreducible difficulty unless you
subtract a per-group baseline.* Any minimax over domains, tasks, languages or
users has the same failure and the same remedy.

## What it does not require

A downstream task. Weights are produced with no evaluation target in the loop
— and on GLaM they match weights that *were* tuned on downstream tasks. Not
knowing the target cost nothing there, which is the paper's most surprising
result and the reason this is usable before anyone has decided what the model
is for.

## Conditions

**Downweighting is not free in general.** "Improves perplexity across all
domains, even when it downweights a domain" is reported, and the authors
construct an appendix example of when reweighting has no trade-off — that it
needs constructing is the tell. Expect the no-trade-off case to be a property
of particular domain structures, not a guarantee for an arbitrary corpus.

The proxy must be large enough for its ranking to transfer, and the paper
evidences one gap (280M → 8B) on two corpora. Nothing here says where that
breaks.

## Against the other instrument in this record

[SOTA-166](SOTA-166.md) sets proportions by fitting a **mixing law** on small runs. Both
avoid training a model per candidate mixture, and they answer different
questions:

- A **mixing law** is a *predictor* over mixtures. It costs a set of runs to
  fit, and in exchange you can optimise for any target you can name, and
  compose with scaling laws to extrapolate.
- **This** is a *producer* of one weighting. It costs a reference and a proxy
  run, names no target, and gives you robustness rather than optimality.

Reach for the law when the target is known and worth optimising against;
reach for this when it is not, or when a defensible default is wanted before
the evaluation suite exists.
