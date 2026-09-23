#!/usr/bin/env python3
"""Djibouti semantic validation: accepted 2024 topology plus depth cycle 1."""
import json

from model import ROOT, read_jsonl, write_json

BASE_SOURCES = {
    "SRC-DJ-PRESIDENCY-REGIONS-2026",
    "SRC-DJ-LAW-122-CITY-2005",
    "SRC-DJ-INSTAD-RGPH3-2024",
    "SRC-DJ-DECENTRALISATION-ROADMAP-2020",
    "SRC-DJ-INTERIOR-PREFECTURES-2026",
}
DEPTH_SOURCES = {
    "SRC-UNESCO-ICH-DJ-STATE-2026",
    "SRC-UNESCO-ICH-ZAFFA-02283-2025",
    "SRC-UNESCO-ICH-XEER-CIISE-02087-2024",
    "SRC-UNESCO-ICH-XEEDHO-02001-2023",
    "SRC-DJ-CONSTITUTION-2010",
    "SRC-DJ-ISO639-3-AFAR",
    "SRC-DJ-ISO639-3-SOMALI",
    "SRC-DJ-CUISINE-MIRROR-2026",
    "SRC-DJ-LANGUAGES-MIRROR-2026",
    "SRC-DJ-CITY-MIRROR-2026",
    "SRC-DJ-QUARTIERS-GUIDE-2026",
    "SRC-DJ-CITY-HISTORY-2026",
    "SRC-DJ-SIGN-LANGUAGES-2021",
    "SRC-DJ-WEDDING-ALJAZIRAH-1999",
}
SOURCES = BASE_SOURCES | DEPTH_SOURCES
TIERS = {"SRC-UNESCO-ICH-DJ-STATE-2026": "A", "SRC-UNESCO-ICH-ZAFFA-02283-2025": "A",
         "SRC-UNESCO-ICH-XEER-CIISE-02087-2024": "A", "SRC-UNESCO-ICH-XEEDHO-02001-2023": "A",
         "SRC-DJ-CONSTITUTION-2010": "A", "SRC-DJ-ISO639-3-AFAR": "A", "SRC-DJ-ISO639-3-SOMALI": "A",
         "SRC-DJ-CUISINE-MIRROR-2026": "E", "SRC-DJ-LANGUAGES-MIRROR-2026": "E",
         "SRC-DJ-CITY-MIRROR-2026": "E", "SRC-DJ-QUARTIERS-GUIDE-2026": "E",
         "SRC-DJ-CITY-HISTORY-2026": "E", "SRC-DJ-SIGN-LANGUAGES-2021": "E",
         "SRC-DJ-WEDDING-ALJAZIRAH-1999": "B"}
ICH_REFS = {"02283": ("shared", 7, "2025"), "02087": ("shared", 3, "2024"), "02001": ("national", 1, "2023")}
DEPTH_PREDICATES = {"intangible_cultural_practice": 3, "convention_ratification_date": 1,
                    "unesco_pending_nomination": 1, "constitutional_provision": 3,
                    "language_presence": 8, "dialect_profile": 1, "script_profile": 1,
                    "language_institution": 1, "food_dish": 12, "clothing_item": 3,
                    "craft_custom": 2, "custom_practice": 3,
                    "administrative_counts_discrepancy": 1}


def L(p):
    return json.loads(p.read_text(encoding="utf8"))


def data():
    e = [r for r in read_jsonl(ROOT / "data/entities/entities.jsonl") if r.get("country_code") == "DJ"]
    ids = {r["id"] for r in e}
    return {
        "entities": e,
        "relationships": [r for r in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if r.get("child_id") in ids or r.get("parent_id") in ids],
        "claims": [r for r in read_jsonl(ROOT / "data/claims/claims.jsonl") if r.get("subject_id") in ids],
        "sources": [L(p) for p in (ROOT / "data/sources").glob("*.json") if L(p).get("id") in SOURCES],
        "denominators": [r for r in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if r.get("country_code") == "DJ"],
        "coverage": [r for r in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if r.get("country_code") == "DJ"],
        "manifest": L(ROOT / "manifests/DJ.yml"),
        "depth": L(ROOT / "data/imports/djibouti/fixtures/cultural_depth_2026.json"),
    }


