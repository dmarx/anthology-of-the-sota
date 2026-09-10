---
number: 12
status: Read
formerly:
- NOTE-tmpd2c6t
paper: LIT-009
title: 'LARS: Large Batch Training of Convolutional Networks'
version: 1
tags:
- training-optimization
date: '2026-09-09'
published: '2017-08-01'
summary: >-
  Linear LR scaling with warm-up is "not general enough and training may diverge". Layer-wise Adaptive Rate Scaling sets a per-layer rate from the ratio of weight norm to gradient norm, reaching AlexNet at batch 8K and ResNet-50 at batch 32K without accuracy loss.
---

# NOTE-012: LARS: Large Batch Training of Convolutional Networks

## Contribution

Data-parallel training grows the batch with the node count, and large batches
cost accuracy. The standing recipe was **linear learning-rate scaling with
warm-up** (Goyal et al.), which had reached batch 8K on ResNet-50. This paper's
first move is negative: that recipe **is not general enough**, and applied
beyond its demonstrated range training diverges. Its second is **Layer-wise
Adaptive Rate Scaling** — a separate learning rate per layer, derived from the
ratio of that layer's weight norm to its gradient norm — which reaches
**AlexNet at 8K and ResNet-50 at 32K without loss in accuracy**.

## Key insight

A single global learning rate assumes every layer wants steps of the same
relative size, and at large batch that assumption breaks unevenly: the ratio
of weight norm to gradient norm differs by orders of magnitude between layers,
so the rate that is safe for the worst layer is far too small for the rest.
Warm-up manages this in *time* — go slowly until things settle — where the
real variation is across *layers*.

That reframing is why the paper can go past 8K. Warm-up postpones the problem
uniformly; a per-layer rate addresses where it actually lives.

## Assumptions

- **Convolutional networks** on ImageNet — AlexNet and ResNet-50. Not
  Transformers, and nothing here is a language model.
- Data-parallel synchronous SGD; the batch grows because the node count does.
- The layer-norm-to-gradient-norm ratio is assumed meaningful per layer,
  which is the premise of the trust-ratio construction.
- 2017 hardware and scales.

## Key results

- **The negative result**: "the current recipe for large batch training
  (linear learning rate scaling with warm-up) is not general enough and
  training may diverge."
- **LARS**: a per-layer rate scaled by the trust ratio between weight norm
  and gradient norm.
- **AlexNet to batch 8K** and **ResNet-50 to batch 32K**, both without loss
  in accuracy.
- Warm-up is described as prior art throughout — "Linear scaling of LR with a
  warm-up is the *state-of-the-art* recipe" — and attributed to Goyal et al.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Linear scaling with warm-up does not generalise past its demonstrated range | strong | they applied it and it diverged; the paper's motivating experiment |
| C2 | The right learning rate varies by layer, not just over time | moderate | argued from the norm ratios and supported by LARS working |
| C3 | LARS reaches batch 32K on ResNet-50 without accuracy loss | strong | measured |
| C4 | Large batch costs accuracy absent such a measure | strong | the premise, and widely replicated since |

## Method

**Algorithm:** Layer-wise Adaptive Rate Scaling.

For each layer, compute a **trust ratio** from `‖w‖ / ‖∇w‖` and scale the
global learning rate by it, so each layer takes a step proportional to its own
weight magnitude rather than to a shared constant.

## Concepts

- **Trust ratio** — `‖w‖/‖∇w‖` per layer, the quantity LARS scales by. The
  ancestor of every later per-layer or per-parameter rate rule.
- **Linear scaling rule** — multiply the learning rate by the batch-size
  multiplier. Prior work here, and the thing shown to have a ceiling.

## Connections

Directly a response to **Goyal et al.** ([LIT-007](../literature.d/LIT-007.md)), whose warm-up plus linear
scaling it cites, uses as the baseline, and argues past. Its per-layer rate is
the empirical ancestor of the parameterisation-based transfer arguments — µP
and relatives — that this record holds later, and of LAMB in the Transformer
era.

## Recommendations

- **R1** — Do not assume linear LR scaling with warm-up holds at an arbitrary
  batch size. *Topic:* large-batch training. *Status:* standard. *Strength:*
  strong. *Applies when:* pushing batch beyond a range someone has
  demonstrated.
- **R2** — Consider a per-layer rate when a global one is the binding
  constraint. *Topic:* optimization. *Status:* experimental for
  Transformers, standard for the CNN case measured. *Strength:* moderate.
  *Applies when:* the layers' weight-to-gradient norm ratios differ widely.

## Bearing on the record

**The one practice sourced to this note is re-sourced.**

| practice | disposition |
|---|---|
| [SOTA-008](../practices.d/SOTA-008.md) linear warmup of LR stabilizes early training with large batch size | **re-sourced** to `LIT-007` |

Warmup is Goyal et al.'s. This paper cites it as prior art and then argues it
**is not general enough**, so the record had the practice sourced to the paper
that found its limit rather than the one that introduced it. `SOTA-008` now
names `LIT-007` first, with this note beside it — a reader should know both
where the recipe comes from and that it has a ceiling.

That is the **second** instance of this shape in [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114), after `SOTA-113`, where
continuous batching was sourced to vLLM rather than Orca. In both cases the
citation landed on the more famous later paper, which described the technique
in its background while contributing something else.

## Limitations

- CNNs on ImageNet. Whether the trust-ratio construction transfers to
  Transformers is not addressed here — LAMB is the paper that asked.
- C2 is argued and demonstrated rather than isolated; no ablation separates
  the per-layer scaling from LARS's other details.
- 32K is a 2017 ceiling on 2017 models, and says nothing directly about the
  token-batch sizes in this record's contemporary practices.

## Open questions

- The record's modern answer to per-layer rates is parameterisation (µP)
  rather than a measured ratio. Is the trust ratio recovering something µP
  derives, or a different quantity?
- C1 says the recipe has a ceiling and locates it empirically. Nothing in
  this record says where the ceiling is for a Transformer.
