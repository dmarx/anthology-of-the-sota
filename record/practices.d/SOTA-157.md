---
number: 157
status: Proposed
formerly:
- SOTA-tmp704hb
promote_when: >-
  A pretraining report on a released model above 8B trained this way, or a
  controlled comparison at matched compute against an autoregressive baseline
  that got its own hyperparameter sweep, from a group other than this one.
  What would not move it: further capability demonstrations at 8B against
  published baseline numbers, which is what the evidence already is.
consensus: unreplicated
consensus_note: >-
  One group, one model. The field has not replied — which is not the same as
  agreeing, and not the same as the dispute `contested` describes. Every
  other practice in this record assumes the paradigm this one rejects, so
  the disagreement is wide and one-sided.
title: 'Train the language model as a masked diffusion model rather than autoregressively'
version: 3
history:
- version: 2
  date: '2026-09-19'
  note: >-
    Gained a second line of evidence and a specialization. Prabhudesai et al.
    (LIT-442) fit a data-constrained scaling law for masked diffusion and
    report a data-reuse half-life sixteen times the autoregressive one, which
    is the first reason in the record to prefer this objective that is not a
    capability comparison. SOTA-254 carries that conditional form. This
    practice's unconditional recommendation and its `promote_when:` are
    unchanged: the new evidence is about data efficiency below 100M unique
    tokens, not about scale.
- version: 3
  date: '2026-09-25'
  note: >-
    MDLM (LIT-702) and SEDD (LIT-701) filed and added as
    corroborating sources, for the *masked* in the title only: both show the
    absorbing process is the right discrete corruption, which LIT-217 does
    not test. Neither supports *rather than autoregressively*. MDLM's
    retrained, same-backbone comparison is the controlled second-group test
    `promote_when:` asks for in all but its conditions, and at 110M it goes
    to autoregression. Recorded in a new section; `promote_when:` and status
    unchanged.
tags:
- model-architecture
- generative-modeling
date: '2026-09-07'
source:
# LIT-217 is the only evidence for the half of the title that says "rather
# than autoregressively". The comparison it reports is against its own ARM
# baselines plus published LLaMA3 8B numbers — which is what promote_when is
# asking somebody else to redo.
- LIT-217
# These two corroborate the other half — *masked* rather than another
# discrete diffusion — and nothing else. On diffusion versus AR their
# controlled numbers favour AR; see "What MDLM and SEDD support".
- LIT-702
- LIT-701
introduced_by:
- LIT-217
implementations:
- 'LLaDA 8B'
summary: >-
  Nie et al. (2025), [LIT-217](../literature.d/LIT-217.md) — hold the paradigm fixed (pretrain, then
  SFT) and swap only the factorization: a forward masking process and a
  reverse process predicting masked tokens, optimizing a likelihood lower
  bound. Competitive with LLaMA3 8B on in-context learning; past GPT-4o on
  reversal poem completion. Filed `Proposed` — one group, one model, 8B.
extended_by:
- SOTA-254
---

# SOTA-157: Train the language model as a masked diffusion model rather than autoregressively
<!-- inactive-ok-file: SOTA-254 — Proposed, and filed in this same contribution as the conditional form of this practice -->

## Source

