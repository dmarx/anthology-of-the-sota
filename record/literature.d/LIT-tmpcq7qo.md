---
status: Active
title: 'Diffusion Models Beat GANs on Image Synthesis'
version: 1
tags:
- generative-modeling
- model-architecture
- vision-and-graphics
- analysis-and-evaluation
date: '2026-09-25'
published: '2021-05-11'
arxiv: '2105.05233'
first_author: 'Dhariwal'
keywords:
- 'classifier-guidance'
- 'adm'
- 'adaptive-group-normalization'
- 'fidelity-diversity-tradeoff'
- 'unet-ablation'
- 'fid'
- 'precision-recall'
implementations:
- 'openai/guided-diffusion'
extends:
- LIT-036
- LIT-439
extended_by:
- LIT-693
compared_against:
- LIT-036
- LIT-560
- LIT-561
- LIT-693
summary: >-
  Dhariwal and Nichol (2021), ARXIV-2105.05233. Two things, and the record uses
  both: **ADM**, the diffusion U-Net that half the later image papers here run
  on, fixed by a single-run ablation on ImageNet 128×128; and **classifier
  guidance**, a gradient scale `s` on a noisy-image classifier that trades recall
  for precision and IS. The trade is not monotone in the direction people quote:
  on an *unconditional* 256×256 model, `s = 1` makes FID **worse** (26.21 →
  33.03) and only `s = 10` improves it (12.00); on the conditional model `s = 1`
  is best (4.59) and `s = 10` is worse again (9.11). Every headline cell is the
  best of a small scale sweep scored on the metric it reports.
---

# LIT-tmpcq7qo: Diffusion Models Beat GANs on Image Synthesis

Dhariwal and Nichol (2021) — ARXIV-2105.05233

## Key takeaways

**The architecture, and how it was chosen.** Starting from the DDPM U-Net
(LIT-036), Table 1 ablates five changes on ImageNet 128×128 at batch 256 with
250 sampling steps, FID at 700K and 1200K iterations against a baseline of
15.33 / 13.21: more attention heads (−0.54 / −0.82), attention at 32, 16 and 8
rather than 16 alone (−0.72 / −0.66), BigGAN residual blocks for up- and
downsampling (−1.20 / −1.21), all three together (−3.14 / −3.00), and
**rescaling residual connections by 1/√2, which hurts** (+0.16 / +0.25) and is
dropped. Depth helps FID but loses on wall clock (Fig. 2), so width is kept. 64
channels per head is chosen on wall clock, "on par" in final FID. Adaptive
group normalization — timestep and class embedding as a scale and shift after
GroupNorm — gives 13.06 against 15.08 for addition-then-GroupNorm (Table 3).
Every cell is one run; Fig. 2's curves use 10k samples, not 50k.

