---
number: 262
status: Active
formerly:
- SOTA-tmp28zyj
consensus: emerging
consensus_note: >-
  Two groups now, independently and in different families of model: MMDiT in
  a text-to-image diffusion model, Mixture-of-Transformers in autoregressive
  and mixed-objective multi-modal LLMs. Both compare against a shared-weight
  backbone at matched budget and both win. What keeps it short of `converged`
  is that nobody has surveyed how widely per-modality weights are actually
  used against the cross-attention conditioning they displace, and that the
  two ingredients have still never been separated.
title: 'Give each modality its own weights and let the streams attend jointly'
version: 2
history:
- version: 2
  date: '2026-09-21'
  note: >-
    Proposed -> Active. The promotion condition asked for a second group
    reporting per-modality weights against a shared-weight backbone at
    matched compute; LIT-483 is that, from a different lab in a
    different family of model, with FLOPs held identical to the dense
    baseline across three settings and two baselines. It also brings the
    component ordering the practice could not previously state — untie the
    feed-forward first, the attention projections second, the layer norms
    not at all — so the recommendation gains a "which weights" it did not
    have. The condition's *second* satisfier, an ablation separating the
    separate weights from the joint attention, is still unmet after two
    papers, and the Conditions section now says so as a standing gap rather
    than as a reason to withhold the practice.
tags:
- multimodal-learning
- model-architecture
- generative-modeling
date: '2026-09-20'
source:
- LIT-449
- LIT-483
introduced_by:
- LIT-449
implementations:
- 'Stable Diffusion 3'
explained_by:
- THEORY-049
summary: >-
  Esser et al. (2024), [LIT-449](../literature.d/LIT-449.md) — MMDiT gives the text and image
  streams separate projections and MLPs, then runs attention over the
  concatenated sequence so information flows both ways. It beats UViT and
  DiT at matched budget. Liang et al. (2024), [LIT-483](../literature.d/LIT-483.md) — the same
  shape reached independently for autoregressive multi-modal LLMs, matching
  a dense baseline at **55.8% of the FLOPs**, and ablated component by
  component: the feed-forward carries most of the benefit, the attention
  projections less, the layer norms none.
---

# SOTA-262: Give each modality its own weights and let the streams attend jointly

## Source

Esser et al. (2024), [LIT-449](../literature.d/LIT-449.md) — [ARXIV-2403.03206](https://arxiv.org/abs/2403.03206).

Liang et al. (2024), [LIT-483](../literature.d/LIT-483.md) — [ARXIV-2411.04996](https://arxiv.org/abs/2411.04996) — read
as [NOTE-232](../notes.d/NOTE-232.md).

## The shape of the recommendation

Two modalities, one sequence. Text tokens and image tokens get **separate
weights** — their own projections and their own MLPs — because they are
different kinds of object and a shared parameterization has to be a
compromise between them. But attention runs over the **concatenated**
sequence, so the two streams are not merely fused at the end: information
flows in both directions at every layer.

That is the distinction worth holding. Cross-attention conditioning, the
prevailing alternative, lets image tokens read text and not the reverse. Here
the text representation is itself updated by what the image is doing.

`LIT-483` puts the second half more precisely than the first source
does. Global self-attention **normalizes attention weights across tokens of
different modalities in one operation**; a cross-attention fusion design
keeps the modalities in separate streams and joins them at intervals. So the
choice is not "separate or joint" — it is *separate parameters, joint
normalization*.

## Which weights to untie, and in what order

This is the part the practice could not say when it had one source. Untying
components one at a time with FLOPs held to the dense architecture:

1. **The feed-forward networks.** The large step, with the substantial gains
   on the image modality. Untie these first; if you untie nothing else you
   have most of it.
2. **The `Q`/`K`/`V` and output projections.** A further real gain — about
   33.3% FLOPs saved on image and 10% on text against feed-forward-only —
   and smaller than the step before it.
3. **The layer norms.** Negligible *on top of* the other two.

<!-- inactive-ok-block: THEORY-049 — Proposed, filed in this same
     contribution, and the sentence citing it says so: the account is named as
     an account and its unsettledness is stated in the same breath. What the
     practice asserts is the ordering, which is measured; the theory is why -->

Two reasons are offered for the ordering, and they are not the same reason.
At a 4,096-token context the feed-forward is simply the larger share of the
FLOPs. And the feed-forward is where a transformer keeps its memory, so
separate memory per modality is where separation should pay. The first
argument weakens as context grows; the second does not. [THEORY-049](../theory.d/THEORY-049.md)
is the account, and is `Proposed` for reasons of its own.

**Do not read step 3 as "layer norms do not matter".** The authors are
explicit that their result is about untying layer norms *given* the other two
untyings, and says nothing about untying them alone.

## What it buys, and where

**In diffusion** (`LIT-449`), against UViT and DiT backbones at matched
budget, and the improvements are not uniform: they concentrate in **text
comprehension, typography and human preference**. That is the right place for
them to land if the mechanism is what the paper claims — the tasks that fail
when the text representation is frozen partway through are exactly the ones a
bidirectional design should fix. It also **follows predictable scaling
trends**, with validation loss tracking the downstream metrics, which is what
made it safe to commit an 8B run to.

**In autoregressive and mixed-objective multi-modal LLMs** (`LIT-483`),
against a dense baseline and a four-expert mixture-of-experts baseline at
identical FLOPs: dense-level performance at **55.8% of the FLOPs** in the
Chameleon setting at 7B, **37.2%** with speech added as a third modality, and
about **one third** in the Transfusion setting, where a **760M model beats a
1.4B dense baseline** on key image metrics. Measured in wall clock on A100s
rather than only in FLOPs: dense image quality in **47.2%** of the time, text
quality in **75.6%**.

The two results are in different objectives, different modalities' roles and
different labs, and they agree.

## Conditions

**Matched on compute, not on memory.** The second source's comparison is
FLOP-matched: a sparse architecture activates only one modality's weights per
token, so at identical FLOPs it holds *more* total parameters than the dense
baseline it matches. "Dense performance at 55.8% of the FLOPs" is a compute
claim, and a deployment decision also has a memory budget. The first source's
"matched budget" is the diffusion-scaling convention and is not the same
control.

**The two ingredients still arrive together.** Separate weights and joint
attention are both in MMDiT and both in Mixture-of-Transformers, and no
variant in either paper varies the attention: every arm attends globally.
What has been ablated is *which parameters* to untie, not *whether the joint
attention is doing the work*. Two independent groups now agree on a bundle
that nobody has taken apart, so a reader implementing one half and attributing
the other half's benefit to it would still not be contradicted by anything in
the record. This is a standing gap, not a reason to disbelieve the pair.

**The second source's settings are its authors' own lineage.** Chameleon and
Transfusion are Meta architectures and this is a Meta paper. The dense and
mixture-of-experts baselines within each setting are controlled; the choice of
settings is not independent.

**Three modalities, not many.** The evidence runs text-and-image, plus one
three-modality result in which speech carries the most favourable ratio and
the least established baseline. Nothing here says what happens at five.

## Known implementations

- Stable Diffusion 3 (MMDiT)
- Chameleon, Chameleon + speech and Transfusion settings reproduced under
  Mixture-of-Transformers, with released training recipes
