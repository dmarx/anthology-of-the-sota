---
status: Deferred
status_note: seeded from the abstract and a skim on 2026-09-25; not read in full
title: 'The Impact of Generative AI on Social Media: An Experimental Study'
version: 1
tags:
- deployment-and-society
date: '2026-09-25'
published: '2025-06-17'
arxiv: '2506.14295'
first_author: 'Møller'
keywords:
- 'controlled experiment'
- 'large language models'
- 'social media'
- 'AI-assisted writing'
- 'online discussion'
implementations: []
summary: >-
  Møller et al. (2025), [ARXIV-2506.14295](https://arxiv.org/abs/2506.14295). In a randomized experiment with 680 US participants, generative-AI writing aids raised engagement and output on a simulated social platform but lowered perceived quality and authenticity, with negative spill-over into threads, and no single tool improved both producer and consumer experience.
---

# LIT-tmpgwgl7: The Impact of Generative AI on Social Media: An Experimental Study

Anders Giovanni Møller, Daniel M. Romero, David Jurgens, Luca Maria Aiello (2025), *arXiv preprint* — [ARXIV-2506.14295](https://arxiv.org/abs/2506.14295)

## Key takeaways

- In a randomized experiment with 680 US participants, generative-AI writing aids raised engagement and output on a simulated social platform but lowered perceived quality and authenticity, with negative spill-over into threads, and no single tool improved both producer and consumer experience.

*Seeded from the abstract and a skim, not a reading. What follows is what the work says about itself.*

The authors built a realistic forum-style platform and randomly assigned 680 representative US participants, in groups of five, to a control condition or one of four GPT-4o-powered aids: open chat, conversation starters, feedback on drafts, and reply suggestions. Some tools increased engagement and the volume of content. They also lowered the perceived quality and authenticity of the discussion and spilled over negatively into the conversations. From these results the authors propose four design principles: transparent disclosure of AI content, user-focused personalisation, sensitivity to topic and intent, and intuitive interfaces.

## Standing in the record

Filed from the survey of 2026-09-25 of work the anthology set aside as out of scope (tier C): 305 seconds of active reading over 2 sessions in the papers-feed tracker. `Deferred` because nobody has read it closely here yet, not on merit.

It was a boundary case in the survey of work this anthology had set aside as out of scope, and it is filed here rather than in the catchall record, nucleation, under the rule that a work in doubt belongs in the anthology. It is a randomized experiment on what LLM writing tools do to a social platform's discussions and the people in them, which is exactly the `deployment-and-society` blurb (information ecosystems, deployed systems among people).

**Priority for a deeper reading: medium — Moderate reading time (t = 305 s over 2 sessions) and a solid experimental design. The skim captures the main findings, but the effect sizes and measurement details need a proper read before anything cites it.**

What a deeper reading should check:

- It is causal (randomized) evidence on deployed-LLM effects in an information ecosystem, which is rarer than observational audits. It is a clean `deployment-and-society` note.
- The external-validity limits a deeper reading should weigh: 10-minute sessions, five-person groups, a simulated platform, one model (GPT-4o), and US participants only.
- A deeper reading should check how "perceived quality" and "authenticity" were measured and how much of the spill-over is statistically robust as opposed to suggestive.

Access when seeded: arXiv abs page (v1 only, 17 Jun 2025, cs.HC, 48 pp.) and the full PDF, extracted with PyMuPDF. I read the Introduction and results overview (pp. 1–4), the AI-usage analysis (pp. 5–8), the Discussion and design principles (p. ~10), the Methods opening (p. 13), and the prompt settings in the Supplementary Information (GPT-4o, temperature 1). I did not read the statistical tables in full.