**Classifier guidance, as derived.** Train a classifier on the *noisy* images
the diffusion model sees (the U-Net's downsampling trunk plus an attention pool),
then shift each reverse step's mean by `sΣ∇log p(y|x_t)` (Algorithm 1), or for
DDIM subtract `√(1−ᾱ_t)·∇log p(y|x_t)` from the predicted noise (Algorithm 2).
The scale is justified as sampling from a sharpened classifier, `p(y|x)^s / Z`.
The derivation is Sohl-Dickstein et al.'s (LIT-439) and Song et al.'s; the scale
and the practice of using it are this paper's.

**The trade is not monotone, and the direction depends on the model.** Table 4,
ImageNet 256×256, 2M iterations each:

| model | scale | FID ↓ | IS ↑ | precision | recall |
| --- | --- | --- | --- | --- | --- |
| unconditional | — | 26.21 | 39.70 | 0.61 | 0.63 |
| unconditional | 1.0 | **33.03** | 32.92 | 0.56 | 0.65 |
| unconditional | 10.0 | 12.00 | 95.41 | 0.76 | 0.44 |
| conditional | — | 10.94 | 100.98 | 0.69 | 0.63 |
| conditional | 1.0 | **4.59** | 186.70 | 0.82 | 0.52 |
| conditional | 10.0 | 9.11 | 283.92 | 0.88 | 0.32 |

On the unconditional model a scale of 1 is worse than no guidance on every
column but recall: the classifier gave the samples "reasonable probabilities
(around 50%)" and they "did not match the intended classes upon visual
inspection" (§4.3). The scale had to go an order of magnitude past the
theoretically grounded value before guidance helped. On the conditional model
FID is best at an intermediate scale (Fig. 4) while precision and IS keep
rising and recall keeps falling.

**Against BigGAN's truncation trick** (Fig. 5, 128×128): "strictly better" on
the FID–IS trade, but on precision–recall only "up until a certain precision
threshold, after which point it cannot achieve better precision".

**Headline numbers** (Table 5): FID 2.97 at 128×128, 4.59 at 256, 7.72 at 512,
and with 25 DDIM steps 5.98 / 5.44 / 8.41 against BigGAN-deep's 6.02 / 6.95 /
8.43. Guidance combined with an upsampling stack gives 3.94 at 256 and 3.85 at
512 (Table 6); only the low-resolution model is guided. Unconditional LSUN
results beat StyleGAN/StyleGAN2 (LIT-561, LIT-560) with architecture alone,
bedroom 1.90, horse 2.57, cat 5.57 — at **1000** sampling steps; a hand-swept
250-step schedule closes most of that gap (App. J).

**Evaluation hygiene worth taking.** Baselines are re-scored from public samples
or models in one codebase, against the full training set as reference, because
"subtle implementation differences can affect the resulting FID values" (§2.2,
citing Parmar et al.). That is the paper's own reason for not copying numbers
from other papers.

## Where the hedges are

Per DP-010:

- **"We can increase this gradient scale factor by an order of magnitude
  without obtaining adversarial examples"** is in the introduction and has no
  experiment of its own. What stands behind it is visual inspection (Figs. 3, 8)
  and a nearest-neighbour check for memorisation run in Inception-V3 feature
  space (App. C). Every quantitative metric in the paper is computed on Inception
  features, and the paper does not say which network its precision and recall
  use. This is the sentence THEORY-109 is about, and the paper does not test it.
- **The best-scale cells are chosen on the metric they report.** App. I:
  scales swept over [0.5, 1, 2] at 128 and 256, [1 … 5] at 512, and separate
  sweeps for 25-step DDIM, with the winners in Table 14 (0.5, 1.0, 4.0; DDIM
  1.25, 2.5, 9.0). Nothing is held out. It is the practice SOTA-307 tells a
  reader to follow, and here it is the source of every ADM-G number.
- **"The same or lower compute budget" than BigGAN-deep** (App. A) rests on
  converting BigGAN's TPU-v3 estimates at "2 TPU-v3 day = 1 V100 day", which the
  paper asserts rather than measures. The comparison is FID at an early
  checkpoint (ADM-G at 450K: 63 V100-days, FID 5.67) against a published range
  (64–128). Their own naive implementation used 18–25% of the hardware (Table 7).
- **Guidance needs labels.** Stated by the authors: "we have provided no
  effective strategy for trading off diversity for fidelity on unlabeled
  datasets" (§7). That is the gap LIT-693 fills.
- **Lower temperature does not substitute** (App. G): scaling the noise or ε by
  `1/τ` gives no substantial improvement and lowers precision *and* recall.
  One model, one figure.

## Standing in the anthology

Filed because the record was already leaning on it without holding it. It is
the model or the instrument in LIT-676 (DPM-Solver++'s ImageNet table runs on
the 256×256 classifier-guided ADM), LIT-630 and NOTE-340 (flow matching trained
on its U-Net, and a throughput claim measured against its 4.36M-iteration run),
LIT-692 (ablations on the ADM U-Net), and LIT-448 (DiT, which replaces the U-Net
this paper ablated). It is the antecedent LIT-693 is named against, and the
method THEORY-109 raises a suspicion about.

What it adds that the record did not have:

- a source for THEORY-109's subject, including the two facts that bear on it
  from the predecessor's side — the guiding classifier is **not** the Inception
  network that scores, and at `s = 1` the paper itself saw a classifier satisfied
  by samples that did not look like the class;
- the tuned scale for the model LIT-676 stress-tests: its authors' best 25-step
  DDIM scale at 256×256 is **2.5**, giving FID 5.44, and LIT-676 runs it at
  **8.0**;
- the U-Net ablation, as a single-run architecture search, for anybody citing
  "the ADM U-Net" as a settled design.

The reading is NOTE-tmpb6qj9.
