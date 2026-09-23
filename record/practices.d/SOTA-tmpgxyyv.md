---
status: Active
consensus: emerging
consensus_note: >-
  Adopted where it matters and not universal. `#290`'s reading of
  `open_clip`'s pretrained table found SigLIP and SigLIP 2 checkpoints
  alongside softmax-trained CLIP, DFN and MetaCLIP — so the two losses coexist
  in the same roster rather than one having displaced the other, which is the
  honest reading. The memory argument is strongest where it is hardest to
  see: teams with few accelerators, who publish least. Read as of 2026-09.
title: 'Score each image-text pair independently with a sigmoid, so the loss needs no global normalization'
version: 1
tags:
- multimodal-learning
- distributed-optimization
- training-optimization
date: '2026-09-23'
source:
- LIT-tmprdppj
introduced_by:
- LIT-tmprdppj
extends:
- SOTA-359
implementations: []
---

# SOTA-tmpgxyyv: Score each image-text pair independently with a sigmoid, so the loss needs no global normalization

## Source

Zhai et al. (2023), [LIT-tmprdppj](../literature.d/LIT-tmprdppj.md) — [ARXIV-2303.15343](https://arxiv.org/abs/2303.15343).

## The claim

Keep the supervision ([SOTA-359](SOTA-359.md)) and change the normalization. Instead of a
softmax over the batch, score each `(image, text)` pair with a **sigmoid**
against a label that is `+1` for a true pair and `−1` otherwise.

The consequence is structural rather than statistical: a softmax term cannot
be computed until every pairwise similarity exists, and a sigmoid term can be
computed from one pair. **The loss stops needing a global view.**

## What that buys, in order of how much it matters

- **The distributed implementation collapses.** Data-parallel contrastive
  training normally needs all-gathers across devices plus the
  `|B|×|B|` similarity matrix in memory. The sigmoid form chunks: negatives
  are swapped between devices in a ring, **no all-gathers**, and only a
  `b×b` per-device block is ever materialised.
- **It is better below 16k batch, "by a large margin".** Above that the gap
  closes and the two are about equal. So the win is concentrated exactly
  where a small lab operates — the regime that published least and was
  therefore least represented in the consensus.
- **Efficiency in practice:** 84.5% ImageNet zero-shot in two days on **four
  TPUv4 chips**, with a frozen public image encoder.

## The one line you cannot omit

`|B|²−|B|` negatives against `|B|` positives means that at initialisation
"the heavy imbalance coming from the many negatives dominates the loss,
leading to large initial optimization steps attempting to correct this bias".

The fix is a **learnable bias `b`** beside the temperature, initialised
`b = −10` and `t' = log 10`, so training "starts roughly close to the prior
and does not require massive over-correction".

This is the same shape as CLIP's clipped temperature ([SOTA-359](SOTA-359.md)): a single
initialisation detail, stated once, without which the method behaves
differently. A pattern worth naming — **the papers in this cluster keep
having exactly one line that the reimplementation drops.**

## Conditions

- **It does not change what is learned, only how it is scored.** The
  supervision is still the caption and the objective is still discrimination;
  everything in [SOTA-359](SOTA-359.md)'s conditions still applies.
- **At large batch the argument is simplicity and memory, not accuracy**, and
  the authors say so. Adopting it for expected quality gains at 32k is
  adopting it for the wrong reason.
- **The chunked implementation is the point.** A naive sigmoid implementation
  that still materialises the full matrix keeps the loss's numerics and
  throws away the reason to use it.
- **Measured on image-text pairs.** The reformulation argument is general to
  any in-batch discrimination loss, and nothing here tests that.

## Known implementations

- `mlfoundations/open_clip` — SigLIP and SigLIP 2 checkpoints in its
  pretrained roster.
