---
number: 232
status: Read
formerly:
- NOTE-tmpl9zt7
paper: LIT-483
title: 'Mixture-of-Transformers'
version: 1
date: '2026-09-21'
summary: >-
  Read to test whether it satisfies `SOTA-262`'s promotion condition. It does,
  as that condition was written — second group, per-modality weights against a
  shared-weight backbone, FLOPs held identical. The component ablation is a
  bonus the condition did not ask for and the practice needed.
---

# NOTE-232: Mixture-of-Transformers

## Contribution

The same architectural idea as MMDiT, arrived at independently, in a different
family of model and against a different baseline — and then ablated in a way
the original was not.

What is true afterwards that was not before: "give each modality its own
weights" stops being one lab's diffusion-model design and becomes a claim with
two controlled comparisons behind it, in autoregressive and mixed-objective
settings, with a component ordering attached.

## Key insight

**Untie the parameters, keep attention global.** The decoupling is complete —
feed-forward, projections, layer norms — and the attention is not: tokens of
every modality attend over the whole sequence together.

The paper's footnote on why is worth having. Cross-attention fusion designs
keep modalities in separate streams and join them at intervals; global
self-attention instead *normalizes attention weights across tokens of
different modalities*, in one operation, with fewer layers. So the choice is
not "separate or joint" but "separate parameters, joint normalization".

## Assumptions

- **Identical FLOPs for training and test** across dense, MoE-4x and MoT.
  Parameters are not matched, which is what sparse means.
- **Early fusion**: all modalities are tokens in one sequence from the start.
- **Images as 1,024 discrete VQ-VAE tokens** in the Chameleon settings; speech
  via a pre-trained tokenizer.
- **Context 4,096**, which the authors say is part of why the feed-forward
  dominates the ablation.

## Key results

- Chameleon 7B: dense performance at **55.8% of FLOPs**.
- Chameleon + speech: comparable speech performance at **37.2% of FLOPs**.
- Transfusion 7B: dense image performance at **one third of FLOPs**; a
  **760M MoT beats a 1.4B dense** on key image metrics.
- Wall clock on A100s: dense image quality at **47.2%** of the time, text at
  **75.6%**.
- Component ablation, FLOPs controlled: feed-forward untying gives the large
  step; adding `Q`/`K`/`V` gives ~33.3% further FLOPs saving on image and 10%
  on text against feed-forward-only; adding layer norms is **negligible**.
- Leave-one-out: merging any two modalities degrades both, and the damage is
  **non-reciprocal** — merging image with speech keeps most of image's gains
  while speech deteriorates.
- MoT and MoE-4x compose: putting MoE-4x inside MoT's text tower accelerates
  text loss further without costing the image side.

## Claims

**Well supported, and the reason this was read:** that per-modality weights
beat a shared-weight backbone at matched compute. Three settings, two
baselines, several scales, and a wall-clock measurement rather than only a
FLOP count.

**The most useful thing, and not what was being tested:** the component
ordering. Feed-forward first, attention projections second, layer norms not at
all. `SOTA-262` recommended untying weights without saying which, and this
says which.

**Carefully bounded by its authors:** the layer-norm result is *on top of* the
other two untyings, and they say it does not establish that untying layer
norms alone does nothing.

**Mechanism, offered:** the feed-forward is the transformer's memory, so
separate memory per modality is where the separation pays — plus the plain
FLOPs-share argument at context 4,096.

## Method

Three multi-modal settings with progressively harder objectives, each against
a dense and an MoE-4x baseline at identical FLOPs, across model scales; a
four-way component ablation; a leave-one-out study over three modalities; and
a systems profile on A100s.

## Connections

- [SOTA-262](../practices.d/SOTA-262.md) — give each modality its own weights and let the streams
  attend jointly. This is the second group its promotion condition asked for,
  and the practice moves to `Active` on it.
- [LIT-449](../literature.d/LIT-449.md) is the first source — MMDiT in Stable Diffusion 3. Different
  lab, different objective, same shape. `compared_against` is declared because
  MoT explicitly reproduces the Transfusion setting, which is the line
  `LIT-449`'s design sits in.
- [SOTA-150](../practices.d/SOTA-150.md) makes the feed-forward a sparse mixture of experts once the
  model is large enough. MoT is a *different* sparsity axis — by modality
  rather than by learned routing — and the paper shows the two compose:
  MoE-4x inside MoT's text tower helps further without hurting image.

## Bearing on the record

It promotes a practice, which is the outcome a `promote_when` exists to
produce, and it refines what that practice says to do.

It does **not** close the question the condition's second clause named. No
variant here separates the modality-specific weights from the global
attention; every arm keeps attention global. So the two ideas still arrive
together, and the practice's conditions say so.

## Limitations

**FLOP-matched, not memory-matched.** At identical FLOPs MoT holds more
parameters. "55.8% of the FLOPs" is a compute claim, and a deployment decision
also has a memory budget.

**The settings are the authors' own lineage.** Chameleon and Transfusion are
both Meta architectures and this is a Meta paper. The dense and MoE-4x
baselines are controlled; the choice of settings is not independent.

**Still no attention ablation.** Which means the record holds two groups
agreeing on a *bundle*, and nobody has taken the bundle apart.

**Speech flatters.** The 37.2% figure is for the modality with the least
established baseline, and it is the largest ratio quoted.

## Open questions

- What does untying layer norms alone do? The authors flag this explicitly as
  unexamined, and it is the cheapest of the three to test.
- Does global attention matter, or would per-modality attention with periodic
  cross-attention do as well at these FLOPs? This is `SOTA-262`'s second
  satisfier and remains open after two papers.
- Does the feed-forward-first ordering survive longer contexts? The authors
  attribute part of it to the feed-forward's FLOPs share at 4,096, which falls
  as context grows.
