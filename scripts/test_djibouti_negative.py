#!/usr/bin/env python3
"""Required Djibouti mutations: accepted topology plus depth cycle 1."""
import copy

from model import ROOT, write_json
from validate_djibouti import data, validate


def main():
    b = data()
    o = []

    def r(n, fn, c):
        d = copy.deepcopy(b)
        fn(d)
        o.append({"mutation": n, "expected_code": c, "detected": any(x["code"] == c for x in validate(d))})

    def depth(d, pred, key=None, val=None):
        for row in d["claims"]:
            if not str(row["id"]).startswith("CLM-DJ-DEPTH") or row["predicate"] != pred:
                continue
            payload = row["value"]["data"]
            if key and (payload.get(key) if not isinstance(payload, dict) else payload.get(key)) != val:
                continue
            return row
        raise AssertionError(f"depth claim missing: {pred}")

    def place(d, token):
        return next(x for x in d["entities"] if x["id"].endswith("-" + token))

    # Accepted-layer mutations (kept from the surface cycle).
    r("DJ_CITY_AS_REGION", lambda d: next(x for x in d["entities"] if x["id"] == "ENT-DJ-DJIBOUTI-CITY").update(entity_type="dj_region"), "DJ_COUNTS")
    r("DJ_COMMUNE_UNDER_REGION", lambda d: next(x for x in d["relationships"] if x["child_id"] == "ENT-DJ-COMMUNE-RAS-DIKA").update(parent_id="ENT-DJ-REGION-ARTA"), "DJ_COMMUNE_PATH")
    r("DJ_SUBPREF_UNDER_CITY", lambda d: next(x for x in d["relationships"] if x["child_id"].startswith("ENT-DJ-SUBPREFECTURE")).update(parent_id="ENT-DJ-DJIBOUTI-CITY"), "DJ_SUBPREFECTURE_PATH")
    r("DJ_DROP_REGION", lambda d: d["entities"].__setitem__(slice(None), [x for x in d["entities"] if x["id"] != "ENT-DJ-REGION-ARTA"]), "DJ_COUNTS")
    r("DJ_POP_TAMPER", lambda d: next(x for x in d["claims"] if x["subject_id"] == "ENT-DJ-REGION-ARTA" and x["predicate"] == "population")["value"].update(data=1), "DJ_POPULATION")
    r("DJ_POP_TOTAL", lambda d: next(x for x in d["claims"] if x["predicate"] == "population")["value"].update(data=1), "DJ_POP_RECONCILIATION")
    r("DJ_FAKE_COMMUNE_COUNT", lambda d: next(x for x in d["denominators"] if x["id"] == "DEN-DJ-CITY-COMMUNES").update(value=6), "DJ_DENOMINATORS")
    r("DJ_FAKE_SUBPREF_COUNT", lambda d: next(x for x in d["denominators"] if x["id"] == "DEN-DJ-SUBPREFECTURES").update(value=15), "DJ_DENOMINATORS")

    # Depth-cycle mutations.
    r("DJ_XEEDHO_NOT_NATIONAL", lambda d: depth(d, "intangible_cultural_practice", "reference", "02001").update(classification="shared"), "DJ_ICH_CONTRACT")
    r("DJ_XEEDHO_UNPUBLISHED", lambda d: depth(d, "intangible_cultural_practice", "reference", "02001").update(published=False), "DJ_ICH_CONTRACT")
    r("DJ_XEER_AS_NATIONAL", lambda d: depth(d, "intangible_cultural_practice", "reference", "02087").update(classification="national"), "DJ_ICH_CONTRACT")
    r("DJ_ZAFFA_STATES_LOST", lambda d: depth(d, "intangible_cultural_practice", "reference", "02283")["value"]["data"].update(co_states=["جيبوتي", "جزر القمر"]), "DJ_ICH_CONTRACT")
    r("DJ_ICH_WRONG_YEAR", lambda d: depth(d, "intangible_cultural_practice", "reference", "02087")["value"]["data"].update(year=2023), "DJ_ICH_CONTRACT")
    r("DJ_CONVENTION_DATE_LOST", lambda d: depth(d, "convention_ratification_date").update(published=False), "DJ_CONVENTION_CONTRACT")
    r("DJ_PENDING_AS_INSCRIBED", lambda d: depth(d, "unesco_pending_nomination").update(predicate="intangible_cultural_practice"), "DJ_DEPTH_COUNTS")
    r("DJ_PENDING_UNPUBLISHED", lambda d: depth(d, "unesco_pending_nomination").update(published=False), "DJ_PENDING_NOMINATION")
    r("DJ_CONSTITUTION_ARTICLE_LOST", lambda d: d["claims"].__setitem__(slice(None), [x for x in d["claims"] if not (x["predicate"] == "constitutional_provision" and str(x["value"]["data"].get("article")) == "2")]), "DJ_CONSTITUTION_CONTRACT")
    r("DJ_CONSTITUTION_UNPUBLISHED", lambda d: next(x for x in d["claims"] if x["predicate"] == "constitutional_provision").update(published=False), "DJ_CONSTITUTION_CONTRACT")
    r("DJ_OFFICIAL_LANGUAGE_UNPUBLISHED", lambda d: depth(d, "language_presence", "name", "العربية").update(published=False), "DJ_LANGUAGE_CONTRACT")
    r("DJ_MINORITY_PUBLISHED", lambda d: depth(d, "language_presence", "name", "الصومالية").update(published=True, verification_status="verified"), "DJ_LANGUAGE_CONTRACT")
    r("DJ_ISO_CODE_LOST", lambda d: depth(d, "language_presence", "name", "العفرية")["value"]["data"].update(iso_codes=[]), "DJ_LANGUAGE_CONTRACT")
    r("DJ_ISO_SOURCE_LOST", lambda d: depth(d, "language_presence", "name", "الصومالية").update(second_source_id=None, second_source_locator=None), "DJ_LANGUAGE_CONTRACT")
    r("DJ_SIGN_LANGUAGE_ISO_CLAIMED", lambda d: depth(d, "language_presence", "level", "signed")["value"]["data"].update(iso_codes=["dgs"]), "DJ_LANGUAGE_CONTRACT")
    r("DJ_SIGN_LANGUAGE_PUBLISHED", lambda d: depth(d, "language_presence", "level", "signed").update(published=True), "DJ_LANGUAGE_CONTRACT")
    r("DJ_SPEAKER_SHARE", lambda d: depth(d, "language_presence", "name", "الصومالية").update(notes="عدد المتحدثين 524,000"), "DJ_NO_COUNTS")
    r("DJ_POPULATION_FIELD_ON_DEPTH", lambda d: depth(d, "food_dish")["value"]["data"].update(population=1200), "DJ_NO_COUNTS")
    r("DJ_SECOND_SOURCE_LOCATOR_LOST", lambda d: depth(d, "custom_practice", "name", "ليالي الزفاف السبع").update(second_source_locator=None), "DJ_SECOND_SOURCE_PAIR")
    r("DJ_SECOND_SOURCE_LOCATOR_ONLY", lambda d: depth(d, "language_presence", "name", "الصومالية").update(second_source_id=None), "DJ_SECOND_SOURCE_PAIR")
    r("DJ_WEAK_DEPTH_PUBLISHED", lambda d: depth(d, "food_dish", "name", "لاهوه").update(published=True), "DJ_WEAK_DEPTH_PUBLISHED")
    r("DJ_FOLK_AS_FACT", lambda d: depth(d, "custom_practice", "name", "برد الأسنان الأمامية بالمبرد الحديدي").update(verification_status="verified"), "DJ_FOLK_NARRATIVE")
    r("DJ_FOLK_PUBLISHED", lambda d: depth(d, "custom_practice", "name", "برد الأسنان الأمامية بالمبرد الحديدي").update(published=True), "DJ_FOLK_NARRATIVE")
    r("DJ_DISCREPANCY_ACCEPTED_BADLY", lambda d: depth(d, "administrative_counts_discrepancy")["value"]["data"].update(accepted_value=35), "DJ_DISCREPANCY")
    r("DJ_DISCREPANCY_PUBLISHED", lambda d: depth(d, "administrative_counts_discrepancy").update(published=True, verification_status="verified"), "DJ_DISCREPANCY")
    r("DJ_PLACE_AS_CURRENT", lambda d: place(d, "BALBALA-Q").update(status="current"), "DJ_PLACE_CONTRACT")
    r("DJ_PLACE_ADMIN_PARENT", lambda d: d["relationships"].append({**d["relationships"][0], "id": "REL-DJ-MUT-PARENT", "child_id": place(d, "EUROPEAN-Q")["id"], "parent_id": "ENT-DJ-COMMUNE-RAS-DIKA", "relationship_type": "administrative_parent"}), "DJ_PLACE_LOCATED_IN")
    r("DJ_PLACE_WRONG_PARENT", lambda d: next(x for x in d["relationships"] if x["child_id"] == place(d, "AMBOULI-Q")["id"]).update(parent_id="ENT-DJ-COMMUNE-BALBALA"), "DJ_PLACE_LOCATED_IN")
    r("DJ_PLACE_CLAIM_ATTACHED", lambda d: d["claims"].append({**depth(d, "food_dish"), "id": "CLM-DJ-MUT-PLACE", "subject_id": place(d, "HERON-Q")["id"], "predicate": "population", "value": {"type": "integer", "data": 5000}}), "DJ_PLACE_CLAIMS")
    r("DJ_PLACE_SOURCE_UPGRADE", lambda d: place(d, "MARABOUT-Q").update(canonical_source_id="SRC-UNESCO-ICH-DJ-STATE-2026", verification_status="source_verified"), "DJ_PLACE_CONTRACT")
    r("DJ_PLACE_CHILD_INFERRED", lambda d: d["relationships"].append({**d["relationships"][0], "id": "REL-DJ-MUT-CHILD", "child_id": "ENT-DJ-COMMUNE-RAS-DIKA", "parent_id": place(d, "EUROPEAN-Q")["id"], "relationship_type": "administrative_parent"}), "DJ_PLACE_LOCATED_IN")
    r("DJ_MARKET_AS_QUARTER", lambda d: place(d, "CENTRAL-M").update(entity_type="quarter"), "DJ_COUNTS")
    r("DJ_SOURCE_TIER_INFLATION", lambda d: next(x for x in d["sources"] if x["id"] == "SRC-DJ-WEDDING-ALJAZIRAH-1999").update(quality_tier="A"), "DJ_SOURCES")
    r("DJ_ICH_LAYER_DENOMINATOR", lambda d: next(l for l in d["manifest"]["pilot_layers"] if l["layer"] == "unesco_intangible_heritage").update(denominator=4, coverage_record_id="COV-DJ-ICH"), "DJ_ICH_LAYER")
    r("DJ_PLACE_LAYER_DENOMINATOR", lambda d: next(l for l in d["manifest"]["pilot_layers"] if l["layer"] == "world_heritage_medinas").update(denominator=12, coverage_record_id="COV-DJ-PLACES"), "DJ_PLACE_LAYER")

    ok = all(x["detected"] for x in o)
    write_json(ROOT / "reports/djibouti_negative_tests.json", {"schema_version": "2.0.0", "country_code": "DJ",
                                                               "status": "PASS" if ok else "FAIL", "required": len(o),
                                                               "detected": sum(x["detected"] for x in o), "mutations": o})
    for row in o:
        print(f"[{'PASS' if row['detected'] else 'FAIL'}] {row['mutation']} -> {row['expected_code']}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
