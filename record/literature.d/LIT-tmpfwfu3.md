---
status: Active
title: 'DINOv2: Learning Robust Visual Features without Supervision'
version: 1
tags:
- data-pipeline
- representation-and-encoding
- model-stability
- vision-and-graphics
date: '2026-09-23'
published: '2023-04-01'
arxiv: '2304.07193'
first_author: 'Oquab'
keywords:
- 'data-curation'
- 'frozen-features'
- 'self-distillation'
- 'foundation-models'
summary: >-
  Oquab et al. (2023), [ARXIV-2304.07193](https://arxiv.org/abs/2304.07193). The thesis is that existing
  self-supervised objectives already produce general-purpose features if
  the data is curated enough, so the contribution is a retrieval-based
  curation pipeline and the engineering to scale it — not a new objective.
  Frozen features, no finetuning, competitive with the best open
  weakly-supervised models.
---

# LIT-tmpfwfu3: DINOv2: Learning Robust Visual Features without Supervision

Oquab et al. (2023) — [ARXIV-2304.07193](https://arxiv.org/abs/2304.07193)

## Key takeaways

- **The claim is about data, and it is stated as such.** "Existing
  pretraining methods, especially self-supervised methods, can produce such
  features **if trained on enough curated data from diverse sources**." The
  objective is assembled from DINO and iBOT rather than invented; what is new
  is the pipeline that feeds it.
- **Curation by retrieval, not by filtering.** Take a large uncurated pool
  and several curated datasets as queries; retrieve each query's nearest
  neighbours in embedding space — **typically 4**, because "much larger than
  4 … leads to more collisions"; deduplicate. The result is **LVD-142M**.
  Faiss for the index; 20 nodes of 8×V100-32GB, under two days. The inspiration
  is named as text-curation pipelines, where a model trained on Wikipedia
  scores documents from a crawl.
- **The controlled comparison is the reason to believe it.** Against **142M
  images randomly sampled from the same source**, curated wins — so this is
  not a data-volume result. Against ImageNet-22k, a ViT-g on LVD-142M matches
  on ImageNet-1k "while significantly outperforming it on the other
  benchmarks", which is the general-purpose claim rather than a
  leaderboard one.
- **Train the big one, distill the small ones.** A 1B-parameter ViT-g is
  trained, then distilled into the smaller models. The distilled model beats
  the same architecture trained from scratch **on all 12 benchmarks**.
- **Two regularisers worth naming.** A **KoLeo** term, from the
  Kozachenko-Leonenko differential entropy estimator, encouraging features to
  spread uniformly within a batch; and **Sinkhorn-Knopp centering** borrowed
  from SwAV ([LIT-tmp6nq8y](LIT-tmp6nq8y.md)) in place of the teacher's softmax centering. Both
  appear as separate ablation rows. This is the same anti-collapse question
  <!-- inactive-ok: THEORY-087 — Deferred by design: the question is open and this cluster is where the record says so. Citing it is the point, not an oversight. -->
  [THEORY-087](../theory.d/THEORY-087.md) tracks, arriving as a stack of regularisers rather than as
  a mechanism anyone claims to understand.
- **The deliverable is frozen features.** The whole argument is features that
  "work across image distributions and tasks without finetuning", competitive
  with the best openly available weakly-supervised models. That is what makes
  it usable as a measurement instrument rather than only as a backbone.

## Standing in the anthology

Unit D of `#304`, filed with [LIT-tmp6nq8y](LIT-tmp6nq8y.md) as the pair of instruments the
<!-- inactive-ok: SOTA-338 — Proposed, and cited for what its promote_when asks for rather than for its recommendation — which is the gap this note closes. -->
record was already reaching for: `SOTA-338`'s `promote_when` requires a
Fréchet distance "in a non-ImageNet feature space (CLIP, SwAV or DINOv2)",
and `SOTA-307` reports DINOv2 FID, precision, density and coverage. The
record could not promote its own practice without a paper it did not hold.

<!-- inactive-ok: THEORY-087 — Deferred by design: the question is open and this cluster is where the record says so. Citing it is the point, not an oversight. -->
Sources [SOTA-tmpj9zpp](../practices.d/SOTA-tmpj9zpp.md), and joins [THEORY-087](../theory.d/THEORY-087.md) as a source for the way it
stacks anti-collapse regularisers rather than choosing among them.
