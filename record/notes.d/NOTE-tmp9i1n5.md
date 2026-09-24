---
status: Read
paper: LIT-633
title: 'AnimateDiff'
version: 1
date: '2026-09-24'
summary: >-
  Temporal-attention modules trained on video over a frozen Stable
  Diffusion 1.5 plug into community checkpoints fine-tuned from the same
  base without further tuning. Against two baselines not built for the
  task it wins clearly only on smoothness: users ranked the training-free
  Text2Video-Zero higher on preserving the personalized domain (2.620
  against 2.280), which is the property the design exists for. Version 1's
  reported failure on stylized domains was dropped in version 2, and its
  "most checkpoints" became "any".
---

# NOTE-tmp9i1n5: AnimateDiff

Read in full: arXiv v2 (8 Feb 2024, ICLR 2024) end to end, and v1 (10 Jul
2023) end to end, including its appendix. Figures are embedded animations
and were read as static frames and captions. **Not read:** the ICLR
supplementary material, which is not in either arXiv PDF. v2 defers to it
for:

- the training configuration (resolution, frame count, iterations, batch
  size, noise schedule)
- the user-study size and protocol
- the CLIP-metric implementation
- the result of the convolution-against-attention ablation
- how Tune-a-Video and Text2Video-Zero were run

The status is `Read` because every claim below is graded from what the two
PDFs contain. Where a claim's strength depends on the supplement, the
table says so and grades it as if the supplement were absent.

## Contribution

A way to animate personalized image checkpoints (DreamBooth or LoRA
fine-tunes of SD 1.5 shared on Civitai) without training anything per
checkpoint. v2 has three trained parts:

- **A domain adapter**, a LoRA on the base model's attention trained on
  video frames as still images and dropped or down-weighted at inference
  (§4.1).
- **A motion module**, a temporal transformer inserted between the frozen
  image layers with a zero-initialized output projection, trained on
  WebVid-10M (§4.2).
- **MotionLoRA**, low-rank adapters on the motion module for specific
  camera motions (§4.3).

v1 had only the motion module.

## Key insight

**If the spatial layers never change, anything fine-tuned from the same
spatial layers can borrow the motion.** The paper's argument is that
personalization "scarcely modifies the feature space of the base T2I
model" (v1 §3.2). A module trained against the base therefore reads
features of the same kind from a personalized descendant. The frozen base
is what buys the compatibility.

## Assumptions

- **Personalized checkpoints stay close to the base's feature space.**
  This is asserted, citing ControlNet (v1 §3.2), and not measured.
- **Factorized processing.** Image layers see each frame independently
  (frames folded into the batch axis), and the motion module attends only
  along time at each spatial position (§4.2). Compatibility depends on this
  split.
- **Training video is realistic** (WebVid). v1 names the gap to stylized
  domains as the cause of its failures (v1 §5).
- **Base model SD 1.5** (v2 §5). v1 says "Stable Diffusion v1" and trains
  at 256×256 on 16-frame clips sampled at stride 4 (v1 §4.1). v2's
  configuration is in the unread supplement.

## Key results

- **Quantitative comparison** (v2 Table 1). User study as average user
  ranking among three methods (higher is better), and CLIP scores:

  | method | AUR text / domain / smooth | CLIP text / domain / smooth |
  |---|---|---|
  | Text2Video-Zero | 1.620 / 2.620 / 1.560 | 32.04 / 84.84 / 96.57 |
  | Tune-a-Video | 2.180 / 1.100 / 1.615 | 35.98 / 80.68 / 97.42 |
  | AnimateDiff | 2.210 / 2.280 / 2.825 | 31.39 / 87.29 / 98.00 |

  Each AUR column sums to 6.0, as it should for three ranks.
- **Domain adapter** (Fig. 6): lowering its scale from 1 to 0 at inference
  improves visual quality and removes WebVid watermarks. This is shown on
  the first frame of one example.
- **MotionLoRA** (Fig. 7): rank 2 (about 1M parameters) looks comparable to
  rank 128 (about 36M). 50 reference videos suffice and 5 do not. 1,000 is
  also shown. §4.3 states 20–50 videos, 2,000 iterations (1–2 hours) and
  "about 30M" of storage.
