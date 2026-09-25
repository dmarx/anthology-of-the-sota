---
number: 353
status: Read
formerly:
- NOTE-tmp8dzmz
paper: LIT-696
title: 'Rarely categorical, highly separable representations along the cortical hierarchy'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Read in full (full text of the published Nature article (open access,
    PDF, 34 pp.), meaning the main text, the complete Methods (data
    inclusion, RRR encoding model, clustering pipelines, ePAIRS,
    α-diversity, representation dimensionality, pseudopopulation decoding,
    the independent-conditions algorithm, separability/AD, synthetic models,
    and the PR-of-Gaussian-clusters derivation, whose displayed equations
    were only partly recoverable from the text layer), every main and
    Extended Data figure legend (ED Figs 1–11), and the Discussion. Figs 3
    and 6 and ED Fig. 11 were also inspected as rendered images. The other
    figures were read through their legends and embedded panel text only.
    Supplementary file 2 (the 34-page Peer Review File: 3 referee reports
    over 2 rounds plus the rebuttals) was read in full. The Reporting
    Summary (MOESM1, 3 pp.) is image-only and was not read. The bioRxiv
    preprint (10.1101/2024.11.15.623878) was not read. Deferred note
    NOTE-353 (Skimmed) is the one this replaces.). Upgraded from `Skimmed`
    to `Read`: the claims table, assumptions and results are new, and the
    skim is corrected where the full text disagreed.
date: '2026-09-25'
summary: >-
  In 14,000+ IBL Neuropixels units (4,617 passing a ΔR² ≥ 0.015
  selectivity threshold), the clustering of 8-D encoding-model selectivity
  vectors beats a covariance-matched Gaussian null in only a handful of
  the ~20 testable cortical regions (VISp, AUDp, SSp-ul at Bonferroni p <
  0.05; clustering z falls with hierarchy position, ρ = −0.62). Pooled
  modules and the whole cortex do cluster (whole-cortex z = 8.0). Among
  the 16 regions with enough trials, once the 16 task conditions are
  merged into pairwise-decodable "independent" ones (M_IC from 5 to 16,
  rising with hierarchy, ρ = 0.77), ≥ 95% of random balanced dichotomies
  are linearly decodable above a shuffle null in every region except
  gustatory cortex (≈0.82).
---

<!-- inactive-ok-file: SOTA-342 — Proposed; named as tangential in Bearing on the record -->
<!-- inactive-ok-file: SOTA-344 — Proposed; named as tangential in Bearing on the record -->
<!-- inactive-ok-file: THEORY-034 — Proposed; this reading qualifies it — its half-space exists for almost any grouping -->
<!-- inactive-ok-file: THEORY-063 — Proposed; named as weakly consistent with this reading -->
<!-- inactive-ok-file: THEORY-090 — Proposed; this reading supports its caution about fitted probes -->

# NOTE-353: Rarely categorical, highly separable representations along the cortical hierarchy

## Contribution

The paper reports a systematic, brain-wide test of whether cortical neurons fall into functional types, using one task, one dataset and one pipeline for every region: the IBL Brainwide Map, with ~180 sessions. It adds three things:

- a categoricality test that compares k-means silhouette against a Gaussian null with the data's own mean and covariance (Fig. 3a);
- an algorithm that merges experimental conditions until every remaining pair is linearly decodable, giving the number of "independent conditions" M_IC (Fig. 2g–i, ED Fig. 3);
- a link, empirical and analytical, between response-profile structure (α-diversity, clustering) and the participation ratio and dichotomy separability of population geometry (Figs 4–6, ED Figs 8–9).

What it establishes is that, within most mouse cortical regions and in this task's variable space, selectivity is a continuous, elongated, roughly Gaussian cloud rather than a set of clusters. Regions differ mainly in *how many* conditions they distinguish (M_IC), not in whether what they distinguish is laid out in low dimension.

## Key insight

