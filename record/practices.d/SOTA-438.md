---
number: 438
status: 'Proposed'
formerly:
- SOTA-tmpgvqng
promote_when: >-
  A comparison at matched total compute, with the source model's own
  pretraining charged, showing that a cloned target reaches a given accuracy
  for less total compute than the same target trained from random
  initialization. Short of that, a second group running symmetric width
  expansion against another growth method (Net2Net-style random replication,
  depth stacking) at the same target budget, above the 5.3B the source
  reached. What does not count: another model reported as "initialized from a
  smaller checkpoint", which is adoption, or a further speedup measured on the
  target's tokens alone, which is the comparison already in hand.
consensus: unreplicated
consensus_note: >-
  One group, one paper, three model pairs, no seeds (LIT-765). Width
  growth from a trained model is older than this paper (Net2Net, LIT-758;
  bert2BERT, LIT-749), but no independent group has re-run the symmetric
  construction on decoder language models. Read as of 2026-10.
title: 'To pretrain a wider language model when a smaller pretrained one of the same depth exists, initialize it by function-preserving symmetric width expansion rather than at random'
version: 1
tags:
- training-optimization
- model-stability
date: '2026-10-01'
source:
- LIT-765
# Kept on the source after both predecessors were filed and read. Net2Net
# (LIT-758) introduced function-preserving width growth, for image CNNs.
# bert2BERT (LIT-749) first grew a pretrained language model wider at the
# same depth instead of training from scratch, on BERT and on a GPT decoder, so
# the source's "BERT-style" undersells it. Neither states this instruction.
# Both replicate units by random sampling, which is only approximately
# function-preserving through layer norm (bert2BERT measures the gap), and
# bert2BERT's own recommendation is AKI, which drops preservation on purpose.
# The symmetric tiling, every unit copied exactly n times and scaled by 1/n, is
# what the practice tells the reader to do, and the source states it first.
introduced_by:
- LIT-765
implementations: []
summary: >-
  Samragh et al. (2024), [LIT-765](../literature.d/LIT-765.md) — HyperCloning. Tile each weight matrix
  of the small model into n×n blocks scaled by 1/n, so the wide model computes
  exactly the small model's function at step 0, then train as usual. On three
  2× pairs from 350M to 2.9B, it reached the random-init baseline's final
  10-task accuracy 2.2–4× sooner and finished higher. The source model's
  pretraining is not charged, so this supports reusing a checkpoint that
  already exists, not training a small model in order to clone it.
---

<!-- inactive-ok-file: SOTA-209 — Proposed; named as the neighbouring practice on another axis, not cited as support -->

# SOTA-438: To pretrain a wider language model when a smaller pretrained one of the same depth exists, initialize it by function-preserving symmetric width expansion rather than at random

## Source

Samragh et al. (2024), [LIT-765](../literature.d/LIT-765.md) — HyperCloning, §2–3 and Appendix A–B.

## What to do

To build a target `n` times wider than a pretrained source of the same depth:

- **Linear layers.** Tile the source weight `n` times along both axes and
  divide by `n`, the input expansion factor. Repeat each bias `n` times.
  Every hidden vector in the target is then `n` stacked copies of the
  source's, and the output logits are identical.
- **Normalization layers and positional embeddings.** Repeat their
  parameters `n` times.
- **Attention.** Either duplicate heads, or widen each head and rescale the
  query weights so the attention scores do not change.

Then train with an unchanged loop. Depth stays fixed. The source presents
width growth as complementary to depth stacking and does not combine them.

The idea is older than this construction, and the source says it builds on
two papers. Net2Net ([LIT-758](../literature.d/LIT-758.md)) introduced function-preserving width
growth in 2015. It copied randomly chosen units and divided their outgoing
weights by the number of copies, and on ImageNet Inception a widened network
reached the from-scratch network's final accuracy roughly 2×10⁶ minibatches
sooner. bert2BERT ([LIT-749](../literature.d/LIT-749.md)) carried that construction to Transformers in
2021. Growing a 12-layer, width-512 BERT to width 768 saved 30.4% of
pre-training FLOPs against training from scratch, and its non-preserving
variant saved 47% on a GPT decoder. It was the first to recommend starting a
wider language model from a smaller pretrained one. What the source adds,
and what this practice instructs, is the symmetric tiling. Because every
unit is copied the same number of times, the widened model computes exactly
the small model's function, layer norm included. bert2BERT's random
replication left a measured gap there: MLM loss 1.70 against the source's
1.67. bert2BERT went the other way, deliberately breaking symmetry with the
next layer's weights (AKI) and reporting that it helped. Nobody has run the
two against each other.

