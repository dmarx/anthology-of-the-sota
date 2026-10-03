---
status: Active
title: 'FFJORD: Free-form Continuous Dynamics for Scalable Reversible Generative Models'
version: 1
tags:
- generative-modeling
- flows-and-transport
date: '2026-10-03'
published: '2018-10-02'
arxiv: '1810.01367'
first_author: 'Grathwohl'
keywords:
- 'continuous-normalizing-flow'
- 'hutchinson-trace-estimator'
- 'free-form-jacobian'
- 'adjoint-method'
- 'bottleneck-trick'
- 'reversible-generative-model'
implementations: []
extends:
- LIT-tmp29nh5
compared_against:
- LIT-tmpgi092
- LIT-tmp086g1
- LIT-644
summary: >-
  Grathwohl, Chen, Bettencourt, Sutskever and Duvenaud, Toronto, Vector and
  OpenAI (2018), [ARXIV-1810.01367](https://arxiv.org/abs/1810.01367). Replaces the CNF's exact Jacobian trace
  with Hutchinson's estimator, one noise vector fixed per solve, so the
  log-density costs O(D) per evaluation and the dynamics network is
  unrestricted (§3, Eq. 8). Best reversible model on all five tabular
  sets, behind the autoregressive MAF-DDSF on four. MNIST 0.99 bits/dim against Glow's 1.05;
  CIFAR-10 3.40 against Glow's 3.35, with under 2% of Glow's parameters.
  Training took about five days on six GPUs, and NFE grows during training
  until it can become "prohibitive" (§6).
---

# LIT-tmpezs1l: FFJORD: Free-form Continuous Dynamics for Scalable Reversible Generative Models

Grathwohl, Chen, Bettencourt, Sutskever and Duvenaud, University of Toronto,
Vector Institute and OpenAI (2018) — [ARXIV-1810.01367](https://arxiv.org/abs/1810.01367). ICLR 2019. Read at
v3 (22 Oct 2018); v1 is 2 Oct 2018.

## Key takeaways

- **An unbiased, linear-cost log-density** (§3.1, Eqs. 7–8, Alg. 1). The
  CNF's trace term costs O(D²) exactly. Tr(A) = E[εᵀAε] for any ε with
  zero mean and identity covariance, and εᵀ(∂f/∂z) is one vector-Jacobian
  product. Fixing ε for the whole solve keeps the dynamics deterministic
  and the estimate unbiased. Cost per evaluation falls to O(DH + D), and
  the network f can be any architecture.
- **A bottleneck lowers the estimator's variance** (§3.1.1, Eq. 9, Fig. 4).
  By the trace's cyclic property the estimate can be taken in the
  narrowest hidden width H rather than D. It sped convergence with Gaussian
  ε and made no difference with Rademacher ε.
- **Density estimation** (Table 2; Table 6 gives three-run standard
  deviations). Tabular test NLL in nats: POWER −0.46, GAS −8.59, HEPMASS
  14.92, MINIBOONE 10.43, BSDS300 −157.40 — better than Real NVP and Glow on
  all five. MAF-DDSF is better on four, TAN on two. Images in bits/dim:
  MNIST 0.99 multiscale (1.05 as one flow) against Real NVP's 1.06 and
  Glow's 1.05; CIFAR-10 3.40 against 3.49 and 3.35.
- **As a VAE posterior it beats every flow it is set against** (§4.3,
  Table 3). Negative ELBO on MNIST 82.82 ± .01 against Sylvester's
  83.32 ± .06, and best on Omniglot, Frey Faces and Caltech Silhouettes,
  with the encoder, decoder and training setup copied from Sylvester flows.
- **NFE tracks the distribution, not the dimension** (§5.2, Fig. 5). VAEs
  with latent dimension 16 to 64 converge to the same NFE. The paper's
  argument: a Gaussian target from a Gaussian base needs a zero field and
  no evaluations at any D.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"State-of-the-art among exact likelihood methods with efficient
  sampling"** (abstract). Glow is better on CIFAR-10, 3.35 against 3.40,
  and the paper calls that "comparable performance" (§4.2). The claim holds
  for the tabular sets and MNIST.
- **"Less than 2% as many parameters as Glow"** (§4.2). The count is
  parameters, not compute. The image models trained 500 epochs on six GPUs
  for about five days (App. B.1). The paper says the method "is slower
  than competing methods" and offers larger batches, which the adjoint's
  memory allows, as the compensation.
- **The NFE problem is stated, not solved** (§6). NFE "tends to grow as
  the models trains and can become prohibitively large". Weight decay and
  spectral normalization reduce it but "hurt performance slightly". Stiff
  dynamics need stiff solvers, which cost more evaluations again; a small
  weight decay kept them non-stiff.
- **The CIFAR-10 and MNIST likelihoods are estimates.** Exact traces were
  infeasible there, so the reported numbers use Hutchinson's estimator,
  whose variance over the validation set the paper bounds below 10⁻⁴ (§4).
- **Solver tolerance biases the objective** (App. C, Fig. 8). Tolerances
  above 10⁻⁵ made the error "non-negligible" during training; images used
  10⁻⁵ and tabular atol 10⁻⁸, rtol 10⁻⁶.
- **The single-scale encoder-decoder FFJORD could not fit CIFAR-10 or SVHN**
  (App. B.1). Only the multiscale architecture borrowed from Real NVP did.

## Which comparisons are like for like

- **The VAE comparison (Table 3) is controlled**: same encoder, decoder,
  learning rate, optimizer, batch size and early stopping as Berg et al.,
  three runs each.
- **The density tables are not.** Baseline rows are the published numbers.
  FFJORD's tabular architectures come from a grid search (App. B.1, Table
  4). Glow uses a learned base distribution and FFJORD and Real NVP a fixed
  Gaussian (§4.2).
- **The 2-D comparison with Glow (Fig. 2)** matches a 100-layer Glow to
  FFJORD's 70–100 solver evaluations and is qualitative.

## Standing in the anthology

It extends Neural ODEs ([LIT-tmp29nh5](LIT-tmp29nh5.md)): the continuous normalizing flow, the
instantaneous change of variables and the adjoint method are that paper's,
and FFJORD replaces the exact trace with a stochastic one so the dynamics
can be an unrestricted network rather than planar-flow units. Neural ODEs
showed the CNF on 2-D toys; FFJORD is where it meets images.

Its Table 2 compares it with Real NVP ([LIT-tmpgi092](LIT-tmpgi092.md)) and Glow
([LIT-tmp086g1](LIT-tmp086g1.md)), and Fig. 2 with a 100-layer Glow on 2-D densities. It
beats both on the tabular sets and MNIST; Glow is better on CIFAR-10.

It is also the baseline the simulation-free line measured itself against.
The stochastic-interpolant flow ([LIT-644](LIT-644.md)) beat FFJORD's tabular NLL on
four of five sets (FFJORD kept BSDS300) at about 400× lower per-epoch cost on MiniBooNE, with the
same vector-field architecture. That cost is the one FFJORD's §6 names: an
ODE solved inside every training step, with NFE that grows. Flow matching
([LIT-630](LIT-630.md)) keeps FFJORD's model class — a CNF evaluated by Theorem 1 — and
drops the simulation from training, which is why the CNF survived and this
way of training it did not.

Filed without a `NOTE`: the takeaways come from one full reading of v3,
appendices included, done for this filing.
