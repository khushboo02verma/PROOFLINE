"""Shared plumbing for the case-study engine: library access, evidence ledger, run log.

Nothing in this module knows about any particular project. Project-specific facts live in
projects/<name>/ (config, extracted evidence, drafts) and are checked against the library at run time.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

TEXT_SUFFIXES = {".md", ".txt", ".csv", ".yaml", ".yml", ".json"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff"}


def norm(text: str) -> str:
    """Normalise text for quote matching: unicode NFKC, unify dashes/quotes, collapse whitespace, strip markdown emphasis."""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u2212", "-").replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("**", "").replace("> ", " ")
    return re.sub(r"\s+", " ", text).strip().lower()


class Library:
    """Read-only view of one project library folder."""

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        if not self.root.is_dir():
            raise FileNotFoundError(f"Library folder not found: {self.root}")
        self.files = sorted(p for p in self.root.rglob("*") if p.is_file())
        self._text: dict[str, str] = {}
        self.data_issues: list[str] = []

    def rel(self, p: Path) -> str:
        return p.relative_to(self.root).as_posix()

    def text(self, rel_path: str) -> str:
        if rel_path not in self._text:
            self._text[rel_path] = (self.root / rel_path).read_text(encoding="utf-8", errors="replace")
        return self._text[rel_path]

    def exists(self, rel_path: str) -> bool:
        return (self.root / rel_path).is_file()

    def csv_rows(self, rel_path: str, merge_overflow_into: str | None = None) -> list[dict]:
        """Rows as dicts. A row with more cells than the header (an unquoted comma in a text field) is
        repaired by re-joining the extra cells into `merge_overflow_into`, or skipped; either way it is
        recorded in self.data_issues."""
        with open(self.root / rel_path, encoding="utf-8", newline="") as fh:
            reader = csv.reader(fh)
            header = next(reader)
            rows = []
            for n, cells in enumerate(reader, start=2):
                extra = len(cells) - len(header)
                if extra > 0:
                    if merge_overflow_into in header:
                        i = header.index(merge_overflow_into)
                        cells = cells[:i] + [",".join(cells[i:i + extra + 1])] + cells[i + extra + 1:]
                        self.data_issues.append(f"{rel_path} line {n}: {extra} unquoted comma(s) in '{merge_overflow_into}', repaired")
                    else:
                        self.data_issues.append(f"{rel_path} line {n}: {len(cells)} cells for {len(header)} columns, row skipped")
                        continue
                rows.append(dict(zip(header, cells + [""] * (len(header) - len(cells)))))
            return rows

    def text_files(self) -> list[str]:
        return [self.rel(p) for p in self.files if p.suffix.lower() in TEXT_SUFFIXES]

    def image_files(self) -> list[str]:
        return [self.rel(p) for p in self.files if p.suffix.lower() in IMAGE_SUFFIXES]

    def find_line(self, rel_path: str, quote: str) -> int | None:
        """1-based line where the quote starts, or None if the quote is not in the file."""
        target = norm(quote)
        lines = self.text(rel_path).splitlines()
        span = 12
        for i in range(len(lines)):
            here = target in norm(" ".join(lines[i:i + span]))
            later = target in norm(" ".join(lines[i + 1:i + 1 + span]))
            if here and not later:
                return i + 1
        return None

    def contains(self, rel_path: str, quote: str) -> bool:
        return norm(quote) in norm(self.text(rel_path))


@dataclass
class Evidence:
    id: str
    date: str
    kind: str          # event | decision | quote | fact | risk | number
    summary: str       # our paraphrase, never used as a source of numbers
    file: str
    quote: str         # must be a verbatim substring of `file`
    actor: str = ""
    tags: list = field(default_factory=list)
    line: int | None = None
    verified: bool = False
    reason: str = ""

    @property
    def ref(self) -> str:
        return f"{self.file}:{self.line}" if self.line else self.file


class Ledger:
    """Evidence items that passed the traceability check, plus the ones that were refused."""

    def __init__(self, items: list[Evidence]):
        self.items = {e.id: e for e in items if e.verified}
        self.refused = [e for e in items if not e.verified]

    def get(self, eid: str) -> Evidence | None:
        return self.items.get(eid)


@dataclass
class RunContext:
    library: Library
    project_dir: Path
    out_dir: Path
    config: dict
    use_llm: bool = False
    log: list = field(default_factory=list)
    ledger: Ledger | None = None
    metrics: dict = field(default_factory=dict)
    exposure: dict = field(default_factory=dict)
    drafts: dict = field(default_factory=dict)
    verified: dict = field(default_factory=dict)
    media: list = field(default_factory=list)

    def note(self, agent: str, message: str) -> None:
        stamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{stamp}] {agent}: {message}"
        self.log.append(line)
        print(line)

    def write(self, rel: str, content: str) -> Path:
        path = self.out_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def write_json(self, rel: str, data) -> Path:
        return self.write(rel, json.dumps(data, indent=2, ensure_ascii=False, default=str))


def sha256_of(paths: list[Path]) -> str:
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def md_table(headers: list[str], rows: list[list]) -> str:
    def cell(v):
        return str(v).replace("|", "\\|").replace("\n", " ")
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    out += ["| " + " | ".join(cell(v) for v in r) + " |" for r in rows]
    return "\n".join(out)
