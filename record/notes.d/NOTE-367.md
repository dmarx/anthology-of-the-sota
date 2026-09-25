---
number: 367
status: Read
formerly:
- NOTE-tmpeqzam
paper: LIT-711
title: 'Narang et al., transformer modifications'
version: 1
date: '2026-09-25'
summary: >-
  About fifty transformer modifications reimplemented in one T5/Mesh TensorFlow codebase
  at 223M parameters, with hyperparameters fixed, on four task families. Most
  do not beat the vanilla pre-norm, relative-attention baseline. The winners
  are GLU-variant activations, RMSNorm, untied embeddings, and sparse experts
  or other variants that cost parameters or time. The Universal Transformer,
  ReZero, Fixup, block sharing and the Evolved Transformer all lose. The
  positives are largely same-codebase re-runs, GLU Variants included, so the
  paper is strong evidence against the losers and weak evidence that the
  winners transfer.
---

<!-- inactive-ok-file: SOTA-403 — Proposed; named as a practice this paper bears on without settling, and its status is not relied on -->
<!-- inactive-ok-file: SOTA-190 — Proposed; named as a practice this paper bounds without confirming, and its status is not relied on -->

# NOTE-367: Narang et al., transformer modifications

## Contribution

A shared-codebase audit of roughly fifty published transformer modifications.
The categories are activations, normalization and initialization, depth versus
width, embedding tying and factorization, cross-layer parameter sharing,
softmax variants, and whole-architecture alternatives: Transparent attention,
the Evolved Transformer, Synthesizer, Funnel, lightweight and dynamic
convolution, MoE, Switch, product-key memory and the Universal Transformer.
All of them run under one training recipe and one set of evaluations. Before
it, each of these carried only its proposer's numbers. After it, the record
holds a common yardstick, and on that yardstick most of them lose to the
baseline.

## Key insight

Held to fixed hyperparameters in a strong codebase, most architecture
modifications do not reproduce their gains. The ones that survive are small,
more expensive, or native to the codebase they were tested in. A published
gain is therefore partly a fact about the paper's implementation, and a
reimplementation is the test that separates the two. It separates them only
when the reimplementation is independent, and for the winners here it mostly
is not.

## Assumptions

- **One implementation.** Mesh TensorFlow, the T5 codebase. The paper's
  conjecture is about transfer *across* implementations, yet it runs only
  one.
- **Fixed hyperparameters.** Adafactor, an inverse-square-root schedule, no
  pre-training regularization, dropout 0.1 during fine-tuning. The one
  exception is ReZero and Fixup, moved to Adam because they did badly under
  Adafactor. The authors defend fixed settings on the ground that a useful
  modification should be hyperparameter-agnostic. That is a design choice
  and handicaps variants that need retuning, as §3.2 shows for the Universal
  Transformer.
- **Encoder-decoder, 223M, 2020-era.** Nothing is decoder-only and nothing is
  above about 1B total parameters. The record's practices mostly assume
  decoder-only models at far larger scale.
- **Matching is approximate.** Parameters or FLOPs are held, not both, and
  MoE, Switch and product-key memory carry 3–5× the parameters. The Universal
  Transformer runs at 4× the FLOPs, and product-key memory reports inflated
  FLOPs from an inefficient implementation.

## Key results

- **Activations.** SwiGLU reaches early loss 2.127 ± 0.003 against 2.182 ±
  0.005, final loss 1.789 against 1.838, and SGLUE 76.00 against 71.66 at the
  same speed. GeGLU and ReGLU are close. ELU and SeLU are worse. Under learned
  positions (Table 2) SwiGLU 2.168 still beats 2.245.
- **Normalization.** RMSNorm gives 2.167 ± 0.008 and 1.821, and 3.68 steps/s
  against 3.50, about 5%. Under learned positions it gives 2.209 against
  2.245 and runs about 2% faster, but it loses on SuperGLUE and WebQuestions.
  ReZero: 2.262. ReZero + LN: 2.223. Fixup: 2.382.
- **Depth at 223M.** Final losses: 18L 1.831, 12L 1.838, 24L 1.843, 8L 1.847,
  6L 1.857. Steps/s falls with depth. Under learned positions every depth
  variant loses to the baseline.
- **Sharing.** All-shared blocks give 2.497 at 65M. Encoder-only sharing
  gives 2.298 and decoder-only 2.352. Sharing hurts everywhere it was tried.
- **Embeddings.** Untying encoder from decoder embeddings helps modestly, and
  factorized embeddings hurt.
- **Sparse layers.** MoE gives 2.148 (648M) and Switch 2.135 (1.1B) at about
  the same FLOPs, about 9% slower per step.
- **Universal Transformer.** 2.40, and 2.265 after 25 tuning runs, still worse
  than 2.182.
- **Correlation.** Spearman ρ between pre-training loss and task score is 0.87
  for SuperGLUE, 0.80 for XSum and 0.69 for WebQuestions.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Most published transformer modifications do not improve on a well-tuned vanilla baseline in this codebase at fixed hyperparameters | strong | Table 1, ~50 variants, 5-seed early loss and four downstream task families; replicated in direction under learned positions (Table 2) |
