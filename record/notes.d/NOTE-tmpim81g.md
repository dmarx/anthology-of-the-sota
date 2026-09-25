---
status: Read
paper: LIT-tmpbukux
title: 'Attention-only transformers'
version: 1
date: '2026-09-25'
summary: >-
  A necessity test of the feed-forward layer with three matchings. Deleting
  it in place costs 0.47 nats. At matched FLOPs the cost is 0.26 nats. At
  matched parameters, with the budget moved into attention depth, the cost is
  0.0055 nats, and it shrinks with tokens. What remains is concentrated on
  low-context tokens, where recall has to come from the weights. QK-norm is
  what keeps the attention-only stack trainable. At or below 87M parameters,
  on a synthetic reasoning corpus.
---

# NOTE-tmpim81g: Attention-only transformers

## Contribution

This is the first necessity test of the transformer FFN that controls
parameters, FLOPs and depth separately. It uses per-arm learning-rate sweeps
and a calibrated noise floor, and one prediction was registered numerically
before its run. It turns "FFNs store facts", which probing and editing had
established by localization, into a measured price for deleting them: about
0.006 nats at matched parameters on this corpus, concentrated where
parametric recall is needed.

## Key insight

The FFN's *parameters* matter and its *functional form* largely does not. Give
the same parameter budget to attention depth and nearly everything comes back,
except prediction on tokens the context cannot help with. The storage the FFN
provided moves to the attention output projection, the only remaining write
path.

## Assumptions

- Decoder-only, `d = 512`, GQA 8Q/4KV, RoPE, zero-centred RMSNorm, pre-norm,
  QK-norm, scalar sigmoid residual gates, tied embeddings. The control arm
  adds a SwiGLU FFN with `d_ff = 4d` behind its own gate.
- Muon is the main optimizer, with an AdamW control, a WSD schedule, and 1.05M
  tokens per step at 2048 context.
- **Data: SYNTH**, a 68B-token synthetic reasoning corpus trained for up to 1.5
  epochs, plus one fineweb-edu pair at 31.5B tokens. Everything is at or below
  87M total parameters and 105B tokens.
- The formal results (conditional linearity, simplex transport, the
  scalar-bottleneck lemma, bounded stream variance at init) hold for the SAN
  block as defined. The authors note the proof's gate hypothesis turned out
  dispensable in practice.

## Key results

- **Headline (Table 3).** SAN 2.0685 ± 0.0028, three seeds. FFN iso-param
  2.0812 ± 0.0230, which becomes 2.0650 ± 0.0006 without the unstable seed.
  FFN iso-FLOP 1.8059 and iso-depth 1.5982. The clean-pair paired Δ is
  +0.0055 and +0.0054, and the same-seed floor is 0.0015.
- **Token axis.** Δ is 0.046 at 5B, 0.019 at 30B and 0.0055 at 105B, each
  budget trained and tuned separately.
- **Size axis at 31.5B tokens.** Δ is −0.045 at the smallest pair, where the
  2-layer FFN arm is depth-limited, then about +0.02 from 16M to 57M
  non-embedding parameters.
- **Repetition.** Up to 18 epochs costs 0.010 nats or less, with no
  architecture × repetition interaction.
- **Regions (Table 4).** On the training-exposed sample, query tokens are
  5.8% of tokens and 7.9% of loss. Their Δ is +0.052 at 31B and +0.038 at
  105B, while trace and answer regions go negative by 105B.
- **Registered OOD test.** On fineweb-edu the prediction was 0.02–0.05 nats
  and the measurement 0.0398. There lambada reverses, SAN 0.203 against FFN
  0.181.
- **Ablations (Table 6).** Without QK-norm the run diverges (8.28). Sandwich
  norm −0.0092. Standard residual −0.0013. ReZero residual +0.0032. No
  residual +0.75. Gates are neutral at 8, 20, 32 and 48 layers and in the FFN
  arm.
- **Optimizer.** A 5B-token crossover, where each architecture prefers a
  different optimizer, is gone by 30B, with within-architecture Δ ≤ 0.002.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | At matched parameters, an attention-only decoder trails a standard one by ~0.006 nats on this corpus at 105B tokens | strong | Table 3, two clean seed pairs agreeing to 1e-4, 3.7× the noise floor, per-arm LR sweeps; third pair excluded for a documented instability |
