---
number: 20
status: Read
formerly:
- NOTE-tmpwwwom
paper: LIT-034
title: "Don't Stop Pretraining"
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-09'
published: '2020-04-01'
summary: >-
  Two adaptive-pretraining stages, and the second is the surprise. Domain-adaptive pretraining (DAPT) on a large in-domain corpus helps; task-adaptive pretraining (TAPT) on the task's own small unlabelled set also helps, and the two are complementary rather than alternatives.
---

# NOTE-020: Don't Stop Pretraining

## Contribution

Asks whether a model pretrained on a broad corpus is done being pretrained.
It is not. **Domain-adaptive pretraining** — continuing on a large unlabelled
corpus from the target domain — improves downstream performance, and
**task-adaptive pretraining** — continuing on the task's *own* unlabelled
text, which is far smaller — does too. The two are **complementary**: doing
both beats either.

## Key insight

The pretraining distribution matters more than the fine-tuning one for a task
far from it, and "the pretraining distribution" is not a single fixed thing
you inherit. It is a stage you can extend, cheaply, with unlabelled text you
usually already have.

The genuinely surprising half is TAPT. A few thousand unlabelled task
examples — orders of magnitude less text than DAPT uses — are worth a further
pretraining stage *even after* the domain corpus has been used. The task's
own inputs carry distributional information that neither the broad corpus nor
the domain corpus supplies, and fine-tuning on the labels does not extract it.

## Assumptions

- **RoBERTa** as the base model throughout; four domains, eight classification
  tasks, 2020 scales.
- Unlabelled in-domain and in-task text is **available**, which is the
  practical precondition and is usually satisfied.
- The evaluation is fine-tuned classification. Nothing here is measured
  through in-context learning or post-training, which is how the record's
  contemporary practices are judged.

## Key results

- **DAPT** — continued pretraining on a large in-domain unlabelled corpus —
  improves over the base model across domains.
- **TAPT** — continued pretraining on the task's unlabelled training text —
  also improves, at a tiny fraction of the compute.
- **DAPT + TAPT is better than either**, which is the result that makes them
  two distinct effects rather than one.
- Gains are largest where the target domain is furthest from the pretraining
  corpus, which is the shape the mechanism predicts.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Continued pretraining on in-domain unlabelled text improves downstream performance | strong | measured across four domains |
| C2 | Continued pretraining on the task's own unlabelled text also improves it | strong | measured across eight tasks; the paper's own surprise |
| C3 | DAPT and TAPT are complementary | strong | the combination beats both |
| C4 | The benefit scales with distance from the pretraining distribution | moderate | the trend across their domains, not a fitted relationship |

## Method

Take a pretrained model. **DAPT**: continue the pretraining objective on a
large unlabelled corpus drawn from the target domain. **TAPT**: continue it on
the unlabelled text of the task's own training set. Then fine-tune. For both,
continue with the *pretraining* objective — the labels are not used until
fine-tuning.

## Concepts

- **DAPT / TAPT** — the paper's own abbreviations, and the reason it is
  citable as two findings rather than one.
- **Adaptive pretraining** — a stage between pretraining and fine-tuning,
  using unlabelled text and the pretraining objective.

## Connections

Sits in the pretrain-then-finetune paradigm and is one of the clearest
statements of why that paradigm's first stage is not fixed. The modern
pipeline's stages are different in kind — the question is now what mixture of
supervised and reinforcement stages follows pretraining — but the underlying
claim about distributional distance survives the change.

## Recommendations

- **R1** — Continue pretraining on unlabelled in-domain text before
  fine-tuning for a distant domain. *Topic:* adaptation. *Status:* standard.
  *Strength:* strong. *Applies when:* the target domain is far from the
  pretraining corpus and unlabelled text exists.
- **R2** — Also continue on the task's own unlabelled text, even after R1.
  *Topic:* adaptation. *Status:* standard. *Strength:* strong. *Applies
  when:* always within R1 — it is nearly free and independently useful.
- **R3** — Treat the pretraining distribution as a lever rather than an
  inheritance. *Topic:* adaptation. *Status:* standard. *Strength:*
  moderate. *Applies when:* any adaptation decision; it is the general form
  of C1 and C4.

## Bearing on the record

**The one practice sourced to this note is confirmed.**

| practice | disposition |
|---|---|
| [SOTA-033](../practices.d/SOTA-033.md) continued pre-training for fine tuning | confirmed — C1 through C3 |

`SOTA-033`'s body already distinguishes the two axes and already says the
surrounding pipeline has been replaced while the underlying claim survives.
Both hold.

The reading adds the paper's own names, `DAPT` and `TAPT`, which matter for a
reason the practice's title obscures: this is **two findings**, and the
second — that a few thousand unlabelled task examples are worth their own
stage *after* the domain corpus — is the one that was not obvious and is not
in the practice's title at all.

## Limitations

- RoBERTa-scale classification in 2020. The modern question is post-training
  composition, not more pretraining before fine-tuning.
- C4 is a trend across four domains, not a measured relationship.
- Nothing addresses how adaptive pretraining interacts with instruction
  tuning or RL stages, because those did not exist in this form.

## Open questions

- TAPT says the task's own unlabelled inputs carry information fine-tuning
  does not extract. Is that still true when the downstream use is in-context
  rather than fine-tuned?
- The record holds practices about mid-training and anti-curricula that are
  arguably the same question at a different scale. Nothing connects them.
