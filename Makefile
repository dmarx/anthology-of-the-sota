# Makefile — the four commands, in the order that works, with the two
# invariants enforced rather than remembered. See ADR-054.

.PHONY: help hooks check views-reset ready

help:
	@echo "make hooks        install .githooks (ADR-018 guard); run once per clone"
	@echo "make check        luria repair -> link --fix -> index -> lint"
	@echo "make views-reset  discard everything luria index regenerated"
	@echo "make ready        check, then views-reset — run before you commit"

hooks:
	git config core.hooksPath .githooks
	@echo "core.hooksPath = .githooks"

# BOTH `repair` and `link --fix` are needed and neither contains the other.
# `repair` populates `created:` from a journal entry's path and retires stale
# config references; `link --fix` writes the converse of a declared relation,
# which `repair` does not. `index` is run for its side effect on the reports as
# much as for the views: docs/reports/reference-status.md is what names the
# citing sites an acknowledgement has to be written from.
check:
	luria repair
	luria link --fix
	luria index
	luria lint

# Unstage first: the pre-commit hook fires on *staged* views, and at that
# point `git checkout -- docs/` restores them from the index, which is where
# the unwanted copies already are. Found by the hook, on its first real catch.
views-reset:
	git reset -q HEAD -- docs/ 2>/dev/null || true
	git checkout -- docs/
	git clean -fdq docs/

ready: check views-reset
	@echo
	@echo "Views discarded. Read the lint output above in full — the stale-directive"
	@echo "line is at the bottom, and EXIT=0 covers warnings as well as violations."
