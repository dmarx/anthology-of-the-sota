---
status: Active
title: 'Olmo Hybrid: From Theory to Practice and Back'
version: 1
tags:
- model-architecture
- attention-techniques
- training-optimization
- analysis-and-evaluation
- adaptation-and-tuning
date: '2026-10-06'
published: '2026-04-03'
arxiv: '2604.03444'
first_author: 'Merrill'
keywords:
- 'hybrid-models'
- 'gated-deltanet'
- 'negative-eigenvalues'
- 'expressivity'
- 'state-tracking'
- 'scaling-laws'
- 'quantization-model'
- 'drope'
- 'long-context'
implementations:
- 'Olmo Hybrid 7B (Ai2)'
# The model is Olmo 3 7B with its sliding-window layers replaced by Gated
# DeltaNet layers; it inherits that model's recipe, data and evaluation, and
# the recurrence is Gated DeltaNet's with the negative-eigenvalue extension.
extends:
- LIT-130
- LIT-137
# Olmo 3 is the controlled 7B/6T comparison; Mamba-2 layers are the rival
# recurrent mixer in the §5.1 ablations; YaRN is the long-context method set
# against DroPE in Table 3; the rest are Table 6's open-weight rows.
compared_against:
- LIT-130
- LIT-162
- LIT-193
- LIT-120
- LIT-183
- LIT-133
- LIT-182
summary: >-
  Merrill et al., Ai2 and Lambda (2026), [ARXIV-2604.03444](https://arxiv.org/abs/2604.03444). Olmo 3 7B with its
  sliding-window layers replaced by Gated DeltaNet (negative eigenvalues), at
  3:1 with full attention, trained to 6T tokens. It reaches Olmo 3's MMLU in
  49% fewer tokens and beats it in every domain after mid-training, though
  data mix, schedule and mid-training batch also changed. Scaling fits from
  60M to 1B give the hybrid a lower data coefficient (83.7 against 94.9,
  non-overlapping CIs); the projected 1.3–1.9× token savings have CIs that
  include 1 at every size but 3B. A theorem shows hybrids express a task
  neither parent can. Removing negative eigenvalues barely changes the
  scaling, which weakens the expressivity explanation.
---

# LIT-tmpax1wi: Olmo Hybrid: From Theory to Practice and Back

Merrill, Li, Romero, Svete, Costello and 17 others, Ai2, UW, Lambda, ETH
Zürich and Cambridge (2026) — [ARXIV-2604.03444](https://arxiv.org/abs/2604.03444). Read at v4 (15 Jun 2026),
main text and Appendices A–E with the proofs skimmed; v1 is 3 Apr 2026.

## Key takeaways

- **The model** (§2.1–2.2, App. A.1). Olmo 3 7B with its three-in-four
  sliding-window layers replaced by Gated DeltaNet layers using the
  negative-eigenvalue extension (β → 2β), and the fourth layer kept as full
  multi-head attention. Two heads are removed (30 heads, d_k 96, d_v 192) to
  match parameters (7.0B against 6.8B) and throughput. A GDN layer's
  inference state is 1.05 MiB, against 512 MiB for a 32K MHA layer
  (Table 1).
- **Against Olmo 3 at 7B** (§2.3, Fig. 1, Tables 2–3). It reaches Olmo 3's
  Common Crawl loss in 35% fewer tokens and its MMLU in 49% fewer, and
  19–58% fewer across six more benchmarks (Fig. 15). After pretraining it
  leads on math, STEM and non-STEM MC and trails on code and GenQA. After
  mid-training it leads in all five domains (e.g. MC non-STEM 81.3 against
  78.2). RULER at 64K: 76.9 against 70.9 with YaRN for both, and 85.0 with
  DroPE.
- **Hybrids express more than either parent** (§3.3–3.4, App. B). Theorem 1:
  state-based recall, which composes pointer swaps with an index into a bit
  array, is solved by one alternation of GDN and attention in either order.
  No transformer can solve it (assuming TC⁰ ≠ NC¹) and no bounded-state RNN
  can (communication complexity). Theorem 3: with polynomial padding, hybrids
  recognize all of NC¹, while padded transformers are exactly TC⁰. Boolean
  formula evaluation separates them.
- **The synthetic tasks agree** (§3.5, Tables 15–17). With 4-layer models,
  state-based recall at n = m = 128 is solved by the hybrid (1.00), against
  0.54 for the transformer and 0.64 for pure GDN. The hybrid without negative
  eigenvalues drops to 0.57, and pure GDN without them fails state tracking
  past n = 32.
- **Scaling fits** (§4.1, Tables 18–20). Transformer, pure GDN and the 3:1
  hybrid are fit from 60M to 1B at 10–160 tokens per parameter, on identical
  data. With free exponents the CIs overlap everywhere. Fixing α = β = 0.22,
  the hybrid's data coefficient B is 83.65 [79.9, 87.0] against the
  transformer's 94.85 [89.3, 101.4]. The fit predicts Olmo Hybrid 7B's final
  loss to 0.28% and Olmo 3 32B's to 1.69%.
- **Why expressivity would show up in scaling** (§4.2, App. E). The
  quantization model of scaling laws is extended so that each task is
  expressible with probability 1 − ε. Inexpressible tasks need more
  parameters or tokens, or reach less loss reduction. Lowering ε then
  lowers the loss curve without changing the exponent. The fitted laws match
  this best if inexpressible tasks need only more tokens.
- **Architecture ablations** (§5.1, Table 5, OlmoBaseEval BPB at 1B, lower is
  better). Transformer 0.682, pure GDN 0.677, pure Mamba-2 0.718. GDN hybrids
  at 1:1 / 3:1 / 7:1 score 0.674 / 0.669 / 0.675, and the Mamba-2 3:1 hybrid
  0.698. Interleaved placement beats concentrating attention in the middle
  (0.669 against 0.672). 7:1 is within 0.005 of 3:1 at 60M–190M and ahead
  of it at 600M (0.748 against 0.754).
- **Post-training is unfinished** (§5.3, Table 7). The Olmo 3 recipe applied
  unchanged gives gains on knowledge, MMLU +4.5 after DPO, and losses on
  reasoning: AIME 2024 −13.4, AIME 2025 −10.2 and BBH −12.0 after DPO.
  Correct generation in vLLM needed eager mode, which costs throughput, or a
  GDN cache held in fp32.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **The 7B comparison is not fully controlled.** App. A.1–A.2 lists the
  changes: the Olmo 3 32B data mix in place of the 7B mix, cosine decay in
  place of a piecewise schedule, a doubled mid-training batch, two merged
  mid-training runs, and a long-context recipe that "differs slightly"
  (footnote 9). Only for the data mix is there a check, a preliminary run
  with "similar trends toward the beginning of training". The 35% and 49%
  token savings and the post-mid-training lead carry all of these.
- **"A 14.1% improvement on RULER 64k"** (§1) is 14.1 points, and it sets
  Olmo Hybrid with DroPE against Olmo 3 with YaRN. With YaRN for both the
  gap is 6.0. Olmo 3 leads at 4K (95.8 against 92.8). Table 6 gives Olmo 3
  67.8 at 64K where Table 3 gives 70.9.
- **The token savings are less certain than the B coefficient.** Table 20's
  savings and 95% CIs: 1.32× [0.67, 4.02] at 1B, 1.57× [1.11, 2.50] at 3B,
  1.68× [0.91, 3.47] at 7B and 1.89× [0.71, 5.81] at 70B. Only 3B excludes
  1. In the fixed-exponent fit the transformer has the lower irreducible loss
  (1.55 against 1.58). At 10²² FLOPs the projected loss gap is −0.04 with a
  CI of [−0.14, +0.06] (Table 19).
- **The expressivity explanation has a counter-result in the same paper.**
  §4.3 says so: GDN without negative eigenvalues "shows very similar scaling
  trends", although only the negative-eigenvalue version can track state. In
  Table 5 at 1B, two hybrid variants beat the selected one: no output gate
  (0.666) and positive eigenvalues with the gate (0.667), against 0.669. The
  authors call the theory "a plausible conceptual explanation" and warn
  against its quantitative predictions. The instantiation that fits was
  chosen after seeing the fits.
- **The synthetic transformer fails where depth is not the issue.** On state
  tracking it scores 0.51 at n = 4 and 0.28 at n = 8. The TC⁰ limit is
  asymptotic in n, and a 4-layer transformer can express a handful of swaps.
  So what Fig. 7 separates is learnability under this curriculum, not only
  expressivity. Each curve is the best run from a sweep, selected on the
  hardest setting and scored on 256 samples (App. C.3). The synthetic
  "hybrid" always ends in its single attention layer.
- **Text and tables disagree in places.** In §5.3, the inference throughput
  numbers do not match Table 8 (e.g. 3,023 against 3,077 tokens/s at 4K), and
  the text cites "Table 7" for them. The fixed-exponent E and A given in
  §4.1 and App. D.1.1 (1.569 / 1.597, 71.8 / 70.1) differ from Table 18's
  (1.55 / 1.58, 66.63 / 65.09). The B values agree. Final pretraining is
  "6T" in the text and 5.5T in Table 4.
- **"The gap growing at larger scales"** (§5.1) for interleaved over middle
  placement is not in Table 5. The gaps are 0.010 at 60M, 0.000 at 600M and
  0.003 at 1B.
- **Ablation sizes are nominal.** The ladder matches each model's blueprint to
  Olmo 3's, not its parameter count, so a "760M" hybrid has 948M parameters
  (Table 22). The scaling fits use exact counts, but the per-scale rows in
  Table 5 do not, which the caption flags.

## Which comparisons are like for like

- **§4.1 and §5.1** share data (the Olmo 3 32B mix), optimizer, batch-size
  scaling, WSD-S schedule and evaluation. Only the sequence mixer changes,
  with MLPs held identical. One run per configuration.
- **Table 2–3's Olmo 3 rows** are the released model's own pipeline, against
  the deviations listed above.
- **Table 6's open-weight rows** differ in data, token budget (2T to 36T) and
  architecture. The authors say they are not meaningful for architecture, and
  the Pareto claim uses 6ND compute estimated from reported counts.

## Standing in the anthology

Here the transformer a linear-attention hybrid is measured against is a
released, fully open model of the same lineage, which no other hybrid paper in
the record has.
It extends Olmo 3 ([LIT-130](LIT-130.md)), whose architecture, data and evaluation it keeps,
and it carries Gated DeltaNet ([LIT-137](LIT-137.md)) with the negative-eigenvalue
extension that Qwen3-Next and Kimi Linear do not use. That makes it a source
for [SOTA-132](../practices.d/SOTA-132.md) from a fourth laboratory. The ratio ablation also supports the
practice's "about 3:1": 3:1 is best at 760M and 1B, second to 7:1 at 600M,
and within 0.005 of 7:1 below 190M. The practice's Variations section says the mixer's family is
"a second-order choice". Here, under one recipe, the Mamba-2 ([LIT-162](LIT-162.md)) hybrid
falls behind the plain transformer at 1B (0.698 against 0.682) while the GDN
hybrid leads it (0.669). For this comparison, the family was first-order.

For [SOTA-135](../practices.d/SOTA-135.md) it is an independent test of the gated delta rule against
Mamba-2's decay-only update, pure and hybrid, at seven scales. GDN wins
every row, and pure GDN is ahead of the transformer at every scale too
(0.677 against 0.682 at 1B).

On position it adds evidence to [SOTA-153](../practices.d/SOTA-153.md). For long context, Olmo Hybrid
compares YaRN ([LIT-193](LIT-193.md)) with DroPE, which removes RoPE from all the
attention layers. That leaves position to the GDN layers, the layout
[SOTA-153](../practices.d/SOTA-153.md) recommends, reached by extension rather than by pretraining
without an encoding. On the same 100B tokens DroPE leads at 32K and 64K
(85.0 against 76.9) and trails slightly at 4K–16K. That is a controlled
comparison against a YaRN-extended model at matched cost, which [SOTA-153](../practices.d/SOTA-153.md)
lists as missing, but it is one model from a group outside the three that
practice names.

Table 6 places it among the open-weight hybrids already in the record:
Falcon-H1 7B ([LIT-120](LIT-120.md)), Nemotron 3 Nano ([LIT-183](LIT-183.md)), Kimi Linear 48B-A3B
([LIT-133](LIT-133.md)), with Qwen3 8B ([LIT-182](LIT-182.md)) as a dense reference. All of them were
trained on other data and budgets. Olmo Hybrid at 6T is below Falcon-H1 at
12T on every average except GenQA, and below Qwen3 8B at 36T on four of
five. The comparison says little about architecture.

The long-context ablation paper from Ai2, with four authors in common
([LIT-tmpnww11](LIT-tmpnww11.md)), finds that Olmo 3's own architecture is among the harder ones
to extend, because of QK norm, post-norm and sliding windows. Olmo Hybrid by
its own description changes only the mixer, so it keeps Olmo 3's QK norm and
post-norm and loses the windows. Part of its RULER gain over Olmo 3 may
come from that removal and not from the recurrence. Neither paper separates
the two.

Filed without a NOTE: the takeaways come from one full reading of v4. The
proofs in Apps. B and E were read for their statements and proof sketches,
not checked line by line. Figs. 1, 8–10 and 13–21 are curves, and only
values stated in the text or tables are quoted.