- **Temporal transformer against 1D temporal convolution** at matched
  parameter count: the convolutional module "aligns all frames to be
  identical but does not incorporate any motion" (§5.3). The evidence is in
  the supplement.
- **v1 noise-schedule ablation** (v1 Table 2, Fig. 6): training with a
  linear β schedule (0.00085–0.012) rather than SD's scaled-linear schedule
  gave better colour and motion. This is qualitative, and the ablation is
  absent from v2's main text.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A motion module trained over the frozen base transfers to personalized descendants without tuning | weak | Qualitative across community checkpoints (Figs. 1, 4). One table against two baselines. Study size in the unread supplement |
| C2 | AnimateDiff gives smoother motion than the two baselines | moderate | User-study AUR 2.825 against 1.560 and 1.615. CLIP smoothness 98.00 against 96.57 and 97.42. The two measures agree |
| C3 | It preserves the personalized domain | weak | CLIP domain similarity is best (87.29), but users ranked Text2Video-Zero higher (2.620 against 2.280) |
| C4 | Text alignment is competitive | weak | Lowest CLIP text score (31.39 against 35.98). AUR level with Tune-a-Video (2.210 against 2.180) |
| C5 | The domain adapter improves quality by absorbing the video data's defects | weak | Fig. 6, one example, first frame, qualitative |
| C6 | A temporal transformer is "adequate" and a temporal convolution is not | weak | One sentence in the main text. The evidence is in the unread supplement. Listed as contribution (2) |
| C7 | MotionLoRA at rank 2 matches rank 128 and needs about 50 videos | weak | Fig. 7, qualitative. 20 videos, stated in §4.3, is not shown |
| C8 | Transfer fails when the personalized domain is far from realistic | weak | v1 §5 and Fig. 7, a stated observation. Dropped in v2 without a result that answers it |

## Method

Inflate SD 1.5 so that a 5D video tensor passes through the image layers
frame by frame. Stage 1 trains a LoRA domain adapter on the base's
self- and cross-attention, using single frames from WebVid and the image
objective. Stage 2 freezes the base and the adapter, inserts the motion
module (temporal self-attention blocks with sinusoidal position encoding
and a zero-initialized output projection behind a residual), and trains it
on video clips with the ε-prediction loss (Eq. 7). Stage 3 optionally trains
LoRA on the motion module's self-attention using rule-augmented clips
(synthetic zoom, pan and roll). At inference, drop the base weights for a
personalized checkpoint, insert the motion module, optionally add
MotionLoRA, and set the adapter scale α.

## Concepts

- **Personalized T2I:** a DreamBooth, LoRA or full fine-tune of a shared
  base, distributed as a checkpoint.
- **Domain adapter:** a disposable LoRA that absorbs the training video's
  visual defects so the motion module does not have to. It has the same
  structure as a LoRA and the opposite use: it is trained in order to be
  removed.
- **Motion prior:** what the temporal module is meant to learn,
  independent of appearance.
- **Average user ranking (AUR):** the mean rank among three methods. With
  three methods, 2.0 is average.

## Connections

It follows Video LDM / Align-Your-Latents ([LIT-621](../literature.d/LIT-621.md)), which v2's related
work says already "shows that the frozen image layers in a general video
generator can be personalized". The contribution over that is the
community-checkpoint setting and the evaluation across such checkpoints.
It uses LoRA ([LIT-046](../literature.d/LIT-046.md)) twice and zero-initialization in the ControlNet
manner. It inflates Stable Diffusion ([LIT-062](../literature.d/LIT-062.md)) as VDM does. Emu Video
([LIT-635](../literature.d/LIT-635.md)) also freezes image layers, and is the one in the record that
measures what freezing costs.

## Recommendations

- **R1.** When a video module must stay compatible with an ecosystem of
  image checkpoints, freeze the shared spatial base and train only
  temporal layers. *Topic:* adaptation-and-tuning. *Status:* experimental.
  *Strength:* weak (C1). *Conditions:* factorized architecture,
  checkpoints fine-tuned from the same base, realistic-to-moderately
  stylized domains. Nothing here says freezing costs no quality.
