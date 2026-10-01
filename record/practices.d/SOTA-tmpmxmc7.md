---
status: Proposed
promote_when: >-
  A group other than the tutorial's authors runs these two tests against
  KFAC implementations it did not write — the existing packages, or the KFAC
  inside a published influence-function or optimizer codebase — and reports
  what they found: which implementations fail, on which flavour, and whether
  the failure was a factor-order or reduction-factor error of the kind the
  source predicts. A bug caught this way and shown to have moved a published
  number would settle it outright. What would NOT meet it: another library
  saying in its documentation that it runs these tests, which is adoption
  (DP-005); or a further derivation of an exact case, which adds a test
  without showing that testing catches anything.
consensus: unreplicated
consensus_note: >-
  One group, and the evidence is a derivation rather than a measurement. The
  identities themselves are not in doubt — they are proved, and the
  deep-linear case is Bernacchia et al. (2018), which the record does not
  hold. What is unmeasured is the practical half: that these are the bugs
  KFAC implementations actually ship with, and that the two tests catch them.
  The only support for that is the authors' report of their own experience,
  and the same group's library already runs the tests, so its use is not
  independent. Read as of 2026-10.
title: 'Test a Kronecker-factored curvature implementation against the cases where KFAC is exact before trusting it'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
date: '2026-10-01'
source:
- LIT-tmpwhqat
# The earliest statement the record holds is the same first author's
# curvlinops position paper (January 2025), which says its KFAC "tests KFAC's
# equivalence to the block-diagonal GGN, empirical Fisher, or type-I Fisher"
# using the scenarios of Bernacchia et al. (2018) and Eschenhagen et al.
# (2023). Neither of those is in the record, and neither states the
# recommendation: the first proves the deep-linear identity, the second
# defines the weight-sharing variants. The tutorial cites curvlinops as the
# fuller implementation of what it teaches.
introduced_by:
- LIT-tmp7eqbw
implementations:
- 'f-dangel/kfac-tutorial'
- 'curvlinops'
summary: >-
  Dangel et al. (2025), [LIT-tmpwhqat](../literature.d/LIT-tmpwhqat.md), §5.2 — a tutorial, so the evidence is a
  derivation, not a training run. KFAC's averaging step is exact whenever the
  layer inputs or the backpropagated vectors do not depend on the data point.
  That gives two tests: a single data point, where KFAC equals the GGN and the
  empirical Fisher exactly and the Monte-Carlo flavour converges to the GGN;
  and a deep linear network under square loss on arbitrary data, where the GGN
  and Monte-Carlo identities still hold and the empirical-Fisher one does not.
  The second is the one the paper says catches scaling bugs.
---

# SOTA-tmpmxmc7: Test a Kronecker-factored curvature implementation against the cases where KFAC is exact before trusting it

## Source

Dangel, Mucsányi, Weber and Eschenhagen (2025), [LIT-tmpwhqat](../literature.d/LIT-tmpwhqat.md) — KFAC From
Scratch, §5.2 and the cheatsheet in §6; with the same first author's
curvlinops position paper, [LIT-tmp7eqbw](../literature.d/LIT-tmp7eqbw.md), as the earliest statement of the
practice the record holds.

## The claim

KFAC approximates each layer's block of a curvature matrix as a Kronecker
product `A ⊗ B`, with `A` built from the layer's inputs and `B` from vectors
backpropagated to its outputs. The approximation is in one step: an average
over data is pulled inside each factor. [LIT-tmpwhqat](../literature.d/LIT-tmpwhqat.md) derives that this step is
exact whenever either the inputs `{x_n}` or the backpropagated vectors
`{g_n,c}` do not depend on the data point `n`. Build two tests on that, in
double precision, and run them on every layer before using the factors for
anything:

| test | KFAC of the GGN (type-II) | KFAC of the MC Fisher | KFAC of the empirical Fisher |
|---|---|---|---|
| **one data point** (any MLP, any pointwise activation, NLL loss) | equals the GGN | converges to the GGN as samples `M → ∞` | equals the empirical Fisher |
| **deep linear net, square loss, arbitrary data** | equals the GGN | converges to the GGN as `M → ∞` | **does not** equal the empirical Fisher |

