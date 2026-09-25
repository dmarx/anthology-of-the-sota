---
number: 228
status: Read
formerly:
- NOTE-tmp290m1
paper: LIT-479
title: 'The Diffusion Duality'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    MDLM and SEDD are now filed (LIT-tmptr16a, LIT-tmpfb0m4); the sentence
    saying they are not in the record now says when that was true.
date: '2026-09-21'
summary: >-
  Reading it: the theorem is elegant and the ablation says it accounts for
  under half the likelihood gain. What the paper actually establishes is a
  regime split — masked diffusion wins on quality at many steps, uniform-state
  wins below about 32, and the reason is architectural rather than tuned.
---

<!-- inactive-ok-file: SOTA-157 — Proposed, and named to say this document does
     NOT contest it: masked diffusion is ahead on likelihood in the source's own
     tables, and the claim here is about a regime that practice does not cover -->

<!-- inactive-ok-file: SOTA-254 — Proposed, and named in the same sentence and for
     the same reason as SOTA-157 -->

# NOTE-228: The Diffusion Duality

## Contribution

A bridge between two literatures that had been developing separately. Discrete
diffusion had its own machinery and comparatively little of it; Gaussian
diffusion had a decade of training and sampling technique. Showing that
uniform-state discrete diffusion *is* the `argmax` of a Gaussian diffusion
makes that technique portable in principle.

What is true afterwards that was not before: a specific, checkable reason to
expect Gaussian-diffusion methods to work on one of the two discrete families —
and a demonstration with two of them, a curriculum and a distillation scheme.

## Key insight

`argmax` is the zero-temperature limit of a tempered softmax, so the map that
defines the duality can be *annealed*. That is the move that turns a theorem
into a training procedure.

The reason it helps is specific and worth keeping: as vocabulary size grows, a
narrow band of the Gaussian noise parameter already spans the whole discrete
one — so the discrete latents ought to be nearly noiseless there, and yet the
loss does not fall, because `argmax` is violently sensitive to small
perturbations and throws the extra signal away. Letting the model see the
continuous latent recovers it. Temperature is then a difficulty dial on the
reconstruction task.

## Assumptions

- **Uniform-state**, not absorbing-state. The duality does not exist for
  masked diffusion, and the conclusion names that as the strategic bet.
- **The training loss is not a valid NELBO** except in the limit `T → ∞`,
  `τ → 0`; the model consumes a continuous variable while the bound is defined
  for a discrete process. Evaluation reverts to the proper discrete bound.
- **Denoising model takes both continuous and discrete latents**, unlike prior
  discrete diffusion models.
- **float64 for all sampling**, to avoid a known low-precision artefact in
  masked-diffusion Gen PPL.
- Curriculum schedule fixed by hand: one `τ` for the first 500K steps, another
  to 1M.

## Key results

- LM1B / OWT test PPL: Duo 29.9 / 25.2; UDLM 31.3 / 27.4; SEDD Uniform 40.3 /
  29.7; **MDLM 27.0 / 23.2**; AR transformer 22.3 / 17.5.
- Zero-shot, 7 datasets: beats every uniform-state and Gaussian baseline on
  all 7; beats SEDD Absorb on 4/7; beats **MDLM on 1/7**; beats the AR
  transformer on **3/7** (Lambada, Pubmed, Arxiv).
- Gradient variance on the top-100 highest-variance weights falls by an order
  of magnitude with the curriculum.
- Duo at 510K steps beats UDLM at 1M by ~1.5 PPL — the "2× faster" claim.
- Distillation: 1024 → 16 steps at matched Gen PPL (64×); Greedy-Tail → 8
  steps (128×), better Gen PPL, lower entropy.
- Distilled Duo beats distilled MDLM below ~32 NFE; MDLM wins above.
- MDLM+SDTT matches AR Gen PPL at entropy 5.4 vs 5.6 — less diverse.
- Ablation: the 3-point gain over UDLM splits ~1.7 (Rao-Blackwellized ELBO)
  and ~1.3 (curriculum).
- Ablation: using the denoising model rather than EMA weights as the
  distillation teacher works better, against common practice in consistency
  models.

## Claims

**Proved:** the duality itself, with the marginal transformation and the
transition ODE both derived and one verified empirically.

**Measured and honest about its composition:** the likelihood improvement,
which the ablation splits roughly evenly between a variance-reduced estimator
and the duality-derived curriculum. So the theorem earns about 1.3 of the 3
points, and the paper prints that.

**Measured and the most useful thing here:** the regime split. Below ~32
function evaluations uniform-state beats masked; above, masked wins. The
mechanism is stated — masked models emit tokens independently and cannot
revise them, uniform-state models can overwrite earlier errors — and it is
structural, so it should survive tuning.

## Method

Theory plus two applications, evaluated against the leading uniform-state
models (SEDD Uniform, UDLM), a Gaussian model (Plaid), masked models (MDLM,
SEDD Absorb, D3PM), and an autoregressive transformer, on LM1B and
OpenWebText with seven zero-shot datasets; distillation compared against
MDLM+SDTT at matched rounds.

## Concepts

The *diffusion transformation operator* relating the two processes' noise
parameters; tempered-softmax relaxation of `argmax` as a curriculum; *Discrete
Consistency Distillation*; the *Greedy-Tail* sampler; number of function
evaluations (NFE) as the sampling budget.

## Connections

- [SOTA-157](../practices.d/SOTA-157.md) and [SOTA-254](../practices.d/SOTA-254.md) recommend masked diffusion for
  language modelling. This **confirms** them on likelihood — MDLM stays ahead
  on 6 of 7 zero-shot datasets and on both training corpora — and adds a
  regime those practices do not address.
- The record's flow and interpolant cluster is the Gaussian side of the bridge
  this paper builds. The bridge is the contribution; neither end is new.
- MDLM and SEDD, the strongest baselines here, were **not in the record** when
  this was read; they arrived as table entries, the third family this session
  to enter that way. Both are now filed and read (LIT-tmptr16a, LIT-tmpfb0m4),
  from the survey of skipped readings of 2026-09-25.

## Bearing on the record

One practice, `Proposed`, about the few-step regime; one account, about why
Gaussian technique transfers to one discrete family and not the other.

The thing to resist is reading "beats autoregressive on 3/7" as a headline.
It is true, the comparison is conservative because diffusion numbers are upper
bounds, and it is 3 of 7 against a transformer that wins the other four by
wide margins — 82.05 vs 89.35 on PTB, 25.75 vs 33.57 on Wikitext.

## Limitations

**The theorem is under half the empirical gain**, by the paper's own ablation.

**Masked diffusion is still better at what the record currently recommends it
for.** Nothing here moves `SOTA-157` or `SOTA-254`.

**Scale.** LM1B and OpenWebText at GPT-2 size. A decision about few-step
generation would be made at serving scale, and there is no evidence there.

**One lab, and it wrote the main baseline.** MDLM is from the same group,
which cuts both ways: the comparison is likely to be competently run, and it
is not independent.

**The curriculum schedule is hand-set** — one temperature for 500K steps, then
another — with a bias-variance study on a 150K-step LM1B run to justify the
choice. No rule for picking it elsewhere.

## Open questions

- Does the few-step advantage survive at serving scale, where the step budget
  is chosen for latency and the model is far larger?
- Can other Gaussian techniques cross the bridge? The paper demonstrates two
  and claims the general possibility; the value of the theorem depends on the
  third and fourth.
- What is the Rao-Blackwellized ELBO worth on its own, in other uniform-state
  models? It is 1.7 of the 3 points here and is independent of the duality.