The rows (neurons in conditions space) and the columns (conditions in neural space) of one activity matrix share a spectrum. Clustering of neurons therefore caps the dimensionality of the condition geometry (in the small-cluster limit PR ≈ k < M), and diverse, unclustered selectivity permits high dimension. High dimension over the conditions a population actually distinguishes makes nearly every dichotomy of them linearly readable. The corollary is the paper's methodological warning: once conditions are pairwise distinguishable and the geometry is high-dimensional, *every* grouping of them is decodable above chance. Finding that some variable is linearly decodable therefore says little about whether the population represents that variable specifically (Discussion, separability paragraph).

## Assumptions

- **Selectivity is linear in 8 experimenter-chosen variables**: block prior, stimulus side, contrast, choice, outcome, wheel velocity, whisking motion energy and licks. It is fitted by a reduced-rank regression with d = 5 temporal bases shared across all neurons and variables, and summed over −0.2 to 0.8 s to give α ∈ ℝ⁸ per neuron. Inputs and outputs are z-scored per time step, so the coefficients are unit-free. The mean cross-validated R² is 0.16 against 0.09 for condition-PSTHs (Fig. 2b). Anything the 8 variables do not span is invisible to the clustering. Referee 3 made this point and the authors added it to the Limitations.
- **Neuron inclusion**: firing rate between 0.5 and 50 Hz, and ΔR²(RRR − trial-average) ≥ 0.015. The threshold matters. Including every neuron adds a "junk" peak at zero selectivity, which a single Gaussian null rejects and so inflates categoricality. Keeping too few neurons hollows the centre (Methods, "Criteria for neuron inclusion"). Robustness across thresholds is shown in ED Fig. 6b.
- **Categorical means** that the maximal-silhouette k-means partition (k = 3–20, 100 inits) beats 100 samples from 𝒩(μ̂, Σ̂) with the same N, at Bonferroni p < 0.05. Clusters are dropped when > 90% of their silhouette mass comes from one session. The authors concede this makes "non-categorical" a *narrow* class, and that elongated or continuous distributions without separated clusters also fail the null (Discussion).
- **Conditions for geometry**: 4 binarized variables (whisking above or below the session median per time bin, block, side, contrast ≤ 0.125 vs higher), giving M = 16 conditions. Choice and outcome were excluded because overtrained mice make too few errors in block-congruent trials. Whisking is labelled per 10 ms bin, so one trial can contribute vectors to both whisking conditions.
- **Pseudopopulations**: each region is resampled to N = 4,000 neurons and T = 100 patterns per condition, keeping simultaneously recorded neurons together. Sessions need ≥ 5 trials per condition. A linear SVM is used (Decodanda; training_fraction 0.8, 100 cross-validations).
- **Independent-conditions threshold** φ_min = 0.666 one-vs-one cross-validated accuracy. The rebuttal reports that 0.6 and 0.7 give highly correlated M_IC and the same correlation with the hierarchy (Reviewer Figs 8–9). That check is not in the published paper.
- **Hierarchy** is the anatomical ordering of Harris et al. (2019), derived from Allen connectivity. It is taken as given.
- The setting is mouse cortex, one overtrained two-alternative task, and trial-averaged or condition-averaged rates. None of it is a trained artificial network. Any transfer to ML is by analogy.

## Key results

