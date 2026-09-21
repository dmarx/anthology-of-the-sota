---
number: 307
status: Active
formerly:
- SOTA-tmpmd52k
consensus: unreplicated
consensus_note: >-
  One group, one combination — SiT under flow matching on class-conditional
  ImageNet `256×256`, scored by Inception-V3 — and the authors say the ~1.3%
  figure is a calibration target for that combination rather than a constant.
  What is not in doubt is the shape: several hundred trained networks, a
  control ruling out numerical non-determinism, and the same floor at four
  model sizes and ten compute budgets. Against it, the prevailing practice in
  the literature is a single number from a single run, which is not a
  competing measurement but the absence of one.
title: 'Report generative FID as an error bar over several training seeds, and treat any gap below about 2% of the mean as inconclusive'
version: 1
tags:
- analysis-and-evaluation
- generative-modeling
date: '2026-09-21'
source:
- LIT-501
introduced_by:
- LIT-501
implementations: []
summary: >-
  Dufour, Efros and Pérez (2026), [LIT-501](../literature.d/LIT-501.md) — on several
  hundred SiT networks, **retraining the same recipe moves FID 3.2× more than
  resampling from a fixed model**, and the coefficient of variation holds at
  **1–2%** across four model sizes and every compute budget to 2M steps.
  Ten times the sampling budget shrinks the small term by `√10` and leaves the
  large one untouched. A lucky training seed is worth up to **2× the compute**.
---

# SOTA-307: Report generative FID as an error bar over several training seeds, and treat any gap below about 2% of the mean as inconclusive

## Source

Dufour, Efros and Pérez (2026), [LIT-501](../literature.d/LIT-501.md) — read as
[NOTE-248](../notes.d/NOTE-248.md).

## When this applies

You are reporting, reading or comparing FID — or a Fréchet-style
distributional metric — for a generative image model, and the comparison is
between recipes, architectures or compute budgets rather than between things
that differ by an order of magnitude.

## Do this

1. **Train several seeds and report the spread.** Three to five is enough to
   matter: with `N` seeds the resolvable gap scales as `2σ/√N`, so `N = 5`
   takes the threshold from ≈0.5–0.8 FID down to ≈0.25 on this family.
2. **Do not substitute sampling seeds for training seeds.** Resampling a fixed
   model shrinks the wrong term. Ten times the sampling budget shrinks
   within-seed jitter by `√10 ≈ 3.2` and leaves the between-seed envelope
   exactly where it was.
3. **Treat a gap below ≈2× the CoV as inconclusive** — roughly 3–4% of the
   baseline FID on this family — unless multiple seeds confirm it. Use it as a
   cheap first-pass filter before spending on seeds.
4. **Tune and evaluate with the same FID you intend to report.** Guided and
   unguided FID disagree about which seeds and which hyperparameters are best.
5. **If you use classifier-free guidance, search the scale per cell** — golden
   section converges in a logarithmic number of evaluations — and report the
   search tolerance with the number, because ±0.05 on the scale injects noise
   comparable to the whole within-seed floor.

## What it buys, and what it costs to ignore

Converged SiT-B/2, 25 training seeds × 10 sampling seeds, 400k steps, no CFG:

| | `σ` | CoV |
|---|---|---|
| between training seeds | **0.438** | ≈1.3% |
| within one model, across sampling seeds | 0.137 | ≈0.4% |

**3.2×.** Per-seed means span 33.75 to 35.42; the 95% interval on the grand
mean is 34.74 ± 0.18, with a one-`σ` distance of 0.44 FID — which the source
observes "is already larger than the headline gain claimed in many recent
papers".

And the floor does not go away with effort: across SiT-S/B/L/XL at every
100k-step checkpoint to 2M, CoV stays inside `[0.74%, 2.06%]` in all 76
cells, non-monotonically in size (S 0.74%, B 1.24%, XL 1.42%, L 1.72%).
Reproducibility here is a property of the metric and the objective, not of
scale or budget.

The cost of ignoring it is stated most sharply by the compute result: anchored
to the FID the unluckiest of ~20 seeds reaches at 2M, the luckiest gets there
**1.25× faster on S/B, 1.82× on L and 2.0× on XL**. A single-seed paper
claiming a ~1.3× speedup on this architecture is competing with what the seed
lottery hands out for free.

## Why the variance is there

Three training-time generators, varied one at a time against a full-random
`σ` of 0.438: per-step flow-matching noise **0.336** (77%), initialisation
**0.294** (67%), data order **0.221** (51%). The loss noise leads, which
contradicts the folk version in which seeds mostly mean initialisations. They
combine sub-additively — quadrature predicts 0.50 against an observed 0.44 —
so one-at-a-time ablations overstate what fixing any single source recovers.

**It is not floating-point non-determinism**, and the source runs the control
that shows it: 24 retrains with init, data order and training noise all fixed,
leaving only multi-GPU reduction-order effects. The EMA weights end 5–6% of
their norm apart — genuinely different networks — and `σ_between` falls to
0.047, *below* the 0.119 sampling floor. The lottery is in the draws the
recipe intends.

## Conditions

**One combination, and the number is calibrated to it.** SiT, flow matching,
class-conditional ImageNet `256×256`, Inception-V3 features. The authors say
plainly that ~1.3% is "a calibration target for that combination, not a
universal constant", and that other backbones, objectives, latent-versus-pixel
diffusion, text-to-image or other Fréchet variants may sit elsewhere. **Port
the protocol, measure your own floor.**

**The appendix reports one metric behaving differently.** Fidelity metrics —
DINOv2 FID, precision, density, coverage — track Inception FID closely;
**recall is the outlier**. A practice written from FID should not be assumed
to cover diversity metrics.

**Per-cell guidance tuning helps and does not solve it.** Golden-section CFG
search takes CoV from 1.26% to 0.67%, but the between-to-within ratio only
falls from 3.2× to 1.87×, so sampling-seed reporting matters *more* under a
tuned protocol, not less. And it reshuffles the winners: Spearman ρ = 0.73
between guided and unguided seed rankings, with 8 of 25 seeds moving five or
more places. Numbers from the two protocols should not be compared across
papers.

**Seed rankings are unstable through the first half of training.** Spearman ρ
against the final 2M ranking is 0.39–0.61 at 200k and 0.65–0.81 at 1.1M.
Picking a seed on an early checkpoint and reusing it for the long run is close
to picking at random.

**Finite panel.** 20–25 training seeds, 10 sampling seeds, nothing past
SiT-XL or 2M steps. Production-scale behaviour is an extrapolation and the
source says so.

## Related

[SOTA-305](../practices.d/SOTA-305.md) asks for the token count and input resolution beside a
*reconstruction* FID. This asks for an error bar over training seeds beside a
*generation* FID. Neither implies the other and they were derived
independently, from different papers, on different halves of the same metric
family — which is a fact about how many ways there are to publish a Fréchet
distance that does not mean what it looks like.
