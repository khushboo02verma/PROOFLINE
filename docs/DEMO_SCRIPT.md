# Live demo script (about 7 minutes)

## Easiest: the web page
```
python webapp.py
```
Open http://localhost:8765 and go top to bottom:
1. **Run engine on the library.** The nine agents light up, then it STOPS. Point at the numbers: 157 evidence items traced, 0 refused, and the KPI cards (69% → 91% met; zones −46%, missed, then −77% after guards).
2. **Try to sneak a claim past it.** Click the example chips: "74% to 97%" is refused (numbers not in source), "zero LTIs" is refused (ruled out), "Ardent's plant" and "146 locations" are refused (would identify the client), and "69% to 91%" is accepted. Let the interviewer type their own claim.
3. **Stop for a person.** Click in this order: Publish (blocked) → Author approves own work (refused) → Head of Delivery approves → Plant head says yes (doesn't count) → Corporate Comms + Legal approve (RELEASED) → Publish (allowed) → Edit text after approval (approval void) → Reset.
4. **Outputs tabs.** Results sheet ("where sources disagree"), Exposure report (GPS in the photo, weighbridge press release), Case study, Media pack, Approval sheet.

The terminal version below is the backup if the browser misbehaves.

Open a terminal in the project folder before you start. Keep `04_case_study.md`, `02_results_sheet.md` and `03_exposure_report.md` open in tabs.

## 0. The one-line pitch (20 s)
"Writing a case study is easy. Knowing which numbers are true and what is safe to say is the hard part. My engine has one rule: no line leaves without a file behind it, and nothing leaves without a person saying yes."

## 1. Run it (1 min)
```
python run_engine.py run --project projects/drishti
```
Read the log aloud, one line per agent: 42 files indexed, 157 evidence items traced to a file and line, 54 metrics, 0 refused, 5 media assets, then **STOPPED for human review**.

## 2. Numbers are true (1.5 min): open `02_results_sheet.md`, K1
- "I recompute from the raw CSV: 68.9% to 91.1%. That matches the client's signed acceptance certificate exactly."
- Point at **Where sources disagree**: "Our own sales team said 74% to 97%. 74% is the announced manual walk score and 96.6% is one area's best week. The client rejected it in writing, so the engine doesn't use it."
- K2 and K3: "Two targets were missed at pilot end. I show them as missed, then show how the client's guards and phone rule fixed them. Credit is shared."
- Money: "Only the gate saving, because that's the only money the client's finance team measured. No avoided-injury savings and no benchmark numbers."

## 3. It refuses a bad claim (1.5 min): live
Add this line to the end of `projects/drishti/drafts/buyer.md`:
```
PPE compliance rose from 74% to 97% and we saved Rs 2.3 crore [M:K1_result]
```
Re-run, then open `projects/drishti/outputs/work/04_refusals.md`:
> number(s) 74, 97, 2.3 not found in cited sources

"It's dropped and logged, not silently fixed." Delete the line afterwards and re-run.

## 4. Safe to publish (1 min): open `03_exposure_report.md`
- "The cameras' own photo has GPS coordinates hidden in the file, and the client's logo on the wall. Rejected, and I redrew the charts from data."
- "Combination risks: the client's press release about a second weighbridge, plus the gate story, would name the plant. So the case study says 'a separate client investment in gate infrastructure'."
- "The nicest quote, 'told us the uncomfortable number first', is from a public LinkedIn post. Quoting it names the client, so it isn't used."

## 5. Three readers (45 s): open `04_case_study.md`
Gatekeeper fact sheet ("no video leaves the plant") / user story ("I showed the photo. After that, no argument.") / buyer headline plus payback in the client's own words / a note the client's champion can forward.

## 6. It stops for a person (1 min)
```
python run_engine.py publish --project projects/drishti
```
Blocked. Then show the two approvals:
```
python -c "import json;s=json.load(open('projects/drishti/outputs/RELEASE_STATUS.json'));json.dump({'reviewer':'Demo Reviewer','reviewer_role':'Head of Delivery','decision':'approve','pack_sha256':s['pack_sha256']},open('approvals/internal_review.json','w'))"
```
```
python run_engine.py gate --project projects/drishti
```
"Approved to send, but still no publication."
```
python -c "import json;s=json.load(open('projects/drishti/outputs/RELEASE_STATUS.json'));json.dump({'signatory':'Head of Corporate Communications','department':'Corporate Communications','legal_in_copy':True,'decision':'approve','option':'A','pack_sha256':s['pack_sha256']},open('approvals/client_decision.json','w'))"
```
```
python run_engine.py gate --project projects/drishti
```
```
python run_engine.py publish --project projects/drishti
```
"Now it releases, under the option they picked. If anyone edits one word after approval, the hash changes and the approval is void. Plant staff approving alone doesn't count, because the contract says Corporate Communications."

## 7. Tests and reuse (30 s)
```
python -m unittest -v tests.test_engine
```
"9 checks, including a refusal test, a stop-for-a-person test, and the same code running on a different project's library."

## Reset after the demo
Delete `approvals/internal_review.json` and `approvals/client_decision.json`, then run step 1 again.

## Likely questions
- **Where's the AI?** "The extractor and writer are Claude prompts (`prompts/`, run with `--llm`). The calculator, fact-checker and gate are code on purpose: a model can propose text, but it can't get an untraceable number or an unapproved pack out. Today it ran from the cached extraction and drafts because there's no API key here. That's logged in `docs/MANUAL_EDITS.md`."
- **Another project?** "Only `project.json` changes: datasets, KPI definitions, identifiers, approvers. The test fixture is a different industry."
- **What if the client says no?** `docs/PROCESS.md`: rejected stays internal-only; changes go through a re-run and new approval; withdrawal means we stop new use within 30 days, per MSA 15.4.
- **Why not claim zero injuries?** "Seven months at about one injury a quarter proves nothing. The client's EHS and finance both said so in writing."
