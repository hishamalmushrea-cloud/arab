#!/usr/bin/env python3
"""Required Bahrain production mutations; every risk must be detected."""
from __future__ import annotations

import copy
import json

from model import ROOT, write_json
from validate_bahrain import load_data, validate_data


def main() -> int:
    base = load_data()
    mutations = []

    def run(name, mutate, expected_code):
        candidate = copy.deepcopy(base)
        mutate(candidate)
        errors = validate_data(candidate)
        detected = any(row["code"] == expected_code for row in errors)
        mutations.append({"mutation": name, "expected_code": expected_code, "detected": detected, "error_count": len(errors)})

    run("BH_WRONG_GOVERNORATE_PARENT",
        lambda d: next(r for r in d["relationships"] if r["child_id"] == "ENT-BH-GOVERNORATE-CAPITAL").update(parent_id="ENT-BH-GOVERNORATE-MUHARRAQ"),
        "BH_WRONG_PARENT")
    run("BH_WRONG_GOVERNORATE_TYPE",
        lambda d: next(r for r in d["entities"] if r["id"] == "ENT-BH-GOVERNORATE-CAPITAL").update(entity_type="bh_area"),
        "BH_GOVERNORATE_IDENTITY")
    run("BH_HISTORICAL_CENTRAL_AS_CURRENT",
        lambda d: d["entities"].append({**next(r for r in d["entities"] if r["id"] == "ENT-BH-GOVERNORATE-CAPITAL"), "id": "ENT-BH-GOVERNORATE-CENTRAL", "canonical_name": "الوسطى"}),
        "BH_HISTORICAL_AS_CURRENT")
    run("BH_CULTURAL_LEAKAGE_TO_GOVERNORATE",
        lambda d: d["claims"].append({**d["claims"][-1], "id": "CLM-BH-MUT-CULTURE", "subject_id": "ENT-BH-GOVERNORATE-CAPITAL", "predicate": "heritage_route_extent"}),
        "BH_CULTURAL_LEAKAGE")
    run("BH_UNSUPPORTED_DIALECT_CLAIM",
        lambda d: d["claims"].append({**d["claims"][-1], "id": "CLM-BH-MUT-DIALECT", "predicate": "lexical_form"}),
        "BH_UNSUPPORTED_DIALECT")
    run("BH_FOREIGN_SOURCE",
        lambda d: next(r for r in d["claims"] if r["predicate"] == "area").update(source_id="SRC-AE-FEDERAL-SEVEN-EMIRATES-2026"),
        "BH_CLAIM_SOURCE")
    run("BH_WHC_DENOMINATOR_INFLATION",
        lambda d: next(r for r in d["denominators"] if r["id"] == "DEN-BH-WHC-20260816").update(value=9, denominator=9),
        "BH_DENOMINATORS")
    run("BH_ALIAS_AS_ENTITY",
        lambda d: d["entities"].append({**next(r for r in d["entities"] if r["id"] == "ENT-BH-GOVERNORATE-CAPITAL"), "id": "ENT-BH-CITY-CAPITAL-ALIAS"}),
        "BH_ENTITY_UNIVERSE")
    run("BH_AREA_VALUE_TAMPER",
        lambda d: next(r for r in d["claims"] if r["subject_id"] == "ENT-BH-GOVERNORATE-NORTHERN" and r["predicate"] == "area")["value"].update(data=999),
        "BH_AREA_VALUE")

    passed = all(row["detected"] for row in mutations)
    report = {"schema_version": "2.0.0", "country_code": "BH", "status": "PASS" if passed else "FAIL", "required": len(mutations), "detected": sum(row["detected"] for row in mutations), "mutations": mutations}
    write_json(ROOT / "reports/bahrain_negative_tests.json", report)
    for row in mutations: print(f"[{'PASS' if row['detected'] else 'FAIL'}] {row['mutation']} -> {row['expected_code']}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