Nie et al. (2025), [LIT-217](../literature.d/LIT-217.md) — [ARXIV-2502.09992](https://arxiv.org/abs/2502.09992).

What is being challenged is an identification rather than a benchmark. The
capabilities everyone attributes to LLMs — in-context learning, instruction
following, scalability — are routinely attributed to *autoregressive*
modelling specifically. LLaDA holds the surrounding paradigm fixed and swaps
only the factorization, which is what makes the result an argument about that
identification.

A forward process masks tokens; a reverse process, parameterized by a
Transformer, predicts them; training optimizes a lower bound on the
likelihood. It is a principled generative model rather than a denoising
heuristic, and that is what gives it probabilistic inference.

## Conditions, and what is not established

Reported: LLaDA 8B is competitive with LLaMA3 8B on in-context learning, and
after SFT shows instruction-following in multi-turn dialogue. It surpasses
GPT-4o on reversal poem completion — the sharpest result here, because it is
the one place where the change in factorization predicts the change in
behaviour in advance rather than after the fact.

The comparison is against **self-constructed ARM baselines** plus published
LLaMA3 numbers, and "comparable to our self-constructed ARM baselines" is the
honest form of the claim. This is a demonstration that the paradigm scales,
not a report that it wins, and one group has made it at one size.

## What MDLM and SEDD support, and what they do not

The practice's title makes two choices, and until 2026-09-25 the record held
evidence for only one of them.

**Masked, rather than another discrete diffusion.** Sahoo et al.,
[LIT-702](../literature.d/LIT-702.md), and Lou et al., [LIT-701](../literature.d/LIT-701.md), are the evidence. SEDD trains
absorbing-state and uniform-state models on the same architecture and recipe,
and absorbing wins on every table (LM1B ≤32.79 against ≤40.25). MDLM derives
the masked-diffusion objective LLaDA trains with — a schedule-weighted average
of masked-LM losses — and beats SEDD at matched training on every likelihood
table it reports. [LIT-479](../literature.d/LIT-479.md)'s uniform-state model narrows the gap and does not
close it. That half of the recommendation is well supported, at GPT-2 scale.

**Rather than autoregressively.** Neither paper supports it, and one argues
the other way. MDLM retrains an autoregressive baseline on its own backbone
and data, which makes it the only same-architecture comparison in the record
from a group other than LLaDA's. AR wins in-domain: LM1B 22.32 against ≤27.04
at 33B tokens and 20.86 against ≤23.00 at 327B; OpenWebText 17.54 against
≤23.21. That is with the AR arm trained for **half the optimizer steps**,
because "matched tokens" counts only the masked tokens a diffusion model is
scored on. MDLM wins 3 of 7 zero-shot sets, which its authors offer as a
hypothesis about robustness, and its own checklist lists underperforming
autoregression as the limitation. SEDD's "beats GPT-2" is 3 of 5 sets against
the released model, trained on different data. Its retrained LM1B baseline
is 31.98 exact against SEDD's ≤32.79 bound.

None of that meets `promote_when:`. It is 110M parameters, the steps are not
matched, and neither arm was swept. It is recorded because it is the nearest
thing to the requested test that exists, and at small scale it favours the
baseline. The case for this practice over autoregression still rests on
[LIT-217](../literature.d/LIT-217.md)'s demonstration at 8B and on [SOTA-254](SOTA-254.md)'s conditional, not on the two
papers that made masked diffusion work.

## What adopting this would cost, which nobody has costed

Most of this registry is advice about training an autoregressive
transformer, and none of it says so. Under this practice the registry splits,
and the split has not been checked by anyone:

- **Carries over unchanged** — the optimizer and schedule material (AdamW's
  decoupled decay, µP, the peak-LR power law), the capacity material
  (mixture-of-experts routing and granularity), data packing. These are about
  optimization and capacity, not about the factorization.
- **Does not carry over** — fill-in-the-middle training, multi-token
  prediction, speculative decoding, KV-cache compression, and context
  extension by RoPE rescaling. Each exists *because* generation is
  left-to-right and cached; under a masked-diffusion decoder some are
  unnecessary and some are incoherent.

That sort is one reader's first pass and the boundary runs through the
attention material, where a practice can be about the cache or about the
pattern. It is recorded here because a recommendation whose adoption cost is
unknown should say so rather than imply the cost is zero.

## A second line of evidence, conditional where this one is not

Prabhudesai et al., [LIT-442](../literature.d/LIT-442.md), give the first reason to prefer this
objective that is not a capability comparison. Refitting [LIT-166](../literature.d/LIT-166.md)'s
data-constrained scaling law with the objective swapped, the half-life of
data reuse is 512.85 for masked diffusion against 31.93 for autoregressive
training — so under a fixed corpus the diffusion model keeps extracting
signal from repeated data roughly sixteen times longer.

It comes with a boundary, which is why it is filed as its own practice rather
than folded in here. Below a computable critical compute threshold the
autoregressive model is better by a wide margin — 7.07 against 10.65 in
validation loss at the single-epoch compute-optimal point. [SOTA-254](SOTA-254.md)
carries that conditional form.

Nothing in it moves this practice's own `promote_when:`. The evidence is
about data efficiency at unique-token budgets below 100M, and what this one
asks for is scale.

## Known implementations

- LLaDA 8B. No frontier report in this record trains this way.
