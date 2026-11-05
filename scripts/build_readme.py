#!/usr/bin/env python3
"""Build README.md and browse/*.md from data/entries.yaml.

Usage:
    python3 scripts/build_readme.py           # validate the data and write the outputs
    python3 scripts/build_readme.py --check   # validate and fail if the outputs are out of date

Badge rules (see CONTRIBUTING.md): an accepted venue gets a green badge; otherwise an arXiv
paper gets a red arXiv-YY.MM badge and an OpenReview submission a grey one. GitHub and GitLab
repositories show a live star count, except sub-directories of larger repositories.
"""
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path
from urllib.parse import quote

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "entries.yaml"
TEMPLATE = ROOT / "templates" / "README.md.tmpl"
README = ROOT / "README.md"
BROWSE = ROOT / "browse"

# key: (section title, one-line description, short label used in entry lines)
TYPES = {
    "agentic": ("Agentic workflows", "Multi-step LLM agents that iterate with compiler, test, or profiler feedback.", "Agentic workflow"),
    "search": ("Search and evolution", "LLMs embedded in evolutionary, tree, or beam search over kernel candidates.", "Search & evolution"),
    "trained": ("Trained kernel models", "Models trained (SFT, RL, distillation) specifically to write or optimize kernels.", "Trained model"),
    "single-pass": ("Single-pass generation and developer tools", "Single-pass or tool-assisted generation, programming models, and developer tooling.", "Single-pass / tooling"),
    "industry": ("Open-source and industry systems", "Open-source repositories, products, and vendor systems without a research paper.", "Open-source / industry system"),
    "benchmark": ("Benchmarks", "Benchmarks and datasets for evaluating LLM-generated kernels.", "Benchmark"),
    "general": ("General-purpose systems with kernel results", "General agents, optimizers, or code models whose evaluations include kernel tasks.", "General-purpose system"),
    "application": ("Applications", "Domain systems where LLM-written kernels are part of the development or evaluation.", "Application"),
    "tool": ("Infrastructure and tools", "Benchmarking isolation, tracing, and kernel libraries used by agents.", "Tool"),
    "study": ("Empirical studies", "Measurement studies and analyses of how LLMs write kernels.", "Empirical study"),
}
AGENT_TYPES = ["agentic", "search", "trained", "single-pass", "industry"]
CONTEXT_TYPES = ["general", "application", "tool", "study"]
HARDWARE = ["NVIDIA", "AMD", "Ascend", "Intel", "Google TPU", "AWS Neuron", "Apple", "CPU", "RISC-V", "Mobile GPU",
            "Meta MTIA", "Moore Threads", "Cambricon", "Tenstorrent", "T-Head PPU", "Hygon DCU", "Cerebras",
            "Research accelerators", "Other"]
LINK_KEYS = ["code", "model", "dataset", "project", "blog", "artifacts"]
FIELDS = {"id", "name", "title", "type", "date", "venue", "paper", "code_status", "institution", "kernel",
          "hardware", "benchmarks", "summary", *LINK_KEYS}
LIST_FIELDS = {"institution", "kernel", "hardware", "benchmarks"}
MONTH = dict(zip([f"{m:02d}" for m in range(1, 13)],
                 ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]))
MIN_VIEW = {"kernel": 4, "benchmarks": 3}  # tags used by fewer entries get no browse page of their own

ARXIV_RE = re.compile(r"arxiv\.org/abs/(\d{4})\.\d{4,5}")
GITHUB_RE = re.compile(r"https://github\.com/([^/]+)/([^/#?]+)(/(?:tree|blob)/[^/]+/.+)?$")
GITLAB_RE = re.compile(r"https://([^/]*gitlab[^/]*)/(.+?)/?$")
BLOG_HOSTS = {"amd.com": "AMD", "pytorch.org": "PyTorch", "nvidia.com": "NVIDIA", "fb.com": "Meta", "meta.com": "Meta",
              "cursor.com": "Cursor", "amazon.com": "AWS", "qwen.ai": "Qwen", "google.dev": "Google",
              "standardkernel.com": "Standard Kernel", "washington.edu": "UW"}
