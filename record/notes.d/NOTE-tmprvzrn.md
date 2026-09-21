---
status: Read
paper: LIT-tmph4no2
title: 'RNA-FM, and the control that does not carry the claim'
version: 1
date: '2026-09-21'
summary: >-
  Read to open the biological-sequence trunk, which this record did not hold.
  The structural results are large and the paper's one clean
  input-swap control is not: replacing one-hot sequence with a 640-dimensional
  pretrained embedding in a published UTR model moves `R²` from **0.814 to
  0.816** on the real-human set, where a 16-dimensional predicted secondary
  structure moves it to **0.820**. No practice filed.
---

# NOTE-tmprvzrn: RNA-FM, and the control that does not carry the claim

## Contribution

The first foundation model for RNA: a 12-layer BERT encoder trained by
masked-token prediction on **23.7 million** unannotated non-coding RNA
sequences from RNAcentral, producing an `L × 640` embedding per sequence, then
used as a frozen feature extractor across secondary structure, 3D contact and
distance maps, SARS-CoV-2 genome structure, protein-RNA binding and 5'UTR
translation regulation.

It is the RNA transcription of [LIT-tmp5vl15](../literature.d/LIT-tmp5vl15.md)'s protein recipe, and says
so: the downstream head is ESM-1b's ResNet32, unchanged, reference 66.

## Key results

**Secondary structure, Table 1** — against twelve published methods, on two
benchmarks, F1 score:

| method | ArchiveII600 | bpRNA TS0 |
|---|---|---|
| **RNA-FM** | **0.941** | **0.704** |
| UFold | 0.905 | 0.654 |
| Contextfold | 0.842 | 0.546 |
| MXfold2 | 0.768 | 0.558 |
| SPOT-RNA | 0.711 | 0.619 |
| E2Efold | 0.690 | 0.130 |
| RNAfold | 0.592 | 0.536 |
| LinearFold | 0.621 | 0.550 |

These are large, clean margins over a well-populated field, and the collapse
of E2Efold from 0.690 to 0.130 across the two benchmarks is its own lesson
about how much of a reported number is the benchmark.

**3D closeness** — a single model on RNA-FM embeddings exceeds an ensemble of
100 models by **30%** on long-range top precision; long-range top-L precision
improves **7 points** over covariance-plus-PETfold features.

**5'UTR mean ribosome load, Table 5.** This is the one experiment where the
input representation is swapped inside somebody else's published architecture
with everything else held fixed — Paul et al.'s three-layer 1D CNN, found by
their grid search, inputs replaced and nothing else touched:

| features | Random7600 `R²` | MSE | Human7600 `R²` | MSE |
|---|---|---|---|---|
| Seq (one-hot, 4 dims) | 0.860 | 0.277 | 0.814 | 0.269 |
| Seq + SS (predicted 2° structure, 16 dims) | 0.866 | 0.266 | **0.820** | 0.261 |
| **RNA-FM (640 dims)** | 0.876 | 0.247 | **0.816** | 0.264 |
| 3DS | 0.864 | 0.271 | 0.813 | 0.267 |
| Seq + SS + RNA-FM | 0.876 | 0.245 | **0.811** | **0.287** |
| Seq + SS + 3DS + RNA-FM | 0.882 | 0.236 | 0.824 | 0.256 |

Random7600 is drawn from the same synthetic library as the training data.
Human7600 is real human 5'UTRs, provided by the library authors *as the
generalization check*, and it is the column that matters.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Masked pretraining on unannotated ncRNA yields representations that improve RNA secondary and tertiary structure prediction | strong | Table 1 against twelve methods on two benchmarks; 3D closeness against a 100-model ensemble |
| C2 | The embeddings carry evolutionary information | moderate | UMAP separation by RNA type; lncRNA and SARS-CoV-2 trajectory inference consistent with a phylogenetic tree |
| C3 | The representations generalize to sequences outside the pretraining distribution | **weak** | Table 5's Human7600 column, where the swap is worth 0.002 `R²` |
| C4 | Adding RNA-FM-derived structure features improves further | **mixed** | true on Random7600; on Human7600 `Seq+SS+RNA-FM` scores **below `Seq` alone** |

## Limitations

**The one clean control is the weakest result in the paper.** Everywhere else
the comparison is RNA-FM's pipeline against somebody else's pipeline, so
architecture, training data and features all differ at once. Table 5 holds all
of that fixed and swaps only the input. On the generalization set the swap
buys **0.002 `R²`** — and a 16-dimensional predicted secondary structure, a
feature that costs almost nothing, buys **0.006**, three times as much from a
representation forty times smaller.

