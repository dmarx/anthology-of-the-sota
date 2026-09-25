---
status: Proposed
promote_when: >-
  The two guidance methods compared at matched sample quality under a metric that
  uses **no** classifier — a human preference study, or a feature distance from a
  self-supervised encoder — so that the suspicion can be separated from the
  measurement. Classifier-free guidance beating classifier guidance on FID and IS
  is not it: both of those are Inception-based, so a win there is consistent with
  both readings and is what this record already holds.
title: 'Classifier guidance may flatter classifier-based metrics because it steps along a classifier gradient, and guidance without a classifier is the control'
version: 1
tags:
- analysis-and-evaluation
- generative-modeling
date: '2026-09-25'
source:
- LIT-tmpy02tv
summary: >-
  Ho and Salimans (2022), [LIT-tmpy02tv](../literature.d/LIT-tmpy02tv.md), raising the question about the method they
  replace. Classifier guidance mixes the score with an image classifier's input
  gradient, which "can be interpreted as attempting to confuse an image
  classifier with a gradient-based adversarial attack" — and FID and Inception
  Score are both computed with an Inception classifier. So the metric gains may
  be partly adversarial rather than perceptual. Classifier-free guidance obtains
  the same trade with no classifier anywhere, which is the control, and it wins
  — but on the same classifier-based metrics.
---

# THEORY-tmpkf09c: Classifier guidance may flatter classifier-based metrics because it steps along a classifier gradient, and guidance without a classifier is the control

## Source

Ho and Salimans (2022), [LIT-tmpy02tv](../literature.d/LIT-tmpy02tv.md), who raise it about their predecessor
rather than about themselves.

## The account

Classifier guidance improves a diffusion model's FID and Inception Score by
mixing the model's score estimate with the input gradient of a classifier's log
probability. Both of those metrics are computed by passing samples through an
Inception classifier.

Taking gradient steps that maximise a classifier's confidence in a target label
is, mechanically, what an untargeted-to-targeted adversarial attack does. The
paper says so:

> because classifier guidance mixes a score estimate with a classifier gradient
> during sampling, classifier-guided diffusion sampling can be interpreted as
> attempting to confuse an image classifier with a gradient-based adversarial
> attack. This raises the question of whether classifier guidance is successful
> at boosting classifier-based metrics such as FID and Inception score simply
> because it is adversarial against such classifiers.

If that were the whole story, the reported gains would be an artefact of the
scoring apparatus rather than a fact about the images — the shape [SOTA-200](../practices.d/SOTA-200.md)
exists to make readers check.

**The control the paper builds.** Classifier-free guidance obtains the same
fidelity/diversity trade with no classifier in the pipeline at all: no classifier
to attack, no classifier gradient to follow. That the trade survives its removal
is evidence the trade is real.

## What was actually shown, and what the control cannot settle

The trade does survive. Guidance weight from 0.1 to 4.0 on ImageNet 64×64 moves
FID from 1.55 to 26.22 and IS from 66.11 to 260.2, with no classifier anywhere in
that sweep, and the qualitative effect the paper reports — less variety, more
per-sample fidelity — is what the metrics say. So the phenomenon is not an
artefact of having a classifier in the loop.

**The suspicion about the predecessor's magnitude is not settled, though,** and
the reason is that the comparison is still scored the same way. At `w = 0.3`
classifier-free guidance beats classifier-guided ADM-G on FID at 128×128. That is
one classifier-based metric preferring the method with no classifier gradient,
which is *consistent* with the adversarial reading having been wrong and equally
consistent with it having been right and the classifier-free method simply being
better. Beating a suspect measurement at its own game does not tell you whether
the measurement was suspect.

Hence the `promote_when`: the question needs a metric with no classifier in it.

## What this does not say

**Not that classifier guidance's results were fake.** The paper raises a
question, does not answer it about classifier guidance, and the record holds no
paper that does — Dhariwal & Nichol (`2105.05233`) is itself still unheld here.

<!-- inactive-ok: SOTA-301 — Proposed, and cited to be excluded: it is named as the neighbouring practice this account does *not* bear on, so its standing is irrelevant to the exclusion. -->
**Not a general claim about gradient-based guidance.** [SOTA-301](../practices.d/SOTA-301.md) recommends
applying an objective gradient before the denoiser when steering diffusion toward
a task objective; nothing here bears on that, because the objective there is not
the thing the evaluation is computed with. The concern is specifically the
coincidence between the network being differentiated and the network doing the
scoring.

**Not an argument for either method.** [SOTA-tmpfci2h](../practices.d/SOTA-tmpfci2h.md) recommends classifier-free
guidance on grounds that have nothing to do with this — one model instead of two,
no noisy-data classifier to train — and would stand if this account were
abandoned entirely.
