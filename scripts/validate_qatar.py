#!/usr/bin/env python3
"""Qatar production semantic validator independent of the importer, extended for depth cycle 1."""
import hashlib
import json

from model import ROOT, read_jsonl, write_json

SNAPSHOT_DATE = "2026-08-16"
DEPTH_DATE = "2026-09-20"
BASE_SOURCES = {
    "SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020",
    "SRC-QA-QNMP-EIGHT-MUNICIPALITIES-2026",
    "SRC-UNESCO-WHC-QA-1402",
}
DEPTH_SOURCES = {
    "SRC-QA-UNESCO-ICH-2026", "SRC-QA-CUISINE-MIRROR-2026", "SRC-QA-DIALECT-DOHA24-2025",
    "SRC-QA-DIALECT-FORUM-2010", "SRC-QA-DRESS-JAZEERA-2018", "SRC-QA-DRESS-QNA-2023",
    "SRC-QA-DRESS-KHALEEJ-2016", "SRC-QA-FIRJAN-PRESS-2024", "SRC-QA-FIRJAN-NAJADA-2022",
    "SRC-QA-SOUQ-WAQIF-2012",
}
ICH_SOURCE = "SRC-QA-UNESCO-ICH-2026"
MUNICIPALITY_IDS = {
    "ENT-QA-MUNICIPALITY-DOHA", "ENT-QA-MUNICIPALITY-AL-RAYYAN", "ENT-QA-MUNICIPALITY-AL-WAKRA",
    "ENT-QA-MUNICIPALITY-UMM-SLAL", "ENT-QA-MUNICIPALITY-AL-KHOR-AL-THAKHIRA",
    "ENT-QA-MUNICIPALITY-AL-SHAMAL", "ENT-QA-MUNICIPALITY-AL-DAAYEN",
    "ENT-QA-MUNICIPALITY-AL-SHEEHANIYA",
}
SHARED_DISHES = {"المجبوس", "المحمر", "المشخول", "الشيلاني", "المضروبة", "الهريس", "الجريش",
                 "الثريد", "المرقوقة", "البلاليط", "العصيدة", "اللقيمات", "الخنفروش",
                 "الزلابية", "الرهش", "الكرك"}


def L(p):
    return json.loads(p.read_text(encoding="utf8"))


def data():
    e = [r for r in read_jsonl(ROOT / "data/entities/entities.jsonl") if r.get("country_code") == "QA"]
    ids = {r["id"] for r in e}
    return {
        "entities": e,
        "aliases": [r for r in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if r.get("entity_id") in ids],
        "relationships": [r for r in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if r.get("child_id") in ids],
        "claims": [r for r in read_jsonl(ROOT / "data/claims/claims.jsonl") if r.get("subject_id") in ids],
        "denominators": [r for r in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if r.get("country_code") == "QA"],
        "coverage": [r for r in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if r.get("country_code") == "QA"],
        "sources": [L(p) for p in (ROOT / "data/sources").glob("*.json") if L(p).get("id") in BASE_SOURCES | DEPTH_SOURCES],
        "manifest": L(ROOT / "manifests/QA.yml"),
    }


