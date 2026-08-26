"""One-shot transform: `data/*.yaml` → a Luria record.

Run once, in the migration that adopted the record (ADR-001). Kept in the tree
rather than deleted because 238 hand-unreviewable files are only auditable if
the thing that wrote them is: every judgement this script makes is either in
`topic_map.yaml` beside it or in the tables below, where a reviewer can check
it against the source data.

    python -m scripts.migration.to_record --check   # report, write nothing
    python -m scripts.migration.to_record           # write the record

It does not run in CI and nothing depends on it. Phase 4 inverts the
direction — `registry.yaml` becomes a projection generated *from* the record
for the frontend — at which point this file becomes history and can go.
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
LIT_DIR = ROOT / "record" / "literature.d"
SOTA_DIR = ROOT / "record" / "practices.d"

# The seven the practice registry uses; LIT adds five more (see topic_map.yaml).
PRIMARY_WEIGHT = 3

# ─────────────────────────────────────────────────────────────────────────
# Judgements that are about individual papers rather than about the mapping,
# and so live here rather than in the topic map.
# ─────────────────────────────────────────────────────────────────────────

# Two papers reached the corpus with no identifier at all — which is what
# `requires = ["arxiv"]` in luria.toml exists to make impossible from now on.
# Both are unambiguous; these are their real ids.
MISSING_ARXIV = {
    "Imagen: Photorealistic Text-to-Image Diffusion Models": "2205.11487",
    "DALL-E 2: Hierarchical Text-Conditional Image Generation with CLIP Latents":
        "2204.06125",
}

# The attic, restated as statuses. The prose `reason` survives in the note
# body; what is written here is the short form the index table shows, and it
# is hand-written for all nine rather than truncated out of the reason,
# because a clause cut at 60 characters is not a status.
ATTIC_STATUS = {
    "2003.04881": "Superseded — by later work on clusterability and mechanistic interpretability",
    "2103.03386": "Rejected — the result does not look interesting enough to carry",
    "2104.08892": "Rejected — needs per-case tuning, no consistent cross-domain benefit",
    "2103.11851": "Superseded — single-cycle cosine decay proved better at scale",
    "2110.13016": "Rejected — theoretical, with no concrete training recommendation",
    "2303.07556": "Rejected — too domain-specific for a general training list",
    "2301.05217": "Rejected — measurement rather than actionable practice",
    "2302.06675": "Rejected — a research direction without demonstrated practical impact",
    "2302.14043": "Rejected — theoretical analysis without concrete recommendations",
}


# `sota_maybe` — one paper, two lines of doubt, and no field in the old schema
# that could hold "probably right, not yet willing to say so". It became
# nothing: the registry builder only ever read `sota`, so the hedge was
# invisible to every consumer.
#
# `Deferred` is the status for exactly this, and the claim is stated here
# rather than derived, because neither original line is a recommendation —
# one is an aside about adoption and one is a hyperparameter llama2 used.
# The claim behind them is written out; both originals are quoted verbatim in
# the body as the reason it is Deferred rather than Active.
DEFERRED_PRACTICES = {
    "1711.05101": [{
        "title": "Prefer AdamW's decoupled weight decay to L2 regularization "
                 "added to the loss",
        "tag": "training-optimization",
        "status": "Deferred — the paper is settled; how widely it is actually "
                  "adopted is not",
    }],
}


def slug_status(raw: str) -> str:
    return raw.split(" — ")[0].strip()


# ─────────────────────────────────────────────────────────────────────────
# YAML helpers
# ─────────────────────────────────────────────────────────────────────────

def q(text: str) -> str:
    """A YAML scalar that survives colons, quotes and unicode.

    Every title in this corpus is somebody else's prose — `Adam:`, `Attention
    Is All You Need`, `β₁=0.9` — so nothing here may rely on a string being
    plain-scalar safe.
    """
    return "'" + str(text).replace("'", "''") + "'"


def block(text: str, indent: str = "  ") -> str:
    """A folded block scalar. Used for `summary:`, which is prose and carries
    references that `luria link --fix` rewrites into links."""
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > 72:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return ">-\n" + "\n".join(indent + ln for ln in lines)


ARXIV_RE = re.compile(r"^\d{4}\.\d{4,5}$")


def norm_arxiv(value, title: str) -> str:
    """An arXiv id as a string, however the YAML happened to spell it.

    Two entries are unquoted in `research.yaml` and reach us as floats. Both
    survive `str()` intact, but a hypothetical `1412.6980` would not — YAML
    would hand back `1412.698` and the trailing digit would be gone with
    nothing to notice. So the shape is checked rather than assumed, and an id
    that does not look like one stops the migration.
    """
    if value in (None, ""):
        return ""
    text = repr(value) if isinstance(value, float) else str(value)
    if not ARXIV_RE.match(text):
        raise SystemExit(
            f"{title!r}: {value!r} does not look like an arXiv id — quote it "
            "in research.yaml")
    return text


# Everything in the record was filed on the same day, because it was: this is
# an import. `date:` is luria's *filing* date and staleness is measured from
# it, so putting a paper's publication date there would have reported the
# `Proposed` notes as nine years overdue for a decision — a warning that is
# permanently wrong, which is the kind that gets a check switched off. The
# publication month is a real fact and keeps its own field.
FILED = "2026-08-24"


def date_of(arxiv: str, year: int) -> str:
    """An arXiv id encodes YYMM, which is a better date than the year alone."""
    if m := re.match(r"^(\d{2})(\d{2})\.", arxiv or ""):
        yy, mm = int(m.group(1)), int(m.group(2))
        if 1 <= mm <= 12:
            return f"20{yy:02d}-{mm:02d}-01"
    return f"{year}-01-01"


# ─────────────────────────────────────────────────────────────────────────
# Loading and de-duplication
# ─────────────────────────────────────────────────────────────────────────

def load_papers() -> list[dict]:
    """Every paper, de-duplicated by arXiv id, in chronological order.

    The corpus carries PaLM twice, with two different `key_takeaways` lists
    and the same id — invisible while papers were rows in a YAML file and
    impossible once each one is a document named for its own identity. The
    two entries are merged rather than one being dropped: both takeaway lists
    were written by someone, so both are kept.
    """
    raw = yaml.safe_load((ROOT / "data" / "research.yaml").read_text())
    merged: dict[str, dict] = {}
    order: list[str] = []
    for year in sorted(raw):
        for paper in raw[year]:
            paper = dict(paper)
            paper.setdefault("year", year)
            arxiv = norm_arxiv(paper.get("arxiv_id"), paper["title"]) \
                or MISSING_ARXIV.get(paper["title"], "")
            paper["arxiv_id"] = arxiv
            key = arxiv or paper["title"]
            if key in merged:
                prior = merged[key]
                for field in ("key_takeaways", "topics", "models"):
                    seen = list(prior.get(field) or [])
                    for item in paper.get(field) or []:
                        if item not in seen:
                            seen.append(item)
                    if seen:
                        prior[field] = seen
                continue
            merged[key] = paper
            order.append(key)
    papers = [merged[k] for k in order]
    papers.sort(key=lambda p: (p["year"], p["arxiv_id"], p["title"]))
    return papers


def load_map() -> tuple[dict, dict, dict]:
    spec = yaml.safe_load((HERE / "topic_map.yaml").read_text())
    topic_to_tag = {
        topic: tag
        for tag, topics in spec["weights"].items()
        for topic in topics
    }
    return topic_to_tag, spec["registry_topics"], spec["overrides"]


def primary_tag(paper: dict, topic_to_tag: dict, overrides: dict) -> str:
    """The paper's one primary tag: weighted vote across its topics.

    The first topic counts triple. Ties break toward the earliest topic in the
    paper's own list, so the ordering somebody chose when writing the entry
    still decides when the arithmetic cannot.
    """
    if hit := overrides.get(paper["arxiv_id"]):
        return hit["tag"]
    score: dict[str, int] = defaultdict(int)
    rank: dict[str, int] = {}
    for i, topic in enumerate(paper.get("topics") or []):
        tag = topic_to_tag.get(topic)
        if not tag:
            continue
        score[tag] += PRIMARY_WEIGHT if i == 0 else 1
        rank.setdefault(tag, i)
    if not score:
        return "model-architecture"
    return min(score, key=lambda t: (-score[t], rank[t]))


def secondary_tags(paper: dict, topic_to_tag: dict, primary: str) -> list[str]:
    """None, on purpose.

    The first draft of this import derived secondaries the same way it derives
    the primary, and they were wrong in a specific way: the corpus's generic
    topic strings (`neural-networks`, `efficiency`, `training`) map somewhere,
    so Adam came out tagged `model-architecture` on the strength of
    `neural-networks` being in its topic list. That is not a claim the source
    data makes; it is an artifact of mapping a word that carries no category.

    A secondary tag is an editorial judgement that this paper genuinely
    belongs on a second page. The import has no way to make it, and inventing
    one puts noise on exactly the browsing pages the consolidation exists to
    make useful. Every original topic string survives in `keywords:`, so
    nothing is lost — add a secondary by hand when one is true.
    """
    return []


# ─────────────────────────────────────────────────────────────────────────
# Literature notes
# ─────────────────────────────────────────────────────────────────────────

def lit_status(paper: dict, by_arxiv: dict[str, str]) -> tuple[str, str, list[str]]:
    """`(status, trailing prose for the body)`.

    This is the split the whole restructure exists for. `attic` and
    `experimental` were fields on a paper; here they become that paper's
    status, and the recommendations drawn from it get their own.
    """
    arxiv = paper["arxiv_id"]
    if "attic" in paper:
        status = ATTIC_STATUS[arxiv]
        reason = (paper["attic"].get("reason") or "").strip()
        refs = paper["attic"].get("superseded_by") or []
        refs = [refs] if isinstance(refs, str) else list(refs)
        also = paper["attic"].get("see_also") or []
        also = [also] if isinstance(also, str) else list(also)
        if reason and reason[-1] not in ".?!":
            reason += "."
        parts = [reason] if reason else []
        cited: list[str] = []
        for ref in refs:
            code = by_arxiv.get(ref)
            if code:
                cited.append(code)
            parts.append(f"Superseded by {code}."
                         if code else
                         f"Superseded by ARXIV-{ref}, which is not in this "
                         "corpus.")
        for ref in also:
            code = by_arxiv.get(ref)
            if code:
                cited.append(code)
            parts.append(f"See also {code}."
                         if code else
                         f"See also ARXIV-{ref}, which is not in this corpus.")
        return status, " ".join(parts), cited
    if paper.get("experimental"):
        notes = paper.get("notes") or ([paper["note"]] if paper.get("note") else [])
        return "Proposed", " ".join(str(n).strip() for n in notes), []
    notes = paper.get("notes") or ([paper["note"]] if paper.get("note") else [])
    return "Active", " ".join(str(n).strip() for n in notes), []


def write_lit(paper: dict, code: str, tags: list[str], status: str,
              standing: str, cited: list[str]) -> str:
    arxiv = paper["arxiv_id"]
    cite = f"{paper['first_author']} et al. ({paper['year']})"
    takeaways = paper.get("key_takeaways") or []
    lead = takeaways[0] if takeaways else paper["title"]
    summary = f"{cite}, ARXIV-{arxiv}. {lead}."

    fm = [
        "---",
        f"status: {q(status)}",
        f"title: {q(paper['title'])}",
        "version: 1",
        "tags:",
        *[f"- {t}" for t in tags],
        f"date: {q(FILED)}",
        f"published: {q(date_of(arxiv, paper['year']))}",
        f"arxiv: {q(arxiv)}",
        f"first_author: {q(paper['first_author'])}",
    ]
    if paper.get("models"):
        fm += ["implementations:", *[f"- {m}" for m in paper["models"]]]
    # The topic strings this note was imported with, kept verbatim. The
    # controlled vocabulary above is what the record enforces; this is what
    # the corpus actually said, and throwing it away would make the
    # consolidation unreviewable.
    fm += ["keywords:", *[f"- {q(t)}" for t in paper.get("topics") or []]]
    fm += [f"summary: {block(summary)}", "---", ""]

    body = [f"# {code}: {paper['title']}", "",
            f"{cite} — ARXIV-{arxiv}", ""]
    if takeaways:
        body += ["## Key takeaways", ""]
        body += [f"- {t}" for t in takeaways]
        body += [""]
    if paper.get("historical_impact"):
        body += ["## Historical impact", ""]
        body += [f"- {t}" for t in paper["historical_impact"]]
        body += [""]
    if standing:
        body += ["## Standing in the anthology", ""]
        # A supersession pointer cites a document that is, by construction,
        # not in force — and sometimes one that is itself retired, which is
        # inactive-ok: LIT-031, LIT-041 — named because they are the case
        # the LIT-031 → LIT-041 chain ADR-004 describes. That citation is the
        # whole content of the section, so it is vouched for here rather than
        # left on the report for someone to rediscover.
        if cited:
            body += [f"<!-- inactive-ok-block: {', '.join(cited)} — the "
                     "successor or cross-reference this retirement names -->"]
        body += [standing, ""]
    return "\n".join(fm + body)


# ─────────────────────────────────────────────────────────────────────────
# Practices
# ─────────────────────────────────────────────────────────────────────────

def write_sota(rec: str, code: str, paper: dict, lit_code: str, tag: str,
               status: str, hedges: list[str] | None = None) -> str:
    cite = f"{paper['first_author']} et al. ({paper['year']})"
    arxiv = paper["arxiv_id"]
    fm = [
        "---",
        f"status: {q(status)}",
        f"title: {q(rec)}",
        "version: 1",
        "tags:",
        f"- {tag}",
        f"date: {q(FILED)}",
        f"published: {q(date_of(arxiv, paper['year']))}",
        f"source: {lit_code}",
        f"summary: {block(f'{cite}, {lit_code} — ARXIV-{arxiv}.')}",
    ]
    if paper.get("models"):
        fm += ["implementations:", *[f"- {m}" for m in paper["models"]]]
    fm += ["---", ""]
    body = [f"# {code}: {rec}", "",
            "## Source", "",
            f"{cite}, {lit_code} — ARXIV-{arxiv}.", ""]
    if paper.get("models"):
        body += ["## Known implementations", ""]
        body += [f"- {m}" for m in paper["models"]]
        body += [""]
    if hedges:
        body += ["## Why this is deferred", "",
                 "Carried over from the `sota_maybe` field, verbatim:", ""]
        for i, hedge in enumerate(hedges):
            if i:
                body += [">"]
            body += [f"> {hedge}"]
        body += ["",
                 "The claim above is not in doubt; its adoption is. Promote "
                 "it to `Active` when that question is settled, or supersede "
                 "it if the answer turns out to be no.", ""]
    return "\n".join(fm + body)


# ─────────────────────────────────────────────────────────────────────────

def run(check: bool = False) -> None:
    topic_to_tag, registry_topics, overrides = load_map()
    papers = load_papers()

    unmapped = {t for p in papers for t in (p.get("topics") or [])
                if t not in topic_to_tag}
    if unmapped:
        raise SystemExit(
            "topic_map.yaml does not cover: " + ", ".join(sorted(unmapped)))

    by_arxiv = {p["arxiv_id"]: f"LIT-{i:03d}"
                for i, p in enumerate(papers, 1) if p["arxiv_id"]}

    # Two passes over the statuses: a cross-reference is only worth vouching
    # for when its target is retired, and pass one is the only way to know
    # that before pass two writes the note that cites it. A directive on a
    # live target is a stale annotation, which the lint reports — correctly.
    retired_free = {
        f"LIT-{i:03d}": lit_status(p, by_arxiv)[0] == "Active"
        for i, p in enumerate(papers, 1)
    }

    lit_files: dict[Path, str] = {}
    tag_of: dict[str, str] = {}
    for i, paper in enumerate(papers, 1):
        code = f"LIT-{i:03d}"
        primary = primary_tag(paper, topic_to_tag, overrides)
        tag_of[paper["arxiv_id"]] = primary
        tags = [primary] + secondary_tags(paper, topic_to_tag, primary)
        status, standing, cited = lit_status(paper, by_arxiv)
        cited = [c for c in cited if not retired_free[c]]
        lit_files[LIT_DIR / f"{code}.md"] = write_lit(
            paper, code, tags, status, standing, cited)

    registry = yaml.safe_load((ROOT / "data" / "registry.yaml").read_text())
    paper_by_arxiv = {p["arxiv_id"]: p for p in papers}

    sota_files: dict[Path, str] = {}
    n = 0
    for entry in registry["recommendations"]:
        arxiv = entry["source"].get("arxiv_id")
        paper = paper_by_arxiv.get(arxiv)
        if paper is None:
            raise SystemExit(f"no paper for recommendation {entry['id']}")
        n += 1
        code = f"SOTA-{n:03d}"
        # A practice's category comes from the registry's own topic through
        # the seven-category table, not from the paper's LIT tag: the paper
        # may sit in one of the five categories only the reading list has.
        tag = registry_topics.get(entry["topic"])
        if tag is None:
            raise SystemExit(f"no seven-category home for topic {entry['topic']!r}")
        sota_files[SOTA_DIR / f"{code}.md"] = write_sota(
            entry["recommendation"], code, paper,
            by_arxiv[arxiv], tag, "Active")

    # The hedges, which the old builder dropped on the floor.
    for arxiv, claims in DEFERRED_PRACTICES.items():
        paper = paper_by_arxiv[arxiv]
        hedges = [str(h).strip() for h in paper.get("sota_maybe") or []]
        for claim in claims:
            n += 1
            code = f"SOTA-{n:03d}"
            sota_files[SOTA_DIR / f"{code}.md"] = write_sota(
                claim["title"], code, paper, by_arxiv[arxiv], claim["tag"],
                claim["status"], hedges)

    counts: dict[str, int] = defaultdict(int)
    for text in lit_files.values():
        counts[slug_status(text.split("status: '", 1)[1].split("'", 1)[0])] += 1
    print(f"papers    {len(papers)} → {len(lit_files)} notes  "
          f"({dict(counts)})")
    print(f"practices {len(sota_files)}")
    tagged: dict[str, int] = defaultdict(int)
    for t in tag_of.values():
        tagged[t] += 1
    for t, c in sorted(tagged.items(), key=lambda kv: -kv[1]):
        print(f"   {c:3d}  {t}")

    if check:
        return
    for directory, files in ((LIT_DIR, lit_files), (SOTA_DIR, sota_files)):
        directory.mkdir(parents=True, exist_ok=True)
        for path, text in files.items():
            path.write_text(text)
    print(f"wrote {len(lit_files) + len(sota_files)} documents")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report what would be written, write nothing")
    run(**vars(ap.parse_args()))
