---
status: Active
title: 'One for All: Towards Training One Graph Model for All Classification Tasks'
version: 1
tags:
- graphs-and-networks
- adaptation-and-tuning
- in-context-learning
date: '2026-10-22'
published: '2023-09-29'
arxiv: '2310.00149'
first_author: 'Liu'
keywords:
- 'graph-foundation-model'
- 'text-attributed-graphs'
- 'graph-prompting'
- 'zero-shot'
- 'few-shot'
- 'cross-domain'
implementations:
- OneForAll
compared_against:
- LIT-582
- LIT-580
summary: >-
  Liu, Feng, Kong, Liang, Tao, Chen, Zhang (ICLR 2024), [ARXIV-2310.00149](https://arxiv.org/abs/2310.00149).
  OFA describes every node and edge in text and embeds it with one language
  model. It adds a task "prompt node" and one node per class to the graph,
  and trains a single R-GCN-style GNN on nine datasets at once. Jointly
  trained, it beats the best of GCN, GAT and GIN on 8 of 10 supervised
  tasks. The large
  gains are on knowledge-graph relation classification (WN18RR 96.91% against
  67.40%), and a separately trained OFA gets those too (97.22%). On Cora
  nodes it is below GAT (75.90% against 82.76%). Zero-shot transfer to
  unseen graphs is weak: AUC 35.67 on HIV, below chance, and 30.96% on
  5-way WN18RR.
---

# LIT-tmptwetd: One for All: Towards Training One Graph Model for All Classification Tasks

Liu, Feng, Kong, Liang, Tao, Chen, Zhang, WashU, NTU and Peking (ICLR 2024)
— [ARXIV-2310.00149](https://arxiv.org/abs/2310.00149)

## Key takeaways

- **Text as the shared feature space** (§3.1): atoms, bonds, papers,
  entities and relations are written as "Feature node. …" sentences and
  embedded by one model: Sentence-BERT, e5-large-v2 or Llama 2 7B/13B
- **One task format** (§3.2–3.3): the nodes a task is about (one node, a
  pair, or the whole graph) and their h-hop subgraph are joined to a "prompt
  node" carrying the task text. That node connects to class nodes carrying
  the class texts, and each class node is scored by a binary MLP. Few-shot
  support examples attach to their class nodes. For zero-shot, the class
  nodes carry the text of unseen classes
- **Supervised** (Tables 2–3, joint training with Sentence-BERT): Cora link
  AUC 94.04 against 93.70 for GAT, PubMed link 98.21 against 91.20, WN18RR
  96.91 against 67.40 for GCN, FB15K237 95.54 against 74.20, HIV 78.02
  against 75.49. Below the baselines on Cora nodes (75.90 against GAT's
  82.76) and Wiki-CS (78.34 against 79.63). The node splits for Cora, PubMed
  and arxiv differ from the standard ones
- **Why the prompt graph matters** (Table 12): removing the class nodes in
  favour of pooling makes no difference when each dataset is trained alone.
  Under joint training it costs 4.1 points on Cora nodes, 4.3 AUC on HIV and
  2.8 on Cora links, which is the paper's evidence that the task text
  carried by the prompt node keeps domains apart
- **Few- and zero-shot** (Tables 4–6, 13–18): on FB15K237, 20-way 5-shot is
  82.56 against Prodigy's 74.92, and 0-shot is 70.20 against 5.11. On Cora,
  transferred with no Cora training, 2-way 5-shot is 76.10 against 92.49 for
  TLP-SURGL trained on Cora. Zero-shot AUC is 35.67 on HIV and 60.62 on PCBA,
  where GIMLET scores 66.24 and 62.11
- **Joint against separate training** (Appendix E.2): joint training helps
  Cora and HIV few-shot. It hurts every link-level setting (FB15K237 10-way
  0-shot: 70.84 joint, 82.08 separate) and PCBA few-shot (51.53 against
  54.80)

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own review, 2026-10-22).
It is the record's first cross-domain graph model. The position paper on
graph foundation models ([LIT-tmpoyulj](LIT-tmpoyulj.md)) takes it as its example of a
"primitive" GFM.

**Compared against GCN** ([LIT-582](LIT-582.md)) **and GIN** ([LIT-580](LIT-580.md)). GCN, GAT and GIN
are its supervised baselines, rerun ten times on the Cora, PubMed and arxiv
node tasks and on WN18RR and FB15K237, and quoted from earlier work
elsewhere. GCN stays ahead
of jointly trained OFA on Cora nodes (78.86 against 75.90) and is far
behind on knowledge-graph relation classification (WN18RR 67.40, FB15K237
74.20). GIN trails OFA on both knowledge graphs (57.30, 70.70) and on PCBA
(22.66 AP against 24.83). The baselines take the datasets' native features.
OFA takes text embeddings, so the comparison bundles feature quality with
architecture. Its largest margins also appear when OFA is trained on one
dataset alone.

**What "one model for all" measured.** Joint training is evaluated at the
final epoch without validation-based selection, over 3 runs. Cross-domain
benefit is mixed in the paper's own appendix: positive for some node and
graph tasks, negative for every link task. The zero-shot HIV result is
below chance (AUC 35.67), and the paper does not discuss it.

Read — [NOTE-tmp25kz1](../notes.d/NOTE-tmp25kz1.md).
