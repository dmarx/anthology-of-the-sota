---
number: 194
status: Read
formerly:
- NOTE-tmp4v78r
paper: LIT-444
title: 'Small Batch Size Training for Language Models'
version: 1
date: '2026-09-20'
summary: >-
  Small batches look unstable because `beta_2` is held fixed while the batch
  changes. Hold the second moment's half-life fixed in tokens instead and
  batch size one trains stably, matches larger batches per FLOP, is far more
  robust to hyperparameters, and lets momentum-free SGD match AdamW at 1.3B.
---

# NOTE-194: Small Batch Size Training for Language Models
<!-- inactive-ok-file: SOTA-097 — Superseded in this same change; named among the practices that assume a large batch is the target -->
<!-- inactive-ok-file: SOTA-062 — Superseded in this same change; named in the same list -->

## Contribution

Shows that the instability attributed to small batches is an artifact of
leaving Adam's second-moment decay rate at its default while the batch size
changes, and gives the one-line reparameterization that removes it. With that
in place, batch size one is not merely survivable but *preferable* on several
axes — per-FLOP loss, robustness to hyperparameter misspecification, memory,
and tolerance of simpler optimizers. The corollary is a recommendation against
gradient accumulation for most practitioners, which contradicts standard
practice directly.

## Key insight

**`beta_2` is a rate per optimizer step, and an optimizer step is not a fixed
amount of data.** Holding `beta_2 = 0.95` while shrinking the batch by 512×
shortens the second moment's averaging window, measured in tokens, by the same
factor — so the variance estimate is computed over far too little data and the
updates become erratic. Nothing about small batches is unstable; what is
unstable is a hyperparameter whose unit nobody wrote down. Once the decay is
expressed as a half-life in tokens and held fixed, the whole "large batches
are more stable" edifice collapses, and with it the case for gradient
accumulation and for optimizers whose advantage was robustness at large
batch.

## Assumptions

- **Batch size is a free choice.** The setting is one where a small batch can
  actually be run — which excludes the multi-device sharded regime where the
  global batch is set by the topology.
- **Throughput floor**: the recommendation to use the smallest batch assumes
  at least a few hundred tokens per device, below which memory bandwidth
  rather than compute binds.
- Most models are trained at roughly Chinchilla's 20 tokens per parameter; the
  1.3B run is the exception at about 10.
- The scaling rule `beta_2' = beta_2^(B'/B)` follows from holding
  `t_half = B·ln2 / ln(1/beta_2)` constant, which assumes the useful averaging
  window is a quantity of data rather than a count of steps.
- Weight decay is turned off in the batch-size-1 configurations rather than
  rescaled, so the reported comparisons hold `λ` out of the picture.

## Key results

- **Batch size 1 trains stably** for pretraining and fine-tuning once `t_2` is
  held fixed. *Holds when:* the half-life rule is applied; with `beta_2` fixed
  instead, small batches underperform badly.
- **`beta_1`'s usual default works across batch sizes**; it is specifically
  `beta_2` that must move.
- **Optimizer choice stops mattering at small batch.** At batch size 1, SGD,
  Adafactor, Adam and Muon reach similar loss on a 30M model; the spread grows
  with batch size.
- **GPT-3 1.3B, vanilla SGD, no momentum, batch size 1, no optimizer state**
  matches the AdamW configuration from Brown et al. at batch 512. Adam and
  Adafactor at batch 1 beat it.
- **GPT-2 124M**: after per-optimizer learning-rate tuning, Adam and Adafactor
  at batch 1 match AdamW at batch 512; SGD is slightly worse.
- **Robustness**: the loss surface over learning rate and `beta` is markedly
  flatter at batch 1 than at batch 512, so less tuning is needed.
- **Square-root learning-rate scaling overshoots**: from batch 1 to 1024 the
  rule prescribes 32×, and about 3× worked better.
- **Fine-tuning** Gemma 3 4B on MATH: batch 1 with the half-life rule compared
  against batch 16 and against LoRA, at matched memory footprint, 8 seeds, 8
  learning rates.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Small-batch instability is an artifact of holding `beta_2` fixed rather than the second moment's half-life in tokens | strong | direct comparison of the two scaling choices across batch sizes, and the reproduction of a prior paper's negative small-batch result followed by its removal |
| C2 | Batch size one matches or beats large batches per FLOP | moderate | 30M sweeps plus 124M and 1.3B checks; the 1.3B run is under-trained and uses an untuned baseline |
| C3 | Small batches are more robust to hyperparameter choice | strong | the loss surface is visibly flatter across two independent hyperparameters |
| C4 | Vanilla SGD without momentum is competitive at small batch | moderate | one 1.3B comparison against one baseline configuration |
| C5 | Gradient accumulation is wasteful except when bottlenecked on inter-device bandwidth | moderate | follows from C1–C3 plus the memory cost of accumulated gradients; not separately measured |

## Method

Express Adam's decay rates as half-lives in tokens:
`t_half = B · ln(2) / ln(1/beta)`. Sweep learning rate, `beta_1`, `beta_2` and
`t_2` independently across batch sizes from 1 to 1024 on a 30M model, and
compare holding `beta_2` fixed against holding `t_2` fixed.

