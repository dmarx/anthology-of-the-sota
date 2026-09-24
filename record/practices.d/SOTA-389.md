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
  Converged in the recent reports: HunyuanVideo (LIT-620), Wan (LIT-619),
  Open-Sora 2.0 (LIT-634) and Movie Gen (LIT-626) recaption with a model
  that takes video input. CogVideoX (LIT-622) is not an example. Its
  version 1 says the reported model trained on GPT-4 summaries of per-frame
  image captions, and that its video captioner was for "the next
  generation". Only Movie Gen measures the choice. SVD (LIT-625) measured a
  related one and found the opposite (see Conditions). Read as of
  2026-09.
title: 'Caption training video with a model that watches the video, not with captions of its frames'
version: 3
history:
- version: 2
  date: '2026-09-24'
  note: >-
    Corrected against full readings of Movie Gen (NOTE-334), CogVideoX
    (NOTE-346) and SVD (NOTE-336). The motion breakdown (+10.7,
    +16.1) is in Movie Gen's prose, which says "most", not "almost all".
    Table 8b holds only −0.8 and +10.8. CogVideoX is removed as an adopter
    and as an implementation. SVD's contrary captioner result is added.
- version: 3
  date: '2026-09-24'
  note: >-
    DALL-E 3 ("Improving Image Generation with Better Captions") is now
    filed; the condition that said the image-domain antecedent was not held
    cites it, with what its controlled evidence actually measures.
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
fixed. The baseline captions three frames and rewrites the frame captions
into one caption:

- **Text alignment.** The video-captioned model wins by a net +10.8 (Table
  8b).
- **Visual quality** is roughly unchanged, −0.8 (Table 8b).
- **Where the gain comes from.** §3.6.2's prose says "most of the increase
  coming from motion alignment (+10.7%)", "particularly on prompts that…
  ask for a high degree of motion" (+16.1%). The breakdown is not in the
  table and has no σ. The +16.1 could be motion alignment or total alignment
  on the high-motion subset. The sentence allows either.
- **Direct caption comparison.** Raters preferred the video captions
  themselves 67% of the time and the frame-rewrite captions 15%.

The gain is concentrated on the thing frame captions cannot describe.

## Why the mechanism is plausible

Make-A-Video ([LIT-632](../literature.d/LIT-632.md)) is the extreme case of the alternative. All of
its text knowledge came from images, and its discussion concedes it "can
not learn associations between text and phenomenon that can only be inferred
in videos". Frame captions are a milder version of the same limit. They can
name what is in the scene but not what happens, and "what happens" is what
separates a video model from an image model.

The analogy is loose. Make-A-Video's text reaches its video decoder only
through one CLIP image embedding, so its limit is partly architectural.
Captioned video alone would not have fixed it ([NOTE-349](../notes.d/NOTE-349.md)).

## Conditions

- **SVD measured a related choice and found the opposite.** In its caption
  ablation ([LIT-625](../literature.d/LIT-625.md), App. E.2.2), CoCa, an image captioner run on each
  clip's middle frame, "surprisingly" beat the video captioner VideoBLIP on
  SVD's human-preference Elo. The two findings don't straightforwardly
  conflict. SVD's video captioner was a weak 2023 model, and Movie Gen's
  baseline was a multi-frame rewrite, not a single image caption. They do
  show that "video-native" is not enough on its own: the captioner has to be
  good at the video part. A second comparison should report which captioner
  it used.

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
- **The image-domain antecedent is weaker than its reputation.** The
  observation that descriptive synthetic captions improve prompt following
  is usually credited to DALL-E 3 ([LIT-648](../literature.d/LIT-648.md)), which Wan cites. Its
  controlled evidence is CLIP score only, not human-rated alignment, and it
  credits Parti with training on synthetic captions first.
