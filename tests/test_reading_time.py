# tests/test_reading_time.py
"""The reading-time ranking merges one paper's several feed keys into one work.

The feed files a paper under whatever id the page offered: `2401.00001`,
`arxiv.2401.00001`, a `url.*` hash whose URL is the arXiv PDF, or a bare
title. Ranked unmerged, one paper's time is split across rows and falls down
the list — which is the failure these tests pin.
"""

from scripts.audit.reading_time import aggregate, unheld


def _session(seconds: int) -> dict:
    return {"type": "reading_session", "data": {"duration_seconds": seconds, "idle_seconds": 99}}


def _snapshot() -> dict:
    return {
        "paper:2401.00001": {"data": {"title": "A Paper", "url": "https://arxiv.org/abs/2401.00001"}},
        "interactions:2401.00001": {"data": {"interactions": [_session(100)]}},
        "paper:arxiv.2401.00001": {"data": {"title": "A Paper", "url": "https://arxiv.org/abs/2401.00001"}},
        "interactions:arxiv.2401.00001": {"data": {"interactions": [_session(50), {"type": "rating", "data": {}}]}},
        "paper:url.ABCD": {"data": {"title": "ABCD", "url": "https://arxiv.org/pdf/2401.00001v2"}},
        "interactions:url.ABCD": {"data": {"interactions": [_session(25)]}},
        "paper:url.EF01": {"data": {"title": "A  Paper", "url": "https://example.org/a-paper"}},
        "interactions:url.EF01": {"data": {"interactions": [_session(5)]}},
        "paper:url.9999": {"data": {"title": "A Blog Post About Diffusion", "url": "https://example.org/blog"}},
        "interactions:url.9999": {"data": {"interactions": [_session(300), _session(1)]}},
        "paper:url-misc.AA": {"data": {"title": "Just a moment...", "url": "https://doi.org/x"}},
        "interactions:url-misc.AA": {"data": {"interactions": [_session(7)]}},
        "paper:url-misc.BB": {"data": {"title": "Just a moment...", "url": "https://doi.org/y"}},
        "interactions:url-misc.BB": {"data": {"interactions": [_session(3)]}},
    }


def test_one_paper_under_four_keys_is_one_work():
    works = aggregate(_snapshot())
    paper = next(w for w in works if w.arxiv == "2401.00001")
    assert paper.seconds == 180
    assert paper.sessions == 4


def test_duration_is_active_time_and_ratings_are_not_sessions():
    works = {w.title: w for w in aggregate(_snapshot())}
    assert works["A Blog Post About Diffusion"].seconds == 301
    assert works["A Blog Post About Diffusion"].sessions == 2


def test_ranked_by_seconds_descending():
    assert [w.seconds for w in aggregate(_snapshot())] == [301, 180, 7, 3]


def test_a_cloudflare_interstitial_is_not_a_title():
    """169 sessions share the title "Just a moment..." — merged, they top the ranking."""
    blocked = [w for w in aggregate(_snapshot()) if w.key.startswith("id:")]
    assert sorted(w.seconds for w in blocked) == [3, 7]


def test_unheld_drops_by_arxiv_id_and_by_title():
    works = aggregate(_snapshot())
    assert [w.title for w in unheld(works, ids={"2401.00001"}, titles=set())][:1] == ["A Blog Post About Diffusion"]
    assert [w.arxiv for w in unheld(works, ids=set(), titles={"A blog post about diffusion"})][:1] == ["2401.00001"]