PRETTY_HOST = {"github.com": "GitHub", "gitcode.com": "GitCode", "arxiv.org": "arXiv", "huggingface.co": "HuggingFace"}


# ---------------------------------------------------------------- data

def load_entries() -> list[dict]:
    raw = yaml.safe_load(DATA.read_text(encoding="utf-8")) or {}
    entries = []
    for item in raw.get("entries") or []:
        entry = {k: (str(v) if k == "date" else v) for k, v in item.items()}
        for key in LIST_FIELDS:
            entry[key] = list(entry.get(key) or [])
        entries.append(entry)
    return entries


def validate(entries: list[dict]) -> list[str]:
    errors, seen = [], set()
    for idx, e in enumerate(entries):
        where = f"entry {idx} ({e.get('id', '?')})"
        for key in ("id", "name", "type", "date"):
            if not e.get(key):
                errors.append(f"{where}: missing '{key}'")
        if e.get("id") in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(e.get("id"))
        if e.get("id") and not re.fullmatch(r"[a-z0-9][a-z0-9.\-]*", str(e["id"])):
            errors.append(f"{where}: id must be lowercase letters, digits, '.', '-'")
        for key in set(e) - FIELDS:
            errors.append(f"{where}: unknown field '{key}'")
        if e.get("type") and e["type"] not in TYPES:
            errors.append(f"{where}: unknown type '{e['type']}'")
        if e.get("date") and not re.fullmatch(r"\d{4}-\d{2}(-\d{2})?", e["date"]):
            errors.append(f"{where}: date must be YYYY-MM or YYYY-MM-DD")
        if e.get("venue") and not re.fullmatch(r".+ \d{4}", str(e["venue"])):
            errors.append(f"{where}: venue must look like 'ICML 2026' or 'ICML Workshop 2026'")
        for key in ["paper", *LINK_KEYS]:
            if e.get(key) and not str(e[key]).startswith("https://"):
                errors.append(f"{where}: {key} must be an https URL")
        if e.get("code_status") not in (None, "unavailable"):
            errors.append(f"{where}: code_status must be 'unavailable' if set")
        if e.get("code_status") and not e.get("code"):
            errors.append(f"{where}: code_status needs a code URL")
        for hw in e.get("hardware") or []:
            if hw not in HARDWARE:
                errors.append(f"{where}: unknown hardware '{hw}' (allowed: {', '.join(HARDWARE)})")
        for key in LIST_FIELDS:
            if any("," in str(v) for v in e.get(key) or []):
                errors.append(f"{where}: {key} items must not contain commas")
        if not e.get("paper") and not any(e.get(k) for k in LINK_KEYS):
            errors.append(f"{where}: needs a paper or at least one link")
    return errors


def sort_key(e: dict):
    return (e["date"], e["name"].lower())


# ---------------------------------------------------------------- badges

def shield(text: str) -> str:
    return str(text).replace("-", "--").replace("_", "__").replace(" ", "_").replace("'", "%27")


def badge(alt: str, label: str, message: str, color: str, url: str | None = None) -> str:
    img = f"![{alt}](https://img.shields.io/badge/{shield(label)}-{shield(message)}-{color})"
    return f"[{img}]({url})" if url else img


def yymm(date: str) -> str:
    return f"{date[2:4]}.{date[5:7]}"


def host_of(url: str) -> str:
    return url.split("/")[2]


def pretty_host(url: str) -> str:
    host = host_of(url).removeprefix("www.")
    return PRETTY_HOST.get(host, host)


def paper_badge(e: dict) -> str | None:
    url = e.get("paper")
    if not url:
        return None
    if e.get("venue"):
        name, year = str(e["venue"]).rsplit(" ", 1)
        return badge(f"{name} {year}", name, year[2:], "green", url)
    match = ARXIV_RE.search(url)
    if match:
        return badge("arXiv", "arXiv", f"{match.group(1)[:2]}.{match.group(1)[2:]}", "red", url)
    if "openreview.net" in url:
        return badge("OpenReview", "OpenReview", yymm(e["date"]), "lightgrey", url)
    return badge("Report", "Report", yymm(e["date"]), "blue", url)


