---
number: 313
status: Read
formerly:
- NOTE-tmpceyj8
paper: LIT-574
title: 'Does Localization Inform Editing?'
version: 1
date: '2026-09-23'
summary: >-
  Per fact, causal tracing's localization is unrelated to where an edit
  succeeds. The edit layer explains 94.7% of the variance in ROME's success
  on GPT-J, and tracing adds 0.1%. Main text read, robustness appendices
  skimmed.
---

# NOTE-313: Does Localization Inform Editing?

## Contribution

A direct test of the premise behind ROME and MEMIT: that you should edit a
fact where it is stored.

## Key insight

**Where information is, and where a change is easiest to write, are
different questions.** Early-to-mid MLP edits work for facts that tracing
places anywhere.

## Key results

- 652 GPT-J facts: tracing peaks spread over layers, many at 1–3 and 16–20
- ROME rewrite score 99% at layer 6, and above 96% at all but the last layer
- Rewrite score vs tracing effect: ρ = −0.13. R² 94.7% from layer alone,
  94.8% with tracing added
- Only Fact Forcing, which mirrors tracing's noised input, shows a relation,
  and the layer still dominates there

## Limitations

- **Mostly GPT-J on CounterFact**, with robustness checks on GPT-2 XL and
  zsRE
- **Explains the non-relation without explaining why mid layers work.** §6
  offers a hypothesis
- **About causal tracing.** Other localization methods are checked in the
  appendix, not exhaustively
