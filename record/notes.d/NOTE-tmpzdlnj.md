---
status: Skimmed
paper: LIT-tmp796kb
title: 'GraphCast'
version: 1
date: '2026-10-22'
summary: >-
  A graph-network weather model on an icosahedral multi-mesh beats ECMWF's
  deterministic HRES on 90% of 1,380 targets at 0.25°. Main text read in
  full; of the 100-page supplement, the graph construction (3.3, 3.5),
  training (4) and ablations (7.3) were read and the rest skimmed.
---

# NOTE-tmpzdlnj: GraphCast

## Contribution

The first machine-learned medium-range forecaster to beat the leading
operational deterministic system across most of a full scorecard at its own
resolution, with a verification protocol that matches the two systems'
assimilation windows.

## Key insight

**Long range from geometry, not depth.** Superimposing the edges of every
refinement level of an icosahedral mesh gives each node hops of every
length, so 16 message-passing layers cover the globe; removing the coarse
levels costs the lead on geopotential under 5 days.

## Key results

- 90.3% of 1,380 targets better than HRES, 89.9% significantly; 99.7% of
  1,180 when 50 and 100 hPa are excluded
- z500 RMSE skill score 7–14% better across 10 days
- Cyclone tracks better from 18 hours to 4.75 days in paired comparison
- Optimally blurring both models: 88.0% of targets still better

## Limitations

- **Deterministic.** No comparison with the ensemble, and MSE training
  makes long-lead forecasts smooth
- **Coarser than HRES** in space, levels and time step
- **Depends on reanalysis** produced by the NWP system it is compared with;
  the authors say it should not be read as a replacement
