---
status: 'Active'
title: "Train self-correction with multi-turn online RL on the model's own traces, rather than prompting for it"
version: 1
tags:
- adaptation-and-tuning
consensus: unreplicated
consensus_note: >-
  One group, two models, one family. What raises it above a single positive
  result is that the negative baseline is independently established —
  [LIT-tmpk5uxn](../literature.d/LIT-tmpk5uxn.md) is a different group reporting that the alternative
  intervention does not work, which is the comparison this practice rests on.
date: '2026-09-17'
source:
- LIT-tmpxvpzp
introduced_by:
- LIT-tmpxvpzp
implementations:
- 'SCoRe'
summary: >-
  Kumar et al. (2024), [LIT-tmpxvpzp](../literature.d/LIT-tmpxvpzp.md) — [ARXIV-2409.12917](https://arxiv.org/abs/2409.12917). Self-correction is a
  capability to be trained, not a behaviour to be requested. Prompting a model
  to revise its own reasoning does not reliably help and can hurt; supervised
  fine-tuning on correction traces fails by distribution mismatch or behaviour
  collapse; multi-turn online RL on self-generated traces reaches +15.6% on
  MATH and +9.1% on HumanEval.
---

# SOTA-tmpdrrh9: Train self-correction with multi-turn online RL on the model's own traces, rather than prompting for it

<!-- inactive-ok-file: SOTA-130 — Proposed, and named throughout as the practice this one rhymes with; the comparison IS the content, so every mention here is deliberate -->
## Source

Kumar et al. (2024), [LIT-tmpxvpzp](../literature.d/LIT-tmpxvpzp.md) — [ARXIV-2409.12917](https://arxiv.org/abs/2409.12917).

## Why not just ask

Because that was tried and measured. [LIT-tmpk5uxn](../literature.d/LIT-tmpk5uxn.md) defines *intrinsic*
self-correction — revision on the model's own capabilities, with no oracle,
verifier or second model — and finds that on reasoning it does not reliably
improve and sometimes degrades.

The reason is structural rather than a prompting deficiency. With no external
signal the model cannot distinguish its correct answers from its incorrect
ones, so a revision pass is about as likely to overwrite a right answer as a
wrong one. Where most first attempts are already right, the expected value of
revision is negative.

**Check which side of that line any self-correction claim sits on.** If an
oracle, a verifier or a critic model is in the loop, the gain is attributable
to that information and not to a capacity the model has.

## Why not supervised fine-tuning on correction traces

The obvious next move, and it fails in two distinguishable ways:

- **Distribution mismatch** — traces collected from some other policy contain
  *that* policy's mistakes, so the model learns to repair errors it does not
  make.
- **Behaviour collapse** — training settles into a single correction mode that
  scores well on training prompts and does not correct at test time. This one
  looks like success until evaluation on new problems.

## What to do instead

Train under the model's **own** distribution of self-generated correction
traces, with regularization aimed at collapse: a first phase of multi-turn RL
on the base model to reach an initialization less prone to it, then a reward
bonus that amplifies correction specifically rather than first-attempt
quality.

No second model, no stronger teacher, no additional supervision — which is
what keeps this a training method rather than a distillation result.

## Conditions

Reported on Gemini 1.0 Pro and 1.5 Flash, on MATH and HumanEval, by one
group. The **choice of intervention** is what this practice records — train
it, on-policy — and not the exact two-stage schedule, which is one recipe
from one set of experiments and would be overread as a recommendation.

Self-correction also has a cost that none of these papers price: it spends
extra decoding on every attempt. A capability that improves accuracy by
15.6% while doubling the tokens is a different trade from one that is free,
and the record has no measurement of that trade to point at.

## Where this rhymes

[SOTA-130](SOTA-130.md) records the R1-Zero line — skip the supervised reasoning stage,
run RL with verifiable rewards on the base model. Both practices conclude a
supervised stage is insufficient for a reasoning-adjacent capability and
reach for online RL.

They are separate claims and stay separate. What this one adds is the
mechanism: `SOTA-130` reports that skipping SFT works, and this reports *why
fitting offline traces fails*, with the two modes named. The mechanism is the
half that transfers to capabilities neither paper studied.
