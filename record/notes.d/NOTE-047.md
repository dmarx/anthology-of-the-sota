---
number: 47
paper: LIT-107
status: Read
formerly:
- NOTE-tmpi1vmg
title: 'MiDaS v3.1 - A Model Zoo for Robust Monocular Relative Depth Estimation'
version: 1
tags:
- vision-and-graphics
date: '2026-09-09'
published: '2023-07-01'
summary: >-
  Swaps the image encoder in a fixed depth-estimation architecture across BEiT, Swin, SwinV2, Next-ViT, LeViT and recent convolutional backbones, and reports the resulting performance-runtime frontier. The best backbone improves depth quality by 28%; the paper's other deliverable is the procedure for integrating a new one.
---

# NOTE-047: MiDaS v3.1 - A Model Zoo for Robust Monocular Relative Depth Estimation

## Contribution

Not a method paper — a **controlled backbone sweep**. The MiDaS architecture and
training recipe are held fixed while the image encoder is varied across the
vision transformers that appeared after v3.0 (which used only vanilla ViT):
**BEiT, Swin, SwinV2, Next-ViT, LeViT**, plus recent convolutional approaches
that match ViTs on classification.

The output is a **model zoo** spanning a performance-runtime frontier, a **28%**
depth-quality improvement from the best backbone, and — explicitly listed as a
contribution — **a description of the general process for integrating a new
backbone.**

## Key insight

The paper's structure is its argument. By holding everything except the encoder
constant it answers a question the individual backbone papers cannot: **does
classification performance transfer to depth estimation?** Its inclusion of
convolutional approaches "that achieve comparable quality to vision transformers
in image classification tasks" is the direct test, and it is the sort of
comparison that only exists if someone does exactly this work.

The second contribution is the underrated one. Publishing **how to integrate a
new backbone** makes the zoo extensible by other people, which is a different
kind of deliverable from a result — and it is the thing that keeps a model zoo
alive after the paper.

## Assumptions

- The rest of the MiDaS architecture is backbone-agnostic enough that the
  comparison is fair — the premise of the whole exercise.
- Depth quality and runtime are the axes that matter, which is reasonable for a
  component used inside other systems.

## Key results

- **28% depth-quality improvement** from the best backbone over the previous
  release.
- **A performance-runtime frontier**, with efficient models "enabling downstream
  tasks requiring high frame rates" — the zoo is the result, not one model.
- Convolutional backbones evaluated alongside transformers on equal terms.
- A documented backbone-integration procedure.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Encoder choice materially changes depth-estimation quality | strong | 28% across a controlled sweep |
| C2 | Different backbones occupy different points on the quality/runtime frontier | strong | measured |
| C3 | The comparison is fair because everything else is held fixed | moderate | the design; some architectures may suit the head better than others |
| C4 | New backbones can be integrated by a documented procedure | moderate | described; its generality is asserted |

## Method

Hold the MiDaS architecture, training data and recipe fixed. Substitute each
encoder. Measure depth quality and runtime. Publish all of them and the
integration procedure.

## Concepts

- **The controlled component sweep** — a paper whose contribution is that
  somebody varied one thing carefully.
- **A frontier rather than a winner** — reporting the trade-off surface,
  because different downstream uses sit at different points.
- **Extensibility as a deliverable** — documenting the integration path.

## Connections

The methodological sibling of `LIT-156` (*Fantastic Pretraining Optimizers*),
read in batch B: both hold a setting fixed and sweep one component fairly, and
both find that the component's reputation elsewhere does not settle its
performance here. `LIT-156` makes the point about optimizers and unequal tuning;
this makes it about encoders and transfer from classification.

## Recommendations

- **R1** — Report a frontier rather than a winner when downstream uses have
  different cost constraints. *Topic:* analysis and evaluation. *Strength:*
  strong.
- **R2** — Do not assume a component's performance on one task transfers to
  another; sweep it. *Strength:* strong, and the same lesson as `LIT-156`.
- **R3** — Publish the procedure for extending the comparison. *Strength:*
  moderate, and rare.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**
Monocular depth estimation is not a line the anthology tracks.

R2 is the transferable one, and it now has two independent instances in this
pass: `LIT-156` for optimizers, this for encoders. **A component that wins on
one task is not thereby the right choice for another, and the only way to know
<!-- inactive-ok-block: SOTA-168 — Proposed, named as the record's adjacent optimizer practice rather than relied on -->
is a fair sweep.** The record has `SOTA-168` and the optimizer neighbourhood
carrying half of that; the general form is stated nowhere.

The document's takeaways — "improved depth estimation", "cross-dataset
generalization", "robust performance", "efficient architecture" — describe the
MiDaS *line* rather than this release, whose entire content is the sweep. None
of them mentions that the paper's contribution is a comparison.

## Limitations

- 2023 backbones; the zoo dates.
- C3's fairness assumption is untested — a head tuned for ViT may suit ViT.
- Relative depth only.
- The 28% is a single best-case figure against the previous release.

## Open questions

- Does the ranking here match the classification ranking? The paper has the data
  to say so directly and reports the depth numbers rather than the correlation,
  which is the question it is best placed to answer.
