---
status: Active
title: 'Text Embeddings by Weakly-Supervised Contrastive Pre-training'
version: 1
tags:
- representation-and-encoding
- data-pipeline
- training-optimization
- adaptation-and-tuning
date: '2026-10-01'
published: '2022-12-07'
arxiv: '2212.03533'
first_author: 'Wang'
keywords:
- 'text-embeddings'
- 'contrastive-pre-training'
- 'weak-supervision'
- 'in-batch-negatives'
- 'consistency-based-filtering'
- 'dense-retrieval'
- 'BEIR'
- 'MTEB'
implementations:
- 'E5'
- 'microsoft/unilm'
compared_against:
- LIT-590
summary: >-
  Wang et al. (2022), ARXIV-2212.03533 — E5. A BERT-initialised bi-encoder
  trained with InfoNCE and in-batch negatives (batch 32,768) on ~270M web text
  pairs, cut from ~1.3B by a consistency filter that keeps a pair only if a
  model trained on the noisy set ranks its passage in the top 2 of 1M. With
  no labelled data the base model averages 42.9 nDCG@10 on 15 BEIR datasets
  against BM25's 41.7, the first unsupervised model reported above BM25; after
  fine-tuning on MS-MARCO, NQ and NLI the 330M large model averages 61.4 on
  56 MTEB English datasets, above the 4.8B GTR-xxl and Sentence-T5-xxl.
---

# LIT-tmp62ra1: Text Embeddings by Weakly-Supervised Contrastive Pre-training

Wang et al. (2022) — ARXIV-2212.03533 (v2, February 2024, corrects the
SummEval numbers).

## Key takeaways

- **The recipe is deliberately plain; the data is the contribution.**
  Shared Transformer encoder, mean pooling, cosine similarity over a
  temperature of 0.01, InfoNCE with in-batch negatives only, and the prefixes
  `query:` and `passage:` to break the symmetry of the shared encoder. Three
  sizes are initialised from MiniLM (33M), bert-base (110M) and bert-large
  (330M). Pre-training is 20k steps at batch 32,768, about 2.5 epochs, on
  16 to 64 V100s for 1 to 2 days.
- **CCPairs: weak pairs mined from semi-structured web sources.** These are
  (post, upvoted comment) pairs from Reddit, (question, answer) from
  Stackexchange, (entity and section title, passage) from Wikipedia, (title,
  abstract) and citation pairs from S2ORC, and (title, passage) from Common
  Crawl and news. After heuristic filtering there are ~1.3B pairs.
- **The consistency filter cuts 1.3B pairs to ~270M.** A model is trained on
  the noisy 1.3B, then ranks each pair's passage against 1M random passages,
  and the pair is kept only if it lands in the top 2. The stated intuition is
  that networks learn clean labels before memorising noisy ones. Table 7
  measures it on six BEIR datasets. With 1M pairs, filtered data averages
  40.7 against 34.9 unfiltered. With all pairs, the filtered set averages
  51.6 against 50.0, even though the unfiltered set holds about 4× more
  data. The threshold `k = 2` was set "based on manual inspection" and is not
  swept.
- **Unsupervised, it is the first to beat BM25 on BEIR.** Across 15 BEIR
  datasets (nDCG@10), E5-PT-base averages 42.9 and E5-PT-large 44.2,
  against BM25 at 41.7 and Contriever at 36.0. BM25 still wins 5 of the 15
  datasets outright, including Trec-Covid (65.6 vs 61.8), Touche-2020 and
  Fever. The authors' own conclusion is that BM25 cannot be replaced "yet":
  dense retrieval still loses in long-tail domains, on long documents and
  wherever exact lexical match matters.
- **Fine-tuning is the second stage.** The model is trained further on
  MS-MARCO, NQ and NLI with 7 mined hard negatives per example, under a loss
  that adds InfoNCE (weight 0.2) to KL distillation from a cross-encoder
  teacher. On 56 MTEB English datasets this gives an average of 58.9, 60.4
  and 61.4 for small, base and large, against 59.0 for GTR-xxl and 59.5 for
  Sentence-T5-xxl, both 4.8B. BERT-FT-base uses the same fine-tuning data
  with no contrastive pre-training and averages 55.2. Clustering is the one
  category that does not improve with fine-tuning (44.3 to 43.3 on large).
- **The fine-tuning mixture trades task against task** (Table 6, base).
  MS-MARCO with NQ is best for retrieval (50.3) and NLI is best for STS
  (81.1) and classification (72.6). All three together score lower on
  retrieval than MS-MARCO with NQ alone (48.7) but give the best MTEB average
  (60.4).
- **The ablations are on the base model and six BEIR datasets.** Batch size:
  1k → 8k → 32k gives 45.8 → 50.2 → 51.6, rising on every dataset, and
  nothing above 32k is tried. Negatives (Table 8): 32k in-batch negatives
  give 51.6, adding pre-batch negatives to reach 64k gives 43.3, and a MoCo
  queue of 130k gives 45.5. The authors add that MoCo was more sensitive to
  temperature and "better results are possible with more tuning". Three
  things were dropped (Appendix C). One BM25 hard negative per pair gained
  ~0.5 BEIR points at 15M pairs but was too slow to compute over 250M+. A
  RoBERTa initialisation did worse than BERT on most BEIR datasets. An
  auxiliary MLM loss on 25% of pairs made no difference and cost compute.
  The `query:`/`passage:` prefixes are said to matter for retrieval tasks
  whose corpus contains paraphrases of the query, but no ablation is shown.

## Standing in the anthology

This is the record's first text-embedding model. The objective is a
neighbour of what the record already holds. The loss is InfoNCE with in-batch
negatives, cited to SimCLR (LIT-591), and THEORY-085 bounds it at `log N`.
At this paper's batch of 32,768 that bound is the same ~10.4 nats THEORY-085
computes for CLIP.

On negatives, it bears on two practices:

- **It supports SOTA-377 below the ceiling and does not test the ceiling.**
  Each step up to 32k helps, and 32k is where both SOTA-377 and this paper
  stop.
- **It sits awkwardly beside SOTA-363 (MoCo, LIT-590).** In its Table 8 the
  paper ran MoCo's queue and momentum encoder in place of in-batch negatives
  in its own text pre-training. The queue was worse by 6.1 points on average
  even though it held four times as many negatives, and reusing negatives
  from earlier batches was worse still. That is the comparison recorded as
  `compared_against`. It is one tuning of MoCo, and the authors say more
  tuning could close the gap. What it shows is that at 32k the batch already
  supplies enough negatives, so SOTA-363's reason for a queue does not come
  up. It is not evidence that a queue is harmful.

On data, the consistency filter is an extreme version of the upper cutoff in
SOTA-243's Conditions, which come from LIT-397. SOTA-243 says that with
abundant data you should keep the hard examples, and its Conditions add that
the hardest examples and the mislabelled ones are the same examples. With
1.3B weak pairs, E5 keeps only pairs a model ranks in the top 2 of 1M. That
discards everything hard, on the theory that a hard pair in a scraped corpus
is a wrong pair, and Table 7 shows it helped at both scales tried. The
two do not conflict, because E5's labels are noisy and SOTA-243's are not.
What a reader should take is that the noise rate decides which end to cut.

SOTA-327 (Matryoshka embeddings) states that its source measured no text
retrieval. E5 is not Matryoshka-trained, so it does not fill that gap. It is
the kind of model the gap is about.

Unread — no NOTE.
