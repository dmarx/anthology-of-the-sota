---
status: Read
paper: LIT-tmp14peb
title: 'Quantized Evolution Strategies'
version: 1
date: '2026-09-21'
summary: >-
  Reading it: the memory trick is the contribution, not the error feedback.
  Error feedback is 1-bit SGD's, correctly credited; what is new is refusing
  to store the accumulator at all and rebuilding it from seeds, which is the
  only reason the method fits in the memory budget that motivated it.
---

<!-- inactive-ok-file: THEORY-006 — Proposed, and named as the misuse this reading
     declines rather than as support; see that account's promote_when -->

# NOTE-tmp4sz3x: Quantized Evolution Strategies

## Contribution

Fine-tuning that happens **in** the quantized model rather than around it.
Before this, updating a quantized model meant dequantizing, or training an
adapter beside it, or accepting that the model is frozen. This searches the
integer lattice directly and never materializes a high-precision copy of the
weights.

What is true afterwards that was not before: an ES update smaller than the
grid spacing is no longer lost. It is banked.

## Key insight

The paper's framing is "apply Delta-Sigma modulation to ES", and that half is
borrowed and credited — error feedback is standard in 1-bit SGD. The half
that is actually new is the observation that **the accumulator does not have
to exist**. It is a deterministic function of the seeds and the scalar rewards
already being stored, and the decay factor means only a short window matters.

That inversion is what makes the method fit its own motivation. Error feedback
alone would have produced a method needing an FP16 buffer the size of the
weights — more memory than the quantized model it was meant to make
trainable, so a paper about memory-constrained devices that does not fit on
one.

## Assumptions

- **Rewards are verifiable** (RLVR framing), so fitness is a correctness score
  on Countdown rather than a learned reward model.
- **The lattice is uniform.** INT4, INT8, W8A8 — §6 names non-uniform and
  floating-point formats as untested.
- **Decay `γ < 1`**, which is what makes truncating the replay window sound.
- **Boundary gating may be checked against current weights**, not the
  historical weights the replay is reconstructing. Measured to be safe here;
  it is an approximation, not an identity.
- **Perturbations are stochastically rounded** to stay on the lattice.

## Key results

- Countdown accuracy, Qwen2.5, 300 generations. INT4/1.5B: base 3.50, QuZO
  5.25, **QES 16.00**, full-residual oracle 18.05. INT4/3B: base 2.80, QuZO
  14.25, **QES 31.85**, oracle 33.50.
- QuZO's competence is size-dependent — near-stagnant at 1.5B, useful at 3B.
  QES works at both.
- Replay window ablation, decay fixed at 0.90: `W` = 50/40/30/20/10 gives
  16.00 / 14.80 / 16.15 / 14.75 / 13.05. Flat. With decay scaled to the
  window instead, `W` = 10 (γ = 0.58) collapses to 4.55 — so the collapse is
  the aggressive decay, not the short window.
- Update sparsity and boundary-hit rates are both small, which is the
  argument that the stateless approximation is faithful.

## Claims

**The mechanism claim is derived, not just observed.** Without a residual,
sub-lattice updates cancel exactly (`w_T = w_0`) or, under stochastic
rounding, random-walk with variance growing in `T`. With one, the virtual
parameters `w + e` follow the unconstrained high-precision trajectory and the
physical weights stay within `Δ/2` of it. That is arithmetic, and it is the
strongest thing in the paper.

**The empirical claim is that this is why QES beats QuZO**, which is an
inference from the mechanism to the numbers, not a measurement of it.

## Method

Two arms plus an oracle variant, on one task, at two model sizes, in three
quantization formats; ablation over replay window and decay; measurement of
update sparsity and boundary-hit rate to justify the approximation.

## Concepts

*Accumulated error feedback* (Σ-Δ modulation, error feedback); *stateless
seed replay*; *virtual continuous parameters* `w̃ = w + e`; *boundary gating*
to keep updates inside the codebook.

## Connections

- [LIT-211](../literature.d/LIT-211.md) is the parent — same corresponding author, and the source of
  the seed-based memory discipline this extends. `extends`.
- [SOTA-154](../practices.d/SOTA-154.md) is the practice this specializes: ES fine-tuning instead of
  policy-gradient RL. The new practice only makes sense if you are already
  doing that.
- The error-feedback lineage runs through 1-bit SGD and communication-efficient
  training, which the paper credits. That is a different corner of the record's
  concerns — the same device used to survive a coarse *gradient* channel, here
  surviving a coarse *parameter* lattice.

## Bearing on the record

It supports one practice, `Proposed` and `unreplicated`, and one account.

The thing it does **not** do is move `SOTA-154`. That practice's consensus
rests on an explicit count of which results come from inside the Qiu line and
which do not, and this is inside it. A reader who sees "another ES paper
works" and updates the consensus has done the thing the note was written to
prevent.

It is also the misuse [THEORY-006](../theory.d/THEORY-006.md) named in advance: a post-training method
that works, read back as evidence for the density account. It is not that.

## Limitations

**Variance is unreported and appears to be large.** QES beats its own
full-residual oracle at INT8 on both models and loses to it by 10 points at
W8A8 on 3B. An approximation outperforming the thing it approximates is
noise, and the noise is the size of the effects being discussed. Every
comparison in the paper should be read with that in mind, including the ones
that favour it.

**One task.** Countdown, which is also the task the parent line is most
argued on.

**The memory claim is complexity, not measurement.** `O(d) → O(W·P)` is
correct and no peak-memory numbers are given.

**Compute cost is acknowledged and unquantified in wall-clock.** `W`
reconstructions per update; §4.5 shows `W` can be halved for about a point of
accuracy, and suggests parallelizing the replay, which is not done.

## Open questions

- Does the error-feedback fix survive non-uniform and sub-4-bit formats?
  Named as future work; the cancellation argument gets worse as `Δ` grows, so
  this is the interesting direction and the one most likely to break.
- Is the residual doing anything ES-specific? The cancellation argument is
  about rounding an update, not about how the update was estimated. The same
  device should rescue a first-order quantized optimizer, and nobody has run
  that comparison.
- How much of the gap to QuZO is error feedback and how much is the rest of
  the setup? The paper ablates the replay window and the decay, not the
  presence of the accumulator against a matched QES without it.
