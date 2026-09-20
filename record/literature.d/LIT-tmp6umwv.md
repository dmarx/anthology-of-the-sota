---
status: Active
title: 'Muon is Not That Special: Random or Inverted Spectra Work Just as Well'
version: 1
tags:
- training-optimization
date: '2026-09-20'
published: '2026-05-01'
arxiv: '2605.11181'
first_author: 'Shumaylov'
keywords:
- 'muon'
- 'spectral-descent'
- 'linear-minimization-oracle'
- 'schatten-norm'
- 'step-size'
implementations:
- 'Freon'
- 'Kaon'
- 'TruncatedSGD'
summary: >-
  Shumaylov et al. (2026), [ARXIV-2605.11181](https://arxiv.org/abs/2605.11181). Replace the gradient's
  singular values with chaotic noise and the optimizer still matches Muon.
  The geometric account of why spectral optimizers work does not survive its
  own control; what survives is that Muon's optimal step size is constant.
---

<!-- inactive-ok-file: THEORY-024 THEORY-tmp6a2vb ADR-031 — THEORY-024 is Proposed as of this contribution and is the account this paper tests; THEORY-tmp6a2vb is Proposed and filed here from this paper; ADR-031 is Proposed and is the decision that makes the practice/explanation split this note relies on -->
# LIT-tmp6umwv: Muon is Not That Special: Random or Inverted Spectra Work Just as Well

Shumaylov et al. (2026) — [ARXIV-2605.11181](https://arxiv.org/abs/2605.11181)

## Key takeaways

- **The control is the contribution.** `Kaon` replaces the gradient's
  singular values with noise from a chaotic logistic recurrence. It computes
  no linear minimization oracle, targets no norm, and has no coherent
  geometry at all — and it matches Muon on NanoGPT. The authors call it a
  pedagogical construction rather than a proposal, which is the right way to
  read it: it is the experiment that the geometric account did not have.
- **The optimum is outside the space the theory can describe.** `Freon`
  sweeps Schatten `p`-updates from SGD through Muon and on into `p < 1`. On
  GPT-2 the best exponents sit strictly in the quasi-norm regime, where no
  unitarily invariant norm exists — so the best-performing update in the
  family is not a steepest-descent direction for any norm, which is what the
  LMO framework would need it to be.
- **Suppressing the large singular values is necessary and not sufficient.**
  `TruncatedSGD` zeroes the top few percent and improves on SGD without
  closing the gap to Muon. The obvious simpler story — that spectral
  optimizers just clip noisy directions — is tested and rejected in the same
  figure.
- **What is left when the geometry goes is step-size realizability.** Under
  exact line search in a random-feature model the ranking *reverses*: plain
  gradient descent beats spectral descent. But optimal GD needs a wildly
  oscillating step-size schedule nobody can implement, while spectral
  descent's optimal step size is effectively constant through training. The
  paper's own summary is that Muon succeeds "not by tracking an ideal global
  geometry, but by guaranteeing step-size optimality".
- **Two local quantities replace the norm.** Batch gradient alignment and
  directional descent potential fall out of the exact local Taylor expansion
  with no appeal to an LMO. Optimizers trade one against the other, and the
  trade only pays at a step size tuned to exploit it.

## Standing in the anthology

This is the outside test [THEORY-024](../theory.d/THEORY-024.md) said it had not had. That document
closes by noting that its three sources share authors and that it is `Active`
"not because anyone outside has confirmed the frame" — and the first outside
group to look comes back negative on the frame's explanatory force. The
derivation there is unaffected; what this paper reaches is the claim that
being the duality map is *why* it works. See [THEORY-tmp6a2vb](../theory.d/THEORY-tmp6a2vb.md).

The evidence is NanoGPT and WikiText-2 at 118M tokens, and the authors list
the scope limit first among their own. The practices the record recommends
here are evidenced at three and four orders of magnitude more, so this
contests an explanation and not a recommendation — which is exactly the split
[ADR-031](../decisions.d/ADR-031.md) created the `THEORY` scheme for.
