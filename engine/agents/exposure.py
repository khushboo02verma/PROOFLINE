"""Agent 5 - Exposure officer. Finds every detail that could identify the client, alone or in
combination, maps it to the contract rule, and gives the safe replacement.

Two detectors: (1) generic patterns that work on any library (emails, phones, IPs, URLs, tax IDs,
PO-style numbers, money, stream URLs); (2) the project's identifier list (names, places, code names)
from the config. It also supplies leak_scan(), which the fact-checker and media agents use on
anything about to leave the building."""
from __future__ import annotations

import re

from ..core import RunContext, md_table

PATTERNS = {
    "email address": (r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", "Remove"),
    "phone number": (r"\+?\d{2}[\s-]?\d{2}[X\d]{3}[\s-]?\d{5}", "Remove"),
    "IP address": (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "Remove; describe as 'inside the plant network'"),
    "URL": (r"(?:https?|rtsp|sap-pi)://\S+|github\.com/\S+", "Remove"),
    "tax ID (GSTIN)": (r"\b\d{2}[A-Z]{5}[X\d]{4,5}[A-Z\d]{3}\b", "Remove"),
    "PO / document number": (r"\b45\d{8}\b|\b[A-Z]{2,5}[/-][A-Z]{2,5}[/-][\w/-]*20\d\d[\w/-]*", "Remove; say 'purchase order'"),
    "exact rupee amount": (r"₹\s?[\d,.]+\s?(?:L|lakh|Cr|crore)?|\b\d+(?:\.\d+)?\s?(?:lakh|crore)\b", "Use a band or a percentage"),
}


def leak_scan(text: str, ctx: RunContext, allow: tuple = ()) -> list[dict]:
    """Return every identifier or pattern hit in `text`. Used as a hard gate on outbound content."""
    hits = []
    for ident in ctx.config["identifiers"]:
        for term in [ident["term"]] + ident.get("aliases", []):
            if term in allow:
                continue
            flags = 0 if ident.get("case_sensitive") else re.I
            if re.search(r"(?<![\w])" + re.escape(term) + r"(?![\w])", text, flags):
                hits.append({"term": term, "category": ident["category"], "rule": ident["rule"]})
    for name, (pat, _) in PATTERNS.items():
        if name in ctx.config.get("outbound_allowed_patterns", []):
            continue
        for m in re.finditer(pat, text):
            if m.group(0) not in allow:
                hits.append({"term": m.group(0), "category": name, "rule": "generic pattern"})
    return hits


def run(ctx: RunContext) -> dict:
    lib, cfg = ctx.library, ctx.config
    found = []
    for ident in cfg["identifiers"]:
        files = {}
        for rel in lib.text_files():
            flags = 0 if ident.get("case_sensitive") else re.I
            n = sum(len(re.findall(r"(?<![\w])" + re.escape(t) + r"(?![\w])", lib.text(rel), flags))
                    for t in [ident["term"]] + ident.get("aliases", []))
            if n:
                files[rel] = n
        found.append({**ident, "files": files, "count": sum(files.values())})

    pattern_hits = []
    for name, (pat, repl) in PATTERNS.items():
        per_file = {}
        for rel in lib.text_files():
            ms = sorted(set(re.findall(pat, lib.text(rel))))
            if ms:
                per_file[rel] = ms
        if per_file:
            pattern_hits.append({"category": name, "replacement": repl, "files": per_file})

    index = {e["file"]: e for e in __import__("json").loads((ctx.out_dir / "work/library_index.json").read_text(encoding="utf-8"))}
    media_rows = []
    for m in cfg.get("media_review", []):
        meta = index.get(m["file"], {}).get("image_meta", {})
        hidden = {k: v for k, v in meta.items() if k not in ("size",)}
        media_rows.append([m["file"], m["visible"], "; ".join(f"{k}={v}" for k, v in hidden.items()) or "none",
                           m["decision"], m["rule"]])

    ctx.exposure = {"identifiers": found, "patterns": pattern_hits}
    out = ["# Exposure report", "",
           "Every detail that could identify the client, alone or in combination, with the safe replacement and the contract rule behind it. "
           f"Contract basis: {cfg['contract_basis']}.", "",
           "## 1. Direct identifiers", "",
           md_table(["Detail", "Category", "Occurrences", "Seen in", "Safe replacement", "Rule"],
                    [[f["term"] + (f" (+{', '.join(f['aliases'])})" if f.get("aliases") else ""), f["category"], f["count"],
                      ", ".join(f"`{k}`" for k in list(f["files"])[:4]) + (" ..." if len(f["files"]) > 4 else ""),
                      f["replacement"], f["rule"]] for f in found]), "",
           "## 2. Pattern detectors (generic, would run on any library)", "",
           md_table(["Pattern", "Examples found", "Files", "Safe replacement"],
                    [[p["category"], ", ".join(sorted({x for v in p["files"].values() for x in v})[:5]),
                      len(p["files"]), p["replacement"]] for p in pattern_hits]), "",
           "## 3. Combination risks (each safe alone, identifying together)", "",
           md_table(["Combination", "Why it identifies", "Decision", "Rule"],
                    [[c["combo"], c["why"], c["decision"], c["rule"]] for c in cfg.get("combination_risks", [])]), "",
           "## 4. Media", "",
           md_table(["File", "What is visible", "Hidden metadata found by the librarian", "Decision", "Rule"], media_rows), "",
           "## 5. Content the client asked us not to use", "",
           md_table(["Item", "Who asked", "Source"], [[d["item"], d["who"], f"`{d['source']}`"] for d in cfg.get("do_not_use", [])]), ""]
    ctx.write("03_exposure_report.md", "\n".join(out))
    ctx.note("exposure", f"{sum(1 for f in found if f['count'])} identifiers and {len(pattern_hits)} pattern types found; "
                         f"{len(cfg.get('combination_risks', []))} combination risks; {len(media_rows)} media files reviewed")
    return ctx.exposure
