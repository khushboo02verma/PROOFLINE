# The process around the engine (one page)

**Goal:** every closed project becomes published proof within ~4 weeks, without anything leaving the building before the client says yes in writing.

## Trigger and owners

| Step | Trigger | Owner | Output | Record |
|---|---|---|---|---|
| 1. Close-out | Project acceptance signed (or 60-day stabilisation ends) | Delivery Manager | Library folder in the standard 12-folder layout; `project.json` filled (datasets, KPI definitions from the BRD, contract clause, approvers) | Library hash in the run log |
| 2. Engine run | Library complete | Engine operator (Delivery Ops) | Six outputs; status `AWAITING_INTERNAL_REVIEW` | `outputs/work/run_log.txt`, evidence ledger, refusals |
| 3. Internal review | Status file says awaiting | Head of Delivery or Legal & Compliance - never the author or the account owner | `approvals/internal_review.json` (decision, comments, pack hash) | Gate history in `RELEASE_STATUS.json` |
| 4. Send for client review | Gate says `APPROVED_TO_SEND_FOR_CLIENT_REVIEW` | Delivery Manager sends the pack by email to the contract's named approvers (here: Corporate Communications, Legal in copy) | Email + approval sheet with reply-by date (contract minimum, here 10 business days) | Sent email filed in the library |
| 5. Client decision | Written reply | Client authorised signatory | `approvals/client_decision.json` with option chosen | Gate: `RELEASED` / `REJECTED` / `WITHDRAWN` |
| 6. Publish | Gate says `RELEASED` | Marketing publishes exactly the frozen pack | Web page, deck slide, LinkedIn | Pack hash recorded against each placement |

## Approval loops

- **Any edit after approval** changes the pack hash; the gate voids the approval and the pack goes back to step 3.
- **Plant staff saying yes** (or a WhatsApp thumbs-up) does not count; the gate checks the client department named in the contract.
- **Champion first:** before step 4 the Delivery Manager walks the client's internal sponsor through the draft (facts only) so the formal request arrives pre-checked.

## What happens on a "no"

| Client says | We do |
|---|---|
| No to publication | Status `REJECTED`. Pack kept for internal lessons-learned only. We ask once whether a narrower version (e.g. security fact sheet only) is acceptable; we do not re-ask for 6 months. |
| Yes, but strike lines X, Y | Writer drafts change, engine re-runs, fact-checker re-verifies, new hash, back to step 3, then the client sees only the diff. |
| Named later (e.g. after an audit) | Anonymised version may run if approved; named version is a new pack and a new approval. Calendar reminder on the date the client gave. |
| Withdraws an earlier yes | Status `WITHDRAWN`. Within 30 days (MSA 15.4) Marketing removes it from every placement recorded against the hash and confirms in writing. |

## Records kept

Per project folder: the library (read-only), `project.json`, evidence ledger (every claim with file:line), refusals log, results sheet with working, exposure report, frozen pack + hash, gate history, sent emails, client decision. Kept 5 years after the MSA ends (matches the confidentiality survival period).

## At 50 projects a year

- **Different data, same engine:** only `project.json` changes (datasets, metric specs, identifier list, approvers). The agents, fact-checker and gate are untouched - shown by `tests/fixtures/mini_project`, a different industry with different files.
- **Extraction at scale:** `--llm` runs the extractor prompt file by file; humans review only refused items and the draft, not 40 files.
- **Throughput:** one engine operator can run ~2 projects a week; reviewer time is the bottleneck, so the approval sheet is built to be read in 10 minutes.
- **Dashboard:** a weekly list of every project's gate status and reply-by dates; anything past its reply-by date gets one polite reminder, never a second channel (no WhatsApp approvals).
