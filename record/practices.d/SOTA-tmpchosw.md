---
status: Active
consensus: emerging
consensus_note: >-
  The grounds are the guarantee, not adoption. The greedy recipe cannot do worse
  than the best sweep member on the held-out set by construction, so the
  downside is bounded at zero and the only cost is the averaging itself. What
  holds it short of `converged` is that the record cannot name an independent
  group reporting it — this paper and LIT-674 share a first author, so they
  are one line of work and `DP-005` says to count them as one. Read as of
  2026-09.
title: 'Average the fine-tuned models from your hyperparameter sweep instead of keeping only the best, adding each one in validation order and only if it helps'
version: 1
tags:
- training-optimization
- adaptation-and-tuning
date: '2026-09-25'
source:
- LIT-tmpay0h1
introduced_by:
- LIT-tmpay0h1
implementations:
- 'model-soups'
summary: >-
  Wortsman et al. (2022), [LIT-tmpay0h1](../literature.d/LIT-tmpay0h1.md). A hyperparameter sweep ends by discarding
  every model but one. Average them instead — sorted by held-out accuracy,
  keeping each only if held-out accuracy improves, which makes the result
  **no worse than the best individual model on that set by construction**.
  `O(1)` inference against an ensemble's `O(k)`. **+0.7 pp** on CLIP and **+0.5
  pp** on ALIGN over the best sweep member; +0.16 on ImageNet and +0.34 under
  distribution shift for ViT-G. Averaging all of them uniformly instead can come
  out *worse* than the best one.
---

# SOTA-tmpchosw: Average the fine-tuned models from your hyperparameter sweep instead of keeping only the best, adding each one in validation order and only if it helps

<!-- inactive-ok-file: SOTA-217 SOTA-408 — Proposed, both, and cited to route the reader to the neighbouring cases — the separately-trained
     one this practice does not cover, and the along-one-trajectory one it shares a precondition with. -->

## Source

Wortsman et al. (2022), [LIT-tmpay0h1](../literature.d/LIT-tmpay0h1.md) —
[ARXIV-2203.05482](https://arxiv.org/abs/2203.05482).

## What to do

At the end of a fine-tuning sweep, you have `k` models and are about to keep one.

1. Sort them by accuracy on a held-out set that is disjoint from training and
   test.
2. Start the soup with the best one.
3. Take each remaining model in order and add it to the average **only if** the
   soup's held-out accuracy improves.
4. Ship the soup.

Do **not** simply average all `k`. One ingredient fine-tuned with a learning
rate that put it in a different basin will drag a uniform average below the best
individual model, and the paper reports exactly that failure. The sorting and the
accept-only-if-it-helps test are what make this safe.

## Why this is a recommendation rather than an option

The greedy recipe "can be no worse than the best individual model on the held-out
validation set" — by construction, not by measurement. The thing you were going
to ship is the soup's first ingredient, and every subsequent step is gated on
improving. The downside is bounded at zero on the selection metric and the cost
is one averaging pass over weights you already have.

What it gains, over the best sweep member:

| | gain |
| --- | --- |
| CLIP | +0.7 pp |
| ALIGN | +0.5 pp |
| ViT-G on ImageNet | +0.16 |
| ViT-G under distribution shift | +0.34 |

And it stays one model: `O(1)` at inference, against `O(k)` for the logit
ensemble that would otherwise be the way to use all `k`.

## Conditions

**Every ingredient must be fine-tuned from the same pretrained initialization.**
This is the single-basin assumption the method rests on, and it is the same
precondition as [SOTA-407](SOTA-407.md) and [SOTA-408](SOTA-408.md): averaging works here because
the weight vectors share a trajectory. For separately trained networks,
[SOTA-217](SOTA-217.md) applies instead. The greedy recipe is best read as an admission that
even a shared initialization is not sufficient — some sweep members land
somewhere the average cannot use, which is why each one is tested rather than
trusted.

**The soup is free given the sweep, not free.** Every number above assumes you
were already training `k` models. Running a sweep in order to soup it is a
different and unmeasured proposition; the paper's NLP experiments used 32 models
per dataset.

**A held-out set gets consumed.** The greedy construction selects on it, so it
is no longer clean for reporting. Budget a third split, or accept that the
guarantee is about the set you selected on.

**The vision numbers are the real ones.** On four GLUE text-classification
tasks, the BERT greedy soup gains **+0.0, +0.7, +0.0 and +0.5** — two of four
gain nothing, and the authors call the NLP work preliminary. Treat this as
established for fine-tuning image models and as untested elsewhere.

## Known implementations

- **model-soups**, the authors' release.
