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
version: 5
history:
- version: 2
  date: '2026-09-23'
  note: >-
    A second source of error named, from a 2018 paper the record did not
    hold. The error bar this practice asks for is spread around the FID
    estimator's own mean; the estimator is biased, and the offset is
    shared by every seed. Averaging runs does not touch it.
- version: 3
  date: '2026-09-24'
  note: >-
    Adds cases from the video line's readings (#331): MAGVIT-v2's 1.78
    against 1.79 "beats diffusion" claim is inside the floor. VDM's
    single-run gaps survive it. The recommendation is unchanged.
- version: 4
  date: '2026-09-25'
  note: >-
    Sources the guidance items. This practice told a reader to search the
    classifier-free guidance scale per cell and quantified the noise ±0.05 on it
    injects, while the record held no paper for the technique. LIT-693 is now
    filed, and its sweep is a stronger argument than the one made here: the weight
    moves FID seventeen-fold and IS almost five-fold from a single checkpoint, so
    fixing it is prior to any seed-noise question rather than a refinement of one.
    Recommendation, status and consensus unchanged.
- version: 5
  date: '2026-09-25'
  note: >-
    Adds the one instance the record holds of the "measure your own floor"
    instruction being followed elsewhere, and it lands far higher:
    LIT-tmptzz06 reports FID varying "by up to ±14%" between consecutive
    StyleGAN training iterations on FFHQ. Different family, different dataset and
    a different quantity — snapshots of one run, not seeds — so it is a second
    calibration point rather than a correction. Also notes what a second metric
    does to the error bar this practice asks for. Recommendation, status,
    consensus and the 2% figure unchanged.
tags:
- analysis-and-evaluation
- generative-modeling
date: '2026-09-21'
source:
- LIT-501
- LIT-693
- LIT-tmptzz06
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
extended_by:
- SOTA-383
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

   The record now holds the measurement that makes this non-negotiable rather
   than fastidious. [LIT-693](../literature.d/LIT-693.md) sweeps the guidance weight on ImageNet 64×64 and
   takes **FID from 1.55 to 26.22 while IS goes from 66.11 to 260.2** — a
   seventeen-fold swing in one metric and a near-quintupling of the other, from
   one checkpoint. Against that, a seed-noise floor is a rounding error: a
   comparison that does not fix the guidance weight is not measuring the
   models.

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

**A second calibration point, and it is much larger.** The instruction
above is to port the protocol and measure your own floor; [LIT-tmptzz06](../literature.d/LIT-tmptzz06.md) is the one
case in this record where somebody did. Training StyleGAN on FFHQ, they report
FID varying "by up to **±14%** between consecutive training iterations" — quoted
in passing, while explaining why they amortise over snapshots. That is a
different family, a different dataset and a different quantity (consecutive
snapshots of one run rather than independent seeds), so it does not touch the 2%
this practice states, and a ±range over
consecutive snapshots is not the coefficient of variation over seeds that the 2%
is. What it does is price the warning: the two numbers are an order of magnitude
apart in a setting that differs in every respect, so reusing either across
families would be exactly the mistake this practice's own Conditions section
predicts. Nobody has measured a GAN's seed-to-seed floor, or an LM-scale
diffusion model's snapshot-to-snapshot one.

**With two metrics the error bar becomes a frontier.** This practice asks for a
spread over seeds because the best-of-N snapshot is an overestimate. [SOTA-425](SOTA-425.md)
asks for precision and recall beside FID, and [LIT-tmptzz06](../literature.d/LIT-tmptzz06.md) shows that the
snapshots of a single run span a range of precision/recall tradeoffs — so "the
best snapshot" is no longer defined and the amortisation has to be a Pareto
frontier instead of a mean and a spread. The two practices are compatible and
neither one alone tells you what to report.

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

**The error bar does not cover the estimator.** Everything measured here is
spread at a fixed sample count. The FID estimator is also *biased* — the
offset depends on the distribution being measured, so it is shared by every
seed and survives any amount of averaging — and no unbiased estimator exists
([THEORY-095](../theory.d/THEORY-095.md), from a paper published eight years before this
one). A run-to-run interval of 1.3% says nothing about whether the centre of
that interval is where the true distance is. Fix `n` as well:
[SOTA-383](SOTA-383.md).

**Finite panel.** 20–25 training seeds, 10 sampling seeds, nothing past
SiT-XL or 2M steps. Production-scale behaviour is an extrapolation and the
source says so.

## Cases from the video line

- **MAGVIT-v2** ([LIT-623](../literature.d/LIT-623.md), [NOTE-342](../notes.d/NOTE-342.md)) claims its tokenizer lets a language
  model beat diffusion at ImageNet 256 with FID 1.78 against MDT's 1.79.
  That is a 0.01 gap from one run each, far inside this practice's floor.
  Its 512 result (1.91 against VDM++'s 2.65) is large enough to survive.
- **VDM and Video LDM** ([LIT-627](../literature.d/LIT-627.md), [LIT-621](../literature.d/LIT-621.md)) report every ablation as a
  single run. VDM's gaps, such as FVD 202 → 58 for joint image training,
  are far larger than the floor. Which of Video LDM's gaps clear it has
  not been checked.

The floor was measured for image FID on SiT. Nobody has measured it for
FVD, so these readings apply the image number as the best available
guess.

## Related

[SOTA-305](../practices.d/SOTA-305.md) asks for the token count and input resolution beside a
*reconstruction* FID. This asks for an error bar over training seeds beside a
*generation* FID. Neither implies the other and they were derived
independently, from different papers, on different halves of the same metric
family — which is a fact about how many ways there are to publish a Fréchet
distance that does not mean what it looks like.