| C2 | Deleting the FFN in place, or at matched FLOPs, costs a lot (0.47 / 0.26 nats) | strong | Table 3, single runs, but margins are enormous |
| C3 | The iso-param gap shrinks with training tokens | moderate | three separately trained budgets, at one size only |
| C4 | The residual gap is parametric recall on low-context tokens | moderate | three measurements agree; region decomposition is on a training-exposed sample with point estimates only; one pre-registered OOD confirmation |
| C5 | QK-normalization is what keeps deep attention-only stacks trainable | weak | one ablation run diverging at the tuned rate, 20 layers; scoped by the authors to that rate |
| C6 | Scalar residual gates (and ReZero residuals) are performance-neutral | moderate | Table 6 and Figure 8, 8–48 layers and both arms; single runs, differences within ~2 noise floors |
| C7 | Q/K spectra crystallize early while content-writing matrices accumulate rank; removing the FFN moves the accumulation to `W_o` | moderate | stable-rank trajectories across all trained models (Figure 5) |
| C8 | Sandwich normalization improves the attention-only stack | weak | one run, −0.0092 nats, ~6× the floor |

## Concepts

- **SAN** (Simple Attention Network) is a pre-norm attention block with the FFN
  deleted and nothing put back.
- **Iso-param / iso-FLOP / iso-depth** name the control standard transformer
  matched to the SAN on total parameters, training FLOPs per token, or layer
  count.
- **Query region** is the span of a SYNTH document before its reasoning
  trace. It has the least context to route from.

## Connections

It is the causal complement of the FFN-as-memory line (Geva, ROME and
knowledge neurons, none held here) and the attention-only side of the
MLP-Mixer/gMLP ablation. It uses QK-norm (LIT-640), ReZero-style residuals
(LIT-047) and sandwich norm (NormFormer, not held), and it runs Muon against
AdamW. The mechanistic attention-only models of LIT-543 are two-layer and
analytic, while this study's run to 48 layers.

## Recommendations

- **R1** — When comparing two architectures that differ in parameters, FLOPs
  and depth together, report all three matchings and tune the learning rate
  per arm. A shared rate "silently biases any comparison" here by 2× in the
  optimum. *Topic:* analysis-and-evaluation. *Status:* standard. *Strength:*
  moderate. *Applies when:* any architecture ablation.
- **R2** — In an attention-only stack, keep QK-norm. *Topic:* model-stability.
  *Status:* experimental. *Strength:* weak (one run). *Applies when:* deep
  stacks without FFNs.

## Bearing on the record

- **SOTA-192 (QK-norm).** Corroborates from a new architecture. It is one
  ablation run at one learning rate and ≤ 24M parameters, and it is recorded
  as a data point, not added as a source.
- **SOTA-051 (zero-init residual branch).** The ReZero residual is neutral
  here, with normalization kept. It does not contradict the practice. It
  shows that the scalar adds nothing measurable when normalization and
  `1/(2N)` output scaling are already present.
- **SOTA-403 (share attention, not FFN).** Relevant only to its mechanism
  paragraph. Deleting the FFN costs mostly parametric recall, which fits the
  storage account the practice calls a coincidence of premise. Deletion is
  not sharing, so the split is untested.
- **SOTA-034 (SwiGLU).** Not bearing. The control arm uses SwiGLU and never
  varies the activation.
- It does **not** support dropping FFNs in any practice. At matched parameters
  the SAN costs about 2× the FLOPs per token, and iso-FLOP favours the FFN by
  0.26 nats.

## Limitations

The authors name these limits themselves. Everything is at or below 87M
parameters and 105B tokens, on one reasoning-dense corpus and one web-text
pair, and MMLU-class benchmarks are at chance. Size-flatness and token
convergence are each measured on one slice. Their conjunction at scale is
extrapolation. The region decomposition has no intervals. Two of eight
registered predictions failed, and the central localization finding came out
of one of those failures. It was revised after the fact and then confirmed by
one pre-registered point. The headline iso-param comparison excludes a
third seed pair whose sign reverses.

## Open questions

The storage account predicts a wider gap on storage-heavy mixtures at larger
scale, and nobody has run that. Does QK-norm's necessity hold at other
learning rates and in standard stacks? Is sandwich norm's −0.009 real beyond
one run?
