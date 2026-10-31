# Case Study Engine

**Turns a finished client project into a case study that is true, safe to publish, and approved by the client.**

You give it the project's records (emails, meeting notes, contracts, purchase orders, data exports, photos). It works out what was promised, what was delivered and which numbers are true. Then it writes the case study for three readers (security/legal, the plant team, the buyer), redacts everything that could identify the client, and **stops until a person approves it**.

One rule runs through everything: **no sentence or number leaves without a file behind it.**

Built for the PanScience Innovation Hackathon (31 Oct 2026) on the fictional *Project Drishti* library.

---

## Contents

1. [Set it up (5 minutes)](#1-set-it-up-5-minutes)
2. [Use it](#2-use-it)
3. [Present it (7-minute demo)](#3-present-it-7-minute-demo)
4. [What it produces](#4-what-it-produces)
5. [How it works](#5-how-it-works)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Set it up (5 minutes)

### Step 1: Install Python
You need **Python 3.10 or newer**. Check in a terminal:
```bash
python --version
```
If it isn't installed, get it from https://www.python.org/downloads/. On Windows, tick **"Add Python to PATH"** during install.

### Step 2: Get the code
```bash
git clone https://github.com/DhruvGargas/case-study-engine.git
```
```bash
cd case-study-engine
```
(The repo is private: you need to be signed in to GitHub with access to it.)

### Step 3: Install the three libraries it uses
```bash
pip install -r requirements.txt
```
That installs `matplotlib` (charts), `Pillow` (images) and `python-pptx` (slides). Nothing else is needed.

### Step 4: Add the project library
The library is confidential, so **it is not in this repo**. Unzip `Project_Drishti_Library.zip` into the `library` folder so the layout is:

```
case-study-engine/
└── library/
    └── Project_Drishti_Library/
        ├── 00_README.md
        ├── 01_contract/
        ├── 02_scoping/
        └── ... (13 folders)
```

On Windows (PowerShell), from the repo folder:
```powershell
Expand-Archive -Path "$HOME\Downloads\Project_Drishti_Library.zip" -DestinationPath library
```

### Step 5: Check everything works
```bash
python -m unittest -v tests.test_engine
```
You should see **`Ran 9 tests ... OK`**. If you do, setup is done.

---

## 2. Use it

### Option A: the web page (best for showing people)
```bash
python webapp.py
```
Open **http://localhost:8765** in your browser. Everything runs on your computer; nothing is sent anywhere. Press `Ctrl+C` in the terminal to stop it.

The page has four sections:

| Section | What you do | What it shows |
|---|---|---|
| **1 · Run the chain** | Click **▶ Run engine on the library** | Nine agents light up in order, then **STOP**. Counters and the key results appear. |
| **2 · Try to sneak a claim past it** | Click an example, or type your own sentence | The fact-checker says **ACCEPTED** or **REFUSED** and why |
| **3 · Stop for a person** | Click the approval buttons | Whether the case study may be sent or published |
| **4 · The six outputs** | Click the tabs | The story timeline, results with working, exposure report, case study, media and approval sheet |

### Option B: the command line
Run the whole engine:
```bash
python run_engine.py run --project projects/drishti
```
It ends with `STOPPED for human approval`. The results land in `projects/drishti/outputs/`.

Try to publish (it will refuse until a person approves):
```bash
python run_engine.py publish --project projects/drishti
```

Check the approval status after approval files are added to `approvals/`:
```bash
python run_engine.py gate --project projects/drishti
```

### Optional: let Claude do the reading and writing
By default the engine runs offline from a saved extraction and saved drafts (`projects/drishti/evidence.json` and `drafts/`). With an Anthropic API key, Claude reads the library and writes the drafts instead. The checker, calculator and approval gate stay the same either way.
```bash
pip install anthropic
```
Set your key (PowerShell: `$env:ANTHROPIC_API_KEY="sk-..."`; Mac/Linux: `export ANTHROPIC_API_KEY=sk-...`), then:
```bash
python run_engine.py run --project projects/drishti --llm
```

### Use it on a different project
Nothing in `engine/` changes. Make a new folder `projects/<name>/` with:
- `project.json`: where the data files are, how each KPI is calculated, which names/places must be hidden, and who approves. Copy `projects/drishti/project.json` as a template.
- `evidence.json` and `drafts/`: created by `--llm`, or written by hand.

`tests/fixtures/mini_project` is a working example from a different industry.

---

## 3. Present it (7-minute demo)

**Before you start:** run `python webapp.py`, open http://localhost:8765, and click **Reset** so it starts clean. The full script with what to say is in [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md).

### Step 1: Open with the problem (30 sec)
> "Our own sales draft for this project said *74% → 97% compliance, zero accidents, ₹2.3 crore saved*. Every one of those is wrong when you check the records, and the client's legal team said no to it. Writing a case study is easy. Knowing what's true and safe to say is the hard part."

### Step 2: Run it (1 min)
Click **▶ Run engine**. Say:
> "Nine agents, each with one job. It read 42 files and traced 157 pieces of evidence to an exact file and line. None were refused. It recomputed 54 numbers from the raw data, and then it **stopped**, because nothing leaves without a person."

Point at the result cards: compliance **69% → 91%** (target met). Zone breaches **−46%**: missed, and then **−77%** after the client fitted guards. "Missed targets are shown as missed, and credit is shared."

### Step 3: Try to trick it (2 min) ← the strongest moment
Click the example buttons one by one:

| Claim | Result | Why |
|---|---|---|
| "PPE compliance rose from 74% to 97%" | ❌ Refused | Those numbers aren't in the cited source |
| "We achieved zero LTIs since go-live" | ❌ Refused | The client ruled this claim out in writing |
| "Ardent's plant reached 91%" | ❌ Refused | Would name the client |
| "Cameras now cover all 146 locations" | ❌ Refused | The camera count identifies the plant |
| "PPE compliance rose from 69% to 91%" | ✅ Accepted | Every number matches the source |

Then **ask the interviewer to type a claim of their own** and watch it get checked.

### Step 4: Show it stops for a person (1.5 min)
Click in this order and read each result out loud:
1. **Publish**: blocked.
2. **Author approves own work**: refused (you can't approve yourself).
3. **Head of Delivery approves**: may now be *sent* to the client, but not published.
4. **Plant head says yes (WhatsApp)**: doesn't count; the contract says Corporate Communications.
5. **Corporate Comms + Legal approve**: **RELEASED**.
6. **Publish**: allowed.
7. **Edit text after approval**: approval void, because the text changed.
8. **Reset**.

### Step 5: Show the outputs (1.5 min)
Click the tabs:
- **Results sheet**: "Every number shows its calculation, and *Where sources disagree* says which figure I used and why."
- **Exposure report**: "The camera photo has the plant's GPS location hidden in the file, and a press release would identify the plant from the gate story. Both were caught."
- **Case study**: one story told three ways: the security fact sheet, the plant team's story ("*I showed the photo. After that, no argument.*"), and the buyer's one-pager.
- **Media pack**: charts and a diagram redrawn from data, with no client photos.
- **Approval sheet**: the one-page form the client signs, with four options and every number's source.

### Step 6: Close (30 sec)
> "Nine automated tests pass, including one where it must refuse a claim and one where it must stop for a person. It runs on a different project with no code changes. The AI can suggest text, but only checked, approved facts can ever leave."

### Questions you might get
- **"Where is the AI?"** The extractor and writer are Claude prompts in `prompts/` (run with `--llm`). The calculator, fact-checker and approval gate are plain code on purpose, so a model can't publish anything unchecked. Today's run used the saved extraction and drafts because there was no API key; [docs/MANUAL_EDITS.md](docs/MANUAL_EDITS.md) says so.
- **"Does it work on another project?"** Yes. Only `project.json` changes; see `tests/fixtures/mini_project`.
- **"What if the client says no?"** See [docs/PROCESS.md](docs/PROCESS.md). A no keeps it internal; requested changes mean a re-run and a fresh approval; a withdrawal means all use stops within 30 days, as the contract requires.

---

## 4. What it produces

Everything is in `projects/drishti/outputs/`:

| # | Output | File |
|---|---|---|
| 1 | **Story spine**: dated timeline, every line linked to its file and line, plus delays from the tracker | `01_story_spine.md` |
| 2 | **Results sheet**: each result's definition, baseline, window, method, final number, other causes, source disagreements and calculation | `02_results_sheet.md` |
| 3 | **Exposure report**: everything that could identify the client, alone or combined, with the safe replacement and the contract rule | `03_exposure_report.md` |
| 4 | **Case study**: gatekeeper, user and buyer versions, plus a note the client's champion can forward | `04_case_study.md` |
| 5 | **Media pack**: two charts, a redrawn architecture diagram, a sales slide and a payback calculator | `05_media/` |
| 6 | **Approval request and approval sheet** | `06_approval/` |

Supporting files are in `work/`: the evidence ledger, refused lines, the run log, and the case study with every source shown.

The other hand-in items: [process on one page](docs/PROCESS.md), [manual edits log](docs/MANUAL_EDITS.md), [prompt log](docs/PROMPT_LOG.md), [test output](docs/test_output.txt), [agent prompts](prompts/), [3-slide pitch](pitch/pitch.pptx).

---

## 5. How it works

```
Librarian → Extractor → Historian → Analyst → Exposure officer → Writer → Fact-checker → Media → Approval clerk → STOP
```

| Agent | Job |
|---|---|
| Librarian | Lists every file and reads hidden image data (GPS, camera model) |
| Extractor | Pulls out evidence; every quote must appear **word for word** in its file |
| Historian | Builds the dated timeline, phases and delays |
| Analyst | Recalculates every number from the raw data and shows the working |
| Exposure officer | Finds names, places, capacities, system names and risky combinations |
| Writer | Writes the three versions; every sentence cites its sources |
| Fact-checker | Deletes any sentence with an unsourced number, a banned claim or an identifying detail |
| Media | Draws charts and a diagram from the data, and strips all hidden file data |
| Approval clerk | Writes the approval request, locks the pack, and **stops** |

**Approval gate:** the pack is locked with a fingerprint (a hash). It needs an internal reviewer who isn't the author, then the client's Corporate Communications with Legal in copy. Change one word and the approvals are void.

More detail: [prompts/README.md](prompts/README.md).

```
run_engine.py        command line
webapp.py            web demo (localhost:8765)
engine/              the nine agents, the approval gate, the optional Claude client
prompts/             agent instructions
projects/drishti/    settings, evidence, drafts, outputs
tests/               9 checks + a second sample project
docs/                process, demo script, manual edits, prompt log
pitch/               3-slide pitch
```

---

## 6. Troubleshooting

| Problem | Fix |
|---|---|
| `Library folder not found` | The library isn't in `library/Project_Drishti_Library/`. Redo setup step 4. |
| `ModuleNotFoundError: matplotlib` (or `PIL`, `pptx`) | Run `pip install -r requirements.txt` |
| `python` not found on Windows | Use `py` instead of `python`, or reinstall Python with "Add to PATH" ticked |
| Port 8765 already in use | Run `python webapp.py 8800` and open http://localhost:8800 |
| An approval says "different version of the pack" | You re-ran the engine after approving. Click **Reset** (or delete `approvals/*.json`) and approve again. |

---

**Confidentiality:** the library is fictional but treated as confidential under the hackathon rules. It is git-ignored and must never be committed. Some files in `outputs/` (the story spine and exposure report) name client people, so **keep this repository private**.
