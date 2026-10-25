---
status: Read
paper: LIT-tmpkyvvg
title: 'LINE'
version: 1
date: '2026-10-22'
summary: >-
  First- and second-order proximity objectives with negative sampling,
  trained by sampling edges in proportion to weight. Edge sampling is what
  makes weighted graphs trainable; on sparse graphs second-order proximity
  loses to DeepWalk unless the graph is densified. Read in full.
---

# NOTE-tmp0e38m: LINE

## Contribution

Two explicit objectives for node embedding, one for direct links and one for
shared neighborhoods, that handle weighted and directed graphs, and an edge
sampler that makes SGD stable when edge weights span orders of magnitude.
It embedded a 2M-node, billion-edge word network in under three hours.

## Key insight

**When the loss multiplies each term by a weight that varies by 10⁴, sample
in proportion to the weight instead.** The expected objective is unchanged
and the gradient no longer carries the weight, so one learning rate fits
every edge. Plain SGD on the same objective reaches 14.49% analogy accuracy;
edge sampling reaches 66.10%.

## Key results

- Wikipedia word analogy: LINE(2nd) 66.10%, SkipGram on raw text 63.02%,
  DeepWalk 43.65%, LINE-SGD(2nd) 14.49% (Table 2)
- Flickr, five communities: LINE(1st+2nd) about 3 Micro-F1 points over
  DeepWalk at every label rate (Table 5)
- YouTube at 1% labeled: DeepWalk 39.68, LINE(1st+2nd) 39.01, LINE(2nd)
  32.98; densifying low-degree nodes lifts LINE(2nd) to 36.78 (Table 6)
- On the directed paper-citation network LINE(2nd) beats DeepWalk, 58.42 to
  52.83 Micro-F1 at 10% (Table 8)

## Limitations

- **The best model is a concatenation** that the authors define only for
  supervised use, with the reweighting left to the classifier
- **Second-order proximity fails on low-degree nodes** (Figure 3), and the
  fix is a preprocessing step with its own threshold
- **One run per setting, with paired t-tests** against DeepWalk but no
  spreads shown
- **Labels on Flickr differ from DeepWalk's task**, so cross-paper numbers
  do not compare
