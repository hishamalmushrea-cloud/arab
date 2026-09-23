#!/usr/bin/env python3
"""Independent Mauritania review: the accepted wilaya layer plus depth cycle 1.

Opens the committed fixtures and source files itself and does not import the
importer or the semantic validator.
"""
import hashlib
import json

from model import ROOT, read_jsonl, write_json

IMPORT_DS = {'state': 'SRC-UNESCO-ICH-MR-STATE-2026', 'theydinn': 'SRC-UNESCO-ICH-THEYDINN-00524-2011',
 'mahadra': 'SRC-UNESCO-ICH-MAHADRA-01960-2023', 'samba': 'SRC-UNESCO-ICH-SAMBA-GUELADIO-01692-2024',
 'couscous': 'SRC-UNESCO-ICH-COUSCOUS-01602-2020', 'calligraphy': 'SRC-UNESCO-ICH-CALLIGRAPHY-01718-2021',
 'datepalm': 'SRC-UNESCO-ICH-DATE-PALM-01902-2022', 'engraving': 'SRC-UNESCO-ICH-ENGRAVING-01951-2023',
 'henna': 'SRC-UNESCO-ICH-HENNA-02116-2024', 'zaffa': 'SRC-UNESCO-ICH-MR-ZAFFA-02283-2025',
 'ksour': 'SRC-UNESCO-WH-MR-KSOUR-750-1996', 'whc_state': 'SRC-UNESCO-WH-MR-STATE-2026',
 'constitution': 'SRC-MR-CONSTITUTION-2012', 'iso_mey': 'SRC-MR-ISO639-3-HASSANIYA', 'iso_fuc': 'SRC-MR-ISO639-3-PULAAR',
 'iso_snk': 'SRC-MR-ISO639-3-SONINKE', 'iso_wol': 'SRC-MR-ISO639-3-WOLOF', 'iso_zen': 'SRC-MR-ISO639-3-ZENAGA',
 'iso_bam': 'SRC-MR-ISO639-3-BAMBARA', 'iso_taq': 'SRC-MR-ISO639-3-TAMASHEQ', 'iso_srr': 'SRC-MR-ISO639-3-SERER',
 'languages': 'SRC-MR-LANGUAGES-MIRROR-2026', 'hassaniya': 'SRC-MR-HASSANIYA-MIRROR-2026',
 'cuisine': 'SRC-MR-CUISINE-MIRROR-2026', 'dress': 'SRC-MR-DRESS-MIRROR-2026', 'nouakchott': 'SRC-MR-NOUAKCHOTT-MIRROR-2026',
 'press2010': 'SRC-MR-NOUAKCHOTT-ALKHALEEJ-2010', 'towns': 'SRC-MR-TOWNS-MIRROR-2026', 'sites': 'SRC-MR-SITES-MIRROR-2026',
 'dgat': 'SRC-MR-DGAT-15-63-2026', 'ansade': 'SRC-MR-ANSADE-RGPH5-2024', 'peer': 'SRC-MR-ANSADE-PEER-REVIEW-2024'}


def L(p):
    return json.loads(p.read_text(encoding="utf8"))