- **Region identity is in single-neuron profiles.** Multiclass decoding of region from a neuron's time-varying profile reaches 0.233 accuracy against a 0.033 ± 0.003 null (time-summed: 0.123). For modules it is 0.422 against 0.203 ± 0.010. Selectivity similarity between regions correlates with anatomical connectivity (Spearman ρ = 0.40, P = 1.8 × 10⁻¹⁰), and pairwise region decodability anti-correlates with it (ρ = −0.49, P = 3.7 × 10⁻¹⁴) (Fig. 2d–f).
- **M_IC** runs from 5 (SSp-n) to 16 (MOs) and increases with hierarchy (ρ = 0.77, P = 0.0005) (Fig. 2i).
- **Within-region categoricality is rare.** VISp, AUDp and SSp-ul pass the Bonferroni threshold, with SSp-ll and GU near it. Silhouette z falls with hierarchy (ρ = −0.62, P = 0.004) (Fig. 3d). Absolute silhouettes are low even where they are significant: VISp's data value is ≈0.23 against a null of ≈0.14–0.18 (Fig. 3b). The trend survives a Leiden clusterer, time-resolved profiles and the choice of ΔR² threshold (ED Fig. 6b–d). The conditions-space and ePAIRS variants give VISp+AUDp and VISp+MOs respectively, and the conditions-space one shows no hierarchy correlation (ED Fig. 6f–i).
- **Pooling produces clusters.** The whole cortex gives z = 8.0 (P = 6 × 10⁻¹⁶). Somatomotor gives z = 8.56, medial 7.84, lateral 2.32 (P = 0.04), and prefrontal 0.54 (n.s.). Here the individually categorical regions were excluded and 100 best-encoded neurons were taken per area. Clusters partly align with area labels (z-scored Rand index) (Fig. 3e,f; ED Fig. 7).
- **α-diversity** is the participation ratio of the N × 8 α matrix, with N subsampled to 120. It tracks M_IC (ρ = 0.73, P = 0.0012) and anti-tracks α-space silhouette (ρ = −0.76, P = 0.0011) (Fig. 4d,e). Examples are SSp-n ≈ 4.0 and MOs ≈ 5.8.
- **Representation dimensionality** is the PR of the M_IC condition centroids. It rises with α-diversity (ρ = 0.67, P = 0.005) and with hierarchy (ρ = 0.79, P = 0.0003) (Fig. 5c,d). Absolute values are small, PR_IC ≈ 2–5.3; for example SSp-n has PR 2.8 and PR_IC 2.0, and MOs PR 5.3 and PR_IC 5.3 (Fig. 5b). Computed on single trials, PR ranges from 10 to 350 and correlates with the centroid PR (Spearman 0.86) (Methods).
- **Clustering caps dimension (analysis).** For k Gaussian clusters with within-cluster spread δ over M conditions, with N → ∞ and M finite, PR → min(k, M) as σ → 0, and PR falls with silhouette at fixed k and M (Methods; ED Fig. 9b). Across regions, conditions-space silhouette predicts lower PR (ρ = −0.77, P = 0.0004), and the formula predicts measured PR from (k, δ, M_IC) (ED Fig. 9c–e).
- **Separability over all 16 conditions** rises with α-diversity (ρ = 0.69, P = 0.003). SSp-n has sep 0.80 and MOs 0.99 (Fig. 6b,c).
- **Separability over independent conditions** is ≥ 0.95 in 15 of 16 regions, GU ≈ 0.82, and uncorrelated with α-diversity (ρ = 0.27, n.s.). AD over independent conditions is likewise uncorrelated (ρ = −0.10, n.s.) (Fig. 6d; ED Fig. 11c,e).
- **Synthetic results**: separability saturates once the latent dimension L ≳ M/2 (P = 16, N = 100, T = 20) (ED Fig. 8g). Stretching one axis lowers PR but leaves separability intact (ED Fig. 8h,i). So separability detects near-degenerate (sub-M/2-dimensional) geometry, not anisotropy.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Within most individual cortical regions, single-neuron selectivity (in the 8-variable RRR space) is not more clustered than a covariance-matched Gaussian; only VISp, AUDp, SSp-ul pass | strong (for this task/variable space) | Fig. 3d, ED Fig. 4; replicated across clusterer, ΔR² threshold, time-resolved profiles (ED Fig. 6b–d) |
| C2 | Clustering quality decreases along the cortical hierarchy | moderate | ρ = −0.62 in α-space (Fig. 3d); **not** reproduced in conditions space (ED Fig. 6f), and ePAIRS flags MOs (ED Fig. 6g); ~20 regions |
| C3 | At mesoscale and whole-cortex scale selectivity is categorical and aligns with anatomy | moderate | Fig. 3e,f, ED Fig. 7. Pooling regions with different mean profiles into a test against one Gaussian makes rejection close to expected, and the paper does not separate "clusters" from "mixture of region means" |
| C4 | A neuron's region can be decoded from its selectivity profile above chance, and functional similarity tracks anatomical connectivity | strong | Fig. 2d–f, shuffle nulls, P ≤ 10⁻¹⁰ |
| C5 | The number of independent conditions a region encodes increases along the hierarchy | moderate | ρ = 0.77 over 16 regions (Fig. 2i); threshold robustness only in the rebuttal |
| C6 | Response diversity (α-diversity) predicts representation dimensionality and all-condition separability | moderate | Spearman ρ 0.67 and 0.69 over 16 regions (Figs 5c, 6c); synthetic support (ED Fig. 8e) |
| C7 | Clustered response profiles bound the PR of the condition geometry, quantitatively | strong (theory) / moderate (fit) | derivation in Methods (large-N, Gaussian-cluster model); ED Fig. 9d,e fit |
| C8 | "All cortical regions exhibit maximal separability" once only independent conditions are counted (abstract) | weak-to-moderate as worded | 15 of 16 analysed regions ≥ 0.95, GU ≈ 0.82. "Separable" means above the 99th percentile of a shuffle null (≈0.53–0.55) on a 4,000-neuron resampled pseudopopulation. Conditions were pre-merged until pairwise decodable at ≥ 0.666, which removes the main route to failure (Fig. 6d, ED Fig. 11e). The abstract's "all" overstates the body |
| C9 | When conditions are pairwise separable, every dichotomy is decodable, so decodability of a single variable often lacks significance | moderate | empirical generalisation from C8, not proven. The paper's own counterexample (collinear centroids, Fig. 6a middle) shows it can fail; it simply did not in these data |
| C10 | Cortex "prioritizes diversity over categorical structure", favouring a high-dimensional, separable regime | weak (interpretive) | an inference from C1 + C8; one overtrained task; the authors list alternatives (Discussion, limitations) |

