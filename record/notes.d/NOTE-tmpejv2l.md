---
status: Read
paper: LIT-tmppdats
title: 'StyleGAN2'
version: 1
date: '2026-09-23'
summary: >-
  Diagnoses two StyleGAN artifacts and fixes each at its cause: weight
  demodulation instead of instance normalization, and a fixed
  skip/residual architecture instead of progressive growing. Adds lazy
  regularization and path-length regularization. Read §1–4.1 and Tables 1–2;
  §4.2 onward and the appendices were skimmed.
---

<!-- inactive-ok-file: SOTA-tmpld8su SOTA-tmpb0fn3 — both Proposed, filed in this same contribution from this paper -->

# NOTE-tmpejv2l: StyleGAN2

## Contribution

Two artifact diagnoses, each tied to a mechanism, and a fix for each that
keeps the good behaviour the flawed part was there for. Instance
normalization kept style mixing working, and demodulation does too.
Progressive growing kept high-resolution training stable, and the
skip/residual architecture does too.

## Key insight

**A network routes around a constraint in the cheapest visible way.** A
generator that cannot pass feature magnitudes through instance
normalization creates a spike that dominates the statistics, which is the
droplet. A generator whose every resolution was once the output learns
output-level frequencies everywhere, which is the phase artifact.
Removing the constraint removes the artifact. Penalizing the artifact
would not.

## Assumptions

- **FFHQ 1024² (25M images seen) and LSUN Car 512×384 (57M)**
- **One training run per configuration**, snapshot chosen by lowest FID,
  metrics averaged over 10 evaluation seeds
- **Style mixing is required.** The demodulation design keeps it

## Key results

- **Table 1, FFHQ:** FID 4.40 → 4.39 (demod) → 4.38 (lazy R1) → 4.34 (PPL
  reg) → 3.31 (no growing) → 2.84 (larger). PPL 212 → 123 through PPL reg
- **Table 1, LSUN Car:** PPL regularization worsens FID (2.83 → 3.43)
- **Table 2:** on FFHQ, output-skip G with residual D gives FID 3.31 against
  4.32 for the original pair. On LSUN Car, residual G and D is best (2.66)
- **Spectral normalization** added to or replacing these changes "invariably
  compromises FID" (Appendix E, not read)

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Droplets are caused by instance normalization | strong | removing normalization removes them; demodulation removes them at equal FID |
| C2 | Progressive growing causes phase artifacts | moderate | mechanism argued, artifact shown, removed by the fixed architecture |
| C3 | A fixed skip/residual architecture beats progressive growing | moderate | Table 1 row E, Table 2; single runs |
| C4 | Regularizers can run every 16 steps without loss | moderate | one row, R1 only |
| C5 | Low PPL tracks perceived quality | weak | correlation on per-image PPL, and the authors' visual judgment |

## Method

Demodulation: `w'_ijk = s_i · w_ijk` (modulate), then
`w''_ijk = w'_ijk / √(Σ_{i,k} w'_ijk² + ε)` (demodulate), implemented with
grouped convolutions. Path-length regularizer:
`E_{w,y}(‖J_wᵀ y‖₂ − a)²`, with `a` an EMA of the lengths.

## Connections

It fixes StyleGAN ([LIT-tmppzrje](../literature.d/LIT-tmppzrje.md)), which inherits progressive growing from
Progressive GAN (not in the record). StyleGAN3 ([LIT-tmp8n96l](../literature.d/LIT-tmp8n96l.md)) takes the
phase-artifact diagnosis further, into aliasing throughout the generator.

## Recommendations

- **R1** — No progressive growing: output-skip G, residual D. Filed as
  [SOTA-tmpld8su](../practices.d/SOTA-tmpld8su.md)
- **R2** — Demodulate weights instead of instance normalization in
  style-modulated layers. Filed as [SOTA-tmpb0fn3](../practices.d/SOTA-tmpb0fn3.md)
- **R3** — Compute expensive regularizers lazily, every k steps. Not filed:
  one configuration, one regularizer

## Bearing on the record

- **[SOTA-tmpld8su](../practices.d/SOTA-tmpld8su.md)** and **[SOTA-tmpb0fn3](../practices.d/SOTA-tmpb0fn3.md)** are new
- The ViT-VQGAN note ([LIT-500](../literature.d/LIT-500.md)) records a StyleGAN discriminator beating
  PatchGAN in its own ablation. That is a different comparison

## Limitations

- **Single runs per configuration**
- **Two datasets**, and FFHQ is highly aligned
- **Path-length regularization's value rests on PPL**, a metric the same
  group introduced

## Open questions

- Whether the fixed-topology result holds for GAN families without style
  modulation