def main():
    I = ROOT / "data/imports/mauritania"
    wil_path = I / "fixtures/wilaya_profiles.json"
    depth_path = I / "fixtures/cultural_depth_2026.json"
    manifest = L(I / "snapshot_manifest.json")
    expected = {r["path"]: r["sha256"] for r in manifest["records"]}
    fails = []

    def check(cond, record_id, message):
        if not cond:
            fails.append({"severity": "P1", "record_id": record_id, "message": message})

    for path, key in ((wil_path, "data/imports/mauritania/fixtures/wilaya_profiles.json"),
                      (depth_path, "data/imports/mauritania/fixtures/cultural_depth_2026.json")):
        check(hashlib.sha256(path.read_bytes()).hexdigest() == expected.get(key), key,
              "fixture checksum differs from the committed manifest")

    wil = L(wil_path)
    depth = L(depth_path)

    entities = [r for r in read_jsonl(ROOT / "data/entities/entities.jsonl") if r.get("country_code") == "MR"]
    ids = {r["id"] for r in entities}
    relationships = [r for r in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if r.get("child_id") in ids]
    claims = [r for r in read_jsonl(ROOT / "data/claims/claims.jsonl") if r.get("subject_id") in ids]
    denominators = [r for r in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if r.get("country_code") == "MR"]
    coverage = [r for r in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if r.get("country_code") == "MR"]
    sources = [L(p) for p in sorted((ROOT / "data/sources").glob("*.json")) if L(p).get("country_codes") == ["MR"]]
    tier_of = {s["id"]: s.get("quality_tier") for s in sources}

    E = {r["id"]: r for r in entities}
    check(len(entities) == 23 and len([1 for r in entities if r["entity_type"] == "mr_wilaya"]) == 15, "entities",
          "the accepted layer plus the seven heritage places do not add up")
    check(len(sources) == 32 and set(tier_of.values()) <= {"A", "B", "E"}, "sources", "source catalogue shape differs")

    # Accepted wilaya layer, read from the roadmap fixture itself.
    for q in wil["wilayas"]:
        eid = "ENT-MR-WILAYA-" + q["code"]
        check(E.get(eid, {}).get("canonical_name") == q["name_fr"], eid, "wilaya identity differs from the fixture")
        check(any(c["subject_id"] == eid and c["predicate"] == "administrative_profile" and c["value"]["data"] == q["profile"]
                  for c in claims), eid, "wilaya profile differs from the fixture")
        check(any(r["child_id"] == eid and r["parent_id"] == "ENT-MR-COUNTRY" and r["relationship_type"] == "administrative_parent"
                  for r in relationships), eid, "wilaya is not parented to the country")
    check({r["id"]: r["value"] for r in denominators} == {"DEN-MR-COUNTRY-SCOPE": 1, "DEN-MR-WILAYAS": 15,
                                                           "DEN-MR-NOUAKCHOTT-WILAYAS": 3, "DEN-MR-REGIONAL-WILAYAS": 12},
          "denominators", "accepted denominators changed")
    check(not [r for r in entities if r["entity_type"] in {"mr_moughataa", "mr_commune"}], "lower levels",
          "a second-level record was created before its register is documented")

    # UNESCO intangible heritage, read from the element pages recorded in the fixture.
    ich = {str(c["value"]["data"].get("reference")): c for c in claims if c["predicate"] == "intangible_cultural_practice"}
    check(len(ich) == len(depth["ich_elements"]) == 9, "ich", "expected nine inscribed elements")
    for el in depth["ich_elements"]:
        row = ich.get(str(el["reference"]))
        check(row is not None, "ENT-MR-ICH-" + str(el["reference"]), "element from the fixture is missing")
        if not row:
            continue
        payload = row["value"]["data"]
        check(payload.get("year") == el["year"] and payload.get("list") == el["list"], row["id"], "year or list differs from the fixture")
        check(sorted(payload.get("co_states", [])) == sorted(el["co_states"]), row["id"], "submitting States differ from the fixture")
        check(payload.get("description") == el["description"] and payload.get("name") == el["name"], row["id"], "element wording differs from the fixture")
        check(row.get("classification") == el["classification"], row["id"], "classification differs from the fixture")
        check("موريتانيا" in payload.get("co_states", []), row["id"], "Mauritania is missing from the co-states")
        check(row.get("published") and row.get("verification_status") == "verified", row["id"], "an inscribed element is not published and verified")
        check(tier_of.get(row.get("source_id")) == "A", row["id"], "element claim does not rest on the element page")
        check(row.get("source_id") == IMPORT_DS.get(el["source"]), row["id"], "element claim does not cite the fixture source")
        solo = len(payload.get("co_states", [])) == 1
        check(solo == (el["classification"] == "national"), row["id"], "sole submission and national classification disagree")
    pending = [r for r in claims if r["predicate"] == "unesco_pending_nomination"]
    check(len(pending) == len(depth["pending_nominations"]) == 3, "pending", "expected three declared nominations")
    for p in depth["pending_nominations"]:
        row = next((r for r in pending if r["value"]["data"].get("element") == p["element"]), None)
        check(row is not None and row["value"]["data"].get("year") == p["year"] and row["value"]["data"].get("list") == p["list"],
              "nomination " + p["element"][:20], "nomination differs from the fixture")
        if row:
            check(row["value"]["data"].get("status") == "قيد النظر" and row.get("published"), row["id"], "nomination is not recorded as still pending")
    check(not [r for r in claims if r["predicate"] == "intangible_cultural_practice"
               and r["value"]["data"].get("name") in {p["element"] for p in depth["pending_nominations"]}], "pending",
          "a pending nomination was recorded as an inscribed element")
    check(len([r for r in claims if r["predicate"] == "convention_ratification_date"
               and r["value"]["data"].get("date") == "2006-11-15" and r.get("published")]) == 1, "ratification",
          "ratification date missing")

    # World Heritage, readable from the state page and the property pages.
    wh = {str(c["value"]["data"].get("reference")): c for c in claims if c["predicate"] == "world_heritage_property"}
    check(len(wh) == len(depth["world_heritage_properties"]) == 2, "world heritage", "expected two properties")
    for el in depth["world_heritage_properties"]:
        row = wh.get(str(el["reference"]))
        check(row is not None and row["value"]["data"].get("criteria") == el["criteria"] and row["value"]["data"].get("category") == el["category"],
              "property " + str(el["reference"]), "criteria or category differs from the fixture")
        if row:
            check(row["value"]["data"].get("year") == el["year"] and row["value"]["data"].get("name") == el["name"], row["id"], "property identity differs from the fixture")
            check(row.get("published") and row.get("verification_status") == "verified", row["id"], "property is not published and verified")
    natural = next(r for r in wh.values() if r["value"]["data"].get("category") == "طبيعي")
    check(natural["value"]["data"].get("criteria") == [], natural["id"], "the natural property carries criteria that the source did not read")
    tent = {str(c["value"]["data"].get("reference")): c for c in claims if c["predicate"] == "unesco_tentative_listing"}
    check(len(tent) == len(depth["tentative_sites"]) == 3, "tentative", "expected three tentative sites")
    for el in depth["tentative_sites"]:
        row = tent.get(str(el["reference"]))
        check(row is not None and row["value"]["data"].get("name") == el["name"] and row["value"]["data"].get("year") == el["year"],
              "tentative " + str(el["reference"]), "tentative listing differs from the fixture")
        if row:
            check(row.get("published") and row["classification"] == "official", row["id"], "tentative listing is not recorded as an official pending listing")
    check(not ({*tent} & {*wh}), "tentative", "a tentative site is recorded as an inscribed property")

    # Constitution, compared with the fixture text record.
    consts = {str(r["value"]["data"].get("article")): r for r in claims if r["predicate"] == "constitutional_provision"}
    for p in depth["constitution_provisions"]:
        row = consts.get(str(p["article"]))
        check(row is not None and row["value"]["data"].get("summary") == p["summary"] and row["value"]["data"].get("topic") == p["topic"],
              "article " + str(p["article"]), "constitutional provision differs from the fixture")
        if row:
            check(row.get("published") and row.get("verification_status") == "verified", row["id"], "constitutional provision is not published")
            check(tier_of.get(row.get("source_id")) == "A", row["id"], "constitutional provision does not rest on the constitution source")
            check(row.get("source_id") == IMPORT_DS["constitution"], row["id"], "constitutional provision cites another source")

    # Language body, compared with the fixture.
    langs = {r["value"]["data"]["name"]: r for r in claims if r["predicate"] == "language_presence"}
    fixture_lang = {l["name"]: l for l in depth["language_presence"]}
    check(set(langs) == set(fixture_lang), "languages", "language set differs from the fixture")
    for name, row in langs.items():
        l = fixture_lang[name]
        check(row["value"]["data"].get("official") == l["official"] and row["value"]["data"].get("level") == l["level"], row["id"], "language flag or level differs from the fixture")
        check(sorted(row["value"]["data"].get("iso_codes", [])) == sorted(l["codes"]), row["id"], "ISO codes differ from the fixture")
        check(row.get("published") == (l["level"] in {"official", "national"}), row["id"], "publishing does not follow the level rule")
        if l["second"]:
            check(row.get("second_source_id") == IMPORT_DS.get(l["second"]) and row.get("second_source_locator"), row["id"], "second source is not the registry entry from the fixture")
        else:
            check(not row.get("second_source_id"), row["id"], "an unregistered language claims a second source")
        check("عدد متحدثين" in (row["value"]["data"].get("note") or ""), row["id"], "the no-count rule is not stated on the record")
    check(langs["العربية"]["value"]["data"]["iso_codes"] == [], "العربية", "an ISO code is recorded for Arabic in this cycle")
    check(not langs["الفرنسية"]["value"]["data"]["official"], "الفرنسية", "French is recorded as official")
    check(not langs["لغة الإشارة الإفريقية الفرنكوفونية"]["value"]["data"]["iso_codes"], "sign language", "an unverified ISO code is recorded for sign language")

    # Weak local knowledge: recorded, classified and never published.
    for pred, items, key in (("food_dish", depth["dishes"], "name"), ("clothing_item", depth["dress"], "name"),
                             ("craft_custom", depth["crafts"], "name"), ("custom_practice", depth["customs"], "name")):
        rows = [r for r in claims if r["predicate"] == pred]
        check(len(rows) == len(items), pred, f"expected {len(items)} rows, found {len(rows)}")
        check(sorted(r["value"]["data"][key] for r in rows) == sorted(i[key] for i in items), pred, "row names differ from the fixture")
        for r in rows:
            check(not r.get("published"), r["id"], "a weak local claim is published")
            check(r.get("verification_status") == "local_reported", r["id"], "a weak local claim is not marked local_reported")
    narr = [r for r in claims if r["predicate"] in {"folk_narrative", "place_name_narrative"}]
    check(len(narr) == len(depth["narratives"]) == 2, "narratives", "expected a folk narrative and a naming narrative")
    folk = next(r for r in narr if r["predicate"] == "folk_narrative")
    check(folk["verification_status"] == "folk_narrative" and folk["classification"] == "folk_narrative" and not folk.get("published"),
          folk["id"], "the folk narrative is not isolated from fact")
    check(all(not r.get("published") for r in narr), "narratives", "a narrative is published")
    dialect = [r for r in claims if r["predicate"] == "dialect_profile"]
    script = [r for r in claims if r["predicate"] == "script_profile"]
    check(len(dialect) == 1 and dialect[0]["value"]["data"].get("features") == depth["dialect_profiles"][0]["features"], "dialect",
          "dialect profile differs from the fixture")
    check(len(script) == 1 and script[0]["value"]["data"].get("features") == depth["script_profiles"][0]["features"], "script",
          "script profile differs from the fixture")
    check(dialect[0]["value"]["data"]["features"].get("iso") == "mey" and tier_of.get(dialect[0]["source_id"]) == "E", "dialect",
          "dialect profile does not rest on the mirror")
    check(not dialect[0].get("published") and not script[0].get("published"), "dialect/script", "a mirror profile is published")
    founding = [r for r in claims if r["predicate"] == "city_founding"]
    check(len(founding) == 1 and founding[0]["value"]["data"].get("detail") == depth["city_founding"]["desc"] and not founding[0].get("published"),
          "capital history", "capital history differs from the fixture or is published")

    # Citation unit, the publication rule and the no-numbers rule.
    for row in claims:
        check(bool(row.get("second_source_id")) == bool(row.get("second_source_locator")), row["id"], "second source and second source locator must occur together")
        if row.get("published"):
            check(row.get("verification_status") in {"verified", "source_verified"}, row["id"], "published claim is not verified")
            check(tier_of.get(row.get("source_id")) == "A", row["id"], "published claim does not rest on an A source")
    blob = json.dumps(claims, ensure_ascii=False)
    for bad in ("عدد المتحدثين", "عدد السكان", "speakers", "705,500", "5.6", "70-80", "15%", "1-3%"):
        check(bad not in blob, "counts", f"a count leaked into the records ({bad})")
    numbers = [(c["id"], c["predicate"]) for c in claims
               if c["predicate"] in {"food_dish", "clothing_item", "craft_custom", "custom_practice", "dialect_profile", "script_profile", "language_presence"}
               and isinstance(c["value"]["data"], dict)
               and any(isinstance(v, (int, float)) and not isinstance(v, bool) for v in c["value"]["data"].values())]
    check(not numbers, "counts", "a weak depth claim carries a number field")
    published = [c for c in claims if c.get("published")]
    check(all(c["source_id"] in tier_of for c in published), "publishing", "a published claim cites an unknown source")
    check(sum(1 for c in claims if str(c["id"]).startswith("CLM-MR-DEPTH") and c.get("published")) == 27, "publishing",
          "the published depth set changed size")

    # Places: located_in only, no parent, no claim, no count.
    fixture_places = {"ENT-MR-TOWN-" + q["latin"].upper().replace(" ", "-"): q for q in depth["places"]["towns"]} | \
                     {"ENT-MR-SITE-" + q["latin"].upper().replace(" ", "-"): q for q in depth["places"]["sites"]}
    place_ids = {i for i, r in E.items() if r["entity_type"] in {"city", "archaeological_site"}}
    check(place_ids == set(fixture_places), "places", "place set differs from the fixture")
    for iid in sorted(place_ids):
        q = fixture_places[iid]
        rels = [r for r in relationships if r["child_id"] == iid]
        parent = "ENT-MR-WILAYA-" + q["wilaya"] if q.get("wilaya") else "ENT-MR-COUNTRY"
        check(len(rels) == 1 and rels[0]["relationship_type"] == "located_in" and rels[0]["parent_id"] == parent, iid,
              "place does not sit on a single located_in relation to its fixtured parent")
        check(expected_place_type := (iid.startswith("ENT-MR-TOWN-") and E[iid]["entity_type"] == "city") or
              (iid.startswith("ENT-MR-SITE-") and E[iid]["entity_type"] == "archaeological_site"), iid, "place type does not follow the fixture class")
        check(not any(c["subject_id"] == iid for c in claims), iid, "a place carries a claim")
        check(not E[iid].get("coordinates"), iid, "a place carries coordinates in this cycle")
        check(E[iid].get("status") == "current" and q["note"] in (E[iid].get("notes") or "") and E[iid].get("source_locator") == E[iid].get("notes"), iid,
              "place text differs from the fixture")
        tier = tier_of.get(E[iid].get("canonical_source_id"))
        if tier == "E":
            check(E[iid].get("verification_status") == "local_reported" and E[iid].get("confidence") == "low", iid, "mirror-sourced place is not kept weak")
        elif tier == "A":
            check(E[iid].get("verification_status") == "source_verified" and E[iid].get("confidence") == "high", iid, "UNESCO-sourced place is not recorded as source verified")
        else:
            check(False, iid, "place source tier is not A or E")
    check(not any(r["relationship_type"] == "administrative_parent" for r in relationships if r["child_id"] in place_ids or r["parent_id"] in place_ids),
          "places", "an administrative path touches a heritage place")

    # The stated count conflict and the depth layer shapes.
    disc = [c for c in claims if c["predicate"] == "commune_count_candidates"]
    check(len(disc) == 1 and sorted(disc[0]["value"]["data"]) == [219, 220], "commune count", "the commune conflict is not recorded as stated")
    if disc:
        check(disc[0]["classification"] == "disputed" and disc[0].get("unit") == "commune" and disc[0].get("published"), disc[0]["id"], "the commune conflict is not recorded as an open published conflict")
    mough = [c for c in claims if c["predicate"] == "moughataa_count"]
    layers = {l.get("layer"): l for l in L(ROOT / "manifests/MR.yml").get("pilot_layers", [])}
    check(len(layers) == 7, "layers", "layer set changed")
    check(layers.get("unesco_intangible_heritage", {}).get("denominator") == 9 and layers.get("unesco_intangible_heritage", {}).get("coverage_record_id") is None,
          "ich layer", "ICH layer shape differs")
    check(layers.get("world_heritage_properties", {}).get("denominator") == 2 and layers.get("world_heritage_properties", {}).get("scope_status") == "closed",
          "wh layer", "World Heritage layer shape differs")
    for layer in ("heritage_places", "classified_local_knowledge"):
        check(layers.get(layer, {}).get("denominator") is None and layers.get(layer, {}).get("scope_status") == "open", layer,
              "an open layer carries a denominator")
    check(len(mough) == 1 and len([1 for r in entities if r["entity_type"] == "mr_wilaya"]) == layers.get("mr_wilaya", {}).get("denominator") == 15,
          "counts", "the wilaya denominator and the recorded counts disagree")
    h = {x["entity_type"]: x for x in L(ROOT / "manifests/MR.yml").get("hierarchy", [])}
    check(h.get("mr_moughataa", {}).get("denominator") == 63 and mough and mough[0]["value"]["data"] == 63, "moughataa",
          "the 63 moughataa count is not carried as an open known count")
    check(h.get("mr_commune", {}).get("denominator") is None and h.get("mr_commune", {}).get("scope_status") == "open", "communes",
          "the commune layer is closed while the register counts conflict")

    families = {"entities": entities, "relationships": relationships, "claims": claims, "sources": sources,
                "denominators": denominators, "coverage": coverage}
    total_rows = sum(len(v) for v in families.values())
    ok = not fails
    sample = {k: {"population": len(v), "sample_size": len(v), "sample_percentage": 100.0,
                  "record_ids": sorted(x["id"] for x in v)} for k, v in families.items()}
    write_json(ROOT / "data/review/mauritania_review_samples.json", {"schema_version": "2.0.0", "country_code": "MR", "families": sample})
    write_json(ROOT / "reports/mauritania_review_samples.json", {"schema_version": "2.0.0", "country_code": "MR", "families": sample})
    result = {k: {"sampled": len(v), "passed": len(v) if ok else 0, "failed": 0 if ok else len(v),
                  "status": "PASS" if ok else "FAIL"} for k, v in families.items()}
    write_json(ROOT / "reports/mauritania_independent_review.json",
               {"schema_version": "2.0.0", "country_code": "MR", "status": "PASS" if ok else "FAIL", "p0": 0,
                "critical_p1": len(fails),
                "method": "Independent fixture and checksum comparison over the full Mauritania population; importer and semantic validator not imported.",
                "families": result, "total_sampled": total_rows, "total_passed": total_rows if ok else 0, "findings": fails})
    print(total_rows)
    for f in fails[:8]:
        print(f)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
