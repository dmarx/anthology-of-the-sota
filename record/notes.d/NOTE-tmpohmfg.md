---
# inactive-ok: LIT-057 — Rejected, and this document is the reading that says why the paper is in the attic and what survives it
paper: LIT-057
status: Read
title: 'What Makes for Good Views for Contrastive Learning?'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-09'
summary: >-
  Argues for an InfoMin principle: views should share as little mutual information as possible while keeping task-relevant information intact. Too much shared information makes the contrastive task trivial, too little destroys the signal, so there is a sweet spot — and augmentation design is the search for it.
---

# NOTE-tmpohmfg: What Makes for Good Views for Contrastive Learning?

## Contribution

Contrastive learning was working and nobody could say what made an augmentation
good. This paper proposes the criterion — **InfoMin**: *reduce the mutual
information between views while keeping task-relevant information intact* — and
designs augmentations from it.

## Key insight

Two views that share too much make the contrastive task trivially solvable
without learning anything useful; two that share too little have no task-relevant
signal in common. So the objective is **not** to maximise agreement or to
maximise difficulty, but to sit at the point where the only thing the views still
share is what the task needs.

That reframes augmentation design from a bag of tricks into a constrained
optimisation with a stated objective, and it is the reason the paper's
augmentation set is derived rather than tried.

## Assumptions

- **Task-relevant information is identifiable in advance**, at least well enough
  to preserve it while destroying the rest. This is the load-bearing assumption
  and it is exactly what self-supervised learning does not have.
- Mutual information between views is the right currency — estimable enough, and
  monotone with the thing that matters.
- ImageNet-scale image self-supervision, 2020.

## Key results

- **InfoMin Aug**, combined with the JigSaw strategy from PIRL, reaches **73.0%
  top-1 on ImageNet linear readout with ResNet-50** — nearly **4% over SimCLR**.
- Transfers of the unsupervised pretrained model to **PASCAL VOC detection and
  COCO instance segmentation consistently beat supervised ImageNet
  pretraining.**
- The sweet-spot argument, supported both theoretically and empirically.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | View selection materially determines representation quality | strong | the 4% gap from augmentation design alone |
| C2 | The right criterion is minimal MI subject to keeping task information | moderate | argued theoretically, and the derived augmentations work |
| C3 | Augmentations derived from C2 beat hand-designed ones | strong | 73.0% vs SimCLR |
| C4 | Unsupervised pretraining beats supervised ImageNet pretraining downstream | strong | VOC and COCO, consistently |
| C5 | Task-relevant information can be preserved without labels | **weak** | the practical gap in C2, and the paper's own tension |

## Method

Formalise view quality as mutual information subject to preserving task
information. Derive augmentations that reduce MI while retaining semantics.
Combine with JigSaw. Evaluate by linear readout and by transfer.

## Concepts

- **InfoMin** — the criterion, and the durable contribution.
- **The sweet spot** — a U-shaped relationship where both extremes fail, which
  is a more useful shape than "more is better".
- **Deriving augmentations from an objective** rather than collecting them.

## Connections

<!-- inactive-ok-block: LIT-092, LIT-044 — Rejected, and named as a paper this one argues with; each has its own reading saying why it is in the attic -->
`LIT-092`, read in the same batch, is the direct rebuttal at the level of
theory: it argues that reasoning about augmentations and the contrastive loss
**cannot** by itself explain downstream performance, because function class and
optimiser matter and are absent from such accounts. InfoMin is precisely an
augmentation-and-objective account. The two documents disagree, they are both in
this record, and the disagreement is the useful part.

<!-- inactive-ok-block: LIT-044 — Rejected, and named as a paper facing the same obstacle; it has its own reading saying why it is in the attic -->
`LIT-044` is the third: it manipulates the *negatives* rather than the views,
and faces the same unlabelled-data obstacle — you cannot avoid false negatives
without labels, just as you cannot preserve task information without knowing the
task.

## Recommendations

- **R1** — State what an augmentation is supposed to destroy and what it must
  preserve, and derive it from that. *Topic:* data pipeline. *Strength:*
  moderate.
- **R2** — Look for U-shaped relationships; "more difficulty is better" and
  "more agreement is better" are usually both wrong. *Strength:* moderate.
- **R3** — Treat "preserve task-relevant information" as an assumption to
  defend, not a step. *Strength:* strong, and it is C5.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice**, and the
document is `Rejected`. Contrastive representation learning at 2020 image scale
is not a line the anthology tracks, and the reading does not argue with the
status.

<!-- inactive-ok-block: LIT-092 — Rejected, and named as a paper this one argues with; each has its own reading saying why it is in the attic -->
What the reading is worth is the **pairing with `LIT-092`**. Both are `Rejected`,
both are in this batch, and one is a direct methodological objection to the
other. Recording that they disagree is worth more than either alone: a reader
who finds InfoMin persuasive should know that a later paper argues its whole
genre of explanation is insufficient.

R2 is the transferable half. The record's practices mostly recommend directions
— more depth, more data, lower learning rate — and a U-shaped criterion is a
different and often more accurate shape.

The document's takeaways — "analysis of view generation", "information
bottleneck perspective", "augmentation strategies", "theoretical framework" —
name the apparatus and not the criterion. "Information bottleneck" is also
loose: InfoMin is about mutual information *between views*, which is not the
information-bottleneck objective.

## Limitations

- 2020, ImageNet-scale image self-supervision.
- C5 is the unresolved tension: the criterion needs to know the task, and the
  setting is defined by not knowing it.
- MI estimation in high dimensions is difficult, and the practical method uses
  proxies.
<!-- inactive-ok-block: LIT-092 — Rejected, and named as a paper this one argues with; each has its own reading saying why it is in the attic -->
- `LIT-092` argues the entire framing is insufficient to predict downstream
  performance.

## Open questions

- Can the InfoMin sweet spot be found without knowing the downstream task? That
  is the question the method needs answered and the setting forbids.