Validate at 124M and 1.3B against published baseline configurations, with the
batch-1 arm given no tuning beyond the one-shot rule. Compare four optimizers
across the batch-size range. Repeat on a fine-tuning task with memory
footprint as the comparison axis.

## Concepts

- **Moment half-life `t_half`** — the number of *tokens* after which a
  mini-batch gradient's contribution to an Adam moment has decayed by half.
  The batch-size-invariant form of a decay rate.
- **`t_1`, `t_2`** — the half-lives of the first and second moments, standing
  in for `beta_1` and `beta_2`.
- **Gradient accumulation** — summing gradients over successive micro-batches
  before one optimizer step. Note it *increases* memory over a genuinely small
  batch, because the accumulated gradient must be stored.
- **Smallest batch that maximizes throughput** — the recommended target: as
  small as possible subject to saturating the device, which in practice means
  not falling below a few hundred tokens per device.

## Connections

Sits against the whole large-batch tradition the record files under
[SOTA-097](../practices.d/SOTA-097.md), [SOTA-062](../practices.d/SOTA-062.md), [SOTA-093](../practices.d/SOTA-093.md) and [SOTA-198](../practices.d/SOTA-198.md), all of which ask how large a
batch may usefully be. It is not a contradiction of the critical-batch-size
line — `B_crit` is a ceiling, this is an argument about where to sit below it
— but it is a contradiction of the assumption they share, that you want to be
near the ceiling.

The reparameterization is the same move [LIT-443](../literature.d/LIT-443.md) makes for weight
decay through the AdamW timescale: a copied constant turns out to be a ratio
with an implicit denominator, and naming the denominator makes the constant
transferable. Two papers, two hyperparameters, one lesson — which is worth
more than either result.

Also connects to the memory-efficient fine-tuning line: batch size 1 with
full fine-tuning is compared against LoRA at matched memory, which is the
comparison LoRA is usually spared.

## Recommendations

- **R1** — Choose the smallest batch size that still maximizes throughput or
  MFU, rather than the largest that fits. *Topic:* batch size. *Status:*
  experimental. *Strength:* moderate. *Applies when:* batch size is a free
  choice and the model fits on a device.
- **R2** — When changing batch size, hold Adam's second-moment half-life in
  tokens fixed rather than `beta_2`: `beta_2' = beta_2^(B'/B)`. Leave
  `beta_1` alone. *Topic:* optimizer hyperparameters. *Status:*
  experimental. *Strength:* strong. *Applies when:* any change of batch size
  with Adam or a variant.
- **R3** — Avoid gradient accumulation unless training across devices with
  multiple replicas bottlenecked on interconnect bandwidth. *Topic:* systems.
  *Status:* experimental. *Strength:* moderate. *Applies when:* the
  alternative of simply using the smaller batch is available.
- **R4** — Do not apply square-root learning-rate scaling across large batch
  ratios; it overshoots by an order of magnitude at 1000×. *Topic:* learning
  rate. *Status:* experimental. *Strength:* moderate. *Applies when:*
  transferring a learning rate across a wide batch-size change.

## Bearing on the record

- **Should produce practices** for R1 and R2. R2 is the load-bearing one: R1
  is only safe *because* of R2, and a reader who takes the first without the
  second gets the instability the paper is explaining away.
- **Reframes rather than contradicts [SOTA-093](../practices.d/SOTA-093.md)** (larger batches later in
  training) and [SOTA-198](../practices.d/SOTA-198.md) (measure the noise scale). Both describe a ceiling
  that rises; this argues against sitting at it.
- **Bears on the record's optimizer recommendations in an uncomfortable way.**
  If optimizer choice stops mattering at small batch, then part of what the
  record's optimizer practices are recommending is robustness at a batch size
  this paper says not to use. That is not a refutation of any of them and it
  is a question none of them answers.
- **Nothing here bears on [SOTA-097](../practices.d/SOTA-097.md) or [SOTA-062](../practices.d/SOTA-062.md) directly** — it is about the
  other end of the range.

## Limitations

- The optimizer sweeps are at 30M parameters. The 1.3B check is a single
  configuration against a single untuned baseline, at about half Chinchilla's
  token ratio.
- Batch size one is only a choice when the model fits on one device. Nothing
  here addresses sharded training, where the global batch is largely set by
  the parallelism topology.
- Weight decay is switched off rather than rescaled in the batch-1
  configurations, which leaves its interaction with the half-life rule
  unexamined — and [LIT-443](../literature.d/LIT-443.md) says weight decay is the hyperparameter that
  should be moving.
- C5 is an inference from the other results plus a memory argument, not a
  measurement of accumulation against its alternative at matched conditions.
- The authors say they do not know why fixing the half-life in tokens
  generalizes across scales.

## Open questions

- How does the half-life rule interact with a batch-size *schedule*? The
  authors raise it and do not answer it.
- Can an optimizer be designed for the small-batch regime specifically, with
  small state? The finding that state buys little there suggests the current
  designs are solving the wrong problem.
- Why does a fixed token half-life transfer across model scales? No account
  is offered, and it is the kind of regularity that usually has one.
