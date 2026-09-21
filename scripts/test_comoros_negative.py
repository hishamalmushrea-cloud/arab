#!/usr/bin/env python3
"""Required Comoros mutations: accepted hierarchy plus depth cycle 1."""
import copy

from model import ROOT, write_json
from validate_comoros import data, validate


def main():
    b = data()
    o = []

    def r(n, fn, c):
        d = copy.deepcopy(b)
        fn(d)
        o.append({"mutation": n, "expected_code": c, "detected": any(x["code"] == c for x in validate(d))})

    def depth(d, predicate, name=None, article=None):
        for row in d["claims"]:
            if not str(row["id"]).startswith("CLM-KM-DEPTH") or row["predicate"] != predicate:
                continue
            payload = row["value"]["data"]
            label = (payload.get("name") or payload.get("variety") or "") if isinstance(payload, dict) else ""
            if name and name not in label:
                continue
            if article and str(row["value"]["data"].get("article")) != article:
                continue
            return row
        raise AssertionError(f"fixture depth claim missing: {predicate}")

    def medina(d, token):
        return next(x for x in d["entities"] if x["id"] == "ENT-KM-MEDINA-" + token)

    # Accepted-layer mutations (kept from cycle 1).
    r("KM_MAYOTTE_CURRENT", lambda d: d["entities"].append({**d["entities"][-1], "id": "ENT-KM-ISLAND-MAYOTTE", "canonical_name": "Mayotte", "entity_type": "km_island"}), "KM_MAYOTTE_CURRENT")
    r("KM_PREF_WRONG_ISLAND", lambda d: next(x for x in d["relationships"] if x["child_id"].startswith("ENT-KM-PREFECTURE")).update(parent_id="ENT-KM-ISLAND-MWALI"), "KM_PREFECTURE_PARENT")
    r("KM_COMMUNE_WRONG_PREF", lambda d: next(x for x in d["relationships"] if x["child_id"].startswith("ENT-KM-COMMUNE")).update(parent_id="ENT-KM-PREFECTURE-DJANDO"), "KM_COMMUNE_PARENT")
    r("KM_58_COMMUNES", lambda d: next(x for x in d["denominators"] if x["id"] == "DEN-KM-COMMUNES").update(value=58), "KM_DENOMINATORS")
    r("KM_OLD_ZERO_WHC", lambda d: next(x for x in d["claims"] if x["predicate"] == "world_heritage_inscription_year")["value"].update(data=0), "KM_WHC_2026")
    r("KM_DROP_ISLAND", lambda d: d["entities"].__setitem__(slice(None), [x for x in d["entities"] if x.get("entity_type") != "km_island"]), "KM_COUNTS")
    r("KM_COMMUNE_AS_VILLAGE", lambda d: next(x for x in d["entities"] if x.get("entity_type") == "km_commune").update(entity_type="village"), "KM_COUNTS")
    r("KM_DROP_COMMUNE", lambda d: d["entities"].__setitem__(slice(None), [x for x in d["entities"] if x["id"] != "ENT-KM-COMMUNE-MORONI"]), "KM_COUNTS")
    r("KM_MAYOTTE_AS_COMMUNE", lambda d: d["entities"].append({**d["entities"][-1], "id": "ENT-KM-COMMUNE-MAYOTTE", "canonical_name": "Mayotte", "entity_type": "km_commune"}), "KM_MAYOTTE_CURRENT")

    # Depth-cycle mutations.
    r("KM_ICH_UNPUBLISHED", lambda d: depth(d, "intangible_cultural_practice").update(published=False), "KM_ICH_CONTRACT")
    r("KM_ICH_NOT_SHARED", lambda d: depth(d, "intangible_cultural_practice").update(classification="national"), "KM_ICH_CONTRACT")
    r("KM_ICH_WRONG_YEAR", lambda d: depth(d, "intangible_cultural_practice")["value"]["data"].update(year=2019), "KM_ICH_CONTRACT")
    r("KM_ICH_TWO_STATES", lambda d: depth(d, "intangible_cultural_practice")["value"]["data"].update(co_states=["Comoros", "Djibouti"]), "KM_ICH_CONTRACT")
    r("KM_CONSTITUTION_ARTICLE_LOST", lambda d: d["claims"].__setitem__(slice(None), [x for x in d["claims"] if not (x["predicate"] == "constitutional_provision" and str(x["value"]["data"].get("article")) == "9")]), "KM_CONSTITUTION_CONTRACT")
    def silence(d):
        row = depth(d, "constitutional_provision", article="6")
        row.update(notes="نص دستوري عن التراب.")
        row["value"]["data"]["note"] = None
        row["value"]["data"]["summary"] = "تنص المادة 6 على تراب الاتحاد."
    r("KM_MAYOTTE_CLAIM_SILENT", silence, "KM_MAYOTTE_CLAIM")
    r("KM_OFFICIAL_LANGUAGE_UNPUBLISHED", lambda d: depth(d, "language_presence", name="العربية").update(published=False), "KM_LANGUAGE_CONTRACT")
    r("KM_MINORITY_PUBLISHED", lambda d: depth(d, "language_presence", name="الملغاشية").update(published=True, verification_status="verified"), "KM_LANGUAGE_CONTRACT")
    r("KM_ISO_CODE_LOST", lambda d: depth(d, "language_presence", name="شيكومور")["value"]["data"].update(iso_codes=["zdj"]), "KM_LANGUAGE_CONTRACT")
    r("KM_SPEAKER_SHARE", lambda d: depth(d, "language_presence", name="شيكومور")["value"]["data"].update(speakers="96.9% من السكان"), "KM_NO_SPEAKER_NUMBERS")
    r("KM_MEDINA_AS_CURRENT", lambda d: medina(d, "MORONI").update(status="current"), "KM_MEDINA_CONTRACT")
    r("KM_MEDINA_ADMIN_PARENT", lambda d: d["relationships"].append({**d["relationships"][0], "id": "REL-KM-MUT-PARENT", "child_id": medina(d, "MORONI")["id"], "parent_id": "ENT-KM-COMMUNE-MORONI", "relationship_type": "administrative_parent"}), "KM_MEDINA_LOCATED_IN")
    r("KM_MEDINA_WRONG_ISLAND", lambda d: next(x for x in d["relationships"] if x["child_id"] == medina(d, "MUTSAMUDU")["id"]).update(parent_id="ENT-KM-ISLAND-NGAZIDJA"), "KM_MEDINA_LOCATED_IN")
    r("KM_MEDINA_AS_CITY", lambda d: medina(d, "DOMONI").update(entity_type="city"), "KM_COUNTS")
    r("KM_MEDINA_CLAIM_ATTACHED", lambda d: d["claims"].append({**depth(d, "food_dish"), "id": "CLM-KM-MUT-MED", "subject_id": medina(d, "IKONI")["id"], "predicate": "population", "value": {"type": "integer", "data": 1200}}), "KM_MEDINA_CLAIMS")
    r("KM_MEDINA_SOURCE_UPGRADE", lambda d: medina(d, "ITSANDRA").update(canonical_source_id="SRC-UNESCO-WHC-KM-1768-2026", verification_status="source_verified"), "KM_MEDINA_CONTRACT")
    r("KM_WEAK_DEPTH_PUBLISHED", lambda d: depth(d, "food_dish", name="مكاترا فوترا").update(published=True), "KM_WEAK_DEPTH_PUBLISHED")
    r("KM_DIALECT_PROMOTED", lambda d: depth(d, "dialect_profile", name="شينجازيجا").update(verification_status="verified"), "KM_WEAK_DEPTH_CAP")
    r("KM_DIALECT_WITHOUT_GLOSS", lambda d: depth(d, "dialect_profile", name="المفردات")["value"]["data"].__setitem__("phrases", [["Eledzina lahaho ndo?"]]), "KM_DIALECT_GLOSS")
    r("KM_WHC_AREA_TAMPER", lambda d: depth(d, "world_heritage_area_hectares").update(value={"type": "number", "data": 30.5}), "KM_WHC_EXTRA")
    r("KM_COMPONENT_NAMES_PUBLISHED", lambda d: depth(d, "serial_component_names").update(published=True, verification_status="verified"), "KM_WHC_EXTRA")
    r("KM_SOURCE_TIER_INFLATION", lambda d: next(x for x in d["sources"] if x["id"] == "SRC-KM-VOCAB-QUIZLET-2016").update(quality_tier="A"), "KM_SOURCES")
    r("KM_SHARED_CUSTOM_AS_NATIONAL", lambda d: depth(d, "custom_practice").update(classification="national"), "KM_WEAK_DEPTH_CAP")
    r("KM_ICH_LAYER_DENOMINATOR", lambda d: next(l for l in d["manifest"]["pilot_layers"] if l["layer"] == "unesco_intangible_heritage").update(denominator=7, coverage_record_id="COV-KM-ICH"), "KM_ICH_LAYER")
    r("KM_MEDINA_LAYER_DENOMINATOR", lambda d: next(l for l in d["manifest"]["pilot_layers"] if l["layer"] == "world_heritage_medinas").update(denominator=6, coverage_record_id="COV-KM-MEDINAS"), "KM_MEDINA_LAYER")

    ok = all(x["detected"] for x in o)
    write_json(ROOT / "reports/comoros_negative_tests.json", {"schema_version": "2.0.0", "country_code": "KM",
                                                              "status": "PASS" if ok else "FAIL", "required": len(o),
                                                              "detected": sum(x["detected"] for x in o), "mutations": o})
    for row in o:
        print(f"[{'PASS' if row['detected'] else 'FAIL'}] {row['mutation']} -> {row['expected_code']}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
