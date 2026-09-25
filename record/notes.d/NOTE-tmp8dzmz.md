---
status: Skimmed
paper: LIT-tmph7ql9
title: 'Rarely categorical, highly separable representations along the cortical hierarchy'
version: 1
date: '2026-09-25'
summary: >-
  Within individual cortical areas neurons rarely form categorical (clustered) selectivity classes, only primary sensory areas do, but their response diversity yields high-dimensional population geometry, so every area is maximally linearly separable once only independently encoded conditions are counted; categorical organization appears only at whole-cortex scale, tracking anatomical connectivity.
---

<!-- inactive-ok-file: LIT-tmph7ql9 — Deferred: this is the seeded skim of the paper, filed with it on 2026-09-25 -->

# NOTE-tmp8dzmz: Rarely categorical, highly separable representations along the cortical hierarchy

## Contribution

The authors revisit whether cortical neurons fall into functionally distinct, categorically organized populations, using 14,000+ units across 43 cortical regions from the International Brain Laboratory Brainwide Map during a complex decision task. They find the answer depends on scale: across the whole cortex, selectivity is categorical and aligned with anatomical connectivity, but within single regions categorical structure is rare, confined to primary sensory areas, and responses are highly diverse. Theory and data together show this diversity produces high-dimensional representations and hence high linear separability of experimental conditions. Accounting for what each area actually encodes, all regions reach maximal separability, suggesting cortex favours diversity over categorical structure.

## Skim

*Abstract, figures and selected sections, read when the work was seeded. Not enough to state its assumptions or results exactly; a `Read` note replaces this one.*

- Framing: a neurons-by-conditions matrix defines a "conditions space" (neurons' selectivity profiles) and a "neural space" (population geometry); the paper links structure in the first to function in the second (Main, Fig. 1a).
- Per-neuron selectivity is estimated with a reduced-rank regression (RRR) encoding model over task, sensory and movement variables, giving an eight-dimensional time-summed selectivity vector per neuron (Response profiles section; Methods, "RRR encoding model").
- Region-average selectivity profiles are distinct enough to guess a neuron's region above chance, and region-region similarity correlates with anatomical connectivity (Fig. 2c,d).
- Categoricality is tested with k-means silhouette scores against a multivariate-Gaussian null; only a few primary sensory areas (VISp, AUDp, SSp-ul are the ones excluded as individually categorical) cluster, while pooled mesoscale modules do cluster (Figs. 3, "Mesoscale clustering").
- Introduces alpha-diversity (participation ratio of regression coefficients), shows it correlates with representation dimensionality (PR over independent conditions), which in turn predicts separability = fraction of balanced dichotomies linearly decodable above a shuffle null; clustering decreases and dimensionality increases up the hierarchy (Figs. 4-6; Discussion).
- Methodological warning: when only independent conditions are considered, all dichotomies are decodable, so decodability of any single variable is weak evidence that it is specifically encoded (Discussion, "Measures of separability").

## Open questions

- "Non-categorical" is defined narrowly (silhouette not different from a Gaussian null); the Discussion concedes elongated, non-isotropic distributions count as non-categorical, so check how much the headline depends on that definition and on k-means/silhouette choices.
- The "maximal separability" result depends on the authors' procedure for finding independent conditions; that step (Methods, "Finding the independent conditions") is what to verify.
- ML link (by analogy, not claimed by the paper beyond Cover's theorem): mixed/diverse selectivity giving high-dimensional, linearly separable codes parallels discussions of polysemantic units, random-feature expansions and linear probing in neural networks; the decoding caveat applies directly to probing studies of learned representations.
- Very recent (July 2026); citation count and replication are minimal so far.
