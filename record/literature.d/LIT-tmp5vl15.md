---
status: Active
title: 'Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences'
version: 1
tags:
- representation-and-encoding
- adaptation-and-tuning
date: '2026-09-21'
published: '2021-04-13'
doi: '10.1073/pnas.2016239118'
first_author: 'Rives'
keywords:
- 'protein language model'
- 'unsupervised learning'
- 'representation learning'
- 'protein structure'
- 'transformer'
implementations: []
extended_by:
- LIT-tmph4no2
summary: >-
  Rives et al. (2021), PNAS 118(15) — the protein language model the
  biological-sequence line runs from. A transformer trained by masked-token
  prediction on 250 million protein sequences, with no structural or
  functional labels, produces representations in which secondary structure,
  tertiary contacts and remote homology are linearly recoverable. Held here
  as the ancestor of [LIT-tmph4no2](LIT-tmph4no2.md), which reimplements the recipe for
  RNA and copies its downstream head.
---

# LIT-tmp5vl15: Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences

Rives, Meier, Sercu, Goyal, Lin, Liu, Guo, Ott, Zitnick, Ma and Fergus
(2021) — `doi:10.1073/pnas.2016239118`.

## Standing

**The trunk of the biological-sequence line, and the record's first document
in it.** Until this filing the corpus held no protein, RNA or genomic
sequence model at all, which is why
[#243](https://github.com/dmarx/anthology-of-the-sota/issues/243)'s lesson applies here: a descendant filed onto an empty
trunk cannot declare the relations that say what it is. This is filed so
[LIT-tmph4no2](LIT-tmph4no2.md) can.

**Not read.** This record holds no `NOTE` on it and has not checked its
numbers against its tables. It is filed on its standing in the field and on
its role in [LIT-tmph4no2](LIT-tmph4no2.md), which cites it as reference 66 and takes its
downstream architecture from it verbatim — *"Similar to ESM-1b, our deep
residual network consists of 32 blocks, where each contains two convolution
layers with a filter size of 64."* Anything this record says about its
contents beyond that citation would be recall rather than reading, and the
summary above is deliberately at the level the citation supports.

**What a reading would be for.** The claim that structure and function
*emerge* from sequence statistics alone is the load-bearing one for
everything downstream of it, including the practice this record declined to
file from [LIT-tmph4no2](LIT-tmph4no2.md). Two things would need checking: whether the
structural information is recovered by a linear probe or by a trained head,
which decides how much the pretraining is doing; and how the evaluation splits
relate to the pretraining corpus, which is the question
[NOTE-tmprvzrn](../notes.d/NOTE-tmprvzrn.md) raises about the RNA descendant and cannot answer for
either.
