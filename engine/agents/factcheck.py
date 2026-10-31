"""Agent 7 - Fact-checker. The engine's refusal mechanism.

A line survives only if: it cites sources (or is marked {framing} and carries no number); every cited
source exists and was verified; every number in it matches a number in the cited sources (to the
precision written); it makes no claim the project has ruled out (do_not_claim); and it leaks no
identifier. Refused lines are dropped and logged with the reason. Nothing is rewritten silently."""
from __future__ import annotations

import re

from ..core import RunContext, md_table
from .exposure import leak_scan

REF = re.compile(r"\[(E|M):([\w.-]+)\]")
FRAMING = "{framing}"
NUMBER = re.compile(r"(?<![\w.])[-−]?\d[\d,]*(?:\.\d+)?")


def numbers_in(text: str) -> list[str]:
    out = []
    for m in NUMBER.finditer(text):
        raw = m.group(0).replace("−", "-").rstrip(",")
        val = raw.replace(",", "")
        try:
            v = float(val)
        except ValueError:
            continue
        if raw.count(",") and not re.fullmatch(r"-?\d{1,3}(,\d{2,3})+(\.\d+)?", raw):
            continue
        if 1990 <= abs(v) <= 2100 and "." not in val:
            continue  # a year
        out.append(val)
    return out


def matches(n: str, candidates: list[float]) -> bool:
    d = len(n.split(".")[1]) if "." in n else 0
    target = abs(float(n))
    return any(abs(round(abs(c), d) - target) < 1e-9 or abs(abs(c) - target) < 1e-9 for c in candidates)


def candidates_for(refs, ctx: RunContext) -> tuple[list[float], list[str]]:
    vals, missing = [], []
    for kind, rid in refs:
        if kind == "E":
            e = ctx.ledger.get(rid)
            if e is None:
                missing.append(f"E:{rid}")
                continue
            vals += [float(x) for x in numbers_in(e.quote)]
        else:
            m = ctx.metrics.get(rid)
            if m is None:
                missing.append(f"M:{rid}")
                continue
            vals.append(m["value"])
    return vals, missing


def check_line(line: str, ctx: RunContext) -> tuple[bool, str, str]:
    """Return (kept, reason, clean_text)."""
    refs = REF.findall(line)
    framing = FRAMING in line
    clean = REF.sub("", line).replace(FRAMING, "").rstrip()
    clean = re.sub(r"\s+([.,;:])", r"\1", clean)
    nums = numbers_in(re.sub(r"^\s*(?:#+|[-*>]|\d+\.)\s+", "", clean))
    if not refs and not framing:
        return False, "no source cited", clean
    if framing and nums and not refs:
        return False, f"framing line contains numbers {nums} with no source", clean
    vals, missing = candidates_for(refs, ctx)
    if missing:
        return False, f"cites unknown or unverified source(s): {', '.join(missing)}", clean
    bad = [n for n in nums if not matches(n, vals)]
    if bad:
        return False, f"number(s) {', '.join(bad)} not found in cited sources", clean
    for rule in ctx.config.get("do_not_claim", []):
        if re.search(rule["pattern"], clean, re.I):
            return False, f"ruled-out claim: {rule['why']} ({rule['source']})", clean
    leaks = leak_scan(clean, ctx)
    if leaks:
        return False, "would expose the client: " + ", ".join(f"{h['term']} ({h['category']})" for h in leaks), clean
    return True, "", clean


def check_document(text: str, ctx: RunContext) -> tuple[str, str, list]:
    kept_clean, kept_traced, refused = [], [], []
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or re.fullmatch(r"\|?[\s:|-]+\|?", stripped) or stripped.startswith("<!--"):
            kept_clean.append(line)
            kept_traced.append(line)
            continue
        if stripped.startswith("#") and not numbers_in(stripped) and not REF.search(stripped):
            kept_clean.append(line)
            kept_traced.append(line)
            continue
        ok, reason, clean = check_line(line, ctx)
        if ok:
            kept_clean.append(clean)
            kept_traced.append(trace(line, ctx))
        else:
            refused.append({"line": i, "text": clean.strip(), "reason": reason})
    return "\n".join(kept_clean), "\n".join(kept_traced), refused


def trace(line: str, ctx: RunContext) -> str:
    def rep(m):
        kind, rid = m.group(1), m.group(2)
        if kind == "E":
            return f"<sup>[{rid} `{ctx.ledger.get(rid).ref}`]</sup>"
        return f"<sup>[{rid} `{ctx.metrics[rid]['source']}`]</sup>"
    return REF.sub(rep, line).replace(FRAMING, "<sup>[framing]</sup>")


def run(ctx: RunContext) -> dict:
    results, all_refused = {}, []
    for aud, text in ctx.drafts.items():
        clean, traced, refused = check_document(text, ctx)
        results[aud] = {"clean": clean, "traced": traced, "refused": refused}
        all_refused += [{**r, "draft": aud} for r in refused]
    ctx.verified = results

    titles = {"gatekeeper": "Version A - for the gatekeeper (procurement, IT security, legal)",
              "user": "Version B - for the user (plant and shift teams)",
              "buyer": "Version C - for the buyer (the person who signs)",
              "champion": "Forwardable note - for the champion inside the client"}
    body = [f"# Case study - {ctx.config['anonymised_title']}", "",
            "> STATUS: DRAFT - NOT APPROVED FOR USE. Anonymised under MSA clause 15.2. Requires written approval from the client's "
            "Corporate Communications with Legal in copy before first use (see 06_approval).", ""]
    traced = list(body)
    for aud in ctx.drafts:
        body += ["---", "", f"## {titles.get(aud, aud)}", "", results[aud]["clean"], ""]
        traced += ["---", "", f"## {titles.get(aud, aud)}", "", results[aud]["traced"], ""]
    ctx.write("04_case_study.md", "\n".join(body))
    ctx.write("work/04_case_study_traced.md", "\n".join(traced))
    ctx.write("work/04_refusals.md", "# Lines refused by the fact-checker\n\n" + (
        md_table(["Draft", "Line", "Text", "Reason"], [[r["draft"], r["line"], r["text"], r["reason"]] for r in all_refused])
        if all_refused else "None - every line traced to a verified source.") + "\n")
    ctx.note("factcheck", f"{sum(len(r['clean'].splitlines()) for r in results.values())} lines kept; {len(all_refused)} refused")
    return results
