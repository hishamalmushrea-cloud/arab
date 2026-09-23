#!/usr/bin/env python3
"""Run the required in-memory UAE semantic mutations for the pilot and its depth cycle."""

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


def depth_claim(bundle: dict[str, Any], predicate: str) -> dict[str, Any]:
    return next(row for row in bundle["claims"] if row.get("predicate") == predicate and str(row.get("id", "")).startswith("CLM-AE-DEPTH"))


def shared_element_as_national(bundle: dict[str, Any]) -> None:
    claim = next(row for row in bundle["claims"] if row.get("predicate") == "intangible_cultural_practice" and row.get("classification") == "shared")
    claim["classification"] = "national"


def deferred_file_scope_invented(bundle: dict[str, Any]) -> None:
    claim = depth_claim(bundle, "unesco_element_deferred_file")
    claim["classification"] = "national"


def deferred_file_published(bundle: dict[str, Any]) -> None:
    claim = depth_claim(bundle, "unesco_element_deferred_file")
    claim["published"] = True
    claim["verification_status"] = "verified"
    claim["confidence"] = "high"


def register_programme_as_element(bundle: dict[str, Any]) -> None:
    depth_claim(bundle, "unesco_safeguarding_programme")["predicate"] = "intangible_cultural_practice"


def pending_nomination_dropped(bundle: dict[str, Any]) -> None:
    target = depth_claim(bundle, "unesco_pending_nomination")
    bundle["claims"] = [row for row in bundle["claims"] if row.get("id") != target["id"]]


def depth_claim_dropped(bundle: dict[str, Any]) -> None:
    bundle["claims"] = [row for row in bundle["claims"] if row.get("id") != depth_claim(bundle, "craft_custom")["id"]]


def criteria_filled_in(bundle: dict[str, Any]) -> None:
    properties = [row for row in bundle["claims"] if row.get("predicate") == "world_heritage_property"]
    properties[0]["value"]["data"]["criteria"] = "(iii)"


def tentative_file_duplicated(bundle: dict[str, Any]) -> None:
    tentative = [row for row in bundle["claims"] if row.get("predicate") == "unesco_tentative_listing"]
    tentative[1]["value"]["data"]["reference"] = tentative[0]["value"]["data"]["reference"]


def inscribed_count_duplicated(bundle: dict[str, Any]) -> None:
    template = next(row for row in bundle["claims"] if row.get("predicate") == "world_heritage_property")
    duplicate = copy.deepcopy(template)
    duplicate["id"] = "CLM-AE-DEPTH-MUTANT-INSCRIBED-COUNT"
    duplicate["predicate"] = "world_heritage_inscribed_count"
    duplicate["value"] = {"type": "integer", "data": 3}
    bundle["claims"].append(duplicate)


def dish_number_injected(bundle: dict[str, Any]) -> None:
    dish = depth_claim(bundle, "food_dish")
    dish["value"]["data"]["population"] = "12"


def weak_source_published(bundle: dict[str, Any]) -> None:
    claim = next(row for row in bundle["claims"] if row.get("predicate") == "craft_custom")
    claim["published"] = True
    claim["verification_status"] = "verified"
    claim["confidence"] = "high"


def place_coordinates_injected(bundle: dict[str, Any]) -> None:
    place = next(row for row in bundle["entities"] if row["id"] == "ENT-AE-SITE-AL-AIN")
    place["coordinates"] = {"latitude": 24.2, "longitude": 55.7, "source_id": place["canonical_source_id"]}


def place_second_parent(bundle: dict[str, Any]) -> None:
    template = next(row for row in bundle["relationships"] if row.get("child_id") == "ENT-AE-SITE-FAYA")
    duplicate = copy.deepcopy(template)
    duplicate["id"] = "REL-AE-MUTANT-PLACE-SECOND-PARENT"
    duplicate["parent_id"] = "ENT-AE-EMIRATE-SHARJAH"
    bundle["relationships"].append(duplicate)


def place_bearing_claim(bundle: dict[str, Any]) -> None:
    template = next(row for row in bundle["claims"] if row.get("predicate") == "food_dish")
    duplicate = copy.deepcopy(template)
    duplicate["id"] = "CLM-AE-DEPTH-MUTANT-PLACE-CLAIM"
    duplicate["subject_id"] = "ENT-AE-SITE-WURAYAH"
    bundle["claims"].append(duplicate)


def pilot_snapshot_merged(bundle: dict[str, Any]) -> None:
    bundle["snapshots"] = [row for row in bundle["snapshots"] if not str(row.get("id", "")).startswith("SNP-AE-PILOT-")]


def depth_source_downgraded(bundle: dict[str, Any]) -> None:
    bundle["sources"]["SRC-UNESCO-WH-AE-STATE-2026"]["quality_tier"] = "E"


