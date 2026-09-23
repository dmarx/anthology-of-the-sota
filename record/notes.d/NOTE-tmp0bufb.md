---
status: Read
paper: LIT-tmpzy774
title: 'AlphaFold 3'
version: 1
date: '2026-09-23'
summary: >-
  AlphaFold generalized to all biomolecular complexes, with a diffusion
  head over atom coordinates. It gains on ligands, nucleic acids and
  antibodies, and inherits generative failure modes (hallucination,
  chirality) that it patches with distillation and ranking. Main text read.
  Extended Data and supplementary methods not read.
---

# NOTE-tmp0bufb: AlphaFold 3

## Contribution

One model for the joint structure of proteins, nucleic acids, small
molecules, ions and modifications, beating specialist tools in each
category tested.

## Key insight

**Generate atoms directly with diffusion, and drop the geometric
machinery.** Multi-scale denoising learns local stereochemistry at low
noise and global arrangement at high noise, without frames, torsions or
equivariant layers.

## Key results

- PoseBusters: beats Vina (P = 2.27×10⁻¹³), which gets the pocket, and
  RoseTTAFold All-Atom (P = 4.45×10⁻²⁵)
- Protein–nucleic acid complexes: better than RoseTTAFold2NA
- Antibody–antigen quality rises with the number of seeds ranked by ipTM
- Cross-distillation from AlphaFold-Multimer "greatly reduced"
  hallucination (in Extended Data, not read)

## Limitations

- **4.4% chirality violations**, and clashes in very large complexes
- **Static structures.** Seeds do not sample the solution ensemble
- **Hallucinated regions are low-confidence but not visibly disordered**
- **Restricted release**, and the key comparisons exist only as figures
