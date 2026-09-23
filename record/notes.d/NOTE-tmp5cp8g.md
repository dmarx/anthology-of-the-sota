---
status: Read
paper: LIT-tmp9cbir
title: 'word2vec (architectures)'
version: 1
date: '2026-09-23'
summary: >-
  CBOW and skip-gram, log-linear models that learn word vectors from
  billions of words cheaply, and the analogy benchmark that made "king − man
  + woman ≈ queen" a test. Read in full.
---

# NOTE-tmp5cp8g: word2vec (architectures)

## Contribution

Word vectors from a model simple enough to train on far more text than
earlier neural language models, and a benchmark for the linear structure
they turned out to have.

## Key insight

**Spend compute on data, not on the model.** Dropping the hidden layer made
the model cheap enough to train on billions of words. At that scale, the
simple model's vectors beat those of richer models trained on less.

## Key results

- Same data (320M words, 640d): skip-gram 55% semantic and 59% syntactic,
  against NNLM 23/53 and RNNLM 9/36
- Skip-gram 300d, 783M words: 53.3% total, against 2–25% for earlier public
  vectors
- 1000d on 6B words with DistBelief: skip-gram 65.6% and CBOW 63.7%

## Limitations

- **Table 4's comparison is not controlled.** It sets models trained on
  37M–6B words at 20–640 dimensions against each other
- **Exact-match analogy accuracy** as the main measure, on its own new test
- **Hierarchical softmax only.** Negative sampling came in the follow-up
