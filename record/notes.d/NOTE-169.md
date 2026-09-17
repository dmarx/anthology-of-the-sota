---
number: 169
status: Read
formerly:
- NOTE-tmpszc5q
paper: LIT-383
title: 'Training Language Models to Self-Correct via Reinforcement Learning'
version: 1
date: '2026-09-17'
summary: >-
  SCoRe teaches self-correction with multi-turn online RL on the model's own
  traces, no teacher and no extra supervision, for +15.6% on MATH and +9.1%
  on HumanEval. The transferable half is the diagnosis: SFT on correction
  traces fails by distribution mismatch or by behaviour collapse, and the
  method's two stages are each aimed at one of those.
---

# NOTE-169: Training Language Models to Self-Correct via Reinforcement Learning

<!-- inactive-ok-file: SOTA-130 — Proposed, and named throughout as the practice this one rhymes with; the comparison IS the content, so every mention here is deliberate -->
Read from [LIT-383](../literature.d/LIT-383.md) — [ARXIV-2409.12917](https://arxiv.org/abs/2409.12917).

## The setup it inherits

It opens by conceding the negative result: self-correction "has consistently
been found to be largely ineffective in modern LLMs" — [LIT-382](../literature.d/LIT-382.md)'s
finding. The response is a change of intervention. If asking does not work,
train for it; and train without a stronger model, an oracle or additional
supervision, because any of those would make the result a distillation result
instead.

## Why supervised fine-tuning does not get there

This is the part I would keep if the method were superseded tomorrow. Two
distinct failure modes, and they are not the same complaint:

- **Distribution mismatch.** Correction traces collected from some
  data-collection policy contain *that policy's* mistakes. The model being
  trained makes different ones, so it is learning to repair errors it does not
  commit.
- **Behaviour collapse.** Training implicitly prefers one mode of correction
  that scores well on the training prompts — the paper's phrasing is that it
  ends up "fitting high-reward responses for a given prompt" rather than
  learning a behaviour that corrects at test time.

The second is the more interesting failure because it looks like success right
up until evaluation on new problems.

## The method, read as a response to those two

Train on the model's **own** distribution of self-generated correction traces,
which is the direct answer to the first. Then regularize against the second,
in two stages: an initial phase of multi-turn RL on the base model to reach an
initialization "less susceptible to collapse", followed by a reward bonus that
specifically amplifies correction rather than first-attempt quality.

Results: +15.6% on MATH, +9.1% on HumanEval, for Gemini 1.0 Pro and 1.5 Flash.

## What this does to the record

Sources one practice — train the capability rather than prompt for it.

The connection worth recording is to [SOTA-130](../practices.d/SOTA-130.md), which the record already
holds: the R1-Zero line, skip the supervised reasoning stage and run RL with
verifiable rewards on the base model directly. Both conclude a supervised
stage is insufficient for a reasoning-adjacent capability and both reach for
online RL.

They are not the same claim and should not be merged. `SOTA-130` reports that
skipping SFT *works*; this paper says *why fitting offline traces fails*, with
two mechanisms named and separated. A reader who has the first and not the
second knows a thing happens and not what breaks — and the mechanism is the
half that transfers to a capability neither paper studied.

Not filed from here: the specific two-stage recipe as a recommendation. It is
reported on two Gemini models by one group, and a practice telling anyone to
adopt that exact schedule would be overreading a single result. What the
practice records is the choice of intervention, which is what the evidence
actually supports.
