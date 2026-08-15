#!/usr/bin/env python3
"""Independent UAE sample review; intentionally does not import or call the UAE importer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from model import ROOT, read_jsonl, write_json

SAMPLES = ROOT / "reports/uae_review_samples.json"
REPORT = ROOT / "reports/uae_independent_review.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    sample_plan = load_json(SAMPLES)
    manifest = load_json(ROOT / "manifests/AE.yml")
    sources_list = [load_json(path) for path in sorted((ROOT / "data/sources").glob("*.json"))]
    sources = {row["id"]: row for row in sources_list}
    entities_list = [row for row in read_jsonl(ROOT / "data/entities/entities.jsonl") if row.get("country_code") == "AE"]
    entity_ids = {row["id"] for row in entities_list}
    families: dict[str, dict[str, dict[str, Any]]] = {
        "entities": {row["id"]: row for row in entities_list},
        "aliases": {row["id"]: row for row in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if row.get("entity_id") in entity_ids},
        "relationships": {row["id"]: row for row in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if row.get("child_id") in entity_ids},
        "claims": {row["id"]: row for row in read_jsonl(ROOT / "data/claims/claims.jsonl") if row.get("subject_id") in entity_ids},
        "denominators": {row["id"]: row for row in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if row.get("country_code") == "AE"},
        "coverage": {row["id"]: row for row in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if row.get("country_code") == "AE"},
        "sources": sources,
    }
    families["cultural_claims"] = {rid: row for rid, row in families["claims"].items() if row.get("predicate") != "jurisdiction_semantics"}
    families["dialect_claims"] = {rid: row for rid, row in families["claims"].items() if row.get("predicate") == "lexical_form"}

    expected_type: dict[str, str] = {}
    expected_parent: dict[str, str] = {}
    for profile in manifest.get("emirate_profiles", []):
        expected_type[profile["emirate_id"]] = "ae_emirate"
        expected_parent[profile["emirate_id"]] = "ENT-AE-COUNTRY"
        for layer in profile.get("lower_layers", []):
            for eid in layer.get("entity_ids", []):
                expected_type[eid] = layer["entity_type"]
                expected_parent[eid] = profile["emirate_id"]
    actual_parent = {row["child_id"]: row["parent_id"] for row in families["relationships"].values() if row.get("relationship_type") == "administrative_parent"}
    den_by_id = families["denominators"]

    findings: list[dict[str, str]] = []
    family_results: dict[str, dict[str, Any]] = {}

    def review(family: str, rid: str, row: dict[str, Any]) -> list[str]:
        issues: list[str] = []
        if family == "entities":
            if row.get("country_code") != "AE" or row.get("status") != "current":
                issues.append("entity country/status mismatch")
            if rid == "ENT-AE-COUNTRY":
                if row.get("entity_type") != "country":
                    issues.append("country type mismatch")
            elif row.get("entity_type") != expected_type.get(rid) or actual_parent.get(rid) != expected_parent.get(rid):
                issues.append("contextual type or profile parent mismatch")
            if row.get("canonical_source_id") not in sources or not row.get("source_locator"):
                issues.append("entity source/locator missing")
        elif family == "aliases":
            if row.get("entity_id") not in entity_ids or row.get("source_id") not in sources or not row.get("source_locator"):
                issues.append("alias entity/source/locator mismatch")
            if row.get("kind") in {"historical", "former"} and row.get("status") == "current":
                issues.append("historical alias marked current")
        elif family == "relationships":
            if row.get("child_id") not in entity_ids or row.get("parent_id") not in entity_ids:
                issues.append("relationship endpoint missing")
            if row.get("relationship_type") != "administrative_parent" or expected_parent.get(row.get("child_id")) != row.get("parent_id"):
                issues.append("relationship profile mismatch")
            if row.get("source_id") not in sources or not row.get("source_locator"):
                issues.append("relationship evidence missing")
        elif family in {"claims", "cultural_claims", "dialect_claims"}:
            if row.get("subject_id") not in entity_ids or row.get("source_id") not in sources or not row.get("source_locator"):
                issues.append("claim subject/source/locator mismatch")
            if not row.get("published") or row.get("verification_status") not in {"verified", "source_verified"}:
                issues.append("claim is not publishable")
            if row.get("sensitivity") == "sensitive" and row.get("status") != "disputed" and row.get("second_source_id") == row.get("source_id"):
                issues.append("sensitive claim sources are not independent")
            if family == "cultural_claims" and row.get("classification") not in {"national", "emirate_specific", "regional", "local", "shared", "historical", "official", "popular", "disputed"}:
                issues.append("cultural scope classification missing")
            if family == "dialect_claims":
                context = row.get("lexical_context") or {}
                required = ("language", "variety", "place_id", "form", "meaning", "register", "study_date")
                if row.get("predicate") != "lexical_form" or not all(context.get(field) for field in required):
                    issues.append("dialect context incomplete")
                if row.get("value", {}).get("data") in {"وايد", "شو"} and row.get("classification") != "regional":
                    issues.append("shared Gulf/Levantine form mislabeled")
        elif family == "sources":
            required = ("title", "publisher", "url", "retrieved_at", "license", "language", "locator", "checksum", "quality_tier")
            if not all(row.get(field) for field in required):
                issues.append("atomic source metadata incomplete")
            if row.get("country_codes") and "AE" not in row.get("country_codes"):
                issues.append("foreign-only source sampled")
        elif family == "denominators":
            if row.get("source_id") not in sources or row.get("snapshot_date") != "2026-08-15" or not row.get("license"):
                issues.append("denominator date/source/license missing")
            if row.get("denominator") is None and (row.get("status") != "unavailable" or not row.get("missing_reason")):
                issues.append("unavailable denominator lacks reason")
        elif family == "coverage":
            den = den_by_id.get(row.get("denominator_id"))
            if not den or row.get("source_id") != den.get("source_id"):
                issues.append("coverage denominator/source mismatch")
            elif den.get("denominator") is None:
                if row.get("coverage_percentage") is not None or row.get("complete"):
                    issues.append("unavailable layer has percentage/completeness")
            elif row.get("matched") + row.get("excluded") != den.get("denominator") or row.get("unmatched") != 0:
                issues.append("closed coverage does not balance")
        return issues

    for family, plan in sample_plan["families"].items():
        population = families[family]
        sampled_ids = plan["record_ids"]
        passed = 0
        for rid in sampled_ids:
            row = population.get(rid)
            issues = ["sampled record missing"] if row is None else review(family, rid, row)
            if issues:
                for issue in issues:
                    findings.append({"severity": "P1", "family": family, "record_id": rid, "message": issue})
            else:
                passed += 1
        minimum_met = plan["sample_size"] >= plan["minimum_required"] and plan["sample_size"] == len(sampled_ids)
        if not minimum_met:
            findings.append({"severity": "P1", "family": family, "record_id": "sample-plan", "message": "sample is below ceil(10%)"})
        family_results[family] = {
            "population": plan["population"],
            "minimum_required": plan["minimum_required"],
            "sampled": len(sampled_ids),
            "sample_percentage": plan["sample_percentage"],
            "passed": passed,
            "failed": len(sampled_ids) - passed,
            "status": "PASS" if minimum_met and passed == len(sampled_ids) else "FAIL",
        }
        print(f"[{family_results[family]['status']}] {family}: {passed}/{len(sampled_ids)} sampled records passed")

    p0 = sum(row["severity"] == "P0" for row in findings)
    p1 = sum(row["severity"] == "P1" for row in findings)
    report = {
        "schema_version": "1.0.0",
        "country_code": "AE",
        "snapshot_date": "2026-08-15",
        "method": "Independent deterministic ID samples reviewed directly against canonical records, manifest profiles, sources, and coverage; this reviewer does not import or call scripts/import_uae_phase5.py.",
        "status": "PASS" if not findings else "FAIL",
        "families": family_results,
        "total_sampled": sum(row["sampled"] for row in family_results.values()),
        "total_passed": sum(row["passed"] for row in family_results.values()),
        "p0": p0,
        "critical_p1": p1,
        "findings": findings,
    }
    write_json(REPORT, report)
    print(f"Independent UAE review: {report['total_passed']}/{report['total_sampled']} passed; P0={p0}; critical P1={p1}.")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
