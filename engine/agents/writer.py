"""Agent 6 - Writer. One true story told three ways (gatekeeper, user, buyer) plus a champion note.

Contract with the fact-checker: one claim per line, and every line ends with its sources:
[E:<evidence id>] for a quote or fact, [M:<metric id>] for a computed number. A line with no factual
claim (a heading-like transition, a question) is marked {framing}. With --llm, Claude writes the drafts
from the verified ledger and metrics (prompts/writer.md); otherwise the reviewed drafts in
projects/<name>/drafts/ are used. Both are checked line by line before anything is kept."""
from __future__ import annotations

import json

from .. import llm
from ..core import RunContext

AUDIENCES = ["gatekeeper", "user", "buyer", "champion"]


def brief(ctx: RunContext) -> str:
    ev = [{"id": e.id, "date": e.date, "kind": e.kind, "summary": e.summary, "quote": e.quote, "tags": e.tags}
          for e in ctx.ledger.items.values()]
    metrics = [{"id": m["id"], "name": m["name"], "value": round(m["value"], m["decimals"]), "unit": m["unit"],
                "note": m["note"]} for m in ctx.metrics.values()]
    return json.dumps({
        "anonymised_client_description": ctx.config["anonymised_name"],
        "vendor": ctx.config["vendor"],
        "evidence": ev, "metrics": metrics,
        "do_not_claim": ctx.config.get("do_not_claim", []),
        "do_not_use": ctx.config.get("do_not_use", []),
        "replacements": [{"detail": i["term"], "write_instead": i["replacement"]} for i in ctx.config["identifiers"]],
        "combination_risks": ctx.config.get("combination_risks", []),
    }, ensure_ascii=False)


def run(ctx: RunContext) -> dict:
    drafts = {}
    if ctx.use_llm:
        b = brief(ctx)
        for aud in AUDIENCES:
            drafts[aud] = llm.call("writer", f"AUDIENCE: {aud}\n\nBRIEF (JSON):\n{b}")
            (ctx.project_dir / "drafts" / f"{aud}.llm.md").write_text(drafts[aud], encoding="utf-8")
        ctx.note("writer", "Claude drafted 4 versions")
    else:
        for aud in AUDIENCES:
            drafts[aud] = (ctx.project_dir / "drafts" / f"{aud}.md").read_text(encoding="utf-8")
        ctx.note("writer", f"loaded {len(drafts)} reviewed drafts")
    ctx.drafts = drafts
    return drafts
