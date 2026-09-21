---
status: Read
paper: LIT-tmpjz53y
title: 'The FID Lottery: which lottery, and how big'
version: 1
date: '2026-09-21'
summary: >-
  Read from the [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) worklist, taken ahead of its dwell rank because
  `SOTA-305` had just landed on the adjacent question. The finding that
  matters is not that FID is noisy but *which* noise dominates: the training
  run, by 3.2×, in a term no amount of extra sampling touches — and a control
  that rules out the boring explanation.
---

# NOTE-tmpimuh6: The FID Lottery: which lottery, and how big

## Contribution

Turned "FID is noisy" from folklore into a measured decomposition, at a scale
that makes the decomposition trustworthy: several hundred SiT networks trained
from scratch on class-conditional ImageNet `256×256`, arranged as an explicit
panel of training seeds × sampling seeds, with the variance split three ways
and a control that eliminates the uninteresting cause.

The useful part is the asymmetry. Everyone knows a single FID has error bars;
almost everyone estimates them the wrong way, by resampling a fixed model.
This shows that term is the small one and quantifies the gap.

## Key insight

There are two lotteries and the field reports the wrong one. The *generation*
lottery — which samples you drew from a fixed network — is what a sampling-seed
confidence interval measures, and it is about 0.4% of the mean. The *training*
lottery — which of the identically-specified models you happened to train — is
3.2× larger, and no amount of resampling reaches it. Ten times the sampling
budget shrinks the small term by `√10` and leaves the large one exactly where
it was.

## Assumptions

- FID is a distribution-level quantity: a Fréchet distance between Gaussians
  fit to Inception features of the reference set and 50,000 generated images.
  It can move on differences too small to perceive, which the paper
  illustrates rather than assuming away.
- One architecture family (SiT S/B/L/XL at patch 2), one objective
  (conditional flow matching), one dataset, one feature extractor.
- Sampling uses a fixed deterministic ODE solver and a fixed NFE, so
  "sampling seed" means only the initial noise draw.
- CFG off by default; enabled only in §4.3, where the scale is searched per
  (training, sampling) seed pair over `[1, 2]` at tolerance 0.01.
- Panels are 20–25 training seeds and 10 sampling seeds — enough for a
  `σ`, thin for a tail.

## Key results

- **§4.1 — the 3.2×.** Converged SiT-B/2, `N = 25`, `K = 10`, 400k steps, no
  CFG: `σ_between = 0.438` (CoV ≈ 1.3%), `σ_within = 0.137` (CoV ≈ 0.4%).
  Per-seed means 33.75–35.42 about a grand mean of 34.74; 95% Student's-`t`
  interval 34.74 ± 0.18, one-`σ` distance 0.44 FID. Within-seed CoV is
  homoscedastic across the 25 seeds, so a single sampling-seed FID carries
  ≈0.14 units of unrepeatable jitter with the model held fixed.
- **§4.2 — the decomposition.** vary-all 0.438 > vary-noise 0.336 (77%) >
  vary-init 0.294 (67%) > vary-data 0.221 (51%). Within-seed `σ` is invariant
  at 0.137–0.150 across all four conditions, so each between-seed `σ` measures
  the trained model and not the scoring. Quadrature of the three gives ≈0.50
  against the observed 0.44 — **14% overshoot**, so the sources share variance
  through the weights.
- **§4.2 — the shape of the data lottery.** vary-data has a tight bulk and a
  long upper tail (skewness +0.74, IQR 0.30, whiskers −0.05/+0.47) against a
  symmetric vary-init (−0.24) and a broader right-skewed vary-noise (+0.62).
  Data-order variance is a few bad runs, not a continuous spread.
- **§4.2 — the control.** 24 retrains with init, data and training noise
  fixed; only DDP floating-point reduction order varies. EMA weights diverge
  **5–6% of norm** (33% on one run). `σ_between = 0.047` against a within-seed
  floor of 0.119 — the ratio inverts to **0.4×**. Different networks, same FID.
