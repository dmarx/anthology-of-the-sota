---
status: Deferred
status_note: seeded from the abstract and a skim on 2026-09-25; not read in full
title: 'Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task'
version: 1
tags:
- deployment-and-society
date: '2026-09-25'
published: '2025-06-10'
arxiv: '2506.08872'
first_author: 'Kosmyna'
keywords:
- 'LLM-assisted writing'
- 'EEG'
- 'cognitive load'
- 'essay writing'
- 'education'
implementations: []
summary: >-
  Kosmyna et al. (2025), [ARXIV-2506.08872](https://arxiv.org/abs/2506.08872). In a small four-month EEG study, participants who wrote essays with ChatGPT showed the weakest brain connectivity, the lowest sense of ownership and the worst recall of their own essays. Those switched from ChatGPT to no tools stayed under-engaged, which the authors call accumulated "cognitive debt".
---

# LIT-tmpk9vfz: Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task

Nataliya Kosmyna, Eugene Hauptmann, Ye Tong Yuan, Jessica Situ, Xian-Hao Liao, Ashly Vivian Beresnitzky, et al. (2025), *arXiv preprint* — [ARXIV-2506.08872](https://arxiv.org/abs/2506.08872)

## Key takeaways

- In a small four-month EEG study, participants who wrote essays with ChatGPT showed the weakest brain connectivity, the lowest sense of ownership and the worst recall of their own essays. Those switched from ChatGPT to no tools stayed under-engaged, which the authors call accumulated "cognitive debt".

*Seeded from the abstract and a skim, not a reading. What follows is what the work says about itself.*

Fifty-four participants wrote SAT-style essays in three sessions, split into three groups: ChatGPT, search engine, and no tools. In a fourth session, 18 of them swapped conditions: ChatGPT users wrote unaided and unaided writers used ChatGPT. EEG connectivity fell as external support increased: the no-tool group had the strongest and most distributed networks, the search group was intermediate, and the ChatGPT group was weakest. Essays within each group were homogeneous in named entities, n-grams and topics. ChatGPT users reported the lowest ownership of their essays and often could not quote from them. The authors conclude that the tool's convenience carries cognitive costs and call for longitudinal study of its educational effects.

## Standing in the record

Filed from the survey of 2026-09-25 of work the anthology set aside as out of scope (tier C): 475 seconds of active reading over 1 session in the papers-feed tracker. `Deferred` because nobody has read it closely here yet, not on merit.

It was a boundary case in the survey of work this anthology had set aside as out of scope, and it is filed here rather than in the catchall record, nucleation, under the rule that a work in doubt belongs in the anthology. It measures what a deployed AI assistant (ChatGPT) does to the people using it, which is the anthology's `deployment-and-society` subject, not neuroscience in its own right.

**Priority for a deeper reading: medium — The owner spent real time on it (t = 475 s), and it is load-bearing in public discussion. Its methodological soundness is the open question, and this skim did not reach the statistics.**

What a deeper reading should check:

- It is widely cited in public debate as evidence that AI assistants harm cognition. A deeper reading should check the statistics behind that use: n = 54 falling to 18 in session 4, the multiple-comparison handling across frequency bands and connections, and whether "connectivity" differences support "cognitive debt".
- It is a preprint marked under review and revised in Dec 2025 (v2). A deeper reading should check what changed between versions and whether it has since been peer-reviewed.
- Whether lower connectivity means under-engagement or efficient offloading is an interpretive step. The authors themselves read one session-3 drop as "neural efficiency adaptation".
- It is a usage-harm study with no practice for building models. In the anthology it would be a note on `deployment-and-society`.

Access when seeded: arXiv abs page (v1 10 Jun 2025, v2 31 Dec 2025) and the full PDF (current version v2, 216 pp., marked "Preprint, under review"). I read the abstract, the "Summary of Results" table, the table of contents, and the Limitations and Conclusions sections. I did not read the EEG methods or statistics sections (pp. ~60–150). The PDF's first-page layout extracts as one word per line with pypdf, so I re-extracted it with PyMuPDF. The eight authors are complete from the arXiv metadata.
