---
status: Proposed
promote_when: >-
  An independent group restarting a low-rank adapter mid-training that runs the
  same three arms — restart with the optimizer reset and no re-warm, restart
  with the re-warm and no reset, and both — FROM A WARM-STARTED MODEL, which is
  the configuration the method is actually used in and the one the source never
  ablated, at 1B or above or across more than one seed, and reports whether the
  reset-without-re-warm arm still diverges. What would NOT meet it: another
  low-rank-restart method that simply uses this recipe, which is adoption
  (DP-005), or a re-run of the 130M from-scratch ablation, which is the result
  already held.
consensus: unreplicated
consensus_note: >-
  One group, one ablation (130M, from random initialisation, one run per arm).
  The record holds no second paper that restarts an adapter and ablates the
  reset or the re-warm. Later low-rank-restart methods exist outside the record
  and have not been checked for whether they ablate it rather than inherit it.
  Read as of 2026-09.
title: 'When you merge and reinitialise a low-rank adapter mid-training, prune the optimizer state and re-warm the learning rate from zero — both, not either'
version: 1
tags:
- training-optimization
- adaptation-and-tuning
- model-stability
date: '2026-09-25'
source:
- LIT-104
introduced_by:
- LIT-104
implementations:
- 'ReLoRA reference implementation (github.com/guitaricet/relora)'
summary: >-
  Lialin et al. (2023), [LIT-104](../literature.d/LIT-104.md) — ReLoRA's restart discipline, read as
  [NOTE-024](../notes.d/NOTE-024.md). At every merge-and-reinit, prune the adapter's Adam state (99% by
  magnitude) **and** drop the learning rate to zero and re-warm it over 50–100
  steps. In the 130M ablation (Table 6) the restart alone does nothing (34.25
  vs LoRA's 34.17), the re-warm without the reset does nothing (34.29), the
  reset without the re-warm **diverges**, and only the pair helps (29.77). A
  rule for *how* to restart, not a recommendation *to* restart.
extends:
- SOTA-184
---

# SOTA-tmppbzba: When you merge and reinitialise a low-rank adapter mid-training, prune the optimizer state and re-warm the learning rate from zero — both, not either

## Source

Lialin et al. (2023), [LIT-104](../literature.d/LIT-104.md) — [ARXIV-2307.05695](https://arxiv.org/abs/2307.05695),
read in full (v4, December 2023) as [NOTE-024](../notes.d/NOTE-024.md). The evidence is Table 6 and the
paragraph under "Adding restarts and optimizer resets" in §4.2; the recipe is
Algorithm 1 and Figure 2.

## When this applies

You are training a low-rank adapter ([SOTA-184](SOTA-184.md)'s `W + s·W_A W_B`) with Adam, and
at some point **during** training you fold the adapter into the frozen weight
and start a fresh one — `W ← W + s·W_A W_B`, `W_A` re-drawn (Kaiming), `W_B`
zeroed — so that the next adapter can learn a direction the last one could not.
ReLoRA does this every 2K–5K steps of pretraining, so that a sum of rank-`r`
updates reaches a rank no single one has.

This practice is about **what the restart needs**. It does not say to restart;
the next section but one says what the evidence for *that* is, and it is much
thinner.

## Do this, at every restart

1. **Prune the optimizer state of the new adapter.** ReLoRA zeroes 99% of the
   Adam moments by magnitude. The reason is specific to Adam: with β₁, β₂ at
   0.9–0.999 the moments accumulated for the old `W_A` steer the new one back
   into the same subspace, which is exactly what the restart was meant to
   escape. Keep the state and the restart is a no-op.
2. **Drop the learning rate to zero and re-warm it.** ReLoRA's "jagged cosine"
   (Figure 2) sets the rate to zero at each reset and warms back onto the
   underlying cosine over 50–100 steps; the 1.3B run used 50. Reset the state
   without this and the run diverges.

The ablation that makes this one practice rather than two (Table 6, 130M, no
warm start, perplexity):

| restarts | optimizer reset | re-warm | ppl |
|:--:|:--:|:--:|--:|
| – | – | – | 34.17 (plain LoRA) |
| ✓ | – | – | 34.25 |
| ✓ | ✓ | – | **diverged** |
| ✓ | – | ✓ | 34.29 |
| ✓ | ✓ | ✓ | 29.77 |

Either half alone is worthless or worse. That is the negative half of this
practice, and it carries its citation in the same table — the shape [ADR-042](../decisions.d/ADR-042.md)
asks a "do not do this" to have.

## What the evidence does not cover

- **The ablation is from random initialisation.** The method as recommended
  starts from a full-rank warm start, and there the reset and re-warm were
  never ablated separately: from a warm start the paper reports only the full
  recipe against no restarts at all. The divergence finding is established for
  one configuration, at one scale, apparently one run per arm.
- **"Optimizer reset" in the ablation is not fully specified.** The method
  prunes 99% of the state; the prose calls the diverging arm "a naive optimizer
  reset", which could mean a full one. Appendix A reports no significant
  dependence on the pruning fraction above 90%, and that higher fractions can
  bring "possible loss instabilities during the reset" — which is the re-warm's
  job. Algorithm 1 as printed prunes the moments of `W_A` only.
- **The 50-step re-warm is anecdote.** The paper says the partial reset plus
  the jagged schedule allowed "as low as 50 steps, instead of hundreds" for an
  optimizer initialised from scratch, from "initial experiments" with no table.
- **The rationale is Adam's.** The argument for the reset is about momentum
  and second-moment state; the paper does not test another optimizer.

## Whether to restart at all, which this practice does not say

The evidence that restarting pays is real and small, and the paper's own
ablation is the reason to read it carefully:

- **Most of ReLoRA's gain is the warm start.** At 130M, LoRA plus the warm
  start alone reaches 25.46; the full restart recipe on top reaches 25.04, and
  regular training 23.65. Across 60M–1.3B the restarts beat warm-started LoRA
  by 0.27–0.96 perplexity (Tables 2 and 4), and with only a 2K-step warm start
  by 1.4 (Appendix E).
- **More restarts is not better.** "Online ReLoRA", merging every ~100 steps
  while resetting every 2–5K, is worse at 250M and 1.3B (Table 5).
- **In fine-tuning it does not help.** On GLUE with T5-base and T5-large,
  ReLoRA does not outperform plain LoRA (Appendix B, Table 8).

So the practice is conditional on a decision this record does not make for
you. If you are restarting, restart this way.

## Known implementations

- The authors' reference implementation, `github.com/guitaricet/relora`.
