---
status: Rejected
status_note: its own paper's unconditional numbers contradict it, and a blur-to-noise sweep shows generation degrading sharply as noise is removed
title: 'What makes a diffusion model generative is iterated restoration of any degradation, not Gaussian noise'
version: 1
tags:
- generative-modeling
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-tmpb9kuz
summary: >-
  Bansal et al. (2022), [LIT-tmpb9kuz](../literature.d/LIT-tmpb9kuz.md) — the account cold diffusion was named
  for: the train-to-restore, sample-by-restore-and-redegrade procedure
  generates whatever the degradation is, so noise is incidental. Its own
  Table 5 has noiseless blur generation at FID 97.00 on CelebA against 23.11
  with noise, and Warm Diffusion's sweep degrades from 1.85 to 11.97 as noise
  is taken out. The procedure survives. The claim that noise is not what
  matters does not.
corrected_by:
- THEORY-tmpyyfqg
---

<!-- inactive-ok-file: THEORY-tmpyyfqg — Proposed, filed in this same contribution as the account that replaces this one -->

# THEORY-tmpc9v4u: What makes a diffusion model generative is iterated restoration of any degradation, not Gaussian noise

## Source

Bansal et al. (2022), [LIT-tmpb9kuz](../literature.d/LIT-tmpb9kuz.md) — read as [NOTE-tmpvd2bq](../notes.d/NOTE-tmpvd2bq.md). Filed for
`#163`'s "[theory] cold diffusion", and filed already retired, because the
evidence against it was in hand when it was filed ([DP-003](../../docs/design-principles.md#dp-3)).

## The account

Diffusion was explained through noise: Langevin dynamics, score matching,
variational inference with a Gaussian prior. Cold Diffusion argued that
these explanations were over-specific. Train any restorer on any continuous
degradation, sample by restoring and re-degrading, and generation emerges.
On this account the noise is one choice of degradation among many, and the
theory built on it is "called into question".

## Why it is `Rejected`

**The paper's own generation numbers.** On CelebA, noiseless cold
generation from blur is FID 97.00 against 23.11 for the noise-based model.
The authors trace the gap to a lack of diversity from perfectly correlated
initial pixels, and fix it by adding Gaussian noise of σ = 0.002, which
brings FID to 49.45. So a tiny amount of noise does half the work, and the
rest of the gap remains.

**The sweep that went looking.** Warm Diffusion ([LIT-tmphm11f](../literature.d/LIT-tmphm11f.md)) holds the
model and sampler fixed and moves only the blur-to-noise ratio. FID goes
from 1.85 at 0.5 to 2.57 at 2 and 11.97 at 10. Generation quality tracks
the amount of noise in the process, which is what this account says it
should not do.

## What survives

**The procedure works conditionally.** Deblurring, inpainting and
super-resolution by iterated restoration improve FID over one-shot
reconstruction. **The sampler is exact** for degradations linear in
severity ([LIT-tmpb9kuz](../literature.d/LIT-tmpb9kuz.md), §3.3). Neither needs this account. The replacement
explanation is [THEORY-tmpyyfqg](THEORY-tmpyyfqg.md).