## Method

1. **RRR encoding model.** For neuron n, ŷ_n(k,t) = Σ_v β_n^v(t) x_v(k,t), with β_n^v(t) = Σ_{i=1..d} U_n^{v,i} V_i(t). The temporal bases V are shared across all neurons and variables, and d = 5 and the ridge λ are chosen by 3-fold CV. The fit uses L-BFGS on a ridge-penalised MSE. The selectivity profile is α_n^v = Σ_t β_n^v(t).
2. **Categoricality.** k-means on α (k = 3–20), pick the k with maximal silhouette, drop session-dominated clusters, then take the z-score of the silhouette against 100 draws from a Gaussian fitted to the data. The conditions-space variant z-scores the 16 condition rates, applies PCA to 90% variance, and uses a log-normal null fitted in the original space. ePAIRS uses the median nearest-neighbour cosine angle against 5,000 null draws.
3. **Independent conditions.** Compute the M × M one-vs-one cross-validated SVM accuracy matrix and threshold it at 0.666 into a "dependent" graph. Bron–Kerbosch finds the largest clique of mutually non-decodable conditions, which is merged into one condition. The matrix is recomputed and the steps repeat until all pairs are decodable. M_IC is the final count.
4. **Separability and AD.** Draw 200 random balanced dichotomies of the M or M_IC conditions, keeping individual conditions balanced within each side. Train a cross-validated linear SVM on the N = 4,000, T = 100 pseudopopulation. Separability is the fraction of dichotomies above the 99th percentile of 200 label-shuffled runs; AD is the mean accuracy. How a balanced split is formed when M_IC is odd (SSp-n has M_IC = 5) is not stated. For small M_IC only a few distinct balanced dichotomies exist (10 for M = 6), so 200 draws repeat them.

## Concepts

