"""Case Study Engine - command line.

  python run_engine.py run  --project projects/drishti --library library/Project_Drishti_Library [--llm]
  python run_engine.py gate --project projects/drishti
  python run_engine.py publish --project projects/drishti     (refuses unless the gate says RELEASED)

The chain: librarian -> extractor -> historian -> analyst -> exposure -> writer -> factcheck -> media -> approval -> STOP.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from engine import llm
from engine.agents import analyst, approval, exposure, extractor, factcheck, historian, librarian, media, writer
from engine.core import Library, RunContext
from engine.gate import GateError, assert_releasable, evaluate

CHAIN = [("librarian", librarian), ("extractor", extractor), ("historian", historian), ("analyst", analyst),
         ("exposure", exposure), ("writer", writer), ("factcheck", factcheck), ("media", media), ("approval", approval)]


def load(project: str):
    pdir = Path(project).resolve()
    cfg = json.loads((pdir / "project.json").read_text(encoding="utf-8"))
    return pdir, cfg


def cmd_run(a) -> int:
    pdir, cfg = load(a.project)
    out = Path(a.out or pdir / "outputs").resolve()
    use_llm = a.llm
    if use_llm and not llm.available():
        print("--llm requested but the anthropic package or API key is missing; running from the cached extraction and drafts.")
        use_llm = False
    ctx = RunContext(library=Library(a.library or pdir / cfg["library"]), project_dir=pdir, out_dir=out, config=cfg, use_llm=use_llm)
    out.mkdir(parents=True, exist_ok=True)
    ctx.note("engine", f"project {cfg['project_label']} | library {ctx.library.root.name} | mode {'claude' if use_llm else 'offline'}")
    for name, mod in CHAIN:
        mod.run(ctx)
    ctx.write("work/run_log.txt", "\n".join(ctx.log) + "\n")
    print(f"\nSTOPPED for human approval. Outputs in {out}. Status: AWAITING_INTERNAL_REVIEW")
    return 0


def cmd_gate(a) -> int:
    pdir, cfg = load(a.project)
    out = Path(a.out or pdir / "outputs").resolve()
    try:
        s = evaluate(out, Path(a.approvals or pdir.parent.parent / "approvals").resolve(), cfg)
    except GateError as e:
        print(f"GATE ERROR: {e}")
        return 2
    print(json.dumps({k: v for k, v in s.items() if k != "history"}, indent=2))
    return 0


def cmd_publish(a) -> int:
    pdir, _ = load(a.project)
    try:
        s = assert_releasable(Path(a.out or pdir / "outputs").resolve())
    except GateError as e:
        print(str(e))
        return 3
    print(f"Released under option '{s['option']}'. Allowed: {s['allowed']}. A person now publishes; the engine does not.")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("run", "gate", "publish"):
        s = sub.add_parser(name)
        s.add_argument("--project", required=True)
        s.add_argument("--out")
        if name == "run":
            s.add_argument("--library")
            s.add_argument("--llm", action="store_true", help="use Claude for extraction and drafting")
        if name == "gate":
            s.add_argument("--approvals")
    a = p.parse_args()
    return {"run": cmd_run, "gate": cmd_gate, "publish": cmd_publish}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
