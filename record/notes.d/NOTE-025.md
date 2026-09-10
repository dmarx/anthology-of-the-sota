---
number: 25
status: Read
formerly:
- NOTE-tmpx9gty
# inactive-ok: LIT-101 — Proposed — a watch-list paper, and this document is the reading that says what would take it off the list
paper: LIT-101
title: 'AdaNorm: Adaptive Gradient Norm Correction based Optimizer for CNNs'
version: 1
tags:
- training-optimization
date: '2026-09-09'
summary: >-
  Keeps an EMA of the gradient's scalar L2 norm and, when the current gradient is smaller than that history, scales it up to match — a floor under the gradient norm, applied to Adam's first moment only. The exact mirror image of gradient clipping. Evidence is VGG/ResNet on CIFAR-10, CIFAR-100 and TinyImageNet; there is no transformer and no language result.
---

# NOTE-025: AdaNorm: Adaptive Gradient Norm Correction based Optimizer for CNNs

## Contribution

A one-line modification that can be dropped into any adaptive optimizer.
Track `e_t`, an EMA of the **scalar L2 norm** of the gradient. If the current
gradient's norm has fallen below that history, rescale the gradient up to
meet it:

    g_norm = ‖g_t‖₂
    e_t    = γ·e_{t−1} + (1−γ)·g_norm
    s_t    = (e_t / g_norm)·g_t   if e_t > g_norm, else g_t

`s_t` then feeds the **first moment only**; the second moment keeps using the
raw `g_t`. The paper instantiates this on Adam, diffGrad, RAdam and AdaBelief
(AdamNorm, diffGradNorm, RadamNorm, AdaBeliefNorm).

## Key insight

The interesting part is what the record already believes about the *other*
side of the same quantity. `SOTA-035` says clip the gradient — put a **ceiling**
on its norm, so one bad batch cannot take a large step. AdaNorm puts a
**floor** under it, on the argument that a gradient much smaller than its own
recent history is uninformative rather than a signal to slow down, and that
Adam "get[s] saturated soon due to the lack of consistent gradients".

So the two are the same instrument pointed in opposite directions, and only
one of them is a practice here. The paper does not make that connection; it
is the reason this note is worth having.

Note also the asymmetry inside the method: the correction is applied to `m_t`
and deliberately **not** to `v_t`, and the ablation says why — the second
moment sets the step size, so correcting it "hampers the effective step-size
leading to poor performance". The method wants a bigger gradient *direction
signal*, not a bigger step.

## Assumptions

- **A gradient below its recent historical norm is uninformative**, and
  restoring its magnitude restores information. This is asserted and
  motivated, not demonstrated independently of the accuracy numbers.
- **One scalar norm characterises the whole gradient.** `e_t` is global across
  all parameters, so a layer whose gradient legitimately shrank is scaled by a
  factor set by the rest of the network.
- The setting is **CNN object recognition at small scale**. Every experiment
  is VGG16, ResNet18 or ResNet50 on CIFAR-10, CIFAR-100 or TinyImageNet.

## Key results

- Accuracy improves in almost all of 4 optimizers × 3 models × 3 datasets,
  averaged over three runs. Largest reported gain **11.15%**, AdamNorm over
  Adam on ResNet50/TinyImageNet.
- **γ = 0.95** is the default. 0.999 is too high; CIFAR prefers ~0.99 and
  TinyImageNet ~0.90, which the authors attribute to TinyImageNet's longer
  run — the EMA's horizon should scale with the number of iterations.
- **First moment only.** Applying the correction to the second moment, or to
  both, is worse.
- Measured gradient norms under AdamNorm are "much higher" than Adam's
  throughout training, which is the mechanism doing what it says.
- Claimed reduced sensitivity to batch size (32/64/128) versus Adam.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Adaptive optimizers suffer from gradients that fall below their historical norm | moderate | motivating argument plus the gradient-norm plots; no isolated experiment |
| C2 | Flooring the norm at its EMA improves CNN accuracy on these benchmarks | strong | 36 cells, 3 seeds, consistent direction |
| C3 | The correction belongs on the first moment and not the second | strong | ablated three ways |
| C4 | γ should shrink as the number of iterations grows | weak | inferred from two datasets differing in run length |
| C5 | The method reduces batch-size sensitivity | weak | three batch sizes, no mechanism offered |
| C6 | The approach is generic across adaptive optimizers | moderate | four instantiations, all in the same regime |

## Method

Insert the three lines above before the moment updates. Tune γ. Everything
else — the optimizer, schedule, initialisation — is unchanged. Train VGG16 /
ResNet18 / ResNet50 on CIFAR-10, CIFAR-100, TinyImageNet, LR dropped by 10×
at epoch 80, average three runs.

## Concepts

- **Gradient norm floor** — the idea itself, and the complement of clipping.
- **History as the reference scale** — the floor is not a constant but the
  EMA of the network's own recent norms, so it tracks the run rather than
  being tuned to it. That part is portable even if the method is not.

## Connections

Sits directly opposite `SOTA-035` (gradient clipping, Pascanu et al.), which
bounds the same quantity from above. Its cited neighbours — diffGrad, RAdam,
AdaBelief, AdaBound, AdaMod, Yogi — are the 2018–2022 wave of Adam variants,
essentially none of which displaced AdamW at language-model scale. `LIT-156`
is the paper that explains why that wave did not transfer: challengers are
usually tuned less carefully than the baseline, and measured too early.

## Recommendations

- **R1** — Do not read a below-average gradient norm as a reason to take a
  smaller step. *Topic:* training optimization. *Strength:* weak — this is
  the paper's thesis and it is established only on small CNNs.
- **R2** — If correcting a gradient, correct the direction signal and not the
  step size: touch the first moment, leave the second alone. *Strength:*
  moderate, and the most transferable thing here — it is a statement about
  what Adam's two moments are *for*.

## Bearing on the record

**No practice is sourced to this paper, and this reading does not create one.**

<!-- inactive-ok-block: LIT-101 — Proposed, and this paragraph is about that document's own defects -->
What it does do is correct the note. `LIT-101` carried four takeaways and two
of them are false:

| takeaway | verdict |
|---|---|
| "Adaptive gradient normalization" | vague but fair |
| "Improved training stability" | **backwards** — the method *amplifies* gradients; the paper's target is saturation, not instability |
| "Scale-invariant updates" | **not in the paper.** Nothing here is scale-invariant; the gradient is rescaled toward a historical average, which is a different property |
| "Large-scale model optimization" | **contradicts the paper's own title**, which ends "for CNNs". The largest dataset is TinyImageNet |

The `Standing` section's advice to "consider AdamW as proven alternative" also
mis-frames the choice: AdaNorm is not an alternative to AdamW but an addition
that could sit on top of one, and the paper never tests that combination.

## Limitations

- No transformer, no language model, no full ImageNet. The four-year gap
  since publication with no scale-up is itself information.
- The floor is global, so it cannot distinguish a network-wide quiet phase
  from one layer going quiet.
- C1 is never isolated: every result is end-of-training accuracy, so
  "uninformative gradients were the problem" is inferred from the fix
  working.
- The interaction with gradient clipping — the practice this record actually
  holds — is not discussed anywhere.

## Open questions

- What happens when a floor and a ceiling are applied together? The record
  recommends clipping; this paper recommends its opposite; nobody has run
  both.
- Does R2 — correct the first moment, never the second — generalise beyond
  this method? It is stated here as an implementation detail and reads like
  a general fact about Adam.