## Evidence

[LIT-765](../literature.d/LIT-765.md), which introduced this construction, ran it against random
initialization with every other setting identical: learning rate,
optimizer, nodes, batch size, context and data order. It used three 2× pairs:
OPT-350M → OPT-1.3B, Pythia-410M → Pythia-1.4B and OLMo-1B → OLMo-2.9B. On the
average of ten lm-eval-harness tasks, the cloned models reached the random
baseline's final accuracy **2.2× to 4× sooner** and ended higher at the
budget trained. The same paper's ablations add three things:

- **Symmetric beats diagonal.** On Pythia-1.4B, four function-preserving
  variants all beat random initialization. The diagonal one, with zeros off
  the diagonal, which the paper identifies with Shen et al. (2022), gains
  least. The symmetric one gains most. Noise added to the symmetric one at 10
  dB SNR adds little, so the paper ships the noise-free version.
- **A better source helps, and the help fades.** Cloning OPT-350M checkpoints
  trained for 16, 32 and 64B tokens into OPT-1.3B, the better source starts
  better and the gap narrows with training.
- **A larger source beats a larger factor.** For a 5.3B-parameter target, a 2×
  clone of OPT-1.3B beats a 4× clone of OPT-350M, and both beat random.

## Conditions and limits

- **The source's compute is free in every comparison.** The speedup is
  counted in the target's own tokens. The Pythia and OLMo sources were
  downloaded, and OLMo-1B had seen 2.4T tokens against the target's roughly
  250B. Only the OPT-350M source was trained by the authors, on 30B tokens, and
  that cost is not added to the curve either. This supports "when such a
  checkpoint already exists, start from it". It says nothing about whether
  training a small model in order to clone it beats training the large one
  directly.
- **No other growth method is a baseline.** Net2Net ([LIT-758](../literature.d/LIT-758.md)), bert2BERT
  ([LIT-749](../literature.d/LIT-749.md)), LEMON and depth stacking are discussed and not run. Only the diagonal variant comes
  close to an external method. So the evidence is "better than random", not
  "better than other ways to grow".
- **It forgets first.** Cloned models lose accuracy early in training, most
  visibly on OLMo, and recover with more training. The authors leave the
  cause and the fix open. A run stopped early can land in that dip.
- **The symmetry does break, but the reason is assumed.** Cosine similarity
  between cloned halves starts at 1 and decays in most layers. After training
  the singular-value spectrum resembles the random-init model's. The paper
  attributes this to stochasticity such as dropout and does not test it.
- **Scale and variance.** Targets reach 5.3B at most, each 2× or 4×, and no
  seeds or run-to-run variance are reported. The Pythia source is 410M in the
  architecture table and called 460M in the text. The Pythia target was
  trained on a different dataset (Dolma) from its source (the Pile).
- **One internal inconsistency.** The related-work section says the noise
  variant "improves the model's convergence rate". The paper's own ablation
  shows noise adding little to the symmetric version. The ablation is the
  measurement.

## Beside the record's other practices

[SOTA-209](SOTA-209.md) says to initialize a mixture-of-experts model from a dense
checkpoint. It shares this practice's premise, that a checkpoint you already
paid for is a better start than noise, and applies it along a different axis.
[SOTA-209](SOTA-209.md) grows sparser, by copying the dense feed-forward weights into each
expert. This practice grows wider, and preserves the function exactly by
construction. Neither depends on the other. The two
differ in evidence. [SOTA-209](SOTA-209.md)'s source compared at matched total compute,
and its `promote_when` asks for exactly that. This practice's source did
not, and its `promote_when` asks for the same thing for the same reason.

## Known implementations

None released by the source.
