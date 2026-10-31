"""Local web demo for the Case Study Engine (standard library only).

  python webapp.py            then open http://localhost:8765

Run the chain, browse the six outputs, try to sneak a claim past the fact-checker, and walk the
approval gate - all from the browser. Nothing here sends anything anywhere; it listens on localhost only.
"""
from __future__ import annotations

import json
import mimetypes
import sys
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from engine.agents import analyst, approval, exposure, extractor, factcheck, historian, librarian, media, writer
from engine.agents.factcheck import check_line
from engine.core import Library, RunContext
from engine.gate import GateError, assert_releasable, evaluate

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / "projects/drishti"
OUT = PROJECT / "outputs"
APPROVALS = ROOT / "approvals"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
CHAIN = [("Librarian", librarian), ("Extractor", extractor), ("Historian", historian), ("Analyst", analyst),
         ("Exposure officer", exposure), ("Writer", writer), ("Fact-checker", factcheck), ("Media", media),
         ("Approval clerk", approval)]

STATE = {"ctx": None, "lock": threading.Lock()}


def run_chain() -> dict:
    cfg = json.loads((PROJECT / "project.json").read_text(encoding="utf-8"))
    ctx = RunContext(library=Library(PROJECT / cfg["library"]), project_dir=PROJECT, out_dir=OUT, config=cfg)
    OUT.mkdir(parents=True, exist_ok=True)
    steps = []
    for name, mod in CHAIN:
        before = len(ctx.log)
        mod.run(ctx)
        steps.append({"agent": name, "log": [l.split(": ", 1)[-1] for l in ctx.log[before:]]})
    ctx.write("work/run_log.txt", "\n".join(ctx.log) + "\n")
    STATE["ctx"] = ctx
    return {"steps": steps, "summary": summary(ctx)}


def summary(ctx: RunContext) -> dict:
    m = ctx.metrics
    pick = lambda k: round(m[k]["value"], m[k]["decimals"])
    return {
        "files": len(ctx.library.files),
        "evidence": len(ctx.ledger.items), "evidence_refused": len(ctx.ledger.refused),
        "metrics": len(m),
        "lines_kept": sum(len([l for l in v["clean"].splitlines() if l.strip()]) for v in ctx.verified.values()),
        "lines_refused": sum(len(v["refused"]) for v in ctx.verified.values()),
        "media": len(ctx.media),
        "kpis": [
            {"label": "PPE compliance (pilot)", "value": f"{pick('K1_base')}% → {pick('K1_result')}%", "note": "target ≥ 90% · MET"},
            {"label": "Zone breaches /1,000 cam-h", "value": f"{pick('K2_base')} → {pick('K2_result')}", "note": f"{pick('K2_change_pct')}% vs −50% · missed, then {pick('K2_post_change')}% after guards"},
            {"label": "Alert acknowledgement", "value": f"{pick('K3_result')} min", "note": f"target ≤ 3 · missed, then {pick('K3_post_pilot')} min after phone rule"},
            {"label": "False alarms", "value": f"{pick('K4_base')}% → {pick('K4_result')}%", "note": "target < 10% · MET"},
            {"label": "Truck turnaround (like-for-like)", "value": f"{pick('gate_like_for_like')}%", "note": "credit shared with client's gate changes"},
        ],
    }


def ctx() -> RunContext:
    with STATE["lock"]:
        if STATE["ctx"] is None:
            run_chain()
        return STATE["ctx"]


def status() -> dict:
    p = OUT / "RELEASE_STATUS.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"status": "NOT RUN"}


def approve(kind: str) -> dict:
    APPROVALS.mkdir(exist_ok=True)
    sha = status().get("pack_sha256")
    docs = {
        "internal": ("internal_review.json", {"reviewer": "Head of Delivery (demo)", "reviewer_role": "Head of Delivery", "decision": "approve"}),
        "author_self": ("internal_review.json", {"reviewer": "engine operator", "reviewer_role": "Sales", "decision": "approve"}),
        "plant_only": ("client_decision.json", {"signatory": "Unit Head", "department": "Plant", "legal_in_copy": False, "decision": "approve", "option": "A"}),
        "client": ("client_decision.json", {"signatory": "Head of Corporate Communications", "department": "Corporate Communications", "legal_in_copy": True, "decision": "approve", "option": "A"}),
        "withdraw": ("client_decision.json", {"signatory": "Head of Corporate Communications", "department": "Corporate Communications", "legal_in_copy": True, "decision": "withdrawn", "comments": "Leadership changed its mind"}),
    }
    name, doc = docs[kind]
    (APPROVALS / name).write_text(json.dumps({**doc, "pack_sha256": sha}, indent=2), encoding="utf-8")
    return evaluate(OUT, APPROVALS, ctx().config)


