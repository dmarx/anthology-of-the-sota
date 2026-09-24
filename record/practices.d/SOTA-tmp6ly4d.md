---
status: Proposed
promote_when: >-
  A second group reporting the dense-metric decline under a long self-supervised
  schedule and recovering it with a Gram-matrix anchor, or with anything else —
  the decline reproducing outside this model line is the part that matters most,
  because it is what makes the recommendation necessary rather than merely
  available. A search over which teacher iteration to anchor to, and how often
  to refresh it, would also move it: both are currently choices rather than
  findings. What would NOT move it: another DINO-line model trained with Gram
  anchoring by the same group.
consensus: unreplicated
consensus_note: >-
  One group, one model line, a technical report. The defect it treats is
  reported as present "to a lesser extent" in DINOv2's own training and,
  by these authors, as unresolved elsewhere — so the record cannot yet say
  whether other self-supervised recipes have it. Nobody has disputed the
  finding and nobody outside the group has looked.
title: 'Anchor the patch Gram matrix to an early teacher when training long, because dense features decay while global metrics improve'
version: 1
tags:
- training-optimization
- representation-and-encoding
- vision-and-graphics
date: '2026-09-24'
source:
- LIT-tmpuy1r1
introduced_by:
- LIT-tmpuy1r1
implementations:
- DINOv3
---

# SOTA-tmp6ly4d: Anchor the patch Gram matrix to an early teacher when training long, because dense features decay while global metrics improve

## Source

Siméoni et al. (2025), `LIT-tmpuy1r1`.

## The problem this exists for, which is the part to read first

On a long self-supervised schedule, the two things you measure come apart:

- **ImageNet linear-probe accuracy improves monotonically**, all the way.
- **Pascal VOC segmentation mIoU declines after about 200k iterations**, and on
  a 7B model falls **below its early levels**.

If you are watching the global number, nothing is wrong. What is degrading is
**locality**: the cosine-similarity map from a reference patch to all others
goes from *"smooth and well-localized"* at 200k to *"substantially"* degraded
by 600k, and CLS-to-patch similarity climbs throughout — patches drifting
toward the global summary and away from their own content.

**This is not the register defect.** With registers, patch norms stay stable
through training (`SOTA-400` is still right and still worth doing). This
is a different failure on a different axis — duration rather than size — and it
needs its own remedy.

## What to do

Keep a **Gram teacher**: an early checkpoint of the EMA teacher, from before
the dense metrics turned over. Add a loss pulling the student's patch
similarity structure towards the teacher's, on `L2`-normalized patch features:

    L_Gram = ‖ X_S · X_Sᵀ − X_G · X_Gᵀ ‖²_F

- Compute it on **global crops only**.
- The point of using the Gram matrix rather than the features is that *"the
  local features are free to move, provided the structure of similarities
  remains the same"* — it constrains geometry, not position.
- **Refresh the Gram teacher** to the current EMA teacher periodically; they
  use every 10k iterations.

It can be started **late**. They begin after 1M iterations for efficiency and
report that the late application *"still manages to 'repair' very degraded
local features"* — dense gains land within the first 10k iterations of turning
it on.

## Conditions

**You only need it if you are training long.** The decline sets in after
~200k iterations in their runs. A short schedule never reaches the regime, and
the cost is a loss term plus a stored teacher for no benefit.

**The trigger is a dense metric, not a global one.** The practice is unusual in
that its own necessity is invisible to the evaluation most people run. If you
are not tracking a patch-level benchmark through training, you cannot tell
whether this applies to you — which is the more portable lesson and holds
whatever you do about the loss.

**One group, one model line.** The `unreplicated` reading is the honest one:
nobody outside the authors has reported the decline, so the record cannot say
whether other self-supervised recipes have it. The authors say it appeared *"to
a lesser extent"* in DINOv2 and is *"unresolved"* elsewhere.

**The teacher choice is unsearched.** Which early iteration, and how often to
refresh, are stated as choices. There is no ablation here saying they matter or
do not.

**It repairs without explaining.** Nothing here says why a global objective
costs locality as training continues. The record holds no account of it, and
this practice does not declare one.

## Known implementations

- DINOv3 — the source's own, so adoption rather than independent replication
  (`DP-005`).
