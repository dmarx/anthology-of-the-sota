---
status: Read
paper: LIT-tmpglf4i
title: 'Zero-Shot CoT'
version: 1
date: '2026-09-21'
summary: >-
  One fixed sentence, no exemplars, twelve datasets. Reading it: the ordering
  is the practical content — it loses to hand-written few-shot chains and
  beats eight-shot standard prompting, so it is the baseline to try first
  rather than the method to settle on.
---

<!-- inactive-ok-file: ADR-050 — Proposed, and named as the decision that created the topic this reading is filed under, which is a fact about the filing rather than a claim resting on the decision -->
# NOTE-tmpsi60o: Zero-Shot CoT

## Contribution

Few-shot chain of thought needs step-by-step exemplars written per task. This
shows that a *single task-agnostic sentence* recovers much of the effect with
no exemplars at all, across arithmetic, commonsense, symbolic and logical
reasoning. What is true afterwards that was not before: the reasoning
capability is reachable without demonstrations, so the exemplars were
eliciting something already present rather than teaching it.

## Key insight

The demonstrations in few-shot CoT were doing two jobs — showing the *format*
and showing the *task*. Separate them and it turns out the format instruction
alone carries most of the weight. "Let's think step by step" is not teaching
arithmetic; it is selecting a mode the model already has.

## Assumptions

- **Two-stage prompting.** Reasoning extraction, then answer extraction from
  the generated trace. Not one call, and the second stage is what makes the
  output parseable.
- **Sufficient scale.** Flat or harmful below roughly 100B, the same
  threshold as its parent.
- **Instruction-tuned models carry the headline.** text-davinci-002 is used
  unless stated otherwise; the effect is also shown on original GPT-3 and
  PaLM.
- **Answer-extraction prompts are task-format-specific** (multiple choice vs
  free numeric), which is a small piece of per-task engineering the "single
  prompt" framing understates.

## Key results

- **MultiArith 17.7 → 78.7, GSM8K 10.4 → 40.7** on text-davinci-002, against
  zero-shot prompting.
- **Underperforms Few-shot-CoT**, stated explicitly, and **outperforms
  standard Few-shot prompting with eight examples per task**. That pair of
  facts is the finding with practical consequences.
- **Scale dependence** — flat curves without chain of thought, sharply rising
  with it, for Original/Instruct GPT-3 and PaLM. 17 models, 0.3B to 540B.
- **Error analysis** — on CommonsenseQA the model often produces correct
  reasoning and then a wrong selection, or refuses to narrow to one option.
  So the errors are not all reasoning errors.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A single task-agnostic trigger substantially improves zero-shot reasoning | strong | 12 datasets, 4 categories, large margins, multiple model families |
| C2 | It underperforms hand-written few-shot chains | strong | direct comparison against Wei et al.'s numbers |
| C3 | It beats eight-shot standard prompting | strong | same comparison |
| C4 | The ability is emergent at scale | moderate | measured on 2022-era models; the same brittle-metric caution as its parent applies |
| C5 | The capability was latent rather than taught | moderate | an interpretation of C1, and the paper's own framing |

## Method

Append the trigger to the question, sample a reasoning trace, then append an
answer-extraction prompt to the trace and sample again. Nothing else.

## Concepts

- **Zero-shot-CoT** — chain of thought elicited by instruction rather than
  demonstration.
- **Trigger sentence** — the fixed task-agnostic instruction.

## Connections

Directly modifies [LIT-467](../literature.d/LIT-467.md) by removing its exemplars, declared as
`extends`. The paper is candid that Reynolds and McDonell had proposed a
similar trigger and distinguishes itself on being task-agnostic and
quantitatively evaluated.

## Bearing on the record

- **It produces [SOTA-tmpi7boj](../practices.d/SOTA-tmpi7boj.md)**, which is a claim about what to try
  *first* rather than what is best — an ordering, which is what C2 and C3
  together license and all they license.
- **It sharpens [SOTA-279](../practices.d/SOTA-279.md)'s conditions.** That practice says to write
  worked steps into the exemplars; this says measure the free version before
  paying for the exemplars, because on many tasks the difference will not
  justify the labour.
- **It lands in `in-context-learning`**, the topic added in `ADR-050`, and is
  the first document filed there after the vocabulary change rather than
  retagged into it.

## Limitations

- **Underperforms few-shot CoT**, which the practice has to carry.
- **2022 models**, and the scale threshold is a fact about that generation.
- **The "single prompt" claim is slightly stronger than the method**, given
  the format-dependent answer-extraction stage.
- **No cost accounting** — two generation calls per question rather than one.
- **Whether the model is reasoning is not addressed**, consistent with its
  parent.

## Open questions

- Is the threshold still ~100B for models trained on more data with better
  recipes, and is the whole effect now absorbed by instruction tuning that
  emits traces unprompted?
- How much of the remaining gap to few-shot CoT is format and how much is
  task information?
