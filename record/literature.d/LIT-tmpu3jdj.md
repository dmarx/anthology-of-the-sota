---
status: Active
title: 'Improving Image Generation with Better Captions'
version: 1
tags:
- data-pipeline
- generative-modeling
- multimodal-learning
- analysis-and-evaluation
date: '2026-09-24'
published: '2023-10-01'
url: 'https://cdn.openai.com/papers/dall-e-3.pdf'
first_author: 'Betker'
keywords:
- 'recaptioning'
- 'descriptive-synthetic-captions'
- 'short-synthetic-captions'
- 'caption-blending'
- 'caption-upsampling'
- 'prompt-following'
implementations:
- 'DALL-E 3'
compared_against:
- LIT-070
- LIT-566
summary: >-
  Betker et al., OpenAI and Microsoft (2023), no arXiv id. Identical
  T5-conditioned latent diffusion models are trained on the same images
  with alt-text, short synthetic or descriptive synthetic captions. The
  descriptive ones give higher CLIP score, and more synthetic in the blend
  is better up to the 95% tested. The controlled evidence is CLIP score
  alone, at 256px, and on ground-truth prompts the gain is inside the
  checkpoint noise. The paper does not describe the DALL-E 3 model, and it
  says its DALL-E 3 comparisons are not a measurement of recaptioning.
---
<!-- inactive-ok-file: SOTA-389 — Proposed practices this paper bears on; named as what the paper informs, not as settled advice -->


# LIT-tmpu3jdj: Improving Image Generation with Better Captions

Betker, Goh, Jing et al., OpenAI and Microsoft (2023). No arXiv id; the source is the OpenAI PDF in `url:`. Known as the DALL-E 3 paper.

## Key takeaways

- **The captioner is a CoCa-style model.** It is a language model
  conditioned on a CLIP image embedding, pre-trained with a CLIP and a
  captioning objective following Yu et al. 2022a (§2.1). It is then
  fine-tuned twice, once on main-subject captions ("short synthetic") and
  once on long captions that cover background, text in the image, style
  and colour ("descriptive synthetic") (§2.1.1, Fig. 3).
- **The controlled setup.** "Identical T5-conditioned image diffusion
  models on the same dataset of images" (§3.2). Each is trained for 500,000
  steps at batch 2048, which is 1B images. Each is a three-stage U-Net
  latent diffusion model at 256px on the SD VAE, with T5-XXL text (App.
  A). Only the caption source varies. Model size is not given. The metric is
  CLIP-S (ViT-B/32) on 50,000 generations with EMA weights.
- **Three caption types were compared** (§3.3, Fig. 4). The models trained
  on alt-text only, on 95% short synthetic and on 95% descriptive
  synthetic. They were scored with ground-truth captions (Fig. 4 left) and
  with descriptive ones (Fig. 4 right). Read off the right panel at 500K,
  the scores are about 33.5, 33.1 and 32.8. The paper tabulates none of
  these numbers.
- **The blend ratio.** 65%, 80%, 90% and 95% descriptive synthetic were
  compared, with the remainder alt-text drawn at random per sample (§3.1,
  §3.4). The 65% run was dropped midway as "far behind". In Fig. 5, which
  has three checkpoints per run, 95% ends near 29.8 and 90% and 80% end
  near 29.4. The blend exists to stop the model overfitting to the
  captioner's formatting quirks (§3.1).
- **DALL-E 3 trains on 95% synthetic and 5% ground truth** (§4). A model
  trained this way wants long prompts at inference. So GPT-4 "upsamples"
  user prompts to match (§3.5, App. C).
- **The system comparison.** Against DALL-E 2 and SDXL, CLIP score on 4,096
  MSCOCO captions is 32.0 / 31.4 / 30.5. GPT-V Drawbench accuracy is 70.4%
  / 49.0% / 46.9%, rising to 81.0% / 52.4% / 51.1% with upsampled prompts.
  T2I-CompBench colour binding is 81.1% / 59.2% / 61.9% (Table 1). Human
  prompt-following Elo is 153.3 for DALL-E 3, −104.8 for Midjourney 5.2 and
  −189.5 for SDXL, over 170 prompts (Table 2).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Reliably improves prompt following" rests on CLIP score.** In Fig. 4
  (left), on ground-truth prompts, all three curves swing about 0.3 between
  checkpoints. The final short-synthetic point sits below the alt-text
  one. §3.3 calls the gain "slightly better" and concludes "no downside".
  The large gap is on descriptive prompts, the captioner's own distribution
  (Fig. 4 right). No image-quality metric and no human rating is reported
  for the controlled models.
- **Figs. 4 and 5 do not reconcile.** Both use ground-truth-caption
  evaluation, and the 95%-descriptive run appears in both. It scores about
  27.0 in one figure and 29.8 in the other. The paper does not explain the
  difference.
- **The DALL-E 3 tables are not evidence for recaptioning.** Footnote 5:
  DALL-E 3 has "many improvements … not covered … and could not be
  ablated", and the evaluation "should not be construed as a performance
  comparison resulting from simply training on synthetic captions".
  §1 says it "does not cover training or implementation details of the
  DALL-E 3 model". It discloses the captioner recipe, the ablation decoder
  and a latent decoder (a DDPM U-Net, consistency-distilled to two steps,
  App. B). It does not give DALL-E 3's size, data, resolution or
  architecture, or the captioner's size or data.
- **The judges have limits.** GPT-V was "not better than random" on
  counting (§4.2.1). MSCOCO was not de-duplicated from training (fn. 6).
  In the prompt-following human eval, raters saw the upsampled prompt.
- **It is not the first use of synthetic captions.** §1 credits Parti with
  the technique and claims the measurement as its own contribution.

## Standing in the anthology

[SOTA-389](../practices.d/SOTA-389.md)'s Conditions list this as its image-domain antecedent, not held
until now. Wan ([LIT-619](LIT-619.md)) cites it for descriptive recaptioning ([NOTE-333](../notes.d/NOTE-333.md)).
Filing it makes [SOTA-389](../practices.d/SOTA-389.md)'s footnote checkable, and the result is narrower
than "usually credited" suggests. The variable here is descriptiveness
and synthetic versus web text, not whether the captioner sees the medium
being generated. The measure is CLIP score, not human-rated alignment. So
it supports [SOTA-389](../practices.d/SOTA-389.md)'s premise that better captions teach prompt following,
and it says nothing on video-native captioners.

Two findings here have no practice in the record: blending about 5% human
captions to regularize caption style, and rewriting prompts at inference to
match the training caption distribution. Movie Gen ([LIT-626](LIT-626.md)) rewrites
prompts with LLaMa3 ([NOTE-334](../notes.d/NOTE-334.md)), which is the video form of the second.

Filed without a `NOTE`: the takeaways come from one full reading of the
19-page PDF (PDF metadata dated 2023-10-31), appendices included, done for
this filing. The Fig. 4 and Fig. 5 values were read off rendered plots
because the paper gives no table for them.