def blog_name(url: str, e: dict) -> str:
    host = host_of(url)
    for suffix, name in BLOG_HOSTS.items():
        if host == suffix or host.endswith("." + suffix):
            return name
    return (e["institution"][0] if e["institution"] else pretty_host(url))[:24]


def link_badge(kind: str, url: str, e: dict) -> str:
    if kind == "code":
        if e.get("code_status") == "unavailable":  # link the URL the authors published, even though it is gone
            return badge("Code unavailable", "Code", "unavailable", "lightgrey", url)
        gh = GITHUB_RE.match(url)
        if gh and gh.group(3):  # sub-directory: the star count would describe the parent repository
            return badge("Code", "Code", "GitHub", "blue", url)
        if gh:
            return f"[![Stars](https://img.shields.io/github/stars/{gh.group(1)}/{gh.group(2)})]({url})"
        gl = GITLAB_RE.match(url)
        if gl:
            query = "" if gl.group(1) == "gitlab.com" else f"?gitlab_url={quote('https://' + gl.group(1), safe='')}"
            return f"[![Stars](https://img.shields.io/gitlab/stars/{quote(gl.group(2), safe='')}{query})]({url})"
        return badge("Code", "Code", pretty_host(url), "blue", url)
    if kind in ("model", "dataset"):
        return badge(kind.title(), kind.title(), pretty_host(url), "yellow", url)
    if kind == "project":
        if "anonymous.4open.science" in url:
            return badge("Code", "Code", "Anonymous", "lightgrey", url)
        return badge("Project", "Project", "Page", "blue", url)
    if kind == "blog":
        if "/releases" in url:
            return badge("Release notes", "Release", "Notes", "blue", url)
        if "changelog" in url.lower():
            return badge("Changelog", "Changelog", pretty_host(url), "blue", url)
        return badge("Blog", "Blog", blog_name(url, e), "blue", url)
    return badge("Artifacts", "Artifacts", pretty_host(url), "lightgrey", url)


def badges(e: dict) -> str:
    out = [paper_badge(e)] + [link_badge(k, e[k], e) for k in LINK_KEYS if e.get(k)]
    return " ".join(b for b in out if b)


# ---------------------------------------------------------------- entry lines

def esc(text: str) -> str:
    return str(text).replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;").replace("*", "\\*")


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(text).lower())


def display_title(e: dict) -> str:
    title, name = e.get("title"), e["name"]
    if not title:
        return name
    variants = [re.sub(r"\s*\(.*?\)", "", name)] + re.findall(r"\((.*?)\)", name) + name.split(" / ")
    if any(norm(v) and norm(v) in norm(title) for v in variants):
        return title
    return f"{name}: {title}"


def entry_md(e: dict, show_type: bool = True) -> str:
    lines = [f"- **{esc(display_title(e))}** {badges(e)}".rstrip()]
    if e.get("summary") and not e.get("title"):
        lines.append(f"  - *{esc(e['summary'])}*")
    if e["institution"]:
        lines.append(f"  - **Institution:** {esc(', '.join(e['institution']))}")
    facts = []
    if show_type:
        facts.append(f"**Type:** {TYPES[e['type']][2]}")
    if e["kernel"]:
        facts.append("**Kernel:** " + " ".join(f"`{k}`" for k in e["kernel"]))
    if e["hardware"]:
        facts.append("**Hardware:** " + ", ".join(e["hardware"]))
    if e["benchmarks"] and e["type"] != "benchmark":
        facts.append("**Benchmark:** " + ", ".join(e["benchmarks"]))
    if facts:
        lines.append("  - " + " · ".join(facts))
    return "\n".join(lines)


def month_blocks(items: list[dict], show_type: bool) -> list[str]:
    by_month: dict[str, list[dict]] = collections.defaultdict(list)
    for e in sorted(items, key=sort_key, reverse=True):
        by_month[e["date"][:7]].append(e)
    out = []
    for month in sorted(by_month, reverse=True):
        out += [f"### {month}", "", "\n".join(entry_md(e, show_type) for e in by_month[month]), ""]
    return out


