---
status: Proposed
promote_when: >-
  A controlled sweep of the masking ratio on at least three modalities that
  differ measurably in redundancy — say text, images and audio — under one
  architecture and one evaluation protocol, reporting the optimum against an
  independently measured redundancy statistic. A paper that finds a high
  ratio works for a fourth modality would not settle it: the claim is that
  the optimum *tracks* redundancy, which needs the correlation and not
  another point.
title: 'Masked prediction transfers across modalities only after the masking ratio is rescaled to the signal''s information density'
version: 1
tags:
- signal-structure
- representation-and-encoding
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-tmp0s7m8
explains:
- SOTA-tmpzm1n3
---

# THEORY-tmpgwgsb: Masked prediction transfers across modalities only after the masking ratio is rescaled to the signal's information density

## Source

He et al. (2021), [LIT-tmp0s7m8](../literature.d/LIT-tmp0s7m8.md) — [ARXIV-2111.06377](https://arxiv.org/abs/2111.06377), §1.

## The account

Masked autoencoding worked in language years before it worked in vision, and
the usual explanation was architectural. MAE argues the architecture was only
one of three differences, and that the load-bearing one is a property of the
data:

> Languages are human-generated signals that are highly semantic and
> information-dense. … Images, on the contrary, are natural signals with
> heavy spatial redundancy — e.g., a missing patch can be recovered from
> neighboring patches with little high-level understanding of parts, objects,
> and scenes.

The consequence is that **the same objective specifies different tasks on
different signals.** Hiding 15% of a dense signal leaves a problem requiring
comprehension. Hiding 15% of a redundant one leaves a problem requiring
interpolation, and the model will solve the problem it is given. Raising the
ratio to 75% is what restores the difficulty, and the paper's framing is
exactly that: high masking "largely eliminates redundancy, thus creating a
task that cannot be easily solved by extrapolation from neighboring patches".

A third consequence, also in the paper and less quoted: the **decoder's**
required capacity differs for the same reason. BERT's decoder can be a
trivial MLP because words are already semantic; a pixel decoder emits
something "of a lower semantic level than common recognition tasks", so
decoder design "plays a key role in determining the semantic level of the
learned latent representations".

## What is good about it and what is missing

**Good:** it is a claim about the data rather than the model, it predicts the
direction of a correction before you run the sweep, and it explains a
five-fold difference that was otherwise a bare hyperparameter. It also makes
a falsifiable prediction for any new modality.

**Missing:** the evidence is two points from two literatures. The ratios were
chosen by groups with different architectures, different evaluation
protocols and different amounts of compute, and "information density" is
invoked qualitatively — nothing here measures the redundancy of either
signal, so the account and the observation cannot be separated.

It is also entangled with a measurement problem that MAE itself documents:
linear probing and fine-tuning put the optimal ratio in different places.
Any account of where the optimum *should* be has to say which optimum it
means, and this one does not.

## Standing

`Proposed` rather than `Active`: plausible, directionally useful, resting on
evidence that is suggestive rather than settling. `SOTA-tmpzm1n3` is `Active`
regardless, because the *practice* — derive the ratio from your signal rather
than inheriting it — is right even if this explanation of why is wrong. That
split is `ADR-031`'s, and this is a cleaner instance than usual: a wrong
theory here would leave the recommendation untouched, since "measure whether
an interpolator can solve your masked task" is an empirical procedure that
needs no account of density at all.
