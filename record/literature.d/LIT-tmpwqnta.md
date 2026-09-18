---
status: Active
title: 'Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-18'
published: '2018-03-14'
arxiv: '1803.05457'
first_author: 'Clark'
keywords:
- 'benchmark'
- 'question-answering'
- 'ai2-arc'
implementations:
- 'ARC-Easy'
- 'ARC-Challenge'
summary: >-
  Clark et al. (2018), [ARXIV-1803.05457](https://arxiv.org/abs/1803.05457). Grade-school science questions split
  into an Easy set and a Challenge set, the latter selected because retrieval
  and word-co-occurrence baselines both fail on it. The "ARC" that appears in
  this record's evaluation suites — and not the one SOTA-235 reports on.
---

# LIT-tmpwqnta: Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge

Clark et al. (2018) — [ARXIV-1803.05457](https://arxiv.org/abs/1803.05457)

## Key takeaways

- Multiple-choice grade-school science questions, partitioned into **ARC-Easy**
  and **ARC-Challenge**, where the Challenge split is defined by what *fails*
  on it: questions both a retrieval baseline and a word-co-occurrence baseline
  answer incorrectly
- Defining a split by baseline failure is the design decision worth noting —
  it makes the Challenge set adversarial to two specific strategies, which is
  narrower and more honest than "hard questions"
- A standard member of the zero-shot evaluation suite, which is how it appears
  here: alongside HellaSwag, PIQA, WinoGrande and LAMBADA rather than on its
  own

## Standing in the anthology

**Carries no practice, deliberately** — `ADR-032`.

<!-- inactive-ok-block: THEORY-007 — Proposed, and cited only as a place the record
     uses `ARC-C` in the AI2 sense. The disambiguation holds whatever that
     explanation's status settles at. -->
**Filed to separate two benchmarks this record was calling by one name.** Ten
documents here write `ARC-Easy` or `ARC-Challenge` and mean this paper —
`THEORY-007` measures across `ARC-C`, `LIT-184` names it beside MMLU as a
target FineWeb-Edu moves. Twelve others write a bare `ARC`, and at least two
of those — `SOTA-235` and `LIT-379` — mean `LIT-tmpnraor`, Chollet's puzzle
benchmark, which shares nothing with this but four letters.

Nothing in the record distinguished them until now, which matters because a
result is only as legible as what it was measured on: "6× a fine-tuned
baseline on ARC" and "ARC-C rises with model scale" are claims about different
objects.

Unread — no `NOTE`.
