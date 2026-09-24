---
number: 389
status: Proposed
formerly:
- SOTA-tmp0e0jt
promote_when: >-
  A second controlled comparison, by a group other than Movie Gen's, of
  captions from a video-native captioner against captions built from
  individual frames, with the generator, data and training budget held
  fixed. It should report motion or text-alignment separately from visual
  quality. A report that recaptions with a video model without the
  comparison does not count.
consensus: converged
consensus_note: >-
  Every video report in the record from CogVideoX on recaptions its training
  video densely with a model that takes video input: CogVideoX (LIT-622),
  HunyuanVideo (LIT-620), Wan (LIT-619), Open-Sora 2.0 (LIT-634) and
  Movie Gen (LIT-626). CogVideoX calls it a significant improvement without
  an ablation. Only Movie Gen measures it. Read as of 2026-09.
title: 'Caption training video with a model that watches the video, not with captions of its frames'
version: 1
tags:
- data-pipeline
- generative-modeling
- multimodal-learning
date: '2026-09-24'
source:
- LIT-626
introduced_by:
- LIT-626
implementations:
- 'Movie Gen'
- 'CogVideoX'
- 'HunyuanVideo'
- 'Wan2.1'
---

# SOTA-389: Caption training video with a model that watches the video, not with captions of its frames

## Source

The Movie Gen team (2024), [LIT-626](../literature.d/LIT-626.md), Table 8b.

## The claim

A text-to-video model learns what text means about motion from the
captions it trains on. **Generate those captions with a captioner that sees
the video**, not by captioning frames and rewriting the frame captions into
a paragraph.

Movie Gen compares the two at 5B, with the generator, data and budget
fixed:

- **Text alignment.** The video-captioned model wins by a net +10.8.
- **Where the gain comes from.** Almost all of it is motion alignment: +10.7
  overall and +16.1 on high-motion prompts.
- **Visual quality** is roughly unchanged (−0.8).
- **Direct caption comparison.** Raters preferred the video captions
  themselves 67% to 15%.

The gain is concentrated on the thing frame captions cannot describe.

## Why the mechanism is plausible

Make-A-Video ([LIT-632](../literature.d/LIT-632.md)) is the extreme case of the alternative. All of
its text knowledge came from images, and its discussion concedes it "can
not learn associations between text and phenomenon that can only be inferred
in videos". Frame captions are a milder version of the same limit. They can
name what is in the scene but not what happens, and "what happens" is what
separates a video model from an image model.

## Conditions

- **One controlled source.** The result is a human-rated win rate on 381
  prompts at 5B and 352×192. It has not been reproduced elsewhere, and the
  field adopted the practice without testing it.
- **The captioner matters and is not separated out.** Movie Gen's captioner
  is a Llama 3-based video model fine-tuned for the job. The comparison is
  that captioner against frame captions, so it cannot say how much a weaker
  video captioner would give.
- **Camera motion is its own problem.** Wan ([LIT-619](../literature.d/LIT-619.md) §3.3) reports that
  general multimodal models, GPT-4o and Gemini included, predict camera angle
  and motion poorly, and trains a dedicated annotator for them. If the
  captioner cannot see camera motion, captions will not teach it, whichever
  kind of model writes them.
- **The image-domain antecedent is not held.** The observation that
  descriptive synthetic captions improve prompt following, usually credited
  to DALL-E 3, is cited by Wan and is not in the record.
