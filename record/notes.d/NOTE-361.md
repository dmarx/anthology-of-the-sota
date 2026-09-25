---
number: 361
status: Read
formerly:
- NOTE-tmpr3mtt
paper: LIT-139
title: 'DeepSeek-V4'
version: 1
date: '2026-09-25'
summary: >-
  Two MoE models (1.6T/49B and 284B/13B) reach a native 1M-token context by
  interleaving two compressed attentions — 4x-compressed KV with top-k
  sparse selection (CSA) and 128x-compressed dense KV (HCA), each with a
  128-token sliding-window branch — at 27% of V3.2's per-token FLOPs and 10%
  of its KV cache for Pro at 1M. Multi-token prediction is kept "without
  modification" from V3 as a depth-1 training objective; the report never
  mentions speculative decoding or a draft model.
---

<!-- inactive-ok-file: SOTA-148 — Proposed; V4's load-balancing settings are named against it in Bearing on the record -->
<!-- inactive-ok-file: SOTA-229 — Proposed; named in Bearing on the record as a practice this report does not bear on -->

# NOTE-361: DeepSeek-V4

## Contribution

A preview technical report for two mixture-of-experts language models,
DeepSeek-V4-Pro (1.6T total, 49B activated, 61 layers, 33T tokens) and
DeepSeek-V4-Flash (284B, 13B, 43 layers, 32T tokens), both with a native
one-million-token context. What is new relative to V3/V3.2 is an attention
design built for that length — a hybrid of Compressed Sparse Attention and
Heavily Compressed Attention — together with Manifold-Constrained
Hyper-Connections (mHC) on the residual stream, Muon for most parameters, and
a long list of infrastructure: a fused expert-parallel MoE kernel, TileLang
kernels, batch-invariant and deterministic kernels end to end, a heterogeneous
KV-cache layout with on-disk prefix storage, and FP4 quantization-aware
training in post-training. Post-training replaces V3.2's mixed RL stage with
multi-teacher on-policy distillation over full-vocabulary logits.

## Key insight

