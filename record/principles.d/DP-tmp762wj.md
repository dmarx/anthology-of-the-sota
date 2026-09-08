---
status: Active
title: Filing is not endorsement — the bar for having a document is lower than the bar for believing it
version: 1
tags:
- craft
date: '2026-09-08'
influenced_by:
- ADR-014
- ADR-015
---

# DP-tmp762wj: Filing is not endorsement — the bar for having a document is lower than the bar for believing it

A collection of recommendations has two thresholds and it is easy to run
them together. One decides whether a claim gets a document. The other decides
whether the project is willing to say the claim is right. They are not the
same threshold, and using the second for the first is a mistake that looks
like rigour.

The failure is specific: a paper arrives with a real recommendation and
weak-but-honest evidence, and the reflex is *not yet*. Nothing bad appears to
happen. But three things are lost at once, and none of them is the
endorsement that was correctly withheld.

**A refusal has nowhere to put what would reverse it.** The condition —
"promote this when a second group reports X" — is the most perishable fact in
the whole encounter, and with no document to carry it, it goes in prose, in a
note about a different subject, where nothing will point at it when the
evidence arrives.

**A judgement about the field needs something to be a judgement about.** How
far the field has converged is a property of a recommendation. Withhold the
recommendation and the second lab to publish has nowhere to be recorded; the
counter that would eventually earn the endorsement was removed by the
refusal.

**And the unused status decays into no status at all.** If only claims that
clear the top bar are filed, the provisional statuses fill with nothing but
the cases somebody filed optimistically and forgot — which is exactly the
distribution [DP-002](design-principles.md#dp-2) is about, reached from the other direction.

Applied here: `status:` carries the belief, `consensus:` carries the field's,
and `promote_when:` carries the condition — so the entry question is only
whether the work contains an instruction. Twelve practices were filed in one
day that the evidence had supported for months, three of them refused *in
writing* on the grounds that nobody at frontier scale had adopted them yet.
That is a correct reason not to mark something `Active` and not a reason for
it to be absent.

The corollary people skip: this cuts the other way too. A document filed at a
provisional status is a promise to revisit, and a provisional status with no
condition attached is the same refusal wearing a document's clothes.
