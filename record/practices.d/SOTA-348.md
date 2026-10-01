---
number: 348
status: Active
formerly:
- SOTA-tmprsfsm
title: 'Evaluate a knowledge edit on the facts it implies — logical consequences, multi-hop compositions, aliases and the subject''s other facts — not only on the edited prompt, its paraphrases and unrelated neighbours'
version: 1
tags:
- analysis-and-evaluation
- adaptation-and-tuning
date: '2026-09-23'
source:
- LIT-577
introduced_by:
- LIT-577
consensus: unreplicated
consensus_note: >-
  One group's benchmark. Its central observation, that editors update the
  queried triple and not its consequences, holds across three editors and
  four models. Other multi-hop editing benchmarks exist, and how widely
  editing papers now report ripple metrics has not been assessed here.
implementations: []
summary: >-
  Cohen et al. (2023), [LIT-577](../literature.d/LIT-577.md) — the standard edit metrics (efficacy,
  paraphrase, neighborhood) cannot see whether an edit changed what the
  model knows or only what it says to one question. On six ripple criteria,
  ROME, MEMIT and MEND average 38–66, and logical generalization falls as low
  as 5.5. Prompting with the new fact scores 81–83 on LLaMA-7B. Report
  ripple metrics beside the standard ones, and compare against in-context
  editing.
---

# SOTA-348: Evaluate a knowledge edit on the facts it implies — logical consequences, multi-hop compositions, aliases and the subject's other facts — not only on the edited prompt, its paraphrases and unrelated neighbours

## Source

Cohen et al. (2023), [LIT-577](../literature.d/LIT-577.md). Read as [NOTE-314](../notes.d/NOTE-314.md).

## The practice

Cohen et al. introduced this evaluation in [LIT-577](../literature.d/LIT-577.md), with RippleEdits, a
benchmark of six criteria for what an edit should change besides the queried
triple. Measured there, ROME, MEMIT and MEND average 38–66 across subsets and
models. Logical generalization falls to 5.5–7.0 on the POPULAR subset for
GPT-2 and GPT-J while subject aliasing scores 86–100, and in-context editing
averages 81–83 on LLaMA-7B against ROME's 49–61. The first bullet answers the
gap between aliases and consequences, and the third is the in-context result.

- **Test the consequences.** For an edit (s, r, o → o′), query relations
  implied by it (inverse and symmetric relations), two-hop questions that
  pass through o′, the subject under its aliases, and s's other facts,
  which should be unchanged
- **Filter to what the model knew before**, so a failure is the edit's and
  not ignorance
- **Include an in-context baseline.** Put the new fact in the prompt and
  score it on the same queries. On RippleEdits it beat every weight editor

## Conditions

- **Template-generated queries from Wikidata**, scored by alias match
- **The in-context baseline needs control of the prompt.** It is a
  benchmark reference, and the right production choice only where that
  control exists
