---
status: Read
paper: LIT-040
title: 'Scaling Laws for Autoregressive Generative Modeling'
version: 1
tags:
- training-optimization
date: '2026-09-09'
summary: >-
  Extends the language scaling laws to image, video, multimodal and mathematics, finding the same power-law-plus-constant form and a nearly domain-independent exponent for optimal model size, N_opt(C) ∝ C^0.7. That exponent implies D ∝ N^0.4 — sub-linear data scaling, which Chinchilla later overturned. The paper also flags the inconsistency that overturned it.
---

# NOTE-tmpyo7dp: Scaling Laws for Autoregressive Generative Modeling

## Contribution

Takes the Kaplan-era scaling laws out of language and shows the same form holds
in **four more domains**: generative image modelling, video, multimodal
image↔text, and mathematical problem solving. In all of them, autoregressive
transformers improve smoothly with model size and compute as a **power law plus
a constant** — the constant being an irreducible loss, the entropy of the data.

The striking result is that the compute-to-optimal-model-size exponent is
**nearly universal**: `N_opt(C) ∝ C^β` with `β ≈ 0.7` across every domain.

## Key insight

The separation of loss into *reducible* and *irreducible* parts is what makes
cross-domain comparison possible at all. Raw losses in nats/token are not
comparable between images and equations; the reducible component's *exponent*
is. Fit `L = L_∞ + (N₀/N)^α` and the interesting quantity is `α`, not `L`.

The second insight is downstream and was, in hindsight, wrong. If
`N_opt ∝ C^0.7` and `C ∝ N·D`, then `D ∝ N^0.4` — **dataset size should grow
sub-linearly in model size**, and the paper says so: "even allowing for
significant errors or deviations, this strongly suggests sub-linear scaling of
dataset size with model size." Chinchilla's answer, two years later, is
`D ∝ N` — equal proportions.

## Assumptions

- **One epoch.** The `D ∝ N^0.4` conclusion is explicitly conditioned on
  training on each data element once.
- **The fitted form is right.** Power-law-plus-constant is assumed and fitted,
  not derived.
- **The exponent transfers.** The universality claim rests on fits across
  domains that differ by orders of magnitude in absolute loss.
- Autoregressive transformers only; 2020 scales.

## Key results

- **`N_opt(C) ∝ C^0.7`, β ≈ 0.7 in every domain** — image, video, multimodal,
  math, and language taken from the GPT-3 paper. Figure 2.
- **Individual-image loss scales with model size the same way the mean does**,
  and the same is expected of other modalities. The scaling law is not an
  artefact of averaging over a heterogeneous distribution.
- **Larger models do not generalise "more strongly."** On mathematical
  extrapolation to harder problems, performance depends *predominantly on
  performance on the training distribution* and is otherwise independent of
  model size. The same holds off-distribution for images: YFCC100M→ImageNet
  loss depends only on YFCC100M loss.
- **Section 6 names the inconsistency.** The `L(C)` and `L(D)` trends, if
  extrapolated, cross — and they cannot, since every learning curve must lie
  above `L(D)`. The intersection "suggests a breakdown of some trend." The
  paper also notes projections are **extremely sensitive**: ±5% on the optimal
  model-size exponent visibly moves the conclusion.
- Larger models approach the `L(D)` bound more closely, i.e. **optimisation
  becomes more effective as models grow**, which is a statement about sample
  efficiency rather than capacity.
- They cannot estimate the entropy of natural language even with the largest
  language models available.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Power-law-plus-constant describes loss in all four new domains | strong | fits across domains, Table 1 |
| C2 | `N_opt(C) ∝ C^0.7` with a near-universal exponent | strong within its regime | fitted in every domain |
| C3 | Therefore `D ∝ N^0.4`, sub-linear | **superseded** | a corollary of C2 under one-epoch training; Chinchilla measures `D ∝ N` |
| C4 | Model size does not buy strong generalisation | strong | isolated on math extrapolation and on off-distribution image loss |
| C5 | The compute and data scaling laws are mutually inconsistent | strong | Section 6, and the reason to distrust C3 |
| C6 | Larger models are more sample-efficient | moderate | learning curves approaching `L(D)` |

