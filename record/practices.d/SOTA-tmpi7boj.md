---
status: Active
consensus: universal
consensus_note: >-
  "Let's think step by step" is one of the most widely repeated instructions
  in the field and models are now post-trained to do it unprompted. That is
  adoption, not evidence — `DP-005` — and the evidence column holds one paper
  about 2022-era models.
title: 'Try the single step-by-step instruction before writing exemplars; it recovers most of the gain for none of the labour'
version: 1
tags:
- in-context-learning
date: '2026-09-21'
source:
- LIT-tmpglf4i
introduced_by:
- LIT-tmpglf4i
extends:
- SOTA-279
implementations: []
summary: >-
  Kojima et al. (2022), [LIT-tmpglf4i](../literature.d/LIT-tmpglf4i.md) — one fixed sentence with no
  exemplars takes MultiArith from 17.7% to 78.7% and GSM8K from 10.4% to
  40.7%. It beats eight-shot standard prompting and loses to hand-written
  few-shot chains, which is the ordering that makes it a first move.
---

# SOTA-tmpi7boj: Try the single step-by-step instruction before writing exemplars; it recovers most of the gain for none of the labour

## Source

Kojima et al. (2022), [LIT-tmpglf4i](../literature.d/LIT-tmpglf4i.md) — [ARXIV-2205.11916](https://arxiv.org/abs/2205.11916),
read as [NOTE-tmpsi60o](../notes.d/NOTE-tmpsi60o.md).

## What to do

Append a fixed, task-agnostic instruction to the question — "Let's think step
by step" is the one measured — and extract the answer from the trace it
produces. No exemplars, nothing task-specific in the trigger.

Then **measure it against the exemplars you were going to write**, because
the ordering is the point:

| approach | relative standing |
|---|---|
| few-shot chain of thought, hand-written exemplars | best |
| **zero-shot chain of thought (this)** | **middle** |
| standard eight-shot prompting | worse |
| standard zero-shot prompting | worst |

This is the cheap baseline, not the better method. [SOTA-279](../practices.d/SOTA-279.md) still
describes the stronger one. What this says is that the stronger one has a
price and you should find out what it buys on your task before paying it.

## Conditions

- **It underperforms few-shot chain of thought**, stated by the authors. Any
  reading of this practice as a replacement is wrong.
- **Same scale regime as its parent** — flat or harmful below roughly 100B on
  2022-era models. Treat the threshold as something to measure rather than a
  number to apply; small-model reasoning has moved since.
- **Two generation calls per question**, not one: reasoning extraction, then
  answer extraction. The instruction is free; the inference is not.
- **The "single prompt" claim is slightly stronger than the method.** The
  answer-extraction stage is format-dependent — multiple choice and free
  numeric need different extraction prompts — so a little per-task
  engineering survives.
- **Not all the remaining errors are reasoning errors.** On CommonsenseQA the
  model often reasons correctly and then selects wrongly, or declines to
  narrow to one option, which is a parsing and instruction-following failure
  wearing a reasoning failure's clothes.

## Relation to the neighbours

Extends [SOTA-279](../practices.d/SOTA-279.md) by removing its exemplars. It composes with
[SOTA-tmp9d9au](../practices.d/SOTA-tmp9d9au.md) in principle — nothing requires the sampled chains to
come from exemplars — though that combination is not what either paper
measured.
