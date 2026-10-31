"""Agent 3 - Historian. Builds the dated story spine from verified evidence only.

Job: first contact to today, in order - asked, scoped, changed (and why), delivered, who decided.
Every line carries its file:line. Turning points (tag `turning_point`) are marked."""
from __future__ import annotations

from collections import defaultdict
from datetime import date

from ..core import RunContext, md_table

SPINE_KINDS = {"event", "decision", "change", "request", "risk"}
LABEL = {"event": "Happened", "decision": "Decided", "change": "Changed", "request": "Asked for", "risk": "Problem"}


def run(ctx: RunContext) -> list:
    items = sorted((e for e in ctx.ledger.items.values() if e.kind in SPINE_KINDS or "turning_point" in e.tags),
                   key=lambda e: (e.date, e.id))
    by_month = defaultdict(list)
    for e in items:
        by_month[e.date[:7]].append(e)

    cfg = ctx.config
    out = [f"# Project story spine - {cfg['project_label']}", "",
           "Built only from evidence items whose quote was found verbatim in the library. "
           "★ marks a turning point. Names here are internal; the exposure report says what may leave the building.", ""]
    phases = cfg.get("phases", [])
    if phases:
        out += ["## Phases", "", md_table(["Phase", "From", "To", "What it was"],
                                          [[p["name"], p["from"], p["to"], p["what"]] for p in phases]), ""]
    for month in sorted(by_month):
        out += [f"## {month}", ""]
        rows = []
        for e in by_month[month]:
            star = "★ " if "turning_point" in e.tags else ""
            rows.append([e.date, LABEL.get(e.kind, e.kind.title()), star + e.summary, e.actor or "-",
                         f"`{e.ref}`", e.id])
        out += [md_table(["Date", "Type", "What", "Who decided / said", "Source", "Evidence"], rows), ""]

    changes = [e for e in items if e.kind == "change"]
    if changes:
        out += ["## What changed between promise and delivery", "",
                md_table(["Date", "Change", "Source"], [[e.date, e.summary, f"`{e.ref}`"] for e in changes]), ""]
    tr = cfg.get("tracker")
    if tr and ctx.library.exists(tr["file"]):
        slips = []
        for r in ctx.library.csv_rows(tr["file"], merge_overflow_into=tr["task"]):
            pe, ae = r.get(tr["planned_end"], ""), r.get(tr["actual_end"], "")
            if pe and ae:
                days = (date.fromisoformat(ae) - date.fromisoformat(pe)).days
                if days > 0 or r.get(tr["status"]) not in ("Done", ""):
                    slip = f"+{days} d" if r.get(tr["status"]) in ("Done", "") else r[tr["status"]]
                    slips.append([r[tr["id"]], r[tr["task"]], r[tr["owner"]], pe, ae, slip, r.get(tr["notes"], "")])
            elif r.get(tr["status"]) not in ("Done", ""):
                slips.append([r[tr["id"]], r[tr["task"]], r[tr["owner"]], pe, ae or "-", r[tr["status"]], r.get(tr["notes"], "")])
        out += ["## Delays and how they were overcome (from the project tracker)", "",
                f"Source: `{tr['file']}`. Tasks that finished after their planned end, or are not done.", "",
                md_table(["Task", "What", "Owner", "Planned end", "Actual end", "Slip", "Tracker note"], slips), ""]
    if ctx.library.data_issues:
        out += ["## Data-quality issues found while reading", ""] + [f"- {d}" for d in ctx.library.data_issues] + [""]
    ctx.write("01_story_spine.md", "\n".join(out))
    ctx.note("historian", f"story spine: {len(items)} dated lines across {len(by_month)} months")
    return items
