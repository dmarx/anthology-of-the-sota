---
number: 18
status: Read
formerly:
- NOTE-tmpn4y0b
paper: LIT-096
title: 'Segment Anything'
version: 1
tags:
- data-pipeline
date: '2026-09-09'
summary: >-
  The data engine is the transferable part. Three stages — assisted-manual, semi-automatic, fully automatic — each stage's labels training the model that produces the next stage's, ending in 1.1B masks. The model and the dataset are built together.
---

# NOTE-018: Segment Anything

## Contribution

A promptable segmentation model, a dataset of **1.1B masks**, and — the part
this record is filed for — the **data engine** that produced them. Annotation
proceeds in three stages: **assisted-manual**, where annotators label with
model help; **semi-automatic**, where the model proposes confident masks and
annotators fill gaps; and **fully automatic**, where the model labels alone.
The model is retrained between stages, so each stage's output trains the model
that produces the next stage's.

## Key insight

A model and its training set do not have to be built in that order. If the
model can be made useful early — even badly — it can be pointed at the
annotation bottleneck, and the loop tightens: better labels give a better
model, which gives cheaper labels.

The reason this is a data-pipeline claim rather than a segmentation one is
that nothing in the loop is about masks. What it requires is that the task
admits **partial automation with human verification**, and that the model's
confidence is informative enough to route work. The 1.1B masks are the
consequence; the loop is the method.

## Assumptions

- The model must be **useful before the dataset exists** — stage one needs
  assistance good enough to speed a human up. A task where the cold-start
  model is worthless has no stage one.
- **Confidence must be informative** enough to separate "propose this
  automatically" from "send this to a human", which is what stage two turns
  on.
- Human verification is available and affordable at stage one and two scale.
- Segmentation masks are cheap to verify visually — a property not every
  annotation target has.

## Key results

- **Three-stage data engine**, with retraining between stages.
- **1.1B masks** over 11M images, the great majority from the fully automatic
  stage.
- A promptable model, zero-shot transferable to a range of segmentation
  tasks.
- Each stage is materially cheaper per label than the one before, which is
  the loop paying off.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A model can be bootstrapped into its own annotation pipeline | strong | the engine ran and produced the dataset |
| C2 | Staged automation with retraining between stages compounds | strong | the per-stage cost curve |
| C3 | The resulting model transfers zero-shot | strong | measured across tasks |
| C4 | The approach generalises beyond segmentation | weak | not tested here; a reading, and the reason this note is in this record |

## Method

**Stage 1, assisted-manual.** Annotators label with model assistance; retrain.
**Stage 2, semi-automatic.** The model proposes masks it is confident about;
annotators label what remains, which concentrates human effort on the hard
cases; retrain. **Stage 3, fully automatic.** The model labels at scale.

## Concepts

- **Data engine** — the paper's own term for the loop. Worth keeping, because
  it names the thing as a *process* rather than as a dataset.
- **Promptable segmentation** — the task formulation that makes the model
  useful at stage one, since it can be steered rather than needing to be
  right unprompted.

## Connections

Method-wise its relatives are active learning and weak supervision; what is
new is doing it at this scale and shipping the resulting dataset. Within this
record its neighbours are the data-selection and mixing practices, which
decide what to train on from data that already exists — this one is about
*making* the data.

## Recommendations

- **R1** — Bootstrap annotation with the model being trained, in stages, with
  retraining between them. *Topic:* data. *Status:* standard. *Strength:*
  strong. *Applies when:* the model can be useful before the dataset is
  complete and outputs are cheap to verify.
- **R2** — Route work by model confidence, so human effort concentrates where
  the model is weak. *Topic:* data. *Status:* standard. *Strength:*
  moderate. *Applies when:* confidence is informative — which is a property
  to check, not assume.
- **R3** — Treat the annotation loop as a designed artifact. *Topic:* data.
  *Status:* standard. *Strength:* moderate. *Applies when:* labels are the
  bottleneck; the paper's framing is that the engine, not the dataset, is the
  contribution.

## Bearing on the record

**The one practice sourced to this note is confirmed.**

| practice | disposition |
|---|---|
| [SOTA-186](../practices.d/SOTA-186.md) bootstrap a large annotation set with the model you are training | confirmed — C1, C2 |

`LIT-096`'s Standing section already made the case that the practice drawn
from this paper "is not about segmentation ... which is a `data-pipeline`
claim and the reason this note is in the record at all under [ADR-020](../decisions.d/ADR-020.md)". The
reading supports that and sharpens the conditions.

The two preconditions are what a reader most needs and what the practice does
not state: the model must be **useful before the dataset exists**, and
**confidence must be informative enough to route work**. A task failing
either has no stage one or no stage two, and the loop does not start.

`C4` — that this generalises past segmentation — is the claim the record is
actually relying on, and it is the weakest one here. The paper does not test
it. That is worth saying plainly in a registry that files the practice under
`data-pipeline` precisely because it believes C4.

## Limitations

- Segmentation masks are unusually cheap to verify. Annotation targets
  requiring expertise or judgement do not inherit the economics.
- C4 is untested — the generalisation is the record's inference, not the
  paper's finding.
- Automatic labels at stage three carry the model's biases into the dataset
  that trains its successor, and nothing here measures that drift.

## Open questions

- What does the fully automatic stage's error distribution do to the next
  model? The loop's compounding is measured on cost, not on error.
- Where does the approach stop? A task needing expert judgement per label
  presumably has no viable stage three, and nobody has drawn that line.
