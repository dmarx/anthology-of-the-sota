# Makefile — the four commands, in the order that works, with the two
# invariants enforced rather than remembered. See ADR-054.

.PHONY: help hooks check views-reset ready

help:
	@echo "make hooks        install .githooks (ADR-018 guard); run once per clone"
	@echo "make check        luria repair -> index -> lint"
	@echo "make views-reset  discard everything luria index regenerated"
	@echo "make ready        check, then views-reset — run before you commit"

hooks:
	git config core.hooksPath .githooks
	@echo "core.hooksPath = .githooks"

# `repair` subsumes `link --fix` and also populates `created:` from a journal
# entry's path. `index` is run for its side effect on the reports as much as
# for the views: docs/reports/reference-status.md is what names the citing
# sites an acknowledgement has to be written from.
check:
	luria repair
	luria index
	luria lint

views-reset:
	git checkout -- docs/
	git clean -fdq docs/

ready: check views-reset
	@echo
	@echo "Views discarded. Read the lint output above in full — the stale-directive"
	@echo "line is at the bottom, and EXIT=0 covers warnings as well as violations."
