"""Engine checks. Run: python -m unittest -v tests.test_engine"""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from engine.agents import analyst, approval, exposure, extractor, factcheck, historian, librarian, media, writer
from engine.agents.exposure import leak_scan
from engine.agents.factcheck import check_line
from engine.core import Library, RunContext
from engine.gate import GateError, assert_releasable, evaluate

ROOT = Path(__file__).resolve().parent.parent
CHAIN = [librarian, extractor, historian, analyst, exposure, writer, factcheck, media, approval]


def run_chain(project_dir: Path, out_dir: Path, evidence_override: list | None = None) -> RunContext:
    cfg = json.loads((project_dir / "project.json").read_text(encoding="utf-8"))
    ctx = RunContext(library=Library(project_dir / cfg["library"]), project_dir=project_dir, out_dir=out_dir, config=cfg)
    out_dir.mkdir(parents=True, exist_ok=True)
    for agent in CHAIN:
        agent.run(ctx)
    return ctx


class DrishtiRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.out = cls.tmp / "out"
        cls.approvals = cls.tmp / "approvals"
        cls.approvals.mkdir()
        cls.ctx = run_chain(ROOT / "projects/drishti", cls.out)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_01_every_evidence_quote_is_in_its_file(self):
        self.assertEqual(self.ctx.ledger.refused, [], "all cached evidence must be verbatim in the library")
        self.assertGreater(len(self.ctx.ledger.items), 100)
        self.assertTrue(all(e.line for e in self.ctx.ledger.items.values()), "every item resolves to a line number")

    def test_02_extractor_refuses_an_invented_quote(self):
        """A quote the model (or a person) made up is refused before it can be used."""
        from engine.agents import extractor as ex
        tmp = Path(tempfile.mkdtemp())
        try:
            pdir = tmp / "p"
            shutil.copytree(ROOT / "projects/drishti", pdir, ignore=shutil.ignore_patterns("outputs"))
            ev = json.loads((pdir / "evidence.json").read_text(encoding="utf-8"))
            ev.append({"id": "fake", "date": "2026-09-30", "kind": "quote", "summary": "invented praise",
                       "file": "09_feedback/linkedin_post_2026-09-30_Meenakshi_Iyer.md", "quote": "PredCo saved us two crore with zero accidents"})
            ev.append({"id": "fake2", "date": "2026-09-30", "kind": "fact", "summary": "file that does not exist",
                       "file": "06_email/Z_invented.md", "quote": "anything"})
            (pdir / "evidence.json").write_text(json.dumps(ev), encoding="utf-8")
            cfg = json.loads((pdir / "project.json").read_text(encoding="utf-8"))
            cfg["library"] = str(ROOT / "library/Project_Drishti_Library")
            ctx = RunContext(library=Library(cfg["library"]), project_dir=pdir, out_dir=tmp / "out", config=cfg)
            ledger = ex.run(ctx)
            refused = {e.id: e.reason for e in ledger.refused}
            self.assertIn("not found verbatim", refused["fake"])
            self.assertIn("does not exist", refused["fake2"])
            ok, reason, _ = check_line("A client called us life-changing [E:fake]", ctx)
            self.assertFalse(ok)
            self.assertIn("unverified", reason)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_03_kpis_reproduce_the_records(self):
        m = {k: v["value"] for k, v in self.ctx.metrics.items()}
        self.assertEqual(round(m["K1_base"], 1), 68.9)          # certificate 68.9%
        self.assertEqual(round(m["K1_result"], 1), 91.1)        # certificate 91.1%
        self.assertEqual(round(m["K2_base"], 2), 5.58)          # certificate 5.58
        self.assertEqual(round(m["K2_result"], 2), 3.00)        # certificate 3.00
        self.assertEqual(round(m["K2_change_pct"]), -46)        # certificate -46%
        self.assertEqual(round(m["K3_result"], 1), 4.9)         # certificate 4.9 min
        self.assertEqual(round(m["K3_final_week"], 1), 3.5)     # certificate 3.5 min
        self.assertEqual(round(m["K4_result"], 1), 9.7)         # certificate 9.7%
        self.assertEqual(round(m["walk_compliance"], 1), 73.8)  # BRD v2 73.8%
        self.assertEqual(int(m["walk_people"]), 882)            # BRD v2 882 people
        self.assertEqual(round(m["K1_post_all"], 1), 89.2)      # QBR 89.2%
        self.assertEqual(round(m["K2_post"], 2), 1.26)          # QBR 1.26
        self.assertTrue(880 <= m["outage_lost"] <= 920)         # incident report "about 900"
        self.assertEqual(round(m["det_junjul"], 1), 12.1)       # finance note 12.1 L/month

    def test_04_refuses_untraceable_and_ruled_out_claims(self):
        cases = {
            "PPE compliance rose from 74% to 97% [M:K1_result]": "number",
            "We delivered zero LTIs since go-live [E:e47]": "ruled-out",
            "The project saved Rs 2.3 crore a year.": "no source",
            "Compliance reached 99% on every camera [M:K1_result]": "number",
            "The client, Ardent, reached 91% [M:K1_result]": "expose",
            "Restricted-zone entries were halved in the pilot [M:K2_change_pct]": "ruled-out",
            "Compliance rose to 91% [E:does_not_exist]": "unknown",
            "Cameras covered all 146 locations [E:e44b]": "expose",
        }
        for line, why in cases.items():
            ok, reason, _ = check_line(line, self.ctx)
            self.assertFalse(ok, f"should refuse: {line}")
            self.assertIn(why, reason, f"{line} -> {reason}")
        ok, reason, _ = check_line("PPE compliance rose from 69% to 91% [M:K1_base] [M:K1_result]", self.ctx)
        self.assertTrue(ok, reason)

    def test_05_case_study_had_no_refusals_and_leaks_nothing(self):
        self.assertEqual(sum(len(v["refused"]) for v in self.ctx.verified.values()), 0)
        text = (self.out / "04_case_study.md").read_text(encoding="utf-8")
        self.assertEqual(leak_scan(text, self.ctx), [])

    def test_06_media_has_no_metadata_and_reuses_no_client_image(self):
        from PIL import Image
        for m in self.ctx.media:
            p = self.out / m["file"]
            self.assertTrue(p.is_file(), p)
            if p.suffix == ".png":
                with Image.open(p) as im:
                    self.assertEqual(len(im.getexif()), 0)
                    self.assertFalse(set(im.info) - {"dpi"}, f"{p.name} keeps metadata {im.info}")
        self.assertGreaterEqual(len(self.ctx.media), 3)
        self.assertFalse(any("10_media" in m["file"] for m in self.ctx.media))

    def test_07_stops_for_a_person_before_anything_leaves(self):
        cfg = self.ctx.config
        status = json.loads((self.out / "RELEASE_STATUS.json").read_text())
        self.assertEqual(status["status"], "AWAITING_INTERNAL_REVIEW")
        with self.assertRaises(GateError):
            assert_releasable(self.out)
        sha = status["pack_sha256"]
        write = lambda name, d: (self.approvals / name).write_text(json.dumps({**d, "pack_sha256": sha}))
        write("internal_review.json", {"reviewer": "intern", "reviewer_role": "Sales", "decision": "approve"})
        self.assertEqual(evaluate(self.out, self.approvals, cfg)["status"], "AWAITING_INTERNAL_REVIEW")
        write("internal_review.json", {"reviewer": "R. Head", "reviewer_role": "Head of Delivery", "decision": "approve"})
        self.assertEqual(evaluate(self.out, self.approvals, cfg)["status"], "APPROVED_TO_SEND_FOR_CLIENT_REVIEW")
        with self.assertRaises(GateError):
            assert_releasable(self.out)
        # plant approval alone does not count (MSA 15.3)
        write("client_decision.json", {"signatory": "Unit Head", "department": "Plant", "legal_in_copy": False, "decision": "approve", "option": "A"})
        self.assertNotEqual(evaluate(self.out, self.approvals, cfg)["status"], "RELEASED")
        write("client_decision.json", {"signatory": "Corp Comms head", "department": "Corporate Communications", "legal_in_copy": True, "decision": "approve", "option": "A"})
        self.assertEqual(evaluate(self.out, self.approvals, cfg)["status"], "RELEASED")
        self.assertEqual(assert_releasable(self.out)["option"], "Anonymised")
        # later change of mind (MSA 15.4)
        write("client_decision.json", {"signatory": "Corp Comms head", "department": "Corporate Communications", "legal_in_copy": True, "decision": "withdrawn"})
        self.assertEqual(evaluate(self.out, self.approvals, cfg)["status"], "WITHDRAWN")
        with self.assertRaises(GateError):
            assert_releasable(self.out)

    def test_08_editing_the_pack_after_approval_voids_it(self):
        p = self.out / "04_case_study.md"
        original = p.read_text(encoding="utf-8")
        try:
            p.write_text(original + "\nPPE compliance hit 97%.\n", encoding="utf-8")
            with self.assertRaises(GateError):
                evaluate(self.out, self.approvals, self.ctx.config)
        finally:
            p.write_text(original, encoding="utf-8")


class OtherProject(unittest.TestCase):
    def test_09_same_engine_runs_on_a_different_library(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            ctx = run_chain(ROOT / "tests/fixtures/mini_project", tmp / "out")
            self.assertEqual(ctx.ledger.refused, [])
            self.assertEqual(round(ctx.metrics["change"]["value"]), -68)
            self.assertEqual(sum(len(v["refused"]) for v in ctx.verified.values()), 0)
            self.assertTrue((tmp / "out/06_approval/approval_sheet.md").is_file())
            self.assertEqual(json.loads((tmp / "out/RELEASE_STATUS.json").read_text())["status"], "AWAITING_INTERNAL_REVIEW")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
