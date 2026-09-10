---
number: 193
status: Proposed
formerly:
- SOTA-tmpbqbcf
promote_when: >-
  An ablation. One training run at scale, with and without the lowered β₂,
  reporting spike frequency and final loss — from anybody. The value is widely
  used and, as far as this record can find, has never been isolated against
  the alternative interventions it competes with.
consensus: converged
consensus_note: >-
  β₂ = 0.95 is what large runs use, against Adam's 0.999 default. The value is
  settled; the *reason* is folklore with one published statement behind it,
  which is why the practice is Proposed while the consensus is converged.
title: "Lower Adam's second-moment decay when the loss spikes, before reaching for the learning rate"
version: 1
tags:
- model-stability
date: '2026-09-10'
source:
- LIT-065
implementations:
- MT-NLG
---

# SOTA-193: Lower Adam's second-moment decay when the loss spikes, before reaching for the learning rate

## Source

Smith et al. (2022), [LIT-065](../literature.d/LIT-065.md) — the MT-NLG 530B training report, which states
it as an operational finding:

> We also reduced β₂ from its standard value of 0.99 to reduce spikes in the
> training loss.

The value they trained with is **β₂ = 0.95**.

## The claim

When the loss spikes, the reflex is to lower the learning rate — which slows
everything, permanently, to fix an intermittent problem. β₂ is the cheaper dial
and it is aimed at the actual mechanism.

β₂ sets how long Adam remembers the second moment. At 0.999 the denominator
averages roughly the last thousand gradients, so a parameter that has been quiet
for a long time has a **small** accumulated second moment — and when a large
gradient finally arrives, it is divided by that small number and the step is
enormous. Shortening the memory means the denominator reflects recent gradient
magnitudes, so a spike is divided by something that has seen spikes.

Lowering β₂ costs adaptivity in the other direction: the per-parameter scale now
swings with a few noisy batches, which is what the long memory was for. That is
the trade, and it is why this is a response to observed spikes rather than a
default.

## Why this is `Proposed` while the consensus is `converged`

β₂ = 0.95 is what frontier runs use. What is missing is the **ablation**: the
paper reports the change and the reason, and does not show the run with and
without. So the record can say the field converged on the value without being
able to say this is why it works, or that it beats the alternatives.

Those alternatives are all in the record already and none has been compared
against this: [SOTA-035](SOTA-035.md) and [SOTA-071](SOTA-071.md) (gradient clipping, static and dynamic),
[SOTA-052](SOTA-052.md) (initialisation variance), and lowering the learning rate. A spike is
overdetermined and the interventions are cheap, so people apply several at once
and nobody isolates any.

## Where it sits against [SOTA-002](SOTA-002.md)

[SOTA-002](SOTA-002.md) records `β₂ = 0.999` as the common default and already observes that
"very large batch training often lowers β₂" — correctly, and without a source
or a number. This is the source and the number, and the *reason* differs from
the one `SOTA-002` gives: that practice attributes the lowering to the gradient
already being averaged over many samples, while `LIT-065` attributes it to loss
spikes. Both may be true and they are different arguments.

## Conditions

One operational report, at 530B, on a dense decoder-only transformer, unablated.
Reported alongside two other stability findings from the same run — that
higher-variance initialisation fails to converge, and that the learning rate was
*projected* from model size rather than swept — so the run had several things
holding it up at once.

## Known implementations

- MT-NLG 530B (β₁ = 0.9, β₂ = 0.95, ε = 1e-8)
