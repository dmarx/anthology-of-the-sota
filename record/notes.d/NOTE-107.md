---
number: 107
status: Read
formerly:
- NOTE-tmp8mk48
paper: LIT-314
title: 'Proving the Limited Scalability of Centralized Distributed Optimization via a New Lower Bound Construction'
version: 1
date: '2026-09-15'
summary: >-
  When server-to-worker communication is non-negligible (tau_s > 0), there is
  a fundamental trade-off: increasing n can improve either the dimension-
  dependent communication term or the variance-dependent compute term, but not
  both—even when all workers share the same data distribution. This exposes an
  inherent scalability wall in centralized federated optimization that
  gradient compression cannot overcome.
---
# NOTE-107: Proving the Limited Scalability of Centralized Distributed Optimization via a New Lower Bound Construction

## Contribution

This paper proves a nearly tight lower bound showing that, even in the
homogeneous (i.i.d.) setting, no algorithm using unbiased random
sparsification compressors can simultaneously scale both the server-to-
worker communication cost (tau_s * d * L*Delta/eps) and the variance-
dependent cost (h * sigma^2 * L*Delta / eps^2) better than poly-
logarithmically in the number of workers n. The result is established via a
new worst-case function construction F_{T,K,a} and a novel proof framework
reducing the bound to a concentration inequality for a random sum.

## Key insight

When server-to-worker communication is non-negligible (tau_s > 0), there is
a fundamental trade-off: increasing n can improve either the dimension-
dependent communication term or the variance-dependent compute term, but not
both—even when all workers share the same data distribution. This exposes an
inherent scalability wall in centralized federated optimization that
gradient compression cannot overcome.

## Assumptions

- The optimizer is zero-respecting: it only activates coordinates that have
  been observed as non-zero in at least one gradient or message.
- Compressors are unbiased random sparsification compressors in U(omega);
  biased compressors (Top-K, signSGD) are not covered by the main theorem.
- The objective is non-convex and L-smooth; the bound may not apply under
  convexity or stronger regularity.
- Server-to-worker communication cost tau_s > 0 (non-negligible downlink);
  if tau_s = 0, the bound degenerates and compression may help.
- Workers sample IID gradients (homogeneous setting); heterogeneous data
  distributions are a strictly easier case for the lower bound.

## Key results

- **Theorem 1.6 / Theorem 4.2 (main lower bound).** Any zero-respecting
  algorithm using U(omega) compressors requires at least Omega(tau_s * d *
  L*Delta / (eps * log^4(n))) + Omega(h * sigma^2 * L*Delta / (eps^2 *
  log^6(n))) time, even in the homogeneous i.i.d. setting with n workers.
  *Holds when:* Non-convex L-smooth objective; n workers; unbiased random
  sparsification compressors with variance parameter omega; tau_s > 0 S2W
  communication cost; gradient variance sigma^2; Delta = f(x_0) - f*.
- **Corollary (tau_s ≈ tau_w regime).** When server-to-worker bandwidth
  equals worker-to-server bandwidth, no compression algorithm achieves
  asymptotically better complexity than Batch Synchronized SGD without
  compression.
  *Holds when:* tau_s = tau_w; homogeneous i.i.d. setting; unbiased
  sparsification compressors.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | No zero-respecting algorithm using unbiased random sparsification compressors can achieve better than poly-log(n) scaling of both tau_s*d*L*Delta/eps and h*sigma^2*L*Delta/eps^2 simultaneously, even in the homogeneous i.i.d. setting. | strong | Formal lower bound Theorem 1.6 and Theorem 4.2 proved via the new worst-case function F_{T,K,a} and a concentration bound on a random sum; the bound is tight up to log^6(n) factors. |
| C2 | When tau_s ≈ tau_w, unbiased sparsified compression provides no asymptotic advantage over uncompressed Synchronized SGD in the centralized distributed setting. | strong | Direct corollary of the lower bound: the lower bound reduces to the complexity of Batch Synchronized SGD, which is already optimal without compression. |
| C3 | The new worst-case function F_{T,K,a} requires K consecutive non-zero coordinates to make gradient progress, preventing multiple workers from simultaneously advancing the optimization front. | strong | Lemma 3.1 proved analytically; the K-dependency in prog^K(x) is the key mechanism that foils the homogeneous setting workaround. |

