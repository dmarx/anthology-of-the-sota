---
status: Active
title: 'Erase-then-Delta Attention: Decoupling Erase and Write Addresses in Delta-Rule Linear Attention'
version: 1
tags:
- attention-techniques
date: '2026-09-05'
published: '2026-06-01'
arxiv: '2606.26560'
first_author: 'Li'
keywords:
- 'delta-rule'
- 'linear-attention'
- 'memory-management'
- 'long-context'
- 'recurrent-state'
implementations:
- EDA
summary: >-
  Li et al. (2026), [ARXIV-2606.26560](https://arxiv.org/abs/2606.26560). The delta rule corrects only at the
  address it is writing to, so stale content elsewhere can never be removed;
  EDA adds an erase step at an independently chosen address.
---

# LIT-tmpngv1m: Erase-then-Delta Attention: Decoupling Erase and Write Addresses in Delta-Rule Linear Attention

Li et al. (2026) — [ARXIV-2606.26560](https://arxiv.org/abs/2606.26560)

## Key takeaways

- A precise limitation of the delta rule, which the record recommends
  ([SOTA-135](../practices.d/SOTA-135.md)): it corrects what is stored **at the current write address**
  before writing there. The correction is anchored to the write. So stale
  information sitting at a *different* address cannot be actively removed —
  it can only decay passively.
- **EDA decouples where to erase from where to write.** A targeted erase step
  along a learned erase direction runs first, then the ordinary delta-style
  corrective write along the write direction. The corrective behaviour is
  preserved and a cleanup path is added beside it.
- Best in both settings tested — dense 2.5B and MoE 25B-A2.8B — and the gain
  **persists after 80B tokens of long-context midtraining**, where it also
  leads long-context evaluations from 4k to 128k.
- The analysis is the useful part: update analysis and memory-state probes
  show EDA allocating its cleanup path most strongly **where passive decay is
  weak**, which is what the mechanism predicts and is rarely demonstrated.

## Standing in the anthology

The current end of the record's delta-rule line, and a sharpening of what
[SOTA-135](../practices.d/SOTA-135.md) recommends. That practice pairs a decay gate for erasure with a
delta update for targeted writes; this says the pairing is incomplete,
because the erasure is passive and global while the write is active and
targeted, and the asymmetry is what limits a fixed-size memory.

Read against [LIT-133](LIT-133.md): Kimi Delta Attention's answer to the same pressure is a
*channel-wise* forgetting gate, letting each channel decay at its own rate —
finer passive decay. EDA's is an *addressed* erase — active removal
somewhere other than where you are writing. Both are about giving a
fixed-size state better memory management, and the record now holds both
without anyone having compared them.
