---
status: Active
consensus: universal
consensus_note: >-
  Not doing it is what needs justifying: every joint-embedding method the
  `#304` audit lists trains through a head and evaluates the layer before it,
  and the `#290` pass found `open_clip` exposing exactly this split — a
  backbone output and a projected embedding, with downstream users taking the
  former. It is now so standard that papers rarely restate the reason, which
  is why the reason is the part of this document worth keeping. Read as of
  2026-09.
title: 'Train through a projection head and then discard it, taking the layer before as the representation'
version: 1
tags:
- representation-and-encoding
- model-architecture
date: '2026-09-23'
source:
- LIT-tmpwwvv6
introduced_by:
- LIT-tmpwwvv6
implementations: []
---

# SOTA-tmpca2pu: Train through a projection head and then discard it, taking the layer before as the representation

## Source

Chen et al. (2020), [LIT-tmpwwvv6](../literature.d/LIT-tmpwwvv6.md) — [ARXIV-2002.05709](https://arxiv.org/abs/2002.05709), §4.2.

## The claim

Put a small nonlinear MLP between the encoder and the contrastive loss, train
through it, and then **throw it away**. The representation you ship is the
encoder output `h`, not the projected `z = g(h)` the loss was actually
computed on.

Both halves are measured on the ImageNet linear probe:

- **The head helps.** Nonlinear beats linear by about 3 points, and beats no
  head at all by more than 10.
- **The head's own output is worse than its input, by more than 10 points** —
  and this holds *with* the nonlinear head in place, so it is not an argument
  against having one.

## Why: the head is where the invariance gets absorbed

The loss demands invariance to the augmentations. Anything the two views
differ by must be discarded somewhere, and a head gives the network a place
to discard it that is not the representation.

The paper tests this rather than asserting it: train an MLP to recover the
applied transformation from each layer.

| recover from | `h` | `g(h)` | chance |
| --- | --: | --: | --: |
| rotation | **67.6** | 25.6 | 25 |
| original vs corrupted | **99.5** | 59.6 | 50 |
| original vs Sobel | **96.6** | 56.3 | 50 |
| colour vs greyscale | **99.3** | 97.4 | 80 |

`g(h)` has genuinely lost the information; `h` still has it. The head is a
sacrificial layer, and its job is to be the thing that gets damaged.

## Why it generalises past contrastive learning

The shape of the argument is: **when a loss demands a property you do not
want in your representation, give the model somewhere else to put it.** That
applies wherever the training objective is a proxy — an auxiliary head, a
task-specific decoder, an alignment layer. Whenever a pipeline ships the
tensor the loss was computed on, this is the question to ask.

## Conditions

- **Nonlinear, and small.** Linear is measurably worse; output dimension
  barely matters once a head is present.
- **It reduces the cost of a strong augmentation policy, it does not remove
  it** ([SOTA-tmp6nbsn](SOTA-tmp6nbsn.md)). Information destroyed before the encoder cannot be
  recovered after it.
- **Measured under linear evaluation on ImageNet.** Whether `h` remains the
  better choice under full fine-tuning is not what this ablation asked.
- **Which layer, exactly, is an empirical question in a deeper stack.** The
  paper compares two adjacent points; a pipeline with several projection-like
  stages has more than two candidates and should measure rather than assume.

## Known implementations

-
