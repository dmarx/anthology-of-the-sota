---
number: 98
status: 'Active'
title: 'Monitor the training loss for unexpected spikes, for the whole run'
version: 2
history:
- version: 2
  date: '2026-10-01'
  note: >-
    Corrected from "Monitor validation loss for unexpected spikes during
    training". PaLM (LIT-069) §5.1 reports about 20 spikes in the training
    loss of the 540B model and never discusses validation loss; the body's
    argument that a validation spike separates damage from a bad batch had
    no source, and PaLM's own ablation points the other way — the spikes
    were a property of particular batches meeting a particular parameter
    state. The practice's intent, catching spikes early enough to act on
    them, is kept, and restated on the signal the source watched.
tags:
# Retagged from the report of unbound lineage. Watching for loss spikes is a
# stability check; SOTA-069, the practice it is compared against, says the
# same thing about a different statistic and already carries this topic.
- model-stability
# Secondary, restored: `training-optimization` names training dynamics, which is what is being watched (ADR-035).
- training-optimization
date: '2026-08-24'
source:
- LIT-069
# Kept at version 2. Watching a loss curve is older than any paper; what
# LIT-069 first put in print is the version stated here — spikes that come
# late and irregularly at the largest scale, through clipping — and the
# response keyed to their onset. The one earlier note that mentions loss
# spikes, MT-NLG (LIT-065, Jan 2022), tunes the optimizer against them and
# says nothing about when they come or what to do once one has.
introduced_by:
- LIT-069
compared_against:
- SOTA-069
summary: >-
  Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311). The 540B
  model's training loss spiked about 20 times, at irregular intervals,
  sometimes late, despite gradient clipping, and never in the smaller models.
---

# SOTA-098: Monitor the training loss for unexpected spikes, for the whole run

## Source

Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).

LIT-069 is the report of the phenomenon at scale. Training the 540B PaLM
model, the authors saw spikes in the loss roughly 20 times, despite gradient
clipping being on, at highly irregular intervals and sometimes late into
training; the smaller models did not show them. They found no principled
mitigation and used the restart in [SOTA-095](SOTA-095.md): back to a checkpoint about
100 steps before the spike started, skipping roughly 200–500 batches. The
signal they report is the training loss. The paper does not discuss
validation loss in this context at all.

## What the source says the watch has to cover

Three facts from that one paragraph set the shape of the practice.

**Irregular and late.** A spike can arrive at any point, so a watch that is
tightened for the early phase and relaxed once the run looks settled is
watching the wrong window.

**Despite clipping.** Clipping bounds the gradient norm; it did not
prevent these. A run with clipping on is not exempt from the watch.

**At the largest scale only.** The spikes appeared in the 540B run and not in
the smaller models, so a monitoring setup validated on
small-scale runs has not been tested against the case it exists for.

## Why it has to be per-step

The response PaLM used is defined in steps from the spike's onset: a
checkpoint about 100 steps before it, and a skip of a few hundred batches
around it. To act on that, the run has to know where the spike *started*,
which means the loss logged at a resolution of steps, not averaged over a
reporting window, and checkpoints recent enough that one sits before the
onset.

The failure this creates is specific: a loss logged or smoothed for a
dashboard — averaged over hundreds of steps because that is what the plot
wants — can blur exactly the onset the restart is keyed to. Two different
consumers of the same number, and the one nobody configures for is the one
that would have caught the problem.

## Against SOTA-069

[SOTA-069](SOTA-069.md) watches the same quantity on a different scale: `exp(loss)`, where
a spike that is small on the log axis is visible. This practice is the
watch PaLM reports keeping and acting on; that one is a choice of axis that
makes the same event easier to see. They are compatible, and neither paper
compared them.

What this practice used to add over SOTA-069 — a validation-loss watch, on
the argument that a validation spike which does not recover separates
damage from a bad batch — had no source. PaLM's own ablation argues against
the bad-batch reading in any case: the batches around a spike, replayed from
a different, earlier checkpoint, did not spike, so the authors put it down
to particular data meeting a particular parameter state.
