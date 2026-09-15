<p align="center">
  <img src="assets/logo.svg" width="200" height="200" alt="ML Training Phase Transitions">
</p>

<h1 align="center">Anthology of the SOTA</h1>

<p align="center">
  Best practices for ML/AI training, validated by research and experience
</p>

---

<!-- luria:site -->
📖 **[dmarx.github.io/anthology-of-the-sota](https://dmarx.github.io/anthology-of-the-sota/)** — this record, published by `luria site`.
<!-- /luria:site -->

Why we -- AI/ML researchers and practitioners -- do the things that we do, and why we do those things the way that we do them.

You might also be interested in my list of significantly impactful works that has more of a historical perspective: https://github.com/dmarx/anthology-of-modern-ml

The main difference here is that where that prior list was focused on big, impactful works, including those which no longer reflect best practice, this list is focused entirely on whatever the current best practice is understood to be and explaining the justification behind that design choice. Where my `Modern ML` anthology focused on paradigm shifts and made no space for important but comparatively "small" (with respect to paradigmatic impact) incremental improvements, I expect this space to be dominated by incremental works. Additional, because the other list operates as a kind of "hall of fame", it generally should not experience churn. This list however, I plan to maintain as a living document with an "attic" in which to deprecate former best practices that have been supplanted.
## The record

The anthology lives in `record/`, as one document per claim, and is rendered
into browsable views in `docs/`. Start at **[docs/README.md](docs/README.md)**.

| | Source | Generated view |
|---|---|---|
| **Practices** — what to do, and why | `record/practices.d` | [docs/practices](docs/practices/README.md) |
| **Theory** — why the things in the registry work | `record/theory.d` | [docs/theory](docs/theory/README.md) |
| **Literature** — the evidence, including the attic | `record/literature.d` | [docs/literature](docs/literature/README.md) |
| **Decisions** — why the anthology is built this way | `record/decisions.d` | [docs/decisions](docs/decisions/README.md) |
| **Principles** | `record/principles.d` | [docs/design-principles.md](docs/design-principles.md) |
| **Curation log** — what entered and what left | `record/curation.d` | [docs/curation](docs/curation/README.md) |

A **practice** is a claim about what you should do; a **theory** is a claim
about why it works; a **note** is a paper's standing in the anthology. All
three carry separate statuses and are allowed to disagree — a foundational
paper can carry advice that has moved on, a paper in the attic can still be
the source of something everybody does, and a technique everybody uses can
have been published with an explanation that turned out to be wrong. Batch
normalization is all three at once, and the record says so in three places.

Nothing is deleted. A practice that stops being right becomes `Superseded`
or `Rejected` and keeps its body, because the contrast with what it replaced
is most of what makes the current entry worth stating.

```
luria new sota    # file a practice (or: theory, lit, adr, dp, changelog)
luria link --fix  # spell the link targets; never hand-write one
luria index       # regenerate every view
luria lint        # the only command that can fail
```