## Concepts

- **Unbiased compressor** — A randomized mapping C: R^d -> R^d with E[C(x)]
  = x and E[||C(x)-x||^2] <= omega*||x||^2; the family of such compressors
  is denoted U(omega).
- **Zero-respecting algorithm** — An algorithm that never assigns non-zero
  values to a coordinate unless at least one available gradient or
  communicated vector already has a non-zero value there; captures virtually
  all practical distributed methods.
- **Server-to-worker (S2W) communication cost** — The time cost tau_s per
  coordinate for the server to broadcast updated parameters or compressed
  gradients to workers; often assumed free but non-negligible in federated
  settings.
- **prog^K(x)** — The largest index i such that coordinates i, i-1, ...,
  i-K+1 are all non-zero in x; measures how far the optimization front has
  advanced in the new worst-case function.
- **Scalability wall** — The fundamental limit proved here: adding more
  workers n improves the total runtime by at most poly-log(n) when both S2W
  communication cost and variance cost must be reduced simultaneously.
- **Homogeneous (i.i.d.) setting** — The distributed optimization scenario
  where all workers sample gradients from the same distribution; considered
  'easiest' because workers can collaborate more effectively.

## Connections

**Builds on.**

- Lower Bounds for Finding Stationary Points I (Carmon et al., 2020) — The
  new worst-case function F_{T,K,a} directly extends Carmon et al.'s chain-
  like construction F_T by requiring K consecutive non-zero activations to
  make progress.
- Improving the Worst-Case Bidirectional Communication Complexity
  (Gruntkowska et al., 2024) — Gruntkowska et al. proved the lower bound in
  the heterogeneous setting; this paper extends the result to the harder
  (for lower bounds) homogeneous setting.
- Lower Bounds for Non-Convex Stochastic Optimization (Arjevani et al.,
  2022) — Provides the stochastic lower bound framework (computation cost)
  that is combined with the new S2W communication lower bound.

## Recommendations

- **R1** — When designing distributed optimization systems where server-to-
  worker bandwidth is comparable to worker-to-server bandwidth, do not
  expect unbiased gradient compression to yield super-logarithmic scaling
  benefits; prefer increasing batch size or reducing synchronization
  frequency instead.
  *Topic:* system design · *Strength:* strong · *When:* Centralized federated
  learning or parameter-server settings with symmetric or near-symmetric
  bidirectional communication costs.
- **R2** — If tau_s << tau_w (downlink much faster than uplink), worker-side
  compression (e.g., QSGD, Rand-K) remains beneficial for the uplink term;
  the lower bound only eliminates simultaneous improvement of both terms.
  *Topic:* compression strategy · *Strength:* moderate · *When:* Asymmetric
  network environments where downlink bandwidth substantially exceeds uplink
  bandwidth.

## Bearing on the record

A lower bound saying unbiased compression cannot improve uplink and downlink
at once. It bears as the thing that bounds what the rest of the compression
line can be claimed to buy, and a practice about compression should know it
exists.

## Limitations

- The lower bound applies specifically to unbiased random sparsification
  compressors; the paper conjectures but does not prove the bound holds for
  all unbiased compressors (the uncertainty principle provides a partial
  argument).
- The bound is tight only up to poly-logarithmic factors (log^4 to log^6 in
  n); whether logarithms can be eliminated is an open problem.
- The lower bound is for nonconvex objectives; convexity or second-order
  smoothness may allow stronger scalability and break the pessimistic bound.
- The result applies to zero-respecting algorithms; non-zero-respecting
  algorithms (unusual in practice) are not covered.
- Practical compressors like Top-K and Rank-K often perform much better than
  worst-case analysis predicts, so the bound may be overly pessimistic for
  specific architectures.

## Open questions

- Can the poly-logarithmic gap be eliminated, or is there a matching upper
  bound that also has logarithmic factors?
- Does the lower bound extend to biased compressors (e.g., Top-K, signSGD)
  without requiring the uncertainty principle argument?
- Are there alternative (non-compression) approaches to the S2W
  bottleneck—such as local SGD or gossip-based methods—that circumvent this
  fundamental limit?
- Does the scalability wall hold under convexity or additional regularity
  assumptions, or do those settings permit genuinely linear-in-n
  improvement?