- **Categorical representation**: neurons form clusters in response-profile (conditions or selectivity) space, per Raposo et al. (2014) and Hirokawa et al. (2019). Tested here against a single Gaussian with matched covariance. It is *not* Freedman-style "categorical" (neurons selective for stimulus categories), which the paper explicitly separates. A strongly category-selective neuron may simply sit on the tail of a Gaussian.
- **Uneven selectivity**: some variables or conditions are encoded much more strongly than others, so the response cloud is elongated. This is the dominant structure in most regions.
- **Explicit vs implicit modularity**: explicit means segregated populations, which form clusters in selectivity space. Implicit means the same activity-space geometry rotated, with no clusters in selectivity space. The two have the same computational properties (Discussion).
- **α-diversity**: the participation ratio of the neurons × variables coefficient matrix.
- **Representation dimensionality**: PR = (Σλ)²/Σλ² of the condition-centroid covariance (embedding dimensionality, not intrinsic).
- **Independent conditions (M_IC)**: the number of condition groups left after merging mutually non-decodable ones.
- **Separability**: the fraction of balanced dichotomies decodable above a shuffle null. It was called "shattering dimensionality" in the submitted version and renamed after review. **AD (average decodability)** is the mean accuracy over dichotomies, which is what Bernardi et al. (2020) called shattering dimensionality.

## Connections

The paper builds on the mixed-selectivity and high-dimensionality programme of Rigotti et al. (2013) and Fusi, Miller & Rigotti (2016), and on the Bernardi et al. (2020) geometry-of-abstraction measures. It takes the "categorical vs category-free" question and the PAIRS/ePAIRS tests from Raposo et al. (2014) and Hirokawa et al. (2019), and its conclusions run against Hirokawa's orbitofrontal categoricality. One referee calls it a correction of Hirokawa; the paper itself frames it more mildly. It is consistent with Khosla et al. (2026) on privileged axes at the mesoscale but not locally, and with Dahmen et al. on dimensionality rising up the visual hierarchy. Cover (1965) is invoked for separability, but the measure here is cross-validated rather than in-sample. The ANN literature enters only in the Discussion, which cites RNN modularity work (Yang et al. 2019; Dubreuil et al. 2022; Driscoll et al. 2024; Johnston & Fusi 2024): simple tasks need no clusters and complex multi-task training produces them.

## Bearing on the record

The paper is neuroscience, but its measurements are the ones `concept-geometry` makes on networks: linear readout of arbitrary groupings, clustering of units in response space, and dimensionality of condition geometry. What it implies for ML claims:

1. **A successful linear probe is weak evidence that a concept is specifically represented.** In a high-dimensional code whose inputs are pairwise distinguishable, almost *every* balanced relabelling of those inputs is linearly decodable above chance. Here that was 15 of 16 regions at ≥ 95% of random dichotomies, with activations far lower-dimensional than a transformer residual stream. The ML consequence is that probe accuracy should be reported against a random-dichotomy baseline over the same inputs (the distribution of accuracies for arbitrary groupings, as in ED Fig. 11), not only against a label-shuffle null. A shuffle null tests "is there signal", not "is this concept privileged". AD (mean accuracy over random dichotomies) is a ready-made reference level. The record has no practice saying this. It is a candidate `SOTA` under `concept-geometry` / `analysis-and-evaluation`, and it would need an ML source that runs the control on a network, since this paper does not.
2. **Linear separability is not categorical structure, and neither follows from the other.** Maximal separability coexisted with *no* clustering in most regions. The paper's own simulations (ED Fig. 8h,i) show separability is blind to anisotropy and only detects near-collapse below ~M/2 dimensions. Observing that concepts are linearly separable in a model therefore says nothing about whether units or features form discrete types, and a clustering claim needs a covariance-matched null, not a visual of sorted units. Sorted selectivity matrices "are often misleading because structured patterns appear whenever a few variables are more strongly encoded" (Results, Fig. 3 discussion).
3. **Mixed selectivity vs superposition and monosemanticity.** This is the biological analogue of polysemantic units, and the result is that non-sensory populations look like a rotated Gaussian continuum rather than a set of unit types. The paper's own distinction between explicit and implicit modularity is the basis problem that sparse dictionaries attack: implicit (rotated) modularity is invisible to unit-level clustering. The Gaussian-null silhouette test is a usable check on whether a network's units, or an SAE's latents, form functional types. The paper does not apply it to any ANN.