- **§4.3 — guidance.** GS-FID per cell: means span [7.31, 7.52] about 7.42,
  `σ_between = 0.050`, `σ_within = 0.027`, CoV **0.67%** against 1.26%
  unguided. The between/within ratio falls only 3.2× → **1.87×**. Recovered
  optima concentrate at `σ_ω ≈ 0.045`, so ±0.05 on the scale injects noise
  comparable to the within-seed floor. Spearman **ρ = 0.73** between guided
  and unguided rankings; 8/25 seeds move ≥5 places.
- **§4.4 — the floor.** CoV inside `[0.74%, 2.06%]` across all 76 cells,
  median **1.30%**. Mean FID halves from 200k to 2M while `σ_between` shrinks
  at most 2.4×. Non-monotonic in scale: S 0.74%, B 1.24%, XL 1.42%, L 1.72%.
  Spread is Gaussian, not heavy-tailed — `(max−min)/σ ∈ [3.1, 5.0]` against
  3.5–3.9 predicted for `n ∈ [19, 25]`.
- **§4.4 — rank instability.** Spearman ρ against the 2M ranking: 0.39–0.61 at
  200k, 0.65–0.81 at 1.1M.
- **§4.5 — compute.** Lucky-versus-unlucky convergence gap: 1.25× on S/B,
  1.82× on L, **2.0×** on XL, anchored to the unluckiest seed's 2M FID. Past
  ~1.5M steps the smallest single-seed improvement clearing `2σ` (0.5–0.8 FID)
  is indistinguishable from 200–500k extra steps.
- **§4.6 — µP.** Ten µP-coordinated LRs log-spaced over
  `[5×10⁻⁵, 5×10⁻⁴]`, four sizes, `N = 10` seeds, 100k steps, ≈400 networks.
  Under GS-FID the valleys are flat-bottomed near `2–3×10⁻⁴` with three
  adjacent LRs sharing the best FID inside the seed envelope — a **1.7×
  window** per size. Under *unguided* FID the curve is monotone, so the
  argmin sits at the right edge, `5×10⁻⁴`, which is also where **3/10 SiT-S
  and 1/10 SiT-XL seeds diverge**. And the CoV does *not* dip at the optimal
  LR: it is 1.7–2.3% there, inside the general floor.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Training-seed variance exceeds sampling-seed variance by ≈3.2× | strong | 25×10 panel, homoscedastic within-seed term, replicated across four sizes |
| C2 | The floor is 1–2% of mean FID and survives scale and compute | strong | 76 cells, four sizes, ten checkpoints |
| C3 | Flow-matching loss noise is the largest of three sources | moderate | one-at-a-time at one size; the sub-additivity the paper itself reports limits how far the attribution carries |
| C4 | Numerical non-determinism is not the cause | strong | the 24-retrain control, with the weight-divergence measurement that makes it a real test |
| C5 | A lucky seed is worth 1.25–2.0× compute | strong | min–max over ~20 seeds against a fixed target |
| C6 | µP transfers a 1.7× LR window rather than a point | moderate | one sweep, 100k steps — short — and only under GS-FID |
| C7 | The ~1.3% CoV generalizes | — | explicitly **not** claimed; the authors call it a calibration target for one combination |

## Method

An `N×K` panel per experiment. A training seed drives initialisation,
data-loader order and the per-step flow-matching noise; a sampling seed drives
the generation-time initial noise. Three nested statistics: `σ_within` across
the `K` sampling evaluations of one model averaged over `N`; `σ_between`
across the `N` per-seed means; `CoV = σ/µ` as the dimensionless comparator,
which is what makes guided (mean ≈7.4) and unguided (mean ≈34.7) panels
comparable at all. Single-source conditions fix two generators and vary the
third.

## Concepts

- **the generation lottery** — variance from resampling a fixed network. The
  one papers report.
- **the training lottery** — variance across identically-specified training
  runs. The one that dominates.
