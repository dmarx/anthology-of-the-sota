---
number: 407
status: Active
formerly:
- SOTA-tmp7f0us
consensus: emerging
consensus_note: >-
  The grounds are the evidence, not adoption. One paper, but an unusually wide
  one: eleven distribution shifts, seven transfer datasets, twelve further
  backbones in the appendix, and a mechanism whose failure mode is stated and
  explained. What holds it short of `converged` is that every measurement is
  image classification, which the authors say, and that the record still cannot
  name an adopter outside the authors' own line of work. LIT-tmpay0h1 extends
  the method and shares a first author with it, so `DP-005` counts the two as
  one line rather than as a result and its replication. `Active` because the
  recommendation is free and the downside is bounded at 0.3 pp. Read as of
  2026-09.
title: 'Interpolate the zero-shot and fine-tuned weights at about half way rather than shipping the fine-tuned model'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Resolves the dependency this document's own consensus note named, and records
    that resolving it changes nothing. The note said the record could not name an
    adopter "outside the authors' own line of work — model soups, which this
    record does not yet hold". LIT-tmpay0h1 is now filed, and it shares a first
    author with this practice's source, so `DP-005` counts the two as one line of
    work rather than as a measurement and a replication. Consensus stays
    `emerging`; what changes is that the note says why instead of leaving a paper
    unread. Also nuances the image-classification limit: the *family* now has a
    non-vision data point, which the authors label preliminary and on which two
    of four tasks gain exactly nothing.
tags:
- adaptation-and-tuning
- multimodal-learning
- model-stability
date: '2026-09-25'
source:
- LIT-674
introduced_by:
- LIT-674
implementations:
- WiSE-FT
summary: >-
  Wortsman et al. (2021), [LIT-674](../literature.d/LIT-674.md). Fine-tuning a zero-shot model spends the
  robustness that made it worth starting from. Ship
  `(1 − α)·θ_zero-shot + α·θ_fine-tuned` at **α = 0.5** instead: **+3.5 to
  +23.2 pp** under six distribution shifts against the fine-tuned model, with
  reference accuracy falling **by at most 0.3 pp** and usually rising, at no
  cost in training or inference. Requires that the fine-tuned weights were
  obtained *from* the zero-shot weights.
---

# SOTA-407: Interpolate the zero-shot and fine-tuned weights at about half way rather than shipping the fine-tuned model

<!-- inactive-ok-file: SOTA-217 THEORY-010 — Proposed, both, and cited to route the reader to the separately-trained case this practice does
     NOT cover, with the account of why it is harder. Their being open is the point. -->

## Source

Wortsman et al. (2021), [LIT-674](../literature.d/LIT-674.md) —
[ARXIV-2109.01903](https://arxiv.org/abs/2109.01903).

## What to do

Keep the zero-shot weights. Fine-tune from them as usual. Then ship the average
rather than the endpoint:

    θ = (1 − α) · θ_zero-shot + α · θ_fine-tuned,    α = 0.5

`α = 0.5` is the default the paper recommends when nothing is known about the
deployment distribution, and it reports that value as close to optimal across
its experiments. Sweeping `α` costs no training, so treat it as a
free hyperparameter evaluated at deployment time — and the models it reaches are
reported to be as good as or better than those other hyperparameter settings
reach, which makes `α` a cheap substitute for part of a search.

## Why it is not a trade-off dial

The reason to state this as a recommendation rather than as an option is that
intermediate `α` beats **both** endpoints on **both** axes. Against the
fine-tuned model at `α = 0.5`, accuracy under six distribution shifts rises by
**3.5, 6.2, 1.7, 2.1, 9.0 and 23.2 pp**, while accuracy on the reference
distribution falls by **at most 0.3 pp** and frequently improves. On ImageNet
plus five derived shifts the paper reports 4–6 pp better under shift than prior
work *and* 1.6 pp better on ImageNet itself.

A method that dominates one of its endpoints and costs nothing is not a knob to
consider; it is what to do unless something rules it out.

## The condition that rules it out

**The two weight vectors must share an optimization trajectory.** This is not a
general operation on two networks that solve the same task. The paper is explicit
that averaging all layers of unrelated networks "typically fails, achieving no
better accuracy than a randomly initialized neural network", and that the
interpolation works here because the fine-tuned model came from the zero-shot
one and the two are joined by a linear path of high accuracy.

If you need to average networks that were trained separately, this practice does
not apply and [SOTA-217](SOTA-217.md) does: align the hidden-unit permutation first, for the
reason [THEORY-010](../theory.d/THEORY-010.md) gives.

## Other conditions

**Fine-tuning only a linear head makes this identical to output-space
ensembling**, algebraically, because the head enters linearly. There is nothing
wrong with using it there — it just is not a new method in that case, and a
reader should not take a linear-probe result as evidence for the end-to-end
claim.

**Image classification only.** The authors state the limitation. Every number
here is a CLIP-family classifier on image benchmarks.

The wider family has since reached text, barely: [LIT-tmpay0h1](../literature.d/LIT-tmpay0h1.md) reports greedy
soups on four GLUE tasks with gains of **+0.0, +0.7, +0.0 and +0.5** for BERT and
calls the experiments preliminary. That is a data point for weight averaging
outside vision and it is not a result for *this* practice, which nobody has run
on text.

**It preserves robustness rather than creating it.** What the interpolation
recovers is the zero-shot model's own consistency across distributions. Starting
from a model that was never robust leaves nothing to recover.

## Known implementations

- **WiSE-FT**, the authors' release.
