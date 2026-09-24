---
status: Active
title: 'Video generation models as world simulators'
version: 1
tags:
- generative-modeling
- vision-and-graphics
- representation-and-encoding
- data-pipeline
date: '2026-09-24'
published: '2024-02-01'
url: 'https://openai.com/index/video-generation-models-as-world-simulators/'
first_author: 'Brooks'
extends:
- LIT-448
- LIT-648
compared_against:
- LIT-619
- LIT-626
keywords:
- 'spacetime-patches'
- 'diffusion-transformer'
- 'native-aspect-ratio'
- 'video-recaptioning'
- 'prompt-upsampling'
- 'emergent-simulation'
implementations:
- 'Sora'
summary: >-
  Brooks, Peebles et al., OpenAI (2024), no arXiv id. Sora is a latent
  diffusion transformer over spacetime patches of a video autoencoder's
  latents. It is trained jointly on images and videos at their native
  durations, resolutions and aspect ratios, with captions from a
  DALL-E 3-style recaptioner. The report withholds model and implementation
  details, and it has no table, number, metric or baseline. Every claim,
  including the scaling comparison and the square-crop ablation, is shown
  by example videos only. The video reports filed after it cite it and
  benchmark against it, and it supplies no measurement of its own.
---
<!-- inactive-ok-file: SOTA-386, SOTA-389 — Proposed practices Sora adopts; named to say it adds adoption, not evidence -->


# LIT-tmpv3o90: Video generation models as world simulators

Brooks, Peebles, Holmes, DePue, Guo, Jing, Schnurr, Taylor, Luhman,
Luhman, Ng, Wang and Ramesh, OpenAI (February 2024). This is a web page
with no arXiv id or PDF, and `url:` is the canonical page. openai.com
refuses this build environment (403), and web.archive.org and archive.ph
refuse the connection. It was read in full through the r.jina.ai reader
rendering of the canonical URL, retrieved 2026-09-24. That copy includes
the author list and all 32 references (reference 30, DALL-E 3, renders
empty). The embedded videos are not in it, so the claims below that rest
on videos are reported as claims.

## Key takeaways

- **The architecture, as far as it is given.** A network compresses video
  "both temporally and spatially" into a latent, with a decoder back to
  pixels. The latent is cut into spacetime patches that act as transformer
  tokens, and an image is a one-frame video. Sora "is a diffusion
  *transformer*", citing DiT ([LIT-448](LIT-448.md)). It is trained to predict the
  "clean" patches from noisy ones. The report says "Model and
  implementation details are not included". No compression factor, patch
  size, parameter count, noise schedule, objective parametrization, data
  size or attention layout is given.
- **Native size instead of crops.** The report trains at native duration,
  resolution and aspect ratio. The reason given is sampling flexibility
  (1920x1080 to 1080x1920, and quick prototyping at low size) and better
  framing. At inference the output size is set by the grid of noise
  patches, and images up to 2048x2048 are generated the same way.
- **Video recaptioning, and prompt upsampling at inference.** "We apply
  the re-captioning technique introduced in DALL·E 3 to videos". A
  "highly descriptive captioner model" captions every training video, and
  GPT expands short user prompts into long captions. The report does not
  say whether the captioner sees video or frames.
- **Conditioning on images and videos.** It animates DALL-E images,
  extends videos backward and forward (and into loops), applies SDEdit for
  zero-shot video-to-video editing, and interpolates between two videos.
- **"Emerging simulation capabilities".** 3D consistency under camera
  motion, object permanence through occlusion, simple state changes
  (brush strokes, bite marks), and Minecraft rendered with "a basic
  policy". These "emerge without any explicit inductive biases … purely
  phenomena of scale".

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **There is no measurement anywhere in it.** The report has no table,
  metric, number of samples or baseline. "Sample quality improves markedly
  as training compute increases" is supported by one set of samples
  at three compute levels (base, 4x, 32x), with seeds and inputs fixed. The claim that native
  aspect ratios improve framing compares Sora with a square-crop variant
  on examples. Neither comparison is quantified, and neither states that
  anything else was held fixed.
- **"Purely phenomena of scale" is asserted, not tested.** No smaller model
  is shown failing at the capabilities listed, and no model with a 3D or
  object prior is compared. The Discussion lists what fails (glass
  shattering, eating, incoherence over long samples, objects appearing
  spontaneously) and points to the landing page for more. Both the
  successes and the failures are sampled examples, not rates.
- **"Improves text fidelity as well as the overall quality"** is the
  recaptioning result, and it is one sentence with no evidence shown.
  DALL-E 3 ([LIT-648](LIT-648.md)), which it cites for the technique, measured CLIP score
  in a controlled setting. This report measures nothing.
- **Later papers attribute details to it that it does not contain.**
  LTX-Video ([LIT-618](LIT-618.md), §2) cites this report as proposing "an upsampler
  working directly in pixel space, conditioned on the latent outputs of the
  base model". This report says nothing about an upsampler.

## Standing in the anthology

The video reports filed after it cite it, and several benchmark against
Sora's outputs. Movie Gen ([LIT-626](LIT-626.md)) compares with Sora in a human study,
where the Sora arm used a different recipe. Wan ([LIT-619](LIT-619.md)) scores it on
VBench and on Wan-Bench, and Open-Sora 2.0 ([LIT-634](LIT-634.md)) reports its VBench
gap to it. Its standing comes from being the reference point others
measure against. Per [DP-005](../../docs/design-principles.md#dp-5), that is adoption, and it is not evidence for
any practice.

What it adopts, the record already holds as practices with better
sources:

- **Joint image and video training** is [SOTA-386](../practices.d/SOTA-386.md). Sora adopts it and does
  not ablate it.
- **Descriptive recaptioning** is [SOTA-389](../practices.d/SOTA-389.md). Sora adopts it, but its
  captioner is not described as watching video, so it is not an adopter of
  that practice's specific claim.
- **Native-size training over fixed crops** has no practice in the record.
  Sora's square-crop comparison is its only evidence here, and it is
  qualitative. A practice would need NaViT-style measurements. NaViT is
  its reference 18 and is not held.

Its lasting contribution is framing. It presents spacetime-patch diffusion
transformers as the scalable video representation and scaling as the
route to "world simulators". The report asserts both and demonstrates
neither.

Filed without a `NOTE`. This note is itself the full reading: there are
about 1,800 words of text before the references, and the evidence is in videos this reading
could not see.
