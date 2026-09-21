---
number: 254
status: Read
formerly:
- NOTE-tmplxznx
paper: LIT-507
title: 'Adaptive estimators: a counter-rebuttal whose body is weaker than its abstract'
version: 1
date: '2026-09-21'
summary: >-
  Read to check whether it softens [LIT-509](../literature.d/LIT-509.md), as
  [#220](https://github.com/dmarx/anthology-of-the-sota/issues/220) feared. It does on one narrow point and not on the one that
  matters. Its own Figure 6 shows a ReLU network averaged over 50
  initializations has **no distinct phase**, and it agrees with the rebuttal
  that hidden-layer compression does not correlate with generalization.
---

# NOTE-254: Adaptive estimators: a counter-rebuttal whose body is weaker than its abstract

## Contribution

Argues that [LIT-509](../literature.d/LIT-509.md)'s ReLU result is an artifact of its binning,
develops adaptive binning and adaptive kernel-density estimators, and reports
that under them saturation is not required for compression.

## Key results

**The technical criticism is specific and correct.** [LIT-509](../literature.d/LIT-509.md) bins
ReLU activity over one global range `[0, m]`, `m` the largest activity
anywhere in the network across all of training. This paper's Figure 1 shows
the **last** ReLU layer dominates that maximum, so a single range
under-resolves every earlier layer, and non-adaptive binning therefore
under-estimates compression. Its equal-bin-area adaptive binning (EBAB) sets
bin boundaries from the distribution of activity in a given layer and epoch,
which makes layers and epochs comparable in a way one fixed range does not.

**And then its own averaging undoes the headline.** The compression it
showcases is a single initialization. §3 reports that initializations vary
enormously — Figure 5 shows hidden layers on "vastly different trajectories"
from initialization alone — and Figure 6, averaged over **50 initializations**
as the original study did, shows a ReLU network with **no distinct fitting or
compression phase**, `I(T;X)` largely flat, with fitting and compression
"mostly cancel[ling] out". The same holds across absolute value, PReLU, ELU,
softplus, centered softplus and Swish.

So the abstract's "saturation of the activation function is not required for
compression" is supported by some initializations and contradicted by the
average of fifty. `DP-010`, and unusually clean: the sentence that will be
cited is the one the paper's own protocol does not support.

**Where it agrees with the rebuttal, which is the part that matters.**
Quantifying hidden-layer compression and comparing it against generalization,
**no significant correlation is observed**. Only compression of the last
softmax layer correlates. That is the same conclusion
[LIT-509](../literature.d/LIT-509.md) reaches by a four-cell dissociation, arrived at
independently by a group trying to defend the theory.

**One genuinely new finding.** L2 regularization induces compression in ReLU
networks and clusters the layers to the same mutual information, in the late
training stage where networks usually begin overfitting. Not obviously
predicted by either side.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Non-adaptive binning under-estimates compression in unbounded activations | strong | Figure 1's layer-wise maximum breakdown; direct comparison of estimators on one run |
| C2 | Saturation is not required for compression | **weak** | holds for some initializations; the 50-initialization average in Figure 6 shows no phase |
| C3 | Hidden-layer compression does not correlate with generalization | strong, and concedes the rebuttal's central point | its own compression metric against generalization |
| C4 | L2 regularization increases compression | moderate | one architecture, 50 initializations |

## Limitations

**It changes two things at once.** The estimator is adaptive *and* the
reported result is a single initialization; the paper establishes the first
carefully and rests its headline on the second.

**It does not address the deterministic-infinity problem at all.** Its
adaptive estimators are a better choice of imposed noise model, not an escape
from having to impose one. Nothing in it answers
[LIT-509](../literature.d/LIT-509.md)'s Appendix C, where a different binning of the *same*
`tanh` run removes the compression the original claimed.

**Nothing on SGD.** The third IB claim — compression arises from SGD's
diffusion — is not contested here, and the rebuttal's full-batch result stands
unchallenged.

## Bearing on the record

**It is the reason the dispute could not be filed from two papers.**
[#220](https://github.com/dmarx/anthology-of-the-sota/issues/220) was right that filing the claim and the rebuttal alone would
misrepresent the state of the argument — but wrong about the direction. Read
carefully, this paper does not rescue the compression phase; it narrows the
dispute to whether `tanh`'s compression is *specifically* a saturation
artifact, while conceding the generalization claim that made the theory
interesting.

**It is the second independent demonstration that the estimator decides the
answer**, pointing the opposite way from the first. The rebuttal changes the
binning and compression *disappears*; this paper changes the binning and
compression *appears*. Neither is the truth, because there is no truth of the
matter for a deterministic map. That symmetry is what
[SOTA-312](../practices.d/SOTA-312.md) rests on, and neither paper states it as its
own conclusion.

## Open questions

- **Does adaptive estimation change the four-cell dissociation?** This paper
  re-estimates information but does not redo the generalization dissociation
  under its own estimators, beyond the correlation study.
- **Why does L2 induce compression?** Reported, not explained, and it is the
  one result here neither side predicts.
- **What would an initialization-resolved account look like?** Figure 5 is the
  most interesting plot in the paper and gets the least attention: whatever
  determines whether a given ReLU network compresses is unidentified.
