---
status: Active
title: 'Run DPO on tiny models for one epoch only'
version: 1
tags:
- training-optimization
- tiny-models
date: '2026-09-05'
published: '2026-01-15'
source:
# The tiny-scale evidence (one epoch, not two) and the algorithm itself,
# which the practice recommended without citing until now (ADR-010).
- LIT-119
- LIT-169
- LIT-129
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. One epoch at LR 1e-6 to 3e-6 took a 90M model's IFEval from about 50 to over 65; a second epoch degraded it while the reward kept rising.
---

# SOTA-126: Run DPO on tiny models for one epoch only

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

DPO on a 90M SFT-pretrained checkpoint, cosine decay, LR sweep over 3e-7,
1e-6, 3e-6, 1e-5. Trained for three epochs, every run degraded sharply on
end-to-end evaluations right after the first epoch — while the DPO reward
kept increasing for the whole run. The reward is not the signal to stop on.
Re-run for a single epoch at 1e-6 and 3e-6, IFEval went from about 50 to
over 65 with the other benchmarks preserved, and the same recipe applied to
the curriculum-SFT model gave the same pattern (40.8 to 53.5). The
multilingual 100M model showed the same: DPO was its main gain in
instruction following. The prior the authors cite for DPO converging at
this scale is [LIT-129](../literature.d/LIT-129.md): a 135M model taken through SFT, reasoning SFT and one
epoch of DPO.

Conditions: the epoch count interacts with the schedule — with cosine decay,
changing the number of epochs changes the whole trajectory, which is why the
authors fixed the epoch count and swept the rate rather than the reverse.
Stated for tiny models because that is where it was measured; the authors
report that a short DPO stage has helped at every scale they have trained
(0.5B–34B), but not the epoch-boundary cliff.

## What DPO is

Introduced in [LIT-169](../literature.d/LIT-169.md): reparameterise the reward so the optimal policy
has a closed form, and the whole RLHF apparatus — a fitted reward model, a
sampling loop, an RL optimiser — collapses into one classification loss over
preference pairs. That is why it is cheap enough to be worth running at 90M
at all.

It also predicts the failure this practice guards against. Optimising the
implicit reward is not the same as improving the policy, so a rising DPO
reward through a second epoch while benchmarks fall is the objective doing
exactly what it says while the model gets worse.

## Known implementations

- Falcon-H1-Tiny-90M-Instruct, Falcon-H1-Tiny-Multilingual-100M-Instruct
