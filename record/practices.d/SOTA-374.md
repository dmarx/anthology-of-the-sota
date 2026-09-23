---
number: 374
status: Active
formerly:
- SOTA-tmpt56rt
title: 'When learning embeddings from co-occurrence, subsample very frequent tokens, discarding each occurrence with probability 1 − √(t/f) with t around 10⁻⁵'
version: 4
history:
- version: 2
  date: '2026-09-23'
  note: >-
    Marked contested: an independent ablation (LIT-607) finds it helps
    similarity and costs 4-12 points on analogies. Status unchanged.
- version: 3
  date: '2026-09-23'
  note: >-
    Adds Baroni et al. (LIT-608), whose best CBOW configurations all
    subsample. Still contested.
- version: 4
  date: '2026-09-23'
  note: >-
    Absorbs SOTA-382, the duplicate recommendation from the same paper and
    the same section, retired to this one. What came across is the mechanism
    argument and the falsifier it implies: the practice is a claim about the
    signal, so it should fail on a near-uniform unit distribution.
tags:
- data-pipeline
- representation-and-encoding
- signal-structure
date: '2026-09-23'
source:
- LIT-603
introduced_by:
- LIT-603
consensus: contested
consensus_note: >-
  The source measured it on its own method. The one independent ablation,
  LIT-607, finds it task-dependent: it helps SGNS on similarity (up to
  +2.2) and costs 4.4 to 5.4 points on analogies, and PPMI 5 to 12. Its speed
  benefit is not disputed. It became part of the standard recipe, which is
  adoption, not evidence (DP-005).
contested_by:
- LIT-607
implementations:
- word2vec
summary: >-
  Mikolov et al. (2013), [LIT-603](../literature.d/LIT-603.md) — in a Zipfian corpus, the few most
  frequent words co-occur with everything and dominate the updates while
  teaching little. Discard each occurrence of word w with probability
  1 − √(t/f(w)). This cut skip-gram training time by 2–3× and raised
  accuracy, only slightly for words (59 → 60% at NEG-5) but a lot for
  phrases (27 → 42% at NEG-15, 19 → 47% with hierarchical softmax).
---

# SOTA-374: When learning embeddings from co-occurrence, subsample very frequent tokens, discarding each occurrence with probability 1 − √(t/f) with t around 10⁻⁵

## Source

Mikolov et al. (2013), [LIT-603](../literature.d/LIT-603.md). Read as [NOTE-326](../notes.d/NOTE-326.md).

## The practice

- **Discard each occurrence of token w with probability 1 − √(t/f(w))**,
  where f is its relative frequency. Tokens rarer than t are never
  discarded, and the frequency ranking is preserved
- **Start at t ≈ 10⁻⁵** for corpora of billions of words
- **Expect speed first and accuracy second.** The run time fell by 2–3×.
  Accuracy gains are largest for rare items and phrases

## Why speed and accuracy move together, which is the unusual part

Most throughput interventions trade quality away. The argument that this one
need not: **an update spent on a very frequent token is nearly redundant with
the last thousand such updates**, so dropping it costs almost no signal, and
the budget it frees goes to tokens where each occurrence still carries
information. The speed-up and the rare-word gain have one cause.

**That is a claim about the data, not about the model**, and it comes with a
falsifier worth stating: on a signal whose units are near-uniform there is
nothing redundant to discard, and subsampling becomes plain data loss. Run
that test before assuming the practice transfers to a non-text stream.

Read the `Conditions` below against this. The mechanism argument predicts a
gain concentrated in rare items; `LIT-607` finds the gain on *similarity* and
a loss on *analogies*. Those are compatible — the argument says where the
freed budget goes, not that every downstream task rewards it — but the
argument is not evidence for the analogy case, and was never tested against
it.

**It is not vocabulary pruning.** Nothing leaves the vocabulary; occurrences
are dropped from the stream. A rare word's representation improves precisely
because its own occurrences survive while its neighbours' do not.

## Conditions

- **Word2vec-style co-occurrence training.** The rationale, that frequent
  tokens co-occur with everything, is a property of text (heavy-tailed word
  frequencies). It transfers to other embedding methods with the same
  structure, but that is not tested here
- **Gains on word analogies were small or zero with enough negatives**
  (NEG-15: 61 → 61%)
- **An independent ablation finds it hurts analogies.** [LIT-607](../literature.d/LIT-607.md) (Table
  8b), at matched tuning on 1.5B tokens: SGNS similarity +0.1 to +2.2, and
  Google and MSR analogies −4.4 and −5.4. For PPMI the analogy losses are 5.0
  and 12.2. The best SGNS configuration used subsampling on 4 of 8 tasks. Use
  it for speed, and check the task before counting on an accuracy gain
- **Baroni et al. ([LIT-608](../literature.d/LIT-608.md)) point the other way on their mix.** Every
  one of their ten best CBOW configurations, ranked across 14 benchmarks
  mostly of relatedness and categorization, uses subsampling
