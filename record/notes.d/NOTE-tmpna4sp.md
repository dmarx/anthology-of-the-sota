---
status: Read
paper: LIT-tmpc4fk2
title: 'Emergent Abilities'
version: 1
date: '2026-09-21'
summary: >-
  The paper that named the phenomenon, read for what it actually argues rather
  than what it is cited for. It raises the metric explanation itself, in §5.1,
  and declines it on two grounds — one of which was later answered and one of
  which still stands.
---

# NOTE-tmpna4sp: Emergent Abilities

## Contribution

A definition and a survey, not an experiment. Before it, "scaling helps" was
a smooth story told with cross-entropy curves; after it, the field had a name
for the tasks where the downstream curve is flat and then is not, and a claim
that those tasks are *unpredictable* from below. What is true afterwards that
was not before: the discontinuity was collected into one object with a
definition you can test, which is also what made it falsifiable.

## Key insight

The definition is the contribution, and it is narrower than the word.
*Emergent* here means only "absent in smaller models, present in larger ones,
and therefore not extrapolable" — not "novel kind of computation", not
"qualitatively new capacity". Every later argument about whether emergence is
real is an argument about curves under that definition, which is why a paper
about *metrics* could engage it at all.

## Assumptions

- **Scale is training FLOPs**, with parameters in an appendix. Justified by
  dense Transformer families scaling the two together, which the paper itself
  notes fails for Chinchilla vs Gopher and for sparse mixtures.
- **Every curve comes from prior work.** No controlled comparison is run here,
  so the metric on each curve is whatever the original authors chose.
- **Tasks have a chance baseline.** "Near-random until a threshold" needs a
  floor; the definition does not apply to tasks without one.
- **Scale thresholds are not properties of abilities.** Stated explicitly —
  better data moves the threshold, and emergence "should probably be viewed
  as a function of many correlated variables".

## Key results

- Eight few-shot emergent abilities across five model families (Fig. 2):
  BIG-Bench arithmetic, IPA transliteration, word unscrambling, Persian QA,
  TruthfulQA, grounded conceptual mappings, MMLU, Word in Context.
- BIG-Bench arithmetic jumps at ~13B for GPT-3 and ~68B for LaMDA.
- MMLU is at chance for ≤10B across GPT-3, Gopher and Chinchilla, and above
  chance at 70B–280B.
- WiC is not cleared by GPT-3 at 175B nor by Chinchilla, and is cleared by
  PaLM at 540B.
- §4: prompting and finetuning strategies — chain of thought among them — are
  flat or harmful below a scale and help above it.
- App. A: cross-entropy improves smoothly on six emergent BIG-Bench tasks
  while exact match, BLEU and accuracy sit at chance.

## Claims

The load-bearing claim is the negative one: these curves **cannot be
predicted by extrapolating smaller models**. Everything about risk,
forecasting and "what else might emerge" rests on that, and it is a claim
about predictability rather than about mechanism. The paper is careful never
to assert a mechanism; §5.1 opens by saying there are "few compelling
explanations".

## Method

Collection and replotting of published results on a log-FLOPs axis, plus one
original analysis (cross-entropy on six BIG-Bench tasks) that the authors run
against their own thesis.

## Concepts

*Emergent ability*; *phase transition* borrowed from Huberman & Hogg;
*augmented prompting strategy* for techniques that only pay above a scale.

## Connections

- [LIT-077](../literature.d/LIT-077.md) is both the source of four of the eight curves and the
  origin of the metric objection the paper answers in §5.1.
- [LIT-tmpgnhq2](../literature.d/LIT-tmpgnhq2.md) is the direct reply, three years of citation later.
- §4's chain-of-thought discussion is the scale condition that
  [SOTA-279](../practices.d/SOTA-279.md) and its descendants carry; this paper is where
  "flat or harmful below ~100B" comes from as a general shape rather than a
  CoT-specific finding.

## Bearing on the record

It closes a citation gap rather than adding a practice. [SOTA-200](../practices.d/SOTA-200.md) told
readers to check emergence claims for metric artefacts while the record held
neither the emergence claim nor its rebuttal — so the practice was
recommending a check against a target the record could not name.

Reading it also corrects the shape of the dispute. The popular version is
"Wei said emergence, Schaeffer said metrics". The actual version is that Wei
et al. raised metrics, tested cross-entropy, and gave two reasons to think it
insufficient — so the reply is not a discovery of an overlooked confound but
an answer to one of two stated objections.

## Limitations

**It is a survey with a definition, and survey evidence cannot separate the
phenomenon from the instrument.** Eight curves drawn from eight papers under
eight authors' metric choices are not eight independent tests; if the metric
is the common cause, the count is one observation repeated.

**The unpredictability claim is the weakest link and the most cited.** It is
established by noting that nobody predicted these thresholds, which is
compatible with the thresholds being artefacts of what was plotted.

## Open questions

- The intermediate-step objection (§5.1, reason one) has not been answered by
  anyone: if final-answer accuracy is a metric artefact, why does the quality
  of intermediate reasoning steps also jump? Answering it needs a
  partial-credit measure over traces, and the record has reasons
  ([SOTA-278](../practices.d/SOTA-278.md)) to distrust reading traces as explanations at all.
- Whether any of the eight curves survives rescoring under a continuous
  metric. [LIT-tmpgnhq2](../literature.d/LIT-tmpgnhq2.md) rescored two arithmetic tasks and LaMDA's
  multiple-choice tasks; the other families were never published in a form
  that allows it.
