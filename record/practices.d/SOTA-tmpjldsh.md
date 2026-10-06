---
status: Proposed
promote_when: >-
  A second group's ablation of the union against top-k alone and top-p
  alone with sparsity or attention compute held matched across the arms,
  in a setting where the selection is trained, reporting generation quality
  with more than one seed. Prism ran the three arms but let the union use
  more blocks, so it does not count. A paper that adopts the union without
  the single-rule arms would not count either, however strong its headline.
consensus: unreplicated
consensus_note: >-
  Two groups use the rule: SpargeAttention2 (Tsinghua and Berkeley), which
  introduced it and ran a near-sparsity-matched ablation, and Prism (Fudan
  and Tencent Hunyuan), which used it eight months later without credit and
  ablated it without matching sparsity. So the matched evidence is one
  group's. Others prefer a single dynamic budget: Sparse VideoGen2 uses
  top-p alone, VMoBA a cumulative threshold pooled per head, and Sol-Attn a
  mean-plus-deviation threshold chosen for routing speed. LongCat-Video
  tried top-p and kept top-k for load balance.
title: 'Select key blocks for block-sparse attention by the union of a small top-k and a top-p cumulative-mass set, so peaked rows keep a floor and flat rows get more blocks'
version: 1
tags:
- attention-techniques
- inference-optimization
- generative-modeling
date: '2026-10-06'
source:
# SpargeAttention2 defined the union, argued for it on two constructed
# attention maps, and ablated it against each rule alone at near-matched
# sparsity on Wan2.1 at 1.3B and 14B. Prism ran the same three arms on a 16B
# video-audio model at 2K without matching sparsity; its top-k at 85% row
# is the closest it comes to a compute-matched comparison.
- LIT-tmpbgw07
- LIT-tmpe78xc
introduced_by:
- LIT-tmpbgw07
implementations:
- 'SpargeAttention2'
- 'Prism'
summary: >-
  Zhang et al. (2026), [LIT-tmpbgw07](../literature.d/LIT-tmpbgw07.md), and Tu et al. (2026), [LIT-tmpe78xc](../literature.d/LIT-tmpe78xc.md).
  Score key blocks by mean-pooled dot products. For each query block, keep
  the top k% (about 3–5%) together with the smallest set whose softmax mass
  reaches p (about 0.2). Top-p alone fails on rows dominated by a sink, and
  top-k alone undercovers flat rows. At near-matched sparsity on Wan2.1, the
  union beats top-p clearly, beats top-k at 14B, and is level with top-k at
  1.3B. One run per arm. Top-p needs a sort and gives uneven block counts.
---

# SOTA-tmpjldsh: Select key blocks for block-sparse attention by the union of a small top-k and a top-p cumulative-mass set, so peaked rows keep a floor and flat rows get more blocks

## Source

Zhang, Jiang, Xiang et al. (2026), [LIT-tmpbgw07](../literature.d/LIT-tmpbgw07.md) — SpargeAttention2, which
names the rule in its title, defines it (its Eq. 9) and ablates it. Tu, Tian
et al. (2026), [LIT-tmpe78xc](../literature.d/LIT-tmpe78xc.md) — Prism, the second group to use it.

## What to do

Mean-pool queries and keys per block and take a softmax over each query
block's row of pooled scores. Keep a key block if it is among the row's top
k%, or if it falls in the shortest prefix of the sorted row whose mass
reaches p. SpargeAttention2 uses k = 0.03 with p = 0.2 at 1.3B and p = 0.16
at 14B, about 95% sparsity. Prism uses top 5% and p = 0.2. Then run exact
attention over the kept blocks.

## Why a union

The two rules fail on opposite kinds of row ([LIT-tmpbgw07](../literature.d/LIT-tmpbgw07.md), §3.2). On a flat
row, where attention is spread out, a fixed k captures little of the mass. On
a sharply peaked row, top-p can reach its threshold on an attention sink
alone and keep almost nothing else. With p = 0.6 and a row of [0.6 on the
sink, 0.2, 0.1, …], top-p keeps only the sink. The union takes whichever rule
keeps more. On two constructed attention maps at equal sparsity, its output
error tracks the better single rule on each map: 0.3707 against 0.4150 for
top-k on the flat map, and 0.1671 against 0.2160 for top-p on the peaked one.
It does not beat both on either.

## What the evidence shows

**The matched ablation is one group's.** SpargeAttention2 ([LIT-tmpbgw07](../literature.d/LIT-tmpbgw07.md),
Table 6) calibrates each single-rule arm to near the union's sparsity: top-k
alone at about 95%, top-p alone at 93–94%. After the same fine-tuning, the
scores are imaging quality / aesthetic quality / combined VQA:
- At 1.3B: union 67.68 / 65.05 / 86.73, top-k 65.84 / 64.57 / 86.90, top-p
  60.56 / 60.12 / 62.57.
- At 14B (100 steps): union 68.41 / 65.02 / 88.22, top-k 65.24 / 63.99 /
  84.25, top-p 63.37 / 63.62 / 86.43.

Top-p alone collapses at 1.3B. Top-k alone is level with the union there and
behind it at 14B.

**The second group's ablation is unmatched but has one useful row.** Prism
([LIT-tmpe78xc](../literature.d/LIT-tmpe78xc.md), Table 7) trains a 16B video-audio model at 2K. Top-k alone at
95% sparsity scores MotionQ 0.61 at 9.8 minutes per step, top-p alone (0.2)
0.37 at 9.9, and the union 0.89 at 10.6. The union uses more blocks than the
top-k arm, so that margin mixes the rule with the budget. But top-k alone at
85% sparsity, which costs more compute than the union (11.8 minutes per
step), scores 0.76. So in Prism's setting, the union beats top-k at more than
matched compute. It is one run per arm, from a paper whose baselines were
trained differently.

## What it costs

- **Routing time.** Top-p needs each row sorted. Sol-Attn ([LIT-tmpx3dxt](../literature.d/LIT-tmpx3dxt.md))
  measures routing at 10.8 ms for top-p against 3.80 ms for top-k and
  0.33 ms for its own threshold rule. The union pays the top-p cost.
- **Uneven work.** A union gives query blocks different numbers of key
  blocks. LongCat-Video ([LIT-tmpid6gf](../literature.d/LIT-tmpid6gf.md)) found top-p better without training
  but kept top-k for training because of load imbalance across GPU work
  units. Prism's union is 8% slower per step than top-k alone at the same k.

## Conditions

- **It is a block-selection rule for diffusion transformers over video.**
  Both sources are video models, and SpargeAttention2's backbones are Wan2.1
  only. Language-model block selection in the record ([LIT-143](../literature.d/LIT-143.md), [SOTA-138](SOTA-138.md)) uses
  learned scores and a fixed budget, and this rule is untested there.
- **Training matters more than the rule.** SpargeAttention2's same masker
  without fine-tuning loses 42–66 points of VQA. The rule is evidence about
  what to select once the model is adapted to the mask.
- **The alternatives are single dynamic budgets.** Sparse VideoGen2
  ([LIT-tmpucn4v](../literature.d/LIT-tmpucn4v.md)) uses top-p alone over content clusters, VMoBA
  ([LIT-tmpmuiol](../literature.d/LIT-tmpmuiol.md)) a cumulative threshold pooled across all queries of a head,
  and Sol-Attn a per-query mean-plus-deviation threshold. VMoBA's per-head
  threshold beat per-query top-k in its ablation, without reported density.
  None of these was compared with the union.

## Known implementations

- SpargeAttention2 (CUDA mask construction and forward and backward kernels)
- Prism (Triton)
