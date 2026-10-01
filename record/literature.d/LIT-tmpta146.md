---
status: Active
title: 'TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems'
version: 1
tags:
- data-pipeline
- systems-optimization
- distributed-optimization
date: '2026-10-01'
published: '2016-03-14'
arxiv: '1603.04467'
first_author: 'Abadi'
keywords:
- 'dataflow-graph'
- 'heterogeneous-systems'
- 'distributed-execution'
- 'queues'
- 'input-prefetching'
implementations:
- TensorFlow
summary: >-
  Abadi et al. (2016), ARXIV-1603.04467 — the TensorFlow white paper (dated
  November 2015). Describes TensorFlow's dataflow-graph interface and its
  execution from a single device to clusters; among its graph features are
  input operations that read from storage directly and queues that let input
  be prefetched from disk while the previous batch is still being computed.
---

# LIT-tmpta146: TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems

Abadi et al. (2016) — ARXIV-1603.04467. The preliminary white paper is
dated November 9, 2015; the arXiv v1 is March 2016.

## Key takeaways

- A computation is a dataflow graph, and one graph runs "with little or no
  change" from phones to distributed systems of hundreds of machines and
  thousands of GPUs. The paper describes the interface and Google's
  implementation of it.
- **Input is part of the graph.** Input operation nodes are configured with
  filenames and yield examples directly from storage into the worker's
  memory, which saves the extra network hop through a client process that
  feeding data would cost (§4.5).
- **Queues decouple input from compute** (§4.6): parts of the graph run
  asynchronously and hand off through blocking Enqueue and Dequeue. "One use
  of queues is to allow input data to be prefetched from disk files while a
  previous batch of data is still being processed by the computational
  portion of a machine learning model." A shuffling queue randomises order
  within a large in-memory buffer.

## Standing in the anthology

Filed as the origin of SOTA-079 (prefetch the next batch during compute).
That practice had been credited to LIT-053, which postdates this by four
years and does not measure prefetching. This paper does not measure it
either: it describes the mechanism as a use of a framework feature, with no
experiment behind it. It is the earliest published statement in an ML
framework paper that the record found; read-ahead and double buffering as
general systems techniques are older, and the record names no paper for them.
