"""Agent 2 - Extractor. Turns each library file into evidence items, each with a verbatim quote.

With --llm the items come from Claude (prompts/extractor.md), file by file. Without it, the cached
extraction in projects/<name>/evidence.json is used. Either way, every item is re-checked here: the
cited file must exist and the quote must appear in it word for word. Anything else is refused."""
from __future__ import annotations

import json

from .. import llm
from ..core import Evidence, Ledger, RunContext, md_table


def extract_with_llm(ctx: RunContext) -> list[dict]:
    items = []
    for rel in ctx.library.text_files():
        body = ctx.library.text(rel)
        if len(body) > 60000:
            body = body[:60000]
            ctx.note("extractor", f"{rel} is long; first 60k chars sent, remainder flagged for manual read")
        out = llm.call_json("extractor", f"FILE: {rel}\n\n{body}")
        for i, it in enumerate(out):
            it.setdefault("id", f"{rel.split('/')[0][:2]}-{i:02d}")
            it["file"] = rel
            items.append(it)
    return items


def run(ctx: RunContext) -> Ledger:
    cache = ctx.project_dir / "evidence.json"
    if ctx.use_llm:
        raw = extract_with_llm(ctx)
        cache.with_name("evidence.llm.json").write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")
        ctx.note("extractor", f"Claude proposed {len(raw)} evidence items")
    else:
        raw = json.loads(cache.read_text(encoding="utf-8"))
        ctx.note("extractor", f"loaded {len(raw)} cached evidence items from {cache.name}")

    items = []
    for r in raw:
        e = Evidence(**{k: r.get(k, "") for k in ("id", "date", "kind", "summary", "file", "quote", "actor")},
                     tags=r.get("tags", []))
        if not ctx.library.exists(e.file):
            e.reason = "cited file does not exist in the library"
        elif not e.quote.strip():
            e.reason = "no verbatim quote given"
        elif not ctx.library.contains(e.file, e.quote):
            e.reason = "quote not found verbatim in the cited file"
        else:
            e.verified = True
            e.line = ctx.library.find_line(e.file, e.quote)
        items.append(e)

    ledger = Ledger(items)
    ctx.ledger = ledger
    ctx.write_json("work/evidence_ledger.json", [vars(e) for e in items])
    if ledger.refused:
        ctx.write("work/evidence_refused.md", "# Evidence refused by the traceability check\n\n" + md_table(
            ["ID", "File", "Quote", "Reason"], [[e.id, e.file, e.quote, e.reason] for e in ledger.refused]) + "\n")
    ctx.note("extractor", f"{len(ledger.items)} items traced to a file and line; {len(ledger.refused)} refused")
    return ledger
