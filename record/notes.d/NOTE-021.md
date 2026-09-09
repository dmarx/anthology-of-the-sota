---
number: 21
status: Read
formerly:
- NOTE-tmpx1otw
paper: LIT-100
title: 'Grouped-Query Attention'
version: 1
tags:
- attention-techniques
date: '2026-09-09'
summary: >-
  MQA is fast and costs quality, and training a separate model for inference is undesirable. Two results: uptrain an existing multi-head checkpoint with 5% of pretraining compute, and use an intermediate number of key-value heads — quality near multi-head at speed near MQA.
---

# NOTE-021: Grouped-Query Attention

## Contribution

Multi-query attention makes decoding much faster and costs quality, and it
poses a second problem the first papers did not address: **you would have to
train a separate model** to get it, which nobody wants to do for an inference
property. This paper answers both. **Uptraining** converts an existing
multi-head checkpoint to fewer key-value heads for **5% of original
pretraining compute**. **Grouped-query attention** generalises MQA to an
*intermediate* number of key-value heads — more than one, fewer than the query
heads — reaching quality close to multi-head at speed comparable to MQA.

## Key insight

MQA framed the key-value head count as a binary: `h` heads or one. It is a
**dial**, and almost all of the bandwidth saving is available before the
quality cost arrives — the first few heads you remove are nearly free, the
last one is not.

The second insight is orthogonal and arguably more useful: an architectural
property of inference does not have to be decided at the start of
pretraining. If a cheap conversion exists, the decision can be deferred to
after the expensive part is done.

## Assumptions

- Starts from an **existing multi-head checkpoint**; uptraining is a
  conversion, not a from-scratch recipe.
- The 5% figure is relative to that checkpoint's original pretraining
  compute — cheap because it is 5%, not because it is small in absolute
  terms.
- Decoder inference is memory-bandwidth bound, inherited from MQA and cited
  to Shazeer and to Pope et al.
- Evaluated at the scales and tasks of the period.

## Key results

- **Uptraining**: convert a multi-head checkpoint to MQA (or GQA) using **5%
  of original pretraining compute**.
- **GQA**: `g` key-value head groups with `1 < g < h`, each shared across a
  group of query heads. MQA is `g = 1`; multi-head is `g = h`.
- **Uptrained GQA achieves quality close to multi-head with speed comparable
  to MQA** — the headline, and the reason the record's models use it.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | MQA's quality degradation is real and avoidable | strong | the comparison that motivates GQA |
| C2 | An intermediate key-value head count gets most of the speed at most of the quality | strong | the paper's central measurement |
| C3 | A multi-head checkpoint can be uptrained for 5% of pretraining compute | strong | measured |
| C4 | The KV head count need not be fixed before pretraining | moderate | follows from C3, and is the practical consequence |

## Method

**Architecture + procedure.**

Partition the `h` query heads into `g` groups; give each group one key head
and one value head. To obtain such a model from an existing multi-head
checkpoint, mean-pool the key and value projections within each group to
initialise the shared heads, then continue pretraining briefly — 5% of the
original budget.

## Concepts

- **Uptraining** — converting a trained checkpoint to a different attention
  configuration with a short continuation, rather than retraining. The
  paper's coinage and the more transferable of its two ideas.
- **Group** — the set of query heads sharing one key/value head. `g` is the
  dial between MQA and multi-head.

## Connections

Directly generalises **MQA** ([LIT-024](../literature.d/LIT-024.md)), which it cites for both the mechanism
and the bandwidth diagnosis, and which it treats as the `g = 1` endpoint of
its own axis. Pope et al. is the other bandwidth citation.

## Recommendations

- **R1** — Use grouped-query attention rather than either extreme. *Topic:*
  architecture. *Status:* standard. *Strength:* strong. *Applies when:*
  decoder inference throughput matters, which is nearly always.
- **R2** — Consider uptraining before retraining, when the change is an
  inference-side architectural property. *Topic:* adaptation. *Status:*
  standard. *Strength:* moderate. *Applies when:* a trained checkpoint
  exists and the property can be initialised from it.
- **R3** — Check whether a binary architectural choice is really a continuum.
  *Topic:* architecture. *Status:* standard. *Strength:* moderate.
  *Applies when:* a prior paper offers two endpoints and no interior; that is
  exactly the gap this one filled.

## Bearing on the record

**The one practice sourced to this note is confirmed.**

| practice | disposition |
|---|---|
| [SOTA-109](../practices.d/SOTA-109.md) prefer GQA to MQA or MHA | confirmed — C1, C2 |

`SOTA-109` gains the second half of its source. The practice is about the
*architecture*; **uptraining** is the other contribution and is arguably the
more portable idea — it says an inference-side property need not be committed
to before pretraining. Nothing in the record states that, and the record holds
several practices that are pretraining-time commitments where the same
question could be asked.

Read alongside [NOTE-016](NOTE-016.md), this closes the MQA line cleanly: MQA
diagnosed the bandwidth bound and took the extreme, this found the interior
and a cheap route to it.

## Limitations

- Uptraining starts from a multi-head checkpoint; nothing here covers
  converting in the other direction or between other configurations.
- The 5% figure is one measurement at one scale; whether it holds at frontier
  scale is not established here.
- No rule for choosing `g` — the paper shows the dial exists and roughly
  where it is flat, not how to set it for a new model.

## Open questions

- How should `g` be chosen? The record uses GQA everywhere and cites no rule
  for the group count.
- R3 generalises: MQA presented a binary and the answer was in the middle.
  Which other two-endpoint choices in this record have an unexamined interior?
