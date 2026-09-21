---
number: 39
status: Active
formerly:
- THEORY-tmptybdn
title: 'A measured capability is the capability minus whatever the evaluation itself demands, and the gap is widest for the weakest model'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-465
- LIT-463
explains:
- SOTA-278
- SOTA-200
summary: >-
  Hu and Frank (2024), [LIT-465](../literature.d/LIT-465.md) — the same capacity measured two
  ways scores differently, and the difference shrinks with size and training.
  So a score is a joint function of model and design, and cross-scale
  comparisons under a demanding evaluation inflate the gap they report.
---

<!-- inactive-ok-file: ADR-031 — Proposed, and cited for the practice/explanation split that lets this account be Active while the dispute it draws an example from stays open -->
# THEORY-039: A measured capability is the capability minus whatever the evaluation itself demands, and the gap is widest for the weakest model

## Source

Hu and Frank (2024), [LIT-465](../literature.d/LIT-465.md) — read as [NOTE-215](../notes.d/NOTE-215.md) —
with [LIT-463](../literature.d/LIT-463.md) ([NOTE-213](../notes.d/NOTE-213.md)) as the worked
example in a case people argued about.

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-278](../practices.d/SOTA-278.md) | rule out the evaluation before reporting a limit | the demand gap is a known quantity with a known sign, so the check has a target |
| [SOTA-200](../practices.d/SOTA-200.md) | check whether an emergent capability is a metric artefact | the same instrument problem with the sign reversed — scale paying down a demand looks like scale unlocking a capacity |

## The account

Developmental psychology has long distinguished two reasons a child fails a
task: the capacity is absent, or the task's *auxiliary demands* defeated
them — not understanding the question, holding several facts at once,
inhibiting a prepotent response. The distinction transfers, and so does the
measurement strategy: ask the same thing two ways, one demanding and one not,
and take the difference.

Do that for analogical reasoning, reflective reasoning, word prediction and
grammaticality judgement, and the low-demand method wins every time. Reading
the probability a model assigns to a word scores higher than asking the model
in words what word it predicts. Forced choice scores higher than free
production.

The load-bearing part is not that gap but its **interaction with capability**.
It narrows as models get larger and as one model trains longer, significantly
so in three of four domains and across five model families. Which means the
demand is not a constant offset that cancels in a comparison. It is a tax the
weaker model pays more of — so comparing a small and a large model on one
demanding evaluation and attributing the difference to capability counts the
tax as capability.

The generalisation is that a score never measures a capacity directly. It
measures a capacity through a design, and the design's cost is itself a
function of the thing being measured.

## What was actually shown

13 models, five families, 1B to 70B, plus one model across ten training
checkpoints. Four capacities, each with two evaluation methods argued to
target the same construct. Mixed-effects models testing the size × method
interaction.

It could have failed and partly did. The interaction is **not** significant
for reflective reasoning, and the paper explains why rather than dropping it:
larger models there prefer the intuitive answer, so raw performance does not
rise with size to begin with. Pythia's gap is flat across sizes, and OLMo's
is flat in one domain. These are reported, not smoothed.

## What this does not say

**It does not say measured limits are usually artefacts.** It says the
artefact exists, has a sign, and scales — not what share of any particular
reported gap it accounts for. The paper attaches no number to that and
neither does this.

**It does not say the two methods measure the same thing.** That is the
assumption the whole design rests on, argued rather than established. If
metalinguistic prompting genuinely requires a capacity that probability
readout does not, the gap is partly real.

**It does not reach instruction-tuned or frontier models.** Base models only,
open weights only, because token-level logits are needed. Instruction tuning
targets task-demand competence directly, so the gap could be much smaller
there — and the loudest capability disputes are about exactly the models this
cannot measure.

**And the low-demand readout does not always exist.** Reading a probability
is a low-demand method for word prediction. There is no equivalent for
multi-step planning, which is where [LIT-466](../literature.d/LIT-466.md) and
[LIT-463](../literature.d/LIT-463.md) are arguing. So the mechanism is established in a
domain where it can be measured and applied in one where it cannot, which is
a real extrapolation and not a hidden one.

## Why `Active`, on a contested subject

Because the account and the dispute are different things. Whether the
reasoning-model collapse is an artefact is unsettled — one side is NeurIPS
2025, the other an underpowered preprint that has already been corrected once
— and nothing here settles it. What is settled is that a demand gap exists,
has the sign claimed, and widens as models weaken, on a systematic study
across five families with a stated statistical test. The record can hold that
while holding the specific dispute open, which is the split
[ADR-031](../decisions.d/ADR-031.md) exists for.
