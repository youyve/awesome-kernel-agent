#!/usr/bin/env python3
"""Generate README tables from data/agents.yaml (single source of truth).

Validates entries against the controlled vocabularies, renders the generated
sections (STATS / AGENTS / MATRIX / TIMELINE) into README.md and README.zh.md
between <!-- BEGIN:X --> / <!-- END:X --> markers, and exports
data/agents.json.

Usage:
    python3 scripts/generate.py            # validate + write
    python3 scripts/generate.py --check    # validate only (CI)

Requires: PyYAML
"""
from __future__ import annotations
import argparse, json, os, re, sys
from collections import Counter, defaultdict

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "agents.yaml")
JSON_OUT = os.path.join(ROOT, "data", "agents.json")
READMES = [os.path.join(ROOT, "README.md"), os.path.join(ROOT, "README.zh.md")]

# ---------------------------------------------------------------- vocabularies
ROUTES = ["A", "B", "C", "D", "E", "tool"]
STATUS = {
    "open": "🟢 OPEN", "partial": "🟡 PARTIAL", "wip": "🟠 WIP",
    "closed": "⚪ CLOSED", "proprietary": "⚫ PROPRIETARY",
}
CLAIM_BADGE = {"yes": "✅", "partial": "◐", "no": "—", "unknown": "?"}

# Primary-DSL sections in display order: (dsl key, heading, blurb).
# Any dsl not listed here lands in the trailing "Emerging" section.
SECTIONS_DSL = [
    ("Triton",   "Triton",              "Largest ecosystem — Python-like syntax and abundant pretraining data make it the LLM lingua franca."),
    ("CUDA",     "CUDA / CUDA-C++",     "The performance-ceiling battleground — RL training, evolutionary search, and multi-agent orchestration."),
    ("CUTLASS",  "CUTLASS / CuTe DSL",  "Template-level performance with a steep learning curve — agents must reason about tiles, layouts, and warp specialization."),
    ("AscendC",  "Ascend C / NPU",      "The fastest-growing non-NVIDIA stack — but mostly closed."),
    ("HIP",      "HIP / ROCm (AMD)",    ""),
    ("NKI",      "NKI (AWS Trainium)",  ""),
    ("SYCL",     "SYCL (Intel)",        ""),
    ("TileLang", "TileLang",            ""),
]
EMERGING_HEADING = "Emerging DSLs & other accelerators"
EMERGING_BLURB = "New backends where AI codegen is in the loop from day one."
MAIN_DSLS = [s[0] for s in SECTIONS_DSL]

REQUIRED = ["id", "name", "org", "date", "route", "status", "dsl",
            "desc", "claim_baseline", "ships_kernels", "budget_disclosed"]


# --------------------------------------------------------------------- loading
def load():
    with open(DATA, encoding="utf-8") as fh:
        entries = yaml.safe_load(fh)["agents"]
    # YAML 1.1 parses bare yes/no as booleans; coerce back to strings.
    for e in entries:
        for f in ("ships_kernels", "budget_disclosed"):
            if isinstance(e.get(f), bool):
                e[f] = "yes" if e[f] else "no"
    return entries


def validate(entries):
    errors = []
    seen = set()
    for e in entries:
        tag = e.get("id") or e.get("name") or "<unknown>"
        for f in REQUIRED:
            if e.get(f) in (None, ""):
                errors.append(f"{tag}: missing required field '{f}'")
        if e.get("id") in seen:
            errors.append(f"duplicate id: {e['id']}")
        seen.add(e.get("id"))
        if not (e.get("code") or e.get("paper")):
            errors.append(f"{tag}: needs at least one of code/paper")
        if e.get("route") not in ROUTES:
            errors.append(f"{tag}: bad route '{e.get('route')}'")
        if e.get("status") not in STATUS:
            errors.append(f"{tag}: bad status '{e.get('status')}'")
        if not re.fullmatch(r"\d{4}-\d{2}", str(e.get("date", ""))):
            errors.append(f"{tag}: date must be YYYY-MM, got '{e.get('date')}'")
        for f in ("ships_kernels", "budget_disclosed"):
            if e.get(f) not in CLAIM_BADGE:
                errors.append(f"{tag}: bad {f} '{e.get(f)}'")
        if not isinstance(e.get("evaluated_on", []), list):
            errors.append(f"{tag}: evaluated_on must be a list")
    return errors


# ------------------------------------------------------------------ rendering
def best_link(e):
    return e.get("code") or e.get("paper")


def render_entry(e):
    head = f"- [{e['name']}]({best_link(e)}) — {e['org']} · {e['date']} · "
    head += "*tooling*" if e["route"] == "tool" else f"**[{e['route']}]**"
    head += f" · {STATUS[e['status']]}"
    if e.get("dsl_also"):
        head += " · also: " + ", ".join(e["dsl_also"])
    body = "  " + e["desc"]
    extras = []
    if e.get("paper") and e.get("paper") != best_link(e):
        extras.append(f"[Paper]({e['paper']})")
    if e.get("blog"):
        extras.append(f"[Blog]({e['blog']})")
    if extras:
        body += " " + " · ".join(extras)
    if e.get("note"):
        body += f" *{e['note']}*"
    ev = " / ".join(e.get("evaluated_on") or ["?"])
    claims = (f"  <sub>eval: {ev} · claim vs: {e['claim_baseline']} · "
              f"ships kernels: {CLAIM_BADGE[e['ships_kernels']]} · "
              f"budget: {CLAIM_BADGE[e['budget_disclosed']]}</sub>")
    return "\n".join([head, body, claims])


