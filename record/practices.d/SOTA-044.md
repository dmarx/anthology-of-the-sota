---
number: 44
status: 'Active'
title: 'Pin memory for CPU-GPU transfers'
version: 1
tags:
- data-pipeline
# Secondary: page-locked host memory and DMA are how a transfer is executed,
# which is the systems-optimization blurb; it is also the topic the evidence
# shares with this practice.
- systems-optimization
date: '2026-08-24'
# Was LIT-050 (Mohan et al., CoorDL). Read in full, it never mentions pinned
# or page-locked memory or host-to-device transfer; its mitigations are
# caching, partitioned caching and coordinated prep. Moved to the paper that
# measures pinned against pageable transfer.
source:
- LIT-tmpiutyj
# Searched and not found: no paper this record can name FIRST MADE this
# recommendation. Was LIT-050, which does not discuss it. The advice is
# NVIDIA's — the CUDA C Programming Guide's page-locked host memory section
# and the 2012 developer note "How to Optimize Data Transfers in CUDA C/C++",
# which LIT-tmpiutyj itself cites for the mechanism — and it reached deep
# learning as a framework default: the PyTorch paper (arXiv 1912.01703)
# says only that its DataLoader manages pinned CUDA memory "to improve
# throughput", with no measurement, years after the CUDA docs. The origin is
# vendor documentation, not a paper; a URL note for it would be weaker than
# leaving this empty (ADR-009). Naming a paper that recommended pinning
# before the CUDA documentation did is how a reader refutes this (ADR-053 §2).
introduced_by: []
summary: >-
  Afroz et al. (2025), LIT-tmpiutyj — [ARXIV-2511.14124](https://arxiv.org/abs/2511.14124). Host-to-device copies
  from pinned memory ran at 24.74 GB/s against 10.16 GB/s from pageable
  memory on PCIe 4.0; the advice itself is NVIDIA's, not a paper's.
---

# SOTA-044: Pin memory for CPU-GPU transfers

## Source

Afroz et al. (2025), LIT-tmpiutyj — [ARXIV-2511.14124](https://arxiv.org/abs/2511.14124).

LIT-tmpiutyj measured the difference this practice rests on. On an NVIDIA
L40S over PCIe 4.0 ×16, a 16 MB FP32 copy from host to device took 1.65 ms
from pageable memory and 0.68 ms from pinned memory — 10.16 against
24.74 GB/s — and the 8 MB FP16 and device-to-host rows show the same
better-than-twofold gap. It was measured to motivate a tensor-offloading
system, not an input pipeline, and it reports copy bandwidth rather than
overlap with compute; the copy is the same copy, but the overlap argument
below is the CUDA programming model's, not a result anyone in the record
measured.

That paper is not where the advice comes from, and nor was the data-stall
study this practice used to cite, which never discusses pinning. The
recommendation is NVIDIA's own CUDA documentation, and frameworks made it a
loader option long before anyone in this record measured it; no paper can be
named as its origin, so `introduced_by` is left empty.

## What pinning actually buys

Pageable host memory cannot be the source of an asynchronous DMA transfer:
the driver has to stage it through an internal pinned buffer first, so the
copy is synchronous from the program's point of view and cannot overlap with
compute. Allocating the staging buffer as page-locked from the start removes
the extra copy and lets the transfer run on a separate stream while the GPU
is still working on the previous batch.

For an input pipeline that is already close to keeping up, that overlap is
the difference between a small stall per step and none.

## The cost is real and is a system-wide one

Pinned pages cannot be swapped or moved. Pinning aggressively — many worker
processes each with a large prefetch depth — takes memory away from the page
cache that the same pipeline depends on for repeat reads ([SOTA-042](SOTA-042.md)), and on a
shared machine it takes it away from other jobs. The failure is not an error;
it is the loader getting slower for reasons that do not appear in its own
metrics.

So this is a default worth having and not a knob worth maximising, and
whether it is helping at all is a question for [SOTA-045](SOTA-045.md)'s measurement rather
than for argument.
