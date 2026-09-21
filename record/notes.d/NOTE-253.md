---
number: 253
status: Read
formerly:
- NOTE-tmp11zjy
paper: LIT-509
title: 'The information-bottleneck rebuttal, and the assumption it makes visible'
version: 1
date: '2026-09-21'
summary: >-
  Read from the ICLR 2018 version, supplied by the record's owner because no
  open route to the paper exists. Three claims tested, none general. The
  finding worth more than the headline is in Appendix C: the same `tanh`
  network, binned evenly in *net input* instead of evenly in *activity*, shows
  **no compression** — because `I(h;X)` in a deterministic network is infinite
  and every finite number is a property of an imposed noise model.
---

# NOTE-253: The information-bottleneck rebuttal, and the assumption it makes visible

## Contribution

Takes the three claims of [LIT-508](../literature.d/LIT-508.md) — two phases, compression
causes generalization, compression comes from SGD's diffusion — and tests each
in the setting that produced them, using the original authors' released code.
None survives as a general statement.

## Key results

**The compression phase tracks the nonlinearity, not the learning.**
Replicating the original 12-10-7-5-4-3-2 network with `tanh` reproduces the
two phases. Swapping to ReLU, everything else held, `I(X;T)` increases
monotonically in every hidden layer. Confirmed across three estimators —
binning, the Kolchinsky-Tracey kernel density estimator, and the Kraskov
`k`-nearest-neighbour estimator — and across four activation functions:

| activation | shape | compresses? |
|---|---|---|
| `tanh` | double-saturating | yes |
| softsign | double-saturating, gentler | modestly |
| ReLU | single-sided | no |
| softplus | single-sided, smooth | no |

**The minimal model that explains it.** Three neurons, `X ~ N(0,1)`,
`h = f(w₁X)`, `T = bin(h)`. Because the map is deterministic, `H(T|X) = 0` and
`I(T;X) = H(T)` exactly. As `w₁` grows, a `tanh` unit saturates and the
distribution of `T` collapses into the two extreme bins — about **1 bit**, a
coin flip. A ReLU unit puts half its inputs in the zero bin and spreads the
rest, so entropy grows without bound. Weights must grow for a `tanh` network
to compute anything nonlinear at all, so the compression phase is what
training a saturating network through a binning estimator looks like.

**The result that generalizes past this paper, in Appendix C.** The same
`tanh` network and the same training run, with bin edges at
`tanh(linspace(-50, 50, N))` — evenly spaced in *net input* rather than in
*activity* — shows **no compression in most layers**. At full machine
precision the information is pinned at `log₂(P) = 12` and barely moves.

The reason is stated plainly: in a deterministic network the continuous
`I(h;X)` is **infinite**, since `H(h|X) = -∞`. A finite number requires
binning or added noise, and *neither is present in the network during
training or testing*. Every information plane in this literature is therefore
a plot of a quantity the analyst created.

**Two consequences the paper draws and almost nobody quotes.** The data
processing inequality does not apply to these estimates, because the noise is
added per-layer for analysis and does not propagate through the network. And
the mutual information is **not invariant to invertible reparameterization**:
for a linear network, scaling `w₁ → w₁/c` and `w₂ → cw₂` computes an
identical input-output map and therefore generalizes identically, but gives
`I(T;X) = log(w₁²/c² + σ²) − log(σ²)`, which depends on `c`. So the promise
that mutual information is a "common currency" for comparing architectures
fails on architectures that compute the same function.

**Compression and generalization dissociate in all four combinations.**

| | generalizes | overfits |
|---|---|---|
| **compresses** | Fig 1A, `tanh` | Fig 4C-D, `tanh` on 30% of data |
| **does not compress** | Fig 1B ReLU; Fig 3 linear | Fig 4A-B, linear, `Ni = P = 100` |

The linear student-teacher setting is what makes this clean: mutual
information is computed in closed form with no binning at all.

