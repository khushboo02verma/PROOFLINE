# Log of manual edits and human inputs

The engine was run offline (no Anthropic API key in this environment), so the two model-driven steps used cached inputs. Those inputs were produced with an AI coding assistant (Claude, via Claude Code) under the extractor and writer instructions, then checked by the engine like any model output. Everything below is listed so a judge can see exactly what was not produced by the engine run itself.

| # | What | Who / how | Checked by |
|---|---|---|---|
| 1 | `projects/drishti/evidence.json` - 157 evidence items with verbatim quotes | Written with Claude Code following `prompts/extractor.md`, after reading all 42 library files | Extractor agent: every quote found verbatim in its file, line number resolved (0 refused). Test 01. |
| 2 | `projects/drishti/drafts/*.md` - gatekeeper, user, buyer, champion drafts | Written with Claude Code following `prompts/writer.md` from the verified ledger and metrics | Fact-checker: every line's sources, numbers, ruled-out claims and leaks checked (0 refused). Tests 04-05. |
| 3 | `projects/drishti/project.json` - metric specs, KPI windows, identifier list, combination risks, media review notes, approvers, reply-date holidays | Written with Claude Code from the BRD, certificate, MSA, QBR and emails | Analyst reproduces the acceptance certificate and QBR figures exactly (Test 03). Visual content of the three client images was described by a person/AI reading them; the engine itself reads only their metadata. |
| 4 | Reply-by date holidays (9-10 Nov 2026) | ASSUMED - not in the library | Flagged as ASSUMED in the approval email. |
| 5 | Planned send date 2 Nov 2026 | ASSUMED - first business day after the hackathon | Flagged in config. |
| 6 | Chart layout fixes (legend placement, arrow routing) | Code changes after viewing the first render | Visual check only. |

No result, quote or person was invented. Two library data-quality issues were found and handled in code, not by editing the data: unquoted commas in `04_delivery/project_tracker.csv` (repaired on read and logged in the story spine) and 4 duplicated survey comments in `07_data/supervisor_survey_sep2026.csv` (counted and reported in the results sheet).
