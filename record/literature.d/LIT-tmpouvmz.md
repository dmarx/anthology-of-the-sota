---
status: Active
title: 'Ovi: Twin Backbone Cross-Modal Fusion for Audio-Video Generation'
version: 1
tags:
- generative-modeling
- multimodal-learning
- model-architecture
- data-pipeline
date: '2026-10-06'
published: '2025-09-30'
arxiv: '2510.01284'
first_author: 'Low'
keywords:
- 'audio-video-generation'
- 'twin-backbone'
- 'blockwise-bidirectional-cross-attention'
- 'scaled-rope'
- 'combined-prompt-conditioning'
- 'text-to-audio'
- 'text-to-speech'
- 'lip-synchronization'
implementations:
- 'Ovi (Character AI)'
extends:
- LIT-619 # video tower is Wan2.2 5B and the audio tower copies its architecture
compared_against:
- LIT-619 # human preference on video quality against the Wan2.2 5B base (Fig. 4)
- LIT-tmpe78xc
- LIT-tmpkvsya
- LIT-tmpmipjh
- LIT-tmpngzke
summary: >-
  Low, Wang and Katyal, Character AI and Yale (2025), [ARXIV-2510.01284](https://arxiv.org/abs/2510.01284). Pairs
  Wan2.2 5B with an audio tower of identical architecture trained from
  scratch, joined by bidirectional cross-attention in all 30 blocks and with
  audio RoPE frequencies scaled by 31/157 so the two token streams share a
  time axis. 50 raters prefer it to JavisDiT and UniVerse-1 in 79–91% of
  pairs on Verse-Bench (Fig. 4). There is no objective synchronization
  metric, no tie option, no clip count and no ablation of the fusion design.
  Its audio tower trails specialist models on most audio metrics, against
  numbers copied from other papers.
---

# LIT-tmpouvmz: Ovi: Twin Backbone Cross-Modal Fusion for Audio-Video Generation

Chetwin Low, Weimin Wang (project lead) and Calder Katyal, Character AI and
Yale University (2025) — [ARXIV-2510.01284](https://arxiv.org/abs/2510.01284). Read at v1 (30 Sep 2025), the
only version, main text in full; the paper has no appendix.

## Key takeaways

- **Two towers of the same shape** (§4.1, Table 1). The video tower is
  initialized from Wan2.2 5B. The audio tower has the identical
  architecture (model dim 3072, FFN 14336, 24 heads of dim 128, 30 blocks)
  and is trained from scratch. Each block adds audio-to-video and
  video-to-audio cross-attention, so the towers exchange information at
  every depth with no projection layers. The joint model is 11B.
- **Scaled RoPE aligns time** (§4.1, Fig. 2). Five seconds is 31 video
  latent frames and 157 audio latent tokens (16 kHz × 5 s / 512). Audio RoPE
  frequencies are multiplied by 31/157 ≈ 0.197, following MMAudio. The
  evidence is a plot of the cross-modal RoPE affinity matrix before and
  after, whose diagonal is misaligned without scaling.
- **One prompt for both modalities** (§3.2, §4.1). A frozen T5 encodes a
  single caption that interleaves visual events with speech in <S>…<E> tags
  and ends with an audio description in <AUDCAP> tags. Both towers
  cross-attend to the same embedding.
- **Audio tower** (§4.2.1, §4.3). Mel spectrograms through MMAudio's 16 kHz
  1D VAE, decoded by BigVGAN. Flow-matching pretraining on "hundreds of
  thousands of hours" of mostly speech up to 12 s, 50k steps at batch 2,880
  and learning rate 10⁻⁴, then fine-tuning on 5.04 s clips with sound
  effects from VGGSound, AudioSet and WavCaps. Scaled RoPE is used from the
  start, so it needs no re-adaptation at fusion.
- **Fusion training** (§4.2.2, §4.3). New cross-modal layers are trained
  from scratch with all FFNs frozen, so 5.7B of 11B parameters are
  trainable: 40k steps at batch 768 and learning rate 5×10⁻⁵. Video and
  audio get independent noise but a shared timestep, and the loss is 0.85
  video plus 0.15 audio. Sampling uses one shared schedule and the UniPC
  solver, chosen over Euler for stability.
- **Data** (§3). 121-frame clips at 24 fps, above 720×720, filtered on RAFT
  motion and an aesthetic score, balanced by face count. Speech clips are
  kept only if SyncNet gives |offset| ≤ 3 and confidence > 1.5, with mean
  volume above −60 dB. "Even a small quantity of out-of-sync data can impede
  lip-sync abilities", stated without a measurement.
- **Joint generation, human preference** (§5.3–5.4, Fig. 4). 50 participants,
  pairwise, on Verse-Bench. Ovi's win rate against JavisDiT: audio 82.4%,
  video 90.7%, sync 79.3%. Against UniVerse-1: 80.5%, 83.3%, 80.2%. On video
  quality against its own Wan2.2 base: 46.5% against 53.5%.
- **Audio tower alone** (Table 2). Ovi-Aud scores FD_PANNs 18.03, FD_VGG
  5.02, IS 11.20, CLAP 0.224, against MMAudio-L's 15.04, 4.03, 12.08, 0.348.
  TTS WER on Seed-TTS test-en is 0.035, against 0.008 for Fish Speech and
  0.018 for F5-TTS.
- **The one ablation** (§5.5, Table 3). A separate CLAP encoder for
  non-speech descriptions, against the single combined T5 prompt: FD_PANNs
  20.78 against 18.03, IS 8.34 against 11.20, CLAP 0.190 against 0.224, WER
  0.033 against 0.035.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Achieves natural synchronization"** (abstract). Synchronization is
  measured only by human preference against two baselines. There is no
  DeSync, LSE-C, LSE-D or ImageBind score. The RoPE scaling is supported by
  an affinity plot, not by a synchronization number with and without it.
- **The human study has no denominators.** 50 participants, but no count of
  prompts or pairs per comparison, no tie option (every bar sums to 100%),
  no interval, and no statement of resolution or duration for the
  baselines.
- **No fusion choice is ablated.** Symmetric towers, fusion in every block,
  bidirectional against one-way cross-attention, frozen FFNs and the shared
  timestep each come with an argument and no comparison. The only ablation
  is the text-encoder one, and it is on the audio tower before fusion.
- **"Comparable to dedicated state-of-the-art models"** (§5.4). Ovi-Aud is
  worse than three of five T2A baselines on FD_PANNs, worse than four on
  FD_VGG and CLAP, worse than two on IS, and worse than three of four TTS
  baselines on WER. All baseline numbers are copied from MMAudio's and
  F5-TTS's papers, not re-run.
- **Video quality drops.** Raters prefer the Wan2.2 base to Ovi on video
  quality, 53.5% to 46.5%. The paper calls this "marginal" and attributes it
  to the narrower audio-video data.
- **"Movie-grade"** and "cinematic storytelling" (abstract) have no metric.
  The limitations section (§6) says clips are 5 s at 720×720, sampling is
  slow at two 5B towers with CFG, and the 16 kHz VAE flattens music and
  spatial cues.
- **Data and training scale are vague.** "Millions of videos" and "hundreds
  of thousands of hours" are the only sizes. The audio-video corpus is
  internal.

## Which comparisons are like for like

- **None against other joint models.** JavisDiT and UniVerse-1 are run as
  released, with different backbones, data and output formats.
- **Against Wan2.2** the comparison is closest: Ovi's video tower starts
  from those weights, so the video-quality gap measures what fusion
  training cost. It is one human-preference number.
- **Table 3** changes only the text conditioning of the audio tower.

## Standing in the anthology

It extends Wan ([LIT-619](LIT-619.md)). The video tower is Wan2.2 5B and the audio tower
reuses its architecture block for block, which is what lets the two
exchange hidden states without projections. Wan2.2 5B and its 16×16×4 VAE
(§2.1) are cited to the Wan report, which describes Wan 2.1. Its comparison
against Wan is on video quality only, where raters prefer the Wan2.2 base
to Ovi 53.5% to 46.5%, the cost of joint training.

Every later joint model in the record measures itself against Ovi, and
every one beats it. LTX-2 ([LIT-tmpkvsya](LIT-tmpkvsya.md)) reports that its internal human
studies favour it over Ovi and that it runs faster, with no counts, win rates
or timings. LTX-2's alternative is an audio stream narrower than its video
stream, where Ovi duplicates the video architecture. daVinci-MagiHuman
([LIT-tmpngzke](LIT-tmpngzke.md)) evaluates "Ovi 1.1", a later release than this paper
describes. On VerseBench's VideoScore2 Ovi 1.1 scores 4.73 / 4.10 / 4.41
(visual quality, text alignment, physical consistency) against MagiHuman's
4.80 / 4.18 / 4.52. Its WER on TalkVid-Bench is 40.45% against 14.60%, and
raters prefer MagiHuman in 80.0% of pairs, 11.8% for Ovi. MOVA
([LIT-tmpmipjh](LIT-tmpmipjh.md)) adopts Ovi's RoPE alignment, credits it, and on Verse-Bench
measures Ovi at DeSync 0.515, IB-Score 0.190, LSE-C 6.378 and multi-speaker
cpCER 0.436, the weakest of the joint models it tests. MOVA wins 70.3% of
arena pairs against Ovi and loses 15.8%. Prism ([LIT-tmpe78xc](LIT-tmpe78xc.md)) fine-tunes Ovi
on its 2K data and scores it lowest among the open joint models in its
Table 1.

None of those comparisons isolates the twin-backbone design. Each
competitor also differs in size, data and pipeline, and two of them test a
later Ovi release. Ovi's symmetric design and Wan2.2 5B start make it the
smallest of the dual-stream models in this batch.

It uses dense attention throughout: full self-attention within each tower,
dense cross-attention between them. It has no sparse or tiled attention.
Its objective is rectified-flow velocity matching ([LIT-636](LIT-636.md)). It names DMD2
([LIT-646](LIT-646.md)) as a route to fewer sampling steps but does not try it.

Filed without a NOTE: the takeaways come from one full reading of v1, main
text and references. Fig. 3 is attention heatmaps, and Fig. 4's percentages
are read from the bar labels.
