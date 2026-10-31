# Agent instructions

The engine is a chain of nine agents, each with one job. Two call Claude when run with `--llm` (`extractor.md`, `writer.md` are their system prompts). The other seven are deterministic programs; their instructions are below and in each module's docstring, because a calculation or a rule check should not depend on a model's mood.

| # | Agent | Job | How it is instructed | Can it invent? |
|---|---|---|---|---|
| 1 | Librarian (`engine/agents/librarian.py`) | Index every file; read hidden image metadata (EXIF, GPS, PNG text) | Code | No |
| 2 | Extractor (`extractor.py`) | Turn each file into evidence items with verbatim quotes | `prompts/extractor.md` (Claude) or the cached extraction; every quote re-checked against the file | Proposes; refused if the quote is not verbatim |
| 3 | Historian (`historian.py`) | Dated story spine with file:line, phases, tracker delays, data-quality issues | Code | No |
| 4 | Analyst (`analyst.py`) | Compute every number from raw data with a declarative metric spec; show the working; record source disagreements | Code + `projects/<p>/project.json` metrics/results | No |
| 5 | Exposure officer (`exposure.py`) | Find identifiers (generic patterns + project list), combination risks, media risks; map each to the contract rule and replacement | Code + config | No |
| 6 | Writer (`writer.py`) | Three reader versions + champion note, every line tagged with sources | `prompts/writer.md` (Claude) or reviewed drafts | Proposes; checked line by line |
| 7 | Fact-checker (`factcheck.py`) | Keep a line only if every source is verified, every number matches, no ruled-out claim, no leak | Code | No - it is the refusal mechanism |
| 8 | Media (`media.py`) | Choose showcase by industry playbook; draw charts/diagram/slide/calculator from data; strip metadata; leak-scan every label | Code + config | No |
| 9 | Approval clerk (`approval.py`) + gate (`engine/gate.py`) | Draft request + one-page sheet with every number's source; freeze the pack hash; STOP | Code + config | No |

Rules every agent follows:
- Only the library. No outside facts, no benchmarks.
- Anything estimated is labelled ASSUMED (e.g. the client's holiday calendar in the reply date).
- Nothing is sent. The engine ends in `AWAITING_INTERNAL_REVIEW`; only signed decision files move it on.