**One row goes the wrong way and is not mentioned.** `Seq + SS + RNA-FM` on
Human7600 scores `R²` **0.811** against `Seq` alone at 0.814, with MSE rising
from 0.269 to **0.287** — the worst MSE in the table. Adding the embedding on
top of sequence-plus-structure makes the model worse on real human UTRs. The
text around the table says "the prediction accuracy is indeed further
improved" and, a paragraph later, that "performance gains are consistent
across all the lengths and contexts".

**Nothing checks the pretraining corpus against the evaluation sets.** The
pretraining set is named **RNAcentral100** in the paper, and the 100 is the
cd-hit-est cut-off: identical sequences were collapsed, and nothing else was
removed. RNAcentral aggregates 47 databases and is described in the paper as
"representing all the ncRNA types from a broad range of organisms". The
secondary-structure test sets are drawn from that same universe. bpRNA-1m is
deduplicated at 80% identity *within itself*, which says nothing about its
relationship to the pretraining corpus. So the model has, in all likelihood,
seen the test sequences unlabelled — which is the standard protocol for this
model family and is not misconduct, but it does mean the margin over methods
that never saw them is not only a margin in representation quality. The paper
does not raise this.

**The reported margin shrinks by a factor of four under redundancy
reduction, and the paper says so.** "RNA-FM outperforms LinearFold by up to
30% and SPOT-RNA by up to 20% ... Even on the low-redundant dataset ... still
outperforms SPOT-RNA by up to 7.5% and UFold by 4%." Stated plainly in the
abstract, which is to the authors' credit. It does not isolate redundancy —
the two dataset families differ in RNA type distribution and length as well —
so it is a signal rather than a measurement.

**A small internal inconsistency.** The body text gives `R²` = 0.875 for
RNA-FM on the synthetic set where Table 5 says 0.876.

**No ablation of the pretraining.** There is no smaller-corpus, shorter-
training or randomly-initialized-encoder arm anywhere, so how much of the
structural gain requires 23.7 million sequences is unmeasured.

## Bearing on the record

**This opens a trunk the record did not have.** Before this filing the corpus
held no protein, RNA or genomic sequence model. [LIT-tmp5vl15](../literature.d/LIT-tmp5vl15.md) is filed
alongside, unread, so that this paper can declare what it extends — the
lesson [#243](https://github.com/dmarx/anthology-of-the-sota/issues/243) taught when GaussianToken landed on an empty tokenizer trunk
and could name none of its four baselines.

**No practice.** Two reasons, and the first is the one the earlier pass-over
gave. The recommendation the paper argues for — pretrain self-supervised on
the unlabelled pool when labels are scarce — is one this record already
carries implicitly across every practice that touches pretraining; a new
domain adds an instance, not evidence, and `DP-005` is about not promoting
adoption into evidence.

The second reason is what the reading found. The narrower and more useful
recommendation this paper *could* have supported — *keep the published task
model and swap its one-hot input for pretrained embeddings* — is exactly the
experiment in Table 5, and on the generalization column it is worth 0.002
`R²` while losing to a 16-dimensional hand-computed feature. A practice
written from the structural tables would rest on comparisons that vary
everything at once; a practice written from the controlled table would have to
say the effect is negligible. Neither is a recommendation.

**Where it does connect.** The 30%-to-4% collapse under redundancy reduction,
and the absence of any check between a 23.7-million-sequence pretraining
corpus and the test sets, are the same shape as the practice filed from
[#241](https://github.com/dmarx/anthology-of-the-sota/issues/241): a reported margin that shares something with its own evaluation.
Counted here, not generalized — `DP-009`, and the mechanisms are different
enough that calling them one thing would be the failure this record keeps
finding in other people's work.

## Open questions

- **Does the structural gain survive an honest pretraining/test split?**
  Screen RNAcentral100 against ArchiveII600 and bpRNA TS0 at a sequence
  identity threshold, retrain, and report Table 1 again. The corpus, the code
  and the weights are all public, so this is a run rather than a project.
- **How much pretraining is needed?** No corpus-size or training-length
  ablation exists. A randomly-initialized encoder with the same ResNet32 head
  is the missing floor for every structural number in the paper.
- **Why does the embedding hurt on top of `Seq + SS`?** The Human7600 row is
  unexplained and may be the most informative number in Table 5 — it suggests
  the embedding and the predicted secondary structure carry overlapping
  information, and that the 640-dimensional version costs capacity the small
  CNN does not have to spare.
- **Does the protein ancestor have the same gap?** [LIT-tmp5vl15](../literature.d/LIT-tmp5vl15.md) is filed
  unread. Whether its structural claims rest on linear probes or trained
  heads, and how its splits relate to its pretraining corpus, are the same two
  questions and would decide whether this is a property of this paper or of
  the recipe.