def validate(d):
    f = L(ROOT / "data/imports/qatar/fixtures/municipalities_census_2020.json")
    depth = L(ROOT / "data/imports/qatar/fixtures/cultural_depth_2026.json")
    exp = {r["name_ar"]: (r["name_en"], r["population"]) for r in f["records"]}
    E = {r["id"]: r for r in d["entities"]}
    municip = {r["canonical_name"]: r for r in E.values() if r["entity_type"] == "qa_municipality"}
    places = {r["id"]: r for r in E.values() if r["entity_type"] in {"quarter", "market"}}
    rels = d["relationships"]
    claims = d["claims"]
    err = []

    def x(code, loc, msg):
        err.append({"code": code, "location": loc, "message": msg})

    expected_entities = {"ENT-QA-COUNTRY", *MUNICIPALITY_IDS, "ENT-QA-ARCHAEOLOGICAL-SITE-AL-ZUBARAH", *places}
    if set(E) != expected_entities or len(E) != 14:
        x("QA_ENTITY_UNIVERSE", "entities", "expected country + 8 municipalities + Al Zubarah + four old-Doha places")
    if len(places) != 4 or sum(1 for r in places.values() if r["entity_type"] == "quarter") != 3 or sum(1 for r in places.values() if r["entity_type"] == "market") != 1:
        x("QA_ENTITY_UNIVERSE", "entities", "expected three firjan and one heritage market")
    if set(municip) != set(exp):
        x("QA_MUNICIPALITY_SET", "municipalities", "eight-name mismatch")
    for ar, (en, pop) in exp.items():
        r = municip.get(ar, {})
        eid = r.get("id")
        if not eid:
            continue
        if not any(a["entity_id"] == eid and a["name"] == en for a in d["aliases"]):
            x("QA_ALIAS", eid, "alias mismatch")
        if not any(q["child_id"] == eid and q["parent_id"] == "ENT-QA-COUNTRY" and q["relationship_type"] == "administrative_parent" for q in rels):
            x("QA_WRONG_PARENT", eid, "wrong parent")
        if not any(c["subject_id"] == eid and c["predicate"] == "population" and c["value"]["data"] == pop and c["observed_at"] == "2020-12-31" for c in claims):
            x("QA_POPULATION", eid, "population mismatch")
    if len(d["aliases"]) != 9 or len(rels) != 13 or len(claims) != 50:
        x("QA_COUNTS", "QA", f"expected aliases/relationships/claims 9/13/50, got {len(d['aliases'])}/{len(rels)}/{len(claims)}")
    for c in claims:
        if c["predicate"].startswith("lexical_"):
            x("QA_DIALECT", c["id"], "unsupported lexical predicate in this cycle")
        if c["subject_id"] in MUNICIPALITY_IDS and c["predicate"] != "population":
            x("QA_CITY_LEAKAGE", c["id"], "non-population municipality claim")
        if not c.get("source_id") or not c.get("source_locator"):
            x("QA_CLAIM_SOURCE", c["id"], "claim without source or locator")
    if {r["id"] for r in d["sources"]} != BASE_SOURCES | DEPTH_SOURCES:
        x("QA_SOURCES", "sources", "source set differs from the accepted catalog")
    tiers = {}
    for r in d["sources"]:
        tiers[r.get("quality_tier")] = tiers.get(r.get("quality_tier"), 0) + 1
    if tiers.get("A") != 4 or tiers.get("E") != 9:
        x("QA_SOURCES", "sources", f"expected four A-tier and nine E-tier sources, got {tiers}")
    if {r["id"]: r["value"] for r in d["denominators"]} != {"DEN-QA-COUNTRY-SCOPE": 1, "DEN-QA-MUNICIPALITIES-2020": 8, "DEN-QA-WHC-20260816": 1}:
        x("QA_DENOMINATORS", "den", "1/8/1 expected")

    # Depth cycle 1: published UNESCO spine, classified unpublished body, bounded old-Doha places.
    for identifier, row in places.items():
        if row.get("status") != "historical" or row.get("verification_status") != "local_reported" or row.get("canonical_source_id") not in DEPTH_SOURCES:
            x("QA_PLACE_CONTRACT", identifier, "old-Doha place must stay historical and local_reported on a depth source")
        links = [r for r in rels if r["child_id"] == identifier]
        if len(links) != 1 or links[0]["relationship_type"] != "located_in" or links[0]["parent_id"] != "ENT-QA-MUNICIPALITY-DOHA":
            x("QA_PLACE_LOCATED_IN", identifier, "place requires exactly one located_in relation to Doha municipality")
        if any(a["entity_id"] == identifier for a in d["aliases"]):
            x("QA_PLACE_ALIAS", identifier, "place carries an alias without an accepted alias source")
        if any(c["subject_id"] == identifier and c["predicate"] == "population" for c in claims):
            x("QA_PLACE_POPULATION", identifier, "no population claim may be attached to an old-Doha place")
    depth_claims = [r for r in claims if str(r.get("id", "")).startswith("CLM-QA-DEPTH")]
    expected_depth = {"intangible_cultural_practice": 4, "custom_practice": 2, "clothing_item": 8,
                      "dialect_profile": 3, "food_dish": 20, "craft_custom": 2, "name_origin_narrative": 1}
    actual_depth = {}
    for r in depth_claims:
        actual_depth[r["predicate"]] = actual_depth.get(r["predicate"], 0) + 1
    if actual_depth != expected_depth or len(depth_claims) != 40:
        x("QA_DEPTH_COUNTS", "QA", f"depth predicate mix differs: {actual_depth}")
    ich = [r for r in depth_claims if r.get("source_id") == ICH_SOURCE]
    if {r["value"]["data"].get("reference") for r in ich} != {e["reference"] for e in depth["ich_elements"]}:
        x("QA_ICH_CONTRACT", "QA", "UNESCO element references differ from the fixture list")
    for r in ich:
        if not r.get("published") or r.get("verification_status") != "verified" or r.get("classification") != "shared":
            x("QA_ICH_CONTRACT", r["id"], "every current Qatari element is a shared multi-State file: verified, published, shared")
    for r in depth_claims:
        if r.get("source_id") == ICH_SOURCE:
            continue
        if r.get("published"):
            x("QA_DEPTH_PUBLISHED_FROM_WEAK", r["id"], "weak-source claim may not be published")
        if r.get("verification_status") not in {"probable", "local_reported", "unverified", "folk_narrative"}:
            x("QA_DEPTH_CONTRACT", r["id"], "weak-source claim exceeds the local_reported cap")
        if not r.get("classification"):
            x("QA_DEPTH_CONTRACT", r["id"], "depth claim requires explicit classification")
    for name in SHARED_DISHES:
        found = next((r for r in depth_claims if r["predicate"] == "food_dish" and r["value"]["data"].get("name") == name), None)
        if not found or found.get("classification") != "shared":
            x("QA_SHARED_NOT_EXCLUSIVE", "QA", f"{name} must stay shared even when described as the national dish")
    for r in depth_claims:
        if r["predicate"] == "dialect_profile":
            for word in r["value"]["data"].get("sample_words", []):
                if len(word) != 2 or not word[1]:
                    x("QA_DIALECT_GLOSS", r["id"], "dialect vocabulary entry needs word and meaning")
    if not any(r["predicate"] == "name_origin_narrative" and r["classification"] == "local_reported" for r in depth_claims):
        x("QA_DEPTH_COUNTS", "QA", "missing Souq Waqif naming narrative")
    if any(r["predicate"] == "language_presence" for r in claims):
        x("QA_LANGUAGE_UNSUPPORTED", "QA", "no sourced non-Arabic presence was accepted; the zero is deliberate")

    m = d["manifest"]
    g = next(q for q in m["hierarchy"] if q["entity_type"] == "qa_municipality")
    if g.get("denominator") != 8 or g.get("scope_status") != "closed":
        x("QA_MANIFEST", "manifest", "municipal scope")
    for t in ["qa_zone", "qa_district"]:
        q = next(z for z in m["hierarchy"] if z["entity_type"] == t)
        if q.get("denominator") is not None or q.get("scope_status") != "unavailable":
            x("QA_LOWER_LAYER", t, "invented lower layer")
    layers = {l.get("layer"): l for l in m.get("pilot_layers", [])}
    ich_layer = layers.get("unesco_intangible_heritage", {})
    if ich_layer.get("denominator") != 7 or ich_layer.get("coverage_record_id") is not None or ich_layer.get("scope_status") != "closed":
        x("QA_ICH_LAYER", "manifest", "ICH layer must close at seven with the list as its own denominator and no coverage record")
    places_layer = layers.get("old_doha_places", {})
    if places_layer.get("denominator") is not None or places_layer.get("coverage_record_id") is not None or sorted(places_layer.get("entity_types", [])) != ["market", "quarter"]:
        x("QA_HERITAGE_LAYER", "manifest", "old-Doha layer must carry no denominator and only quarter/market types")
    knowledge_layer = layers.get("classified_local_knowledge", {})
    if knowledge_layer.get("denominator") is not None or knowledge_layer.get("scope_status") != "open":
        x("QA_KNOWLEDGE_LAYER", "manifest", "classified knowledge layer must stay open with no denominator")
    return err


def main():
    d = data()
    e = validate(d)
    met = {k: len(d[k]) for k in ["entities", "aliases", "relationships", "claims", "sources", "denominators", "coverage"]}
    met["depth_claims"] = sum(str(r.get("id", "")).startswith("CLM-QA-DEPTH") for r in d["claims"])
    met["depth_places"] = sum(r["entity_type"] in {"quarter", "market"} for r in d["entities"])
    met["published_claims"] = sum(bool(r.get("published")) for r in d["claims"])
    write_json(ROOT / "reports/qatar_validation.json", {"schema_version": "2.0.0", "country_code": "QA", "snapshot_date": DEPTH_DATE, "status": "PASS" if not e else "FAIL", "p0": len(e), "critical_p1": 0, "metrics": met, "errors": e})
    print(json.dumps(met, ensure_ascii=False))
    if e:
        for row in e:
            print(f"- {row['code']} {row['location']}: {row['message']}")
    print("Qatar production semantic validation " + ("passed." if not e else "failed."))
    return 0 if not e else 1


if __name__ == "__main__":
    raise SystemExit(main())
