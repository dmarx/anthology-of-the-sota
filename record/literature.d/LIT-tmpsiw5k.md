---
status: Active
title: 'Gated DeltaNet-2: Decoupling Erase and Write in Linear Attention'
version: 1
tags:
- attention-techniques
- model-architecture
date: '2026-10-06'
published: '2026-05-21'
arxiv: '2605.22791'
first_author: 'Hatamizadeh'
keywords:
- 'linear-attention'
- 'delta-rule'
- 'erase-gate'
- 'write-gate'
- 'channel-wise-decay'
- 'fast-weights'
- 'chunkwise-wy'
- 'hybrid-architecture'
implementations:
- 'GatedDeltaNet-2 (NVlabs)'
# The recurrence is KDA's with its scalar beta split into two channel-wise
# gates, and it reduces to KDA, and then to Gated DeltaNet, when the gates are
# tied. Both are what it could not stand without.
extends:
- LIT-133
- LIT-137
# Table 2-4: every baseline retrained under one recipe at 1.3B/100B, recurrent
# and hybrid, at matched recurrent state size.
compared_against:
- LIT-162
- LIT-137
- LIT-133
- LIT-165
summary: >-
  Hatamizadeh, Choi and Kautz, NVIDIA (2026), [ARXIV-2605.22791](https://arxiv.org/abs/2605.22791). The delta
  rule's scalar beta decides two things at once: how much to erase along the
  key and how much of the value to write. Splitting it into a channel-wise
  erase gate on the key and a channel-wise write gate on the value, on top of
  KDA's channel-wise decay, gives the best average of six recurrent mixers at
  1.3B/100B tokens and matched state size (53.11 against 52.39 for Mamba-3
  MIMO and 52.28 for KDA; 53.97 hybrid). One run each. The erase gate carries
  most of the gain. Its multi-key retrieval lead is real, but Gated DeltaNet
  beats it on the word-needle task at 4K, 60.6 against 31.8.
---

# LIT-tmpsiw5k: Gated DeltaNet-2: Decoupling Erase and Write in Linear Attention

Hatamizadeh, Choi and Kautz, NVIDIA (2026) — [ARXIV-2605.22791](https://arxiv.org/abs/2605.22791). Read at v1
(21 May 2026), the only version, main text and Appendices A–E.

## Key takeaways

- **The scalar gate is two decisions** (§3.1, Eqs. 8–10). In the gated delta
  rule, β scales both the read that is subtracted and the value that is
  written. Gated Delta Rule-2 replaces it with an erase gate b on the key
  axis and a write gate w on the value axis, each a sigmoid of its own
  projection: S_t = (I − k_t (b_t ⊙ k_t)ᵀ) D_t S_{t−1} + k_t (w_t ⊙ v_t)ᵀ.
  The write direction stays k_t. The read direction becomes b_t ⊙ k_t, so
  the erase update is asymmetric. Tying b = w = β·1 gives KDA exactly, and
  tying the decay to a scalar as well gives Gated DeltaNet (App. A.5).
- **Training stays chunkwise** (§3.3–3.4, Apps. A–B). Normalising the state
  by the cumulative decay folds the channel-wise decay into the two factors of
  each rank-one erase, so the chunk equations keep KDA's shape and the WY
  inverse is shared by the erase and write sides. The one real change is in
  the backward pass: a scalar β can be pulled outside the dot products that
  accumulate dA, and per-channel gates cannot, so they are baked into those
  products. Gradients match a token-wise reference to machine precision in
  fp64 (App. D.6).
- **Best average in both families at matched state** (Table 2; App. E.1).
  Every model is 1.3B, 100B FineWeb-Edu tokens, 4K training length, and one
  recipe. Recurrent state is 262,144 floats per layer for all of them.
  Recurrent average: Gated DeltaNet-2 53.11, Mamba-3 MIMO 52.39, KDA 52.28,
  Gated DeltaNet 52.07, Mamba-2 51.82, Mamba-3 SISO 51.42, with the lowest
  Wiki perplexity (15.90). With a 2K sliding window in every other block:
  53.97, against 52.72 for the next best and 50.86 for the Transformer.
- **Retrieval, where it leads and where it does not** (Tables 3–4). Recurrent
  multi-key NIAH: 72.6 / 51.4 / 37.8 at 1K / 2K / 4K, against 58.0 / 44.2 /
  28.0 for the best of the rest. Real-world recall average: 29.88 recurrent
  and 42.28 hybrid, both best.
- **The erase gate does most of the work** (Table 5). The ablation scalarises
  one gate at a time by averaging it over channels, keeping the projections.
  Channel-wise erase only: Wiki 16.12, average 52.79, word-needle at 2K 84.6.
  Channel-wise write only: 16.55, 52.45, 71.4. Both: 15.90, 53.11, 89.8.
  Widening the erase range to [0, 2] for negative eigenvalues changes nothing
  at this scale (53.04).
- **The cost is small but not zero** (Fig. 2). On one H100, hybrid training
  throughput falls only from 38.0 to 36.1 K tokens/s between 2K×8 and 16K×1,
  and sits slightly below KDA's, which the figure shows without numbers.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Remains strong" on needles is selective.** In the recurrent family the
  word-needle task at 4K goes to Gated DeltaNet, 60.6 against 31.8, a
  reversal the text does not mention. In the hybrid family, Mamba-3
  SISO is level or ahead on the numeric needle at 4K (58.2 against 57.9).
  The multi-key lead is the clean one.
- **The real-world average hides one task.** Recurrent DROP is the lowest of
  the six (17.87, against 21.80 for KDA). The text puts this gap down to
  local evidence aggregation. In the hybrid table, Mamba-3 MIMO is ahead on
  FDA (55.31 against 54.68).
- **One run per model, no variance.** The recurrent average margin over
  Mamba-3 MIMO is 0.72 points and the hybrid margin over the next best is
  1.25. Nothing in the paper says how much a reseed moves these averages.
- **"Matched parameter count" has no table.** State size is matched and
  shown (App. E.1). The two gate projections add d_model → H·d_k and
  d_model → H_v·d_v per layer where KDA has a scalar β, and the paper does
  not say how the 1.3B was rebalanced. "A stronger update rule rather than a
  larger memory" holds for the state, not for the parameters.
- **The ablation's protocol is ambiguous.** Gates are averaged "and the scalar
  broadcast back at runtime, while keeping the original projections". It
  does not say whether these variants were retrained or are the full model
  evaluated with averaged gates. Neither variant is the tied single-β gate
  that KDA uses, so the b-only row is not a clean KDA-plus-erase comparison.

## Which comparisons are like for like

- **Tables 2–4** retrain every baseline under the same recipe, data, length
  and state budget, in both recurrent and hybrid forms. Within a family the
  rows differ only in the token mixer.
- **The Transformer row** appears only in the hybrid half and has no
  recurrent counterpart, so it is a reference rather than a pair.
- **Hybrid needles at the training length are low for everyone** (Table 3).
  On passkey at 4K every hybrid scores 47–55, while the recurrent models
  score 63–100. The paper does not comment on this. It means the hybrid
  retrieval numbers measure something the 2K window layout does to retrieval
  at this scale, not only the recurrent mixer.

## Standing in the anthology

It extends Kimi Linear's KDA ([LIT-133](LIT-133.md)), whose channel-wise decay it keeps, and
Gated DeltaNet ([LIT-137](LIT-137.md)), which shares two of its three authors. Both are
recovered by tying the new gates, and both were retrained here as baselines,
with KDA trailing at 52.28 and Gated DeltaNet at 52.07 against 53.11. The
paper's Table 1 places them, Mamba-2 ([LIT-162](LIT-162.md)) and Mamba-3 ([LIT-165](LIT-165.md)) in one
fast-weight view. Mamba-2 and Mamba-3 add correlations to a decayed state,
while the delta-rule models write a residual. Under that recipe Mamba-3 MIMO
is the closest recurrent rival (52.39), and SISO is last (51.42).

<!-- inactive-ok-block: SOTA-177 — Proposed, and this paragraph is about
     whether this paper meets its promote_when; its standing is the subject -->
**It bears directly on [SOTA-177](../practices.d/SOTA-177.md).** In Gated Delta Rule-2 the read that is
erased runs along b_t ⊙ k_t while the write runs along k_t. That is an erase
address decoupled from the write address, which is what the Alibaba EDA
paper ([LIT-177](LIT-177.md)) proposed a month later from a different group. Neither paper
cites the other. The forms differ: EDA learns an erase direction of its own,
while here it is restricted to a channel reweighting of the current key.
[SOTA-177](../practices.d/SOTA-177.md) is waiting for "an independent group running an addressed erase
against a channel-wise decay gate". The b-only row of Table 5 is close to
that. It is channel-wise erase on top of KDA's decay, against KDA, and it
gives 52.79 against 52.28 and Wiki 16.12 against 16.81. The caveats are one
run, 1.3B, and the restricted address. The answer it gives to that
practice's open question is that the two remedies stack rather than compete.

For [SOTA-135](../practices.d/SOTA-135.md) it is a further step in the gated delta rule's line, from
the group that introduced it, and evidence about how the gate is parameterized
rather than about whether to have one.

Filed without a NOTE: the takeaways come from one full reading of v1, main
text and Appendices A–E. Fig. 2's throughput curves are quoted only where
the text gives a number.
