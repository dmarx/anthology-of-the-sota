---
status: 'Proposed'
promote_when: >-
  A second group, on a different weakly-paired corpus, reports filtered against
  unfiltered at matched training steps and with the cost of the filtering
  model counted, and sweeps the rank cutoff rather than fixing it by eye. The
  source fixed its cutoff "based on manual inspection" and measured one cutoff
  at two data scales on six BEIR sets, so a sweep that finds where the gain
  peaks and where it turns into discarding good pairs is what would turn this
  into an instruction with a setting. A further embedding model that ships a
  consistency filter does not count: that is adoption.
consensus: unreplicated
consensus_note: >-
  One group, one ablation table (LIT-tmp62ra1, Table 7, base model, six BEIR
  datasets). The mechanism itself is older and has been used before on
  generated query-passage pairs, where it was tuned and did not help everywhere
  (Promptagator, arXiv 2209.11755, not held). Nobody in the record has re-run
  it on a scraped corpus. Read as of 2026-10.
title: 'When a web-scraped pair corpus is noisy, filter it by self-consistency: keep only the pairs whose passage a model trained on the noisy set ranks near the top'
version: 1
tags:
- data-pipeline
date: '2026-10-01'
source:
- LIT-tmp62ra1
# E5 says it "propose[s]" the filter, and also cites Promptagator (Dai et al.
# 2022, arXiv 2209.11755) for it. Promptagator trains a retriever on its own
# LLM-generated queries and keeps a pair only if that retriever ranks the
# source passage top-1. That is the same mechanism, applied to synthetic
# pairs, and it credits round-trip consistency to Alberti et al. 2019
# (1906.05416). Neither is held. What is first stated here is the use on a
# scraped, not generated, corpus at web scale, as a filter for contrastive
# pre-training. Filing Promptagator would let this field name the older origin.
introduced_by:
- LIT-tmp62ra1
implementations:
- 'E5 (microsoft/unilm)'
summary: >-
  Wang et al. (2022), [LIT-tmp62ra1](../literature.d/LIT-tmp62ra1.md), Table 7. Train a dual encoder on the noisy
  pairs, rank each pair's passage against 1M random passages, and keep the
  pair only if it lands in the top 2. On six BEIR datasets, filtered beat
  unfiltered at 1M pairs (40.7 against 34.9 nDCG@10) and with all pairs (51.6
  against 50.0), though the filtered set is about a quarter the size. One
  cutoff, chosen by inspection and never varied, and the filtering model's
  cost is not counted.
---

<!-- inactive-ok-file: SOTA-243, SOTA-246 — Proposed; named as neighbouring data practices in prose, not cited as support -->

# SOTA-tmpuqury: When a web-scraped pair corpus is noisy, filter it by self-consistency: keep only the pairs whose passage a model trained on the noisy set ranks near the top

## Source

Wang et al. (2022), [LIT-tmp62ra1](../literature.d/LIT-tmp62ra1.md) — E5, §3 and Table 7.

## What to do

Given a large corpus of weak (query, passage) pairs mined from the web:

1. Train a dual encoder on the whole noisy corpus.
2. For each pair, rank its passage against a large pool of random passages
   using that model. E5 used a pool of 1M.
3. Keep the pair only if its own passage ranks in the top `k`. E5 used
   `k = 2`.
4. Pre-train on what is left.

E5 cut about 1.3B pairs to about 270M this way. The stated reason is that
networks fit clean labels before they memorise noisy ones, so a model trained
on the noisy set still agrees with the clean pairs and disagrees with many of
the wrong ones. The paper gives that reason and does not test it.

[LIT-tmp62ra1](../literature.d/LIT-tmp62ra1.md) is the first to recommend this filter for a scraped corpus,
and it says it proposes the technique. It also cites Promptagator (arXiv
2209.11755, not held), which trained a retriever on its own LLM-generated
queries and kept a pair only if the retriever ranked the source passage
top-1. That is the same mechanism applied to synthetic pairs. What E5 adds is
its use on weak pairs mined from the web, at the scale of a billion pairs.

## Evidence

The evidence is one ablation in [LIT-tmp62ra1](../literature.d/LIT-tmp62ra1.md) (Table 7), on the base model,
scored as nDCG@10 on six BEIR datasets:

| pairs | filter | NFCorpus | NQ | FiQA | Quora | DBPedia | SciFact | avg |
|---|---|--:|--:|--:|--:|--:|--:|--:|
| 1M | without | 23.0 | 15.1 | 18.5 | 83.1 | 18.2 | 51.4 | 34.9 |
| 1M | with | 26.8 | 22.7 | 24.5 | 85.0 | 27.5 | 57.5 | **40.7** |
| all | without | 34.5 | 35.4 | 39.1 | 85.7 | 32.9 | 72.5 | 50.0 |
| all | with | 35.8 | 39.0 | 40.0 | 85.7 | 35.4 | 73.7 | **51.6** |

At 1M pairs the filtered set wins on all six datasets, by 5.8 points on
average. With every pair used, the unfiltered set holds about four times as
much data and still loses by 1.6. The filtered set ties on Quora and wins on
the other five. The second comparison is the one that supports the instruction: the
filter is not only choosing a better 1M, it beats having four times more
data.

## Conditions and limits

- **One cutoff, never varied.** E5 set `k = 2` "based on manual inspection of
  data quality". The paper offers no evidence about whether 1, 10 or 100
  would do better or worse. Promptagator, which E5 cites for the technique,
  tuned its cutoff on a validation set and chose top-1. That is a different
  corpus and different pairs, so it does not transfer either.
- **The filtering run is not charged.** Step 1 is a full training run over
  the noisy corpus, and step 2 scores 1.3B pairs against a 1M pool. Table 7
  compares the pre-training runs that follow, not total cost. E5 also states
  a second motive, to "make training costs manageable", so the filter was
  partly chosen to shrink the data and not only to improve it.
- **Measured once, on one model, on six of BEIR's datasets.** There are no
  seeds and no variance. The filter's effect on the full 15-dataset BEIR
  average, or on MTEB, is not separated out.
- **It can hurt where pairs are few.** In Promptagator's use of the same
  mechanism on generated queries, the filter improved 8 of 11 datasets but
  lowered NFCorpus and SciFact, the two with the fewest generated queries.
  In E5's run, those two datasets improved. The direction is therefore not
  settled across settings.
- **It assumes the labels are what is noisy.** The filter keeps pairs that
  are easy for the model, which means it discards hard pairs as well as wrong
  ones. That is the right trade when wrong pairs are common, as in scraped
  Reddit and Common Crawl pairs. On a clean corpus it would discard the
  examples that teach the most.

## Beside the record's other data practices

[SOTA-243](SOTA-243.md) says that with abundant data you should keep the hard
examples. Its Conditions add that the hardest examples and the mislabelled
ones are the same examples, so the upper edge of the kept window should move
down as label noise rises. This practice takes that upper edge to the
extreme. It keeps only pairs the model already ranks in the top 2 of 1M, and
it does so because the corpus is scraped. The two do not conflict. The noise
rate decides which end to cut, and E5's corpus is at the noisy extreme.
Nothing here measures the noise rate, though, so this does not locate where
the switch happens.

[SOTA-246](SOTA-246.md) finds mislabelled examples by self-influence rather
than by loss. This practice uses a cheaper signal, the model's own ranking,
and nobody has compared the two on the same corpus.

## Known implementations

- E5 (microsoft/unilm), the source's code.
