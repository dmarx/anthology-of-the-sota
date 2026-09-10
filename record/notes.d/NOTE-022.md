---
number: 22
status: Read
formerly:
- NOTE-tmpx5gy4
paper: LIT-023
title: 'RMSNorm'
version: 1
tags:
- model-stability
date: '2026-09-09'
published: '2019-10-01'
summary: >-
  LayerNorm gives re-centering and re-scaling invariance; the hypothesis is that re-centering is dispensable. Normalize by root mean square alone — re-scaling invariance and implicit learning-rate adaptation kept, 7–64% less time per step.
---

# NOTE-022: RMSNorm

## Contribution

LayerNorm's benefit is usually attributed to two invariances it confers:
**re-centering** (subtract the mean) and **re-scaling** (divide by the
standard deviation). Its cost is real — the paper's motivating case is that
it "significantly slows the underlying network, e.g. RNN in particular". This
paper hypothesises that **re-centering is dispensable**, keeps only the
division by root mean square, and shows the resulting normalization is
computationally simpler while retaining what matters.

## Key insight

The two halves of LayerNorm are separable, and only one of them is doing the
work the field cares about. Re-scaling invariance is what makes the layer
robust to the magnitude of its inputs and weights, and it comes with an
**implicit learning-rate adaptation**: the effective step on a weight vector
scales inversely with its norm. Re-centering buys invariance to a *shift* in
the summed inputs, which is a symmetry nothing in a Transformer particularly
needs.

Dropping half an operation for none of the benefit is the kind of result that
only shows up if you ask what each half is for.

## Assumptions

- The claim is a **hypothesis the paper tests empirically**, not a proof —
  its own word: "we hypothesize that re-centering invariance in LayerNorm is
  dispensable".
- Evaluated on 2019 architectures, with RNNs as the motivating case for the
  speed argument.
- **`pRMSNorm`**, the partial variant, additionally assumes the RMS can be
  estimated from `p%` of the summed inputs — a further approximation with its
  own error.

## Key results

- **RMSNorm** normalizes by root mean square only, giving **re-scaling
  invariance** and **implicit learning-rate adaptation**, without
  re-centering.
- **7–64% less time per step** across the settings measured — the range is
  wide because the saving depends on how much of the step the normalization
  was.
- **Comparable quality** to LayerNorm across the tasks tried.
- **`pRMSNorm`** estimates the RMS from `p%` of the summed inputs, cheaper
  again.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Re-centering invariance is dispensable | moderate | stated as a hypothesis and supported empirically across tasks, not proved |
| C2 | Re-scaling invariance is what LayerNorm's benefit rests on | moderate | inferred from C1 holding, rather than isolated directly |
| C3 | RMSNorm confers implicit learning-rate adaptation | strong | follows from the form: the effective step scales inversely with weight norm |
| C4 | 7–64% less time per step | strong | measured |
| C5 | Quality is comparable to LayerNorm | strong | measured across the paper's tasks |

## Concepts

- **Re-centering invariance** — output unchanged when a constant shift is
  added to the summed inputs. The half this paper discards.
- **Re-scaling invariance** — output unchanged when inputs or weights are
  scaled. The half it keeps.
- **Implicit learning-rate adaptation** — because the normalizer scales with
  the weight norm, the effective step size does too, without an optimizer
  knowing about it.

## Connections

A direct simplification of Ba et al.'s LayerNorm. Its interesting neighbour is
[LIT-025](../literature.d/LIT-025.md), published the same year, which also concludes part of LayerNorm is
unnecessary and **picks the other part** — that paper keeps the normalization
whole and drops the learnable gain and bias, where this keeps the gain and
drops the centering. Both report improvements; the field adopted this one.

## Recommendations

- **R1** — Use RMSNorm in place of LayerNorm. *Topic:* normalization.
  *Status:* standard. *Strength:* strong. *Applies when:* effectively always
  in a modern decoder; the quality is comparable and the step is cheaper.
- **R2** — When a component is expensive, ask which of its properties you
  are paying for. *Topic:* architecture. *Status:* standard. *Strength:*
  moderate. *Applies when:* any composite operation whose parts confer
  separable properties.

## Bearing on the record

**The one practice sourced to this note is confirmed.**

| practice | disposition |
|---|---|
| [SOTA-182](../practices.d/SOTA-182.md) compute the normalization statistic without centering | confirmed — C1, C4, C5 |

`SOTA-182`'s body already carried the 7–64% figure and the placement caveat,
and both hold. It gains one thing from the reading: the paper frames its own
claim as a **hypothesis**, which is a weaker footing than a practice marked
`universal` implies. The practice is right that a centered LayerNorm is now
the thing needing justification; the paper it cites did not prove
re-centering useless, it proposed that it is and was not contradicted.

## Limitations

- C1 is a hypothesis supported by results, not an isolation experiment. What
  re-centering *does* is never measured directly.
- 2019 tasks and scales; the adoption at frontier scale is field practice
  rather than this paper's evidence.
- `pRMSNorm` adds an approximation whose error is not characterised for the
  regimes anyone now uses.

## Open questions

- This paper and `LIT-025` each drop a different half of LayerNorm and each
  report an improvement. Has anyone dropped **both** the centering and the
  gain?
- C3 says RMSNorm adapts the learning rate implicitly. How does that interact
  with parameterisations that set the rate explicitly per layer, like µP?
