---
number: 257
status: Proposed
formerly:
- SOTA-tmpdngkz
promote_when: >-
  A second group comparing an ensemble against a single model of the same
  total parameter count under a fixed corpus, at any scale, with the
  ensemble's members tuned for the ensemble; or a released model that was
  distilled from an ensemble trained this way. What would not move it: an
  ensemble beating a single model of the same *member* size, which is the
  comparison that has always been true and is not what this claims.
consensus: unreplicated
consensus_note: >-
  One group. The result is a comparison between two extrapolated asymptotes
  rather than between two measured losses, which is a weaker form of evidence
  than the underlying sweep — though the K=4 ensemble already beats the
  parameter-scaling limit without extrapolation.
title: 'Spend surplus compute on an ensemble of independently seeded models and distil it, rather than on one larger model'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    LIT-tmpa3ip4 (Hinton et al. 2015) added as a second source, for the
    distillation leg only. It independently measures a 10-member ensemble
    distilling into one member-sized model and keeping 86% of the gain. It
    uses a different method from LIT-441 (soft targets rather than
    sequence-level), and it says nothing about the headline comparison
    against one model of the same total size. Status and consensus are
    unchanged.
tags:
- training-optimization
date: '2026-09-19'
source:
- LIT-441
# LIT-tmpa3ip4 supports the distillation leg only ("distil to pay for it once").
# It never compares an ensemble with a single model of equal total size,
# which is this practice's claim (ADR-030).
- LIT-tmpa3ip4
introduced_by:
- LIT-441
implementations: []
summary: >-
  Kim et al. (2025), [LIT-441](../literature.d/LIT-441.md) — under a fixed corpus, training K
  models that differ only in seed and averaging their logits reaches a lower
  loss asymptote than scaling one model to the same total parameter count.
  Two 300M models beat one 600M. Members want more epochs and less weight
  decay than a standalone model, and an 8-member ensemble distils into a
  300M student retaining about 83% of the gain.
---

# SOTA-257: Spend surplus compute on an ensemble of independently seeded models and distil it, rather than on one larger model
<!-- inactive-ok-file: SOTA-255 — Proposed, and filed in this same contribution from this same source -->

## Source

Kim et al. (2025), [LIT-441](../literature.d/LIT-441.md) — [ARXIV-2509.14786](https://arxiv.org/abs/2509.14786).

## The claim, stated so the wrong version cannot be read into it

Ensembles beating single models is old and uninteresting when the comparison
is against one *member*. The claim here is against **the same total parameter
count**: `K` models of size `N` against one model of size `K·N`, under a
fixed corpus, with both recipes properly regularized first.

Two 300M models beat one 600M. In the limit, the ensembling asymptote (≈3.34)
is below the parameter-scaling asymptote (≈3.43), and even a 4-member
ensemble beats what parameter scaling reaches at infinity. The two compose:
taking members to infinity and then member size to infinity gives ≈3.13.

Members differ only in random seed — data order and initialization. Either
source of randomness alone gets most of the benefit.

## Members should be tuned for the ensemble, not as models

This is the part most likely to be skipped and it is worth ~0.17 loss. The
hyperparameters that are best for a single model are not the ones that give
the best many-member asymptote: the ensemble wants **more epochs and less
weight decay per member** — each member individually more overfit. Tuning
against the limit rather than against `K = 1` moved the asymptote from 3.34
to 3.17.

The offered explanation is Allen-Zhu and Li's multi-view account: the data
admits several sufficient feature sets, one model is biased toward learning
one of them, and independently seeded members happen to pick up different
ones. A more overfit member commits harder to its view.

## Distillation is what makes it deployable

An ensemble is `K` times the inference cost, which would normally end the
discussion. Distilling an 8-member ensemble into a single 300M student
retains **about 83%** of the gain and still beats the parameter-scaling
asymptote outright. Self-distillation — a 300M teacher into a 300M student of
identical architecture — also improves on its teacher, which removes the
large model from training as well as from serving.

The distillation leg has a second, older measurement from a different
method. Hinton et al. ([LIT-tmpa3ip4](../literature.d/LIT-tmpa3ip4.md)) distil a 10-member speech ensemble
into one model the size of a member, using temperature-softened soft targets,
and keep **86%** of the frame-accuracy gain. Kim et al. use sequence-level
distillation. Two methods, a decade apart, land at about the same fraction.
That strengthens this half and says nothing about the other.

So the practice is the pair, not the ensemble alone: ensemble to extract the
data efficiency, distil to pay for it once.

## What it is competing with

Every scaling decision in this record assumes the unit being scaled is one
model. This says that at sufficient parameter count under a fixed corpus,
that default is the wrong move — which is a claim the record has no other
document to set against, because nothing in it trains an ensemble.

The aggregate effect, combined with [SOTA-255](SOTA-255.md)'s regularization, is
reported as ~5.2x the data efficiency of the standard recipe at 200M seed
tokens, and the fitted data-scaling laws say the multiple is roughly constant
across token counts.

## Conditions, and why this is `Proposed`

**The headline comparison is between two extrapolations.** Both asymptotes
are fitted limits, and the composed figure is an asymptote of asymptotes. The
sensitivity analysis covers seed variance in the fits, not error in the
double limit. The `K = 4` result stands without extrapolation and is the part
to lean on.

One group, 200M seed tokens, members up to 1.4B. Whether ensemble scaling
still wins once members are individually under-parameterized for the corpus
is not measured, and that crossing is exactly where frontier training sits.

The comparison is at matched total parameters, not matched wall-clock or
matched engineering effort. `K` independent runs plus a distillation pass is
a different operational proposition from one run, and none of that cost
appears in the accounting.

## Known implementations

- None in the record.
