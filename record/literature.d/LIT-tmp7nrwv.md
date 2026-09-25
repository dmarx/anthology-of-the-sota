---
status: Active
title: 'Analyzing and Improving the Training Dynamics of Diffusion Models'
version: 1
tags:
- training-optimization
- generative-modeling
- model-architecture
date: '2026-09-25'
published: '2023-12-05'
arxiv: '2312.02696'
first_author: 'Karras'
keywords:
- 'post-hoc-ema'
- 'weight-averaging'
- 'magnitude-preserving'
- 'diffusion'
- 'imagenet-512'
implementations:
- 'EDM2'
summary: >-
  Karras, Aittala, Lehtinen, Hellsten, Aila and Laine (2023),
  [ARXIV-2312.02696](https://arxiv.org/abs/2312.02696). **Post-hoc EMA**: keep two power-function weight averages
  during training, snapshot them periodically, and afterwards reconstruct the
  average for *any* decay length by least squares — reconstruction error falling
  as `O(1/n⁴)` in the snapshot count. That makes the averaging length a sweep
  instead of a pre-training guess, and the consequence is the headline number
  here: with the length fixed at 13%, varying the learning-rate decay over
  `t_ref ∈ [30k, 160k]` moves FID **by up to 72%**; sweeping the length post hoc
  brings the whole bracket **within 10% of the optimum**. Also EDM2's
  magnitude-preserving architecture, reaching FID 1.91 on ImageNet-512 without
  guidance.
---

<!-- inactive-ok-file: SOTA-415, SOTA-408, SOTA-217, SOTA-156, SOTA-288, THEORY-tmpwhyfx — every weight-averaging practice in this record is Proposed, and this note cites them as the cluster whose gap it fills, not as settled support: the point being made is that six not-yet-in-force recommendations all work around the choice this paper removes. THEORY-tmpwhyfx is the account this note introduces. -->

# LIT-tmp7nrwv: Analyzing and Improving the Training Dynamics of Diffusion Models

Karras, Aittala, Lehtinen, Hellsten, Aila and Laine (2023) —
[ARXIV-2312.02696](https://arxiv.org/abs/2312.02696)

## Key takeaways

- **Post-hoc EMA, and the mechanism is cheap.** Maintain two power-function
  averages during the run at `σ_rel` 0.05 and 0.10 (`γ = 16.97` and `6.94`),
  store both in each periodic snapshot — every ~8M images, i.e. every 4096 steps
  at batch 2048 — and afterwards find the least-squares fit between the stored
  profiles and whatever profile you want, then take that linear combination.
  Reconstruction MSE falls "experimentally in the order of `O(1/n⁴)`" in the
  number of snapshots `n`, and "a few dozen snapshots is more than sufficient for
  a virtually perfect EMA reconstruction".
- **It works retroactively, at reduced accuracy.** Reconstruction "can be done
  even from a single stored `θ̂` per snapshot, albeit with much lower accuracy",
  which "opens the possibility of revisiting previous training runs that were not
  run with post-hoc EMA in mind". Any run whose checkpoints survive can have its
  averaging length swept after the fact.
- **The profile is a power function, not an exponential, for two stated
  reasons.** A very long exponential EMA "puts non-negligible weight on initial
  stages of training where network parameters are mostly random"; and longer runs
  benefit from longer averages, so the profile should scale with training time by
  itself. The power profile gives `θ(t=0)` weight exactly zero and is
  scale-independent: doubling the training time stretches it by the same factor.
  The authors note the name is a misnomer — the decay is not exponential — and
  keep it anyway.
- **It is parameterized by width, not by `γ`.** `σ_rel`, the relative standard
  deviation of the profile's peak as a fraction of training time, because `γ` "has
  a somewhat unintuitive effect". "EMA length of 10%" means `σ_rel = 0.10`.
- **The result that matters outside diffusion (Fig. 12).** A sweet spot in the
  learning-rate decay parameter still exists (`t_ref = 70k` here), but "the
  possibility of sweeping over the EMA lengths post hoc drastically reduces the
  importance of this exact choice": `t_ref ∈ [30k, 160k]` all land within 10% of
  the optimum. **"In contrast, if the EMA length was fixed at 13%, varying `t_ref`
  would increase FID much more, at worst by 72% in the tested range."** The
  learning-rate decay looked like a sensitive hyperparameter because the
  averaging length was frozen. [THEORY-tmpwhyfx](../theory.d/THEORY-tmpwhyfx.md) is that claim.
- **The optimal length is not a constant, in three separate ways.** It "differs
  considerably between the configurations" b–g; the optimum *narrows* as the
  architecture improves; and it "slowly shifts towards relatively longer EMA as
  the training progresses" — notable because the definition is already relative
  to training length.
- **Different weight tensors want different averaging lengths, and the gap is
  worth 10% FID.** Sweeping one tensor's EMA while holding the rest at the global
  optimum has "surprisingly large effects on FID": in Config B, FID improved from
  **7.24 to ~6.5**, "in one instance … using a very short per-tensor EMA, and in
  another, a very long one". The authors' hypothesis is that "any global choice is
  an uneasy compromise". In the final Config G the effect disappears and the
  tensors agree — so tensor disagreement is a *symptom of an unfinished
  architecture*, and its narrowing optimum is a good sign rather than an alarming
  one. Per-tensor EMA is left unexplored beyond this experiment.
- **The architecture half.** Magnitude-preserving layers, redistributing
  activation and weight magnitudes rather than normalizing them post hoc, giving
  ImageNet-512 FID **1.91** without guidance against VDM++'s 2.99, and at much
  lower complexity: EDM2-S reaches **2.56** at 280 Mparams, 102 Gflops and **63**
  NFE, against VDM++'s 2.99 at 2455 Mparams, 555 Gflops and 256 NFE. With
  guidance, 2.23 for EDM2-S and 1.85 for EDM2-XL. ADM ([LIT-699](LIT-699.md)) is 23.24/7.72 at
  559 Mparams and 250 NFE.
- **Dropout is turned on only where overfitting shows.** Enabled for M–XXL,
  "while disabling it in the smaller configurations (XS, S) where it is
  harmful" — the criterion being training loss still falling while validation
  loss and FID rise.

## Standing in the anthology

Filed against a measured gap rather than a ranking. The record holds a dense
weight-averaging cluster — [SOTA-408](../practices.d/SOTA-408.md) (average the tail under a cyclical or high
constant learning rate), [SOTA-409](../practices.d/SOTA-409.md) (average a hyperparameter sweep), [SOTA-415](../practices.d/SOTA-415.md)
(uniform-average recent stable-phase checkpoints to estimate an annealed score),
[SOTA-156](../practices.d/SOTA-156.md), [SOTA-217](../practices.d/SOTA-217.md), [SOTA-288](../practices.d/SOTA-288.md) — and before this note **no document in it mentioned
post-hoc EMA, and none said the averaging length could be chosen after the run.**
Zero files contained the phrase.

That absence was read as low priority twice, on the grounds that this paper
"extends a well-sourced practice rather than correcting one" — it succeeds
[SOTA-188](../practices.d/SOTA-188.md)'s source. Re-measured against the question that has been productive
— *does the record make a claim this paper would correct or source* — the
absence is the opposite of low priority, because the cluster is full of documents
working around the choice this paper removes.

What it supplies:

- [SOTA-tmp0s2gj](../practices.d/SOTA-tmp0s2gj.md), the recommendation;
- [THEORY-tmpwhyfx](../theory.d/THEORY-tmpwhyfx.md), the entanglement account, which the record had no theory for;
- the correction to [SOTA-415](../practices.d/SOTA-415.md)'s justification for uniform averaging, and the
  reason [SOTA-408](../practices.d/SOTA-408.md)'s compute objection does not transfer.

**What it does not settle.** Whether any of this holds outside diffusion.
Everything here is ImageNet-512 with EDM2's own architecture, and the record's
other averaging practices are about ResNet classification ([SOTA-408](../practices.d/SOTA-408.md)), fine-tuned
CLIP models ([SOTA-409](../practices.d/SOTA-409.md)) and language-model pretraining ([SOTA-415](../practices.d/SOTA-415.md)). The mechanism
is architecture-agnostic — it is arithmetic on stored parameter vectors — but the
claim that a *frozen* averaging length inflates another knob's apparent
importance is measured in one setting on one metric.
