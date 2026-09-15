---
number: 139
status: Read
formerly:
- NOTE-tmporee4
paper: LIT-298
title: 'On the Global Convergence of Gradient Descent for Over-parameterized Models using Optimal Transport'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  Over-parameterized particle gradient descent on F_m(u_1,...,u_m) can be
  viewed as a discretization of a Wasserstein gradient flow on measures.
  Although the non-convex landscape has many local minima, homogeneity of Phi
  and V plus a "separation" property of the initialization support — preserved
  along the flow — force any limit point to be a global minimizer.
---
# NOTE-139: On the Global Convergence of Gradient Descent for Over-parameterized Models using Optimal Transport

## Contribution

Establishes asymptotic global convergence of particle gradient descent for a
class of non-convex measure optimization problems (including sparse
deconvolution and two-layer neural network training) in the many-particle
limit. The key technical tool is recasting particle gradient flow as a
Wasserstein gradient flow in the space of probability measures, exploiting
homogeneity of Phi and V. Provides results for both 2-homogeneous (ReLU) and
partially 1-homogeneous (sigmoid, sparse spikes) settings.

## Key insight

Over-parameterized particle gradient descent on F_m(u_1,...,u_m) can be
viewed as a discretization of a Wasserstein gradient flow on measures.
Although the non-convex landscape has many local minima, homogeneity of Phi
and V plus a "separation" property of the initialization support — preserved
along the flow — force any limit point to be a global minimizer. The many-
particle limit plays the role of a mean-field limit that makes escaping
spurious stationary points generic.

## Assumptions

- R convex, differentiable, with dR Lipschitz on bounded sets and bounded on
  sublevel sets
- Phi differentiable with locally Lipschitz dPhi; V semiconvex
- Sublinear growth of |dPhi| and |dV| on nested sets Q_r
- 2-homogeneous case: Phi and V both positively 2-homogeneous on R^d
- Partially 1-homogeneous case: Phi(w,theta)=w*phi(theta),
  V(w,theta)=|w|*V_tilde(theta)
- Sard-type regularity: regular values of theta -> <f,Phi(theta)>+V(theta)
  dense in range
- Initialization support satisfies a separation property (e.g., separates
  two spheres, or support includes {0} x Theta)
- Wasserstein gradient flow assumed to converge (weakly, after projection)

## Key results

- **Theorem 3.3 (2-homogeneous case).** If initialization support separates
  r_a S^{d-1} from r_b S^{d-1} and mu_t converges in W_2, then
  lim_{t,m->infty} F(mu_{m,t}) = min F.
  *Holds when:* Requires ReLU-type 2-homogeneity, Sard regularity, convex
  smooth R.
- **Theorem 3.5 (partially 1-homogeneous case).** If initialization support
  separates {-r}xTheta from {r}xTheta (e.g., supported on {0}xTheta) and
  h^1(mu_t) converges weakly, then lim F(mu_{m,t}) = F*.
  *Holds when:* Sigmoid/sparse-deconvolution setting; requires boundary
  conditions on phi.
- **Theorem 2.6 (many-particle limit).** Empirical measures mu_{m,t} from
  particle gradient flow converge (in W_2) to the unique Wasserstein
  gradient flow of F as m -> infty.
  *Holds when:* Under Assumptions 2.1 with mu_{m,0} -> mu_0 in W_2.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Particle gradient flow converges to global minimizers in the many-particle limit despite non-convexity. | strong | Theorems 3.3, 3.5 (qualitative, non-quantitative) |
| C2 | Slight over-parameterization m > m_0 is empirically sufficient to reach global optima, vastly better than convex gridding approaches. | moderate | Synthetic experiments on sparse deconvolution and shallow NNs (Figure 3) |
| C3 | Homogeneity of Phi and V is the key structural property enabling escape from spurious local minima, not noise/mixing. | strong | Propositions C.1, C.4 (escape criteria) |
| C4 | Initialization on {0}xTheta (or symmetrically around origin on a sphere) is the 'right' choice for good particle-complexity. | moderate | Figure 6 ablation and proof structure (Lemma C.18) |

## Method

**Particle gradient flow (continuous-time gradient descent on weights and
positions).**

Parameterize measure as mu_m = (1/m) sum_i delta_{u_i} and run continuous-
time gradient descent u'(t) in -m*subgrad F_m(u(t)). Initialize particles
with support satisfying a separation property (e.g., on {0}xTheta for
1-homogeneous case, or on a sphere for 2-homogeneous/ReLU case). In the
many-particle limit, the empirical measure evolves as a Wasserstein gradient
flow of F; homogeneity + separation preservation imply any convergent limit
is a global minimizer.

