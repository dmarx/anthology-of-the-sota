---
status: Active
title: 'How Does Critical Batch Size Scale in Pre-training?'
version: 1
tags:
- training-optimization
date: '2026-09-20'
published: '2024-10-01'
arxiv: '2410.21676'
first_author: 'Zhang'
corrects:
- LIT-028
keywords:
- 'critical-batch-size'
- 'data-parallelism'
- 'scaling-laws'
- 'maximal-update-parameterization'
- 'exponential-weight-averaging'
implementations: []
summary: >-
  Zhang et al. (2024), [ARXIV-2410.21676](https://arxiv.org/abs/2410.21676). Decouples model size from
  data size, which prior batch-size studies had scaled together, and finds
  critical batch size tracks the token budget and is almost flat in model
  size. Backed by an argument from muP — past a width, more width does not
  raise it — and by a least-squares analysis giving the same shape. 85M to
  1.2B on C4.
---

# LIT-tmphgpkf: How Does Critical Batch Size Scale in Pre-training?
<!-- inactive-ok-file: SOTA-097 — Superseded in this same change, and this note is half the evidence for it -->
<!-- inactive-ok-file: SOTA-062 — Superseded in this same change, and this note is the decoupling experiment that retires it -->

## Key takeaways

- **The defect it fixes is confounding, not measurement error.** Prior work
  scaled model and data together, as Chinchilla prescribes, and then reported
  critical batch size (CBS) growing "with scale". With both moving there is
  no way to say which one is responsible. This study holds each fixed in
  turn.
- **The answer is data.** Models of different sizes trained on the *same*
  token count have nearly the same CBS; at fixed model size, CBS rises with
  tokens. The fitted law in model size at fixed data is weakly dependent;
  the law in data is not.
- **The measurement needed a new instrument.** CBS is defined against steps
  to a target loss, and a decaying learning-rate schedule requires committing
  to a training duration in advance. They replace the schedule with a
  constant learning rate plus **exponential weight averaging**, which reaches
  comparable loss, permits training past any fixed horizon, and lets a run
  resume from a checkpoint until the target is hit.
- **Two theoretical supports, with different jobs.** Under muP, beyond some
  width, more width does not raise CBS — which is the model-size half. For
  mini-batch SGD on least squares under power-law source and capacity
  conditions, CBS grows as `n^a` in the sample count, and in the
  variance-dominated regime the exponent is explicit — which is the data
  half.
- **Practical consequence stated directly**: as the token budget grows, more
  data parallelism becomes available without paying in FLOPs, so serial
  training time falls for free.
- Depth and width raise CBS about equally under Chinchilla scaling, which on
  their reading is because both are proxies for the data that scaled with
  them.
- 85M–1.2B parameters, context length 512, C4, Adam, muP proxy at 151M.

## Standing in the anthology

**One of two independent measurements that retire [SOTA-097](../practices.d/SOTA-097.md).** This gives
`B_crit ∝ D^0.462`; Bergsma et al. ([LIT-tmp5olz5](LIT-tmp5olz5.md)), with a different
architecture, dataset, context length, parameterization, schedule and
hyperparameter strategy, get `0.47`. Neither is a replication of the other in
the usual sense — they did not run each other's protocol — and that is
precisely what makes the agreement informative: two ways of asking, one
answer.

**It also contradicts [SOTA-062](../practices.d/SOTA-062.md) directly.** That practice says to scale batch
size with *model* size, sub-linearly, from a 2021 heuristic. This is the
measurement that practice's own body invited: "a reader with a measurement
should prefer it". Holding data fixed, the model-size dependence very nearly
vanishes.

The relationship to [SOTA-198](../practices.d/SOTA-198.md) is subtler and is not a contradiction. That
practice says to measure the gradient noise scale rather than sweep batch
size, and to expect it to grow during a run. Nothing here disputes the
instrument; what it disputes is the *account* of what the growth tracks.
Gradient noise scale rising through a run is consistent with CBS rising in
tokens seen, and this work makes the token budget the variable rather than
the model.

The EWA instrument is worth noting on its own. A measurement protocol that
removes the need to fix the training duration in advance is reusable well
beyond this question, and the record holds no practice about it.
