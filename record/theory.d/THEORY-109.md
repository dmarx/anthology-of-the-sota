---
number: 109
status: Proposed
formerly:
- THEORY-tmpkf09c
promote_when: >-
  The two guidance methods compared at matched sample quality under a metric that
  uses **no** classifier — a human preference study, or a feature distance from a
  self-supervised encoder — so that the suspicion can be separated from the
  measurement. Classifier-free guidance beating classifier guidance on FID and IS
  is not it: both of those are Inception-based, so a win there is consistent with
  both readings and is what this record already holds.
title: 'Classifier guidance may flatter classifier-based metrics because it steps along a classifier gradient, and guidance without a classifier is the control'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    The predecessor is now held and read, LIT-tmpcq7qo, and is added as a source:
    the account is about its method, and it carries the two facts that bear on
    the account from that side. Its guiding classifier is a noisy-image U-Net
    trunk, not the Inception network that scores, so the closing sentence's
    "coincidence between the network being differentiated and the network doing
    the scoring" was wrong and is corrected — the concern is transfer between two
    ImageNet classifiers. And at scale 1 it saw a classifier report ~50% on
    samples that visibly were not the class. Its own sentence against the
    suspicion ("without obtaining adversarial examples") is asserted, not tested.
    Status and promote_when unchanged.
tags:
- analysis-and-evaluation
- generative-modeling
date: '2026-09-25'
source:
- LIT-693
- LIT-tmpcq7qo
summary: >-
  Ho and Salimans (2022), [LIT-693](../literature.d/LIT-693.md), raising the question about the method they
  replace. Classifier guidance mixes the score with an image classifier's input
  gradient, which "can be interpreted as attempting to confuse an image
  classifier with a gradient-based adversarial attack" — and FID and Inception
  Score are both computed with an Inception classifier. So the metric gains may
  be partly adversarial rather than perceptual. Classifier-free guidance obtains
  the same trade with no classifier anywhere, which is the control, and it wins
  — but on the same classifier-based metrics.
---

# THEORY-109: Classifier guidance may flatter classifier-based metrics because it steps along a classifier gradient, and guidance without a classifier is the control

## Source

Ho and Salimans (2022), [LIT-693](../literature.d/LIT-693.md), who raise it about their predecessor
rather than about themselves.

## The account

Classifier guidance (Dhariwal & Nichol, [LIT-tmpcq7qo](../literature.d/LIT-tmpcq7qo.md)) improves a diffusion
model's FID and Inception Score, at a tuned scale, by mixing the model's score
estimate with the input gradient of a classifier's log probability. Both of those metrics are computed by passing samples through an
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

## What the predecessor says for itself

Dhariwal & Nichol ([LIT-tmpcq7qo](../literature.d/LIT-tmpcq7qo.md)) anticipate the worry in one sentence of their
introduction — the scale can be raised "by an order of magnitude without
obtaining adversarial examples" — and **no experiment stands behind it**: the
support is sample grids and a nearest-neighbour check run in Inception-V3 feature
space. Every number they report is Inception-based. So the predecessor does not
settle this either.

It does add two facts that change the account's shape:

- **The classifier being followed is not the classifier doing the scoring.** It
  is the U-Net's downsampling trunk with an attention pool, trained on noised
  ImageNet; FID and IS use Inception-V3. The mechanism would have to be
  *transfer* — a gradient that raises one ImageNet classifier's confidence also
  moving another's features — which is plausible, but is one step more than
  "attacking the scorer".
- **The paper observed the predicted shape once, at the low end.** On an
  unconditional model at scale 1 "the classifier assigned reasonable
  probabilities (around 50%) to the desired classes", and the samples "did not
  match the intended classes upon visual inspection"; FID got worse (26.21 →
  33.03). A classifier satisfied by images that do not look like the class is
  what the account is about. Scaling up to 10 fixed it by eye and in FID, which
  is the case the account cannot yet distinguish from a real improvement.

## What this does not say

**Not that classifier guidance's results were fake.** The paper raises a
question, does not answer it about classifier guidance, and the record holds no
paper that does — Dhariwal & Nichol ([LIT-tmpcq7qo](../literature.d/LIT-tmpcq7qo.md)), now held, assert the
opposite in one sentence and do not test it.

<!-- inactive-ok: SOTA-301 — Proposed, and cited to be excluded: it is named as the neighbouring practice this account does *not* bear on, so its standing is irrelevant to the exclusion. -->
**Not a general claim about gradient-based guidance.** [SOTA-301](../practices.d/SOTA-301.md) recommends
applying an objective gradient before the denoiser when steering diffusion toward
a task objective; nothing here bears on that, because the objective there is not
the thing the evaluation is computed with. The concern is specifically that
the network being differentiated and the network doing the scoring are both
ImageNet classifiers — not the same network, as the predecessor makes clear, but
close enough for a gradient on one to plausibly move the other.

**Not an argument for either method.** [SOTA-424](../practices.d/SOTA-424.md) recommends classifier-free
guidance on grounds that have nothing to do with this — one model instead of two,
no noisy-data classifier to train — and would stand if this account were
abandoned entirely.
