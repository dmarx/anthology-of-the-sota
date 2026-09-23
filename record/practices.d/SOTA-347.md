---
number: 347
status: Proposed
formerly:
- SOTA-tmp2nfwy
promote_when: >-
  An evaluation on current models showing mass weight edits propagate to
  the edited facts' implications (RippleEdits or similar) at least as well
  as in-context or retrieval-based editing, with neighborhood damage
  reported at the number of edits used.
title: 'To write many facts into a model''s weights, update a range of early-to-mid MLP layers jointly in one batched solve (MEMIT), choosing the range by measured edit success rather than causal tracing'
version: 1
tags:
- adaptation-and-tuning
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-576
- LIT-574
introduced_by:
- LIT-576
consensus: contested
contested_by:
- LIT-577
consensus_note: >-
  MEMIT is the standard mass-editing baseline. RippleEdits shows that it,
  like other weight editors, updates the edited triple without its
  implications, and that stating the fact in context does better. Whether
  weight editing should be used for knowledge updates at all is the open
  question.
implementations:
- memit
summary: >-
  Meng et al. (2023), [LIT-576](../literature.d/LIT-576.md) — sequential single-fact edits collapse
  after tens of facts (ROME scores 50.3 at 10,000). Distributing each update
  over a range of MLP layers in one least-squares solve holds 85.8 on GPT-J,
  with neighborhood success falling from 83.5 to 73.7. Choose the layers by
  editing performance: per-fact causal tracing does not predict it
  ([LIT-574](../literature.d/LIT-574.md)). Evaluate implications too, because weight editors fail
  them ([LIT-577](../literature.d/LIT-577.md)).
---

# SOTA-347: To write many facts into a model's weights, update a range of early-to-mid MLP layers jointly in one batched solve (MEMIT), choosing the range by measured edit success rather than causal tracing

## Source

Meng et al. (2023), [LIT-576](../literature.d/LIT-576.md), read as [NOTE-316](../notes.d/NOTE-316.md). Hase et al.
(2023), [LIT-574](../literature.d/LIT-574.md), for how to choose layers.

## The practice

If you must edit facts into weights, for example without control over the
prompt at inference:

- **Batch the edits and spread them over several layers.** ROME-style
  single-layer rank-one edits interfere past about 10–30 facts. MEMIT's
  joint solve held up to 10,000 on GPT-J and GPT-NeoX-20B
- **Choose the layer range by editing results.** Sweep edit success,
  paraphrase and neighborhood scores over candidate ranges on held-out
  edits. Do not use a per-fact tracing peak
- **Measure neighborhood damage at the edit count you use.** It grows with
  the number of edits, and at 10,000 it cost about 10 points of
  neighborhood success (83.5 to 73.7)
- **Test implications, not just recall** ([SOTA-348](SOTA-348.md))

## Conditions

- **Contested as a way to update knowledge.** On RippleEdits, weight
  editors average 38–66, and in-context editing beats them
- **Directional facts**, on GPT-J and GPT-NeoX-class models with ungated
  MLPs
