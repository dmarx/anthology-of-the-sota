---
status: Active
title: 'HellaSwag: Can a Machine Really Finish Your Sentence?'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-18'
published: '2019-05-19'
arxiv: '1905.07830'
first_author: 'Zellers'
keywords:
- 'benchmark'
- 'commonsense'
- 'adversarial-filtering'
implementations:
- 'HellaSwag'
summary: >-
  Zellers et al. (2019), [ARXIV-1905.07830](https://arxiv.org/abs/1905.07830). Commonsense sentence completion whose
  wrong answers are generated and then filtered against the models of the day
  until those models fail — so the benchmark's difficulty is defined relative
  to a specific generation of systems, which is the caveat to carry.
---

# LIT-tmpn6zv1: HellaSwag: Can a Machine Really Finish Your Sentence?

Zellers et al. (2019) — [ARXIV-1905.07830](https://arxiv.org/abs/1905.07830)

## Key takeaways

- Multiple-choice completion of a short context, where the distractors are
  **machine-generated and adversarially filtered**: candidates are kept
  precisely when contemporary models rank them plausibly and humans do not
- **The difficulty is therefore relative to the discriminator used to build
  it.** That is the property to hold onto when reading a HellaSwag number
  today: the set was constructed to be hard for 2019's models, and later
  models were not what it was filtered against
- Fifteen documents in this record report on it, almost always as one member
  of a zero-shot suite rather than as a headline

## Standing in the anthology

**Carries no practice, deliberately** — `ADR-032`.

What it earns its place for is the caveat above, which is the shape `#137`
asks a benchmark note to supply: what the benchmark measures, and what it is
insensitive to. An adversarially filtered benchmark ages differently from a
sampled one — its discriminating range is tied to the models used in its
construction — and this record reports HellaSwag numbers across a seven-year
span of systems without anywhere to say so.

`NOTE-082` is the nearest live use: HellaSwag declining as Countdown training
continues past convergence, which is a claim about forgetting measured on this
instrument.

Unread — no `NOTE`.
