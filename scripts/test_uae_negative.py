#!/usr/bin/env python3
"""Run the eight required in-memory UAE semantic mutations."""

from __future__ import annotations

import copy
from typing import Any, Callable

from model import ROOT, write_json
from validate_uae import load_bundle, validate_bundle

REPORT = ROOT / "reports/uae_negative_tests.json"
Mutation = Callable[[dict[str, Any]], None]


def relationship(bundle: dict[str, Any], child_id: str) -> dict[str, Any]:
    return next(row for row in bundle["relationships"] if row.get("child_id") == child_id and row.get("relationship_type") == "administrative_parent")


def wrong_emirate_parent(bundle: dict[str, Any]) -> None:
    relationship(bundle, "ENT-AE-ABU-DHABI-MUNICIPALITY")["parent_id"] = "ENT-AE-EMIRATE-DUBAI"


def wrong_local_type(bundle: dict[str, Any]) -> None:
    entity = next(row for row in bundle["entities"] if row["id"] == "ENT-AE-ABU-DHABI-MUNICIPALITY")
    entity["entity_type"] = "ae_dubai_planning_sector"


def alias_as_entity(bundle: dict[str, Any]) -> None:
    template = next(row for row in bundle["entities"] if row["id"] == "ENT-AE-MASFOUT-CONSTITUENT")
    duplicate = copy.deepcopy(template)
    duplicate["id"] = "ENT-AE-ALIAS-AS-ENTITY-MASFOUT"
    duplicate["canonical_name"] = "مصفوت"
    duplicate["canonical_name_language"] = "ar"
    bundle["entities"].append(duplicate)
    rel = copy.deepcopy(relationship(bundle, "ENT-AE-MASFOUT-CONSTITUENT"))
    rel["id"] = "REL-AE-MUTANT-ALIAS-AS-ENTITY"
    rel["child_id"] = duplicate["id"]
    bundle["relationships"].append(rel)


def shared_food_as_exclusive(bundle: dict[str, Any]) -> None:
    claim = next(row for row in bundle["claims"] if row.get("predicate") == "food_culture" and row.get("classification") == "shared")
    claim["predicate"] = "food_exclusive_origin"
    claim["classification"] = "national"
    claim["value"] = {"type": "string", "data": "Khameer is exclusive to the UAE."}


def national_claim_as_local(bundle: dict[str, Any]) -> None:
    claim = next(row for row in bundle["claims"] if row.get("predicate") == "food_culture" and row.get("classification") == "national")
    claim["subject_id"] = "ENT-AE-EMIRATE-AJMAN"
    claim["classification"] = "local"


def historic_as_current(bundle: dict[str, Any]) -> None:
    alias = next(row for row in bundle["aliases"] if row.get("name") == "Julfar")
    alias["status"] = "current"


def same_name_different_parent_collapse(bundle: dict[str, Any]) -> None:
    # Simulate wrongly merging Fujairah's Dibba authority into Sharjah's differently parented Dibba Al Hisn identity.
    dropped = "ENT-AE-DIBBA-MUNICIPALITY"
    kept = "ENT-AE-DIBBA-AL-HISN-MUNICIPALITY"
    bundle["entities"] = [row for row in bundle["entities"] if row["id"] != dropped]
    for row in bundle["relationships"]:
        if row.get("child_id") == dropped:
            row["child_id"] = kept
    bundle["aliases"] = [row for row in bundle["aliases"] if row.get("entity_id") != dropped]
    bundle["claims"] = [row for row in bundle["claims"] if row.get("subject_id") != dropped]


def foreign_source(bundle: dict[str, Any]) -> None:
    foreign_id = next(sid for sid, source in bundle["sources"].items() if source.get("country_codes") == ["SA"])
    claim = next(row for row in bundle["claims"] if row.get("predicate") == "jurisdiction_semantics")
    claim["source_id"] = foreign_id


MUTATIONS: list[tuple[str, str, Mutation]] = [
    ("UAE_WRONG_EMIRATE_PARENT", "UAE_PARENT_PROFILE", wrong_emirate_parent),
    ("UAE_WRONG_LOCAL_TYPE", "UAE_LOCAL_TYPE", wrong_local_type),
    ("UAE_ALIAS_AS_ENTITY", "UAE_ALIAS_ENTITY", alias_as_entity),
    ("UAE_SHARED_FOOD_AS_EXCLUSIVE", "UAE_EXCLUSIVITY", shared_food_as_exclusive),
    ("UAE_NATIONAL_CLAIM_AS_LOCAL", "UAE_NATIONAL_SCOPE", national_claim_as_local),
    ("UAE_HISTORIC_AS_CURRENT", "UAE_TEMPORAL_STATUS", historic_as_current),
    ("UAE_SAME_NAME_DIFFERENT_PARENT", "UAE_IDENTITY_COLLAPSE", same_name_different_parent_collapse),
    ("UAE_FOREIGN_SOURCE", "UAE_FOREIGN_SOURCE", foreign_source),
]


def main() -> int:
    baseline = load_bundle()
    baseline_result = validate_bundle(copy.deepcopy(baseline))
    if baseline_result["status"] != "PASS":
        raise SystemExit("baseline UAE data must pass before mutation testing")

    outcomes = []
    for name, expected_code, mutate in MUTATIONS:
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        result = validate_bundle(candidate)
        codes = sorted({row["code"] for row in result["errors"]})
        detected = result["status"] == "FAIL" and expected_code in codes
        outcomes.append({"mutation": name, "expected_error_code": expected_code, "detected": detected, "observed_error_codes": codes})
        print(f"[{'PASS' if detected else 'FAIL'}] {name}: expected {expected_code}; observed {codes}")

    report = {
        "schema_version": "2.0.0",
        "country_code": "AE",
        "snapshot_date": "2026-08-15",
        "status": "PASS" if all(row["detected"] for row in outcomes) else "FAIL",
        "baseline_status": baseline_result["status"],
        "required": len(MUTATIONS),
        "detected": sum(row["detected"] for row in outcomes),
        "mutations": outcomes,
    }
    write_json(REPORT, report)
    print(f"UAE negative tests: {report['detected']}/{report['required']} required mutations detected.")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