def validate(d):
    f = L(ROOT / "data/imports/djibouti/fixtures/topology_2024.json")
    dd = d["depth"]
    E = {r["id"]: r for r in d["entities"]}
    R = d["relationships"]
    C = d["claims"]
    err = []

    def x(c, l, m):
        err.append({"code": c, "location": l, "message": m})

    # 1. Accepted topology (unchanged from the surface cycle).
    counts = {t: sum(r["entity_type"] == t for r in E.values())
              for t in ["country", "dj_region", "djibouti_city", "dj_commune", "dj_subprefecture", "quarter", "market"]}
    if counts != {"country": 1, "dj_region": 5, "djibouti_city": 1, "dj_commune": 3,
                  "dj_subprefecture": 13, "quarter": 10, "market": 2}:
        x("DJ_COUNTS", "entities", str(counts))
    city = "ENT-DJ-DJIBOUTI-CITY"
    if not any(r["child_id"] == city and r["parent_id"] == "ENT-DJ-COUNTRY" for r in R):
        x("DJ_CITY_PARENT", city, "special city parent")
    for q in f["city"]["communes"]:
        cid = "ENT-DJ-COMMUNE-" + q["token"]
        if not any(r["child_id"] == cid and r["parent_id"] == city for r in R):
            x("DJ_COMMUNE_PATH", cid, "commune not under city")
    for g in f["regions"]:
        gid = "ENT-DJ-REGION-" + g["token"]
        children = {r["child_id"] for r in R if r["parent_id"] == gid}
        expected = {"ENT-DJ-SUBPREFECTURE-" + q["token"] for q in g["subprefectures"]}
        if children != expected:
            x("DJ_SUBPREFECTURE_PATH", gid, "regional child set")
        if not any(c["subject_id"] == gid and c["predicate"] == "population" and c["value"]["data"] == g["population"] for c in C):
            x("DJ_POPULATION", gid, "RGPH population")
    if not any(c["subject_id"] == city and c["predicate"] == "population" and c["value"]["data"] == f["city_population"] for c in C):
        x("DJ_POPULATION", city, "city population")
    if sum(c["value"]["data"] for c in C if c["predicate"] == "population") != f["population_total"]:
        x("DJ_POP_RECONCILIATION", "claims", "national total")
    if {r["id"]: r["value"] for r in d["denominators"]} != {"DEN-DJ-COUNTRY-SCOPE": 1, "DEN-DJ-REGIONS": 5,
                                                            "DEN-DJ-SPECIAL-CITY": 1, "DEN-DJ-CITY-COMMUNES": 3,
                                                            "DEN-DJ-SUBPREFECTURES": 13}:
        x("DJ_DENOMINATORS", "den", "1/5/1/3/13")
    if len(R) != 34 or len(C) != 46:
        x("DJ_RECORD_COUNTS", "DJ", f"34 rel/46 claims, got {len(R)}/{len(C)}")

    # 2. Source set, tiers and the citation unit.
    if {s["id"] for s in d["sources"]} != SOURCES or len(d["sources"]) != 19:
        x("DJ_SOURCES", "sources", "source set differs from the accepted catalog")
    tier_count = {}
    for s in d["sources"]:
        tier_count[s.get("quality_tier")] = tier_count.get(s.get("quality_tier"), 0) + 1
    if any(TIERS.get(s["id"], s.get("quality_tier")) != s.get("quality_tier") for s in d["sources"]):
        x("DJ_SOURCES", "sources", "a depth source tier was inflated")
    for c in C:
        if not c.get("source_id") or not c.get("source_locator"):
            x("DJ_CLAIM_SOURCE", c["id"], "claim without source or locator")
        if bool(c.get("second_source_id")) != bool(c.get("second_source_locator")):
            x("DJ_SECOND_SOURCE_PAIR", c["id"], "a second source must be cited with its own locator, and a locator never stands alone")
        if c.get("published") and TIERS.get(c.get("source_id"), "A") not in {"A", "B"} and c.get("source_id") not in BASE_SOURCES:
            x("DJ_PUBLISHED_FROM_WEAK", c["id"], "published claim must rest on an A/B source")
        if c.get("published") and c.get("verification_status") not in {"verified", "source_verified"}:
            x("DJ_PUBLISHED_STATUS", c["id"], "published claim must be verified")

    # 3. Depth cycle 1: UNESCO spine, constitution, classified body.
    depth = [c for c in C if str(c["id"]).startswith("CLM-DJ-DEPTH")]
    mix = {}
    for r in depth:
        mix[r["predicate"]] = mix.get(r["predicate"], 0) + 1
    if mix != DEPTH_PREDICATES or len(depth) != 40:
        x("DJ_DEPTH_COUNTS", "DJ", f"depth predicate mix differs: {mix}")
    ich = [r for r in depth if r["predicate"] == "intangible_cultural_practice"]
    if len(ich) != 3:
        x("DJ_ICH_CONTRACT", "DJ", "three inscribed elements expected")
    for r in ich:
        ref = r["value"]["data"].get("reference")
        cls, states, year = ICH_REFS.get(ref, (None, None, None))
        if cls is None:
            x("DJ_ICH_CONTRACT", r["id"], "unknown element reference")
            continue
        if (r.get("classification"), len(r["value"]["data"].get("co_states", [])), str(r["value"]["data"].get("year"))) != (cls, states, year):
            x("DJ_ICH_CONTRACT", r["id"], "classification, submitting-States count or year differs from the element page")
        if not (r.get("published") and r.get("verification_status") == "verified"):
            x("DJ_ICH_CONTRACT", r["id"], "an inscribed element is published and verified")
        if cls == "shared" and len(r["value"]["data"].get("co_states", [])) < 2:
            x("DJ_ICH_CONTRACT", r["id"], "a shared file keeps its co-submitting States")
    if not any(r["predicate"] == "convention_ratification_date" and r["value"]["data"].get("date") == "2007-08-30"
               and r.get("published") for r in depth):
        x("DJ_CONVENTION_CONTRACT", "DJ", "the 30 August 2007 ratification is missing")
    pend = [r for r in depth if r["predicate"] == "unesco_pending_nomination"]
    if len(pend) != 1 or not pend[0].get("published") or pend[0]["value"]["data"].get("year") != 2026:
        x("DJ_PENDING_NOMINATION", "DJ", "the 2026 Afar nomination must stay a stated nomination, published once")
    if any(r["predicate"] == "intangible_cultural_practice" and r["value"]["data"].get("reference") not in ICH_REFS for r in depth):
        x("DJ_PENDING_NOMINATION", "DJ", "a pending nomination may not masquerade as an inscribed element")
    consts = [r for r in depth if r["predicate"] == "constitutional_provision"]
    if {str(r["value"]["data"].get("article")) for r in consts} != {"1", "2"} or len(consts) != 3 or not all(r.get("published") for r in consts):
        x("DJ_CONSTITUTION_CONTRACT", "DJ", "articles 1 and 2 must appear once each for languages, religion and capital, published")
    langs = [r for r in depth if r["predicate"] == "language_presence"]
    official = {r["value"]["data"]["name"] for r in langs if r["value"]["data"].get("official")}
    if official != {"العربية", "الفرنسية"} or not all(r.get("published") for r in langs if r["value"]["data"].get("official")):
        x("DJ_LANGUAGE_CONTRACT", "DJ", "official languages are Arabic and French, published from article 1")
    if any(r.get("published") for r in langs if not r["value"]["data"].get("official")):
        x("DJ_LANGUAGE_CONTRACT", "DJ", "a non-official language must stay unpublished in this cycle")
    somali = next((r for r in langs if r["value"]["data"]["name"] == "الصومالية"), None)
    afar = next((r for r in langs if r["value"]["data"]["name"] == "العفرية"), None)
    if not somali or somali.get("second_source_id") != "SRC-DJ-ISO639-3-SOMALI" or "som" not in somali["value"]["data"].get("iso_codes", []):
        x("DJ_LANGUAGE_CONTRACT", "DJ", "Somali needs the ISO 639-3 som code with the registry as second source")
    if not afar or afar.get("second_source_id") != "SRC-DJ-ISO639-3-AFAR" or "aar" not in afar["value"]["data"].get("iso_codes", []):
        x("DJ_LANGUAGE_CONTRACT", "DJ", "Afar needs the ISO 639-3 aar code with the registry as second source")
    sign = next((r for r in langs if r["value"]["data"].get("level") == "signed"), None)
    if not sign or sign.get("classification") != "local" or sign.get("published") or sign["value"]["data"].get("iso_codes"):
        x("DJ_LANGUAGE_CONTRACT", "DJ", "the sign language stays unpublished with no ISO code claimed")
    blob = json.dumps([{k: v for k, v in r.items() if k != "source_locator"} for r in C], ensure_ascii=False)
    for bad in ("speakers", "نسبة المتحدث", "عدد المتحدثين", "متحدثًا", "متحدثا"):
        if bad in blob:
            x("DJ_NO_COUNTS", "DJ", f"no speaker count or share may be recorded ({bad})")
    for r in depth:
        if r["predicate"] in {"language_presence", "dialect_profile", "script_profile", "language_institution"}:
            continue
        if isinstance(r["value"]["data"], dict) and any(isinstance(v, (int, float)) and not isinstance(v, bool)
                                                       for k, v in r["value"]["data"].items() if k in ("population", "speakers", "share", "percentage")):
            x("DJ_NO_COUNTS", r["id"], "a count or share field is not accepted in this cycle")
    folk = [r for r in depth if r["predicate"] == "custom_practice" and r.get("verification_status") == "folk_narrative"]
    if len(folk) != 1 or folk[0].get("published") or "رواية شعبية" not in (folk[0].get("notes") or ""):
        x("DJ_FOLK_NARRATIVE", "DJ", "exactly one declared folk narrative, unpublished, with its status in the notes")
    disc = [r for r in depth if r["predicate"] == "administrative_counts_discrepancy"]
    if len(disc) != 1 or disc[0]["value"]["data"].get("accepted_value") != 13 or disc[0]["value"]["data"].get("mirror_value") != 35 or disc[0].get("published"):
        x("DJ_DISCREPANCY", "DJ", "the mirror count discrepancy stays stated, unpublished, with the accepted 13 kept")
    weak = [r for r in depth if r["predicate"] in {"food_dish", "clothing_item", "craft_custom", "custom_practice", "dialect_profile", "script_profile", "language_institution", "administrative_counts_discrepancy"}]
    if any(r.get("published") for r in weak):
        x("DJ_WEAK_DEPTH_PUBLISHED", "DJ", "a weak-source depth claim is published")
    if any(r.get("classification") not in {"local", "regional", "shared", "historical", "official", "national"} for r in depth):
        x("DJ_WEAK_DEPTH_CAP", "DJ", "a depth claim carries an unacceptable classification")

    # 4. Places: located_in only, no parent, no claim, no count.
    place_ids = {i for i, r in E.items() if r["entity_type"] in {"quarter", "market"}}
    expected_places = {"ENT-DJ-QUARTER-" + q["token"] for q in dd["places"]["quarters"]} | {"ENT-DJ-MARKET-" + q["token"] for q in dd["places"]["markets"]}
    if place_ids != expected_places:
        x("DJ_PLACE_CONTRACT", "entities", "place set differs from the fixture")
    for iid in sorted(place_ids):
        row = E[iid]
        rels = [r for r in R if r["child_id"] == iid]
        if row.get("status") != "historical" or row.get("verification_status") != "local_reported" or row.get("confidence") != "low":
            x("DJ_PLACE_CONTRACT", iid, "place must stay historical and local_reported on its local source")
        if len(rels) != 1 or rels[0]["relationship_type"] != "located_in" or rels[0]["parent_id"] != city:
            x("DJ_PLACE_LOCATED_IN", iid, "a place carries exactly one located_in relation to the city")
        if any(r["relationship_type"] == "administrative_parent" for r in rels):
            x("DJ_PLACE_LOCATED_IN", iid, "no administrative parent may be inferred for a place")
        if any(r["parent_id"] == iid and r["relationship_type"] == "administrative_parent" for r in R):
            x("DJ_PLACE_LOCATED_IN", iid, "no entity may be parented to a heritage place")
        if any(c["subject_id"] == iid for c in C):
            x("DJ_PLACE_CLAIMS", iid, "no claims may be attached to a place in this cycle")
        if row.get("canonical_source_id") not in {"SRC-DJ-QUARTIERS-GUIDE-2026", "SRC-DJ-CITY-HISTORY-2026"}:
            x("DJ_PLACE_CONTRACT", iid, "place source must stay on the local guides")

    # 5. Depth layers in the manifest.
    layers = {l.get("layer"): l for l in d["manifest"].get("pilot_layers", [])}
    ich_layer = layers.get("unesco_intangible_heritage")
    if not ich_layer or ich_layer.get("denominator") != 3 or ich_layer.get("coverage_record_id") is not None or ich_layer.get("scope_status") != "closed":
        x("DJ_ICH_LAYER", "manifest", "ICH layer closes at three elements with no coverage record")
    place_layer = layers.get("world_heritage_medinas")
    if not place_layer or place_layer.get("denominator") is not None or place_layer.get("scope_status") != "open" or set(place_layer.get("entity_types", [])) != {"quarter", "market"}:
        x("DJ_PLACE_LAYER", "manifest", "place layer carries no denominator and only quarter/market entities")
    know = layers.get("classified_local_knowledge")
    if not know or know.get("denominator") is not None or know.get("scope_status") != "open":
        x("DJ_KNOWLEDGE_LAYER", "manifest", "classified knowledge layer stays open with no denominator")
    return err


def main():
    d = data()
    e = validate(d)
    met = {k: len(d[k]) for k in ["entities", "relationships", "claims", "sources", "denominators", "coverage"]}
    write_json(ROOT / "reports/djibouti_validation.json", {"schema_version": "2.0.0", "country_code": "DJ",
                                                           "status": "PASS" if not e else "FAIL", "p0": len(e),
                                                           "critical_p1": 0, "metrics": met, "errors": e})
    print(json.dumps(met, ensure_ascii=False))
    print("Djibouti semantic validation passed." if not e else f"{len(e)} error(s): {e[:3]}")
    return 0 if not e else 1


if __name__ == "__main__":
    raise SystemExit(main())
