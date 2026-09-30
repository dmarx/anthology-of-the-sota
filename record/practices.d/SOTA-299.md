---
number: 299
status: Proposed
formerly:
- SOTA-tmpe5ykn
promote_when: >-
  The same end-to-end-generative-finetuning recipe carrying a *different*
  dense task past its label distribution — depth, normals, correspondence,
  amodal completion — with a from-scratch-head baseline on the same backbone
  and data to show the head is what fails. The baseline is the load-bearing
  half: this practice rests on `SimpleClick` scoring 1.4–2.4 mIoU, and a
  result without that control is a good segmenter rather than evidence for
  this. What would not move it: another paper finetuning a diffusion model
  for a perception task and reporting competitive in-distribution numbers,
  which is common and does not test generalization beyond the labels.
consensus: unreplicated
consensus_note: >-
  One group, one task. Transferring diffusion priors to perception is a
  crowded area — the paper's related work lists depth, normals, flow,
  correspondence and amodal segmentation — so the *recipe* is not novel and
  its adoption would not be evidence. What is unreplicated is the
  generalization claim and the controls that attribute it, and those are
  what this practice rests on.
title: 'Finetune the whole generative model, encoder and decoder, for a dense perception task instead of attaching a head to a backbone'
version: 1
tags:
- vision-and-graphics
- adaptation-and-tuning
- representation-and-encoding
date: '2026-09-21'
source:
- LIT-488
introduced_by:
- LIT-488
implementations: []
explained_by:
- THEORY-052
summary: >-
  Khangaonkar and Pirsiavash (2025), [LIT-488](../literature.d/LIT-488.md) — the freshly-initialized
  mask head is the part that cannot generalize, because it has only ever seen
  the finetuning categories. Keep every parameter generatively pretrained,
  encode the target as an image, and a model finetuned on **furniture and
  cars** segments people, x-rays and paintings. The same backbone under a
  conventional head scores **1.4–2.4 mIoU**.
---

# SOTA-299: Finetune the whole generative model, encoder and decoder, for a dense perception task instead of attaching a head to a backbone

## Source

Khangaonkar and Pirsiavash (2025), [LIT-488](../literature.d/LIT-488.md) — [ARXIV-2505.15263](https://arxiv.org/abs/2505.15263) — read
as [NOTE-237](../notes.d/NOTE-237.md).

## What to do

**Express the dense target in the pretrained model's own output space.** For
instance segmentation that means an RGB image: one colour per instance, black
background. The model then does the thing it was pretrained to do —
image-to-image — rather than something new.

**Train a permutation-free objective**, since the colour assignment is
arbitrary. Three terms: low variance within an instance, separation between
instance means, and a penalty for an instance's colour appearing outside it.

**Finetune encoder and decoder together, and add no new parameters.** This is
the whole point. MAE's decoder is conventionally discarded before finetuning;
here it is the part that carries pixel-level generative structure, and
keeping it is what the practice is about.

**Read the answer out of the output field directly** if you can — a prompt
point becomes a query colour, a similarity map, a threshold. The source uses
no trained mask decoder at all, deliberately, to show the features carry the
structure.

## Why the standard recipe fails, with the control that shows it

The usual approach takes a pretrained encoder, discards low-level detail, and
learns a mask predictor or feature pyramid **from scratch** to upsample back.
That freshly-initialized module has seen only the finetuning categories. When
a novel object type arrives it has no prior to fall back on.

The paper tests exactly this rather than asserting it. `SimpleClick` — a
state-of-the-art promptable segmenter using the **same MAE-B backbone**,
finetuned on the **same data** — scores **1.4 to 2.4 mIoU across all seven
evaluation splits**. That is not degraded performance, it is no performance,
and it isolates the head as the culprit because everything else is held.

A second control narrows it further: attach the generative decoder (Stable
Diffusion's frozen VAE) to *discriminative* features (DINO-B) and the average
rises to 14.9, against MAE-B's 21.6 and SD's 30.9. The decoder recovers part
of the gap; the generatively pretrained encoder is the rest.

## What it buys

Finetuned on indoor furnishings and cars only — no people, no animals, one
photorealistic style — and evaluated on art, egocentric video, fine
structures and luggage x-rays:

- **COCO-Large:** 57.6 against SAM's 57.0.
- **iShape (fine, complex structures):** **51.4 against SAM's 16.8**.
- **Edge AP on BSDS500:** nearly all their models beat SAM.
- **Cost:** 29 hours on four RTX6000 Ada and **3.7M masks**, against SAM's
  68 hours on 256 A100s and 1.1B masks — roughly **0.3% of the annotation**.

Three ablations remove the rival explanations. Pretraining scale is not it:
MAE on **unlabeled ImageNet-1K alone**, no text, generalizes to art and
x-rays. Category diversity is not it: ten Hypersim classes match the full
thirty-three, and five still work. Label cleanliness is not it: finetuning on
COCO's coarse polygonal masks loses **under 5 edge-AP points**, so a model
trained on polygons does not predict polygons.

## Conditions

**It loses badly on small objects.** COCO-Medium 38.8 against SAM's 59.5,
COCO-Small **8.5 against 56.9**. If your objects are small this is the wrong
recipe today, and "approaches SAM" is an aggregate that hides it. The authors
give two candidate causes — pretraining bias toward large central objects,
and finetuning at a quarter of SAM's resolution — and separate neither.

**Prompting here is a probe, not a system.** No trained mask decoder, by
choice, to demonstrate the features carry the structure. So these numbers are
a lower bound on the method *and* not a like-for-like comparison against
SAM's engineered path — and adding a mask decoder might reintroduce the
from-scratch component that made `SimpleClick` fail, which nobody has tried.

**One task, one group.** Instance segmentation. The related work transfers
diffusion priors to depth, normals, flow and correspondence, but none of
those is a generalization-beyond-the-labels test, so the promotion condition
asks for one.

**This is not a reason to stop annotating.** [SOTA-186](SOTA-186.md) is the other
route — bootstrap a huge annotation set with the model you are training —
and it still wins where it wins. What changed is that the trade now has
numbers on both sides.

## Known implementations

- gen2seg (Stable Diffusion 2 and MAE-B/H variants), code and demo released
