---
status: Active
title: 'Sparse Autoencoders Trained on the Same Data Learn Different Features'
version: 1
tags:
- concept-geometry
- analysis-and-evaluation
date: '2026-11-26'
published: '2025-01-28'
arxiv: '2501.16615'
first_author: 'Paulo'
keywords:
- 'sparse-autoencoder'
- 'seed-dependence'
- 'feature-universality'
- 'hungarian-matching'
- 'topk'
- 'orphan-latents'
implementations: []
summary: >-
  Paulo and Belrose (EleutherAI, ICLR 2026), [ARXIV-2501.16615](https://arxiv.org/abs/2501.16615). Two SAEs
  trained on the same activations, in the same data order, differ only in
  the initialization seed. Matched by the Hungarian algorithm, only 42% of
  latents are shared at 32K latents on Pythia 160M, and 30% at 131K on
  Llama 3 8B. Against eight other seeds, about 35% of a base SAE's latents
  are found nowhere else, and many of those are interpretable. Overlap falls
  with width and k, rises with training length, and is higher for L1-ReLU
  than for TopK.
---

<!-- inactive-ok-file: SOTA-tmprih86, SOTA-344 — Proposed. The first is filed from this paper in this contribution; the second is named as the practice this paper adds a condition to -->

# LIT-tmplifgh: Sparse Autoencoders Trained on the Same Data Learn Different Features

Paulo and Belrose, EleutherAI (ICLR 2026) — [ARXIV-2501.16615](https://arxiv.org/abs/2501.16615)

## Key takeaways

- **Method** (§3): match the latents of two SAEs with the Hungarian
  algorithm, separately on encoder and decoder cosine similarity. A latent
  is *shared* if both matchings pick the same partner, each with cosine
  similarity of at least 0.7. Otherwise it is an *orphan*. The matched
  similarities are bimodal (Figure 1), which is what makes a threshold
  usable. Mean max cosine similarity, the earlier metric, gives nearly the
  same picture (Figures A2–A3)
- **Headline**: two SAEs with 2¹⁵ latents on Pythia 160M's layer-6 MLP,
  trained on 8B Pile tokens in the same order, share 42% of latents. On
  Llama 3 8B with 131K latents the figure is 30%
- **Orphans persist with more seeds** (§4, Figure 2): with nine seeds,
  about 35% of a base SAE's latents are orphans against all eight others. A
  power law with an offset fits better than one without, so the authors
  read the orphan fraction as having a floor. Frequently firing latents are
  shared most often and rarely firing latents least often
- **Orphans are often interpretable** (§5, Figure 6, Table 1): under
  detection scoring, latents shared by more seeds score higher on average.
  A substantial fraction of single-seed latents still score well. So one
  run misses interpretable features, not only noise
- **What moves the overlap** (§6, Figures 4–5): it falls as the number of
  latents and k rise, and rises with training tokens. It is lower in the
  first and last layers than in the middle ones. L1-trained ReLU and Gated
  SAEs overlap more than TopK, which reconciles this paper with earlier
  reports of over 90% overlap between GPT-2 seeds: those were smaller ReLU
  SAEs
- **The authors' reading** (§7): an SAE gives a pragmatically useful
  decomposition of activation space, not the list of features the model
  "truly uses". They attribute this to the non-convexity of the SAE loss

## Standing in the anthology

**Filed as the primary evidence the survey [LIT-tmpilnw1](LIT-tmpilnw1.md) cited** for
SAE features differing across seeds. It is the source of [SOTA-tmprih86](../practices.d/SOTA-tmprih86.md), a check
the record lacked. It also gives a second, independent route to the
conclusion of [SOTA-310](../practices.d/SOTA-310.md). Méloux et al. ([LIT-504](LIT-504.md)) show many explanations
pass the criteria for one fixed network. This paper shows that the
decomposition itself changes when only the seed does.

**It bears on [SOTA-344](../practices.d/SOTA-344.md) without contesting it.** That practice recommends
TopK over an L1 penalty on the reconstruction–sparsity frontier, from Gao et
al. ([LIT-571](LIT-571.md)). This paper does not dispute the frontier. It finds that
TopK latents recur across seeds less often than L1-ReLU latents do. That is
a cost the frontier does not show, and the practice now says so.

**What the headline omits.** The abstract says TopK's lower stability holds
"even when controlling for the level of sparsity". The body does not
describe that control. The comparison is a single GPT-2 panel (Figure 5),
which this reading could not inspect. The paper also says SAEs "diverge,
rather than converge, with increasing scale". The scale meant is SAE width
and model size. The Llama comparison varies both at once, and longer
training goes the other way, raising overlap. Whether the Pythia SAEs, at
8B tokens, were trained to convergence is not addressed.

Read — [NOTE-tmpf455e](../notes.d/NOTE-tmpf455e.md).
