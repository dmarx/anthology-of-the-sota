---
number: 109
status: Proposed
formerly:
- THEORY-tmpkf09c
promote_when: >-
  **A CLIP or SwAV Fréchet distance on guided against unguided samples at matched
  FID**, or a human preference study on the same pair — the instrument SOTA-337
  already recommends for exactly this hazard, applied to the case it names and
  nobody has run. If the non-ImageNet distance tracks FID, the trade is
  perceptual; if FID moves and CLIP-FD does not, it is the artefact
  Kynkäänniemi et al. demonstrated for pretrained discriminators, arriving
  through the sampler instead. Classifier-free guidance beating classifier
  guidance on FID and IS is not it: both are Inception-based, so a win there is
  consistent with both readings and is what this record already holds.
title: 'Classifier guidance may flatter classifier-based metrics because it steps along a classifier gradient, and guidance without a classifier is the control'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Filed with a promote_when that asked for "a feature distance from a
    self-supervised encoder" without noticing that SOTA-337 already recommends
    precisely that, names CLIP and SwAV, and lists a classifier in the sampling
    loop among the cases it suspects. The condition now names that instrument and
    that practice. Adds LIT-tmpbbn7z, read after this account was filed: the
    antecedent asserts it produces no adversarial examples in one clause of its
    introduction and runs no test — so the question was denied before it was
    raised, and unmeasured in both papers. Status stays Proposed.
tags:
- analysis-and-evaluation
- generative-modeling
date: '2026-09-25'
source:
- LIT-693
- LIT-tmpbbn7z
summary: >-
  Ho and Salimans (2022), [LIT-693](../literature.d/LIT-693.md), raising the question about the method they
  replace. Classifier guidance mixes the score with an image classifier's input
  gradient, which "can be interpreted as attempting to confuse an image
  classifier with a gradient-based adversarial attack" — and FID and Inception
  Score are both computed with an Inception classifier. So the metric gains may
  be partly adversarial rather than perceptual. Classifier-free guidance obtains
  the same trade with no classifier anywhere, which is the control, and it wins
  — but on the same classifier-based metrics. The antecedent
  (LIT-tmpbbn7z) had already asserted the
  negative, in one clause of its introduction, with no test anywhere in the
  paper. SOTA-337 names the instrument that would settle it and nobody has run
  it on guided sampling.
---

# THEORY-109: Classifier guidance may flatter classifier-based metrics because it steps along a classifier gradient, and guidance without a classifier is the control

## Source

Ho and Salimans (2022), [LIT-693](../literature.d/LIT-693.md), who raise it about their predecessor
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

## What the antecedent says about it, which is less than it looks

[LIT-tmpbbn7z](../literature.d/LIT-tmpbbn7z.md) was read after this account was filed, and it changes the shape of
the dispute rather than the verdict. **Dhariwal and Nichol got there first and
did not measure it either.** Their introduction says the gradient scale can be
raised

> by an order of magnitude without obtaining adversarial examples

citing Szegedy et al. (2013), and the word "adversarial" does not appear again
anywhere in the paper — no test, no held-out classifier, no non-Inception
distance. The nearest check is a memorization test on "a handful of samples",
run in InceptionV3 feature space, which is the same circularity one level down.

So the sequence is not "raised in 2022, already answered in 2021". It is
**asserted away in 2021 without evidence, raised in 2022, and measured by
neither.** That is why this stays `Proposed` with both papers as sources: two
documents gesture at the question and the record has no measurement from either.

**The record already owns the instrument.** [SOTA-337](../practices.d/SOTA-337.md) says that when an ImageNet
classifier is in the pipeline, FID's ranking is not to be trusted, and names CLIP
and SwAV Fréchet distances as the check; its source explicitly suspected
classifiers "placed in the sampling loop". That practice's v1 title said
"training", which is why this connection was missed when this account was filed
hours earlier the same day. The experiment is cheap, the instrument is named, and
it has not been run.

## What this does not say

**Not that classifier guidance's results were fake.** The trade it reports is
real in the sense that matters — classifier-free guidance reproduces it with no
classifier anywhere. What is open is the *magnitude* attributable to the
classifier gradient, and neither paper measured it.

<!-- inactive-ok: SOTA-301 — Proposed, and cited to be excluded: it is named as the neighbouring practice this account does *not* bear on, so its standing is irrelevant to the exclusion. -->
**Not a general claim about gradient-based guidance.** [SOTA-301](../practices.d/SOTA-301.md) recommends
applying an objective gradient before the denoiser when steering diffusion toward
a task objective; nothing here bears on that, because the objective there is not
the thing the evaluation is computed with. The concern is specifically the
coincidence between the network being differentiated and the network doing the
scoring.

**Not an argument for either method.** [SOTA-424](../practices.d/SOTA-424.md) recommends classifier-free
guidance on grounds that have nothing to do with this — one model instead of two,
no noisy-data classifier to train — and would stand if this account were
abandoned entirely.
