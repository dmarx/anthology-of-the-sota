---
status: Read
paper: LIT-tmplifgh
title: 'Sparse Autoencoders Trained on the Same Data Learn Different Features'
version: 1
date: '2026-11-26'
summary: >-
  SAEs differing only in initialization seed share 42% of latents at 32K on
  Pythia 160M and 30% at 131K on Llama 3 8B, by Hungarian matching with a
  0.7 cosine threshold. Overlap falls with width and k, rises with training
  length, and is higher for L1-ReLU than TopK. Read in full at arXiv v2,
  appendix captions included. The figures could not be inspected.
---

<!-- inactive-ok-file: SOTA-tmprih86, SOTA-344 — Proposed, named in Bearing on the record as the practice this reading files and the one it adds a condition to -->

# NOTE-tmpf455e: Sparse Autoencoders Trained on the Same Data Learn Different Features

Read in full from arXiv v2 (29 January 2025): all eight sections and the
captions of Figures A1–A3. The plots themselves did not render in the HTML
used, so numbers that appear only in figures are not recorded here. The ICLR
2026 version on OpenReview (`EjInprGpk9`) refused automated access. It may
differ from v2, and this reading does not cover it.

## Contribution

A measurement of how much of an SAE's dictionary depends on the random
seed alone, with data and data order fixed. Before it, ReLU SAEs had been
reported stable across seeds (over 90% on GPT-2). This paper shows that for
TopK SAEs at larger widths, most latents do not recur. It also gives a
matching procedure and a definition of "shared" that others can reuse.

## Key insight

**An SAE's dictionary is one local optimum, not the model's feature set.**
Change only the initialization and a majority of latents can change, many
of the new ones interpretable. A claim that rests on a particular latent is
a claim about one training run until that latent is found in another.

## Assumptions

- Only the initialization seed varies. Data and data order are identical,
  so this measures initialization sensitivity, not data sensitivity
- *Shared* is defined by a 0.7 cosine threshold on both encoder and
  decoder matchings. Figure A1 shows the shared fraction as the threshold
  moves, and the choice rests on the bimodal distribution, not a derivation
- Unless stated otherwise: SAEs with 2¹⁵ latents on the output of
  Pythia 160M's layer-6 MLP, trained on the first 8B tokens of the Pile with
  EleutherAI's `sae` library. That these are TopK is implied by the k
  sweep on this configuration (Figure 4), not stated

## Key results

- **42%** of latents shared between two seeds at 2¹⁵ latents on Pythia 160M
  (§3). **30%** at 131K latents on a Llama 3 8B MLP (abstract, §1)
- With **nine seeds**, about **35%** of a base SAE's latents are orphans
  against all eight others. A power law with an offset fits the decline
  better than one without (§4, Figure 2)
- Shared latents fire more often. Never-shared latents are the rarest, yet
  many orphans fire more often than latents shared with all seeds (§4,
  Figure 3)
- Detection scores for two 32K seeds average **0.72**, interquartile range
  0.62–0.8. Latents shared by more seeds score higher. A substantial
  fraction of single-seed latents also score high (§5, Figure 6, Table 1)
- Overlap **decreases** with more latents and with larger k, and
  **increases** with training tokens (§6, Figure 4). It is lowest in the
  early and last layers (Figure 5)
- L1-trained ReLU and Gated SAEs overlap more than TopK on GPT-2 (§6,
  Figure 5)

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Same-data SAEs differing only in seed share well under half their latents at 32K+ widths, for TopK | strong | §3–4: two models directly, nine seeds on Pythia, three LLMs per abstract |
| C2 | A floor of seed-specific latents persists as seeds are added | moderate | §4: offset power law fitted to nine seeds on one configuration |
| C3 | Many seed-specific latents are interpretable, so one run misses real features | moderate | §5: detection scoring on two seeds of one SAE. The score measures an explanation's predictiveness, not causal relevance |
| C4 | TopK is less seed-stable than L1-ReLU even at matched sparsity | weak | abstract. The body shows one GPT-2 architecture panel and does not describe the sparsity control |
| C5 | Instability grows with width and k and shrinks with training length | moderate | §6, Figure 4: single-factor sweeps on Pythia 160M |
| C6 | SAEs diverge rather than converge with scale | weak | §7: rests on width and on Llama, which varies model and width together. Training length points the other way |
| C7 | The seed dependence is not mainly feature absorption | weak | §6: inferred from the direction of the k and training-length trends. The authors say the absorption metric may not suit MLP SAEs |
| C8 | Gemma Scope's positive cross-layer matching likely depends on all its SAEs sharing a seed | weak | §2: personal communication about the seed, and the inference is untested |

## Concepts

- **Shared latent** — same partner under the encoder and the decoder
  Hungarian matchings, with cosine similarity of at least 0.7 in both
- **Orphan latent** — any latent that is not shared, i.e. matched to an
  unrelated counterpart
- **Alignment score** — mean cosine similarity of matched pairs

## Connections

The matching is the permutation alignment of Git Re-Basin ([LIT-333](../literature.d/LIT-333.md))
applied to dictionary latents. The architectures compared are TopK from Gao
et al. ([LIT-571](../literature.d/LIT-571.md)), L1-ReLU, and Gated SAEs. It answers prior reports of
over 90% stability (Braun et al., 2024, and an anonymous ICLR 2025
submission) by showing those used smaller ReLU SAEs. It is the work the
survey [LIT-tmpilnw1](../literature.d/LIT-tmpilnw1.md) cites in §6.5.4.

## Recommendations

- **R1** — Before resting a claim on a specific SAE latent, train at least
  one more seed and check that the latent recurs, using Hungarian matching
  on both encoder and decoder. Report the shared fraction. *Topic:*
  concept-geometry. *Status:* experimental. *Strength:* moderate. *Applies
  when:* the claim is about a particular feature, not about aggregate
  reconstruction
- **R2** — Do not read a single dictionary as an exhaustive feature
  inventory. *Strength:* moderate (C1, C3)
- **R3** — If seed stability matters more than the reconstruction–sparsity
  frontier, L1-ReLU or Gated SAEs may be preferable to TopK. *Strength:*
  weak (C4)

## Bearing on the record

R1 is filed as [SOTA-tmprih86](../practices.d/SOTA-tmprih86.md), `Proposed`. R2 is consistent with [SOTA-310](../practices.d/SOTA-310.md) and adds
a second route to it. R3 is recorded as a condition on [SOTA-344](../practices.d/SOTA-344.md), whose
recommendation and status are unchanged: the reconstruction frontier it
rests on is not in dispute here.

## Limitations

- One seed axis. Data order, data and hyperparameters are held fixed, so
  the paper bounds how much a dictionary depends on initialization only
- The ablations are single-factor sweeps on one small model. The larger
  models appear in a few comparisons
- The training-length trend runs against the paper's conclusion. Overlap
  rises with tokens, and whether 8B tokens trains a 32K Pythia SAE to
  convergence is not addressed
- Interpretability is measured by detection scoring, an automated
  explanation metric. Whether orphan latents are causally used was not
  tested
- No error bars or repeated sweeps are reported in the text
- Of this note: the figures could not be read, so the architecture
  comparison and any per-layer numbers are recorded only as the text
  states them

## Open questions

- Does overlap keep rising with training length until it saturates, and
  where? If it reaches the ReLU figures, the TopK result is partly about
  undertraining
- Does a claim that rests on an orphan latent, a circuit or a steering
  result, fail to replicate on the other seed? That is the downstream test
  of whether checking matters
- How much does varying data order add to the instability from
  initialization?
