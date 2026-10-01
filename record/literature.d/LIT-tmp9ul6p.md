---
status: Active
title: 'bert2BERT: Towards Reusable Pretrained Language Models'
version: 1
tags:
- training-optimization
- model-stability
date: '2026-10-01'
published: '2021-10-14'
arxiv: '2110.07143'
first_author: 'Chen'
keywords:
- 'pretrained-language-models'
- 'efficient-pre-training'
- 'function-preserving-initialization'
- 'advanced-knowledge-initialization'
- 'model-growth'
- 'width-expansion'
- 'two-stage-pre-training'
implementations: []
extends:
- LIT-tmpqc73y
summary: >-
  Chen et al. (2021), [ARXIV-2110.07143](https://arxiv.org/abs/2110.07143) — bert2BERT. Initialize a larger
  Transformer language model from a smaller pretrained one by Net2Net-style
  width expansion, then stack layers for depth. Growing a 54M BERT (12
  layers, width 512) into BERT-base (width 768) with function-preserving
  initialization saves 30.4% of pre-training FLOPs at equal GLUE and SQuAD
  scores. Its recommended variant breaks function preservation by
  borrowing the next layer's weights and adds a two-stage schedule, which
  saves 45.2% on BERT-base and 47% on a GPT-base decoder.
extended_by:
- LIT-tmpvf8fm
---
<!-- inactive-ok-file: SOTA-tmpgvqng — Proposed; named to say this paper is its lineage, not its origin -->

# LIT-tmp9ul6p: bert2BERT: Towards Reusable Pretrained Language Models

Chen et al. (2021), Tsinghua University and Huawei Noah's Ark Lab — [ARXIV-2110.07143](https://arxiv.org/abs/2110.07143)

## Key takeaways

- **Function-preserving initialization (FPI) carried to Transformers.** Every
  matrix is expanded in its input dimension and then its output dimension,
  through index mappings that keep the source's units and fill the new ones
  by uniform sampling. Rows are divided by the number of copies, as in
  Net2WiderNet. Attention is expanded head by head, by reusing whole heads,
  and the mappings are tied across the embedding, attention, feed-forward
  and residual paths. The preservation is approximate: expanding layer-norm
  parameters changes the mean and variance of a non-uniformly replicated
  hidden vector. Expanding a 12×512 source to 12×768, the initialized model's
  MLM loss is 1.70 against the source's 1.67, and 10.42 at random
  initialization (Table 1).
- **The method it recommends is not function-preserving.** Advanced
  knowledge initialization (AKI) fills a layer's new output units from the
  expanded weights of the layer above. The stated reasons are that this
  breaks FPI's symmetry and supplies "high-level knowledge". It starts at a
  higher loss than FPI and converges faster. Filling the new units from the
  layer below did worse. Depth comes from stacking the widened model, as in
  StackBERT. A two-stage schedule first trains randomly sampled bottom
  sub-models, updating only their top 3 layers, and then the full model.
- **Results on BERT-base (Table 2, 3 runs, mean and standard deviation).**
  From the 54M S(12, 512) source, against 7.3e19 FLOPs from scratch: FPI
  saves 30.4%, AKI 38.4%, and AKI with two-stage training 45.2%. All reach
  GLUE and SQuAD averages of 85.7 to 86.0, against 85.5 from scratch.
  Copying the source into a corner and initializing the rest at random
  saves 12.2%. The baselines were re-implemented: StackBERT saves 24.3%
  and MSLT 10.7%. The saving is counted as FLOPs to reach the scratch
  model's final MLM loss.
- **On a decoder (Table 5).** A GPT with 12 layers and width 768, grown from
  a 12×512 source with AKI and full-model training, reaches its loss target
  with 47% fewer FLOPs, with zero-shot perplexity on PTB, WikiText-2 and
  WikiText-103 within 2 points of the scratch model (lower on PTB and
  WikiText-103, higher on WikiText-2).
- **What is and isn't ablated.** With a smaller source, S(6, 512) at 35M,
  the saving falls to 23.9%, and the copy-into-a-corner baseline saves
  nothing (Table 3). Sub-model epochs E_b = 0, 5, 10 and 20 save 38.4%,
  45.2%, 43.9% and 25.4%, and the GLUE average falls from 86.0 to 84.3 as
  E_b grows (Table 4). FLOPs spent pre-training the source are not
  counted. The targets are base-sized, about 110M parameters. FPI alone was
  not run on GPT.

## Standing in the anthology

It extends Net2Net ([LIT-tmpqc73y](LIT-tmpqc73y.md)), and says so. Its abstract describes the
method as extending "the previous function-preserving" work of Chen et al.,
and §3.3.1 reuses Net2WiderNet's random mapping and division by replication
count for every Transformer matrix. What it adds is head-wise expansion for
attention, consistency constraints across the residual stream, and a
departure from preservation (AKI) that it measures as faster.

It is the first paper in the record to recommend initializing a wider
pretrained language model of the same depth from a smaller pretrained one
rather than from scratch, and it ran that comparison on an encoder and on
a decoder. HyperCloning ([LIT-tmpvf8fm](LIT-tmpvf8fm.md)) builds on it and on Net2Net. It
describes bert2BERT as covering "BERT-style" models, which understates the
GPT experiment here. It replaces the random replication with a symmetric
tiling, copying every unit exactly `n` times, so the expanded hidden vector
has the same mean and variance and the layer-norm gap measured in Table 1
does not arise. This paper is therefore the lineage of [SOTA-tmpgvqng](../practices.d/SOTA-tmpgvqng.md) but
not its origin. The instruction there names the symmetric construction,
and bert2BERT's own recommendation is AKI, which gives up exact
preservation.

The two papers point in different directions on symmetry. bert2BERT
deliberately breaks it at initialization and reports that this helps.
HyperCloning keeps it and reports that training breaks it unaided. Neither
ran the other's method, so the record cannot yet say which is better.

Unread — no NOTE.
