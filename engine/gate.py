"""Human gate. Two approvals, in order, each tied to the exact pack it approves:

1. approvals/internal_review.json - a PredCo reviewer (not the author) confirms the pack may be sent to
   the client for review. Status -> APPROVED_TO_SEND_FOR_CLIENT_REVIEW.
2. approvals/client_decision.json - the client's written decision from an authorised signatory in
   Corporate Communications with Legal in copy (MSA 15.3). Status -> RELEASED (with the option chosen)
   or REJECTED / WITHDRAWN.

If the pack changes after an approval (hash mismatch), the approval no longer counts. The gate never
sends or publishes anything itself; it only records decisions and says what is allowed."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class GateError(RuntimeError):
    pass


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def evaluate(out_dir: Path, approvals_dir: Path, config: dict) -> dict:
    status_path = out_dir / "RELEASE_STATUS.json"
    status = _load(status_path)
    if not status:
        raise GateError("No release status found - run the engine first.")
    manifest = _load(out_dir / "06_approval/pack_manifest.json")
    from .core import sha256_of
    current = sha256_of([out_dir / f for f in manifest["files"]])
    if current != manifest["sha256"]:
        raise GateError("Pack files changed after the engine froze them. Re-run the engine.")
    rules = config["approval"]["gate"]
    history = status.get("history", [])

    internal = _load(approvals_dir / "internal_review.json")
    if not internal:
        new = {"status": "AWAITING_INTERNAL_REVIEW", "allowed": "nothing leaves the building",
               "reason": "no internal review on file"}
    elif internal.get("pack_sha256") != current:
        new = {"status": "AWAITING_INTERNAL_REVIEW", "allowed": "nothing leaves the building",
               "reason": "internal review was for a different version of the pack"}
    elif internal.get("reviewer_role") not in rules["internal_reviewer_roles"] or internal.get("reviewer") in rules.get("authors", []):
        new = {"status": "AWAITING_INTERNAL_REVIEW", "allowed": "nothing leaves the building",
               "reason": f"reviewer must hold one of {rules['internal_reviewer_roles']} and must not be an author"}
    elif internal.get("decision") != "approve":
        new = {"status": "RETURNED_TO_AUTHOR", "allowed": "nothing leaves the building", "reason": internal.get("comments", "")}
    else:
        client = _load(approvals_dir / "client_decision.json")
        if not client:
            new = {"status": "APPROVED_TO_SEND_FOR_CLIENT_REVIEW",
                   "allowed": "a person may send 06_approval/ to the client reviewers named in it; no publication",
                   "reason": f"internal review by {internal['reviewer']}"}
        elif client.get("pack_sha256") != current:
            new = {"status": "APPROVED_TO_SEND_FOR_CLIENT_REVIEW", "allowed": "no publication",
                   "reason": "client decision refers to a different version of the pack - send the current one"}
        elif client.get("department") not in rules["client_departments"] or not client.get("legal_in_copy"):
            new = {"status": "APPROVED_TO_SEND_FOR_CLIENT_REVIEW", "allowed": "no publication",
                   "reason": "client approval must come from Corporate Communications with Legal in copy (MSA 15.3); plant approval alone does not count"}
        elif client.get("decision") == "withdrawn":
            new = {"status": "WITHDRAWN", "allowed": "stop all new use within 30 days; remove from website, deck and CRM",
                   "reason": client.get("comments", "")}
        elif client.get("decision") == "reject":
            new = {"status": "REJECTED", "allowed": "internal lessons-learned only; do not use externally",
                   "reason": client.get("comments", "")}
        elif client.get("option") in [o["id"] for o in config["approval"]["options"]]:
            opt = next(o for o in config["approval"]["options"] if o["id"] == client["option"])
            new = {"status": "RELEASED", "option": opt["name"], "allowed": opt["publishes"],
                   "reason": f"written approval by {client.get('signatory')} ({client.get('department')})"}
        else:
            new = {"status": "APPROVED_TO_SEND_FOR_CLIENT_REVIEW", "allowed": "no publication",
                   "reason": "client decision has no recognised option"}
    new["pack_sha256"] = current
    new["checked_at"] = datetime.now().isoformat(timespec="seconds")
    new["history"] = history + [{k: new[k] for k in ("status", "reason", "checked_at")}]
    status_path.write_text(json.dumps(new, indent=2), encoding="utf-8")
    return new


def assert_releasable(out_dir: Path) -> dict:
    status = _load(out_dir / "RELEASE_STATUS.json") or {}
    if status.get("status") != "RELEASED":
        raise GateError(f"Blocked: status is {status.get('status', 'unknown')}. A person must approve before anything is used.")
    return status