def render_agents(entries):
    by_date = lambda e: e["date"]
    blocks = []
    for dsl, heading, blurb in SECTIONS_DSL:
        rows = sorted([e for e in entries if e["dsl"] == dsl], key=by_date, reverse=True)
        cross = sorted([e for e in entries if dsl in (e.get("dsl_also") or [])], key=by_date, reverse=True)
        if not rows and not cross:
            continue
        blocks.append(f"### {heading}\n")
        if blurb:
            blocks.append(f"> {blurb}\n")
        blocks += [render_entry(e) for e in rows]
        if cross:
            sec = {s[0]: s[1] for s in SECTIONS_DSL}
            blocks.append("\n<sub>Cross-listed: " + " · ".join(
                f"**{e['name']}** (see {sec.get(e['dsl'], EMERGING_HEADING)})" for e in cross) + "</sub>")
        blocks.append("")
    emerging = sorted([e for e in entries if e["dsl"] not in MAIN_DSLS], key=by_date, reverse=True)
    if emerging:
        blocks.append(f"### {EMERGING_HEADING}\n")
        blocks.append(f"> {EMERGING_BLURB}\n")
        blocks += [render_entry(e) for e in emerging]
    return "\n".join(blocks).rstrip()


def render_stats(entries):
    agents = [e for e in entries if e["route"] != "tool"]
    tools = len(entries) - len(agents)
    by_route = Counter(e["route"] for e in agents)
    by_status = Counter(e["status"] for e in agents)
    dsls = sorted({e["dsl"] for e in entries} | {d for e in entries for d in e.get("dsl_also") or []})
    ships = sum(1 for e in agents if e["ships_kernels"] == "yes")
    out = [
        f"**{len(agents)} agent systems** (+{tools} tooling entries) across **{len(dsls)} DSLs/backends** · "
        f"last data update **{max(e['date'] for e in entries)}**.",
        "",
        "| Route | A single-shot | B iterative | C RL | D multi-agent+profiler | E evolutionary |",
        "|:---|:--:|:--:|:--:|:--:|:--:|",
        "| **Count** | " + " | ".join(str(by_route.get(r, 0)) for r in "ABCDE") + " |",
        "",
        "| Status | 🟢 open | 🟡 partial | 🟠 wip | ⚪ closed | ⚫ proprietary |",
        "|:---|:--:|:--:|:--:|:--:|:--:|",
        "| **Count** | " + " | ".join(str(by_status.get(s, 0)) for s in
                                       ("open", "partial", "wip", "closed", "proprietary")) + " |",
        "",
        f"Only **{ships}/{len(agents)}** agent systems ship re-runnable generated kernels "
        f"(`ships kernels: ✅`) — the rest of the headline speedups cannot be independently audited.",
    ]
    return "\n".join(out)


def render_matrix(entries):
    cols = MAIN_DSLS + ["Emerging"]
    counts = defaultdict(lambda: defaultdict(int))
    for e in entries:
        col = e["dsl"] if e["dsl"] in MAIN_DSLS else "Emerging"
        counts[e["route"]][col] += 1
    route_label = {"A": "A single-shot", "B": "B iterative", "C": "C multi-turn RL",
                   "D": "D multi-agent+profiler", "E": "E evolutionary", "tool": "tooling"}
    out = ["| Route \\ DSL | " + " | ".join(cols) + " | Σ |",
           "|:---|" + ":--:|" * (len(cols) + 1)]
    for r in ROUTES:
        tot = sum(counts[r][c] for c in cols)
        if tot == 0:
            continue
        out.append(f"| {route_label[r]} | " +
                   " | ".join(str(counts[r][c] or "") for c in cols) + f" | {tot} |")
    out.append("")
    out.append("Empty cells are open gaps — e.g. no trained-RL (C) agent exists outside "
               "Triton/CUDA/Ascend/MUSA, and Pallas (TPU) / Triton-Gluon still have no dedicated agent at all.")
    return "\n".join(out)


def render_timeline(entries):
    by_month = defaultdict(list)
    for e in entries:
        if e["route"] != "tool":
            by_month[e["date"]].append(e)
    out = ["```mermaid", "timeline",
           "    title LLM kernel agents by month (route in brackets)"]
    year = None
    for month in sorted(by_month):
        y = month[:4]
        if y != year:
            out.append(f"    section {y}")
            year = y
        names = " : ".join(f"{e['name']} [{e['route']}]" for e in sorted(by_month[month], key=lambda e: e["name"]))
        out.append(f"        {month} : {names}")
    out.append("```")
    return "\n".join(out)


SECTIONS = {
    "STATS": render_stats,
    "AGENTS": render_agents,
    "MATRIX": render_matrix,
    "TIMELINE": render_timeline,
}


def inject(text, key, content):
    begin, end = f"<!-- BEGIN:{key} -->", f"<!-- END:{key} -->"
    if begin not in text or end not in text:
        return text
    pre, post = text.split(begin)[0], text.split(end, 1)[1]
    note = "<!-- generated by scripts/generate.py — do not edit by hand -->"
    return f"{pre}{begin}\n{note}\n\n{content}\n\n{end}{post}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    entries = load()
    errors = validate(entries)
    if errors:
        for e in errors:
            print(f"  ERROR: {e}", file=sys.stderr)
        sys.exit(f"{len(errors)} validation error(s)")
    print(f"validated {len(entries)} entries")
    if args.check:
        return

    with open(JSON_OUT, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    for readme in READMES:
        if not os.path.exists(readme):
            continue
        with open(readme, encoding="utf-8") as fh:
            txt = fh.read()
        for key, fn in SECTIONS.items():
            txt = inject(txt, key, fn(entries))
        with open(readme, "w", encoding="utf-8") as fh:
            fh.write(txt)
        print(f"wrote {os.path.basename(readme)}")
    print("wrote data/agents.json")


if __name__ == "__main__":
    main()
