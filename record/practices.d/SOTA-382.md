---
number: 382
status: Active
formerly:
- SOTA-tmpoaohk
consensus: emerging
consensus_note: >-
  Standard wherever token frequency is Zipfian and the objective is
  predictive — it survived into the tokenizer and sampling stages of most
  text pipelines — but the record has one measurement behind it and has not
  looked for a second. `emerging` rather than `converged` on those grounds:
  what is measured is real, and the reading of how widely it is *deliberately*
  chosen rather than inherited has not been made (`DP-005`). Read as of
  2026-09.
title: 'Subsample frequent tokens: it is faster and it improves the rare ones'
version: 1
tags:
- data-pipeline
- signal-structure
date: '2026-09-23'
source:
- LIT-609
introduced_by:
- LIT-609
implementations: []
---

# SOTA-382: Subsample frequent tokens: it is faster and it improves the rare ones

## Source

Mikolov et al. (2013), [LIT-609](../literature.d/LIT-609.md) — [ARXIV-1310.4546](https://arxiv.org/abs/1310.4546), §2.3.

## The claim

Token frequency is heavy-tailed, so a predictive objective spends most of its
updates on the handful of tokens that carry the least information. **Discard
frequent tokens stochastically, at a rate that rises with frequency.**

The result the paper reports is a pair, and the pair is the point:
"significant speedup" **and** improved "accuracy of the representations of
less frequent words".

## Why both at once, which is the unusual part

Most throughput interventions trade quality away. This one does not, because
the two effects have the same cause: an update spent on a very frequent token
is nearly redundant with the last thousand such updates, so removing it costs
almost no signal — and the budget it frees goes to tokens where each
occurrence still carries information.

That is a claim about the **signal** rather than about the model. It should
hold for any heavy-tailed unit distribution and fail for a uniform one, which
is the test to run before assuming it transfers.

## Conditions

- **It is a distributional assumption, not a universal one.** On a signal
  whose units are near-uniform there is nothing redundant to discard and the
  practice becomes plain data loss.
- **The discard rate is a hyperparameter with a threshold**, and the
  behaviour at the extremes is the obvious failure: too aggressive and the
  frequent tokens are undertrained, which matters if they carry syntax you
  need.
- **Measured on skip-gram word vectors**, once, in 2013. The mechanism
  argument is general and the evidence is not.
- **Distinct from vocabulary pruning.** Nothing is removed from the
  vocabulary; occurrences are dropped from the stream. A rare word's
  representation improves precisely because its occurrences survive while its
  neighbours' do not.

## Known implementations

-