def depth_layer_denominator_removed(bundle: dict[str, Any]) -> None:
    layer = next(row for row in bundle["manifest"]["pilot_layers"] if row.get("layer") == "heritage_places")
    layer["denominator_id"] = None


def depth_layer_total_shifted(bundle: dict[str, Any]) -> None:
    layer = next(row for row in bundle["manifest"]["pilot_layers"] if row.get("layer") == "unesco_intangible_heritage")
    layer["denominator"] = 20


def natural_place_retyped(bundle: dict[str, Any]) -> None:
    next(row for row in bundle["entities"] if row["id"] == "ENT-AE-SITE-WURAYAH")["entity_type"] = "cultural_site"


MUTATIONS: list[tuple[str, str, Mutation]] = [
    ("UAE_WRONG_EMIRATE_PARENT", "UAE_PARENT_PROFILE", wrong_emirate_parent),
    ("UAE_WRONG_LOCAL_TYPE", "UAE_LOCAL_TYPE", wrong_local_type),
    ("UAE_ALIAS_AS_ENTITY", "UAE_ALIAS_ENTITY", alias_as_entity),
    ("UAE_SHARED_FOOD_AS_EXCLUSIVE", "UAE_EXCLUSIVITY", shared_food_as_exclusive),
    ("UAE_NATIONAL_CLAIM_AS_LOCAL", "UAE_NATIONAL_SCOPE", national_claim_as_local),
    ("UAE_HISTORIC_AS_CURRENT", "UAE_TEMPORAL_STATUS", historic_as_current),
    ("UAE_SAME_NAME_DIFFERENT_PARENT", "UAE_IDENTITY_COLLAPSE", same_name_different_parent_collapse),
    ("UAE_FOREIGN_SOURCE", "UAE_FOREIGN_SOURCE", foreign_source),
    ("UAE_DEPTH_SHARED_AS_NATIONAL", "UAE_DEPTH_ELEMENT_SCOPE", shared_element_as_national),
    ("UAE_DEPTH_DEFERRED_SCOPE_INVENTED", "UAE_DEPTH_ELEMENT_SCOPE", deferred_file_scope_invented),
    ("UAE_DEPTH_DEFERRED_PUBLISHED", "UAE_DEPTH_ELEMENT_SCOPE", deferred_file_published),
    ("UAE_DEPTH_REGISTER_AS_ELEMENT", "UAE_DEPTH_ELEMENT_SCOPE", register_programme_as_element),
    ("UAE_DEPTH_PENDING_DROPPED", "UAE_DEPTH_ELEMENT_SCOPE", pending_nomination_dropped),
    ("UAE_DEPTH_CLAIM_DROPPED", "UAE_DEPTH_CLAIMS", depth_claim_dropped),
    ("UAE_DEPTH_CRITERIA_FILLED", "UAE_DEPTH_WH", criteria_filled_in),
    ("UAE_DEPTH_TENTATIVE_DUPLICATED", "UAE_DEPTH_WH", tentative_file_duplicated),
    ("UAE_DEPTH_INSCRIBED_COUNT", "UAE_DEPTH_WH", inscribed_count_duplicated),
    ("UAE_DEPTH_DISH_NUMBER", "UAE_DEPTH_NO_COUNTS", dish_number_injected),
    ("UAE_DEPTH_WEAK_PUBLISHED", "UAE_DEPTH_PUBLICATION", weak_source_published),
    ("UAE_DEPTH_PLACE_COORDINATES", "UAE_DEPTH_PLACE_SHAPE", place_coordinates_injected),
    ("UAE_DEPTH_PLACE_SECOND_PARENT", "UAE_DEPTH_PLACE_SHAPE", place_second_parent),
    ("UAE_DEPTH_PLACE_CLAIM", "UAE_DEPTH_PLACE_SHAPE", place_bearing_claim),
    ("UAE_DEPTH_PLACE_RETYPED", "UAE_DEPTH_PLACE_SHAPE", natural_place_retyped),
    ("UAE_DEPTH_PILOT_SNAPSHOT_MERGED", "UAE_DEPTH_SNAPSHOT", pilot_snapshot_merged),
    ("UAE_DEPTH_SOURCE_DOWNGRADED", "UAE_DEPTH_SOURCES", depth_source_downgraded),
    ("UAE_DEPTH_LAYER_DENOMINATOR", "UAE_DEPTH_LAYERS", depth_layer_denominator_removed),
    ("UAE_DEPTH_LAYER_TOTAL", "UAE_DEPTH_LAYERS", depth_layer_total_shifted),
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
        "depth_snapshot_date": "2026-09-23",
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