## Method

Train families of autoregressive transformers per domain across model sizes
and compute budgets. Fit `L = L_∞ + (N₀/N)^α` for model size and the analogous
form for compute. Read `N_opt(C)` off the compute-scaling envelope.

## Concepts

- **Reducible vs irreducible loss** — the decomposition that makes the
  exponents comparable across modalities.
- **The domain-independent exponent** — the paper's headline, and the reason
  scaling-law thinking spread out of language.
- **An inconsistency you can see but not resolve** — Section 6 is a model of
  reporting a defect in your own framework.

## Connections

Sibling to Kaplan (`LIT-028`), which `#114` read: same lab, same year, same
functional form, and `LIT-028` carries `LR(N)` and the schedule choice that
Chinchilla later identified as the source of the wrong allocation. This paper
carries the multi-domain generalisation *and* the sub-linear data conclusion,
so it is the second half of the pre-Chinchilla picture.

`LIT-099` (PaLM 2) independently re-derives the scaling laws at larger compute
and lands on **1:1** — the record therefore contains the full arc:
Kaplan/this paper (sub-linear, 2020) → Chinchilla (1:1, 2022) → PaLM 2
(1:1 confirmed independently at larger scale, 2023).

<!-- inactive-ok-block: SOTA-130 — Proposed, named as the neighbourhood this 2020 measurement bears on rather than relied on -->
C4 also connects to the reasoning literature: "larger models do not extrapolate
better once you control for in-distribution loss" is a 2020 statement of
something the record's `SOTA-130` neighbourhood keeps re-encountering.

## Recommendations

- **R1** — Fit and report the *reducible* loss exponent, not the raw loss, when
  comparing across data distributions. *Topic:* analysis and evaluation.
  *Strength:* strong.
- **R2** — Do not read improved benchmark performance from a larger model as
  better generalisation; check whether it is explained by in-distribution loss.
  *Strength:* strong, and C4 is a clean isolation.
- **R3** — Treat a scaling-law extrapolation as sensitive to its exponent at
  the ±5% level. *Strength:* strong, and stated by the authors about their own
  projections.
- **R4** — Do **not** use `D ∝ N^0.4`. *Strength:* superseded by Chinchilla;
  recorded so the number is not picked up from this paper.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.** Its
allocation conclusion is superseded, and the record already sources the
successor.

What the reading is worth is R3 and R4 as reading instructions. This document
sits in the anthology with `status: Active` and contains a prominently derived
`D ∝ N^0.4` that the record elsewhere says is wrong. Before this reading the
document's four takeaways — "universal scaling behaviours", "compute-optimal
model sizing", "resource allocation guidance" — advertised exactly the
superseded conclusion without stating it, so a reader could neither use it nor
know to distrust it. Now the takeaways name the number *and* say it was
overturned.

That is the most useful thing a note-repair pass can do for a superseded
paper: not retire it, but stop it being quietly wrong.

## Limitations

- 2020 scales, and the compute-scaling figures for language are imported from
  the GPT-3 paper rather than measured here.
- One epoch throughout, which is the condition C3 depends on and which no
  modern run satisfies.
- The universality of β ≈ 0.7 is a fit across four domains, not a derivation.
- No estimate of natural-language entropy, so `L_∞` for the domain everyone
  cares about is unknown.

## Open questions

- Section 6's inconsistency was resolved by Chinchilla changing the schedule
  methodology. Is the inconsistency *fully* accounted for by that, or is there
  residue? The paper poses a question the successor answered by other means.
- C4 — model size buys no strong generalisation — has aged into one of the
  live disputes about reasoning models, and this is a 2020 measurement of it
  that nobody cites.
