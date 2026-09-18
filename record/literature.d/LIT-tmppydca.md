---
status: Active
title: 'Qwen2.5 Technical Report'
version: 1
tags:
- model-architecture
date: '2026-09-18'
published: '2024-12-19'
arxiv: '2412.15115'
first_author: 'Qwen'
keywords:
- 'model-report'
- 'open-weights'
- 'baseline'
implementations:
- 'Qwen2.5'
summary: >-
  Qwen Team (2024), [ARXIV-2412.15115](https://arxiv.org/abs/2412.15115). The open-weight family this record
  measures against more than any other — forty-five documents here name it,
  and until now none of them could point at it.
---

# LIT-tmppydca: Qwen2.5 Technical Report

Qwen Team (2024) — [ARXIV-2412.15115](https://arxiv.org/abs/2412.15115)

## Key takeaways

- The Qwen2.5 family, open-weight across a wide size range, which is what
  makes it the default base for method papers that need a model they can
  fine-tune, perturb or run evolution strategies over
- Filed for what it **is**, not for what it recommends: when a result here
  says "Qwen2.5-7B", this is the document that says which model that was

## Standing in the anthology

**Carries no practice, deliberately** — `ADR-032`. A model report is
admissible for what it establishes; this one establishes an identity, and the
identity is the thing forty-five documents in this record have been assuming.

**The incumbent shape, for the third time this week.** The record already held
`LIT-182` (Qwen3), `LIT-135` (Qwen3.8) and `LIT-125` (Qwen2.5-Coder) — the
successors and a sibling — and not the base model they and everyone else
measure against. Same pattern as DoReMi behind the mixing laws, and DCLM
behind the filtering practices: the thing that becomes everybody's baseline
gets cited constantly and filed never, because nobody encounters it as news.

Unread — no `NOTE`. `ADR-025` makes that mean exactly what it says, and for a
model report the identity is what the record needed.
