---
status: Active
title: 'Accurate structure prediction of biomolecular interactions with AlphaFold 3'
version: 1
tags:
- biomolecular-modeling
- generative-modeling
- model-architecture
date: '2026-09-23'
published: '2024-05-08'
doi: '10.1038/s41586-024-07487-w'
first_author: 'Abramson'
keywords:
- 'alphafold'
- 'diffusion'
- 'protein-ligand'
- 'biomolecular-complexes'
- 'cross-distillation'
implementations:
- AlphaFold 3
extends:
- LIT-tmpmz8pl
summary: >-
  Abramson et al. (Nature 2024), DOI 10.1038/s41586-024-07487-w. AlphaFold 3
  predicts complexes of proteins, nucleic acids, ligands, ions and modified
  residues. A pairformer with lighter MSA processing replaces the Evoformer,
  and a diffusion module over raw atom coordinates replaces the structure
  module, with no built-in rotational equivariance. It beats Vina on
  PoseBusters without the pocket information Vina gets (P = 2.27×10⁻¹³). The
  generative head hallucinates structure in disordered regions, which
  cross-distillation from AlphaFold-Multimer reduces. Chirality is violated
  in 4.4% of PoseBusters predictions even after ranking penalties.
---

# LIT-tmpzy774: Accurate structure prediction of biomolecular interactions with AlphaFold 3

Abramson, Adler, Dunger, Evans, Green, Pritzel, Ronneberger, Willmore et
al., Google DeepMind and Isomorphic Labs (Nature 630, 2024) — DOI
10.1038/s41586-024-07487-w

## Key takeaways

- **Architecture:** a pairformer (48 blocks) with reduced MSA processing
  replaces the Evoformer. A diffusion module predicts raw atom coordinates,
  replacing AF2's frames and torsions. Neither needs invariance or
  equivariance to global rotations, which "simplif[ies] the machine
  learning architecture"
- **Results** (Figure 1c): on PoseBusters (428 protein–ligand complexes,
  run with a model trained to a 2019 cutoff), it beats AutoDock Vina
  (P = 2.27×10⁻¹³), although Vina is given the solved pocket and AF3 is not.
  It beats RoseTTAFold All-Atom (P = 4.45×10⁻²⁵). It is also better than
  RoseTTAFold2NA on protein–nucleic acid complexes under 1,000 residues,
  and than AlphaFold-Multimer v2.3 on protein–protein and antibody
  interfaces. The success rates are plotted, not stated in the text
- **Hallucination:** a generative model invents plausible structure in
  disordered regions. Training data enriched with AlphaFold-Multimer
  predictions, where disorder appears as extended loops, "greatly reduced"
  this (Extended Data Figure 1, not read)
- **Confidence under diffusion:** training runs a cheap "mini-rollout" of
  the sampler to get a full structure, so the confidence head can be
  trained against that structure's true error
- **Sampling:** five seeds × five diffusion samples, ranked by predicted
  confidence with chirality and clash penalties. For antibody interfaces,
  quality keeps rising with more seeds, up to 1,000 (Figure 5a)
- **Limits:** 4.4% chirality violations on PoseBusters, clashes in very
  large protein–nucleic complexes, hallucination that is low-confidence
  but not ribbon-like, and one static conformation. For example it always
  predicts cereblon closed, as bound, even when no ligand is given (apo)

## Standing in the anthology

**Filed from `#163`** ("AlphaFold"). It `extends` AlphaFold 2 ([LIT-tmpmz8pl](LIT-tmpmz8pl.md)).
It sources [SOTA-tmp3m2p6](../practices.d/SOTA-tmp3m2p6.md) (cross-distillation against hallucination) and is
a second source for [SOTA-tmpej1tr](../practices.d/SOTA-tmpej1tr.md) (confidence-ranked sampling).

**On the headline comparisons.** The PoseBusters comparison is fairer to
the baseline than to AF3, since Vina gets the pocket. The success
percentages are only in figures, so none are quoted here. The code and
weights were released under restricted terms, which limits independent
checks.

Read — [NOTE-tmp0bufb](../notes.d/NOTE-tmp0bufb.md).
<!-- inactive-ok-file: SOTA-tmp3m2p6, SOTA-tmpej1tr — Proposed, filed in this same contribution with this paper as a source -->
