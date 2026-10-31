"""Agent 9 - Approval clerk. Drafts the approval request and the one-page approval sheet, then stops.

It never sends anything. It freezes the pack (hash of text and media) and sets the release status to
AWAITING_INTERNAL_REVIEW. Only engine.gate can move it on, and only with signed decisions on file."""
from __future__ import annotations

import re
from datetime import date, timedelta

from ..core import RunContext, md_table, sha256_of
from .factcheck import REF


def add_business_days(start: date, n: int, holidays: set) -> date:
    d = start
    while n:
        d += timedelta(days=1)
        if d.weekday() < 5 and d.isoformat() not in holidays:
            n -= 1
    return d


def numbers_register(ctx: RunContext) -> list[list]:
    seen, rows = set(), []
    for aud, text in ctx.drafts.items():
        for kind, rid in REF.findall(text):
            if (kind, rid) in seen:
                continue
            seen.add((kind, rid))
            if kind == "M" and rid in ctx.metrics:
                m = ctx.metrics[rid]
                rows.append([m["name"], f"{m['value']:.{m['decimals']}f}{m['unit']}", f"`{m['source']}`", m["working"][:140]])
            elif kind == "E" and ctx.ledger.get(rid) and re.search(r"\d", ctx.ledger.get(rid).quote):
                e = ctx.ledger.get(rid)
                rows.append([e.summary, f'"{e.quote}"', f"`{e.ref}`", "quoted from the record"])
    return rows


def run(ctx: RunContext) -> dict:
    cfg, ap = ctx.config, ctx.config["approval"]
    sent = date.fromisoformat(ap["planned_send_date"])
    reply_by = add_business_days(sent, ap["review_business_days"], set(ap.get("holidays", [])))
    first_use = add_business_days(reply_by, 1, set(ap.get("holidays", [])))
    media_rows = [[m["file"], m["label"], m["reader"]] for m in ctx.media]
    changes = [[c["what"], c["why"], c["rule"]] for c in cfg["approval"]["changes_made"]]
    n_refused = sum(len(v["refused"]) for v in ctx.verified.values())

    request = [
        "# Approval request (DRAFT - not sent)", "",
        "> Held by the engine. A PredCo reviewer must approve this pack before it is sent (see engine/gate.py). Nothing leaves the building from here.", "",
        f"**To:** {ap['to']}  ",
        f"**Cc:** {ap['cc']}  ",
        f"**From:** {ap['from']}  ",
        f"**Subject:** {ap['subject']}", "",
        *ap["message"], "",
        f"**Reply requested by {reply_by.strftime('%A %d %B %Y')}** - {ap['review_business_days']} business days from {sent.strftime('%d %B %Y')}, as clause 15.2(e) requires. "
        f"Holidays assumed: {', '.join(ap.get('holidays', [])) or 'none'} (ASSUMED - please correct for your calendar). We will not use any of it before {first_use.strftime('%d %B %Y')}, "
        "and not at all without a written yes.", "",
        *ap["signoff"], "",
    ]
    ctx.write("06_approval/approval_request_email.md", "\n".join(request))

    sheet = [
        f"# Approval sheet - {cfg['anonymised_title']}", "",
        f"**For:** {ap['to']} | **Copy:** {ap['cc']} | **Reply by:** {reply_by.isoformat()} | **Our reference:** {ap['reference']}", "",
        "## 1. Your choice (tick one)", "",
        md_table(["", "Option", "What it means", "What we publish"], [["☐", o["name"], o["means"], o["publishes"]] for o in ap["options"]]), "",
        "You can withdraw any approval later by written notice; we stop new use within 30 days (clause 15.4).", "",
        "## 2. Exactly what would be used", "",
        "- Text: `04_case_study.md` (attached in full, four short versions).",
        *[f"- Media: `{r[0]}` - {r[1]}" for r in media_rows],
        "- Nothing else: no logo, no photo of premises, people or vehicles, no screenshot of your systems.", "",
        "## 3. Every number and where it comes from", "",
        md_table(["Claim", "Value", "Your record", "How it was worked out"], numbers_register(ctx)), "",
        "## 4. What we changed, and why", "",
        md_table(["Change", "Why", "Rule"], changes), "",
        f"The engine also refused {n_refused} draft line(s) that could not be traced to a record or broke a rule (log available on request).", "",
        "## 5. What we deliberately do not claim", "",
        md_table(["Not claimed", "Why"], [[d["claim"], d["why"]] for d in cfg.get("do_not_claim", [])]), "",
        "## 6. Sign-off", "",
        md_table(["Role", "Name", "Decision", "Date", "Signature"],
                 [[r, "", "", "", ""] for r in ap["signatory_roles"]]), "",
    ]
    ctx.write("06_approval/approval_sheet.md", "\n".join(sheet))

    pack = [ctx.out_dir / "04_case_study.md"] + [ctx.out_dir / m["file"] for m in ctx.media]
    digest = sha256_of(pack)
    ctx.write_json("06_approval/pack_manifest.json", {"files": [p.relative_to(ctx.out_dir).as_posix() for p in pack], "sha256": digest,
                                                       "reply_by": reply_by.isoformat()})
    ctx.write_json("RELEASE_STATUS.json", {"status": "AWAITING_INTERNAL_REVIEW", "pack_sha256": digest,
                                           "next": "Internal reviewer signs approvals/internal_review.json, then run: python run_engine.py gate"})
    ctx.note("approval", f"approval pack frozen (sha256 {digest[:12]}...); reply-by {reply_by}; STOPPED for human review")
    return {"sha256": digest, "reply_by": reply_by.isoformat()}
