#!/usr/bin/env python3
"""Required Qatar production mutations: base layer plus depth cycle 1."""
import copy

from model import ROOT, write_json
from validate_qatar import data, validate


def main():
    b = data()
    o = []

    def r(n, fn, c):
        d = copy.deepcopy(b)
        fn(d)
        e = validate(d)
        o.append({"mutation": n, "expected_code": c, "detected": any(x["code"] == c for x in e)})

    def depth(d, predicate=None, name=None):
        for row in d["claims"]:
            if not str(row["id"]).startswith("CLM-QA-DEPTH"):
                continue
            if predicate and row["predicate"] != predicate:
                continue
            if name and row["value"]["data"].get("name") != name:
                continue
            return row
        raise AssertionError("fixture depth claim missing")

    def place(d, entity_type="quarter"):
        return next(r for r in d["entities"] if r["entity_type"] == entity_type)

    r("QA_WRONG_PARENT", lambda d: next(x for x in d["relationships"] if x["child_id"].startswith("ENT-QA-MUNICIPALITY")).update(parent_id="ENT-QA-MUNICIPALITY-DOHA"), "QA_WRONG_PARENT")
    r("QA_ZONE_AS_MUNICIPALITY", lambda d: d["entities"].append({**d["entities"][-1], "id": "ENT-QA-MUNICIPALITY-ZONE-1", "entity_type": "qa_municipality"}), "QA_ENTITY_UNIVERSE")
    r("QA_HISTORICAL_TEN_CURRENT", lambda d: d["entities"].extend([{**d["entities"][-1], "id": "ENT-QA-MUNICIPALITY-OLD-A"}, {**d["entities"][-1], "id": "ENT-QA-MUNICIPALITY-OLD-B"}]), "QA_ENTITY_UNIVERSE")
    r("QA_POPULATION_TAMPER", lambda d: next(x for x in d["claims"] if x["predicate"] == "population")["value"].update(data=1), "QA_POPULATION")
    r("QA_UNDATED", lambda d: next(x for x in d["claims"] if x["predicate"] == "population").update(observed_at=None), "QA_POPULATION")
    r("QA_CITY_LEAKAGE", lambda d: d["claims"].append({**d["claims"][-1], "id": "CLM-QA-MUT", "subject_id": "ENT-QA-MUNICIPALITY-DOHA", "predicate": "city_status"}), "QA_CITY_LEAKAGE")
    r("QA_DIALECT_LEXICAL_PREDICATE", lambda d: d["claims"].append({**d["claims"][-1], "id": "CLM-QA-DIA", "predicate": "lexical_form"}), "QA_DIALECT")
    r("QA_LOWER_DENOMINATOR", lambda d: next(x for x in d["manifest"]["hierarchy"] if x["entity_type"] == "qa_zone").update(denominator=98, scope_status="closed"), "QA_LOWER_LAYER")
    r("QA_DEPTH_PUBLISHED_FROM_WEAK", lambda d: depth(d, "food_dish", "الألبة").update(published=True), "QA_DEPTH_PUBLISHED_FROM_WEAK")
    r("QA_DIALECT_PROMOTED", lambda d: depth(d, "dialect_profile").update(verification_status="verified", confidence="high"), "QA_DEPTH_CONTRACT")
    r("QA_SHARED_NOT_EXCLUSIVE", lambda d: depth(d, "food_dish", "المجبوس").update(classification="national"), "QA_SHARED_NOT_EXCLUSIVE")
    r("QA_ICH_UNPUBLISHED", lambda d: depth(d, "intangible_cultural_practice").update(published=False), "QA_ICH_CONTRACT")
    r("QA_ICH_NOT_SHARED", lambda d: depth(d, "intangible_cultural_practice").update(classification="national"), "QA_ICH_CONTRACT")
    r("QA_ICH_LAYER_DENOMINATOR", lambda d: next(l for l in d["manifest"]["pilot_layers"] if l["layer"] == "unesco_intangible_heritage").update(denominator=9, coverage_record_id="COV-QA-ICH"), "QA_ICH_LAYER")
    r("QA_HERITAGE_LAYER_DENOMINATOR", lambda d: next(l for l in d["manifest"]["pilot_layers"] if l["layer"] == "old_doha_places").update(denominator=4, coverage_record_id="COV-QA-OLD-DOHA"), "QA_HERITAGE_LAYER")
    r("QA_PLACE_AS_CURRENT", lambda d: place(d).update(status="current"), "QA_PLACE_CONTRACT")
    r("QA_PLACE_ADMIN_PARENT", lambda d: d["relationships"].append({**d["relationships"][0], "id": "REL-QA-MUT-PARENT", "child_id": place(d)["id"], "parent_id": "ENT-QA-MUNICIPALITY-AL-RAYYAN", "relationship_type": "administrative_parent"}), "QA_PLACE_LOCATED_IN")
    r("QA_PLACE_WRONG_MUNICIPALITY", lambda d: next(x for x in d["relationships"] if x["child_id"] == place(d)["id"]).update(parent_id="ENT-QA-MUNICIPALITY-AL-WAKRA"), "QA_PLACE_LOCATED_IN")
    r("QA_PLACE_POPULATION", lambda d: d["claims"].append({**depth(d, "food_dish"), "id": "CLM-QA-MUT-POP", "subject_id": place(d)["id"], "predicate": "population", "value": {"type": "integer", "data": 500}}), "QA_PLACE_POPULATION")
    r("QA_PLACE_SOURCE_UPGRADE", lambda d: place(d).update(canonical_source_id="SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020", verification_status="source_verified"), "QA_PLACE_CONTRACT")
    r("QA_UNSOURCED_LANGUAGE", lambda d: d["claims"].append({**depth(d, "food_dish"), "id": "CLM-QA-MUT-LANG", "predicate": "language_presence", "value": {"type": "json", "data": {"language": "الإنجليزية"}}, "classification": "regional"}), "QA_LANGUAGE_UNSUPPORTED")
    r("QA_SOURCE_TIER_INFLATION", lambda d: next(x for x in d["sources"] if x["id"] == "SRC-QA-SOUQ-WAQIF-2012").update(quality_tier="A"), "QA_SOURCES")
    r("QA_DIALECT_WITHOUT_GLOSS", lambda d: depth(d, "dialect_profile")["value"]["data"]["sample_words"].__setitem__(0, ["شلونك"]), "QA_DIALECT_GLOSS")

    ok = all(x["detected"] for x in o)
    write_json(ROOT / "reports/qatar_negative_tests.json", {"schema_version": "2.0.0", "country_code": "QA", "status": "PASS" if ok else "FAIL", "required": len(o), "detected": sum(x["detected"] for x in o), "mutations": o})
    for row in o:
        print(f"[{'PASS' if row['detected'] else 'FAIL'}] {row['mutation']} -> {row['expected_code']}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