def reset() -> dict:
    for f in APPROVALS.glob("*.json"):
        f.unlink()
    with STATE["lock"]:
        return run_chain()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code: int, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else (json.dumps(body, ensure_ascii=False) if ctype == "application/json" else body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + ("; charset=utf-8" if ctype.startswith(("text", "application/json")) else ""))
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        try:
            if url.path == "/":
                return self.send(200, PAGE, "text/html")
            if url.path == "/api/state":
                c = STATE["ctx"]
                return self.send(200, {"status": status(), "summary": summary(c) if c else None})
            if url.path == "/out":
                rel = parse_qs(url.query).get("p", [""])[0]
                target = (OUT / rel).resolve()
                if OUT.resolve() not in target.parents or not target.is_file():
                    return self.send(404, {"error": "not found"})
                ctype = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
                if target.suffix == ".md":
                    ctype = "text/plain"
                return self.send(200, target.read_bytes(), ctype)
            return self.send(404, {"error": "not found"})
        except Exception as e:  # keep the demo alive
            traceback.print_exc()
            return self.send(500, {"error": str(e)})

    def do_POST(self):
        url = urlparse(self.path)
        n = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(n) or b"{}")
        try:
            if url.path == "/api/run":
                with STATE["lock"]:
                    res = run_chain()
                return self.send(200, {**res, "status": status()})
            if url.path == "/api/check":
                ok, reason, clean = check_line(body.get("line", ""), ctx())
                return self.send(200, {"ok": ok, "reason": reason, "clean": clean})
            if url.path == "/api/approve":
                return self.send(200, {"status": approve(body["kind"])})
            if url.path == "/api/publish":
                try:
                    s = assert_releasable(OUT)
                    return self.send(200, {"ok": True, "message": f"Released under option '{s['option']}'. Allowed: {s['allowed']}"})
                except GateError as e:
                    return self.send(200, {"ok": False, "message": str(e)})
            if url.path == "/api/tamper":
                p = OUT / "04_case_study.md"
                p.write_text(p.read_text(encoding="utf-8") + "\nPPE compliance hit 97% and zero accidents.\n", encoding="utf-8")
                try:
                    evaluate(OUT, APPROVALS, ctx().config)
                    return self.send(200, {"ok": True, "message": "not detected"})
                except GateError as e:
                    return self.send(200, {"ok": False, "message": f"{e} (case study edited after approval - run Reset)"})
            if url.path == "/api/reset":
                res = reset()
                return self.send(200, {**res, "status": status()})
            return self.send(404, {"error": "not found"})
        except GateError as e:
            return self.send(200, {"status": {"status": "GATE ERROR", "reason": str(e)}})
        except Exception as e:
            traceback.print_exc()
            return self.send(500, {"error": str(e)})


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Case Study Engine</title>
<style>
:root{--bg:#f6f7f9;--card:#fff;--ink:#1f2933;--muted:#6b7280;--line:#e5e7eb;--accent:#1d6fb8;--ok:#15803d;--okbg:#ecfdf3;--bad:#b91c1c;--badbg:#fef2f2;--warn:#b45309;--warnbg:#fffbeb}
:root{color-scheme:light}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}
header{padding:20px 24px;border-bottom:1px solid var(--line);background:var(--card);display:flex;gap:16px;align-items:center;flex-wrap:wrap}
header h1{font-size:20px;margin:0}header p{margin:0;color:var(--muted);font-size:13px}
.badge{margin-left:auto;padding:6px 12px;border-radius:999px;font-weight:600;font-size:13px;background:var(--warnbg);color:var(--warn)}
.badge.RELEASED{background:var(--okbg);color:var(--ok)}.badge.WITHDRAWN,.badge.REJECTED{background:var(--badbg);color:var(--bad)}
main{max-width:1240px;margin:0 auto;padding:20px 16px;display:grid;gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
h2{font-size:15px;margin:0 0 10px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
button{font:inherit;border:1px solid var(--line);background:var(--card);color:var(--ink);padding:8px 14px;border-radius:8px;cursor:pointer}
button:hover{border-color:var(--accent)}button.primary{background:var(--accent);color:#fff;border-color:var(--accent);font-weight:600}
button:disabled{opacity:.5;cursor:wait}
.chain{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0}
.agent{padding:8px 10px;border:1px solid var(--line);border-radius:8px;font-size:13px;min-width:110px;transition:.3s}
.agent.done{border-color:var(--ok);background:var(--okbg)}.agent.stop{border-color:var(--warn);background:var(--warnbg)}
.agent small{display:block;color:var(--muted);font-size:11px;line-height:1.3;margin-top:2px}
.arrow{color:var(--muted)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}
.stat{border:1px solid var(--line);border-radius:10px;padding:10px}.stat b{display:block;font-size:24px}.stat span{color:var(--muted);font-size:12px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;margin-top:10px}
.kpi{border-left:3px solid var(--accent);padding:6px 10px}.kpi b{font-size:20px;display:block}.kpi span{font-size:12px;color:var(--muted)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media(max-width:860px){.two{grid-template-columns:1fr}}
input[type=text]{width:100%;font:inherit;padding:10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}.chips button{font-size:12px;padding:4px 8px}
.verdict{margin-top:10px;padding:10px;border-radius:8px;display:none}.verdict.ok{display:block;background:var(--okbg);color:var(--ok)}.verdict.bad{display:block;background:var(--badbg);color:var(--bad)}
.gate{display:flex;flex-wrap:wrap;gap:8px}.hist{font-size:13px;margin-top:10px;max-height:180px;overflow:auto}
.hist div{padding:4px 0;border-bottom:1px solid var(--line)}
.tabs{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}.tabs button.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.doc{max-height:640px;overflow:auto;padding-right:6px}
.doc table{border-collapse:collapse;width:100%;font-size:13px;margin:8px 0}.doc th,.doc td{border:1px solid var(--line);padding:5px 7px;vertical-align:top;text-align:left}
.doc th{background:var(--bg)}.doc h1{font-size:22px}.doc h2{font-size:17px;text-transform:none;letter-spacing:0;color:var(--ink);margin-top:18px}.doc h3,.doc h4{font-size:15px}
.doc blockquote{margin:8px 0;padding:8px 12px;border-left:3px solid var(--warn);background:var(--warnbg)}
.doc sup{color:var(--accent);font-size:10px}.doc code{font-size:12px;background:var(--bg);padding:1px 4px;border-radius:4px}
.media{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px}.media img{width:100%;border:1px solid var(--line);border-radius:8px;background:#fff}
.media a{color:var(--accent)}.muted{color:var(--muted);font-size:13px}
</style></head><body>
<header><div><h1>Case Study Engine</h1><p>Project library → traceable, client-approvable case study · no line leaves without a file behind it</p></div>
<span id="badge" class="badge">NOT RUN</span></header>
<main>
<section class="card"><h2>1 · Run the chain</h2>
<button id="run" class="primary">▶ Run engine on the library</button> <span id="runmsg" class="muted"></span>
<div class="chain" id="chain"></div>
<div class="stats" id="stats"></div><div class="kpis" id="kpis"></div></section>

<div class="two">
<section class="card"><h2>2 · Try to sneak a claim past it</h2>
<p class="muted">Type a case-study line. Cite sources as [E:id] (evidence) or [M:id] (metric). The fact-checker decides.</p>
<input type="text" id="claim" placeholder="e.g. PPE compliance rose from 74% to 97% [M:K1_result]">
<div class="chips" id="chips"></div><button id="check" class="primary">Check this line</button>
<div id="verdict" class="verdict"></div></section>

<section class="card"><h2>3 · Stop for a person</h2>
<p class="muted">The pack is frozen by hash. Two approvals, in order. Try the wrong ones first.</p>
<div class="gate">
<button data-a="publish">Publish</button>
<button data-a="author_self">Author approves own work</button>
<button data-a="internal">Head of Delivery approves</button>
<button data-a="plant_only">Plant head says yes (WhatsApp)</button>
<button data-a="client">Corporate Comms + Legal approve</button>
<button data-a="tamper">Edit text after approval</button>
<button data-a="withdraw">Client withdraws</button>
<button data-a="reset">Reset</button></div>
<div id="gatemsg" class="verdict"></div><div class="hist" id="hist"></div></section>
</div>

<section class="card"><h2>4 · The six outputs</h2>
<div class="tabs" id="tabs"></div><div class="doc" id="doc"><p class="muted">Run the engine first.</p></div></section>
</main>
<script>
const AGENTS=[["Librarian","indexes files, reads hidden metadata"],["Extractor","evidence with verbatim quotes"],["Historian","dated story spine"],["Analyst","recomputes every number"],["Exposure officer","what could identify the client"],["Writer","3 readers + champion"],["Fact-checker","refuses untraceable lines"],["Media","charts, diagram, slide"],["Approval clerk","request + sheet, then STOP"]];
const TABS=[["Case study","04_case_study.md"],["Traced (with sources)","work/04_case_study_traced.md"],["Results sheet","02_results_sheet.md"],["Story spine","01_story_spine.md"],["Exposure report","03_exposure_report.md"],["Approval sheet","06_approval/approval_sheet.md"],["Approval email","06_approval/approval_request_email.md"],["Media pack","media"],["Refusals","work/04_refusals.md"]];
const CHIPS=["PPE compliance rose from 74% to 97% [M:K1_result]","We achieved zero LTIs since go-live [E:e47]","The project saved Rs 2.3 crore a year.","Ardent's plant reached 91% compliance [M:K1_result]","Cameras now cover all 146 locations [E:e44b]","Zone breaches were halved in the pilot [M:K2_change_pct]","PPE compliance rose from 69% to 91% in the pilot [M:K1_base] [M:K1_result]","Truck turnaround fell 24% on like-for-like data [M:gate_like_for_like]"];
const $=s=>document.querySelector(s);
const esc=s=>s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
function inline(s){return esc(s).replace(/&lt;sup&gt;(.*?)&lt;\/sup&gt;/g,"<sup>$1</sup>").replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").replace(/`([^`]+)`/g,"<code>$1</code>")}
function md(t){const L=t.split(/\r?\n/);let h="",i=0;while(i<L.length){let l=L[i];
 if(/^\s*\|/.test(l)){const rows=[];while(i<L.length&&/^\s*\|/.test(L[i]))rows.push(L[i++]);const cells=r=>r.trim().replace(/^\||\|$/g,"").split(/(?<!\\)\|/).map(c=>inline(c.trim().replace(/\\\|/g,"|")));
  h+="<table><tr>"+cells(rows[0]).map(c=>"<th>"+c+"</th>").join("")+"</tr>";rows.slice(2).forEach(r=>h+="<tr>"+cells(r).map(c=>"<td>"+c+"</td>").join("")+"</tr>");h+="</table>";continue}
 let m=l.match(/^(#{1,4})\s+(.*)/);if(m){h+=`<h${m[1].length}>${inline(m[2])}</h${m[1].length}>`;i++;continue}
 if(/^>\s?/.test(l)){h+="<blockquote>"+inline(l.replace(/^>\s?/,""))+"</blockquote>";i++;continue}
 if(/^\s*[-*]\s+/.test(l)){h+="<ul>";while(i<L.length&&/^\s*[-*]\s+/.test(L[i]))h+="<li>"+inline(L[i++].replace(/^\s*[-*]\s+/,""))+"</li>";h+="</ul>";continue}
 if(/^---+$/.test(l.trim())){h+="<hr>";i++;continue}
 if(!l.trim()){i++;continue}
 const p=[];while(i<L.length&&L[i].trim()&&!/^(#|\||>|\s*[-*]\s|---)/.test(L[i]))p.push(L[i++]);h+="<p>"+p.map(inline).join("<br>")+"</p>"}return h}
async function api(path,body){const r=await fetch(path,body===undefined?{}:{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});return r.json()}
function drawChain(done){$("#chain").innerHTML=AGENTS.map((a,i)=>`${i?'<span class="arrow">→</span>':''}<div class="agent ${i<done?(i==8?'stop':'done'):''}" id="ag${i}"><b>${a[0]}</b><small>${a[1]}</small></div>`).join("")+(done>=9?'<span class="arrow">→</span><div class="agent stop"><b>⏸ STOP</b><small>waits for a person</small></div>':'')}
function setStatus(s){const b=$("#badge");b.textContent=(s.status||"").replace(/_/g," ");b.className="badge "+s.status;const h=(s.history||[]).slice().reverse();$("#hist").innerHTML=h.map(x=>`<div><b>${x.status.replace(/_/g," ")}</b> — ${esc(x.reason||"")}</div>`).join("")}
function setSummary(s){if(!s)return;const st=[[s.files,"library files read"],[s.evidence,"evidence items traced to file:line"],[s.evidence_refused,"evidence refused"],[s.metrics,"metrics recomputed"],[s.lines_kept,"case-study lines verified"],[s.lines_refused,"lines refused"],[s.media,"media assets built"]];
 $("#stats").innerHTML=st.map(x=>`<div class="stat"><b>${x[0]}</b><span>${x[1]}</span></div>`).join("");$("#kpis").innerHTML=s.kpis.map(k=>`<div class="kpi"><span>${k.label}</span><b>${k.value}</b><span>${k.note}</span></div>`).join("")}
let cur=0;async function showTab(i){cur=i;document.querySelectorAll("#tabs button").forEach((b,j)=>b.classList.toggle("on",i==j));const t=TABS[i][1];
 if(t=="media"){$("#doc").innerHTML=`<div class="media">${["chart_compliance_cohorts.png","chart_gate_turnaround.png","architecture_generic.png"].map(f=>`<div><img src="/out?p=05_media/${f}&t=${Date.now()}"><div class="muted">${f}</div></div>`).join("")}</div><p>Also: <a href="/out?p=05_media/gate_payback_calculator.html" target="_blank">interactive payback calculator ↗</a> · <a href="/out?p=05_media/case_study_slide.pptx">sales slide (.pptx) ↓</a></p>`;return}
 const r=await fetch("/out?p="+encodeURIComponent(t));$("#doc").innerHTML=r.ok?md(await r.text()):'<p class="muted">Run the engine first.</p>'}
$("#tabs").innerHTML=TABS.map((t,i)=>`<button>${t[0]}</button>`).join("");document.querySelectorAll("#tabs button").forEach((b,i)=>b.onclick=()=>showTab(i));
$("#chips").innerHTML=CHIPS.map(c=>`<button>${esc(c)}</button>`).join("");document.querySelectorAll("#chips button").forEach((b,i)=>b.onclick=()=>{$("#claim").value=CHIPS[i];check()});
async function check(){const v=$("#verdict");v.className="verdict";const r=await api("/api/check",{line:$("#claim").value});v.className="verdict "+(r.ok?"ok":"bad");v.innerHTML=r.ok?"✔ ACCEPTED — every source verified, every number matches.":"✘ REFUSED — "+esc(r.reason)}
$("#check").onclick=check;$("#claim").onkeydown=e=>{if(e.key=="Enter")check()};
async function animateRun(path){const btn=$("#run");btn.disabled=true;$("#runmsg").textContent="running…";drawChain(0);
 const p=api(path,{});for(let i=1;i<=9;i++){await new Promise(r=>setTimeout(r,280));drawChain(i)}const r=await p;btn.disabled=false;
 if(r.error){$("#runmsg").textContent="error: "+r.error;return}
 r.steps.forEach((s,i)=>{const el=$("#ag"+i);if(el)el.title=s.log.join("\n")});$("#runmsg").textContent="done — stopped for human review (hover an agent for its log)";setSummary(r.summary);setStatus(r.status);showTab(cur)}
$("#run").onclick=()=>animateRun("/api/run");
document.querySelectorAll(".gate button").forEach(b=>b.onclick=async()=>{const a=b.dataset.a,g=$("#gatemsg");
 if(a=="reset"){$("#gatemsg").className="verdict";await animateRun("/api/reset");return}
 if(a=="publish"||a=="tamper"){const r=await api("/api/"+a,{});g.className="verdict "+(r.ok?"ok":"bad");g.textContent=(r.ok?"✔ ":"✘ ")+r.message;setStatus((await api("/api/state")).status);return}
 const r=await api("/api/approve",{kind:a});const s=r.status;g.className="verdict "+(s.status=="RELEASED"?"ok":"bad");g.textContent=s.status.replace(/_/g," ")+" — "+(s.reason||"")+(s.allowed?" · allowed: "+s.allowed:"");setStatus(s)});
(async()=>{drawChain(0);const s=await api("/api/state");setStatus(s.status);if(s.summary){drawChain(9);setSummary(s.summary)}showTab(0)})();
</script></body></html>"""


if __name__ == "__main__":
    print(f"Case Study Engine demo on http://localhost:{PORT}  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
