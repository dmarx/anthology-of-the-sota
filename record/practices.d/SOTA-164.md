---
number: 164
status: Active
formerly:
- SOTA-tmpkwpaw
consensus: universal
consensus_note: >-
  Every pipeline this record describes deduplicates, and none argues for it —
  Falcon-H1-Tiny, Kimi K3 and DeepSeek-V4 all do it as a matter of course,
  and Olmo 3 cites this paper for it. Not doing it is what would need
  justifying, which is the definition of the value.
title: 'Deduplicate the pretraining corpus at both substring and document granularity before training on it'
version: 1
tags:
- data-pipeline
date: '2026-09-08'
published: '2021-07-01'
source:
# The paper that measured it. Everything else in the record deduplicates
# without reporting what it bought, which is adoption and belongs in
# consensus_note rather than here (ADR-017).
- LIT-202
implementations: []
summary: >-
  Lee et al. (2021), [LIT-202](../literature.d/LIT-202.md) — a single 61-word sentence appears thousands of
  times in C4. Deduplicating cuts verbatim emission about tenfold, reaches
  equal or better accuracy in fewer steps, and removes train-test
  contamination from standard validation sets. Two granularities, because a
  repeated boilerplate paragraph is not a duplicated document.
---

# SOTA-164: Deduplicate the pretraining corpus at both substring and document granularity before training on it

## Source

Lee et al., Google Research (2021), [LIT-202](../literature.d/LIT-202.md) — [ARXIV-2107.06499](https://arxiv.org/abs/2107.06499).

Run two passes, because they catch different things:

- **Exact substring matching**, which finds long repeated spans wherever they
  sit — the paper's example is one 61-word English sentence appearing
  thousands of times in C4.
- **Approximate near-duplicate detection at document granularity**, which
  finds documents that are the same page with different boilerplate.

A repeated paragraph is not a duplicated document, and a pipeline that runs
only one of the two passes leaves the other failure mode in the corpus.

## What it buys, which is three things usually conflated into one

- **Memorisation.** Deduplicated models emit memorised training text about
  **ten times** less frequently in unprompted generation.
- **Efficiency.** They reach the same or better accuracy in **fewer training
  steps**.
- **Honest evaluation.** Train-test overlap contaminates a large fraction of
  the validation sets of standard datasets, so the numbers mean more
  afterwards.

Only the second is an efficiency argument. A pipeline that deduplicates for
speed alone and stops when the speed-up looks small has given up the other
two without noticing.

## Filed late, and the reason is worth keeping

<!-- inactive-ok-block: SOTA-124 — Proposed, and this practice is the other
     end of the axis it argues about -->
This was in every pipeline the record describes before it was in the record.
A step nobody argues about produces no debate to notice, which is a different
way of going unrecorded from a technique that is too new to endorse — and the
registry was missing nodes at both ends. Its practical consequence is
[SOTA-124](SOTA-124.md), which says when *deliberate* repetition of good data is safe;
this is the paper establishing that repetition is not free by default, and
that the damage shows up as verbatim emission rather than as loss.

## Known implementations

- Falcon-H1-Tiny, Kimi K3, DeepSeek-V4, Olmo 3 — and, so far as the record
  can tell, everything else.
