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
    def depth(d, predicate=None, name=None):
        for row in d["claims"]:
            if not str(row["id"]).startswith("CLM-BH-DEPTH"):
                continue
            if predicate and row["predicate"] != predicate:
                continue
            if name and row["value"]["data"].get("name") != name:
                continue
            return row
        raise AssertionError("fixture depth claim missing")

    def place(d, entity_type="quarter"):
        return next(r for r in d["entities"] if r["entity_type"] == entity_type)

    run("BH_AREA_VALUE_TAMPER",
        lambda d: next(r for r in d["claims"] if r["subject_id"] == "ENT-BH-GOVERNORATE-NORTHERN" and r["predicate"] == "area")["value"].update(data=999),
        "BH_AREA_VALUE")

    run("BH_DEPTH_PUBLISHED_FROM_WEAK",
        lambda d: depth(d, "food_dish", "المحمر").update(published=True),
        "BH_DEPTH_PUBLISHED_FROM_WEAK")
    run("BH_DIALECT_PROMOTED_TO_VERIFIED",
        lambda d: depth(d, "dialect_profile").update(verification_status="verified", confidence="high"),
        "BH_DEPTH_CONTRACT")
    run("BH_SHARED_NOT_EXCLUSIVE",
        lambda d: depth(d, "food_dish", "المموش").update(classification="national"),
        "BH_SHARED_NOT_EXCLUSIVE")
    run("BH_ICH_UNPUBLISHED",
        lambda d: depth(d, "intangible_cultural_practice").update(published=False),
        "BH_ICH_CONTRACT")
    run("BH_ICH_LAYER_DENOMINATOR",
        lambda d: next(l for l in d["manifest"]["pilot_layers"] if l["layer"] == "unesco_intangible_heritage").update(denominator=7),
        "BH_ICH_LAYER")
    run("BH_HERITAGE_LAYER_DENOMINATOR",
        lambda d: next(l for l in d["manifest"]["pilot_layers"] if l["layer"] == "muharraq_heritage_places").update(denominator=23, coverage_record_id="COV-BH-HERITAGE"),
        "BH_HERITAGE_LAYER_DENOMINATOR")
    run("BH_FIRIJ_AS_CURRENT",
        lambda d: place(d).update(status="current"),
        "BH_PLACE_CONTRACT")
    run("BH_FIRIJ_ADMIN_PARENT",
        lambda d: d["relationships"].append({**d["relationships"][0], "id": "REL-BH-MUT-PARENT",
                                             "child_id": place(d)["id"], "parent_id": "ENT-BH-GOVERNORATE-MUHARRAQ",
                                             "relationship_type": "administrative_parent"}),
        "BH_PLACE_ADMIN_PARENT")
    run("BH_PLACE_POPULATION",
        lambda d: d["claims"].append({**depth(d, "food_dish"), "id": "CLM-BH-MUT-POP",
                                      "subject_id": place(d)["id"], "predicate": "population",
                                      "value": {"type": "integer", "data": 1000}}),
        "BH_PLACE_POPULATION")
    run("BH_PLACE_SOURCE_UPGRADE",
        lambda d: place(d).update(canonical_source_id="SRC-BH-SLRB-GOVERNORATE-AREA-2024", verification_status="source_verified"),
        "BH_PLACE_CONTRACT")
    run("BH_SOURCE_TIER_INFLATION",
        lambda d: next(r for r in d["sources"] if r["id"] == "SRC-BH-CUISINE-MIRROR-2026").update(quality_tier="A"),
        "BH_SOURCE_CATALOG")
    run("BH_DIALECT_WITHOUT_GLOSS",
        lambda d: depth(d, "dialect_profile")["value"]["data"]["sample_words"].__setitem__(0, ["خلق"]),
        "BH_DIALECT_GLOSS")

    passed = all(row["detected"] for row in mutations)
    report = {"schema_version": "2.0.0", "country_code": "BH", "status": "PASS" if passed else "FAIL", "required": len(mutations), "detected": sum(row["detected"] for row in mutations), "mutations": mutations}
    write_json(ROOT / "reports/bahrain_negative_tests.json", report)
    for row in mutations: print(f"[{'PASS' if row['detected'] else 'FAIL'}] {row['mutation']} -> {row['expected_code']}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
