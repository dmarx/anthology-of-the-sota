---
number: 346
status: Read
formerly:
- NOTE-tmpkkcdb
paper: LIT-622
title: 'CogVideoX'
version: 1
date: '2026-09-24'
summary: >-
  An open text-to-video DiT whose design choices are backed by curves rather
  than numbers. On full 3D against factorized attention, the text says only
  that factorized FVD is "much higher … in early steps" and that factorized
  training is "unstable and prone to collapse". Model size, steps and
  resolution are unstated. The one measured number is the cost: full
  attention's forward pass is 1.08×, 1.67× and 2.30× slower at three sizes.
---

<!-- inactive-ok-file: SOTA-333 SOTA-386 SOTA-389 SOTA-390 — Proposed, and cited here to weigh the evidence for them; this document is part of that evidence, not an endorsement -->

# NOTE-346: CogVideoX

Read in full from arXiv v3 (26 Mar 2025, the ICLR 2025 version), appendices
A–K included. v1 (12 Aug 2024) was read in full to compare where versions
differ. v2 was not available, so "added in v3" below means "absent from v1,
present in v3". The figures were not viewed, because this environment cannot
render PDF pages, and their values are not in the extracted text. Where a
result lives only in a plot, this note gives its direction and says so.

## Contribution

A text-to-video diffusion transformer, released at 2B and 5B with weights,
VAE and captioner. It has four parts. The first is a causal 3D VAE at
8×8×4 compression with 16 latent channels. The second is a single sequence
of T5 text tokens and video patches with modality-specific adaLN ("expert
adaLN"). The third is full attention over that sequence. The fourth is a
data pipeline: six Video-LLaMA negative-label filters and a dense
recaptioning pipeline. Training uses v-prediction with zero terminal SNR,
mixed-duration packing, progressive resolution and a per-rank
timestep-stratification trick.

## Key insight

**The attention argument is a picture, and the evidence is a curve.** The
case for full 3D attention is Figure 5. Under factorized attention a moving
head in frame i+1 "cannot directly attend to the head in frame i", so the
information has to pass "implicitly … through other background patches".
The ablation that backs it (Figs. 8b, 10b) is described in two sentences and
has no setup. The cost side, by contrast, is a table (Table 8). Of the two
halves of [SOTA-390](../practices.d/SOTA-390.md), the paper measures the cost more carefully than the
benefit.

## Assumptions

- A compressed latent: the ablation's VAE and patch size are not stated.
  Variant B (8×8×4, 16 channels) is "used for pretraining" (Table 1).
- A T5 text encoder, text length 226 (App. Table of hyperparameters).
- Diffusion with v-prediction and zero SNR on the LDM schedule (§3), with
  uniform timesteps made explicit per rank (§3.3).
- FlashAttention makes full attention affordable: "the increase in sequence
  length does not make the inference time unacceptable" (Table 8 caption).

## Key results

**The full-attention ablation, as the text states it** (§4.1). "In Figure 8b
and Figure 10b, when we replace 3D full attention with 2D + 1D attention,
the FVD will become much higher than 3D attention in early steps. We also
observe that 2D+1D is unstable and prone to collapse. We suppose that as the
model size increases, such as 5B, training becomes more prone to
instability." The setup the text gives: FVD on "WebVid test dataset with 500
videos" (Fig. 8 caption), and a training-loss curve (Fig. 10b). The text does
not give model size, training steps, resolution, frame count, patch size,
parameter matching between the two variants, or any FVD value. It does not
say the gap persists past "early steps". It says nothing about Fig. 10b's
loss curve beyond citing it. The 5B sentence is a supposition, and it
leaves unclear whether the ablated model was 5B.

**The cost** (App. Table 8). One DiT forward step, bf16, H800. Model size
not stated.

| input | 2D+1D | 3D full | ratio |
|---|---|---|---|
| 256×384×6s | 0.38s | 0.41s | 1.08× |
| 480×720×6s | 1.26s | 2.11s | 1.67× |
| 768×1360×5s | 4.17s | 9.60s | 2.30× |

**VAE** (Table 1). Flicker is the L1 difference between adjacent frames.

| variant | compression | channels | flicker ↓ | PSNR ↑ |
|---|---|---|---|---|
| SDXL 2D | 8×8×1 | 4 | 93.2 | 28.4 |
| A | 8×8×4 | 8 | 87.6 | 27.2 |
| B (used) | 8×8×4 | 16 | 86.3 | 28.7 |
| C | 8×8×4 | 32 | 87.7 | 30.5 |
| D | 8×8×8 | 32 | 87.8 | 29.0 |
| E | 16×16×8 | 128 | 87.3 | 27.9 |

At 16×16×8 "the convergence of the model also becomes extremely difficult",
with no numbers. Against other open 3D VAEs at 256², 17 frames: flicker 85.5
and PSNR 29.1, against Open-Sora 92.4 / 28.5 and Open-Sora-Plan 90.2 / 27.6
(Table 2). The paper does not explain why its own row differs from variant B.

**Expert adaLN** (Figs. 8a, 8d, 10c). Compared against no expert adaLN,
against MMDiT at equal parameters ("MMDiT1") and against MMDiT at equal
depth with twice the parameters ("MMDiT2"). It "significantly outperforms"
the first two on FVD, CLIP4Clip and loss. No values are given. Cross-attention
DiT was not run: "shown to be inferior to MMDiT in (Esser et al., 2024), so
we don't repeat."

**Explicit uniform sampling** (Table 9, validation loss at 40k steps):
0.222/0.130/0.119/0.133/0.161 without it and 0.216/0.126/0.116/0.129/0.157
with it, at t = 100/300/500/700/900.

**RoPE against sinusoidal** (Fig. 10a): RoPE's loss "converges significantly
faster". The released 2B model uses sinusoidal encoding and the 5B RoPE
(appendix hyperparameter table).

**System evaluation.** CogVideoX-5B is best on 5 of 7 selected VBench and
dynamics metrics (Table 3). On a 100-prompt human rating it outscores Kling:
total 2.74 against 2.17 (Table 4). The rater count is not given, and scores
are absolute 0/0.5/1 ratings, not pairwise preferences (App. J).

**Data.** About 35M single-shot clips averaging 6s, plus 2B aesthetics-
filtered images from LAION-5B and COYO-700M (§3.4). The filter classifiers
reach 0.89–0.99 test accuracy (Table 14).

## What changed between v1 and v3

- **The attention and adaLN-vs-MMDiT ablations are absent from v1.** v1's
  ablations were four loss curves: RoPE vs sinusoidal, RoPE vs RoPE plus
  learnable absolute, expert adaLN vs expert adaLN plus expert MLP, and
  uniform sampling. v3 drops two of them.
- **Captions.** v1 states that "the pipeline above", Panda-70M short video
  captions plus per-frame CogVLM image captions summarized by GPT-4 and then
  a fine-tuned Llama 2, "generates the caption data that is used to train
  the CogVideoX model introduced in this report". v1 also says data from the
  video-input CogVLM2-Caption "is used to train the next generation". v3
  deletes both sentences and says only that the pipeline recaptions "all
  video training data".
- **Resolution.** v1's introduction says the open-sourced model generates
  720×480, 6s, 8 fps. v3's abstract says 768×1360, 10s, 16 fps.
- **Table 3 (v1 Table 1).** The CogVideoX-2B row changed (e.g. Human
  Action 88.0 → 96.6, Scene 39.94 → 55.35). The 5B row and the Kling table
  (Table 4 / v1 Table 2) are identical.
- **Other.** v1 did not patchify in time. v3 allows a temporal patch q, with
  the value not stated. v1's VAE loss is L2 + LPIPS + GAN; v3's is L1 + LPIPS
  + KL, with GAN added later. The image corpus appears only in v3.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Full 3D attention reaches lower FVD than 2D+1D early in training | weak | Fig. 8b, no values; setup unstated |
| C2 | 2D+1D training is unstable and prone to collapse | weak | observation, no runs or rates shown |
| C3 | Full attention costs 1.08× to 2.30× the forward time, growing with sequence length | strong | Table 8, a direct measurement; model size unstated |
| C4 | A causal 3D VAE flickers less than a frame-wise 2D VAE | moderate | Table 1; one metric the authors define |
| C5 | 16×16×8 compression makes the generator hard to train | weak | asserted |
| C6 | Expert adaLN beats MMDiT at equal parameters | weak | Figs. 8a/8d/10c, no values; model size unstated |
| C7 | Explicit uniform sampling lowers loss at every timestep | moderate | Table 9; one run, gaps 0.003–0.006 |
| C8 | Dense recaptioning "significantly improves" generation | weak | asserted in abstract and §1; no ablation in either version |
| C9 | CogVideoX-5B beats Kling on human evaluation | weak | Table 4; one system comparison, rater count unstated |
| C10 | Top-20% quality fine-tuning removes watermarks and subtitles at a slight semantic cost | weak | App. A, no numbers |
| C11 | Fixed-frame joint image-video training splits into two generative modes | weak | observation (§3.1) |

## Concepts

- **Expert adaLN** — one transformer stack over the concatenated sequence,
  with separate timestep-conditioned adaLN parameters for text and vision
  tokens.
- **3D full attention** — attention over all text and video tokens at once,
  against 2D spatial attention plus 1D temporal attention.
- **Explicit uniform sampling** — split [1, T] into one interval per
  data-parallel rank so each batch covers the timesteps evenly.
- **Multi-resolution frame pack** — pack clips of different duration and
  resolution into one batch, with RoPE extrapolated rather than interpolated.

## Connections

Takes its VAE from MAGVIT's causal convolution, its single-sequence design
from DiT and SD3's MMDiT ([LIT-449](../literature.d/LIT-449.md)), and its I2V conditioning from SVD
([LIT-625](../literature.d/LIT-625.md)). Successors kept the full attention and the VAE ratio and dropped
the expert adaLN, per [LIT-622](../literature.d/LIT-622.md).

## Recommendations

- **R1** — Budget full spatio-temporal attention as a cost that grows with
  token count: 1.08× at 256×384 and 2.30× at 768×1360 for one forward pass.
  *Topic:* attention-techniques. *Status:* standard. *Strength:* strong.
  *Conditions:* H800, FlashAttention, one unstated model size.
- **R2** — Prefer full attention to factorized attention in a video DiT.
  *Topic:* attention-techniques. *Status:* experimental. *Strength:* weak.
  *Conditions:* one comparison, early training, setup unstated.
- **R3** — Stratify diffusion timesteps across data-parallel ranks.
  *Topic:* training-optimization. *Status:* experimental. *Strength:*
  moderate. *Conditions:* small loss gains, one run, no sample-quality
  measure.

## Bearing on the record

- **[SOTA-390](../practices.d/SOTA-390.md): direction confirmed, and the body overstates the source.**
  The text supports "lower FVD early, and the factorized model is unstable".
  Four statements in the practice are not in the text. First, "with
  everything else fixed (Fig. 8)": nothing is said to be fixed. Second,
  "wins on … training loss": Fig. 10b is cited without comment. Third,
  "made at 8×8×4 compression with 2×2 patches": no patch size appears in
  v3. Fourth, "appears only in the paper's third arXiv version": it is absent
  from v1, and v2 was not read. It should also say that 2.3× is inference
  time at one resolution, 1.67× at 480×720, and that the instability means a
  later-step FVD comparison may be comparing against a collapsed run.
  `promote_when` stands.
- **[SOTA-389](../practices.d/SOTA-389.md): the consensus note mislabels CogVideoX.** v1 says the reported
  model trained on captions built by summarizing per-frame image captions,
  with a short Panda-70M video caption as one input. That is closer to the
  frame-caption arm Movie Gen tested against than to a video-native
  captioner. CogVLM2-Caption, which does watch the video, was trained on
  those summaries and used for "the next generation".
- **[SOTA-386](../practices.d/SOTA-386.md):** CogVideoX trains on 2B images alongside 35M clips, untested.
  That is adoption. §3.1 notes that fixed-length joint training "diverge[s]
  into two generative modes", and uses that to motivate frame packing.
  That is an unmeasured caveat on the "alongside" clause.
- **[SOTA-187](../practices.d/SOTA-187.md):** Table 1 is video evidence for the practice's condition that
  compression is a trade. Channels raise PSNR at fixed ratio, and the most
  aggressive ratio is reported as hard to train.
- **[SOTA-195](../practices.d/SOTA-195.md), [SOTA-266](../practices.d/SOTA-266.md):** v-prediction with zero SNR and uniform timesteps.
  That is adoption; no test.
- **[SOTA-333](../practices.d/SOTA-333.md):** no bearing.
- **Should produce:** nothing new at `Active`. R3 is too thin, and R1 belongs
  in [SOTA-390](../practices.d/SOTA-390.md)'s cost paragraph.

## Limitations

- No architecture ablation states its model size, steps or resolution. The
  appendix stage table lists 400k + 220k + 120k + 10k = 750k steps for the
  released models, with batch falling from 2000 to 100.
- Every ablation value is in a plot.
- Evaluation mixes a selected subset of VBench with a human rating against
  one closed system.
- The captioning claim, the most repeated one, has no ablation.

## Open questions

- Does the full-attention FVD gap persist once the factorized model is
  stabilized? The text leaves open whether it is a quality gap or a
  stability gap.
- Which captions trained the v3 checkpoints, given v1's statement and v3's
  silence?
- What produced the changed 2B VBench row?

## Corrections to the LIT note

- **"Full 3D attention … wins on FVD and loss (Fig. 8)."** The text says
  factorized FVD is "much higher than 3D attention in early steps", and that
  2D+1D is "unstable and prone to collapse". The loss curve is Fig. 10b and
  the text makes no claim about it. Fix: "It has lower FVD early in training
  (Fig. 8b), and the factorized variant is reported unstable. No values are
  given."
- **Summary: "Full 3D attention beats factorized attention at 2.3× the
  forward cost."** 2.3× is the inference forward-step time at 768×1360×5s.
  It is 1.67× at 480×720×6s and 1.08× at 256×384×6s (Table 8). Fix: "at
  1.1× to 2.3× the forward time, rising with resolution."
- **"Version 1 claims 720×480, 6s at 8 fps."** v1's abstract states no
  resolution. The figure is in v1's introduction and describes the
  open-sourced model. Fix: "Version 1's introduction gives the open model as
  720×480, 6s at 8 fps."
- **"The architecture ablations (Figs. 8 and 10) appear in version 3."**
  Absent from v1, present in v3; v2 was not checked. v1 did have ablations,
  as loss curves, two of which v3 dropped. Fix accordingly.
- **Missing, and worth adding under hedges:** v1 says the reported model's
  captions came from the frame-caption summarization pipeline. v3 removed
  the sentence. The 2B VBench row also changed between versions while the
  5B row and the Kling table did not.
