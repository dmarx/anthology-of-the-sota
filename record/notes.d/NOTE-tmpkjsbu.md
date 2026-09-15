---
status: Read
paper: LIT-tmpt15qm
title: 'A Growing Neural Gas Network Learns Topologies'
version: 1
tags:
- representation-and-encoding
date: '2026-09-15'
summary: >-
  Topology learning can be done incrementally and locally: connect the two
  nearest units to each input (Hebbian edge), age and prune stale edges, and
  periodically insert a new unit between the unit with maximum accumulated
  squared error and its worst-error neighbor.
---
# NOTE-tmpkjsbu: A Growing Neural Gas Network Learns Topologies

## Contribution

Introduces the Growing Neural Gas (GNG) algorithm, an incremental
unsupervised network that learns the topology of a data distribution by
combining competitive Hebbian learning with periodic insertion of new units
at locations of high accumulated quantization error. Unlike Martinetz &
Schulten's neural gas, GNG uses only constant parameters (no annealing) and
network size need not be specified in advance.

## Key insight

Topology learning can be done incrementally and locally: connect the two
nearest units to each input (Hebbian edge), age and prune stale edges, and
periodically insert a new unit between the unit with maximum accumulated
squared error and its worst-error neighbor. Because new units are
interpolated from existing well-placed ones, no decaying global parameters
(learning rate, neighborhood width) are needed — adaptation can continue
indefinitely until a user-defined criterion is met.

## Assumptions

- Stationary input distribution P(xi) over R^n from which i.i.d. signals are
  drawn
- Euclidean distance is meaningful for nearest/second-nearest selection
- Constant hyperparameters (eps_b, eps_n, alpha, d, a_max, lambda) are
  appropriate throughout training
- No formal convergence assumptions — paper is empirical/algorithmic

## Key results

- **Informal (no formal theorem).** Edges produced by competitive Hebbian
  learning form a subgraph of the Delaunay triangulation (the 'induced
  Delaunay triangulation') which optimally preserves topology of P(xi)
  *Holds when:* Result attributed to Martinetz (1993); GNG tracks this graph
  as units move.
- **Empirical demonstration.** GNG adapts to distributions of varying
  intrinsic dimensionality and clustered distributions, producing center
  distributions comparable to NG with 100 units
  *Holds when:* Demonstrated with lambda=100, eps_b=0.2, eps_n=0.006,
  alpha=0.5, a_max=50, d=0.995

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | An incremental growing network with only constant parameters can learn topology as well as the neural gas method that requires annealed parameters and a pre-specified size | moderate | Empirical comparison in figures 2 and 3 |
| C2 | Competitive Hebbian edge insertion plus local edge aging tracks the induced Delaunay triangulation as units move | moderate | Informal argument grounded in Martinetz (1993) |
| C3 | Inserting new units at the location of maximum accumulated squared error reduces quantization error and adapts local resolution to data density | moderate | Algorithmic design plus empirical demonstration |
| C4 | Initializing inserted units by interpolation between existing well-adapted units enables training without parameter annealing | weak | Informal argument in discussion |

## Method

**Growing Neural Gas (GNG).**

Maintain a graph of units with reference vectors in R^n. For each input xi:
(1) find nearest s1 and second-nearest s2; (2) increment age of edges from
s1; (3) accumulate squared distance ||w_s1 - xi||^2 in s1's error counter;
(4) move s1 by eps_b toward xi and topological neighbors by eps_n; (5) reset
(or create) the s1–s2 edge to age 0; (6) remove edges older than a_max and
any resulting isolated units. Every lambda inputs, insert a new unit halfway
between the maximum-error unit q and its highest-error neighbor f, rewire
edges, and decay q's and f's errors by factor alpha. After each step, decay
all error counters by d. Continue until a stopping criterion is met.

- Competitive Hebbian edge creation between nearest and second-nearest unit
- Local edge aging and removal to track moving induced Delaunay
  triangulation
- Per-unit accumulated squared-error counter to identify high-error regions
- Periodic insertion (every lambda steps) at site of maximum accumulated
  error
- Constant learning rates eps_b for winner and eps_n for topological
  neighbors

## Concepts

- **Induced Delaunay triangulation** — Subgraph of the Delaunay
  triangulation containing only edges whose corresponding Voronoi-cell
  border lies in regions where P(xi) > 0; provably topology-preserving.
- **Competitive Hebbian Learning (CHL)** — For each input, connect the two
  closest centers by an edge; constructs the induced Delaunay triangulation.
- **Topology learning** — Finding a graph structure over R^n whose
  connectivity reflects the topology of a data distribution P(xi).
- **Dead units** — Centers placed outside the support of P(xi) that develop
  no edges and contribute nothing to topology learning.

## Connections

**Builds on.**

- A neural-gas network learns topologies (Martinetz & Schulten, 1991) — GNG
  replaces the annealed neural gas adaptation with constant-parameter
  incremental growth while keeping CHL for edge construction.
- Competitive Hebbian learning rule forms perfectly topology preserving maps
  (Martinetz, 1993) — Adopts CHL as the edge-insertion mechanism.
- Growing cell structures (Fritzke, 1994b) — Reuses the error-driven
  incremental insertion idea but removes the fixed-dimensional topology
  constraint.

## Recommendations

- **R1** — Use error-driven incremental insertion when the appropriate model
  size is unknown; this avoids restarts that fixed-size methods require.
  *Topic:* model sizing · *Strength:* moderate · *When:* Unsupervised topology
  learning or vector quantization on stationary distributions of unknown
  complexity.
- **R2** — Prefer constant-parameter algorithms with local insertion over
  schedule-based annealing when continual or open-ended learning is desired.
  *Topic:* training schedules · *Strength:* moderate · *When:* When training
  horizon is unknown or learning must continue indefinitely.
- **R3** — Initialize new units by interpolation from well-adapted neighbors
  rather than randomly to avoid the need for global neighborhood-width
  annealing.
  *Topic:* warm starts · *Strength:* moderate · *When:* Incremental/growing
  network architectures.

## Bearing on the record

Growing neural gas. Filed for the vector-quantization line; nothing in the
record cites it.

## Limitations

- No formal convergence or consistency theorems
- Assumes stationary input distribution; behavior under drift is not
  analyzed
- Requires choosing 6 hyperparameters (lambda, eps_b, eps_n, alpha, d,
  a_max) and a stopping criterion
- Empirical evaluation is limited to 2D toy distributions
- Edge aging threshold a_max effectively reintroduces a time-scale parameter
  despite the 'no annealing' claim

## Open questions

- How should hyperparameters be chosen as a function of intrinsic data
  dimensionality?
- Does GNG retain its properties on non-stationary or streaming
  distributions?
- Can the insertion criterion be generalized for supervised tasks (later
  pursued as incremental RBF networks)?
- What is the asymptotic relationship between the GNG graph and the true
  induced Delaunay triangulation?
