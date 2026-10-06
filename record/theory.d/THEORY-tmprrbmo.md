---
status: Proposed
promote_when: >-
  The contrast that would isolate the delta rule: the same lockstep
  perturbation measurement on a decay-only recurrence, such as Mamba-2, at
  matched decay horizons. The account predicts that there an impulse
  persists for about the decay horizon and injected noise climbs toward a
  higher plateau, while in a delta-rule layer both are cut short. A second
  delta-rule model showing the same plateau would strengthen the claim but
  not settle it, because it cannot tell the overwrite from other features
  the two models share.
title: 'A delta-rule recurrence does not accumulate small per-step perturbations, because each write overwrites the state along the current key, so injected error plateaus and an impulse fades far faster than the forget gate implies'
version: 1
tags:
- attention-techniques
- numerics-and-precision
- analysis-and-evaluation
date: '2026-10-06'
source:
- LIT-tmpd8csx
summary: >-
  Kozyrev and Maiboroda (2026), [LIT-tmpd8csx](../literature.d/LIT-tmpd8csx.md), §5.3, Table 6, Fig. 1. In
  Qwen3.8-27B's Gated DeltaNet layers, run in FP32 lockstep over 32K tokens,
  4-bit quantization noise holds state error at a plateau of about 12.6%. A
  1% state impulse falls to 1/e in 80–1,382 steps, where the decay gates
  imply horizons of 1,895–61,659 tokens. The authors attribute the extra
  forgetting to the delta rule's overwrite along each new key. No arm
  removes the delta rule, so the attribution is inferred, not measured.
---

<!-- inactive-ok-file: SOTA-177 — Proposed; named for the contrast with its
     account of the delta rule, not relied on -->

# THEORY-tmprrbmo: A delta-rule recurrence does not accumulate small per-step perturbations, because each write overwrites the state along the current key, so injected error plateaus and an impulse fades far faster than the forget gate implies

## Source

Kozyrev and Maiboroda (2026), [LIT-tmpd8csx](../literature.d/LIT-tmpd8csx.md) — §5.2–5.4, Tables 3, 4 and 6,
Figs. 1–2.

## The account

**The intuition it replaces.** A recurrence carries its state for tens of
thousands of tokens, so a small error injected at every step, from
quantization or anything else, should compound. Every public 4-bit build of
Qwen3.8-27B acted on that intuition and kept its Gated DeltaNet layers in 8
or 16 bits.

**What the delta rule does instead.** The gated delta rule writes
S_t = α_t S_{t−1} + β_t k_t (v_t − S_{t−1}ᵀ k_t)ᵀ. The write replaces
whatever the state currently returns for key k_t with v_t, so any error
stored along k_t is overwritten, not added to. As new tokens arrive with new
keys, old errors are deleted direction by direction. The decay α_t forgets
uniformly and slowly, while the overwrite forgets selectively and fast.
Injection and erasure balance, so error reaches an equilibrium. It does not
grow.

**The gates are shielded by their parameterization.** The decay is
exp(−exp(A)·softplus(a + b)) and the write strength is a sigmoid. A ~11%
error in the gate projections becomes 7.5% on 1 − α and 5.2% on β. A
mis-scaled β is then itself corrected by later writes.

## What was measured

- **The plateau** (Table 6, Fig. 1a). Kozyrev and Maiboroda ([LIT-tmpd8csx](../literature.d/LIT-tmpd8csx.md))
  replayed Qwen3.8-27B's own GDN layers with NVFP4 error injected. Five layers spread over depth, eleven
  perturbed trajectories against one clean one, 32K tokens. With every
  projection quantized, state error is 12.96% at token 256, 12.09% at 4,096
  and 12.31% at 32,768. The maximum is 14.94%.
- **The impulse** (App. B.3). A 1% perturbation at token 1,024 falls to 1/e
  after 550 / 164 / 281 / 80 / 1,382 steps in the five layers, against
  decay-implied horizons of 43,970 / 1,895 / 4,156 / 8,342 / 61,659 tokens.
- **Where the fragility is** (Table 6). Multiplicative noise of 0.1%
  applied directly to α gives 22% state error, and 1% gives 46%. The same
  1% on β gives 0.39%. The recurrence is not robust to everything. It is
  robust to noise that reaches it through the write and through
  log-parameterized gates.
- **End to end** (Table 4). The weight-quantization gap in per-token NLL is
  +0.081 nats over the first half of a 32K window and +0.011 over the
  second.

## What this does not say

- **Not that the overwrite is proved to be the cause.** There is no arm with
  the delta rule removed, and no decay-only recurrence at matched horizons.
  The gap between impulse decay and decay horizon fits the account, but
  other things could close it: the key normalization, the convolution, or
  how fast keys change in real text. That is the condition in
  `promote_when:`.
- **Not that any recurrence is safe to quantize.** The authors say a
  linearly parameterized decay may not have the gate shielding, and the
  direct-α arm shows how sensitive the horizon is.
- **Not a statement past 32K tokens**, one model, one format.

## Where it sits

It reads oddly against [SOTA-177](../practices.d/SOTA-177.md). That practice, from [LIT-177](../literature.d/LIT-177.md), calls the
delta rule's correction incomplete because it acts only at the current
write address. Stale content elsewhere is left to passive decay. Here the
same address-bound overwrite is enough to clear a 1% perturbation within a
few thousand tokens. The two are compatible. A random perturbation is
spread over every direction, and keys in real text sweep across them
quickly. A specific stale association sits in a direction no new key may
revisit soon. Neither paper tests the distinction.
