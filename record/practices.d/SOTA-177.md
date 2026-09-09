---
number: 177
status: Proposed
formerly:
- SOTA-tmpk6q3n
promote_when: >-
  A released model whose linear layers carry a decoupled erase, or an
  independent group running an addressed erase against a channel-wise decay
  gate — the record holds both answers to the same pressure and nobody has
  compared them. What would not move it: a further gain from this group at a
  third scale.
consensus: unreplicated
consensus_note: >-
  One group, two scales, no deployment. The rival answer to the same problem
  — a channel-wise forgetting gate — ships at 2.8T, so the comparison that
  matters is available to somebody and has not been run.
title: 'Decouple the erase address from the write address in a delta-rule recurrence'
version: 1
tags:
- attention-techniques
date: '2026-09-08'
published: '2026-06-01'
source:
- LIT-177
extends:
- SOTA-135
implementations: []
summary: >-
  Li et al. (2026), [LIT-177](../literature.d/LIT-177.md) — the delta rule corrects what is stored at the
  *current write address* before writing there, so stale information at a
  different address can only decay passively. EDA runs a targeted erase along
  a learned erase direction first, then the ordinary corrective write. Best at
  both 2.5B dense and 25B-A2.8B MoE, and the gain persists after 80B tokens of
  long-context midtraining.
---

# SOTA-177: Decouple the erase address from the write address in a delta-rule recurrence

## Source

Li et al. (2026), [LIT-177](../literature.d/LIT-177.md) — [ARXIV-2606.26560](https://arxiv.org/abs/2606.26560).

[SOTA-135](SOTA-135.md) pairs a decay gate for erasure with a delta update for targeted
writes. This names a limitation in that pairing precisely enough to act on:
**the delta rule corrects what is stored at the current write address before
writing there.** The correction is anchored to the write. So stale
information sitting at a *different* address cannot be actively removed — it
can only decay passively, which is what the gate is for and is the blunt
instrument the gate always was.

EDA decouples the two. A targeted erase step along a **learned erase
direction** runs first, then the ordinary delta-style corrective write along
the write direction. The corrective behaviour is preserved and a cleanup path
is added beside it.

## The evidence, and the part of it that is unusual

Best in both settings tested — dense 2.5B and MoE 25B-A2.8B — and the gain
**persists after 80B tokens of long-context midtraining**, where it also
leads long-context evaluations from 4k to 128k. Persistence through
midtraining matters more than the headline: a memory-management improvement
that washes out once the model has seen long contexts would be measuring
something else.

The analysis is the part worth reading. Update analysis and memory-state
probes show EDA allocating its cleanup path most strongly **where passive
decay is weak** — which is what the mechanism predicts, and is the kind of
confirmation architecture papers usually assert rather than demonstrate.

## The rival answer, which nobody has compared it to

Kimi Delta Attention meets the same pressure with a **channel-wise
forgetting gate**, letting each channel decay at its own rate: finer *passive*
decay. EDA's answer is an **addressed erase**: active removal somewhere other
than where you are writing.

Both are about giving a fixed-size state better memory management, they are
not variants of each other, and the record now holds both with no comparison
between them. That is the condition in `promote_when:`, and it is available
to be run — the channel-wise gate ships at 2.8T.

## Known implementations

- None in the record.
