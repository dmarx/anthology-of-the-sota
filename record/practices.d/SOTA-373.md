---
number: 373
status: Active
formerly:
- SOTA-tmpzm1n3
consensus: emerging
consensus_note: >-
  The specific 75% is widely copied for images and the *principle* is rarely
  restated, which makes the reading awkward. What the record can point to is
  that its two masked-prediction papers sit at very different ratios — MAE at
  75% of image patches against BERT's 15% of tokens — and that `SOTA-250`'s
  masking design is argued from semantic content rather than inherited. Only
  one side of that contrast is a measurement: MAE swept the ratio and reports
  the optimum as "surprisingly high", while BERT declared 15% and never varied
  it. `emerging` because the principle is followed more often than it is
  stated, and the record has not seen it tested on a third modality. Read as of
  2026-09.
title: "Set the masking ratio by the signal's redundancy, not by the ratio that worked on text"
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Two corrections, neither touching the recommendation. The consensus note
    called BERT one of "the two masked-prediction documents it holds" and the
    record held one; BERT is now filed as LIT-670 and the claim is true.
    Worse for the argument, and the reason this matters: BERT **never swept the
    15%** — "in all of our experiments, we mask 15%", with the one appendix
    table headed "Masking Rates" varying the 80/10/10 replacement split at a
    fixed selection rate. RoBERTa (LIT-671) varies the masking schedule and
    not the rate either. So the title's "the ratio that worked on text" names a
    number that was declared rather than measured, and the practice now says so
    instead of treating it as the text-side datum.
tags:
- representation-and-encoding
- signal-structure
date: '2026-09-23'
source:
- LIT-601
- LIT-670
introduced_by:
- LIT-601
implementations: []
explained_by:
- THEORY-088
---

# SOTA-373: Set the masking ratio by the signal's redundancy, not by the ratio that worked on text

## Source

He et al. (2021), [LIT-601](../literature.d/LIT-601.md) — [ARXIV-2111.06377](https://arxiv.org/abs/2111.06377).

## The claim

A masked-prediction objective is only as good as the task it creates. If the
signal is redundant enough that a hidden region can be recovered from its
neighbours, the model learns interpolation and stops. **The masking ratio is
the knob that decides which of those two things gets learned**, and its right
value is a property of the signal.

BERT masks **15%** of tokens. MAE masks **75%** of image patches — five times
as much — and the paper calls the optimum "surprisingly high". The
justification is not a sweep: images are natural signals with heavy spatial
redundancy, so a high ratio "largely eliminates redundancy, thus creating a
task that cannot be easily solved by extrapolation from neighboring patches".

**The text end of that contrast is weaker than it looks, and the difference
matters to how this practice should be read.** BERT's own words are *"in all of
our experiments, we mask 15% of all WordPiece tokens in each sequence at
random"* — [LIT-670](../literature.d/LIT-670.md). There is no sweep of the rate in the paper. Its one
appendix table on masking is headed "Masking Rates" and varies the 80/10/10
`[MASK]`/random/unchanged substitution mix at a fixed 15% selection, which is a
different knob. RoBERTa — [LIT-671](../literature.d/LIT-671.md) — revisits BERT's recipe in detail and
varies *when* the mask is drawn, never how much of the sequence it covers.

So "the ratio that worked on text" is not a result anybody reported. 15% is a
choice from 2018 that nothing in this record shows to be right for text, which
does not weaken the recommendation — it strengthens the half that says *do not
inherit the number*. What it removes is the reading where 15% and 75% are two
measured optima whose difference needs explaining. One of them is measured.

Wettig et al. (2022), `2202.08005`, is the paper that sweeps the text side and
reports a higher optimum. The record does not hold it, and until it does, this
practice's text anchor is an unexamined default rather than a rival datum.

## How to set it for a signal nobody has done yet

The transferable procedure is the question, not the number: **can a
competent interpolator solve my masked task?** If yes, the ratio is too low,
whatever it worked out to elsewhere.

Practical proxies for redundancy — the autocorrelation of the signal, how
well a cheap baseline (nearest-neighbour, linear interpolation, a small
local model) reconstructs a masked region — are cheaper to measure than a
full pretraining sweep and answer the same question. A modality where a
trivial baseline fills the gap needs a ratio high enough to break it.

## The measurement caveat that comes with it

**Linear probing and fine-tuning disagree about the optimum**, and the paper
shows it: linear-probe accuracy rises steadily with the masking ratio to a
sweet spot, fine-tuning is flatter. So the ratio you pick depends on the
protocol you evaluate with, and a paper reporting one has made a choice it
may not have disclosed — which is `SOTA-196` exactly.

The decoder has the same property. Depth matters for linear probing; a
single-block decoder already reaches 84.8% fine-tuned.

## Conditions

- **Two modalities, one paper.** The 15%-versus-75% contrast is a comparison
  across two literatures, not a controlled experiment, and no third modality
  <!-- inactive-ok: THEORY-088 — Proposed by design: the account rests on two points from two literatures, and the practice it explains is Active regardless. Citing the open question is the point. -->
  is tested here. [THEORY-088](../theory.d/THEORY-088.md) is where the record keeps what would settle
  it.
- **Redundancy is not one number.** Spatial redundancy in images, temporal
  redundancy in video and spectral redundancy in audio are different things,
  and a single scalar ratio may not be the right control for all of them.
- **A high ratio compounds with [SOTA-372](SOTA-372.md)** — most of that practice's
  speedup is the masking ratio — so the two are usually chosen together and
  their benefits are not independent.
- **It is about the ratio, not the pattern.** MAE masks uniformly at random;
  `SOTA-250` argues for large, semantically meaningful blocks. Those are
  separate choices and this document only covers the first.

## Known implementations

-