- **GS-FID** — FID at the per-cell golden-section-optimal CFG scale. About 14
  evaluations per cell; a more precise estimator that is not comparable to
  unguided numbers.
- **CoV** — `σ/µ`. The paper's insistence on this over absolute FID is load
  bearing: guidance drops the mean from 34.7 to 7.4, so absolute ranges
  overstate the improvement in reproducibility.

## Connections

The models are SiT ([LIT-447](../literature.d/LIT-447.md)), which the record holds, and the
paper measures that family rather than extending it — so no machine-readable
relation is declared. `extends` would claim it builds on SiT's contribution,
which it does not; it uses it as an instrument.

## Recommendations

- **R1** — report FID as an error bar over several training seeds, and treat
  gaps under ≈2% as inconclusive. *Filed* as `SOTA-tmpmd52k`.
- **R2** — tune and evaluate with the same FID variant you will report, and
  search the CFG scale per cell with golden section. *Filed inside R1's
  practice*, since it is a rider on the same protocol rather than a separate
  instruction.
- **R3** — read a µP-transferred learning rate as a window. *Filed* as a
  qualification on [SOTA-143](../practices.d/SOTA-143.md) rather than a new practice: µP transfer
  is that practice's claim, and this measures its resolution rather than
  replacing it.
- **R4** — do not select a training seed on an early checkpoint. *Not filed.*
  It follows from the rank-instability numbers, but nobody here is
  recommending seed selection in the first place, and a practice against a
  thing the record does not recommend is a straw man.

## Bearing on the record

**Qualifies [SOTA-143](../practices.d/SOTA-143.md).** That practice says to tune hyperparameters
on a narrow proxy under µP and transfer across width, and its Conditions
already note that production recipes treat the transferred values as a
starting point. This measures the size of that hedge on one family — a 1.7×
LR window — and adds a sharper failure: selecting the LR on *unguided*
single-seed FID lands at the edge of training stability, where 3 of 10 SiT-S
seeds diverge, with a confident-looking number attached. The practice goes to
v2 with this as a second source.

**Sits beside [SOTA-305](../practices.d/SOTA-305.md) without overlapping.** Reconstruction FID needs
its rate stated; generation FID needs its seed resampled. Independent findings
about the same metric family.

**Does not touch [THEORY-040](../theory.d/THEORY-040.md)**, which is about metrics that compose or
threshold per-token error turning smooth capability curves sharp. Different
mechanism — that one is about the metric's shape, this is about the training
run's variance — and conflating them would be easy and wrong.

## Limitations

- **One combination**, stated by the authors as a scope limit: SiT, flow
  matching, class-conditional ImageNet `256×256`, Inception-V3. The 1.3% is
  calibration, not a constant.
- **Recall behaves differently** from the fidelity metrics in the appendix
  replication. A protocol written from FID should not be assumed to cover
  diversity.
- **20–25 training seeds** is enough for a second moment and thin for
  anything about tails — though the paper checks Gaussianity and finds it.
- **The µP sweep is at 100k steps**, which is short, and the conclusion about
  windows may not survive to convergence.
- **The source attribution is one-at-a-time at one size**, and the paper's own
  sub-additivity result says that overestimates each source's marginal
  contribution.
- **Two claims rest on `N = 1`:** the 33% EMA-norm divergence is "one run", and
  the compute-gap anchors are min and max over ~20 seeds, which are the
  least stable order statistics in the panel.

## Open questions

- **Where is the floor for other families?** The obvious next measurement, and
  the paper hands over the protocol to run it. Latent versus pixel diffusion,
  text-to-image, and non-Fréchet metrics are all named and untested.
- **Does the 1.7× LR window survive to convergence?** Measured at 100k on a
  family the paper elsewhere trains to 2M.
- **Why does loss noise lead?** The decomposition establishes the ordering and
  offers no account of it. A mechanism would say which objectives inherit the
  problem — flow matching redraws `ε` every step, and an objective that does
  not might sit on a different floor entirely.