Record documents it bears on:

- **[THEORY-090](../theory.d/THEORY-090.md)** (probe = steering vector = pair direction; `Proposed`) — **supports its caution, qualifies its "measurement" sense.** [THEORY-090](../theory.d/THEORY-090.md) distinguishes subspace, measurement and intervention senses of linearity, and already notes that a fitted probe absorbs off-target concepts. This paper supplies the reason the measurement sense is the weakest of the three: in a high-dimensional code, a probe exists for nearly any grouping. It does not contradict [THEORY-090](../theory.d/THEORY-090.md), whose central objects are counterfactual pair directions, not probe success.
- **[THEORY-034](../theory.d/THEORY-034.md)** (concepts as intersections of half-spaces; `Proposed`) — **qualifies, and sharpens its own "What this does not say".** If near-arbitrary dichotomies are linearly separable, then a thresholded half-space exists for almost any grouping. Its existence is therefore not evidence that the model represents *that* concept or lattice. [THEORY-034](../theory.d/THEORY-034.md) names as its "severe test" the step of clustering the model's own representations to look for structure nobody put there. That is exactly this paper's method, which in cortex mostly finds *no* clusters beyond a Gaussian null. The cheap test is a fair one, and it can come back negative.
- **[SOTA-345](../practices.d/SOTA-345.md)** (probe with logistic regression on raw activations; `Active`) — **consistent, qualifies interpretation only.** [SOTA-345](../practices.d/SOTA-345.md) is about which probe to use, and this paper does not touch that. It adds that the resulting AUC needs a random-dichotomy reference before it is read as evidence of a represented concept.
- **[SOTA-342](../practices.d/SOTA-342.md) / [SOTA-344](../practices.d/SOTA-344.md)** (SAE evaluation and training; `Proposed`), via [LIT-571](../literature.d/LIT-571.md) — **tangential.** The categorical-vs-mixed test is a candidate way to ask whether SAE latents form discrete functional types. Nothing here bears on SAE training practice.
- **[THEORY-063](../theory.d/THEORY-063.md)** (concept directions in the low-variance tail; `Proposed`) — **weakly consistent.** ED Fig. 8h,i shows that low-variance (unstretched) directions keep full separability, so readability of quiet directions is expected. That is no evidence for [THEORY-063](../theory.d/THEORY-063.md)'s specific placement claim.
- **[LIT-696](../literature.d/LIT-696.md)** is this paper, currently `Deferred`, with **NOTE-353** (`Skimmed`) the reading this replaces. The note's tag `concept-geometry` is justified. `analysis-and-evaluation` would also be justifiable given point 1.

No `SOTA` practice currently cites this paper, so there is no mis-citation to report.

## Limitations

- **One overtrained task, 8 variables, 4 binarized for geometry.** "Rarely categorical" means no discrete types *within the IBL-variable space*. The authors agree and cite RNN work where complex tasks do produce clusters. Choice and outcome are absent from the geometry analysis.
- **Coverage.** Clustering covers ~20 regions and geometry 16, although the dataset has 43. The abstract's "all cortical regions exhibit maximal separability" overstates a 15-of-16 result.
- **Separability is lenient and scale-dependent.** It counts dichotomies above the 99th percentile of a shuffle null (≈0.53–0.55 accuracy) on 4,000 resampled pseudo-neurons with T = 100. Mean accuracies over independent conditions are ~0.65–0.90 (ED Fig. 11e). The rebuttal shows the value depends on T/N before converging, and only one region (VISp) was tested for this. Referee 1 asked whether small but consistent off-subspace "jiggle" of true centroids makes everything separable. Cross-validation, the authors' answer, addresses trial noise but not small real signal dimensions.
- **Near-circularity of C8.** M_IC is built by merging conditions until every pair is decodable at ≥ 0.666. Separability over those conditions then fails only for near-degenerate geometry. The authors argue the result is non-trivial because collinear geometries would fail (Fig. 6a). That is true in principle, but the test's power against realistic, merely anisotropic geometry is low by the paper's own ED Fig. 8i.
- **Mesoscale "categorical" is expected from the null.** Pooling regions with different mean profiles, tested against a single Gaussian, rejects the null because the pool is a mixture. The Rand-index alignment shows the clusters partly *are* the regions. Whether there is within-module categorical structure beyond region means is not separated.
- **Pipeline disagreement.** The hierarchy trend in categoricality appears only in the α-space pipeline. The conditions-space version shows no trend, and ePAIRS flags MOs.
- **Low absolute silhouettes** (≈0.2 even in VISp): "categorical" regions are statistically, not visibly, clustered.
- **Correlations over ~16–20 regions** with overlapping neuron pools, and bootstrapped CIs on regression lines. There are no mixed-effects models across sessions or animals.
- **Not tested in any artificial network.** Every ML implication above is by analogy.

