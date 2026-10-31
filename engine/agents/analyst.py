"""Agent 4 - Analyst. Computes every number from the raw data with a small declarative metric language
(defined in the project config), and writes the results sheet with the working shown.

Supported ops: ratio_of_sums, sum, count, mean, weighted_mean, duplicate_count, expr.
Filters: equality, in, not_in, between (inclusive), contains, nonblank.
expr inputs may be other metrics or literal values that cite an evidence id - so even a number that
comes from an email (not a CSV) is traceable."""
from __future__ import annotations

import ast
import operator
import statistics

from ..core import RunContext, md_table

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
       ast.USub: operator.neg}


def safe_eval(expr: str, env: dict) -> float:
    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.Name):
            return env[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](ev(node.operand))
        raise ValueError(f"unsupported expression element: {ast.dump(node)}")
    return ev(ast.parse(expr, mode="eval"))


def match(row: dict, flt: dict) -> bool:
    for col, cond in flt.items():
        val = row.get(col, "")
        if isinstance(cond, dict):
            if "in" in cond and val not in cond["in"]:
                return False
            if "not_in" in cond and val in cond["not_in"]:
                return False
            if "between" in cond and not (cond["between"][0] <= val <= cond["between"][1]):
                return False
            if "contains" in cond and cond["contains"].lower() not in val.lower():
                return False
            if cond.get("nonblank") and not str(val).strip():
                return False
            if cond.get("blank") and str(val).strip():
                return False
        elif val != cond:
            return False
    return True


def num(v) -> float:
    return float(str(v).replace(",", ""))


def compute(spec: dict, rows: list[dict], done: dict, ledger) -> dict:
    op = spec["op"]
    rec = {"id": spec["id"], "name": spec.get("name", spec["id"]), "op": op, "unit": spec.get("unit", ""),
           "dataset": spec.get("dataset", ""), "filter": spec.get("filter", {}), "note": spec.get("note", "")}
    if op == "expr":
        env, shown = {}, []
        for name, src in spec["inputs"].items():
            if isinstance(src, str):
                env[name] = done[src]["value"]
                shown.append(f"{name} = {src} = {env[name]:.4g}")
            else:
                ev = ledger.get(src["evidence"])
                if ev is None:
                    raise ValueError(f"{spec['id']}: input {name} cites evidence {src['evidence']} which is not verified")
                env[name] = src["value"]
                shown.append(f"{name} = {src['value']} (from {ev.id}, `{ev.ref}`)")
        rec["value"] = safe_eval(spec["expr"], env)
        rec["working"] = "; ".join(shown) + f" -> {spec['expr']} = {rec['value']:.4g}"
        rec["rows_used"] = 0
        return rec

    sel = [r for r in rows if match(r, spec.get("filter", {}))]
    rec["rows_used"] = len(sel)
    if not sel and op not in ("count", "duplicate_count"):
        raise ValueError(f"{spec['id']}: filter selected no rows")
    scale = spec.get("scale", 1)
    if op == "ratio_of_sums":
        n = sum(num(r[spec["numerator"]]) for r in sel)
        d = sum(num(r[spec["denominator"]]) for r in sel)
        rec["value"] = scale * n / d
        rec["working"] = f"sum({spec['numerator']}) = {n:,.0f}; sum({spec['denominator']}) = {d:,.0f}; {scale} x {n:,.0f} / {d:,.0f} = {rec['value']:.4f}"
    elif op == "sum":
        rec["value"] = sum(num(r[spec["column"]]) for r in sel)
        rec["working"] = f"sum({spec['column']}) over {len(sel)} rows = {rec['value']:,.4g}"
    elif op == "count":
        rec["value"] = len(sel)
        rec["working"] = f"rows matching filter = {len(sel)}"
    elif op == "mean":
        vals = [num(r[spec["column"]]) for r in sel if str(r[spec["column"]]).strip()]
        rec["value"] = statistics.mean(vals)
        rec["working"] = f"mean({spec['column']}) over {len(vals)} non-blank rows = {sum(vals):,.1f} / {len(vals)} = {rec['value']:.4f}"
    elif op == "weighted_mean":
        w = [num(r[spec["weight"]]) for r in sel]
        v = [num(r[spec["column"]]) for r in sel]
        rec["value"] = sum(a * b for a, b in zip(v, w)) / sum(w)
        rec["working"] = f"sum({spec['column']} x {spec['weight']}) / sum({spec['weight']}) = {sum(a * b for a, b in zip(v, w)):,.1f} / {sum(w):,.0f} = {rec['value']:.4f}"
    elif op == "duplicate_count":
        vals = [r[spec["column"]] for r in sel if r[spec["column"]].strip()]
        rec["value"] = len(vals) - len(set(vals))
        rec["working"] = f"{len(vals)} non-blank values, {len(set(vals))} distinct -> {rec['value']} repeats"
    else:
        raise ValueError(f"unknown op {op}")
    return rec


