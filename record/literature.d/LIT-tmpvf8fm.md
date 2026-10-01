---
status: Active
title: 'Scaling Smart: Accelerating Large Language Model Pre-training with Small Model Initialization'
version: 1
tags:
- training-optimization
- model-stability
date: '2026-10-01'
published: '2024-09-19'
arxiv: '2409.12903'
first_author: 'Samragh'
keywords:
- 'hypercloning'
- 'model-growth'
- 'width-expansion'
- 'function-preserving-initialization'
- 'knowledge-transfer'
- 'pretraining-acceleration'
implementations: []
summary: >-
  Samragh et al. (2024), [ARXIV-2409.12903](https://arxiv.org/abs/2409.12903) — HyperCloning. Initialize a wider
  language model from a smaller pretrained one of the same depth by tiling
  each weight matrix into n×n blocks scaled by 1/n, so every hidden vector
  is n stacked copies of the small model's and the logits match exactly.
  Against random initialization with every other setting identical, the
  cloned models reach the random baseline's final 10-task accuracy 2.2–4×
  sooner and finish higher, on OPT, Pythia and OLMo targets of 1.3–2.9B.
  The small model's own pretraining is not charged to the comparison.
---
<!-- inactive-ok-file: SOTA-209 — Proposed; named as neighbours this paper informs or tests, with their standing stated where they are cited -->

# LIT-tmpvf8fm: Scaling Smart: Accelerating Large Language Model Pre-training with Small Model Initialization

Samragh et al. (2024), Apple — [ARXIV-2409.12903](https://arxiv.org/abs/2409.12903)

## Key takeaways

- **The construction is exact and cheap.** For an n-fold width expansion,
  each linear layer's weight is the source matrix tiled n times along both
  axes and divided by n (the input expansion factor), and each bias is
  repeated n times. Every hidden representation in the large network is then
  n copies of the small network's, and the output logits are identical.
  Layer norm affine parameters and positional embeddings are repeated;
  attention is expanded either by duplicating heads or by widening each head,
  in which case the query weights are rescaled so the attention scores do
  not change. Depth is held fixed; the paper presents width growth as
  complementary to the depth-stacking methods it cites.
- **The comparison is against random initialization, everything else
  matched.** Learning rate, optimizer, nodes, batch size, context size and
  data order are identical across the two arms. Pairs: OPT-350M → OPT-1.3B,
  Pythia-410M → Pythia-1.4B, OLMo-1B → OLMo-2.9B, each a 2× width expansion.
  Averaged over ten lm-eval-harness tasks, the cloned model reaches the
  random baseline's final accuracy **2.2× to 4× sooner** and ends higher at
  the training budget used. The OLMo-1B source had seen 2.4T tokens; the
  cloned target is trained on about 250B. The paper's text calls the
  Pythia source 460M; its architecture table says 410M.
- **It forgets before it gains.** Cloned models show catastrophic
  forgetting at the start of training, most visibly on OLMo, and recover
  from it with further training. The authors leave the cause and the
  mitigation open.
- **The duplicated weights do not stay duplicated.** The cosine similarity
  between cloned halves of a row starts at 1 and decays in most layers, and
  the singular values tell the same story. At initialization half the
  singular values of a cloned matrix are zero; after training the spectrum
  resembles that of the randomly initialized model. The authors attribute
  the symmetry breaking to stochasticity such as dropout and do not test
  that attribution.
- **What is ablated.** On Pythia-1.4B, four function-preserving variants
  all beat random initialization: symmetric tiling, diagonal (source blocks
  on the diagonal, zeros off it), and noisy versions of each at 10 dB SNR.
  Diagonal gains least and symmetric and noisy-symmetric gain most, with
  noise adding little, so the paper ships the noise-free version. Its
  related-work section separately says noise addition "improves the
  model's convergence rate", which its own ablation does not show. Cloning
  an OPT-350M checkpoint at 16, 32 or 64B tokens: the better source starts
  better and the gap shrinks with training. For an OPT-5.3B target, a 2×
  clone of OPT-1.3B beats a 4× clone of OPT-350M, and both beat random.
- **What is not.** The compute that trained the source model is never
  counted; the speedup is measured on the target's own tokens. No other
  growth method is run as a baseline (Net2Net, LEMON, depth stacking).
  The diagonal variant is the closest to an external method, and the paper
  identifies it with Shen et al. (2022). There is no depth expansion, no
  target beyond 5.3B, and no statement of seeds or run-to-run variance.

## Standing in the anthology

The record holds no model-growth paper; this is the first. Its nearest
neighbour is [SOTA-209](../practices.d/SOTA-209.md), which says to initialize a mixture-of-experts model
from a dense checkpoint, on the evidence of [LIT-227](LIT-227.md)'s sparse upcycling.
The two share a premise: a checkpoint you already paid for is a better
starting point than noise for a larger model. HyperCloning makes the same
move along a different axis, wider rather than sparser, and it preserves
the function exactly where upcycling copies feed-forward weights into
experts.

The two papers differ in what they can support. [LIT-227](LIT-227.md)'s claim rests on a
comparison at matched total compute, and [SOTA-209](../practices.d/SOTA-209.md)'s `promote_when` asks for
exactly that, dense pretraining included. This paper charges nothing for
the source model, which for OLMo was a 2.4T-token run downloaded from
Hugging Face. Its result therefore supports "reuse an existing smaller
checkpoint when one exists". It says nothing about whether training a small
model in order to clone it beats training the large one directly.

It also bears, from the side, on [LIT-519](LIT-519.md). That paper found that shaping an
initialization to imitate a trained model's spectral profile changes the
spectra and does not improve results. HyperCloning transfers the trained
function itself, not a statistic of it, and does improve results.
Together the two papers suggest that what helps is the function and not
the shape of the spectrum, though neither paper tests that directly.

Unread — no NOTE.
