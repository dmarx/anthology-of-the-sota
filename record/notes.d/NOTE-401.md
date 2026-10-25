---
number: 401
status: Read
formerly:
- NOTE-tmpf44no
paper: LIT-822
title: 'MeshGraphNets'
version: 1
date: '2026-10-22'
summary: >-
  A graph network over the simulation mesh, plus world-space edges for
  contact, learns cloth, elastic and fluid dynamics stably over long
  rollouts, and can learn where to refine the mesh. Main text and the
  appendix sections on training, noise and timing read.
---

# NOTE-401: MeshGraphNets

## Contribution

Learned simulation on unstructured, adaptive meshes: message passing in
mesh space approximates the differential operators, world-space edges catch
interactions the mesh does not connect, and a learned sizing field drives a
generic remesher at test time.

## Key insight

**Pass messages where the solver would.** The mesh already encodes which
nodes interact and at what scale; using its edges, with relative positions
as features, gives a model that is resolution-independent and handles meshes
whose density varies by four orders of magnitude.

## Key results

- No world edges: rollout RMSE +51% (FlagDynamic) and +92% (SphereDynamic)
- Absolute instead of relative positions: Airfoil full-rollout RMSE 26.5
  against 11.5
- GCN baselines unstable on Airfoil; GNS diverges on cloth
- Speed: 4–22× on equal CPU hardware, 11–290× with the model on a GPU

## Limitations

- **Accuracy is against the solver**, with no physical constraint enforced;
  energy-conserving integration is named as future work
- **Training noise is borrowed from GNS** and its contribution here is not
  measured
- **Baselines** are a reimplemented GCN and U-Net trained in the same setup;
  stronger grid surrogates (neural operators) are not compared
