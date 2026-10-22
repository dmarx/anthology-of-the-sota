---
status: Active
title: 'Learning Mesh-Based Simulation with Graph Networks'
version: 1
tags:
- physical-sciences
- graphs-and-networks
- model-architecture
date: '2026-10-22'
published: '2020-10-07'
arxiv: '2010.03409'
first_author: 'Pfaff'
keywords:
- 'meshgraphnets'
- 'learned-simulation'
- 'encode-process-decode'
- 'adaptive-remeshing'
- 'cloth'
- 'cfd'
- 'structural-mechanics'
- 'rollout'
implementations:
- 'deepmind-research/meshgraphnets'
summary: >-
  Pfaff, Fortunato, Sanchez-Gonzalez, Battaglia (ICLR 2021), [ARXIV-2010.03409](https://arxiv.org/abs/2010.03409).
  MeshGraphNets: an encode-process-decode graph network that passes messages
  along simulation-mesh edges and, for deforming bodies, along world-space
  proximity edges, trained on one-step targets with input noise and rolled
  out for hundreds of steps. It beats a grid U-Net, a GCN and the particle
  model GNS on cloth, plates and 2D flows, and can learn the remesher's
  sizing field. The quoted 11–290× speedup is a GPU model against CPU
  solvers; on the same CPU it is 4–22×.
extended_by:
- LIT-tmp796kb
---

# LIT-tmpfbgua: Learning Mesh-Based Simulation with Graph Networks

Pfaff, Fortunato, Sanchez-Gonzalez, Battaglia, DeepMind (ICLR 2021) —
[ARXIV-2010.03409](https://arxiv.org/abs/2010.03409)

## Key takeaways

- **Two edge sets** (§3.1): mesh edges carry relative mesh-space and
  world-space displacement and their norms; world edges join nodes within a
  radius in world space that are not mesh neighbors, for contact and
  collision. No absolute position is an input, which gives translation
  equivariance. 15 message-passing blocks with unshared weights, latent
  size 128, residual MLPs with LayerNorm
- **Training**: one-step L2 on the decoded derivative, integrated by forward
  Euler. Gaussian noise added to inputs, with targets corrected for it, is
  what keeps long rollouts stable; the scheme is GNS's and is not ablated
  here
- **Results** (Table 1, RMSE ×10⁻³, 100 test trajectories): one-step errors
  of 0.25–2.34 on the five non-Airfoil datasets, and full-trajectory rollout
  errors of 15.1–151.1. Airfoil is the hard case: one-step 314, rollout-50
  582, full rollout 11,529. A model trained on 400-step trajectories stays
  stable for 40,000 (shown in video)
- **Ablations** (§5): without world edges, rollout RMSE rises 51% on
  FlagDynamic and 92% on SphereDynamic. With absolute positions as node
  features in place of relative edge features, Airfoil full-rollout RMSE is
  26.5 against 11.5. A GCN, even widened and deepened to 15 blocks, does not
  roll out stably on Airfoil. GNS without mesh positions diverges on cloth
- **Grid baseline**: MeshGraphNets has lower rollout RMSE than a 128×128
  U-Net on CylinderFlow and Airfoil. The U-Net misses the wake near the
  airfoil while using four times the cells over a sixteenth of the area
- **Hyperparameters** (Figure 5d): more message-passing steps helps up to
  about 15; the shortest history (h = 1 for cloth, 0 otherwise) is best,
  where GNS used 2–5
- **Generalization**: a flag model trained on ~2k-node meshes runs on a 20k-
  node windsock; Airfoil at steeper angles and higher Mach raises full-rollout
  RMSE from 11.5 to 12.4 and 13.1
- **Speed** (A.5.1): GPU model against the CPU solvers ArcSim, COMSOL and SU2,
  11–290×. Same 8-core CPU for both, 4–22×

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22). It is the mesh-based graph simulator GraphCast
([LIT-tmp796kb](LIT-tmp796kb.md)) builds on, from the same group.

**The speedup is a hardware comparison.** The abstract's "1-2 orders of
magnitude faster" is the GPU column, against solvers with no GPU support. On
equal hardware the gain is 4–22×, which is still real and is the number to
carry. Accuracy is reported as RMSE against the solver it imitates, not
against physical ground truth, and the cloth rollouts decohere after about
50 steps, which is why the bar plots use 50-step error.

**Against the record's other physical-systems model.** Erwin ([LIT-763](LIT-763.md))
reports Airfoil as its clear failure, attributing it to the mesh's density
falling steeply away from the wing. Here mesh-space message passing is
designed for exactly that irregularity, and the absolute-position ablation is
the evidence that relative encoding is what lets it cope. The two papers use
different Airfoil setups, so the numbers do not compare.

Read — [NOTE-tmpf44no](../notes.d/NOTE-tmpf44no.md).
