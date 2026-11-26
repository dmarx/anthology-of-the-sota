---
status: Proposed
promote_when: >-
  A second group measures cross-seed overlap at a width of at least 131K
  latents on a model of at least 7B parameters, with training length
  reported. And a downstream test shows that a claim resting on an orphan
  latent (a circuit, a steering result or a probe) fails to replicate on
  another seed more often than one resting on a shared latent. Overlap
  figures alone cannot satisfy this: the practice is worth its cost only
  if the check changes conclusions.
title: 'Before resting a claim on a particular sparse-autoencoder latent, train a second seed and check that the latent recurs'
version: 1
tags:
- concept-geometry
- analysis-and-evaluation
date: '2026-11-26'
source:
- LIT-tmplifgh
introduced_by:
- LIT-tmplifgh
consensus: unreplicated
consensus_note: >-
  One group's measurement. The survey LIT-tmpilnw1 repeats it as a
  reporting recommendation, which is adoption, not a second test. Earlier
  reports of high stability used smaller L1-ReLU SAEs, a different regime,
  and are reconciled with this result rather than contradicting it.
implementations: []
summary: >-
  Paulo and Belrose (2025), [LIT-tmplifgh](../literature.d/LIT-tmplifgh.md) — SAEs differing only in seed
  share 42% of latents at 32K on Pythia 160M and 30% at 131K on Llama 3 8B.
  About 35% of latents appear in none of eight other seeds, many of them
  interpretable. If a finding names a specific latent, match a second seed's
  dictionary with the Hungarian algorithm and report whether that latent is
  shared.
---

# SOTA-tmprih86: Before resting a claim on a particular sparse-autoencoder latent, train a second seed and check that the latent recurs

## Source

Paulo and Belrose (2025), [LIT-tmplifgh](../literature.d/LIT-tmplifgh.md). Read as [NOTE-tmpf455e](../notes.d/NOTE-tmpf455e.md).

## When this applies

You trained an SAE and are about to report something about a specific
latent. Examples: that the model represents concept X as this feature, that
this feature sits in a circuit, or that steering on it changes behaviour.
It does not apply to aggregate claims about reconstruction or sparsity.

## Do this

- **Train at least one more SAE**, identical except for the
  initialization seed
- **Match the dictionaries** with the Hungarian algorithm, once on encoder
  cosine similarity and once on decoder cosine similarity
- **Call a latent shared** if both matchings give it the same partner,
  each at cosine similarity of at least 0.7. This is the source's
  definition, and its similarity distribution is bimodal, so the result is
  not very sensitive to the exact threshold
- **Report** the shared fraction overall and whether each latent the claim
  rests on is shared. If it is an orphan, the claim is about one training
  run, and the write-up should say so

The evidence is [LIT-tmplifgh](../literature.d/LIT-tmplifgh.md), which isolated the seed by holding the data
and its order fixed. Two SAEs with 2¹⁵ latents on Pythia 160M share 42% of
latents. At 131K latents on Llama 3 8B they share 30%. Against eight other
seeds, about 35% of a base SAE's latents recur in none of them, and the
paper's offset power-law fit suggests that fraction has a floor. Those
orphans are not just noise: under detection scoring, many of them have
explanations as good as those of shared latents.

## Conditions

- **Expect the shared fraction to depend on configuration.** In the source
  it falls with more latents and larger k, rises with training length, and
  is higher for L1-trained ReLU and Gated SAEs than for TopK. Report width,
  k, training tokens and architecture beside it, or the number cannot be
  compared
- **Cost**: one extra SAE training run per configuration, plus the
  matching, which grows cubically with width in the Hungarian algorithm.
  The source reports that mean max cosine similarity gives nearly the same
  picture, so it is a cheaper approximation when width makes matching
  impractical
- **Rarely firing latents are the least stable.** Check those first
- **A shared latent is evidence of a stable direction, not of a true
  feature.** Méloux et al. showed for small networks ([LIT-504](../literature.d/LIT-504.md)) that many
  explanations pass the usual criteria, which is [SOTA-310](SOTA-310.md). Recurrence across
  seeds narrows the candidates without settling which is the mechanism
- **This is unvalidated downstream.** Nobody has yet shown that a finding
  on an orphan latent fails to replicate more often. That test is what
  `promote_when` asks for