# ---------------------------------------------------------------- browse pages

def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def anchor(title: str) -> str:
    return "#" + re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")


def browse_page(title: str, items: list[dict], intro: str = "") -> str:
    lines = [f"# {title}", "", f"[← README](../README.md) · {len(items)} entries, newest first", ""]
    if intro:
        lines += [f"_{intro}_", ""]
    by_year: dict[str, list[dict]] = collections.defaultdict(list)
    for e in sorted(items, key=sort_key, reverse=True):
        by_year[e["date"][:4]].append(e)
    for year in sorted(by_year, reverse=True):
        lines += [f"## {year}", ""] + [entry_md(e) for e in by_year[year]] + [""]
    return "\n".join(lines).rstrip() + "\n"


def build_browse(entries: list[dict]) -> tuple[dict[str, str], dict[str, list[str]]]:
    pages: dict[str, str] = {}
    rows: dict[str, list[str]] = collections.defaultdict(list)

    def add(row: str, label: str, fname: str, title: str, items: list[dict], intro: str = "") -> None:
        pages[fname] = browse_page(title, items, intro)
        rows[row].append(f"[{label}](browse/{fname}) {len(items)}")

    for key in AGENT_TYPES + ["benchmark"] + CONTEXT_TYPES:
        items = [e for e in entries if e["type"] == key]
        if items:
            add("type", TYPES[key][0], f"type-{slug(TYPES[key][0])}.md", TYPES[key][0], items, TYPES[key][1])
    hw_count = collections.Counter(h for e in entries for h in e["hardware"])
    for hw in [h for h in HARDWARE if hw_count[h]]:
        add("hardware", hw, f"hw-{slug(hw)}.md", f"Hardware: {hw}", [e for e in entries if hw in e["hardware"]])
    lang_count = collections.Counter(k for e in entries for k in e["kernel"])
    main_langs = [k for k, n in lang_count.most_common() if n >= MIN_VIEW["kernel"]]
    for lang in main_langs:
        add("kernel", lang, f"lang-{slug(lang)}.md", f"Kernel language: {lang}", [e for e in entries if lang in e["kernel"]])
    other = [e for e in entries if e["kernel"] and not set(e["kernel"]) & set(main_langs)]
    if other:
        add("kernel", "Other", "lang-other.md", "Kernel language: other", other)
    bench_count = collections.Counter(b for e in entries for b in e["benchmarks"])
    for bench in [b for b, n in bench_count.most_common() if n >= MIN_VIEW["benchmarks"]]:
        add("benchmark", bench, f"bench-{slug(bench)}.md", f"Benchmark: {bench}", [e for e in entries if bench in e["benchmarks"]])
    years = sorted({e["date"][:4] for e in entries}, reverse=True)
    recent = [y for y in years if y >= "2025"]
    for year in recent:
        add("year", year, f"year-{year}.md", f"Year: {year}", [e for e in entries if e["date"][:4] == year])
    older = [e for e in entries if e["date"][:4] < "2025"]
    if older:
        add("year", "2024 and earlier", "year-2024-and-earlier.md", "Year: 2024 and earlier", older)
    pages["all.md"] = browse_page("All entries", entries, "Every entry on one page, newest first.")
    rows["all"].append("[All entries on one page](browse/all.md)")
    return pages, rows


def browse_table(rows: dict[str, list[str]]) -> str:
    labels = [("type", "Type"), ("hardware", "Hardware"), ("kernel", "Kernel language"), ("benchmark", "Benchmark"),
              ("year", "Year"), ("all", "Everything")]
    out = ["| Browse by | |", "| --- | --- |"]
    out += [f"| **{label}** | {' · '.join(rows[key])} |" for key, label in labels if rows.get(key)]
    return "\n".join(out)


# ---------------------------------------------------------------- README

LEGEND = (
    "**Badges:** "
    "![arXiv](https://img.shields.io/badge/arXiv-YY.MM-red) preprint · "
    "![Venue](https://img.shields.io/badge/Venue-YY-green) accepted at a peer-reviewed conference or workshop · "
    "![OpenReview](https://img.shields.io/badge/OpenReview-YY.MM-lightgrey) OpenReview submission, not yet accepted · "
    "![Blog](https://img.shields.io/badge/Blog-Org-blue) blog or technical report · "
    "![Stars](https://img.shields.io/badge/stars-live-white) GitHub stars, updated automatically"
)


