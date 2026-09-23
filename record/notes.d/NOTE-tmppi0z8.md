---
status: Read
paper: LIT-tmpmiyeb
title: 'Reading Tea Leaves'
version: 1
date: '2026-09-23'
summary: >-
  Two human tasks, word intrusion and topic intrusion, measure whether a
  topic model's topics and document assignments mean anything to people. The
  model with the best held-out likelihood, CTM, does worst on both. Read in
  full.
---

# NOTE-tmppi0z8: Reading Tea Leaves

## Contribution

The first quantitative, human-grounded evaluation of the thing topic models
are used for: whether the latent space is interpretable.

## Key insight

**A predictive metric measures the probability of observations and ignores
the representation.** If the representation is the product, as it is when
people read the topics, then it has to be measured directly. The paper's
two tasks turn "does this topic make sense" into a detection rate.

## Key results

- CTM has the best held-out likelihood (Table 1) and the worst model
  precision and topic log odds (Figures 3 and 6)
- LDA is usually best on word intrusion. LDA and pLSI beat CTM on topic
  intrusion
- pLSI's word-intrusion precision falls as the number of topics grows,
  consistent with overfitting
- Human–model agreement on topic intrusion is lowest for documents that span
  disparate subjects
- Model precision is negatively correlated with the words' number of WordNet
  senses (Spearman ρ of about −0.24)

## Limitations

- **"Negatively correlated" rests on 18 points** (3 models × 3 K × 2
  corpora), and the trend is carried mostly by CTM. Within LDA and pLSI,
  topic log odds are nearly constant across K
- **Small likelihood gaps**, in the second decimal place of per-word log
  likelihood
- **Proper nouns were removed** for the subjects' benefit, so the corpora are
  not what a practitioner would fit
- **Subjects could see the model's answer** after responding. The authors
  report that small experiments showed no bias
- **Three bag-of-words models of 2009.** The tasks, not the rankings, are
  what transfers
