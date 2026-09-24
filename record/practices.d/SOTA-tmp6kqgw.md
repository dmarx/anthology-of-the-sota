---
status: Proposed
promote_when: >-
  A controlled comparison of freezing against unfreezing the spatial layers
  over the whole video-training run, not one stage. It should measure image
  quality from the same model as well as video quality, since protecting the
  image model is the stated reason to freeze. It should also include
  compatibility with community checkpoints of the same base, measured
  quantitatively.
consensus: unreplicated
consensus_note: >-
  Emu Video (LIT-635) freezes, and measured it once. AnimateDiff (LIT-633)
  freezes for compatibility and did not measure it. The large reports (Movie
  Gen, HunyuanVideo, Wan) train every parameter, so at frontier scale the
  field does the opposite. That is consistent with the practice's condition,
  since none of them serves a checkpoint ecosystem. Read as of 2026-09.
title: 'Freeze the image model''s spatial layers when adding time if checkpoint compatibility matters; do not expect a quality gain from it'
version: 1
tags:
- adaptation-and-tuning
- generative-modeling
- vision-and-graphics
date: '2026-09-24'
source:
- LIT-635
introduced_by:
- LIT-621
implementations:
- 'Video LDM'
- 'AnimateDiff'
- 'Emu Video'
summary: >-
  Girdhar et al. (2023), [LIT-635](../literature.d/LIT-635.md), and Guo et al. (2023), [LIT-633](../literature.d/LIT-633.md). Freezing a
  text-to-image model's spatial layers and training only temporal ones keeps
  the model a drop-in for checkpoints fine-tuned from the same base. Emu
  Video's one controlled test finds freezing costs nothing and gains little
  (55.0 / 58.1 against fine-tuning). The reason to freeze is compatibility,
  not quality.
---

<!-- inactive-ok-file: SOTA-386 SOTA-390 — Proposed; named here as the neighbouring practice this one must be read against, not as support -->

# SOTA-tmp6kqgw: Freeze the image model's spatial layers when adding time if checkpoint compatibility matters; do not expect a quality gain from it

## Source

Girdhar et al. (2023), [LIT-635](../literature.d/LIT-635.md) — Emu Video, Table 1. Guo et al. (2023),
[LIT-633](../literature.d/LIT-633.md) — AnimateDiff. Video LDM (Blattmann et al., 2023, [LIT-621](../literature.d/LIT-621.md)) froze
the spatial layers first, and showed its temporal layers transferring to a
DreamBooth checkpoint qualitatively.

## The claim

When a video model is built by adding temporal layers to a text-to-image
model, there is a choice: keep the image layers frozen, or train them along
with time. **Freeze them when you need the result to stay compatible with
checkpoints fine-tuned from the same image base.** Freezing is what lets
AnimateDiff's motion modules drop into DreamBooth and LoRA personalizations
of Stable Diffusion with no tuning.

Do not freeze expecting better video. Emu Video's controlled comparison
has frozen spatial layers against fully fine-tuned ones. Freezing is
preferred by 55.0% on quality and 58.1% on faithfulness (Table 1, 307
prompts, majority of 5 raters), a narrow margin with no confidence interval.
The honest reading is that freezing costs nothing measurable.

## Conditions

- **The one test is narrow.** Emu Video unfroze the spatial layers only
  during its 512px stage, and gave both arms the same conditioning images.
  So the test cannot see whether unfreezing damages the image model's own
  generation, and that is the thing freezing is meant to protect.
- **Compatibility is argued, not measured.** AnimateDiff's transfer to
  personalized checkpoints is shown by one user study against two baselines
  not built for the task. AnimateDiff leads clearly only on smoothness. The
  first version of the paper reported failure on stylized checkpoints far
  from realism, and the second version dropped that section.
- **Freezing constrains the architecture.** Full 3D attention ([SOTA-390](SOTA-390.md))
  replaces per-frame spatial attention with attention across frames. A
  frozen image model keeps its per-frame spatial layers, so time can only be
  added in new layers around them. That rules out [SOTA-390](SOTA-390.md)'s design for the
  frozen part of the network.
- **At frontier scale the field trains everything.** The large reports train
  every parameter. This practice is for the adaptation case, not for
  training a video foundation model.
- **Relation to [SOTA-386](SOTA-386.md).** That practice recommends showing the model
  images. Freezing is a third way of keeping what the image model knows,
  alongside initialization and joint training, and none of the three has
  been compared against the others at matched compute.
