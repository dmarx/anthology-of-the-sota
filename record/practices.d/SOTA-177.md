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
  One group, two scales, no deployment for the design as filed. A second
  group (LIT-tmpsiw5k, NVIDIA) independently decoupled the erase from the
  write a month earlier, but only as a channel reweighting of the write key,
  so the freely learned erase direction remains one group's result. The
  rival answer to the same problem — a channel-wise forgetting gate — ships
  at 2.8T.
# Left at `unreplicated` at v2, deliberately and as a judgement: the second
# group's mechanism is a restricted case of this one, not a repeat of it.
# See the body's last section before moving it.
title: 'Decouple the erase address from the write address in a delta-rule recurrence'
version: 2
history:
- version: 2
  date: '2026-10-06'
  note: >-
    Records Gated DeltaNet-2 (LIT-tmpsiw5k), from NVIDIA, published a month
    before the EDA paper and not citing it or cited by it. It erases along
    the write key reweighted by a channel-wise gate, which is a decoupled
    erase address in restricted form, and it does so on top of KDA's
    channel-wise decay and against KDA. That comes close to the second
    clause of `promote_when:`, and the body says why it is not treated as
    meeting it. Status and recommendation are unchanged; consensus stays
    `unreplicated` with a revised note.
tags:
- attention-techniques
date: '2026-09-08'
source:
- LIT-177
introduced_by:
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

These results are [LIT-177](../literature.d/LIT-177.md)'s, the paper that introduces EDA and first makes
this recommendation: it names the write-anchored correction as the limitation
and tests the decoupled erase against the plain delta rule at both scales,
through the 80B-token midtraining.

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

## A second group, in a narrower form

Gated DeltaNet-2 ([LIT-tmpsiw5k](../literature.d/LIT-tmpsiw5k.md)), from NVIDIA and published in May 2026, a
month before the EDA paper, reached a version of the same idea
independently. Its update is S_t = (I − k_t (b_t ⊙ k_t)ᵀ) D_t S_{t−1} +
k_t (w_t ⊙ v_t)ᵀ. The write still runs along k_t, but the read that gets
erased runs along b_t ⊙ k_t, a channel-wise gate on the key. So the erase
address is decoupled from the write address. Unlike EDA's learned erase
direction, it can only reweight the coordinates of the current key. It is
built on KDA's channel-wise decay and measured against it at 1.3B / 100B
tokens with matched state size. The variant that keeps only the erase gate
channel-wise averages 52.79 against KDA's 52.28 (Wiki perplexity 16.12
against 16.81). The full model averages 53.11.

That is close to "an independent group running an addressed erase against a
channel-wise decay gate", and it answers the comparison the section above
asks for in one way: the two remedies stack rather than compete. It is not
treated here as meeting `promote_when:`, for three reasons. The erase
direction is a restricted case of the one recommended here. It is one run
at one scale. And its ablation does not say whether the scalarised variants
were retrained. A reader who disagrees with that judgement has the numbers
above to disagree with.

## Known implementations

- None in the record for the design as filed. GatedDeltaNet-2 (NVlabs)
  implements the restricted, channel-reweighted form.
