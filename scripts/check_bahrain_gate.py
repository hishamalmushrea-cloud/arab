#!/usr/bin/env python3
"""Bahrain production release gate, layered after the accepted Phase 5 gate."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from model import ROOT, read_jsonl, write_json

MANAGED = [
    "data/entities/entities.jsonl", "data/aliases/aliases.jsonl", "data/relationships/relationships.jsonl",
    "data/claims/claims.jsonl", "data/coverage/denominators.jsonl", "data/coverage/coverage.jsonl",
    "data/snapshots/snapshots.jsonl", "manifests/BH.yml", "data/cultural/bahrain_domain_status.json",
    "data/imports/bahrain/source_catalog.json",
]

class Gate:
    def __init__(self): self.checks, self.errors = {}, []
    def require(self, ok, name, detail):
        self.checks[name] = {"status": "pass" if ok else "fail", "detail": detail}
        if not ok: self.errors.append(f"{name}: {detail}")
    def command(self, name, command):
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        self.checks[name] = {"status": "pass" if result.returncode == 0 else "fail", "command": " ".join(command), "returncode": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
        if result.returncode: self.errors.append(f"{name}: exit {result.returncode}")


def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def file_hashes(): return {p: sha(ROOT / p) for p in MANAGED}

def source_hashes():
    result = {}
    for path in sorted((ROOT / "data/sources").glob("*.json")):
        row = json.loads(path.read_text(encoding="utf-8"))
        if row.get("country_codes") == ["BH"]: result[str(path.relative_to(ROOT))] = sha(path)
    return result

def non_bahrain_hash() -> str:
    entities = read_jsonl(ROOT / "data/entities/entities.jsonl")
    bh_ids = {r["id"] for r in entities if r.get("country_code") == "BH"}
    payload = {
        "entities": [r for r in entities if r["id"] not in bh_ids],
        "aliases": [r for r in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if r["entity_id"] not in bh_ids],
        "relationships": [r for r in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if r["child_id"] not in bh_ids and r["parent_id"] not in bh_ids],
        "claims": [r for r in read_jsonl(ROOT / "data/claims/claims.jsonl") if r["subject_id"] not in bh_ids],
        "denominators": [r for r in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if r["country_code"] != "BH"],
        "coverage": [r for r in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if r["country_code"] != "BH"],
        "snapshots": [r for r in read_jsonl(ROOT / "data/snapshots/snapshots.jsonl") if not r["id"].startswith("SNP-BH-")],
    }
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main() -> int:
    gate = Gate()
    before_sources = source_hashes()
    gate.command("bahrain_source_refresh", [sys.executable, "scripts/build_bahrain_sources.py"])
    after_sources = source_hashes()
    gate.require(len(after_sources) == 7 and before_sources == after_sources, "bahrain_source_idempotence", f"atomic sources={len(after_sources)}/7, unchanged={before_sources == after_sources}")
    before_files, before_other = file_hashes(), non_bahrain_hash()
    gate.command("bahrain_import_refresh", [sys.executable, "scripts/import_bahrain_production.py"])
    after_files, after_other = file_hashes(), non_bahrain_hash()
    gate.require(before_files == after_files, "bahrain_import_idempotence", f"all {len(MANAGED)} managed hashes unchanged={before_files == after_files}")
    gate.require(before_other == after_other, "non_bahrain_preservation", f"canonical non-Bahrain SHA-256 unchanged={after_other}")
    gate.command("general_validation", [sys.executable, "scripts/validate.py"])
    gate.command("bahrain_semantic_validation", [sys.executable, "scripts/validate_bahrain.py"])
    gate.command("bahrain_negative_tests", [sys.executable, "scripts/test_bahrain_negative.py"])
    sample_path = ROOT / "data/review/bahrain_review_samples.json"
    before_sample = sha(sample_path)
    gate.command("bahrain_review_sample_refresh", [sys.executable, "scripts/build_bahrain_review_samples.py"])
    gate.require(before_sample == sha(sample_path), "bahrain_review_sample_idempotence", f"full-population sample unchanged={before_sample == sha(sample_path)}")
    before_review = sha(ROOT / "reports/bahrain_independent_review.json")
    gate.command("bahrain_independent_review", [sys.executable, "scripts/review_bahrain.py"])
    gate.require(before_review == sha(ROOT / "reports/bahrain_independent_review.json"), "bahrain_review_idempotence", f"independent review unchanged={before_review == sha(ROOT / 'reports/bahrain_independent_review.json')}")
    gate.command("generated_freshness", [sys.executable, "scripts/generate.py", "--check"])
    validation = json.loads((ROOT / "reports/bahrain_validation.json").read_text(encoding="utf-8"))
    negatives = json.loads((ROOT / "reports/bahrain_negative_tests.json").read_text(encoding="utf-8"))
    review = json.loads((ROOT / "reports/bahrain_independent_review.json").read_text(encoding="utf-8"))
    gate.require(validation.get("status") == "PASS" and validation.get("p0") == 0 and validation.get("critical_p1") == 0, "bahrain_findings_closed", f"status={validation.get('status')}, P0={validation.get('p0')}, critical P1={validation.get('critical_p1')}")
    gate.require(negatives.get("status") == "PASS" and negatives.get("detected") == negatives.get("required") == 9, "bahrain_required_mutations", f"detected={negatives.get('detected')}/{negatives.get('required')}")
    gate.require(review.get("status") == "PASS" and review.get("total_sampled") == review.get("total_passed") == 48, "bahrain_review_threshold", f"full review passed={review.get('total_passed')}/{review.get('total_sampled')}")
    for required in ["reports/BAHRAIN_PRODUCTION_CLOSEOUT.md", "reports/LESSONS_LEARNED_BAHRAIN.md", "reports/EXPANSION_LESSONS.md", "reports/NEXT_COUNTRY_DECISION.md"]:
        gate.require((ROOT / required).is_file(), "artifact_" + Path(required).stem.lower(), f"{required} exists")
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
    gate.require(not status, "bahrain_clean_worktree", f"git worktree clean={not status}")
    report = {"schema_version": "2.0.0", "country_code": "BH", "snapshot_date": "2026-08-16", "status": "pass" if not gate.errors else "fail", "checks": gate.checks, "errors": gate.errors}
    write_json(ROOT / "reports/bahrain_gate.json", report)
    for name, result in gate.checks.items(): print(f"[{'PASS' if result['status']=='pass' else 'FAIL'}] {name}: {result.get('detail', result.get('command',''))}")
    if gate.errors:
        for error in gate.errors: print("- " + error, file=sys.stderr)
        return 1
    print(f"Bahrain production gate passed ({len(gate.checks)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
