---
status: Read
paper: LIT-tmpeu23i
title: 'Freezing the spectrum by construction, and what one 60M run can and cannot show'
version: 1
date: '2026-09-22'
summary: >-
  Read as the third position on one axis. If the problem is that weight
  spectra drift during training, the options are renormalize them, bound how
  fast they move, or make them constant. This does the third. The idea is
  clean and the evidence for the claim worth recommending is one model at 60M,
  which is why no practice is filed.
---

# NOTE-tmpwddew: Freezing the spectrum by construction, and what one 60M run can and cannot show

## Contribution

An optimizer whose updates are coupled left and right orthogonal
transformations of each weight matrix. Because an orthogonal equivalence
transformation preserves singular values exactly, the spectrum is invariant
for the whole run and only the singular vectors move.

## Key results

**The gap it targets is specific and real.** Muon orthogonalizes the *update*,
which makes each step µP-compatible, but the *weights'* spectral norms still
drift. Existing fixes bolt normalization or spectral retraction onto Muon.
Pion removes the drift by deriving the update on the iso-spectral manifold, so
no normalization step is needed and the update's spectral norm is bounded
too.

**Pretraining, LLaMA-1.3B, 54B tokens** (2× Chinchilla, ~400K steps, C4,
T5-base tokenizer, sequence length 256):

| | avg benchmark | validation loss |
|---|---|---|
| AdamW | 44.74 | 2.7700 |
| Muon | 46.34 | **2.7225** |
| Pion | **47.69** | 2.7350 |

Worth stating plainly: Pion wins the eight-benchmark average and **loses to
Muon on the loss it is optimizing**. The paper reports both.

**Normalization-free pretraining, 60M LLaMA.** Every normalization layer
removed. AdamW and Muon make initial progress and then diverge to NaN; Pion
completes 9.6B tokens and converges. This is the result that would justify a
recommendation, and it is one model and one run.

**200-layer DeepNet, 50B tokens.** Mean standard deviation of the local loss
trajectory: AdamW 0.0931, Muon 0.0927, **Pion 0.0892**. A 4% difference in one
stability statistic.

**Cost.** Peak per-GPU memory 59,839 MB against AdamW's ~51,600 and Muon's
~47,300 — +16.0% and +26.6%. Step time 0.5679s against 0.3932s (AdamW) and
0.5505s (Muon): 44.4% slower than AdamW, 3.2% slower than Muon. Dropping the
second-moment Lie-algebra buffers cuts memory to 45,289 MB — below both
baselines — at slightly worse quality.

**Also reported:** supervised fine-tuning on Qwen2.5-1.5B and Llama-3.2-3B,
and GRPO on RLVR tasks, with Pion best in both settings.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Orthogonal equivalence updates preserve the spectrum exactly | strong, and definitional | it is what the transformation is |
| C2 | Pion is competitive with Muon at 1.3B | moderate | one run each, benchmarks better and loss worse |
| C3 | Spectrum-preserving updates can substitute for normalization layers | **suggestive only** | one 60M model, one run, against two baselines that fail |
| C4 | It is the most stable optimizer at extreme depth | weak | 0.0892 against 0.0927 |
| C5 | Cost is acceptable relative to Muon | strong | measured on 8×H100 |

## Limitations

**One run per cell, throughout.** Including the headline pretraining
comparison and the normalization-free demonstration.

**The depth claim should not be quoted.** A 4% difference in a loss-variance
statistic, single seed, is not a stability result; reporting it as "the most
stable optimizer" is the paper's framing and not what the number supports.

**A new optimizer from one group.** The record's bar for an optimizer
recommendation is higher than a single paper — the spectral-optimizer
documents it already holds took several arrivals to reach `Proposed`.

**The benchmark-versus-loss split is unexplained.** Better downstream averages
with worse validation loss than Muon is the kind of divergence worth an
explanation, and the paper offers none.

## Bearing on the record

**It completes an axis the record can now see in full.** Three ways to handle
a drifting weight spectrum: renormalize it every step
([LIT-tmpzz9pi](../literature.d/LIT-tmpzz9pi.md)), bound how fast it may move
([LIT-tmp8a9ww](../literature.d/LIT-tmp8a9ww.md)), or forbid it from moving
([LIT-tmpeu23i](../literature.d/LIT-tmpeu23i.md)). All three report removing a crutch —
warmup, normalization, or both. Nobody has compared them, and the axis is only
visible because all three are filed together.

**It juxtaposes sharply with a paper filed hours earlier.**
[LIT-tmpxqt7b](../literature.d/LIT-tmpxqt7b.md) measures that the trace-normalized spectrum
stops moving early in ordinary pretraining and stays put. Pion makes it never
move. The obvious question — is the early spectral motion Pion forbids the
part that was doing the work? — is asked by neither paper, and the two are
contemporaneous with no citation in either direction. Recorded as a
juxtaposition and not as a relation, because nobody ran the comparison
([ADR-011](../decisions.d/ADR-011.md)).

**No practice is filed, and that is the point of reading it.** The
recommendable claim is C3, and C3 rests on one 60M run.
[DP-005](../../docs/design-principles.md#dp-5) is about adoption not being evidence; this is the
adjacent failure, a striking demonstration not being evidence either. What
would change it is named below.

## Open questions

- **Does normalization-free training hold above 60M?** One run at 1B or
  above, with and without normalization, is the experiment that would turn
  C3 into a practice.
- **Is the fixed spectrum a cost anywhere?** A spectrum set at initialization
  is a spectrum chosen by the initializer, and nothing here asks whether the
  initial singular values are the right ones to be stuck with.
- **Pion against Muon-plus-normalization.** The paper's own framing says
  existing work fixes Muon's drift by adding normalization. That is the
  baseline the comparison needs and does not have.
