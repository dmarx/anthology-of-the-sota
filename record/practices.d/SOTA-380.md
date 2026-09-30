---
number: 380
status: Rejected
formerly:
- SOTA-tmpcx9ae
status_note: >-
  the advantage it reports disappears when the count-based baselines get the
  design choices word2vec shipped with and every method is tuned alike
  ([LIT-607](../literature.d/LIT-607.md)): no family wins consistently. Retired with no successor. What
  replaces it is an evaluation practice, [SOTA-379](SOTA-379.md), which corrects it
title: 'Use prediction-based word vectors rather than count-based distributional vectors'
version: 1
tags:
- representation-and-encoding
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-608
introduced_by:
- LIT-608
implementations:
- word2vec
summary: >-
  Baroni, Dinu and Kruszewski (2014), [LIT-608](../literature.d/LIT-608.md) — across 14 benchmarks,
  word2vec CBOW beat PPMI, SVD and NMF count vectors almost everywhere, and
  the authors recommend "anybody interested in using DSMs" to "go for the
  predict models". Retired: [LIT-607](../literature.d/LIT-607.md) traces the gap to settings the count
  models were not given, and finds no consistent winner once they are.
corrected_by:
- SOTA-379
---

# SOTA-380: Use prediction-based word vectors rather than count-based distributional vectors

## Source

Baroni, Dinu and Kruszewski (2014), [LIT-608](../literature.d/LIT-608.md), read as [NOTE-330](../notes.d/NOTE-330.md).

## What it said

Train word vectors by predicting contexts (word2vec) rather than by counting
co-occurrences and reweighting them. On one 2.8B-token corpus and 14
lexical-semantics benchmarks, the predict models won most tasks by a wide
margin and degraded far less under bad settings.

## Why it is retired

**The comparison was not like for like.** word2vec ran with the settings its
authors had tuned: negative sampling (which shifts PMI by log k) and a
noise distribution raised to 0.75 (which smooths the context distribution).
The count models got neither. Their SVD variants also kept the singular-value
weighting, which [LIT-607](../literature.d/LIT-607.md) found costs up to 15 points.

**Equalized, the gap goes.** [LIT-607](../literature.d/LIT-607.md) ports those choices to PPMI and SVD and
tunes all methods on one corpus. SVD matches or beats skip-gram on
similarity at small windows, and no family wins consistently. Only MSR's
syntactic analogies show a large prediction advantage.

**The paper foresaw the mechanism.** The authors note that basing the
comparison on Collobert and Weston's vectors "would have reached opposite
conclusions". The conclusion was about the two configurations, not the two
families.

## What still holds

- Prediction-trained vectors are a good default. SGNS "does not
  significantly underperform in any scenario" and is the cheapest to train
  ([LIT-607](../literature.d/LIT-607.md)). That is a claim about one method, not about the family.
- Their robustness across the grid tested here is not in dispute.
