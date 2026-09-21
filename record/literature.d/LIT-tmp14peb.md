---
status: Active
title: 'Quantized Evolution Strategies: High-precision Fine-tuning of Quantized LLMs at Low-precision Cost'
version: 1
tags:
- numerics-and-precision
- adaptation-and-tuning
- training-optimization
date: '2026-09-21'
published: '2026-02-01'
arxiv: '2602.03120'
first_author: 'Xu'
keywords:
- 'quantization'
- 'evolution-strategies'
- 'error-feedback'
- 'fine-tuning'
- 'memory'
extends:
- LIT-211
implementations: []
summary: >-
  Xu, Miikkulainen and Qiu (2026), [ARXIV-2602.03120](https://arxiv.org/abs/2602.03120). Fine-tune a
  quantized model in its own integer space: accumulate the part of each
  evolution-strategies update that is smaller than the lattice spacing until
  it crosses a grid point, and rematerialize that accumulator from stored
  seeds so it costs kilobytes instead of an FP16 copy of the weights.
  Countdown, Qwen2.5 at 1.5B and 3B, INT4/INT8/W8A8.
---

<!-- inactive-ok-file: THEORY-006 — Proposed, and named only to say this paper is
     NOT evidence for it. That account's promote_when calls out this exact misuse;
     citing it to decline the inference is the opposite of leaning on it -->

# LIT-tmp14peb: Quantized Evolution Strategies: High-precision Fine-tuning of Quantized LLMs at Low-precision Cost

## Why it's here

It joins two of the record's lines at a point neither had reached.
[SOTA-154](../practices.d/SOTA-154.md) says to fine-tune with evolution strategies rather than
policy-gradient RL; `numerics-and-precision` holds what a bit budget costs.
This is the intersection: what happens when the parameters you are searching
live on an INT4 lattice, and the answer is that ordinary ES stops moving.

**It is not an independent result in the ES line.** Its corresponding author
is Xin Qiu, first author of [LIT-211](LIT-211.md), the paper `SOTA-154` is built on.
`SOTA-154`'s consensus note keeps a running count of which results come from
inside that line; this one is inside it, and adds nothing to the independent
side of the ledger.

## The problem it names

An ES update is `w ← w + η · ĝ`. On an integer lattice with spacing `Δ`, you
must round. In fine-tuning, `η · ĝ` is routinely smaller than `Δ/2`.

The paper's §5 makes the failure exact rather than intuitive. Write the
rounding as identity plus an error, `Q(x) = x + ε(x)`. Expand the trajectory
over `T` steps and the accumulated quantization loss term **exactly cancels**
the accumulated ideal update whenever every step falls short of the grid:
`w_T = w_0`. The model does not move at all. Round stochastically instead and
the errors become zero-mean noise that random-walks with variance growing in
`T`, producing a noise floor that buries the fine-tuning signal. Those are the
two failure modes, and they are the two things a quantized zeroth-order
method can do.

## What it does

**Accumulated error feedback.** Keep an FP16 residual `e`. Add it to the
desired update before rounding, and carry the remainder forward. This is
Delta-Sigma modulation, and the paper says so — the same device as 1-bit SGD's
error feedback. Infinitesimal signals integrate in `e` until they cross a
threshold and trigger a discrete step.

The payoff is stated as a bound: define virtual continuous parameters
`w̃ = w + e`; these evolve by exactly the unconstrained high-precision update,
and the physical weights satisfy `‖w − w̃‖ ≤ Δ/2` at every step. The discrete
trajectory shadows the continuous one to within half a grid cell, instead of
cancelling against it or random-walking away from it.

**Stateless error tracking via seed replay.** An FP16 residual over all
parameters costs more memory than the quantized weights it is meant to make
trainable, which would defeat the exercise. So it is not stored. The residual
is deterministic given the history, so it is rematerialized on demand by
replaying the last `W` steps from their random seeds and scalar rewards — a
few kilobytes — exploiting `γ < 1` so older contributions vanish. Memory drops
from `O(d)` to `O(W·P)`; compute rises by `W` reconstructions per update.

The approximation in the replay is that boundary gating is checked against
current weights rather than historical ones. The paper measures why this is
safe: fewer than a small fraction of parameters change per step, and of those
a negligible fraction sit at a quantization boundary, so the two conditions
required for a divergence essentially never coincide.

## What was measured

Countdown, Qwen2.5 at 1.5B and 3B, quantized to INT4 and INT8 with GPTQ and
to W8A8 with LLM-Compressor, 300 generations. Baselines: the unmodified
quantized model, QuZO (the quantized zeroth-order incumbent, run at its
best configuration from a hyperparameter search), and a Full-Residual variant
of QES that stores the FP16 accumulator — described as the oracle the
memory-saving version is approximating.

| model | format | base | QuZO | full residual | QES |
|---|---|---|---|---|---|
| Qwen2.5-1.5B | INT4 | 3.50 | 5.25 | 18.05 | 16.00 |
| | INT8 | 4.20 | 4.50 | 22.10 | 26.35 |
| | W8A8 | 4.20 | 4.20 | 15.25 | 15.35 |
| Qwen2.5-3B | INT4 | 2.80 | 14.25 | 33.50 | 31.85 |
| | INT8 | 4.50 | 15.85 | 33.30 | 37.40 |
| | W8A8 | 8.20 | 10.75 | 31.70 | 21.35 |

The headline comparison is against QuZO, and it is decisive at the coarse end:
at INT4 on the 1.5B model QuZO moves 3.50 → 5.25 while QES reaches 16.00.
QuZO's weakness is size-dependent — it manages 2.80 → 14.25 at 3B — which the
paper reads as small quantized models being harder to optimize.

## Conditions

**The approximation beats its own oracle, twice.** QES exceeds the
Full-Residual variant at INT8 on both models (26.35 vs 22.10; 37.40 vs 33.30)
and falls 10 points short of it at W8A8 on the 3B model (21.35 vs 31.70). An
approximation cannot really be better than the thing it approximates, so these
gaps are **run-to-run variance**, and they are the same size as the
differences the paper is interpreting. No seeds, repeats or error bars are
reported. The caption's "only slightly lower than with full residuals" does
not describe the W8A8 row.

**One task, one model family, two sizes.** Countdown, Qwen2.5, 1.5B and 3B.
Countdown is already the task `SOTA-154`'s line is most argued on, so this
adds a setting rather than breadth.

**The prose disagrees with the table twice in §4.2.** It reports QES reaching
"18.00%" on INT4/1.5B where the table gives QES 16.00 and the oracle 18.05,
and it describes 14.25 → 31.85 as doubling "the performance of the base
model" where 14.25 is QuZO's number and the base model's is 2.80. The table is
the record; the numbers above are taken from it.

**Memory is argued, not benchmarked.** The claim is that optimizer-state
memory falls from `O(d)` to `O(W·P)` and that training then fits in
inference-sized memory. The complexity argument is sound and no measured
peak-memory figures accompany it.

**The scale-up paragraph is speculation and is labelled as such.** §6 suggests
that trading precision for parameters plus ES's inference-only memory could
allow training models "one or two orders of magnitude larger" on the same
hardware. That is future work in the authors' own framing, and nothing here
tests it.

**Do not read it as evidence for [THEORY-006](../theory.d/THEORY-006.md).** That account's
`promote_when` names this exact misuse — "a further post-training method that
works and is read back as evidence for the account" — and QES is one. It also
runs at 1.5B, the low end where `SOTA-154`'s negative results cluster, but on
quantized weights against a quantized baseline, which is not the comparison
that threshold was measured on.
