---
number: 88
status: Proposed
formerly:
- THEORY-tmpgwgsb
promote_when: >-
  A controlled sweep of the masking ratio on at least three modalities that
  differ measurably in redundancy — say text, images and audio — under one
  architecture, one evaluation protocol, **one model capacity and one masking
  strategy**, reporting the optimum against an independently measured
  redundancy statistic. The last two are not pedantry: LIT-tmpqkx1z moves the
  optimum by a factor of nearly three within a single modality by changing
  capacity alone, so a cross-modality correlation drawn from models of
  different sizes measures capacity as much as redundancy. A paper that finds a
  high ratio works for a fourth modality still would not settle it: the claim
  is that the optimum *tracks* redundancy, which needs the correlation and not
  another point.
title: 'Masked prediction transfers across modalities only after the masking ratio is rescaled to the signal''s information density'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Corrected, not qualified. The claim was that the masking optimum is a
    property of the signal's information density. LIT-tmpqkx1z sweeps the rate
    within one signal — English text — and finds the optimum moving with **model
    capacity** (40% at 354M, 20% at 124M, 15% at 51M) and with **masking
    strategy** (uniform admits a higher rate than span or PMI masking). Both
    hold the signal fixed. And at an 80% rate, where validation perplexity
    exceeds 1,000 and nothing can be reconstructed, 95% of fine-tuning
    performance survives — so reconstruction feasibility, which is what
    redundancy governs, is not what sets the useful rate. The `promote_when`
    asked for a cross-modality correlation and has to ask for capacity and
    strategy to be held fixed as well, or the correlation it finds will be
    confounded.
tags:
- signal-structure
- representation-and-encoding
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-601
- LIT-tmpqkx1z
explains:
- SOTA-373
---

# THEORY-088: Masked prediction transfers across modalities only after the masking ratio is rescaled to the signal's information density

## Source

He et al. (2021), [LIT-601](../literature.d/LIT-601.md) — [ARXIV-2111.06377](https://arxiv.org/abs/2111.06377), §1.

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

## What moves the optimum, measured within one signal

The account says the optimum is a property of the signal. [LIT-tmpqkx1z](../literature.d/LIT-tmpqkx1z.md) holds the
signal fixed — English text, one architecture family, one evaluation protocol —
and moves the optimum anyway:

- **by capacity.** 40% at 354M parameters, 20% at 124M, 15% at 51M. Nearly a
  factor of three, with the signal identical.
- **by masking strategy.** Uniform masking is an easier task than span or PMI
  masking at a given rate, so it admits a higher optimum. The strategy is a
  property of the objective, not of the text.

So "information density" cannot be the whole story, and the honest form of the
account reads *the optimum depends on the signal's redundancy, the model's
capacity and the masking strategy* — at which point the cross-modality
correlation the `promote_when` asks for has to hold the other two fixed, which
it now says.

**And the link to reconstruction is broken.** Redundancy governs whether a
hidden region can be recovered from its neighbours; that is what this account is
about. At an 80% masking rate on text, validation perplexity exceeds **1,000** —
recovery is hopeless — and the model still preserves **95% of fine-tuning
performance** and **90% of BLiMP probing accuracy** against a 15% baseline.
Whether the masked content can be reconstructed and how good the representations
are come apart. Wettig et al. suggest such a model may be operating as a
powerful skip-gram model, which if true is a different account of what the
objective buys.

## Standing

`Proposed` rather than `Active`: plausible, directionally useful, resting on
evidence that is suggestive rather than settling. `SOTA-373` is `Active`
regardless, because the *practice* — derive the ratio from your signal rather
than inheriting it — is right even if this explanation of why is wrong. That
split is `ADR-031`'s, and this is a cleaner instance than usual: a wrong
theory here would leave the recommendation untouched, since "measure whether
an interpolator can solve your masked task" is an empirical procedure that
needs no account of density at all.

That prediction has now been tested. `LIT-tmpqkx1z` damaged this account and
left `SOTA-373` standing: the practice was amended twice in one day and its
recommendation never changed, while the explanation behind it lost a term. The
split was doing exactly what it was built for.