**Stochasticity is not the cause.** `tanh` networks compress as much under
full-batch gradient descent as under SGD. The gradient signal-to-noise
transition the original paper ties compression to appears in ReLU networks
that never compress, on MNIST, and in a 1-1-1 linear network where
compression is impossible by construction — so the two-phase gradient
behaviour is general and unrelated.

There is also a theoretical objection: the maximum-entropy argument is about
the distribution of weights *across training runs*, while `H(X|T)` is
uncertainty about inputs from the data distribution. No general reason
connects a single draw from the former to maximizing the latter.

**What it concedes, in §5.** Partition the input into 30 task-relevant and 70
task-irrelevant dimensions and the information about the *irrelevant*
subspace does compress — concurrently with fitting, not in a later phase,
while overall `I(X;T)` still rises. So the intuition that learning discards
noise is right; the claim that this shows up as a second phase in total input
information is what fails.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The compression phase is a property of double-saturating nonlinearities under a binning/noise assumption | strong | replication with original code, three estimators, four activations, exact minimal model |
| C2 | Any finite `I(X;T)` for a deterministic network is an artifact of the analyst's noise model | **strong, and analytic** | `H(h|X) = -∞`; two binning schemes give opposite conclusions on one run |
| C3 | Compression and generalization are not causally linked | strong | four-cell dissociation, with exact MI in the linear cases |
| C4 | SGD stochasticity does not cause compression | strong | full-batch GD compresses; SNR transition without compression in three settings |

## Limitations

**The linear analysis uses one input covariance.** All input dimensions have
equal variance and teacher weights are drawn independently, so no subspace is
privileged. The paper says so, and says it has not investigated whether real
tasks put the signal in the high-variance directions — where compression might
appear for reasons that are about the data rather than the estimator.

**The ReLU binning choice is the one thing later contested.** Bins are placed
over a single global range `[0, m]`, `m` the largest activity anywhere in the
network over all of training. [LIT-507](../literature.d/LIT-507.md) shows the last layer
dominates that maximum, so earlier layers are under-resolved. The KDE and
Kraskov confirmations do not use that binning, which is why C1 does not fall
with it — but the specific ReLU panel is fair game.

**The dissociation is demonstrated, not quantified.** Four cells, each from a
small setting. Nothing here says how often compression and generalization
coincide in practice, which is what a reader wanting to keep the IB heuristic
would ask.

## Bearing on the record

**This is the rebuttal [#220](https://github.com/dmarx/anthology-of-the-sota/issues/220) was blocked on, and it changes what the unit is
about.** The issue framed the IB dispute as a third instance of "the finding
was in the measurement", alongside emergence and grokking under
[SOTA-200](../practices.d/SOTA-200.md). That framing is too weak. In the emergence case the
underlying quantity is real and a discontinuous scoring rule made it look
sharp. Here the underlying quantity is **infinite**, and every number ever
plotted on an information plane was manufactured by a choice the paper
reporting it usually does not defend. That is a different and worse failure,
and it is why this supports its own practice rather than a third bullet on
[SOTA-200](../practices.d/SOTA-200.md).

**It does not refute the information bottleneck principle**, and says so. The
principle is more general; the paper addresses one scheme for linking it to
practice. It explicitly points at stochastic networks with explicit
compression regularizers as where the idea may still pay.

## Open questions

- **Does the IB-bound claim survive?** The original's third finding is that
  converged layers sit on or near the IB bound. A bound in units of a
  quantity that is infinite without an imposed noise model inherits every
  problem above, and this paper does not take it up.
- **Is the computational benefit of depth still standing?** The original's
  fourth claim — depth dramatically reduces epochs to good generalization — is
  examined by neither this paper nor [LIT-507](../literature.d/LIT-507.md).
- **Do real tasks put signal in high-variance input directions?** Named by the
  paper as uninvestigated, and the one route by which compression might be
  about data rather than instruments.
