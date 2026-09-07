---
status: Active
consensus: contested
consensus_note: >-
  LIT-145 and LIT-131 both compare WSD against cosine with each schedule's
  hyperparameters tuned separately, and reach opposite answers at opposite
  scales: a near-match at 124M-360M, cosine consistently ahead at 2.8T.
  Neither disputes the practical advantages; K3 does not address them.
contested_by:
- LIT-131
title: 'Use a warmup-stable-decay schedule: hold the learning rate, then decay it sharply over the final 10–20% of tokens'
version: 4
tags:
- training-optimization
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Marked contested. Kimi K3's scaling-law study (LIT-131) retunes per
    schedule and prefers cosine; the summary's claim that WSD was the
    schedule of every 2025-2026 report in the record was false once that
    report was read. The recommendation is unchanged.
- version: 3
  date: '2026-09-07'
  note: >-
    Sourced to LIT-145 as well as LIT-144. The Source section already named
    Hägele et al. "for the comparison against cosine", and that comparison is
    what makes this practice evidenced rather than reported; the frontmatter
    named only MiniCPM. The recommendation is unchanged.
- version: 4
  date: '2026-09-07'
  note: >-
    The Sequence gained a third answer: Schedule-Free AdamW, which removes the
    stopping time rather than choosing a shape to decay through. Literature
    only at filing; now a Proposed practice of its own, named in the
    Sequence. The recommendation is unchanged.
date: '2026-09-05'
published: '2024-04-01'
source:
# The practice's own Source section names both — "Hu et al. (2024), LIT-144 —
# MiniCPM; Hägele et al. (2024), LIT-145, for the comparison against cosine"
# — and the comparison is what makes this evidenced rather than reported.
# LIT-146 and LIT-147 are conditions with practices of their own, and the
# Sequence names LIT-035 and LIT-042 as predecessors; all stay in the body.
- LIT-144
- LIT-145
summary: >-
  Hu et al. (2024), [LIT-144](../literature.d/LIT-144.md), with the controlled comparison in [LIT-145](../literature.d/LIT-145.md) — matches cosine at equal tuning, leaves the token budget open, makes every stable-stage checkpoint a usable branch point; contested at frontier scale by [LIT-131](../literature.d/LIT-131.md), which retuned per schedule and chose cosine.
extended_by:
- SOTA-141
- SOTA-142
---

# SOTA-140: Use a warmup-stable-decay schedule: hold the learning rate, then decay it sharply over the final 10–20% of tokens

## Source

Hu et al. (2024), [LIT-144](../literature.d/LIT-144.md) — MiniCPM; Hägele et al. (2024), [LIT-145](../literature.d/LIT-145.md), for the
comparison against cosine.

Warm up, hold the learning rate at its peak for most of training, then
decay it fast over the last stretch — about 10% of the tokens in MiniCPM,
up to about 20% in Hägele et al., who found the cooldown's length and
shape to matter and recommend a 1-sqrt shape to zero. Most of the loss
improvement arrives in the decay. The schedule scales as predictably as
cosine across model sizes.

On quality, be precise about what [LIT-145](../literature.d/LIT-145.md) found, because it is the half that
is now contested. Sweeping the maximum learning rate **for both schedules**,
it reports "an almost perfect match between the performance of the best
cosine and cooldown schedule even for different training durations", with
the cooldown slightly ahead when it runs for 10–20% of steps and the
cooldown length needed to match cosine shrinking as training gets longer.
A match, in other words, plus the practical advantages below — not a
quality win that the advantages come on top of.

What it buys beyond quality: the total token count need not be fixed when
training starts, since the decay can be launched from any stable-stage
checkpoint; scaling laws can be fitted from one run's checkpoints instead
of a run per duration; continued pretraining is a matter of resuming the
stable stage; and high-quality or SFT-style data can be concentrated in
the decay ([LIT-144](../literature.d/LIT-144.md)), which is where [LIT-119](../literature.d/LIT-119.md)'s recipes put theirs.

Conditions: the peak learning rate must be tuned for the constant stage —
a value tuned for cosine is too high to hold. [LIT-146](../literature.d/LIT-146.md) ([SOTA-142](SOTA-142.md)) is one
way to set it. How far the decay goes is its own question: [LIT-147](../literature.d/LIT-147.md)
<!-- inactive-ok: SOTA-141 — a Proposed refinement of the decay, named as part of the schedule chain -->
([SOTA-141](SOTA-141.md)) argues for all the way to zero; production recipes in the record
decay to a floor (Falcon-H1-Tiny: ×64 exponential over 100 GT of 800 GT).