| C2 | SwiGLU and GeGLU improve pre-training, fine-tuning and supervised translation at no speed cost | moderate | Table 1 and Table 2; effect well outside seed std. Not independent of [LIT-030](../literature.d/LIT-030.md), which ran the same codebase and configuration |
| C3 | RMSNorm improves quality and speed over LayerNorm | moderate | Table 1 loss and step/s; under learned positions (Table 2) loss improves but SuperGLUE and WebQuestions do not, and the speedup is ~2–5%, not 7–64% |
| C4 | Deeper models outperform shallower ones at fixed parameter count | weak | the §3.1 sentence; Table 1 is non-monotone (24L worse than 12L on final loss), Table 2 has every depth variant worse than baseline |
| C5 | ReZero, Fixup and cross-layer block sharing hurt | strong | Table 1 and Table 2, large margins; ReZero/Fixup even given a different optimizer |
| C6 | The Universal Transformer does not match the vanilla Transformer even after tuning | moderate | §3.2, 25 configurations, one task (pre-training loss) |
| C7 | Sparse-expert layers (MoE, Switch) improve quality at roughly matched FLOPs | moderate | Table 1; but both invented in this codebase, and step/s drops ~9% |
| C8 | Modifications do not transfer across implementations and applications | weak | argument by elimination plus non-adoption; only one implementation is run |
| C9 | Pre-training perplexity correlates with fine-tuned quality, more weakly for knowledge-intensive QA | moderate | Figure 1, Spearman ρ across variants |

## Concepts

- **Vanilla Transformer** here means the original architecture with pre-norm
  and shared relative-attention biases, not Vaswani et al. as published.
- **Early loss** is the mean ± std of held-out C4 log-perplexity over 5 runs
  at 65,536 steps, one-eighth of pre-training. **Final loss** is a single run
  at 524,288 steps.

## Connections

Reimplements and scores work the record holds: GLU Variants ([LIT-030](../literature.d/LIT-030.md)) and its
GLU origin ([LIT-199](../literature.d/LIT-199.md), as "GLU"), RMSNorm ([LIT-023](../literature.d/LIT-023.md)), ReZero ([LIT-047](../literature.d/LIT-047.md)), the
sparsely-gated MoE ([LIT-188](../literature.d/LIT-188.md)), Switch ([LIT-189](../literature.d/LIT-189.md)), ALBERT's sharing and
factorized embeddings ([LIT-668](../literature.d/LIT-668.md)), and lightweight/dynamic convolution
([LIT-020](../literature.d/LIT-020.md)). Its baseline is the T5 recipe ([LIT-425](../literature.d/LIT-425.md)). The Universal Transformer,
the Evolved Transformer, Synthesizer, Funnel, product-key memory and Fixup are
not held.

## Recommendations

- **R1** — When claiming an architecture gain, test it in a second, unrelated
  codebase and on more than one task family. Report mean and std over seeds.
  *Topic:* analysis-and-evaluation. *Status:* standard. *Strength:* moderate
  (argued, with this paper as the negative example). *Applies when:* proposing
  or adopting an architecture change.
- **R2** — Default to a GLU-variant FFN and RMSNorm. Do not adopt ReZero in
  place of normalization, Fixup, or full cross-layer sharing on a published
  gain alone. *Topic:* model-architecture. *Status:* standard. *Strength:*
  moderate. *Applies when:* dense transformer pre-training.

## Bearing on the record

- **[SOTA-034](../practices.d/SOTA-034.md) (SwiGLU).** The gain reproduces with five seeds and on all four
  task families. The re-run is in [LIT-030](../literature.d/LIT-030.md)'s own codebase and configuration, so
  it corroborates the measurement, not its transfer. The practice now says so.
- **[SOTA-182](../practices.d/SOTA-182.md) (RMSNorm).** Loss reproduces. The speedup is about 2–5% here,
  against 7–64% in [LIT-023](../literature.d/LIT-023.md), and downstream wins do not survive the switch to
  learned positions. The practice now says so.
- **[SOTA-150](../practices.d/SOTA-150.md) (MoE).** The quality gain at matched FLOPs reproduces, in the
  codebase MoE and Switch were built in, at about 9% lower step rate. Added.
- **[SOTA-051](../practices.d/SOTA-051.md) (ReZero).** ReZero *as a replacement for LayerNorm* fails
  badly here, which bounds [LIT-047](../literature.d/LIT-047.md)'s claim that the normalization and warmup
  of deep stacks become unnecessary. The practice's own use of the zero-init
  principle (adapters, ControlNet) is not tested. Added.
- **[SOTA-403](../practices.d/SOTA-403.md) (share attention, not FFN).** The split is not tested. What is
  tested is all-shared, encoder-only and decoder-only sharing, and all three
  hurt. The Universal Transformer's reported gain, which the practice cites
  as pointing the other way, does not reproduce even after tuning. Added.
- **[SOTA-190](../practices.d/SOTA-190.md) (depth first).** The depth sweep is non-monotone and slower with
  depth. It neither confirms nor contradicts at this scale. Tay is an author of
  both papers, so this is not the outside group `promote_when` asks for. Added
  as a bound.
- **[SOTA-032](../practices.d/SOTA-032.md) (pre-norm).** Not evidence. Pre-norm is the untested baseline,
  justified by adoption.

## Limitations

One codebase, which the authors' own conjecture says is the thing that
matters. Fixed hyperparameters penalize variants that need retuning. Only
encoder-decoder models at 223M are tested. The final loss is a single run. The
text gives vanilla SuperGLUE as 70.97 and Table 1 gives 71.66. The
downstream scores are noisy: every depth variant beats the baseline on
SuperGLUE, by up to 4.8 points, while their losses straddle it. Read
SuperGLUE differences of a few points as within noise.

## Open questions

Does the negative result hold in a second codebase, in decoder-only models
and at scale? Nobody has rerun the audit. Do the winners transfer? That needs
exactly what the paper recommends and does not do: the same variants in an
unrelated implementation.