def fmt(rec: dict) -> str:
    d = rec.get("decimals", 1)
    return f"{rec['value']:.{d}f}{rec.get('unit', '')}"


def series(ctx: RunContext, spec: dict) -> list[tuple[str, float]]:
    """Grouped ratio series for charts, e.g. weekly compliance per cohort."""
    rows = ctx.library.csv_rows(ctx.config["datasets"][spec["dataset"]])
    sel = [r for r in rows if match(r, spec.get("filter", {}))]
    groups: dict[str, list] = {}
    for r in sel:
        groups.setdefault(r[spec["group_by"]], []).append(r)
    out = []
    for k in sorted(groups):
        g = groups[k]
        if spec["op"] == "ratio_of_sums":
            d = sum(num(r[spec["denominator"]]) for r in g)
            out.append((k, spec.get("scale", 1) * sum(num(r[spec["numerator"]]) for r in g) / d))
        elif spec["op"] == "value":
            v = g[0][spec["column"]]
            out.append((k, num(v) if str(v).strip() else float("nan")))
    return out


def run(ctx: RunContext) -> dict:
    cfg = ctx.config
    cache: dict[str, list] = {}
    done: dict[str, dict] = {}
    for spec in cfg["metrics"]:
        rows = []
        if spec["op"] != "expr":
            path = cfg["datasets"][spec["dataset"]]
            rows = cache.setdefault(path, ctx.library.csv_rows(path))
        rec = compute(spec, rows, done, ctx.ledger)
        rec["decimals"] = spec.get("decimals", 1)
        rec["source"] = cfg["datasets"].get(spec.get("dataset", ""), "evidence ledger")
        done[spec["id"]] = rec
    ctx.metrics = done

    out = ["# Results sheet", "",
           "Every number below is recomputed from the raw exports in `07_data` (or from a cited line where no raw data exists). "
           "The working column shows the calculation. Where sources disagree, the table says which one was used and why.", ""]
    for res in cfg["results"]:
        out += [f"## {res['id']} - {res['name']}", ""]
        rows = [["Definition", res["definition"]],
                ["Baseline", f"{fmt(done[res['baseline']])} ({res['baseline_window']})" if res.get("baseline") else res.get("baseline_text", "n/a")],
                ["Measurement window", res["window"]],
                ["Method", res["method"]],
                ["Final number", "; ".join(f"**{fmt(done[m])}** {lbl}" for m, lbl in res["finals"])],
                ["Target", res.get("target", "-")],
                ["Status", res.get("status", "-")],
                ["What else contributed", res.get("contributors", "-")],
                ["Honest worth", res.get("worth", "-")]]
        out += [md_table(["Field", "Value"], rows), ""]
        if res.get("disagreements"):
            out += ["**Where sources disagree**", "",
                    md_table(["Source says", "Where", "Used?", "Why"],
                             [[d["claim"], d["where"], d["used"], d["why"]] for d in res["disagreements"]]), ""]
        ids = [res.get("baseline")] + [m for m, _ in res["finals"]] + res.get("extra_metrics", [])
        out += ["**Working**", "", md_table(["Metric", "Value", "Rows", "Calculation", "Source"],
                                           [[done[i]["id"], fmt(done[i]), done[i]["rows_used"], done[i]["working"], f"`{done[i]['source']}`"]
                                            for i in ids if i]), ""]
    out += ["## All computed metrics", "", md_table(["ID", "Name", "Value", "Filter", "Calculation"],
            [[r["id"], r["name"], fmt(r), str(r["filter"]) if r["filter"] else "-", r["working"]] for r in done.values()]), ""]
    ctx.write("02_results_sheet.md", "\n".join(out))
    ctx.write_json("work/metrics.json", done)
    ctx.note("analyst", f"computed {len(done)} metrics; {len(cfg['results'])} results written with working")
    return done
