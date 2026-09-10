---
number: 46
paper: LIT-109
status: Read
formerly:
- NOTE-tmphqeph
title: 'NeuS2: Fast Learning of Neural Implicit Surfaces for Multi-view Reconstruction'
version: 1
tags:
- vision-and-graphics
date: '2026-09-09'
published: '2022-12-01'
summary: >-
  Cuts NeuS surface reconstruction from about 8 hours to minutes for a static object, and to as little as 20 seconds per frame for a moving sequence. The point of the speedup is what it unlocks: at 8 hours per object, dynamic scenes with thousands of frames are simply not attemptable.
---

# NOTE-046: NeuS2: Fast Learning of Neural Implicit Surfaces for Multi-view Reconstruction

## Contribution

NeuS produces high-quality implicit surfaces from multi-view images and takes
**about 8 hours** per static object. This paper's framing of why that matters is
the useful part:

> the training of NeuS takes an extremely long time (8 hours), which makes it
> almost impossible to apply them to dynamic scenes with thousands of frames

NeuS2 reduces it to **minutes** for a static object and **up to 20 seconds per
frame** for a moving-object sequence.

## Key insight

**The speedup is not an optimisation, it is an enabling condition.** A thousand-
frame sequence at 8 hours per frame is not slow, it is impossible; at 20 seconds
it is an afternoon. The paper is explicit that dynamic reconstruction is the
target and the runtime is what stood between the method and it.

That reframing is the transferable observation: a cost reduction of two orders
of magnitude does not make an existing workflow faster, it makes a different
workflow exist. Whether a speedup is worth pursuing depends on which side of a
feasibility threshold it lands on.

## Assumptions

- Multi-view capture with known cameras.
- The quality of the original method is preserved — the claim is speed at equal
  fidelity, not a new reconstruction criterion.
- Per-frame incremental reconstruction is valid for a moving object, i.e. frames
  are similar enough for warm starting to help.

## Key results

- **~8 hours → minutes** for a static object.
- **Up to 20 seconds per frame** for a moving-object sequence.
- Multi-view consistency preserved.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Implicit surface reconstruction can be made orders of magnitude faster at comparable quality | strong | measured against NeuS |
| C2 | The speedup is what makes dynamic sequences feasible | strong | arithmetic, and the demonstration |
| C3 | Per-frame incremental reconstruction is sound for moving objects | moderate | the 20s/frame figure depends on it |

## Method

Accelerate the NeuS formulation — hash-encoding-style representation and a
second-order optimisation treatment — and reuse the previous frame's solution
when reconstructing a sequence.

## Concepts

- **Feasibility thresholds** — the reason to measure a speedup against what it
  makes possible rather than against the previous number.
- **Warm-starting across a sequence** — the frames-are-similar assumption, which
  is where the per-frame figure comes from.

## Connections

The same pressure `LIT-064` and `LIT-108` respond to, applied to implicit
surfaces rather than radiance fields, and it inherits the hash-encoding line
`LIT-064` established.

C2 is the clearest instance in this pass of a point the record makes nowhere:
**cost reductions are not fungible.** The record's efficiency practices —
`SOTA-086`, `SOTA-019`, `LIT-102` — all report speedups as ratios, and a ratio
does not say whether the result crossed a threshold that changes what can be
attempted.

## Recommendations

- **R1** — Report a speedup against the workflow it enables, not only as a
  ratio. *Topic:* analysis and evaluation. *Strength:* moderate.
- **R2** — Warm-start from the previous frame when reconstructing a sequence.
  *Strength:* moderate, domain-specific.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**
Multi-view surface reconstruction is not a line the anthology tracks.

R1 is worth recording because the record's own efficiency practices are all
stated as ratios. A 2× speedup and a 1000× speedup are qualitatively different
claims — the second changes what problems exist — and the record has no way of
saying so.

The document's takeaways — "accelerated surface reconstruction", "implicit
function learning", "multi-view consistency", "optimization techniques" — are
four categories, and none of them carries the number that is the paper's entire
argument.

## Limitations

- 2022, multi-view capture, single objects.
- The per-frame figure depends on inter-frame similarity.
- Reported against NeuS specifically, so the "orders of magnitude" is relative
  to one baseline.

## Open questions

- How far does the warm-start assumption stretch? Fast motion is the obvious
  failure case and the paper reports a best case.
