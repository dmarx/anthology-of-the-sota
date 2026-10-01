---
number: 94
status: 'Active'
title: 'count accelerator efficiency alongside sample efficiency when choosing a batch size: larger batches mean larger matrix multiplications'
version: 1
tags:
# Retagged from the report of unbound lineage, with SOTA-092 and SOTA-093.
# It is the fourth of one paper's four claims about batch size, and
# `training-optimization` names batch size in its blurb. All four carried
# `model-architecture` because their source is a model report.
- training-optimization
date: '2026-08-24'
source:
- LIT-069
# Was LIT-069, under the old title "throughput (energy efficiency) wins out
# over theoretically optimal sample efficiency", which PaLM does not say: it
# gives TPU efficiency as one of two reasons for its batch ramp, ranks
# neither, and never mentions energy. Retitled in the correction pass to what
# it does say. Left empty (ADR-053) because PaLM states that reason uncited,
# as something already known, not as a recommendation of its own. Searched and
# not found: LIT-017 (McCandlish et al. 2018) is the nearest document, and it
# trades steps against examples under data parallelism with the exchange rate
# left "according to preference", not per-device efficiency against sample
# efficiency. Naming the paper that first argued batch size up for matmul
# efficiency is how a reader refutes this.
introduced_by: []
summary: >-
  Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).
implementations:
- PaLM
---

# SOTA-094: count accelerator efficiency alongside sample efficiency when choosing a batch size: larger batches mean larger matrix multiplications

## Source

Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).

## Known implementations

- PaLM

## Two reasons for one batch size

[SOTA-092](SOTA-092.md) and [SOTA-093](SOTA-093.md) are statements about loss per token seen. This
is the other quantity a batch size moves: what a training run spends is
accelerator-hours, and a batch chosen on sample efficiency alone can leave the
hardware underused.

[LIT-069](../literature.d/LIT-069.md) gives this as the second reason for its batch ramp, beside the
sample-efficiency one: "larger batch sizes result in larger matrix
multiplication dimensions, which increases TPU efficiency." The same pressure
shows elsewhere in the paper — PaLM 540B rematerialises activations because
the larger batch that permits gives higher training throughput, and the
discussion notes that holding TPU efficiency at larger scale would need a
drastic increase in batch size when 4M tokens is already of unclear sample
efficiency.

What the paper does not do is rank the two. It runs a schedule that both
reasons point toward, measures neither against the other, and in the
discussion treats sample efficiency as the constraint on going larger rather
than something throughput overrides. This practice said, until the correction
pass, that throughput "wins out" and that it is "energy efficiency"; neither
is in the paper, and the record has no other source for the ordering. What
remains is the weaker and supported claim: both quantities belong in the
choice.

Nor is PaLM where this comes from. It states the reason in a clause, uncited,
as something its readers already know, and the record cannot name the work
that first argued it — so `introduced_by` is left empty (ADR-053) rather than
crediting PaLM with an origin it does not claim.

## Where it stops holding

At the extreme it obviously fails: a batch large enough to saturate the
hardware and then keep growing buys nothing per step past the critical batch
size ([SOTA-093](SOTA-093.md)) and still costs memory. The rule is "let utilisation push the
batch up within the range where sample efficiency still holds", which is how
PaLM's discussion reads it, not "maximise batch".

And the underlying quantity is *energy or cost per unit of progress*, not
throughput as such. Those come apart on heterogeneous hardware and under a
schedule that trades precision for speed, where the faster configuration is
not the cheaper one — worth naming, because this practice's old title treated
them as the same thing.
