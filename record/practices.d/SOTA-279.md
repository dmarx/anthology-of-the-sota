---
number: 279
status: Active
formerly:
- SOTA-tmplac25
consensus: universal
consensus_note: >-
  Showing intermediate steps is now so standard that models are post-trained
  to do it unprompted and the field argues about how to evaluate the traces
  rather than whether to elicit them. `universal` is a statement about
  adoption and not about evidence — DP-005 — and the evidence here is one
  paper on 2022-era models plus everything built on top since.
title: 'Put worked reasoning steps in the few-shot exemplars when the task needs more than one step, and only once the model is large enough'
version: 1
tags:
- in-context-learning
- adaptation-and-tuning
date: '2026-09-21'
source:
- LIT-467
introduced_by:
- LIT-467
extends:
- SOTA-038
implementations: []
summary: >-
  Wei et al. (2022), [LIT-467](../literature.d/LIT-467.md) — eight exemplars carrying worked
  steps more than doubled PaLM 540B on GSM8K, beating a fine-tuned model with
  a verifier. Three ablations rule out the equation, the extra tokens and
  knowledge activation. Below ~100B it does nothing or hurts.
extended_by:
- SOTA-280
- SOTA-281
---

<!-- inactive-ok-file: SOTA-130 — Proposed, and named as a practice that assumes this one, not as a source for it -->
# SOTA-279: Put worked reasoning steps in the few-shot exemplars when the task needs more than one step, and only once the model is large enough

## Source

Wei et al. (2022), [LIT-467](../literature.d/LIT-467.md) — [ARXIV-2201.11903](https://arxiv.org/abs/2201.11903),
read as [NOTE-216](../notes.d/NOTE-216.md).

## What to do

Write the few-shot exemplars as `⟨input, worked steps, output⟩` rather than
`⟨input, output⟩`. Eight is enough. Nothing else changes — no fine-tuning, no
training data, no task-specific checkpoint.

## When it pays, and when it does not

| condition | effect |
|---|---|
| multi-step problem, model ≥ ~100B | large; GSM8K more than doubled |
| single-step problem | negative or negligible |
| model below ~100B | absent, and often worse than plain prompting |

The second and third rows are the part that gets dropped when this is
repeated. Small models produce chains the paper describes as "fluent but
illogical" and score *below* standard prompting, and on SingleOp — the
one-step subset of MAWPS — the gain is negative or very small. This is a
recommendation with a regime, not a universal improvement.

## Why the ablations matter more than the headline

Three rival explanations were built and knocked down, which is why this is
the trunk rather than one result among many:

- **Not the equation.** Prompting for the equation alone does not help on
  GSM8K.
- **Not the extra tokens.** Emitting a row of dots as long as the needed
  equation performs at baseline. Buying the model more positions to compute
  in, with nothing in them, buys nothing.
- **Not knowledge activation.** Putting the chain *after* the answer performs
  at baseline, so the answer depends on the chain rather than being primed
  by it.

## Conditions

- **The evidence is 2022 models** — LaMDA, GPT-3, PaLM. The ~100B threshold
  is a fact about that generation, and small-model reasoning has moved a long
  way since. Treat the threshold as a caution to measure rather than a
  number to apply.
- **Chains are tokens.** The paper reports negative gains on the easiest
  problems and does not price the ones it wins on. There is a regime where
  this loses on accuracy and cost at once.
- **A correct chain is not guaranteed and a correct answer does not imply
  one.** Their own error analysis found two of fifty correct answers reached
  through incorrect reasoning. Reading a chain as an explanation of the
  answer is a separate claim this does not support.
- **Whether the model is "reasoning" is explicitly left open by the
  authors**, and the practice takes no position either.
- **The emergence claim rests on a brittle metric.** Exact-match over
  multi-step answers is the shape [SOTA-200](../practices.d/SOTA-200.md) says to distrust. The
  *gains* at 540B survive three ablations and are not in doubt; the
  *discontinuity* has not been re-measured against a continuous score.

## Why `Active` and `universal` at once

`Active` because the effect is large, ablated against its three obvious
alternatives, and robust across annotators, exemplar sets, orders and three
model families. `universal` because the field stopped arguing about this
years ago — models are now post-trained to produce traces unprompted, and the
live disputes are about how to *evaluate* traces
([LIT-466](../literature.d/LIT-466.md), [LIT-463](../literature.d/LIT-463.md)) rather than whether to
elicit them. [DP-005](../principles.d/DP-005.md) is why those are two separate fields: adoption
this complete is not itself evidence, and the evidence column here still
holds one paper about a generation of models nobody serves any more.

## What this practice does not cover

The record holds nothing yet on the immediate descendants, and each is a
separate recommendation:

- **Zero-shot chain of thought** — appending "Let's think step by step" with
  no exemplars at all (`ARXIV-2205.11916`).
- **Self-consistency** — sampling several chains and taking the majority
  answer (`ARXIV-2203.11171`).
- **Whether to elicit chains at all on an easy query**, which
  [LIT-466](../literature.d/LIT-466.md) bears on directly: at low complexity its
  non-thinking models beat their own thinking counterparts and used fewer
  tokens, which is this paper's SingleOp finding arriving again three years
  later by a different route.

## Relation to the neighbours

Extends [SOTA-038](../practices.d/SOTA-038.md), in-context few-shot adaptability, which is the
mechanism it modifies. [SOTA-127](../practices.d/SOTA-127.md) — filter chain-of-thought traces out
of a tiny specialist's training data — is the other side of the scale
threshold, and now has the paper explaining why small models' chains are bad
sitting beside it. [SOTA-130](../practices.d/SOTA-130.md) and the reasoning-model literature assume
this and had no antecedent in the record for what they were extending.
