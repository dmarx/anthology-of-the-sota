---
number: 186
status: Read
formerly:
- NOTE-tmp9kngh
paper: LIT-215
title: 'V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning'
version: 1
date: '2026-09-19'
summary: >-
  I-JEPA's construction at video scale — 1M+ hours, up to 1B parameters — plus
  a second act: post-train a latent action-conditioned world model on under 62
  hours of unlabelled robot video and plan with it zero-shot on real arms.
  The scaling section attributes its gains one ingredient at a time, and the
  one worth stealing is unrelated to video: raise resolution only in the decay
  phase and pretraining costs up to 8x less.
---

<!-- inactive-ok-file: SOTA-251 — Proposed, and this note is the reading that sources it; the citation is to the practice filed from this paper, not a claim it is settled -->

# NOTE-186: V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning

## Contribution

Two things stacked. First, scaling the joint-embedding predictive
architecture to video — mask denoising in representation space, over a
million hours, at up to a billion parameters. Second, showing that the
resulting action-free model can be post-trained into an action-conditioned
world model good enough to plan with, on a very small amount of interaction
data.

## Key insight

The interesting claim is about **where the data has to come from**. Almost
all of the model's knowledge of how the world moves is learned from internet
video with no actions in it; the action-conditioning is a small amount of
post-training on 62 hours of unlabelled robot video. Planning then works
zero-shot in labs whose data was never collected.

## Concepts

- **Action-free pretraining** — the encoder never sees an action label
- **V-JEPA 2-AC** — the latent action-conditioned world model post-trained on
  top
- **Progressive-resolution training** — short, low-resolution clips through
  warmup and the constant phase, resolution and clip length raised in the
  decay

## Assumptions

- **Internet video contains the dynamics.** The whole design rests on it
- **A latent world model is good enough to plan in** without decoding to
  pixels
- **Image goals are a sufficient task specification** for the robot results —
  picking and placing, not long-horizon or contact-rich manipulation
- **The V-JEPA framework carries over**, which the paper inherits from Bardes
  et al. rather than re-arguing

## Key results

- **Motion understanding 77.3 top-1 on Something-Something v2**; **39.7
  recall-at-5 on Epic-Kitchens-100** human action anticipation, described as
  surpassing previous task-specific models. *Holds when:* those benchmarks,
  1B-parameter encoder.
- **Aligned with an LLM at 8B**: 84.0 on PerceptionTest, 76.9 on TempCompass.
- **Zero-shot robot pick-and-place on Franka arms in two labs**, from under
  62 hours of unlabelled Droid robot video, with **no data from those
  environments and no task-specific training or reward.**
- **The ablation attributes gains separately** — data 2M→22M videos +1.0,
  model 300M→1B +1.5, 90K→252K iterations +0.8, resolution and clip length
  to 88.2% for +4.0 cumulative over the ViT-L/16 baseline.
- **Progressive-resolution training is up to 8x cheaper** than training at
  full resolution throughout, in GPU-days for ViT-g on A100s.
- **Data curation beats raw scale**: cluster-based curation of YT1B
  outperforms raw YT1B at matched size.
- **A null result, reported:** fixed teacher EMA and weight-decay
  coefficients instead of ramp-up schedules showed minimal impact.

## Limitations

- **Same lab as `LIT-216`, shared authors.** This scales the line; it does not
  replicate it
- **The robot result is narrow.** Pick-and-place with image goals on two
  Franka setups. "Planning in the physical world" is the paper's framing, not
  a measured scope
- **The 8x is a projection against full-resolution training**, not a
  head-to-head run to matched quality
- **No comparison against generative video pretraining**, which is the rival
  paradigm and is exactly what `LIT-218` is about

## Connections

`LIT-216` is the parent and the `extends:` edge already records it.
`SOTA-140` is the schedule the progressive-resolution result sits inside, and
`SOTA-251` is that result as a practice. `LIT-218` is the opposing bet:
generative video models acquiring the same capabilities by a different route.

## Bearing on the record

The scaling evidence for `SOTA-250` — which is why that practice's
`consensus_note` names this paper and its `source:` does not. Per `ADR-017`,
the recommendation survives losing this paper; what it loses is the knowledge
that the construction holds at 1B parameters and a million hours.

Sources `SOTA-251` in its own right, which is the more surprising
outcome: the transferable rule in a video paper is about **schedules**, and
it belongs to `training-optimization` rather than to vision.