## Contested

Kimi K3 ([LIT-131](../literature.d/LIT-131.md)) ran the comparison again at 2.8T and came out the other
way. Its argument is the same one [LIT-145](../literature.d/LIT-145.md) acted on: the two schedules'
optimal peak learning rates and batch sizes differ substantially even at
matched model size and token budget, so a shared hyperparameter setting
silently favours whichever schedule it happens to suit. K3 therefore runs an
independent scaling-law search per schedule — over batch size, learning
rate, tokens-per-parameter and model shape — and reports that under each
schedule's own optimum, cosine decay consistently reaches a lower final
loss. K3 adopts cosine.

So both sides of this disagreement accept the same methodology and disagree
on the result. Three things stop that from settling the question:

- **Scale.** [LIT-145](../literature.d/LIT-145.md) ran at 124M–360M; K3 fitted at the scale of a 2.8T
  model. [LIT-145](../literature.d/LIT-145.md) itself reports that the cooldown length needed to match
  cosine falls as training lengthens, so the two are not obviously
  measuring the same regime.
- **Decay depth is held fixed, and it is a live variable here.** K3 compares
  "under a fixed minimum learning rate", while the WSD [LIT-145](../literature.d/LIT-145.md) recommends
  decays to zero with a 1-sqrt shape — the question
  <!-- inactive-ok: SOTA-141 — the Proposed practice this disagreement turns on -->
  [SOTA-141](SOTA-141.md) is Proposed about. A WSD arm stopped at a floor is not the
  WSD this practice's own evidence endorses, and K3 does not say which shape
  or depth its arm used.
- **The practical case is not contested — it is not addressed.** The
  argument above is about an open token budget, branchable stable-stage
  checkpoints, and scaling laws fitted from one run. K3 compares final loss
  and nothing else, and gives those up silently: a whole-run cosine fixes
  the duration in advance, which is the one thing [LIT-145](../literature.d/LIT-145.md) set out to avoid.
  (It keeps a late "cooldown phase" — that is where its context window goes
  from 256K to 1M — so what it drops is the open budget, not the idea of a
  final stretch.)

The rest of the frontier has not moved with K3. DeepSeek-V4 ([LIT-139](../literature.d/LIT-139.md)),
whose report precedes it by a month, warms up over 2000 steps, holds the peak for most of
training, and decays near the end — warmup-stable-decay, with cosine as the
*shape of the cooldown* rather than as the schedule. That distinction is
easy to lose: a report saying "cosine" may mean K3's whole-run cosine or
V4's cooldown shape, and only the first contests this practice.

## Sequence

<!-- inactive-ok: LIT-042 — the retired warm-restarts paper, named as the start of the schedule chain -->
Warm restarts ([LIT-042](../literature.d/LIT-042.md), retired) → a single cosine cycle ([LIT-035](../literature.d/LIT-035.md),
<!-- inactive-ok: SOTA-039 — the retired cosine practice, named as the predecessor in the chain -->
[SOTA-039](SOTA-039.md), retired by this) → WSD, with its decay shape and depth still
<!-- inactive-ok: SOTA-141 — a Proposed refinement of the decay, named as part of the schedule chain -->
being settled ([SOTA-141](SOTA-141.md)) and its peak set by scaling law ([SOTA-142](SOTA-142.md)).

<!-- inactive-ok-block: SOTA-tmpvlopd — Proposed, and it is named here as the
     rival that is not yet asserted, which is what Proposed is for -->

There is a third answer, filed as [SOTA-tmpvlopd](SOTA-tmpvlopd.md) and `Proposed`.
Schedule-Free AdamW says the branch point above was the wrong one: the
question is not which shape to decay through but whether to name a stopping
time at all. It reaches this practice's headline property — the token budget
need not be fixed when training starts — with no decay phase to launch and no
peak re-tuned for a constant stage, since there is no constant stage. Nobody
has run the two against each other; that practice's `promote_when:` is what
this record is waiting for before it would displace this one.

## Known implementations

- MiniCPM; Falcon-H1 and Falcon-H1-Tiny; DeepSeek-V4 (constant peak, cosine-shaped cooldown near the end)
- Against: Kimi K3, which compared the two with hyperparameters retuned per schedule and adopted a whole-run cosine