## Open questions

- Does "rarely categorical" survive a multi-task or less-trained dataset? The authors predict more clustering with task complexity, from RNN results. A multi-task brain-wide recording analysed with the same pipeline would settle it.
- How sensitive is independent-condition separability to its operating point? The questions are whether it stays at ~1 when the "separable" criterion is raised (for example to Rigotti's 85% in the large-N limit, or to AD relative to a random-dichotomy baseline), and when N is the real rather than resampled neuron count.
- Is there categorical structure within modules beyond region means? This could be tested by pooling after subtracting per-region mean profiles, or against a per-region Gaussian-mixture null.
- For ML: in trained networks, do non-input layers pass the Gaussian-null categoricality test in the unit basis, in an SAE basis, or in neither? Is linear-probe accuracy for named concepts distinguishable from the distribution of accuracies for random dichotomies of the same inputs? The second is the control this paper implies, and no record document yet reports it.

## Corrections to the seeded skim

- "14,000+ units across 43 regions" describes the dataset, not the analyses. The within-region analyses use 4,617 neurons that pass ΔR² ≥ 0.015. Clustering covers the ~20 regions with ≥ 50 such neurons (Fig. 3d). The geometry, dimensionality and separability analyses cover 16 regions (Figs 5–6, ED Fig. 11e). "Every area is maximally separable" therefore means 16 areas, and one of them (GU, ≈0.82) is not.
- "Maximally separable" means ≥ 0.95 of 200 random balanced dichotomies scoring above the 99th percentile of a label-shuffled null. That threshold sits near 0.53–0.55 accuracy in ED Fig. 11e. Mean independent-condition decoding accuracy (AD) runs from ~0.65 (GU) to ~0.90 (SSp-n). So this is above-chance separability, not high-accuracy separability. It is measured on a resampled pseudopopulation of N = 4,000 with T = 100 pseudo-trials per condition, and the rebuttal's Reviewer Fig. 5 shows that separability rises with T/N before converging.
- The skim's "only a few primary sensory areas cluster" holds for the main RRR/α-space pipeline only. The two robustness pipelines disagree in detail. Conditions-space clustering flags VISp and AUDp and shows no correlation with the hierarchy (ED Fig. 6f). ePAIRS flags VISp and **MOs**, a high-hierarchy area (ED Fig. 6g). The hierarchy trend in categoricality is therefore not reproduced by the conditions-space test.
- "Categorical organization at whole-cortex scale" comes from a single-Gaussian null applied to pooled regions whose means differ (Fig. 2c). That pooled sample is a mixture, so rejecting the null is close to expected. The paper does not frame it that way (see Limitations).
- The skim cites a Discussion section called "Measures of separability". In the published version the warning is in the separability paragraphs of the Discussion, with no such heading.
- Minor points. The published SSp-n M_IC is 5, while the rebuttal text says 6. The article title in Crossref and the final version is "Rarely categorical, highly separable representations along the cortical hierarchy". The earlier title ("Rarely categorical and highly separable: how neural representations change along the cortical hierarchy") belongs to the preprint and the revision.
