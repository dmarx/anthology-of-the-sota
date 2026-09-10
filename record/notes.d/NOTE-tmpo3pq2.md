---
paper: LIT-071
status: Read
title: 'CoCa: Contrastive Captioners are Image-Text Foundation Models'
version: 1
tags:
- model-architecture
date: '2026-09-09'
summary: >-
  Trains one encoder-decoder with both a contrastive and a captioning loss by omitting cross-attention in the first half of the decoder — so those layers produce unimodal text embeddings for the contrastive loss, and the cascaded remainder cross-attends for captioning. Both objectives share one computational graph, at minimal extra cost.
---

# NOTE-tmpo3pq2: CoCa: Contrastive Captioners are Image-Text Foundation Models

## Contribution

Subsumes contrastive models (CLIP) and generative ones (SimVLM) in one
pretrained model, with a single architectural change: **the first half of the
decoder layers omit cross-attention.**

Those layers therefore compute a **unimodal** text representation, which is what
a contrastive loss against the image embedding requires. The remaining layers
cascade and do cross-attend to the image encoder, producing multimodal
representations for an autoregressive **captioning** loss. Both losses are
computed on **one forward pass through a shared computational graph**, so the
second objective is nearly free.

## Key insight

The two objectives want different things from the text tower — contrastive needs
a text embedding that has not seen the image, generative needs one that has —
and the usual response is two towers or two models. **Splitting the decoder by
depth gives both from one stack**, because "has not seen the image yet" is
exactly what the early layers of a decoder are if you withhold cross-attention.

It is a scheduling observation rather than an architectural invention: the
information you want to withhold can be withheld *for a while* instead of
permanently.

Second decision, quietly important: pretrained end-to-end from scratch on both
web alt-text and annotated images, **by treating all labels simply as text**. One
supervision format, so labelled and unlabelled data enter the same objective.

## Assumptions

- Half the decoder is enough depth for a good unimodal text representation, and
  the remaining half enough for multimodal fusion. The split point is a
  hyperparameter presented as a design.
- Labels-as-text loses nothing relative to a classification head.
- 2022 image-text scale.

## Key results

- **ImageNet: 86.3% zero-shot top-1**, **90.6%** with a frozen encoder and a
  learned classification head, **91.0%** fine-tuned — state of the art at the
  time.
- State of the art or near it across visual recognition (ImageNet,
  Kinetics-400/600/700, Moments-in-Time), crossmodal retrieval (MSCOCO,
  Flickr30K, MSR-VTT), multimodal understanding (VQA, SNLI-VE, NLVR2) and
  captioning (MSCOCO, NoCaps).
- **Minimal overhead** for the second objective, by construction.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Contrastive and generative pretraining can share one model and one graph | strong | the architecture, and it works |
| C2 | Withholding cross-attention by depth yields usable unimodal text representations | strong | the contrastive results depend on it |
| C3 | The combination beats either objective alone | moderate | strong absolute results; the ablation against single-objective baselines is the load-bearing comparison |
| C4 | Treating labels as text unifies supervised and web data | moderate | done throughout; not isolated |
| C5 | The second objective is nearly free | strong | shared forward pass |

## Method

An image encoder and a text decoder. The first half of the decoder has no
cross-attention; its output pools to a text embedding used in a contrastive loss
against the image embedding. The remaining layers cross-attend to the image
encoder and are trained with an autoregressive captioning loss. Train from
scratch on alt-text plus annotated images, labels rendered as text.

## Concepts

- **Withholding information by depth rather than by architecture** — the
  transferable idea. A representation "before" and "after" fusion from one
  stack.
- **One computational graph, two objectives** — the cost argument, and the
  reason this is a design rather than a compromise.
- **Labels as text** — a uniform supervision format, the same move `LIT-097`
  makes with timesteps.

## Connections

Sits with `LIT-080` (PaLI) and `LIT-070` in the image-text neighbourhood.
The depth-split idea is the same *kind* of move as `LIT-097`'s per-modality
timesteps: **make one model serve several objectives by varying something
continuous rather than by branching the architecture.** Two instances in this
pass.

## Recommendations

- **R1** — When two objectives need different amounts of fusion, consider
  splitting by depth rather than by branch. *Topic:* model architecture.
  *Strength:* moderate.
- **R2** — Render every supervision signal in one format so heterogeneous data
  enters the same objective. *Strength:* moderate.
- **R3** — Cost a second objective by whether it shares a forward pass.
  *Strength:* strong, and underused.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**
Image-text foundation models are not a line this anthology tracks as practice.

The reading's contribution is a second instance of a pattern. `LIT-097` unifies
several distributions by making the timestep a per-modality value; CoCa unifies
two objectives by making fusion a function of depth. Both replace an
architectural branch with a continuous variable, and both get a capability or a
saving out of it. **Two independent instances is when a pattern becomes worth
stating**, and the record states it nowhere.

The document's takeaways — "unified vision-language architecture", "contrastive
and generative learning", "zero-shot capabilities", "multi-task foundation
model" — are the fourth use of "zero-shot capabilities" in this batch as a
substitute for content, and none of them mentions the mechanism, which is one
sentence long.

## Limitations

- 2022; the absolute numbers are historical.
- The decoder split point is a design choice presented without a sweep.
- C3 needs the single-objective ablation to be conclusive and the headline is
  the absolute result.
- Nothing here transfers obviously to text-only modelling, which is the
  record's centre.

## Open questions

- How deep must the unimodal half be? The whole design turns on that number and
  it is stated rather than studied.
