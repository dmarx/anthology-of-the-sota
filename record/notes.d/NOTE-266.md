---
number: 266
status: Read
formerly:
- NOTE-tmpo1rg6
paper: LIT-521
title: 'Not all entropy collapse crashes a model, and the discriminator is low-rankness'
version: 1
date: '2026-09-22'
summary: >-
  Read after the paper it contradicts. The contribution is a distinction the
  record did not have: an attention map can be sparse with near-zero entropy
  and the run is fine, provided it is not also low-rank. That makes entropy
  the symptom and spectral energy concentration in the query-key product the
  cause, and it makes a warmup-free optimizer fall out.
---
<!-- inactive-ok-file: THEORY-061 THEORY-062 — both Proposed and
     both filed in this contribution. This reading is about the disagreement
     between them, so naming them is the subject rather than a reliance. -->

# NOTE-266: Not all entropy collapse crashes a model, and the discriminator is low-rankness

## Contribution

Split attention entropy collapse into two modes, show only one is fatal, give
a measurable predictor for the fatal one, and derive a learning-rate rule from
Weyl's inequality that suppresses it — removing learning-rate warmup.

## Key results

**The two modes.** When attention collapses the map goes sparse. The paper
then distinguishes:

| mode | attention map | outcome |
|---|---|---|
| **benign** | sparse, **not** low-rank — close to an identity matrix | trains fine |
| **malignant** | sparse **and** low-rank | model crashes |

The paper states the consequence directly: state B "is a counterexample of
entropy collapse … According to the definition of entropy collapse, state B
should lead to model crash; however, our experiments show that the model
remains stable in this state."

**The predictor.** `SEC(d_q, s)`, the fraction of spectral energy of
`W_q^T W_k` held in its top `s` singular directions. In crashed runs the
energy collapses into **fewer than 10 directions**; in successful runs it
stays distributed. The paper also rejects the competing account — rank
collapse of *activations* — on the grounds that the cause sits in the weight
matrix rather than in what flows through it.

**Theorem 1.** If `X` is low-rank and `W = W_q^T W_k` is low-rank with a few
dominant singular values — "greater than `C₀√d_q` for `C₀ ≫ 1`" — then the
attention map is sparse and simultaneously low-rank with high probability.

**The remedy, from Weyl's inequality.** `σ_{i+j−1}(W₁+W₂) ≤ σ_i(W₁)+σ_j(W₂)`,
hence `σ₁(W_t) ≤ σ₁(W_{t−1}) + σ₁(∇W_t)`. So cap the step: if
`α_t > τ·σ₁(W_{t−1})/σ₁(∇W_t)`, truncate `α_t` to that value; otherwise use
the scheduled rate. Spectral norms come from power iteration capped at 3
iterations, and the paper says 2 suffice. The result is called AdamW².

**And warmup goes away at matched quality:**

| | ViT-B 86M | ViT-L 307M | GPT-S 125M | Swin-S 50M | Swin-B 88M |
|---|---|---|---|---|---|
| AdamW, with warmup | 80.22 | 81.65 | 2.848 | 83.02 | 83.48 |
| AdamW², no warmup | 80.58 | 81.82 | 2.840 | 83.14 | 83.44 |

The warmups replaced are 60 epochs (ViT), 20 epochs (Swin) and 2000 steps
(GPT). AdamW² uses a plain cosine decay from maximum.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Sparse-but-not-low-rank collapse is benign | strong as a counterexample | observed stable runs in that state; one observation is enough to break a universal |
| C2 | Malignant collapse is what crashes | moderate | Theorem 1 plus SEC curves for crashed against healthy runs |
| C3 | SEC of `W_q^T W_k` is the cause | moderate | correlational in the figures; the theorem gives sufficiency, not necessity |
| C4 | Bounding the step by the spectral ratio replaces warmup | strong for this scale | five configurations, three architectures, matched or better |
| C5 | Activation rank collapse is the wrong locus | argued, not tested | reasoning about where the cause must sit, no experiment separating the two |

## Limitations

**One group's counterexample.** The strongest claim — that a published account
of instability is insufficient — rests on this group's own observation of
stable runs in the benign state. Nobody has reproduced it, and the paper it
contradicts has not replied.

**No comparison against the remedies it displaces.** The baselines are AdamW
with warmup and architectural stabilizers. σReparam, QK-norm and QK-clip all
target the same failure and none of them appears in the comparison, so "this
works" is established and "this works better" is not.

**Modest scale.** 50M–307M. GPT-S is 125M on OpenWebText.

**`τ` is a new hyperparameter.** Traded against warmup length, with an
ablation over four values per architecture. The paper does not claim `τ` is
insensitive, and the ablation curves show it is not entirely.

**Theorem 1 is a sufficiency result.** It says those conditions produce a
sparse low-rank map with high probability. It does not say the crash cannot
arrive another way.

## Bearing on the record

**It corrects a filed account rather than extending it.** The distinction
matters for how the record stores this:
[THEORY-061](../theory.d/THEORY-061.md) says low attention entropy is what breaks a
transformer. This says there is a stable state with low attention entropy, so
the reasoning is replaced even though most of what the earlier account
predicts still happens. `corrects`, not `extends`, and the record carries both
because neither has been adjudicated.

**It refines what [SOTA-192](../practices.d/SOTA-192.md) says about its own mechanism.** That
practice describes "almost one-hot attention weights with near-zero entropy"
as the failure. On this reading that description names a state that is
sometimes harmless, and the sharper predictor is whether the map is also
low-rank. The recommendation does not move — bounding the logits prevents both
modes — but a reader diagnosing a live run from entropy alone would be using
the wrong instrument.

**It is the only member of this cluster that acts on the update.** σReparam
rescales the weight, Pion constrains the update's geometry, this caps the step
size by a ratio of spectral norms. Three places to intervene, no comparison
between them.

**Second of three warmup removals**, and the tempting synthesis is left
unfiled for the reason given in [NOTE-265](NOTE-265.md).

## Open questions

- **Is the benign state benign at scale?** An identity-like attention map that
  trains fine at 125M may not be harmless at 70B, and the counterexample is
  the whole argument.
- **AdamW² against σReparam, QK-norm and QK-clip.** Four remedies, one failure,
  and the closest thing to a comparison is that each paper beats plain AdamW.
- **Does SEC predict crashes prospectively?** The curves are shown for runs
  already known to have crashed. Used as an early-warning signal — flag the run
  before it diverges — it would be worth more than the optimizer.
