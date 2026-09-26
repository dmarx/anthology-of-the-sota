---
status: Active
title: 'Guided backpropagation and DeconvNet do partial image recovery, not attribution: the backward ReLU plus a CNN''s local connections reconstruct the input regardless of the class or the weights'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-26'
source:
- LIT-tmpbspyz
explains:
- SOTA-430
summary: >-
  Nie, Zhang and Patel (2018), [LIT-tmpbspyz](../literature.d/LIT-tmpbspyz.md), Theorems 1 and 2. In a **random**
  three-layer CNN, `s_k^GBP(x) ≈ x` — guided backpropagation recovers the input,
  with untrained weights and regardless of the class — while the saliency map and
  DeconvNet are `N(0, I)`. The causes are the **backward ReLU** and the small
  filters that local connectivity implies. So these maps are "unrelated to the
  decision-making of neural networks", which is why they survive weight
  randomization, why they look the same for every class, and why an untrained
  edge detector matches them.
---

<!-- inactive-ok-file: SOTA-430 — Proposed, and declared in `explains:`; this account underwrites the last unexplained row of that practice's verdict table and also supplies the mechanism behind its do-not-validate-by-eye argument. Explaining a not-yet-in-force practice is the normal case. -->
<!-- inactive-ok-file: THEORY-113 — Proposed, and cited to draw the boundary between three accounts over disjoint method families; neither rests on the other. -->

# THEORY-tmpv7nad: Guided backpropagation and DeconvNet do partial image recovery, not attribution: the backward ReLU plus a CNN's local connections reconstruct the input regardless of the class or the weights

## Source

Nie, Zhang and Patel (2018), [LIT-tmpbspyz](../literature.d/LIT-tmpbspyz.md) — ICML 2018, §3 and §4.

## The account

Guided backpropagation and DeconvNet apply a **backward ReLU**: they zero the
backpropagated signal wherever the top gradient is negative, GBP additionally
keeping the forward ReLU's mask ([LIT-727](../literature.d/LIT-727.md) states the rule from the method's
side). The claim is that this turns the backward pass into an approximate
**inversion of the input**, and that the inversion has nothing to do with the
decision.

**Theorem 1.** In a random three-layer CNN with sufficiently many filters,

    s_k^GBP(x) ≈ x

Not "resembles the object", not "highlights the object" — recovers the image,
with weights drawn i.i.d. Gaussian and independently of which logit `k` is
explained.

**Theorem 2.** In the same network, `s_k^Sal(x)` and `s_k^Deconv(x) ~ N(0, I)`.

So neither the plain gradient nor the backward ReLU alone produces recovery; the
combination does. And the second cause is structural: the number of filters
needed scales as `Õ(p/ε²)` in the filter size `p`, so small filters — which is
what local connectivity means — make the recovery cheap. A 3×3×3 filter needs at
most `O(10³)` filters for error under 0.1.

**In a trained network the claim weakens to *partial* recovery**, and the paper
is precise about what the weights then buy: they "control which image patch could
form an active path to the class logit. More importantly, this filtering process
is not class sensitive." The weights select *where*, not *which class*.

## Why this is `Active`

Four arms, two of them built by changing the architecture, and one that runs in
the opposite direction from all the randomization work.

- **Remove the local connections.** In a fully connected network GBP fails too —
  and not marginally: at `N_h = 70000` hidden units, which the paper calls
  "definitely unrealistic", the FCN still does not match a CNN with `N = 64`
  filters. The account names local connectivity as a cause and deleting it
  destroys the effect.
- **Add max-pooling.** DeconvNet goes from noise to human-interpretable while GBP
  and the saliency map are unaffected — "adding the max-pooling makes the
  DeconvNet behave like GBP". An intervention the account says must move exactly
  one of three methods, and it moves exactly that one.
- **The adversarial arm, which is the sharpest.** FGSM turns "panda" into
  "busby" on VGG-16: the input barely changes, the predicted class flips. A
  class-sensitive map must change; a recovery map must not. The saliency map
  "changes significantly"; GBP and DeconvNet "remain almost unchanged". This is
  the mirror image of a randomization test — hold the input fixed and destroy the
  weights, or hold the weights fixed and flip the class — and the account
  survives both.
- **It refutes the rival account by construction.** If these methods visualised
  learned weights, a random network would give noise. GBP gives the image.

## What it explains that the record already held

- **Why guided backprop survives weight randomization** ([LIT-713](../literature.d/LIT-713.md)'s headline
  failure, carried in [SOTA-430](../practices.d/SOTA-430.md)'s verdict table): the map was never about the
  weights.
- **Why an untrained edge detector matches these maps.** `LIT-713` uses that
  comparison rhetorically and `SOTA-430` carries it as the argument against
  validating by eye. Partial image recovery is what an edge detector
  approximates; the comparison was the mechanism.
- **Why the maps are class-insensitive** — the same fact, since `k` does not
  appear in the approximation.

## What it does not say

- **It is not the account for the other two families.** Integrated Gradients,
  InputXGradient, DeepLIFT and Gradient SHAP fail for the input multiplier
  ([THEORY-113](THEORY-113.md)); DTD, LRP-α1β0, Excitation BP and PatternAttribution fail by
  rank-1 convergence of a non-negative chain ([THEORY-114](THEORY-114.md)). Three mechanisms,
  disjoint method sets, and `LIT-729` hands this family here explicitly.
- **It does not conflict with `LIT-729` about pooling switches, though it
  looks like it might.** That paper says class insensitivity "is not caused by
  missing ReLU masks and Pooling switches", rejecting Gu et al.'s account of the
  `z⁺` family; this one says switches are what turn DeconvNet's output from noise
  into recovery. Different families, and recovery is *why* DeconvNet is
  insensitive rather than a competing cause of it.
- **It does not say the maps are useless.** "Partial image recovery" is a real
  description of what you get, and [SOTA-430](../practices.d/SOTA-430.md)'s own escape clause already
  allows a method that fails its tests to serve if you wanted an
  image-processing view of the input. What it forbids is calling that an
  explanation of the model.
- **The theorems are asymptotic and the network is shallow and random.**
  Proposition 1 argues the statistics carry to depth; the trained case is the
  weaker partial-recovery statement, not a bound.