- **R2.** Absorb the training data's visual defects in a separate adapter
  that is removed at inference. *Topic:* adaptation-and-tuning. *Status:*
  experimental. *Strength:* weak (C5). *Conditions:* one qualitative
  ablation.
- **R3.** When the design goal is fidelity to a domain, report that
  column's human ranking, not only CLIP. *Topic:* analysis-and-evaluation.
  *Status:* standard. *Strength:* moderate. *Conditions:* the two measures
  disagree in v2 Table 1.

## Bearing on the record

| practice | disposition |
|---|---|
| [SOTA-386](../practices.d/SOTA-386.md) images before and alongside video | adoption of the first clause only, as the practice already records. The domain adapter is trained on video frames as images, which is an image-mode stage on video data, not an image corpus |
| [SOTA-390](../practices.d/SOTA-390.md) full 3D attention in video DiTs | adds a condition. AnimateDiff's compatibility requires image layers that see one frame at a time. Joint space-time attention would give up the plug-in property. It is a U-Net, not a DiT, and it runs no comparison |
| [SOTA-051](../practices.d/SOTA-051.md) zero-initialize an added branch | adoption, with no ablation |
| [SOTA-184](../practices.d/SOTA-184.md) LoRA | adoption, twice. The MotionLoRA rank finding (C7) is qualitative |
| [SOTA-187](../practices.d/SOTA-187.md) compressed latent | adoption. SD's frame-wise 2D latent with no temporal compression |
| [SOTA-389](../practices.d/SOTA-389.md) video-native captions | no bearing. Trains on WebVid's own captions |
| [SOTA-266](../practices.d/SOTA-266.md), [SOTA-333](../practices.d/SOTA-333.md) | no bearing. ε-prediction DDPM, not autoregressive |

Nothing here should produce a new practice at better than weak strength.
If one is filed from R1, it should cite Emu Video's controlled freeze
result ([LIT-635](../literature.d/LIT-635.md)) as the evidence and AnimateDiff as the setting.

## Limitations

- **Freezing is never compared with fine-tuning** in either version.
- **The baselines were not built for the task.** Text2Video-Zero is
  training-free. v1 excluded Tune-a-Video because it "requires an
  additional input video", and v2 includes it without saying in the main
  text how that requirement was met.
- **The only quantitative table has its protocol in the unread
  supplement.** The number of participants, prompts and checkpoints behind
  Table 1 is not in the PDF.
- **The limitation was removed, not resolved.** v1 §5 reported failure on
  domains "far from realistic, e.g., 2D Disney cartoon". v2 has no
  limitations section. Its abstract says "any personalized T2Is originating
  from the same base", where v1 said "most of the existing personalized
  text-to-image models". The domain adapter added in v2 targets WebVid's
  quality defects, not the realism gap, and no result shows the cartoon
  failure fixed.
- **v1's schedule ablation mislabels itself.** It calls Schedule B "the
  original schedule of SD" when its own Table 2 lists Schedule A as SD's.

## Open questions

- What does freezing cost relative to fine-tuning the spatial layers, in
  this setting? Emu Video answers it narrowly for its own model.
- How far can a checkpoint drift from the base before transfer fails? No
  measure of drift is reported.
- Does the transformer-against-convolution result hold at matched
  receptive field, and what does the supplement show?

## Corrections to the LIT note

- **"Against Text2Video-Zero and Tune-a-Video (Table 1), AnimateDiff has
  the best user-study ranks."** It has the best rank on motion smoothness
  (2.825) and a near-tie on text (2.210 against Tune-a-Video's 2.180). On
  domain similarity, Text2Video-Zero ranks higher (2.620 against 2.280).
  Fix: "AnimateDiff ranks best on smoothness and ties on text alignment.
  Users ranked Text2Video-Zero higher on domain similarity (2.620 against
  2.280), though CLIP puts AnimateDiff first there (87.29)."
- **"trained on WebVid-10M (§4.2)."** WebVid-10M training is stated in §1
  and §5. §4.2 is the module design. Fix: "(§5)".
- **Addition to the hedges.** The v1-to-v2 change is wider than the
  dropped section. The claim itself moved from "most" personalized models
  (v1 abstract) to "any" (v2 abstract) with no new evidence on the
  stylized case.
