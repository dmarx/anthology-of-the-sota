---
status: Rejected
status_note: per-fact causal-tracing localization explains 0.1% of the variance in edit success once the edit layer is accounted for, and edits succeed at layers tracing does not point to
title: 'Causal tracing shows where a language model stores a fact, and that is where the fact should be edited'
version: 1
tags:
- analysis-and-evaluation
- adaptation-and-tuning
date: '2026-09-23'
source:
- LIT-tmpvij69
- LIT-tmp6e8di
summary: >-
  Meng et al. (2022), [LIT-tmpvij69](../literature.d/LIT-tmpvij69.md) — tracing puts factual recall in mid-layer
  MLPs at the last subject token, and ROME and MEMIT edit there on that
  basis. Hase et al. (2023), [LIT-tmp6e8di](../literature.d/LIT-tmp6e8di.md), test the link per fact on GPT-J.
  Tracing peaks are spread across layers, while edits succeed at layer 6
  for almost everything. The edit layer explains 94.7% of the variance in
  success and tracing 0.1% more. The editors work. The reason given for
  where they edit does not hold.
---

# THEORY-tmpde7eo: Causal tracing shows where a language model stores a fact, and that is where the fact should be edited

## Source

Meng et al. (2022), [LIT-tmpvij69](../literature.d/LIT-tmpvij69.md), read as [NOTE-tmpicaci](../notes.d/NOTE-tmpicaci.md), for the account.
Hase et al. (2023), [LIT-tmp6e8di](../literature.d/LIT-tmp6e8di.md), read as [NOTE-tmpceyj8](../notes.d/NOTE-tmpceyj8.md), for why it is
filed already retired ([DP-003](../../docs/design-principles.md#dp-3)).

## The account

Localize, then edit. Causal tracing finds the hidden states whose clean
values restore a corrupted fact, and those states concentrate in mid-layer
MLP outputs at the last subject token. If that is where the association
lives, that is where a rank-one or batched update should go. ROME chose its
layer from tracing averaged over facts, and MEMIT chose its layer range
from the same analysis.

## Why it is rejected

- **Per fact, tracing and edit success are unrelated.** ρ = −0.13 between a
  fact's tracing effect at the edit layer and its rewrite score
- **The layer, not the localization, predicts success.** R² 94.7% from the
  layer alone, and 94.8% with tracing added
- **Edits succeed where tracing does not point.** Many facts trace to
  layers 1–3 or 16–20, and editing them at layer 6 still works
- **It is robust:** MEMIT and fine-tuning show the same, and so do other
  metrics, GPT-2 XL and zsRE

## What survives

The editing methods (MEMIT is [SOTA-tmp2nfwy](../practices.d/SOTA-tmp2nfwy.md)), and causal tracing as a
description of where information flows. What does not survive is using one
to choose the other. Pick the edit layers by measured editing performance.
<!-- inactive-ok-file: SOTA-tmp2nfwy — Proposed and contested, cited as the editing method that survives this account's rejection -->
