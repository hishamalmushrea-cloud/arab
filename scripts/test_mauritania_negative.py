#!/usr/bin/env python3
"""Required Mauritania mutations: accepted wilaya layer plus depth cycle 1."""
import copy

from model import ROOT, write_json
from validate_mauritania import data, validate


def main():
    b = data()
    o = []

    def r(n, fn, c):
        d = copy.deepcopy(b)
        fn(d)
        o.append({"mutation": n, "expected_code": c, "detected": any(x["code"] == c for x in validate(d))})

    def depth(d, pred, key=None, val=None):
        for row in d["claims"]:
            if not str(row["id"]).startswith("CLM-MR-DEPTH") or row["predicate"] != pred:
                continue
            payload = row["value"]["data"]
            if key and isinstance(payload, dict) and (key not in payload if val is None else payload.get(key) != val):
                continue
            return row
        raise AssertionError(f"depth claim missing: {pred}")

    def place(d, token):
        return next(x for x in d["entities"] if x["id"].endswith("-" + token))

    # Accepted-layer mutations (kept from the wilaya cycle).
    r("MR_WILAYA_LOST", lambda d: d["entities"].__setitem__(slice(None), [x for x in d["entities"] if x["id"] != "ENT-MR-WILAYA-07"]), "MR_COUNTS")
    r("MR_COUNTRY_LOST", lambda d: d["entities"].__setitem__(slice(None), [x for x in d["entities"] if x["id"] != "ENT-MR-COUNTRY"]), "MR_COUNTS")
    r("MR_WRONG_PROFILE", lambda d: next(x for x in d["claims"] if x["predicate"] == "administrative_profile")["value"].update(data="wrong"), "MR_ACCEPTED")
    r("MR_MOUGHATAA_57", lambda d: next(x for x in d["claims"] if x["predicate"] == "moughataa_count")["value"].update(data=57), "MR_MOUGHATAA_SCOPE")
    r("MR_DENOM_16", lambda d: next(x for x in d["denominators"] if x["id"] == "DEN-MR-WILAYAS").update(value=16), "MR_DENOMINATORS")
    r("MR_PREMATURE_MOUGHATAA", lambda d: d["entities"].append({**d["entities"][-1], "id": "ENT-MR-MOUGHATAA-X", "entity_type": "mr_moughataa"}), "MR_LOWER")
    r("MR_PREMATURE_COMMUNE", lambda d: d["entities"].append({**d["entities"][-1], "id": "ENT-MR-COMMUNE-X", "entity_type": "mr_commune"}), "MR_LOWER")
    # Depth-cycle mutations.
    r("MR_ICH_WRONG_YEAR", lambda d: depth(d, "intangible_cultural_practice", "reference", "02116")["value"]["data"].update(year=2023), "MR_ICH_CONTRACT")
    r("MR_ICH_COSTATE_LOST", lambda d: depth(d, "intangible_cultural_practice", "reference", "01902")["value"]["data"].update(co_states=["موريتانيا"]), "MR_ICH_CONTRACT")
    r("MR_ICH_SHARED_AS_NATIONAL", lambda d: depth(d, "intangible_cultural_practice", "reference", "01602").update(classification="national"), "MR_ICH_CONTRACT")
    r("MR_ICH_NATIONAL_AS_SHARED", lambda d: depth(d, "intangible_cultural_practice", "reference", "00524").update(classification="shared"), "MR_ICH_CONTRACT")
    r("MR_ICH_UNPUBLISHED", lambda d: depth(d, "intangible_cultural_practice", "reference", "00524").update(published=False), "MR_ICH_CONTRACT")
    r("MR_ICH_WEAK_SOURCE", lambda d: depth(d, "intangible_cultural_practice", "reference", "01692").update(source_id="SRC-MR-SITES-MIRROR-2026"), "MR_ICH_CONTRACT")
    r("MR_ICH_EXTRA_ELEMENT", lambda d: d["claims"].append({**depth(d, "intangible_cultural_practice"), "id": "CLM-MR-MUT-ICH", "value": {"type": "json", "data": {**depth(d, "intangible_cultural_practice")["value"]["data"], "reference": "09999"}}}), "MR_ICH_CONTRACT")
    r("MR_DEPTH_PREDICATE_LOST", lambda d: depth(d, "food_dish").update(predicate="meal_item"), "MR_DEPTH_COUNTS")
    r("MR_DEPTH_CLAIM_DROPPED", lambda d: d["claims"].__setitem__(slice(None), [x for x in d["claims"] if x["id"] != depth(d, "dialect_profile")["id"]]), "MR_DEPTH_COUNTS")
    r("MR_PENDING_AS_INSCRIBED", lambda d: depth(d, "unesco_pending_nomination", "element").update(predicate="intangible_cultural_practice"), "MR_PENDING_NOMINATION")
    r("MR_PENDING_UNPUBLISHED", lambda d: depth(d, "unesco_pending_nomination").update(published=False), "MR_PENDING_NOMINATION")
    r("MR_PENDING_STATUS_UPGRADED", lambda d: depth(d, "unesco_pending_nomination")["value"]["data"].update(status="مُدرج"), "MR_PENDING_NOMINATION")
    r("MR_PENDING_ELEMENT_INSCRIBED", lambda d: depth(d, "unesco_pending_nomination", "element").update(predicate="intangible_cultural_practice"), "MR_PENDING_NOMINATION")
    r("MR_PENDING_ELEMENT_NAMED_AS_INSCRIBED", lambda d: depth(d, "intangible_cultural_practice", "reference", "01960")["value"]["data"].update(name="العود: الممارسات والمهارات والفنون الأدائية"), "MR_PENDING_NOMINATION")
    r("MR_CONVENTION_DATE_LOST", lambda d: depth(d, "convention_ratification_date").update(published=False), "MR_CONVENTION_CONTRACT")
    r("MR_CONVENTION_WRONG_DATE", lambda d: depth(d, "convention_ratification_date")["value"]["data"].update(date="2011-11-15"), "MR_CONVENTION_CONTRACT")
    r("MR_CONSTITUTION_ARTICLE_LOST", lambda d: d["claims"].__setitem__(slice(None), [x for x in d["claims"] if not (x["predicate"] == "constitutional_provision" and str(x["value"]["data"].get("article")) == "7")]), "MR_CONSTITUTION_CONTRACT")
    r("MR_CONSTITUTION_UNPUBLISHED", lambda d: next(x for x in d["claims"] if x["predicate"] == "constitutional_provision").update(published=False), "MR_CONSTITUTION_CONTRACT")
    r("MR_CONSTITUTION_OFFICIAL_LANGUAGE_LOST", lambda d: next(x for x in d["claims"] if x["predicate"] == "constitutional_provision" and str(x["value"]["data"].get("article")) == "6")["value"]["data"].update(summary="للمواطنين حرية التعبير."), "MR_CONSTITUTION_CONTRACT")
    r("MR_WH_NATURAL_CRITERIA", lambda d: depth(d, "world_heritage_property", "reference", "506")["value"]["data"].update(criteria=["x"]), "MR_WH_CONTRACT")
    r("MR_WH_KSOUR_CRITERIA_LOST", lambda d: depth(d, "world_heritage_property", "reference", "750")["value"]["data"].update(criteria=["iv"]), "MR_WH_CONTRACT")
    r("MR_WH_CATEGORY_SWAPPED", lambda d: depth(d, "world_heritage_property", "reference", "506")["value"]["data"].update(category="ثقافي"), "MR_WH_CONTRACT")
    r("MR_WH_UNPUBLISHED", lambda d: depth(d, "world_heritage_property", "reference", "750").update(published=False), "MR_WH_CONTRACT")
    r("MR_TENTATIVE_AS_INSCRIBED", lambda d: depth(d, "unesco_tentative_listing").update(predicate="world_heritage_property"), "MR_TENTATIVE_CONTRACT")
    r("MR_TENTATIVE_UNPUBLISHED", lambda d: depth(d, "unesco_tentative_listing").update(published=False), "MR_TENTATIVE_CONTRACT")
    r("MR_TENTATIVE_REFERENCE_LOST", lambda d: depth(d, "unesco_tentative_listing")["value"]["data"].update(reference="9999"), "MR_TENTATIVE_CONTRACT")
    r("MR_OFFICIAL_LANGUAGE_UNPUBLISHED", lambda d: depth(d, "language_presence", "name", "العربية").update(published=False), "MR_LANGUAGE_CONTRACT")
    r("MR_NATIONAL_LANGUAGE_AS_OFFICIAL", lambda d: depth(d, "language_presence", "name", "الولوفية")["value"]["data"].update(official=True), "MR_LANGUAGE_CONTRACT")
    r("MR_NATIONAL_LANGUAGE_UNPUBLISHED", lambda d: depth(d, "language_presence", "name", "السوننكية").update(published=False), "MR_LANGUAGE_CONTRACT")
    r("MR_NATIONAL_SOURCE_WEAKENED", lambda d: depth(d, "language_presence", "name", "البولارية (بولاار)").update(source_id="SRC-MR-LANGUAGES-MIRROR-2026"), "MR_LANGUAGE_CONTRACT")
    r("MR_ISO_CODE_LOST", lambda d: depth(d, "language_presence", "name", "الولوفية")["value"]["data"].update(iso_codes=[]), "MR_LANGUAGE_CONTRACT")
    r("MR_ISO_SOURCE_LOST", lambda d: depth(d, "language_presence", "name", "البولارية (بولاار)").update(second_source_id=None, second_source_locator=None), "MR_LANGUAGE_CONTRACT")
    r("MR_WEAK_LANGUAGE_PUBLISHED", lambda d: depth(d, "language_presence", "name", "الحسانية").update(published=True, verification_status="verified", classification="official"), "MR_LANGUAGE_CONTRACT")
    r("MR_SIGN_LANGUAGE_ISO_CLAIMED", lambda d: depth(d, "language_presence", "level", "signed")["value"]["data"].update(iso_codes=["x"]), "MR_LANGUAGE_CONTRACT")
    r("MR_EXTRA_LANGUAGE", lambda d: d["claims"].append({**depth(d, "language_presence"), "id": "CLM-MR-MUT-LANG", "value": {"type": "json", "data": {**depth(d, "language_presence")["value"]["data"], "name": "الماندرين"}}}), "MR_LANGUAGE_CONTRACT")
    r("MR_SECOND_SOURCE_LOCATOR_LOST", lambda d: depth(d, "language_presence", "name", "السوننكية").update(second_source_locator=None), "MR_SECOND_SOURCE_PAIR")
    r("MR_SECOND_SOURCE_ID_ONLY", lambda d: depth(d, "language_presence", "name", "السوننكية").update(second_source_id=None), "MR_SECOND_SOURCE_PAIR")
    r("MR_SPEAKER_SHARE", lambda d: depth(d, "language_presence", "name", "الحسانية").update(notes="نسبة المتحدثين 52%."), "MR_NO_COUNTS")
    r("MR_SPEAKER_COUNT", lambda d: depth(d, "language_presence", "name", "الحسانية").update(notes="يبلغ عدد المتحدثين 705,500."), "MR_NO_COUNTS")
    r("MR_POPULATION_FIELD_ON_DEPTH", lambda d: depth(d, "food_dish")["value"]["data"].update(population=1200), "MR_NO_COUNTS")
    r("MR_PERCENT_FIELD_ON_DEPTH", lambda d: depth(d, "clothing_item")["value"]["data"].update(share="15%"), "MR_NO_COUNTS")
    r("MR_WEAK_DEPTH_PUBLISHED", lambda d: depth(d, "food_dish", "name", "مافي").update(published=True, verification_status="verified"), "MR_WEAK_DEPTH_PUBLISHED")
    r("MR_PRESS_DEPTH_PUBLISHED", lambda d: depth(d, "folk_narrative").update(published=True, verification_status="verified"), "MR_WEAK_DEPTH_PUBLISHED")
    r("MR_FOLK_AS_FACT", lambda d: depth(d, "folk_narrative").update(verification_status="verified", classification="national"), "MR_FOLK_NARRATIVE")
    r("MR_FOLK_PUBLISHED", lambda d: depth(d, "folk_narrative").update(published=True), "MR_FOLK_NARRATIVE")
    r("MR_NAMING_NARRATIVE_PUBLISHED", lambda d: depth(d, "place_name_narrative").update(published=True, verification_status="verified", classification="national"), "MR_FOLK_NARRATIVE")
    r("MR_DISCREPANCY_SINGLE_VALUE", lambda d: next(x for x in d["claims"] if x["predicate"] == "commune_count_candidates")["value"].update(data=[220]), "MR_DISCREPANCY")
    r("MR_DISCREPANCY_PUBLISHED_AS_FACT", lambda d: next(x for x in d["claims"] if x["predicate"] == "commune_count_candidates").update(classification="official", verification_status="verified"), "MR_DISCREPANCY")
    r("MR_COMMUNE_220_DEFAULT", lambda d: next(x for x in d["manifest"]["hierarchy"] if x["entity_type"] == "mr_commune").update(denominator=220), "MR_COMMUNE_CONFLICT")
    r("MR_CLOSE_MOUGHATAA_NO_RECORDS", lambda d: next(x for x in d["manifest"]["hierarchy"] if x["entity_type"] == "mr_moughataa").update(scope_status="closed"), "MR_MOUGHATAA_SCOPE")
    r("MR_PLACE_ADMIN_PARENT", lambda d: d["relationships"].append({**d["relationships"][0], "id": "REL-MR-MUT-PARENT", "child_id": place(d, "CHINGUETTI")["id"], "parent_id": "ENT-MR-WILAYA-07", "relationship_type": "administrative_parent"}), "MR_PLACE_LOCATED_IN")
    r("MR_PLACE_WRONG_PARENT", lambda d: next(x for x in d["relationships"] if x["child_id"] == place(d, "TICHITT")["id"]).update(parent_id="ENT-MR-WILAYA-07"), "MR_PLACE_LOCATED_IN")
    r("MR_PLACE_LOCATION_LOST", lambda d: d["relationships"].__setitem__(slice(None), [x for x in d["relationships"] if x["child_id"] != place(d, "OUADANE")["id"]]), "MR_PLACE_LOCATED_IN")
    r("MR_PLACE_CHILD_INFERRED", lambda d: d["relationships"].append({**d["relationships"][0], "id": "REL-MR-MUT-CHILD", "child_id": "ENT-MR-WILAYA-07", "parent_id": place(d, "OUALATA")["id"], "relationship_type": "administrative_parent"}), "MR_PLACE_LOCATED_IN")
    r("MR_PLACE_CLAIM_ATTACHED", lambda d: d["claims"].append({**depth(d, "food_dish"), "id": "CLM-MR-MUT-PLACE", "subject_id": place(d, "AZOUGUI")["id"], "predicate": "population", "value": {"type": "integer", "data": 5000}}), "MR_PLACE_CLAIMS")
    r("MR_PLACE_COORDINATES", lambda d: place(d, "KUMBI-SALEH").update(coordinates={"lat": 15.7, "lon": -7.9}), "MR_PLACE_CONTRACT")
    r("MR_MIRROR_PLACE_UPGRADED", lambda d: place(d, "AZOUGUI").update(verification_status="source_verified", confidence="high"), "MR_PLACE_CONTRACT")
    r("MR_UNESCO_PLACE_DOWNGRADED", lambda d: place(d, "CHINGUETTI").update(verification_status="local_reported", confidence="low"), "MR_PLACE_CONTRACT")
    r("MR_PLACE_AS_CURRENT_CITY", lambda d: place(d, "TEGDAOUST").update(entity_type="city"), "MR_PLACE_CONTRACT")
    r("MR_SOURCE_TIER_INFLATION", lambda d: next(x for x in d["sources"] if x["id"] == "SRC-MR-SITES-MIRROR-2026").update(quality_tier="A"), "MR_SOURCES")
    r("MR_PRESS_TIER_INFLATION", lambda d: next(x for x in d["sources"] if x["id"] == "SRC-MR-NOUAKCHOTT-ALKHALEEJ-2010").update(quality_tier="A"), "MR_SOURCES")
    r("MR_SOURCE_LICENSE_LOST", lambda d: next(x for x in d["sources"] if x["id"] == "SRC-MR-DGAT-15-63-2026").update(license=None), "MR_SOURCES")
    r("MR_ICH_LAYER_DENOMINATOR", lambda d: next(l for l in d["manifest"]["pilot_layers"] if l["layer"] == "unesco_intangible_heritage").update(denominator=10, coverage_record_id="COV-MR-ICH"), "MR_ICH_LAYER")
    r("MR_ICH_LAYER_CAVEAT_LOST", lambda d: next(l for l in d["manifest"]["pilot_layers"] if l["layer"] == "unesco_intangible_heritage").update(special_cases=[]), "MR_PLACE_LAYER")
    r("MR_PLACE_LAYER_DENOMINATOR", lambda d: next(l for l in d["manifest"]["pilot_layers"] if l["layer"] == "heritage_places").update(denominator=7, coverage_record_id="COV-MR-PLACES"), "MR_PLACE_LAYER")
    r("MR_KNOWLEDGE_LAYER_DENOMINATOR", lambda d: next(l for l in d["manifest"]["pilot_layers"] if l["layer"] == "classified_local_knowledge").update(denominator=20), "MR_PLACE_LAYER")
    r("MR_WH_LAYER_DENOMINATOR", lambda d: next(l for l in d["manifest"]["pilot_layers"] if l["layer"] == "world_heritage_properties").update(denominator=3, coverage_record_id="COV-MR-WH"), "MR_WH_CONTRACT")
    r("MR_LAYER_LOST", lambda d: d["manifest"]["pilot_layers"].__setitem__(slice(None), [l for l in d["manifest"]["pilot_layers"] if l["layer"] != "classified_local_knowledge"]), "MR_ICH_LAYER")
    r("MR_WEAK_CLAIM_PUBLISHED", lambda d: depth(d, "city_founding").update(published=True), "MR_PUBLISH")
    r("MR_MIRROR_TIER_UPGRADE", lambda d: next(x for x in d["sources"] if x["id"] == "SRC-MR-CUISINE-MIRROR-2026").update(quality_tier="A"), "MR_SOURCES")
    r("MR_PRESS_CLAIM_PUBLISHED", lambda d: depth(d, "city_founding").update(published=True, verification_status="source_verified"), "MR_WEAK_DEPTH_PUBLISHED")

    ok = all(x["detected"] for x in o)
    write_json(ROOT / "reports/mauritania_negative_tests.json", {"schema_version": "2.0.0", "country_code": "MR",
        "status": "PASS" if ok else "FAIL", "required": len(o), "detected": sum(x["detected"] for x in o), "mutations": o})
    bad = [x for x in o if not x["detected"]]
    print({"required": len(o), "detected": sum(x["detected"] for x in o), "missed": bad})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