def render(entries: list[dict]) -> dict[Path, str]:
    pages, rows = build_browse(entries)
    by_type = collections.Counter(e["type"] for e in entries)
    agents = [e for e in entries if e["type"] in AGENT_TYPES]
    months = sorted({e["date"][:7] for e in agents}, reverse=True)
    toc_years = []
    for year in sorted({m[:4] for m in months}, reverse=True):
        links = " · ".join(f"[{MONTH[m[5:7]]}](#{m}) {sum(1 for e in agents if e['date'][:7] == m)}"
                           for m in months if m[:4] == year)
        toc_years.append(f"  - **{year}** — {links}")
    context_toc = " · ".join(f"[{TYPES[k][0]}]({anchor(TYPES[k][0])}) ({by_type[k]})" for k in CONTEXT_TYPES)
    contents = "\n".join([
        f"- [**Kernel agents**](#kernel-agents) ({len(agents)})",
        *toc_years,
        f"- [**Benchmarks**](#benchmarks) ({by_type['benchmark']})",
        f"- **Context** — {context_toc}",
        "- **Resources** — [Evaluation integrity and reward hacking](#evaluation-integrity-and-reward-hacking) · "
        "[Competitions and leaderboards](#competitions-and-leaderboards) · [Datasets](#datasets) · "
        "[Representations and infrastructure](#representations-and-infrastructure)",
    ])
    stats = (f"**{len(agents)} kernel agents** · **{by_type['benchmark']} benchmarks** · "
             f"**{by_type['general']} general-purpose systems** · **{by_type['study']} empirical studies** · "
             f"**{by_type['application']} applications** · **{by_type['tool']} tools**")
    context = []
    for key in CONTEXT_TYPES:
        context += [f"## {TYPES[key][0]}", "", f"_{TYPES[key][1]}_", ""]
        context += month_blocks([e for e in entries if e["type"] == key], show_type=False)
    fills = {
        "STATS": stats,
        "BROWSE": browse_table(rows),
        "LEGEND": LEGEND,
        "CONTENTS": contents,
        "KERNEL_AGENTS": "\n".join(month_blocks(agents, show_type=True)).rstrip(),
        "BENCHMARKS": "\n".join(month_blocks([e for e in entries if e["type"] == "benchmark"], show_type=False)).rstrip(),
        "CONTEXT": "\n".join(context).rstrip(),
    }
    text = TEMPLATE.read_text(encoding="utf-8")
    for key, value in fills.items():
        text = text.replace("{{" + key + "}}", value)
    leftover = re.findall(r"\{\{[A-Z_]+\}\}", text)
    if leftover:
        raise SystemExit(f"template placeholders not filled: {leftover}")
    outputs = {README: re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n"}
    outputs.update({BROWSE / name: body for name, body in pages.items()})
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if README.md or browse/ is out of date")
    args = parser.parse_args()
    entries = load_entries()
    errors = validate(entries)
    if errors:
        print("data/entries.yaml has errors:\n  " + "\n  ".join(errors), file=sys.stderr)
        return 1
    outputs = render(entries)
    stale_browse = {p for p in BROWSE.glob("*.md")} - set(outputs)
    if args.check:
        stale = [str(p.relative_to(ROOT)) for p, body in outputs.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != body]
        stale += [str(p.relative_to(ROOT)) for p in stale_browse]
        if stale:
            print("out of date (run python3 scripts/build_readme.py):\n  " + "\n  ".join(stale), file=sys.stderr)
            return 1
        print(f"ok: {len(entries)} entries, {len(outputs)} files up to date")
        return 0
    BROWSE.mkdir(exist_ok=True)
    for path in stale_browse:
        path.unlink()
    for path, body in outputs.items():
        path.write_text(body, encoding="utf-8")
    print(f"wrote README.md and {len(outputs) - 1} browse pages from {len(entries)} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
