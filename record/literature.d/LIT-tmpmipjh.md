---
status: Active
title: 'MOVA: Towards Scalable and Synchronized Video-Audio Generation'
version: 1
tags:
- generative-modeling
- multimodal-learning
- model-architecture
- data-pipeline
date: '2026-10-06'
published: '2026-02-09'
arxiv: '2602.08794'
first_author: 'OpenMOSS Team'
keywords:
- 'video-audio-generation'
- 'image-text-to-video-audio'
- 'asymmetric-dual-tower'
- 'bidirectional-bridge-cross-attention'
- 'aligned-rope'
- 'dual-sigma-shift'
- 'dual-classifier-free-guidance'
- 'mixture-of-experts'
- 'lip-synchronization'
- 'audio-visual-captioning'
implementations:
- 'MOVA-360p, MOVA-720p (OpenMOSS)'
extends:
- LIT-619 # video tower is Wan2.2 I2V A14B, video VAE is Wan2.1's, audio tower is Wan2.1-1.3B's architecture
compared_against:
- LIT-619 # cascaded baseline: Wan2.1 for video, then MMAudio for audio (Table 4, Fig. 8)
- LIT-tmpkvsya # LTX-2 on Verse-Bench metrics and in the human arena
- LIT-tmpouvmz # Ovi on Verse-Bench metrics and in the human arena
- LIT-tmpe78xc
summary: >-
  OpenMOSS Team, Shanghai Innovation Institute, MOSI, Fudan, SJTU and others
  (2026), [ARXIV-2602.08794](https://arxiv.org/abs/2602.08794). Couples Wan2.2's 14B-active video MoE to a 1.3B
  audio DiT through a 2.6B bidirectional cross-attention bridge (32B total,
  18B active), trained 42 days on 1,024 GPUs. On Verse-Bench it leads LTX-2
  and Ovi on lip sync (LSE-C 7.800 against 6.109 and 6.378) and semantic
  alignment, and in a 5,000-vote arena it beats LTX-2 51.5% to 37.1%. The
  best rows use a guidance scale tuned on the same benchmark, the cascaded
  Wan2.1 + MMAudio baseline keeps the best DeSync (0.260 against 0.351), and
  no architectural or training choice is ablated.
extended_by:
- LIT-tmpe78xc
---

# LIT-tmpmipjh: MOVA: Towards Scalable and Synchronized Video-Audio Generation

SII-OpenMOSS Team (core contributors listed alphabetically; project leads
Qinyuan Cheng and Tianyi Liang; corresponding authors Xie Chen and Xipeng
Qiu), Shanghai Innovation Institute, MOSI Intelligence, Fudan University,
Shanghai Jiao Tong University and five other universities (2026) —
[ARXIV-2602.08794](https://arxiv.org/abs/2602.08794). Read at v2 (10 Feb 2026), main text and Appendices
A.1–A.6; v1 is 9 Feb 2026.

## Key takeaways

- **Two pretrained towers of very unequal size** (§2.2, Fig. 2, §9). The
  video tower is Wan2.2 I2V A14B, a high-noise and a low-noise 14B expert
  switched by timestep. The audio tower is a 1.3B text-to-audio DiT with
  Wan2.1-1.3B's architecture, its 3D positional encoding replaced by a 1D
  temporal one (§4.2). A randomly initialized 2.6B "Bridge" adds two
  cross-attention blocks per interaction layer, video into audio and audio
  into video. Fig. 2 draws 30 bridged video blocks and 10 video blocks
  without a bridge; the text does not say which layers are paired. Totals
  are 32B parameters and 18B active.
- **Latents** (§2.1). Video uses the Wan2.1 VAE. Audio is 48 kHz mono
  through the DAC-style VAE of HunyuanVideo-Foley. Both stay frozen.
- **Aligned RoPE** (§2.2). Video temporal indices are multiplied by the
  ratio of audio to video latent frame rate, so tokens for the same moment
  share a temporal position. It is credited to MMAudio and Ovi; Ovi scales
  the audio side down instead.
- **Independent timesteps per modality** (§4.4, Eq. 4). Training draws t_v
  and t_a separately, each through its own shift σ(t) = shift·t / (1 +
  (shift − 1)t). Phase 1 uses shift 5.0 for video and 1.0 for audio; Phase
  2 raises audio to 5.0 "to improve timbre fidelity". Audio loss weight is
  0.2 (Table 7).
- **Full end-to-end training with two learning rates** (§4.4). Bridge at
  2×10⁻⁵, towers at 1×10⁻⁵, all updated from the first step. A two-stage
  warm-start with frozen towers "reached an early performance plateau" in
  early experiments. Because FSDP needs a fixed graph, odd steps train the
  high-noise expert and even steps the low-noise one, with bridge and audio
  tower updated every step (§4.5).
- **Recipe and cost** (§4.3, Table 7). Phase 1: 360×640, 193 frames (8 s at
  24 fps), about 61,500 hours, text dropout 0.5, 15 days. Phase 2: 360p,
  about 37,600 hours (16.8M clips) filtered by OCR, lip-sync (LSE-D ≤ 9.5,
  LSE-C ≥ 4.5) and DOVER, LUFS loudness normalization, dropout 0.2, 7 days.
  Phase 3: 720×1280, about 11,000 hours, 20 days. All on 1,024 GPUs, batch
  128 at 360p and 64 at 720p, about 43,000 GPU-days, about 35% MFU with FSDP
  and USP sequence parallelism.
- **Data pipeline** (§3, Table 1, App. A.3–A.5). Clips are padded to 16:9 or
  9:16 at 720p, cut to 8.05 s around VAD speech and scene cuts, and filtered
  on Audiobox-aesthetics, DOVER, and SynchFormer offset ≤ 0.5 *or* ImageBind
  ≥ 0.2 (Table 9). 26.39% of raw duration survives Stage 2. Captions come
  from MiMo-VL (visual), Qwen3-Omni (speech transcript and non-speech) and
  GPT-OSS-120B (merging).
- **Dual CFG** (§5.1, Eq. 6, §7.2). Guidance splits into a bridge term
  (unconditional branch with cross-modal injection off) and a text term on
  top, derived from InstructPix2Pix's two-condition CFG. With s_B = 1 it
  reduces to text-only CFG.
- **Verse-Bench results** (Table 4). LTX-2 / Ovi / MOVA-360p with dual CFG
  (s_B = 3.5) / MOVA-720p: DeSync 0.451 / 0.515 / 0.351 / 0.485, IB-Score
  0.213 / 0.190 / 0.315 / 0.277, LSE-D 7.261 / 7.468 / 7.004 / 8.048, LSE-C
  6.109 / 6.378 / 7.800 / 6.593, cpCER 0.220 / 0.436 / 0.247 / 0.149. The
  Wan2.1 + MMAudio cascade has the best DeSync (0.260) and IB-Score (0.317).
- **The guidance trade-off** (Table 5). Raising s_B from 1.0 to 4.0 at 360p
  lowers DeSync from 0.475 to 0.365 and raises LSE-C from 6.278 to 7.891,
  while DNSMOS falls from 3.797 to 3.631 and cpCER rises from 0.177 to
  0.264.
- **Human arena** (§6.2.3, Fig. 8). 732 prompts (600 Verse-Bench, 132 from
  the authors' benchmark), over 5,000 votes, ELO with K = 4 and 1,000
  bootstrap rounds, each model with its own prompt rewriter. ELO: MOVA-720p
  1113.8, LTX-2 1074.1, Ovi 925.4, Wan2.1 + MMAudio 886.9. MOVA's win / tie /
  loss: 51.5 / 11.4 / 37.1% against LTX-2, 70.3 / 13.9 / 15.8% against Ovi,
  71.9 / 11.6 / 16.4% against the cascade.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Through controlled scaling studies, we find that increasing video model
  capacity … substantially improves lip synchronization, where smaller
  models show clear performance saturation"** (§9). No such study is in the
  paper. There is one model size. The scaling evidence is Fig. 9, LSE-C and
  LSE-D over the training steps of a single run, and each phase boundary
  also changes resolution, data, audio sigma shift, text dropout or loudness
  normalization. The curve cannot separate data volume from any of these.
- **The best rows are tuned on the test benchmark.** s_B = 3.5, used for the
  "w/ dual CFG" rows of Table 4, is chosen from the sweep of Table 5, which is
  run on the same Verse-Bench subsets. Table 4 does not say whether s_T was
  set equal to s_B, which decides whether those rows cost two or three model
  calls per step.
- **"MOVA virtually closes the gap"** with the cascade (§6.2.1). The cascade
  keeps the best DeSync, 0.260 against MOVA's best 0.351, and its IB-Score
  of 0.317 is above every MOVA row in Table 4. The audio-quality lead holds
  (IS 4.269 against 4.036).
- **Baselines at 720p, best rows at 360p.** §6.1 says resolution was
  standardized at 720p, but MOVA's best alignment and lip-sync numbers are
  the 360p rows. MOVA-720p without dual CFG trails LTX-2 on DeSync (0.485
  against 0.451) and LSE-D (8.048 against 7.261). The paper does not say
  what clip length or aspect ratio the baselines generated; Ovi's native
  output is 5 s at 720×720 and MOVA's is 8 s.
- **Metric subsets are small and partly self-built.** DNSMOS and lip sync
  are on Verse-Bench set3 only, and cpCER on the multi-speaker subset of the
  authors' own benchmark, scored with their own MOSS Transcribe Diarize
  model. The prompts use MOVA's [S01]/[S02] speaker-tag format and were
  unified by GPT-5. Ovi's 0.436 cpCER may partly measure prompt format.
- **No architectural or training choice is ablated.** The asymmetric
  towers, the Bridge, Aligned RoPE, independent timesteps, the two learning
  rates and end-to-end training against warm-start are each justified by a
  sentence or "in our experiments", with no numbers.
- **No variance on objective metrics.** Tables 4–6 are single numbers. The
  arena reports 95% intervals only as error bars. In the internal arena
  (Fig. 7) those bars span roughly ±30 ELO and overlap across all five
  variants, including MOVA-360p (1004.0) above MOVA-720p (982.9).
- **The audio tower's lead is partial** (Tables 2–3). Against TangoFLUX it
  is worse on KL (1.47 against 1.02), CLAP (0.463 against 0.546) and IS
  (10.54 against 13.28). The text reports only the comparison with
  AudioLDM2 for KL, and reads FD as "semantic fidelity", which FD does not
  measure.
- **Counts disagree.** The abstract says 32B total, 18B active; §8 says "a
  29B dual-tower architecture". §3.3 says only speech segments were selected
  for training, while Phase 1 data (§4.3) and the audio tower (§4.2) include
  non-speech, music and cartoons.
- **The cited Wan report does not describe the video tower.** Wan2.2's MoE
  is cited to the Wan report ([LIT-619](LIT-619.md)), which describes Wan 2.1.
- **Dual CFG has a precedent the paper does not credit.** LTX-2
  ([LIT-tmpkvsya](LIT-tmpkvsya.md)), which MOVA cites and evaluates, already guides each stream
  with a text term and a cross-modal term (its §4.1). MOVA derives its
  version from InstructPix2Pix. The nesting differs, the idea does not.

## Which comparisons are like for like

- **None against other models.** LTX-2, Ovi and the cascade are released
  models run "with recommended configurations". Nothing is retrained on
  shared data, and the cascade uses Wan2.1, not the Wan2.2 that MOVA starts
  from.
- **Within MOVA, Table 5 is clean.** One checkpoint, one benchmark, s_B the
  only change. Table 6 changes only the conditioning image (white
  placeholder for T2VA).
- **360p against 720p** (Table 4) is one model before and after Phase 3,
  which also changes data. The paper attributes the cpCER gain to "training
  data scale and training stages", not to resolution.

## Standing in the anthology

It is the backbone of Prism ([LIT-tmpe78xc](LIT-tmpe78xc.md)). Prism replaces MOVA's dense
video self-attention with content-shaped block-sparse attention and
fine-tunes at 2K. MOVA itself has no sparse attention: video self-attention
is dense (it cites FlashAttention for efficiency), audio self-attention is
dense, and the Bridge is dense cross-attention. Its own limitations section
names the problem Prism takes up. A 720p, 8 s clip is about 1.6×10⁵ tokens,
and it proposes "hierarchical or blockwise generation" as future work. It
contains no 3D tiling of attention, no block selection and no
trainable-against-training-free comparison.

It extends Wan ([LIT-619](LIT-619.md)). The video tower and video VAE are Wan weights, and
the audio tower copies Wan2.1-1.3B's architecture "to maximally reuse
engineering and training practices" (§4.2). The context-parallel VAE trick
also comes from Wan (§4.5). It also compares against Wan, as the video half
of the Wan2.1 + MMAudio cascade. That cascade has the best DeSync and
IB-Score in Table 4 but the lowest arena ELO, 886.9, and MOVA wins 71.9% of
pairs against it. Speech is what the cascade cannot do.

Against LTX-2 ([LIT-tmpkvsya](LIT-tmpkvsya.md)), the other large dual-stream open model, MOVA
leads on IB-Score (0.315 against 0.213), lip sync with dual CFG and
multi-speaker cpCER at 720p (0.149 against 0.220). It trails without dual
CFG on DeSync and LSE-D. The arena margin is the narrowest of the three:
51.5% wins against 37.1% losses, ELO 1113.8 against 1074.1. Against Ovi
([LIT-tmpouvmz](LIT-tmpouvmz.md)), whose RoPE alignment MOVA adopts, the gaps are wider: DeSync
0.351 against 0.515, IB-Score 0.315 against 0.190, cpCER 0.149 against
0.436, and 70.3% arena wins. Ovi pairs two matched 5B towers; MOVA pairs a
14B-active video MoE with a 1.3B audio tower and a 2.6B bridge. No
experiment here separates that design choice from the larger video model
and data.

Its timestep shift is Stable Diffusion 3's ([LIT-449](LIT-449.md)), applied with a
different value per modality, and its objective is rectified-flow velocity
matching ([LIT-636](LIT-636.md)). daVinci-MagiHuman ([LIT-tmpngzke](LIT-tmpngzke.md)) cites MOVA but does not
evaluate it.

Filed without a NOTE: the takeaways come from one full reading of v2, main
text and Appendices A.1–A.6. Figs. 1, 3–6 are diagrams and samples, Fig. 9
is curves, and the ELO values of Figs. 7–8 are read from their printed
labels. The caption prompts of App. A.5 were skimmed.
