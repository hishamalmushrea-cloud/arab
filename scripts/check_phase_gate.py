#!/usr/bin/env python3
"""Executable Phase 0 and Phase 1 exit gates."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from model import COUNTRIES, ROOT, read_jsonl, write_json


class Gate:
    def __init__(self, phase: str):
        self.phase = phase
        self.errors: list[str] = []
        self.checks: dict[str, Any] = {}

    def require(self, condition: bool, name: str, detail: str):
        self.checks[name] = {"status": "pass" if condition else "fail", "detail": detail}
        if not condition: self.errors.append(f"{name}: {detail}")

    def command(self, name: str, command: list[str]):
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        self.checks[name] = {
            "status": "pass" if result.returncode == 0 else "fail",
            "command": " ".join(command),
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
        if result.returncode:
            self.errors.append(f"{name}: command failed with exit {result.returncode}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def phase0(gate: Gate) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    legacy_readme = (ROOT / "قاعدة_بيانات_الأماكن/README.md").read_text(encoding="utf-8")
    gate.require("غير مكتملة" in readme and "جميع المدن" in readme and "100%" in readme, "completion_claims", "README declares incomplete local coverage and constrains 100%")
    gate.require("ليست المصدر السلطوي" in legacy_readme and "اكتمال المدن" in legacy_readme, "legacy_authority", "legacy CSV README disclaims authority and completeness")

    required_schemas = ["entity", "alias", "relationship", "source", "claim", "snapshot", "denominator", "coverage"]
    missing = [name for name in required_schemas if not (ROOT / f"schema/{name}.schema.json").is_file()]
    gate.require(not missing and (ROOT / "schema/schema_v1.md").is_file() and (ROOT / "schema/entity_types.md").is_file(), "schema_contract", f"required schemas present; missing={missing}")

    manifests = sorted((ROOT / "manifests").glob("*.yml"))
    manifest_codes = {path.stem for path in manifests}
    gate.require(len(manifests) == 22 and manifest_codes == set(COUNTRIES), "all_manifests", f"manifests={len(manifests)}, ISO set matches={manifest_codes == set(COUNTRIES)}")

    sources = list((ROOT / "data/sources").glob("*.json"))
    gate.require(bool(sources), "atomic_sources", f"atomic source files={len(sources)}")
    country_entities = [row for row in read_jsonl(ROOT / "data/entities/entities.jsonl") if row.get("entity_type") == "country"]
    gate.require(len(country_entities) == 22 and all(row.get("canonical_source_id") for row in country_entities), "country_roots", f"source-backed country roots={len(country_entities)}")

    repairs = read_jsonl(ROOT / "data/quarantine/legacy_repairs.jsonl")
    actions = Counter(row.get("action") for row in repairs)
    links = read_jsonl(ROOT / "data/quarantine/link_repairs.jsonl")
    gate.require(actions["join_excess_csv_fields_into_notes"] == 2, "saudi_rows", f"malformed Saudi row repairs={actions['join_excess_csv_fields_into_notes']}")
    gate.require(actions["rename_duplicate_legacy_id"] == 58, "duplicate_id_repairs", f"renamed duplicate ID occurrences={actions['rename_duplicate_legacy_id']}")
    gate.require(len(links) == 25, "broken_link_repairs", f"logged link repairs={len(links)}")

    workflow = ROOT / ".github/workflows/validate.yml"
    gate.require(workflow.is_file(), "ci_workflow", ".github/workflows/validate.yml exists")
    gate.require((ROOT / "scripts/validate.py").is_file(), "validator", "dependency-free validator exists")
    gate.command("validation", [sys.executable, "scripts/validate.py"])


def phase1(gate: Gate) -> None:
    phase0(gate)
    gate.command("generated_freshness", [sys.executable, "scripts/generate.py", "--check"])

    entities = read_jsonl(ROOT / "data/entities/entities.jsonl")
    claims = read_jsonl(ROOT / "data/claims/claims.jsonl")
    relationships = read_jsonl(ROOT / "data/relationships/relationships.jsonl")
    coverage = read_jsonl(ROOT / "data/coverage/coverage.jsonl")
    denominators = read_jsonl(ROOT / "data/coverage/denominators.jsonl")
    ledger = read_jsonl(ROOT / "data/quarantine/migration_ledger.jsonl")
    entity_by_id = {row["id"]: row for row in entities}
    den_by_id = {row["id"]: row for row in denominators}
    cov_by_scope = {(row["country_code"], row["layer"]): row for row in coverage}

    gate.require(len(entities) <= 500, "no_mass_expansion", f"active entity count={len(entities)} (country roots and bounded Tunisia/Libya pilots only)")
    gate.require(all(row.get("canonical_source_id") for row in entities), "sourced_entities", f"source-backed entities={len(entities)}")
    gate.require(all(row.get("source_id") for row in claims), "sourced_claims", f"source-backed claims={len(claims)}")

    tn_gov = [row for row in entities if row["country_code"] == "TN" and row["entity_type"] == "tn_governorate"]
    tn_del = [row for row in entities if row["country_code"] == "TN" and row["entity_type"] == "tn_delegation"]
    tn_claims = [row for row in claims if entity_by_id[row["subject_id"]]["country_code"] == "TN"]
    gate.require((len(tn_gov), len(tn_del), len(tn_claims)) == (24, 264, 24), "tunisia_core", f"governorates={len(tn_gov)}, delegations={len(tn_del)}, population claims={len(tn_claims)}")
    tn_mun_cov = cov_by_scope.get(("TN", "municipalities_2018"), {})
    tn_mun_den = den_by_id.get(tn_mun_cov.get("denominator_id"), {})
    gate.require(tn_mun_den.get("value") == 350 and tn_mun_cov.get("matched") == 0 and tn_mun_cov.get("missing") == 350, "tunisia_municipalities", "dated 2018 denominator=350, matched=0, missing=350")
    gate.require(den_by_id[cov_by_scope[("TN", "imadas")]["denominator_id"]]["value"] is None, "tunisia_imadas", "unverified denominator remains unavailable")

    ly_current = [row for row in entities if row["country_code"] == "LY" and row["entity_type"] == "ly_municipality"]
    ly_historic = [row for row in entities if row["country_code"] == "LY" and row["entity_type"] == "ly_shabiya_historical"]
    ly_current_den = den_by_id[cov_by_scope[("LY", "current_municipalities")]["denominator_id"]]
    gate.require((len(ly_current), len(ly_historic)) == (93, 22), "libya_layers", f"matched current municipality subset={len(ly_current)}, historical sha‘biyat={len(ly_historic)}")
    gate.require(ly_current_den.get("value") is None and ly_current_den.get("status") == "unavailable", "libya_denominator", "current national municipality denominator remains unresolved")
    historic_ids = {row["id"] for row in ly_historic}
    current_ids = {row["id"] for row in ly_current}
    mixed = [row["id"] for row in relationships if row.get("child_id") in historic_ids and row.get("parent_id") in current_ids]
    gate.require(not mixed, "libya_temporal_separation", f"historical-to-current parent links={len(mixed)}")

    # Ledger must account for every data row, including the one-row CSV template.
    csv_rows = 0
    import csv
    for path in (ROOT / "قاعدة_بيانات_الأماكن").glob("*.csv"):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            csv_rows += sum(1 for _ in csv.DictReader(handle))
    gate.require(len(ledger) == csv_rows, "migration_ledger", f"ledger={len(ledger)}, legacy rows including template={csv_rows}")

    required_outputs = []
    for family in ["entities", "aliases", "relationships", "claims", "sources"]:
        required_outputs += [ROOT / f"generated/json/{family}.json", ROOT / f"generated/csv/{family}.csv"]
    required_outputs += [ROOT / "generated/markdown/README.md", ROOT / "generated/html/index.html"]
    required_outputs += [ROOT / f"generated/markdown/countries/{iso}.md" for iso in COUNTRIES]
    required_outputs += [ROOT / f"generated/html/countries/{iso}.html" for iso in COUNTRIES]
    missing = [str(path.relative_to(ROOT)) for path in required_outputs if not path.is_file()]
    gate.require(not missing, "four_formats", f"required generated files present; missing={missing}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["phase0", "phase1"])
    args = parser.parse_args()
    gate = Gate(args.phase)
    (phase0 if args.phase == "phase0" else phase1)(gate)
    report = {"phase": args.phase, "status": "pass" if not gate.errors else "fail", "checks": gate.checks, "errors": gate.errors}
    write_json(ROOT / f"reports/{args.phase}_gate.json", report)
    for name, result in gate.checks.items():
        print(f"[{'PASS' if result['status'] == 'pass' else 'FAIL'}] {name}: {result.get('detail', result.get('command', ''))}")
    if gate.errors:
        print(f"{args.phase} gate failed with {len(gate.errors)} error(s)", file=sys.stderr)
        for error in gate.errors: print(f"- {error}", file=sys.stderr)
        return 1
    print(f"{args.phase} gate passed ({len(gate.checks)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
