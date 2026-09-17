---
status: Read
paper: LIT-tmpk5uxn
title: 'Large Language Models Cannot Self-Correct Reasoning Yet'
version: 1
date: '2026-09-17'
summary: >-
  Asked to revise its own reasoning with no external feedback, a model does
  not reliably improve and sometimes degrades. The durable part is the
  definition rather than the number: INTRINSIC self-correction, meaning no
  oracle, no verifier, no second model — a line that a lot of contemporary
  self-correction claims were quietly on the other side of.
---

# NOTE-tmp27xgr: Large Language Models Cannot Self-Correct Reasoning Yet

Read from [LIT-tmpk5uxn](../literature.d/LIT-tmpk5uxn.md) — [ARXIV-2310.01798](https://arxiv.org/abs/2310.01798).

## What it establishes

A definition and a measurement against it. **Intrinsic self-correction** is
the model revising "based solely on its inherent capabilities, without the
crutch of external feedback". Under that definition, on reasoning, models
struggle — and performance sometimes *degrades* after the revision step.

The mechanism is not subtle and is the reason the result should not have been
surprising. A model with no external signal has nothing to tell a correct
answer from an incorrect one. A revision pass is therefore about as likely to
overwrite a right answer as a wrong one, and if the initial answers are mostly
right, the expected effect of revision is negative.

## Why the definition outlives the result

Because a great deal of the literature it was written against is measuring
something else. If an oracle says "this is wrong, try again", or a verifier
filters, or a second model critiques, the loop contains information the model
did not have — and the gain is attributable to that information rather than to
any capacity for self-correction. The paper's contribution is drawing that line
and insisting results declare which side they are on.

That makes it a lens rather than a verdict, which is also why the title's
"yet" is doing real work. It is a claim about models as they were, under one
specific protocol.

## What it does to the record

No practice is sourced here, deliberately — the finding is that an
intervention does not work, and the useful instruction it supports belongs to
the paper that supplies the alternative ([LIT-tmpxvpzp](../literature.d/LIT-tmpxvpzp.md)).

Two things it is worth holding for. First, as the baseline that makes SCoRe's
numbers mean something: a gain measured against prompted self-correction is
only interesting because prompted self-correction is known not to work.
Second, as a reading instrument — any self-correction claim in this corpus
should be checked for whether external feedback was in the loop before its
number is believed.
