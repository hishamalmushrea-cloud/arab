#!/usr/bin/env python3
"""Comoros semantic validator: accepted Union hierarchy plus depth cycle 1."""
import json

from model import ROOT, read_jsonl, write_json

BASE_SOURCES = {"SRC-KM-LAW-11-006-AU-2011", "SRC-KM-INSEED-RGPH17-ADMIN", "SRC-UNESCO-WHC-KM-1768-2026"}
DEPTH_SOURCES = {
    "SRC-UNESCO-ICH-KM-ZAFFA-2025", "SRC-KM-CONSTITUTION-2018", "SRC-KM-ISO639-3-COMORIAN",
    "SRC-KM-MEDINAS-WIKI-2026", "SRC-KM-LANGUAGES-MIRROR-2026", "SRC-KM-COMORIAN-LANGS-WIKI-2026",
    "SRC-KM-CUISINE-MIRROR-2026", "SRC-KM-FOOD-TRAVEL-2021", "SRC-KM-FOOD-YOUM7-2022",
    "SRC-KM-CULTURE-RASEEF22-2023", "SRC-KM-CUSTOM-JAZEERA-2025", "SRC-KM-CUSTOM-MIDAD-2016",
    "SRC-KM-ECONOMY-MIRROR-2015", "SRC-KM-VOCAB-QUIZLET-2016", "SRC-KM-CULTURE-ALAYYAM-2024",
}
WHC = "SRC-UNESCO-WHC-KM-1768-2026"
ICH = "SRC-UNESCO-ICH-KM-ZAFFA-2025"
CONST = "SRC-KM-CONSTITUTION-2018"
ISO = "SRC-KM-ISO639-3-COMORIAN"
MEDINA_SRC = "SRC-KM-MEDINAS-WIKI-2026"
WEAK_CAP = {"probable", "local_reported", "unverified", "folk_narrative"}
ALLOWED_CLASS = {"local", "regional", "shared", "historical", "official"}
DEPTH_PREDICATES = {
    "intangible_cultural_practice": 1, "constitutional_provision": 3, "language_presence": 5,
    "dialect_profile": 5, "food_dish": 10, "clothing_item": 3, "craft_custom": 1, "custom_practice": 2,
    "world_heritage_criteria": 1, "world_heritage_area_hectares": 1,
    "world_heritage_buffer_zone_hectares": 1, "serial_component_names": 1,
}


def L(p):
    return json.loads(p.read_text(encoding="utf8"))


def data():
    e = [r for r in read_jsonl(ROOT / "data/entities/entities.jsonl") if r.get("country_code") == "KM"]
    ids = {r["id"] for r in e}
    sids = BASE_SOURCES | DEPTH_SOURCES
    return {
        "entities": e,
        "relationships": [r for r in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if r.get("child_id") in ids],
        "claims": [r for r in read_jsonl(ROOT / "data/claims/claims.jsonl") if r.get("subject_id") in ids],
        "sources": [L(p) for p in (ROOT / "data/sources").glob("*.json") if L(p).get("id") in sids],
        "denominators": [r for r in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if r.get("country_code") == "KM"],
        "coverage": [r for r in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if r.get("country_code") == "KM"],
        "manifest": L(ROOT / "manifests/KM.yml"),
    }