The report's thesis is that at a million tokens attention *is* the model's
cost, and that compression along the sequence, not only sparsity, is what
makes it tractable: every `m` (CSA) or `m'` (HCA) tokens' KV become one
learned-weighted entry, CSA then lets a lightning indexer pick the top-k
compressed entries, HCA stays dense over far fewer entries, and a small
uncompressed sliding window restores what the compression cannot see (a
query's own block). Everything else that changes is either carried from V3
"without modification" or is engineering to make that attention trainable
and servable.

## Assumptions

- **This is a model report, not a controlled study.** Almost every design
  choice is stated, not ablated. There is no ablation of CSA vs HCA vs
  either alone, of mHC vs a plain residual, of Muon vs AdamW, of the hybrid
  Newton-Schulz schedule, or of MTP. Comparisons are to DeepSeek-V3.2 and to
  other labs' models under DeepSeek's internal harness.
- The efficiency figures (Fig. 1 right; §1) are **estimated** single-token
  inference FLOPs "measured in equivalent FP8 FLOPs" and accumulated KV-cache
  size, not measured serving throughput or latency.
- The baseline for the "~2% of KV cache" figure is BF16 GQA8 with head
  dimension 128 at 1M context (§2.3.4).

## Key results

- **Configuration (§4.2.1).** Flash: 43 layers, d = 4096, first two layers
  pure sliding-window attention, then CSA/HCA interleaved; CSA m = 4, top-k
  512, 64 indexer heads of dim 128; HCA m' = 128; 64 query heads of dim 512;
  window n_win = 128; 1 shared + 256 routed experts, 6 active; first 3 MoE
  layers hash-routed; **MTP depth 1**; mHC n_hc = 4, 20 Sinkhorn-Knopp
  iterations. Pro: 61 layers, d = 7168, first two layers HCA; top-k 1024; 128
  query heads; 384 routed experts, 6 active; **MTP depth 1**.
- **Multi-token prediction (§2, §2.1, §4.2.2).** "The Multi-Token Prediction
  (MTP) configuration remains identical to that of DeepSeek-V3"; "Given that
  the MTP strategy has been validated in DeepSeek-V3, we adopt the same
  strategy for DeepSeek-V4 series without modification." Fig. 2 shows MTP
  modules producing an MTP loss beside the LM loss. The MTP loss weight is
  0.3 for most of training and 0.1 from the start of learning-rate decay, for
  both models. That is the whole of what the report says about MTP. **The
  words "speculative", "draft" and "acceptance" do not occur**; no section
  describes using the MTP module at inference, fine-tuning it into a draft
  model, or any decode-speed figure attributable to it. The inference
  framework "largely inherits from that of DeepSeek-V3, with some differences
  in KV Cache management" (§3.5), and the only inference topics treated are
  KV-cache layout and on-disk prefix reuse. EAGLE (Li et al., 2024) appears
  in the report only as one of four citations attached to the phrase
  "Multi-Token Prediction (MTP)" in §2.
- **Efficiency (§1, Fig. 1).** At 1M tokens, Pro needs 27% of V3.2's
  single-token FLOPs and 10% of its KV cache; Flash 10% and 7%. Mixed KV
  storage (BF16 for the 64 RoPE dimensions, FP8 for the rest) roughly halves
  KV size against pure BF16; the indexer's attention runs in FP4; a smaller
  top-k than V3.2 helps short and medium contexts (§2.3.4).
- **Attention details (§2.3.3).** RMSNorm on each query head and on the
  single compressed-KV head before core attention, which "avoids exploding
  attention logits"; for that reason "we do not employ the QK-Clip technique"
  (§2.4). Partial RoPE on the last 64 dimensions, with RoPE at position −i
  applied to the attention output so it carries relative position; learnable
  per-head attention-sink logits; grouped output projection.
- **Muon (§2.4, Algorithm 1).** Muon for all but the embedding, prediction
  head, mHC static biases and gating factors, and RMSNorm weights (AdamW
  there). Weight decay 0.1, momentum 0.95, Nesterov, update RMS rescaled to
  0.18. Hybrid Newton-Schulz: 8 steps with (3.4445, −4.7750, 2.0315) then 2
  with (2, −1.5, 0.5).
- **Load balancing (§2.1, §4.2.2).** Auxiliary-loss-free bias at update
  speed 0.001 plus a sequence-wise balance loss at weight 0.0001; affinity
  activation changed from Sigmoid to Sqrt(Softplus); node-limited routing
  removed.
- **Schedule (§4.2.2).** Sequence length 4K → 16K → 64K → 1M; dense
  attention for the first 1T tokens (Flash; Pro's dense stage is longer),
  sparse attention introduced at 64K after a short indexer warm-up.
  Batch ramps to 75.5M (Flash) and 94.4M (Pro) tokens. Peak LR 2.7e-4
  (Flash) and 2.0e-4 (Pro), cosine-decayed to a tenth at the end.
- **Stability (§4.2.3).** Loss spikes traced to MoE outliers. Two fixes,
  explicitly without a theory: *Anticipatory Routing* (routing indices
  computed with parameters from Δt steps earlier, triggered automatically on
  a spike, ~20% wall-clock overhead while active) and *SwiGLU clamping*
  (linear part to [−10, 10], gate capped at 10).
- **FP4 QAT (§5.2.1).** In post-training only: MXFP4 for MoE expert weights
  and the CSA indexer's QK path; FP4→FP8 dequantization is lossless under a
  scale-ratio condition the authors verify empirically; index scores
  FP32→BF16 give a 2x faster top-k selector at 99.7% recall.
- **Infrastructure (§3).** Fused wave-scheduled EP kernel: 1.50–1.73x over
  non-fused baselines on general inference, up to 1.96x for latency-sensitive
  cases; mHC wall-time overhead held to 6.7% of a 1F1B stage.
- **Evaluations (§4.3, §5.3).** Base models: V4-Flash-Base beats
  V3.2-Base on most of Table 1 with fewer parameters. Chat: V4-Pro-Max
  reports e.g. SimpleQA-Verified 57.9, HLE 37.7, Codeforces 3206, SWE
  Verified 80.6, MRCR 1M 83.5 (Table 6), with MRCR stable to 128K and
  degrading beyond (Fig. 9).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | V4 keeps V3's MTP module and objective unchanged, at depth 1, with loss weight 0.3 then 0.1 at LR decay | strong (as a statement of what was done) | §2, §2.1, §4.2.1, §4.2.2 — stated repeatedly; no ablation |
| C2 | V4 uses its MTP module for speculative decoding at inference | **none** | not stated anywhere in the report; no draft, acceptance rate or decode speed-up is reported |
| C3 | At 1M context V4-Pro needs 27% of V3.2's per-token FLOPs and 10% of its KV cache (Flash: 10%, 7%) | moderate | Fig. 1 right, §1; estimated FP8-equivalent FLOPs and computed cache size, not measured throughput |
| C4 | RMSNorm on queries and compressed KV entries prevents exploding attention logits, making QK-Clip unnecessary | weak-to-moderate | §2.3.3, §2.4; stated as an architectural consequence and supported by the run completing, no ablation or logit trace shown |
| C5 | V4-Flash-Base outperforms V3.2-Base on most base benchmarks with fewer total and activated parameters | moderate | Table 1, one internal harness; data, architecture and optimizer all changed at once |
| C6 | Anticipatory Routing and SwiGLU clamping eliminate V4's loss spikes without hurting performance | weak | §4.2.3; practitioner report, "comprehensive theoretical understanding ... remains an open question"; no curves or ablations |
| C7 | FP4 QAT on expert weights and the indexer QK path costs little: index-score BF16 keeps 99.7% KV recall at 2x top-k speed | moderate for the recall figure, weak for end quality | §5.2.1; no before/after quality comparison for the weight quantization |
| C8 | The fused EP kernel gives 1.50–1.73x on general inference and up to 1.96x in latency-sensitive settings | moderate | §3.1; against "strong non-fused baselines", on two hardware platforms, figures summarised rather than tabulated |

## Concepts

- **CSA (Compressed Sparse Attention)** — KV compressed m:1 by softmax-weighted
  pooling over two overlapping projected streams (each entry draws on 2m
  tokens), then DSA-style top-k selection by a lightning indexer, then
  shared-KV MQA with a sliding-window branch.
- **HCA (Heavily Compressed Attention)** — non-overlapping m':1 compression
  (m' = 128) with dense attention over all compressed entries, plus the same
  sliding-window branch.
- **MTP depth** — the number of additional future tokens predicted by
  sequential MTP modules; 1 here, as in V3.
- **Anticipatory Routing** — computing a step's routing decisions with
  parameters from Δt steps earlier, decoupling router and backbone updates.

## Connections

The DeepSeek line in the record: V3 ([LIT-160](../literature.d/LIT-160.md)) is the source of the MTP
configuration, the auxiliary-loss-free balancing and the inference framework
V4 inherits; V3.2's DeepSeek Sparse Attention ([LIT-142](../literature.d/LIT-142.md)), itself after NSA
([LIT-143](../literature.d/LIT-143.md)), is the selection step inside CSA; mHC is [LIT-140](../literature.d/LIT-140.md); the Muon
recipe follows Moonshot ([LIT-122](../literature.d/LIT-122.md)) except for the Newton-Schulz schedule and
the absence of QK-Clip. MTP itself traces to Gloeckle et al. ([LIT-163](../literature.d/LIT-163.md)), which
V4 cites alongside ProphetNet, EAGLE and V3.

## Recommendations

- **R1** — Normalise queries and keys (here: RMSNorm per query head and on
  the compressed KV) before the logit rather than clipping weights after the
  fact. *Topic:* model stability. *Status:* standard at this lab.
  *Strength:* weak (no ablation). *Applies when:* the attention architecture
  exposes the query and key inputs to a norm.
- **R2** — When a long-context model compresses KV per block, add an
  uncompressed sliding window so a query can see its own block. *Topic:*
  attention. *Status:* experimental. *Strength:* weak (argued from causality,
  not ablated). *Applies when:* compression blocks are larger than one token.
- **R3** — Anneal the MTP auxiliary loss weight at LR decay (0.3 → 0.1).
  *Topic:* training objective. *Status:* standard at this lab (inherited from
  V3). *Strength:* weak (no ablation here).

## Bearing on the record

- **[LIT-185](../literature.d/LIT-185.md)'s claim that this model ships the EAGLE-3 arrangement is not
  supported.** Its standing section said [LIT-135](../literature.d/LIT-135.md) and this paper "ship the same
  arrangement" as Kimi K3 — the MTP head fine-tuned into a single-layer draft
  model. The full report says only that V4 keeps V3's MTP module unchanged
  as a training objective (C1); it says nothing about drafting or
  speculative decoding (C2). Whether DeepSeek serves V4 speculatively, as it
  may have V3, is not something this report states, and "the inference
  framework largely inherits from that of DeepSeek-V3" cannot carry it: the
  sentence is about KV-cache management. [LIT-185](../literature.d/LIT-185.md), [SOTA-227](../practices.d/SOTA-227.md) and [LIT-163](../literature.d/LIT-163.md)
  are corrected alongside this reading.
- **[SOTA-162](../practices.d/SOTA-162.md)** (MTP heads) — V4 is an adopter, correctly listed, and its
  report states only the *training* motive: an auxiliary loss with an
  annealed weight, no inference use. [SOTA-162](../practices.d/SOTA-162.md) is qualified accordingly. That is a point
  for the practice's "double motive, which nobody has separated", not
  against it; it still ablates nothing.
- **[SOTA-227](../practices.d/SOTA-227.md)** (speculative decoding) — no bearing; this report is not an
  adopter of record. [SOTA-229](../practices.d/SOTA-229.md) likewise.
- **[SOTA-131](../practices.d/SOTA-131.md)** (QK-Clip) — confirms what [LIT-139](../literature.d/LIT-139.md) already records: a Muon
  run at 1.6T without QK-Clip, relying on q/KV RMSNorm instead (C4).
- **[SOTA-139](../practices.d/SOTA-139.md)** (staged context extension) — confirmed: 4K → 16K → 64K → 1M,
  with sparse attention introduced partway.
- **[SOTA-148](../practices.d/SOTA-148.md)** (bias-based balancing) — V4 runs the bias at 0.001 *plus* a
  0.0001 sequence-wise loss, as [LIT-139](../literature.d/LIT-139.md) records.
- **[SOTA-121](../practices.d/SOTA-121.md)** (Muon with AdamW-matched RMS) — adopter; RMS target 0.18.

## Limitations

The report is a "preview" and its own conclusion concedes the architecture
retains "many preliminarily validated components and tricks" to minimise
risk and is "relatively complex"; which of them carry weight is exactly what
it does not test. Its stability fixes are offered without understanding. The
efficiency headline is estimated, not measured end-to-end. Several external
comparisons have gaps where competitors' APIs "were too busy to return
responses".

## Open questions

- Is V4 served with MTP-based speculative decoding? Only DeepSeek's serving
  code or a statement elsewhere (e.g. the V3 report, [LIT-160](../literature.d/LIT-160.md), for the
  predecessor) could settle it; this report does not.
- How much of the 1M-context quality comes from CSA vs HCA vs the sliding
  window, and what does each cost at short context?
- Do Anticipatory Routing and SwiGLU clamping address the same outlier
  mechanism, and is either sufficient alone?
