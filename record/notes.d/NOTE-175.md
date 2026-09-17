---
number: 175
status: Read
formerly:
- NOTE-tmpu2o31
paper: LIT-391
title: 'DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining'
version: 1
date: '2026-09-17'
summary: >-
  A 280M proxy under group DRO sets the domain weights for an 8B run: +6.5
  points few-shot and the baseline in 2.6x fewer steps, with no downstream
  task in the loop. The transferable part is the objective — worst-case
  EXCESS loss against a reference model, because worst-case raw loss would
  upweight whichever domain is noisiest.
---

# NOTE-175: DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining

<!-- inactive-ok-file: SOTA-166 — Proposed, the practice this one is measured against here -->

Read from [LIT-391](../literature.d/LIT-391.md) — [ARXIV-2305.10429](https://arxiv.org/abs/2305.10429).

## The objective is the paper

The method is easy to state — Group DRO over domains, minimise the worst
domain — and stated that way it does not work. The paper says why, and this is
the sentence worth keeping:

> a naive worst-case approach would upweight the domains with the most noisy
> data, as every domain has a different optimal loss (aka, the entropy)

Minimising worst-case *loss* rewards whichever domain is hardest, and the
hardest domain is usually the one with the most irreducible noise. A mixture
optimised that way spends its budget on text nobody can predict.

The fix is a subtraction: optimise worst-case **excess loss**, the gap between
the model under evaluation and a pretrained reference model. That converts
"which domain is hard" into "which domain has headroom left", which is the
quantity a mixture should actually chase.

**The reference model exists only to supply that subtraction**, which is why
the method has three steps rather than two. Reading the pipeline without the
objective makes the first step look like overhead; it is the thing that makes
the second step mean anything.

## What transfers past data mixing

The pattern is general and the record meets it elsewhere: **a worst-case
objective over heterogeneous groups will select for irreducible difficulty
unless you subtract a per-group baseline.** Any minimax formulation over
domains, tasks, users or languages has the same failure mode, and the same
remedy.

That makes this more than a data-mixing paper for a record that is mostly
about language models — the mixing result is the instance, the baseline
subtraction is the lesson.

## The results, and one caveat the paper supplies itself

280M proxy, 8B target — a 30x transfer. +6.5 points average few-shot
downstream accuracy over The Pile's default weights, baseline accuracy in
**2.6x fewer steps**. On GLaM the task-agnostic weights match weights that
were tuned on downstream tasks, which is the most surprising number in the
paper: not knowing the target cost nothing.

"Improves perplexity across all domains, even when it downweights a domain"
is the claim most likely to be over-generalised, and the authors evidently
thought so too — there is an appendix constructing a simple example where
reweighting has no trade-off. That it needs constructing is the signal: the
no-trade-off case is a property of particular domain structures, not a general
guarantee, and a reader should not expect downweighting to be free in an
arbitrary corpus.

## What this does to the record

Sources [SOTA-238](../practices.d/SOTA-238.md).

The record already held [SOTA-166](../practices.d/SOTA-166.md) — set proportions by fitting a mixing law on
small runs, from a 2024 paper — and not this one, from 2023, which that
literature measures itself against. The successor was filed and the incumbent
was not, which is a quieter version of the trunk problem: not a technique
nobody wrote down, but one that arrived early enough to become the baseline
everyone assumes.

They are not rivals so much as different instruments, and the practice says
which to reach for: a mixing law gives you a *predictor* over mixtures, so you
can optimise it for any target you can name; this gives you one *weighting*,
robustly, without naming a target at all.
