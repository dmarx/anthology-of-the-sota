---
number: 315
status: Read
formerly:
- NOTE-tmpicaci
paper: LIT-578
title: 'ROME'
version: 1
date: '2026-09-23'
summary: >-
  Causal tracing localizes factual recall to mid-layer MLPs at the last
  subject token, and a rank-one MLP edit there rewrites single facts with
  both generalization and specificity. Main text and the CounterFact
  appendix read.
---

# NOTE-315: ROME

## Contribution

A localization method (causal tracing), an editing method (rank-one
update), and a benchmark (CounterFact) that measures generalization and
specificity together.

## Key insight

**If an MLP is a linear associative memory, one fact is one key-value pair,
and inserting it is a closed-form rank-one update** that minimally disturbs
other keys.

## Key results

- CounterFact Score: ROME 89.2 (GPT-2 XL) and 91.5 (GPT-J). The best
  baseline is 66.9 on GPT-2 XL (FT+L) and 68.7 on GPT-J (FT+L)
- Fine-tuning reaches full efficacy but destroys neighbors on GPT-J
  (NS 10.3, against 83.0 unedited)
- The edit works best at the last subject token in middle layers
  (Figure 5)

## Limitations

- **One fact per edit, and directional**, as §3.7 says
- **Neighborhood success falls** below the unedited model's on both models
- **The edit layer comes from tracing averaged over facts.** Whether the
  average tells you anything about a given fact is the question Hase et al.
  answer: it doesn't ([LIT-574](../literature.d/LIT-574.md))