def validate(d):
    f = L(ROOT / "data/imports/comoros/fixtures/current_hierarchy_2026.json")
    dd = L(ROOT / "data/imports/comoros/fixtures/cultural_depth_2026.json")
    E = {r["id"]: r for r in d["entities"]}
    R = d["relationships"]
    C = d["claims"]
    tiers = {r["id"]: r.get("quality_tier") for r in d["sources"]}
    err = []

    def x(code, loc, msg):
        err.append({"code": code, "location": loc, "message": msg})

    depth_claims = [r for r in C if str(r.get("id", "")).startswith("CLM-KM-DEPTH")]

    # 1. Structural universe: accepted hierarchy plus the six inscribed medinas.
    cnt = {t: sum(r["entity_type"] == t for r in E.values()) for t in
           ["country", "km_island", "km_prefecture", "km_commune", "cultural_site", "quarter"]}
    if cnt != {"country": 1, "km_island": 3, "km_prefecture": 16, "km_commune": 54, "cultural_site": 1, "quarter": 6}:
        x("KM_COUNTS", "entities", str(cnt))
    for island in f["islands"]:
        iid = "ENT-KM-ISLAND-" + island["token"]
        for p in island["prefectures"]:
            pid = "ENT-KM-PREFECTURE-" + p["token"]
            if not any(r["child_id"] == pid and r["parent_id"] == iid for r in R):
                x("KM_PREFECTURE_PARENT", pid, "island parent")
            for q in p["communes"]:
                cid = "ENT-KM-COMMUNE-" + q["token"]
                if E.get(cid, {}).get("canonical_name") != q["name"] or not any(r["child_id"] == cid and r["parent_id"] == pid for r in R):
                    x("KM_COMMUNE_PARENT", cid, "prefecture parent")
    if any("MAYOTTE" in r["id"] or r.get("canonical_name") == "Mayotte" for r in E.values()):
        x("KM_MAYOTTE_CURRENT", "entities", "Mayotte excluded from current administration")
    if {r["id"]: r["value"] for r in d["denominators"]} != {"DEN-KM-COUNTRY-SCOPE": 1, "DEN-KM-ISLANDS": 3,
                                                           "DEN-KM-PREFECTURES": 16, "DEN-KM-COMMUNES": 54, "DEN-KM-WHC": 1}:
        x("KM_DENOMINATORS", "den", "1/3/16/54/1")
    w = f["world_heritage"]["entity_id"]
    if w not in E or not any(c["subject_id"] == w and c["predicate"] == "world_heritage_inscription_year" and c["value"]["data"] == 2026 for c in C):
        x("KM_WHC_2026", w, "current inscription")

    # 2. Source population and the published-claim contract.
    if {r["id"] for r in d["sources"]} != BASE_SOURCES | DEPTH_SOURCES:
        x("KM_SOURCES", "sources", "source set differs from the accepted catalog")
    tier_count = {}
    for r in d["sources"]:
        tier_count[r.get("quality_tier")] = tier_count.get(r.get("quality_tier"), 0) + 1
    if tier_count.get("A") != 6 or tier_count.get("B") != 1 or tier_count.get("E") != 11:
        x("KM_SOURCES", "sources", f"expected six A, one B and eleven E sources, got {tier_count}")
    for c in C:
        if not c.get("source_id") or not c.get("source_locator"):
            x("KM_CLAIM_SOURCE", c["id"], "claim without source or locator")
        if c.get("published") and tiers.get(c.get("source_id")) not in {"A", "B"}:
            x("KM_PUBLISHED_FROM_WEAK", c["id"], "published claim must rest on an A/B source")
        if c.get("published") and c.get("verification_status") not in {"verified", "source_verified"}:
            x("KM_PUBLISHED_STATUS", c["id"], "published claim must be verified")

    # 3. Depth cycle 1: published spine and unpublished classified body.
    mix = {}
    for r in depth_claims:
        mix[r["predicate"]] = mix.get(r["predicate"], 0) + 1
    if mix != DEPTH_PREDICATES or len(depth_claims) != 34:
        x("KM_DEPTH_COUNTS", "KM", f"depth predicate mix differs: {mix}")
    ich = [r for r in depth_claims if r.get("source_id") == ICH]
    el = dd["ich_elements"][0]
    if len(ich) != 1 or ich[0]["value"]["data"].get("reference") != el["reference"] or ich[0]["value"]["data"].get("year") != el["year"]:
        x("KM_ICH_CONTRACT", "KM", "UNESCO element reference or year differs from the fixture")
    else:
        row = ich[0]
        if row.get("classification") != "shared" or not row.get("published") or row.get("verification_status") != "verified":
            x("KM_ICH_CONTRACT", row["id"], "the element is a seven-State file: verified, published, shared")
        if sorted(row["value"]["data"].get("co_states", [])) != sorted(el["co_states"]):
            x("KM_ICH_CONTRACT", row["id"], "submitting States differ from the element page")
    for r in depth_claims:
        if r["predicate"] == "constitutional_provision":
            arts = {str(r["value"]["data"].get("article")) for r in depth_claims if r["predicate"] == "constitutional_provision"}
            break
    arts = {str(r["value"]["data"].get("article")) for r in depth_claims if r["predicate"] == "constitutional_provision"}
    if arts != {"6", "9", "10"}:
        x("KM_CONSTITUTION_CONTRACT", "KM", f"constitution articles differ: {sorted(arts)}")
    for r in depth_claims:
        if r["predicate"] == "constitutional_provision" and str(r["value"]["data"].get("article")) == "6":
            note = (r.get("notes") or "") + (r["value"]["data"].get("note") or "")
            if "مايوت" not in note or "خارج الإدارة الحالية" not in note:
                x("KM_MAYOTTE_CLAIM", r["id"], "the territorial provision must state that Mayotte is outside the current administration")
    official = [r for r in depth_claims if r["predicate"] == "language_presence" and r["value"]["data"].get("official")]
    minority = [r for r in depth_claims if r["predicate"] == "language_presence" and not r["value"]["data"].get("official")]
    if len(official) != 3 or len(minority) != 2:
        x("KM_LANGUAGE_CONTRACT", "KM", f"expected three official and two minority languages, got {len(official)}/{len(minority)}")
    for r in official:
        if not r.get("published") or r.get("source_id") != CONST:
            x("KM_LANGUAGE_CONTRACT", r["id"], "official language must be published from the constitution")
    for r in minority:
        if r.get("published") or r.get("verification_status") not in WEAK_CAP:
            x("KM_LANGUAGE_CONTRACT", r["id"], "minority language stays unpublished and capped")
    comorian = next((r for r in official if "شيكومور" in r["value"]["data"].get("name", "")), None)
    if not comorian or set(comorian["value"]["data"].get("iso_codes", [])) != {"zdj", "wni", "swb", "wlc"} or comorian.get("second_source_id") != ISO:
        x("KM_LANGUAGE_CONTRACT", "KM", "Comorian must carry the four ISO 639-3 codes with the registry as second source")
    for r in depth_claims:
        blob = json.dumps(r["value"]["data"], ensure_ascii=False)
        if any(token in blob for token in ('"speakers"', 'نسبة المتحدثين', 'نسبة المتحدث')):
            x("KM_NO_SPEAKER_NUMBERS", r["id"], "no speaker count or share may be recorded in this cycle")
    medinas = {r["id"]: r for r in E.values() if r["entity_type"] == "quarter"}
    fixture_map = {c["token"]: c for c in dd["places"]["medinas"]}
    if {r["canonical_name"] for r in medinas.values()} != {c["name"] for c in fixture_map.values()}:
        x("KM_MEDINA_CONTRACT", "entities", "medina names differ from the fixture")
    for token, c in fixture_map.items():
        iid = "ENT-KM-MEDINA-" + token
        row = medinas.get(iid, {})
        if row.get("status") != "historical" or row.get("verification_status") != "local_reported" or row.get("canonical_source_id") != MEDINA_SRC:
            x("KM_MEDINA_CONTRACT", iid, "medina must stay historical and local_reported on the mirror source")
        links = [r for r in R if r["child_id"] == iid]
        if len(links) != 1 or links[0]["relationship_type"] != "located_in" or links[0]["parent_id"] != "ENT-KM-ISLAND-" + c["island"]:
            x("KM_MEDINA_LOCATED_IN", iid, "medina requires exactly one located_in relation to its island")
        if any(r["relationship_type"] == "administrative_parent" for r in links):
            x("KM_MEDINA_ADMIN_PARENT", iid, "no administrative parent may be inferred for a medina")
        if any(r["relationship_type"] == "administrative_parent" for r in R if r["child_id"] == iid):
            x("KM_MEDINA_ADMIN_PARENT", iid, "no administrative parent may be inferred for a medina")
        if any(c2["subject_id"] == iid for c2 in C):
            x("KM_MEDINA_CLAIMS", iid, "no claims may be attached to a heritage place in this cycle")
    weak_depth = [r for r in depth_claims if r.get("source_id") != ICH and r.get("source_id") != CONST
                  and r["predicate"] not in {"world_heritage_criteria", "world_heritage_area_hectares", "world_heritage_buffer_zone_hectares"}]
    if any(r.get("published") for r in weak_depth):
        x("KM_WEAK_DEPTH_PUBLISHED", "KM", "a weak-source depth claim is published")
    if any(r.get("verification_status") not in WEAK_CAP for r in weak_depth):
        x("KM_WEAK_DEPTH_CAP", "KM", "a weak-source depth claim exceeds the local_reported cap")
    if any(not r.get("classification") for r in depth_claims):
        x("KM_WEAK_DEPTH_CAP", "KM", "a depth claim lacks classification")
    for r in depth_claims:
        if r.get("classification") not in ALLOWED_CLASS:
            x("KM_WEAK_DEPTH_CAP", r["id"], f"classification {r.get('classification')} claims exclusivity and is not accepted in this cycle")
    for r in depth_claims:
        if r["predicate"] == "dialect_profile":
            for word in r["value"]["data"].get("phrases", []):
                if len(word) != 2 or not word[1]:
                    x("KM_DIALECT_GLOSS", r["id"], "dialect phrase entry needs a word and its meaning")
            for num in r["value"]["data"].get("numerals", []):
                if len(num) != 2 or not num[1]:
                    x("KM_DIALECT_GLOSS", r["id"], "numeral entry needs a digit and its form")
    whc_extra = {r["predicate"]: r for r in depth_claims if r["source_id"] == WHC}
    exp = dd["world_heritage_extra"]
    if whc_extra.get("world_heritage_criteria", {}).get("value", {}).get("data") != exp["criteria"]:
        x("KM_WHC_EXTRA", "KM", "criteria differ from the property page")
    if whc_extra.get("world_heritage_area_hectares", {}).get("value", {}).get("data") != exp["area_hectares"]:
        x("KM_WHC_EXTRA", "KM", "property area differs from the property page")
    if whc_extra.get("world_heritage_buffer_zone_hectares", {}).get("value", {}).get("data") != exp["buffer_zone_hectares"]:
        x("KM_WHC_EXTRA", "KM", "buffer area differs from the property page")
    comp = next((r for r in depth_claims if r["predicate"] == "serial_component_names"), None)
    if not comp or len(comp["value"]["data"]) != 6 or comp.get("published"):
        x("KM_WHC_EXTRA", "KM", "component names stay unpublished with six entries")
    for r in depth_claims:
        if r["predicate"] in {"food_dish", "clothing_item", "craft_custom", "custom_practice", "dialect_profile"} and r.get("published"):
            x("KM_WEAK_DEPTH_PUBLISHED", r["id"], "classed local knowledge must stay unpublished")

    # 4. Manifest layers.
    layers = {l.get("layer"): l for l in d["manifest"].get("pilot_layers", [])}
    ich_layer = layers.get("unesco_intangible_heritage", {})
    if ich_layer.get("denominator") != 1 or ich_layer.get("coverage_record_id") is not None or ich_layer.get("scope_status") != "closed":
        x("KM_ICH_LAYER", "manifest", "ICH layer closes at one element with no coverage record")
    medina_layer = layers.get("world_heritage_medinas", {})
    if medina_layer.get("denominator") is not None or medina_layer.get("coverage_record_id") is not None or medina_layer.get("entity_types") != ["quarter"]:
        x("KM_MEDINA_LAYER", "manifest", "medina layer carries no denominator and only quarter entities")
    knowledge_layer = layers.get("classified_local_knowledge", {})
    if knowledge_layer.get("denominator") is not None or knowledge_layer.get("scope_status") != "open":
        x("KM_KNOWLEDGE_LAYER", "manifest", "classified knowledge layer stays open with no denominator")
    return err


def main():
    d = data()
    e = validate(d)
    met = {k: len(d[k]) for k in ["entities", "relationships", "claims", "sources", "denominators", "coverage"]}
    met["depth_claims"] = sum(1 for r in d["claims"] if str(r.get("id", "")).startswith("CLM-KM-DEPTH"))
    met["medinas"] = sum(r["entity_type"] == "quarter" for r in d["entities"])
    met["published_claims"] = sum(bool(r.get("published")) for r in d["claims"])
    write_json(ROOT / "reports/comoros_validation.json", {"schema_version": "2.0.0", "country_code": "KM",
                                                          "snapshot_date": "2026-09-20", "status": "PASS" if not e else "FAIL",
                                                          "p0": len(e), "critical_p1": 0, "metrics": met, "errors": e})
    print(json.dumps(met, ensure_ascii=False))
    for row in e:
        print(f"- {row['code']} {row['location']}: {row['message']}")
    print("Comoros semantic validation " + ("passed." if not e else "failed."))
    return 0 if not e else 1


if __name__ == "__main__":
    raise SystemExit(main())