- Lifting: convert signed-measure problem over Theta to probability-measure
  problem on Omega = R x Theta
- Wasserstein gradient flow as mean-field limit
- Separation property of initialization support (preserved by the flow via
  topological degree)
- Escape criterion: if F'(mu) not nonnegative, particles in sublevel set
  eventually leave

## Concepts

- **Wasserstein gradient flow** — Absolutely continuous curve in P_2(Omega)
  satisfying the continuity equation d_t mu = -div(v_t mu) with v_t in
  -subgrad F'(mu_t).
- **Lifting** — Reformulation of signed-measure problem on Theta as
  positive-measure problem on R x Theta with Phi(w,theta)=w*phi(theta),
  V(w,theta)=|w|.
- **Separation property** — Support of mu_0 is a set that topologically
  separates two prescribed boundary sets (e.g., two spheres or two
  hyperplanes).
- **Positively p-homogeneous** — f(lambda x) = lambda^p f(x) for all lambda
  > 0.
- **Particle-complexity** — Number of particles m needed for gradient flow
  to reach a global minimizer (empirically m slightly > m_0).

## Connections

**Builds on.**

- Gradient flows in metric spaces and in the space of probability measures
  (Ambrosio-Gigli-Savaré, 2008) — Uses abstract Wasserstein gradient flow
  theory for existence/uniqueness.
- Stochastic particle gradient descent for infinite ensembles (Nitanda-
  Suzuki) — Shared viewpoint of particle methods as discretizations of
  measure optimization; this paper adds global convergence.
- A mean field view of the landscape of two-layer neural networks (Mei-
  Montanari-Nguyen) ([LIT-271](../literature.d/LIT-271.md)) — Concurrent mean-field analysis of two-
  layer NNs; complementary — they quantify SGD to mean-field limit, this
  paper proves global convergence via homogeneity.

**Related.**

- Neural networks as interacting particle systems (Rotskoff-Vanden-Eijnden)
  ([LIT-365](../literature.d/LIT-365.md)) — Concurrent mean-field analysis of two-layer NNs.
- Mean field analysis of neural networks (Sirignano-Spiliopoulos) (LIT-
  tmp7pep0) — Concurrent mean-field analysis with different focus on SGD
  convergence to PDE limit.

## Recommendations

- **R1** — Initialize two-layer network parameters symmetrically around the
  origin (e.g., on a small sphere or with zero second-layer weights) to
  satisfy the separation property that enables escape from spurious minima.
  *Topic:* initialization · *Strength:* moderate · *When:* Training shallow
  networks where mean-field / over-parameterization is operative.
- **R2** — Over-parameterize two-layer networks modestly beyond problem
  intrinsic complexity m_0; very large m is not required for global
  optimality empirically.
  *Topic:* width selection · *Strength:* moderate · *When:* Shallow networks
  with homogeneous activations on synthetic-style problems.
- **R3** — Prefer particle/neuron gradient descent over fixed-grid convex
  approximation of measure optimization problems; particle-complexity is
  dramatically lower.
  *Topic:* optimization design · *Strength:* strong · *When:* Convex-in-measure
  problems with homogeneous feature maps.

## Bearing on the record

The optimal-transport route to global convergence, and the one of the four
that states an initialization condition a practitioner could act on — cover
the sphere, do not start concentrated.

## Limitations

- Results are asymptotic and non-quantitative: no rate in m or t.
- Requires convergence of the Wasserstein gradient flow as an assumption; no
  proof of convergence given.
- Sard-type regularity is assumed, hard to verify in practice (especially
  the boundary condition at infinity for sigmoid NNs).
- Only shallow (two-layer) networks; multi-layer extension left open.
- ReLU requires a reparameterization (signed-square) to ensure
  differentiability.
- Experiments are on synthetic low-dimensional or teacher-student setups.

## Open questions

- Quantitative particle-complexity bounds: how many particles m suffice as a
  function of problem parameters?
- Extension to deep (multi-layer) networks where homogeneity structure is
  less clean.
- Conditions ensuring convergence of the Wasserstein gradient flow
  (Lojasiewicz inequalities in Wasserstein space).
- Tightness of the separation property — can weaker initialization
  conditions still yield global convergence?