The single-point case holds because the sum over `n` disappears. The
deep-linear case holds because the network is linear in each layer's weights,
so the Jacobian from a layer's output to the prediction is constant, and under
square loss the backpropagated vector is a column of the identity (GGN) or a
standard normal draw (MC Fisher) — neither depends on `n`. For the empirical
Fisher it is the residual `y_n − f_n`, which does, and so that flavour is not
exact there. A test suite that expects all three to match on the deep linear
net is wrong; one that expects the empirical flavour to fail there is
checking something.

The paper assigns the two tests different jobs. The single-point test is "a
basic functionality check for KFAC, particularly regarding the criterion
function and its backpropagated vectors". The deep-linear test "is useful for
preventing scaling bugs in the Kronecker factor computations" — the loss's
reduction factor carried into the wrong factor, or not at all. A third bug
the tests catch by construction is the factor order: under the column-major
flattening the literature uses the block is `A ⊗ B`, under the row-major
flattening PyTorch uses it is `B ⊗ A`, and comparing against the exact
matrix under the flattening you actually use is what exposes a swap.

[LIT-tmp7eqbw](../literature.d/LIT-tmp7eqbw.md) states the practice six months earlier, as what its library
does: testing KFAC "is challenging because they only become exact in special
settings", without testing it "can easily introduce scaling bugs where a
Kronecker factor is off by a scalar", and so its KFAC is tested against the
block-diagonal GGN, empirical Fisher and type-I Fisher in exactly these
scenarios. That is the origin as far as the record can see. It says the
scenarios "are not comprehensive".

## Why a derivation is enough to file this, and not enough to make it Active

The record already files practices whose evidence is a proof:
[SOTA-383](SOTA-383.md) is `Active` with half its claim a proof that no unbiased FID
estimator exists, and [SOTA-314](SOTA-314.md) is `Active` on one paper because its reason is
proved rather than measured. In both, the proof is evidence *about the
recommendation* — it is the reason to do the thing. Here the derivation
establishes that the two test oracles are correct, which is half of what the
practice says, and is not in question.

The other half is that these tests are worth running — that KFAC
implementations really do ship with reduction-factor and factor-order
errors, and that these two cases find them. [LIT-tmpwhqat](../literature.d/LIT-tmpwhqat.md)'s support for that is
its authors' experience ("some of the authors themselves have dealt with
these challenges and experienced the discomfort of not being able to fully
test their code") and no count of bugs found in anything. That is a reason
the practice is cheap rather than a reason it is effective, and it is why
this is `Proposed`.

## Conditions

- **It tests the factors, not the optimizer.** Passing says the Kronecker
  factors are the ones KFAC defines. It says nothing about damping, inverse
  updates, or whether KFAC trains faster than anything; [LIT-tmpwhqat](../literature.d/LIT-tmpwhqat.md) runs no
  training experiment.
- **Necessary, not sufficient.** Neither case exercises a nonlinearity whose
  Jacobian varies across data points, which is exactly where the
  approximation is an approximation. A bug that only appears there passes
  both tests.
- **Fully-connected layers without weight sharing.** The tutorial defers the
  expand and reduce variants that transformers and convolutions need, and
  eigenvalue-corrected KFAC. It notes that the deep-linear test survives an
  independent sequence dimension; beyond that it gives no exact case.
- **The Monte-Carlo identity is a limit.** It holds as the number of sampled
  labels grows, so that row of the test is a tolerance check over many
  samples, not an equality, and a loose tolerance there can hide a small
  scaling error the GGN row would have caught.

## Known implementations

- `f-dangel/kfac-tutorial` (the tutorial's own tests,
  `kfac_tests/mlp_batch_size_1.py` and `kfac_tests/deep_linear_regression.py`)
- `curvlinops`
