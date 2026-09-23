# tests/test_repo_features.py
"""The harness behind #291 — what a repository ships, diffed against the record.

Every test here is a claim the #287 pilot measured. The two that matter most
are the two halves of the matching result: bodies over-match and subjects
under-match, and a tool that picks one silently commits whichever error the
choice makes.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.repo_features import corpus, extract, run


# ── extraction ───────────────────────────────────────────────────────────

def test_arxiv_ids_reads_links_and_bibtex():
    """A catalogue README cites both ways, and reading only the links loses
    real papers — measured at 8 of 84 on x-transformers."""
    text = ("see https://arxiv.org/abs/2306.00978 and\n"
            "https://arxiv.org/pdf/2205.14135v2\n"
            "@article{x, eprint = {2312.07104}}\n")
    assert extract.arxiv_ids(text) == ["2205.14135", "2306.00978", "2312.07104"]


def test_arxiv_ids_are_sorted_and_unique():
    """Sorted rather than in document order: the list is compared against the
    previous run, and a README that reorders its sections would otherwise
    read as a wholesale change."""
    text = ("arxiv.org/abs/2306.00978 arxiv.org/abs/2205.14135 "
            "arxiv.org/pdf/2306.00978")
    assert extract.arxiv_ids(text) == ["2205.14135", "2306.00978"]


def test_feature_names_unwrap_links_and_abbreviations():
    """vLLM's matrix writes a feature as a link or an <abbr>; the name is the
    useful part, because it is what a practitioner would search for."""
    text = ("| Feature | x |\n| - | - |\n"
            "| [LoRA](lora.md) | y |\n"
            '| <abbr title="Async Output Processing">async output</abbr> | z |\n')
    assert extract.feature_names(text) == ["LoRA", "Async Output Processing"]


def test_feature_names_drop_separators_and_the_header():
    text = "| Feature | a |\n| - | - |\n| --- | --- |\n| CUDA graph | b |\n"
    assert extract.feature_names(text) == ["CUDA graph"]


def test_exported_names_can_filter_by_suffix():
    """`diffusers` lists every scheduler it ships in a lazy-import table."""
    text = '_import = [\n    "DDIMScheduler",\n    "AutoPipeline",\n    "PNDMScheduler",\n]\n'
    assert extract.exported_names(text, "Scheduler") == ["DDIM", "PNDM"]


def test_exported_names_read_the_shape_diffusers_actually_uses():
    """Regression, found by a live run rather than by this suite. The first
    pattern anchored a name to its own line, which is how the fixture above
    is written and is not how the real file is — `diffusers` puts several
    names on one line inside a lazy-import table, and the anchored pattern
    reported the module as exporting nothing."""
    text = ('    _import_structure["scheduling_ddim"] = ["DDIMScheduler"]\n'
            '    _import_structure["deprecated"] = ["KarrasVeScheduler", '
            '"ScoreSdeVpScheduler"]\n')
    assert extract.exported_names(text, "Scheduler") == [
        "DDIM", "KarrasVe", "ScoreSdeVp"]


# ── matching, and why it is two answers ──────────────────────────────────

@pytest.fixture
def record(tmp_path: Path) -> Path:
    def practice(code, title, summary, body):
        d = tmp_path / "record" / "practices.d"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{code}.md").write_text(
            f"---\ntitle: '{title}'\nsummary: >-\n  {summary}\n---\n\n{body}\n")
    practice("SOTA-105", "PagedAttention to accelerate batch inference",
             "Kwon et al.", "Blocks of KV cache.")
    practice("SOTA-143", "Parameterize the model with muP",
             "Yang et al.", "The run was in FP8 throughout.")
    practice("SOTA-227", "Decode with a draft model and an accept-reject rule",
             "Leviathan et al.", "This is speculative decoding, losslessly.")
    return tmp_path


def test_a_subject_hit_is_confirmation(record):
    c = corpus.practices(record)
    confirmed, _ = corpus.matching(c, "PagedAttention")
    assert confirmed == ["SOTA-105"]


def test_a_body_hit_is_only_a_candidate(record):
    """The pilot's false positive, kept as a test: µP's body mentions FP8
    once and the practice is not about FP8."""
    c = corpus.practices(record)
    confirmed, candidates = corpus.matching(c, "FP8")
    assert confirmed == []
    assert candidates == ["SOTA-143"]


def test_subjects_alone_would_miss_a_real_practice(record):
    """The opposite failure, and the reason both are reported. SOTA-227 IS
    speculative decoding and its title never says so, so a subject-only tool
    would call it a coverage gap."""
    c = corpus.practices(record)
    confirmed, candidates = corpus.matching(c, "speculative decoding")
    assert confirmed == []
    assert candidates == ["SOTA-227"], "found, but only as a lead"


def test_a_feature_nothing_mentions_is_absent_from_both(record):
    c = corpus.practices(record)
    assert corpus.matching(c, "AWQ") == ([], [])


# ── the lockfile, which is what makes this a diff ────────────────────────

def test_changes_reports_new_and_gone():
    now = {"vllm": {"items": ["APC", "LoRA"]}}
    before = {"vllm": {"items": ["LoRA", "multi-step"]}}
    assert run.changes(now, before) == {
        "vllm": {"new": ["APC"], "gone": ["multi-step"]}}


def test_a_repository_not_in_the_lockfile_is_all_new():
    """A first run has seen nothing before, and that is not the same as a
    repository having added everything overnight — the counts say which."""
    assert run.changes({"new-repo": {"items": ["a"]}}, {}) == {
        "new-repo": {"new": ["a"], "gone": []}}


def test_the_lockfile_round_trips(tmp_path: Path):
    observed = {"vllm": {"repo": "vllm-project/vllm", "kind": "adoption",
                         "sha": "a" * 40, "items": ["LoRA"]}}
    run.write_lock(tmp_path, observed)
    assert run.load_lock(tmp_path) == observed


def test_a_missing_lockfile_is_not_an_error(tmp_path: Path):
    assert run.load_lock(tmp_path) == {}


def test_the_lockfile_records_the_sha_it_read(tmp_path: Path):
    """ADR-058 requires the observation to name what it read. The pilot could
    not — it fetched from `main` and cannot now say which `main`."""
    run.write_lock(tmp_path, {"x": {"sha": "b" * 40, "items": []}})
    written = json.loads((tmp_path / run.LOCK).read_text())
    assert written["repos"]["x"]["sha"] == "b" * 40
    assert written["generated"].endswith("Z")


def test_an_unknown_extractor_refuses(tmp_path: Path):
    """A manifest typo must not silently extract nothing, which would report
    a repository as having lost every feature it has."""
    with pytest.raises(ValueError, match="unknown extractor"):
        run._extract("tabel", "| Feature |\n| - |\n| LoRA |\n")


def test_a_file_with_two_tables_can_select_one():
    """vLLM's quantization page holds a hardware matrix and an API reference.
    Reading both put `get_name()` in a list of techniques."""
    text = ("| Implementation | Ampere |\n| - | - |\n| AWQ | yes |\n"
            "\nsome prose\n\n"
            "| Method | Description |\n| - | - |\n| `get_name()` | the name |\n")
    assert extract.feature_names(text, 0) == ["AWQ"]
    assert extract.feature_names(text, 1) == ["`get_name()`"]
    assert len(extract.feature_names(text)) == 2, "both, when none is chosen"


def test_exported_names_strip_the_suffix():
    """`DDIMScheduler` is a class; `DDIM` is the technique, and the technique
    is what the record calls it."""
    text = '["DDIMScheduler", "LCMScheduler"]'
    assert extract.exported_names(text, "Scheduler") == ["DDIM", "LCM"]
