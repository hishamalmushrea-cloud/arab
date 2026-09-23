#!/usr/bin/env python3
"""Independent Djibouti review: topology plus depth cycle 1.

Opens the committed fixtures and source files itself and does not import the
importer or the semantic validator.
"""
import hashlib
import json

from model import ROOT, read_jsonl, write_json


def L(p):
    return json.loads(p.read_text(encoding="utf8"))


def main():
    I = ROOT / "data/imports/djibouti"
    topo_path = I / "fixtures/topology_2024.json"
    depth_path = I / "fixtures/cultural_depth_2026.json"
    manifest = L(I / "snapshot_manifest.json")
    expected = {r["path"]: r["sha256"] for r in manifest["records"]}
    fails = []

    def check(cond, record_id, message):
        if not cond:
            fails.append({"severity": "P1", "record_id": record_id, "message": message})

    for path, key in ((topo_path, "data/imports/djibouti/fixtures/topology_2024.json"),
                      (depth_path, "data/imports/djibouti/fixtures/cultural_depth_2026.json")):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        check(digest == expected.get(key), key, "fixture checksum differs from the committed manifest")

    topo = L(topo_path)
    depth = L(depth_path)

    entities = [r for r in read_jsonl(ROOT / "data/entities/entities.jsonl") if r.get("country_code") == "DJ"]
    ids = {r["id"] for r in entities}
    relationships = [r for r in read_jsonl(ROOT / "data/relationships/relationships.jsonl")
                     if r.get("child_id") in ids or r.get("parent_id") in ids]
    claims = [r for r in read_jsonl(ROOT / "data/claims/claims.jsonl") if r.get("subject_id") in ids]
    denominators = [r for r in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if r.get("country_code") == "DJ"]
    coverage = [r for r in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if r.get("country_code") == "DJ"]

    source_rows = [L(p) for p in sorted((ROOT / "data/sources").glob("*.json"))]
    sources = [s for s in source_rows if s.get("country_codes") == ["DJ"]]
    tier_of = {s["id"]: s.get("quality_tier") for s in sources}

    E = {r["id"]: r for r in entities}
    city = "ENT-DJ-DJIBOUTI-CITY"

    # Accepted topology, read from the census fixture itself.
    check(E.get(city, {}).get("canonical_name") == "Djibouti-Ville", city, "special-status city row missing")
    for g in topo["regions"]:
        gid = "ENT-DJ-REGION-" + g["token"]
        check(gid in E, gid, "region row missing")
        for q in g["subprefectures"]:
            sid = "ENT-DJ-SUBPREFECTURE-" + q["token"]
            check(E.get(sid, {}).get("canonical_name") == q["name_fr"], sid, "sub-prefecture identity differs from the roadmap fixture")
            check(any(r["child_id"] == sid and r["parent_id"] == gid for r in relationships), sid, "sub-prefecture parent differs from the fixture")
        check(any(c["subject_id"] == gid and c["predicate"] == "population" and c["value"]["data"] == g["population"] for c in claims), gid, "region population differs from the census fixture")
    for q in topo["city"]["communes"]:
        cid = "ENT-DJ-COMMUNE-" + q["token"]
        check(E.get(cid, {}).get("canonical_name") == q["name_fr"], cid, "commune identity differs from the law fixture")
        check(any(r["child_id"] == cid and r["parent_id"] == city for r in relationships), cid, "commune is not under the special-status city")
    total = sum(c["value"]["data"] for c in claims if c["predicate"] == "population")
    check(total == topo["population_total"], "population", "regional plus city rows do not reconcile to the national total")
    check({r["id"]: r["value"] for r in denominators} == {"DEN-DJ-COUNTRY-SCOPE": 1, "DEN-DJ-REGIONS": 5,
                                                           "DEN-DJ-SPECIAL-CITY": 1, "DEN-DJ-CITY-COMMUNES": 3,
                                                           "DEN-DJ-SUBPREFECTURES": 13}, "denominators", "accepted denominators changed")

    # UNESCO spine, read from the element pages recorded in the fixture.
    ich = [r for r in claims if r["predicate"] == "intangible_cultural_practice"]
    check(len(ich) == len(depth["ich_elements"]) == 3, "ich", "expected three inscribed elements")
    fixture_el = {e["reference"]: e for e in depth["ich_elements"]}
    for row in ich:
        payload = row["value"]["data"]
        el = fixture_el.get(payload.get("reference"))
        check(el is not None, row["id"], "element reference is not in the fixture")
        if not el:
            continue
        check(payload.get("year") == el["year"], row["id"], "inscription year differs from the fixture")
        check(payload.get("list") == el["list"], row["id"], "list differs from the fixture")
        check(sorted(payload.get("co_states", [])) == sorted(el["co_states"]), row["id"], "submitting States differ from the fixture")
        check(row.get("classification") == el["classification"], row["id"], "classification differs from the fixture")
        check(row.get("published") and row.get("verification_status") == "verified", row["id"], "an inscribed element is published and verified")
        check(tier_of.get(row.get("source_id")) == "A", row["id"], "element claim does not rest on the element page")
        shared = [s for s in payload.get("co_states", []) if s != "جيبوتي"]
        check((len(payload.get("co_states", [])) > 1) == (el["classification"] == "shared"), row["id"], "shared files keep their co-submitting States")
    pending = [r for r in claims if r["predicate"] == "unesco_pending_nomination"]
    check(len(pending) == 1 and pending[0]["value"]["data"].get("year") == 2026 and pending[0].get("published"), "pending", "the 2026 nomination is not recorded once as stated")
    check(len([r for r in claims if r["predicate"] == "convention_ratification_date" and r["value"]["data"].get("date") == "2007-08-30"]) == 1, "ratification", "ratification date missing")

    # Constitution, compared with the fixture text record.
    consts = {(str(r["value"]["data"].get("article")), r["value"]["data"].get("topic")): r for r in claims if r["predicate"] == "constitutional_provision"}
    for p in depth["constitution_provisions"]:
        row = consts.get((str(p["article"]), p["topic"]))
        check(row is not None and row.get("published") and row["value"]["data"].get("summary") == p["summary"], f"article {p['article']} {p['topic']}", "constitutional provision differs from the fixture")
        if row:
            check(tier_of.get(row.get("source_id")) == "A", row["id"], "constitutional provision does not rest on the constitution source")

    # Language body, compared with the fixture.
    langs = {r["value"]["data"]["name"]: r for r in claims if r["predicate"] == "language_presence"}
    fixture_lang = {l["name"]: l for l in depth["language_presence"]}
    check(set(langs) == set(fixture_lang), "languages", "language set differs from the fixture")
    for name, row in langs.items():
        l = fixture_lang[name]
        check(row["value"]["data"].get("official") == l["official"], row["id"], "official flag differs from the fixture")
        check(sorted(row["value"]["data"].get("iso_codes", [])) == sorted(l.get("codes", [])), row["id"], "ISO codes differ from the fixture")
        if l["official"]:
            check(row.get("published"), row["id"], "an official language is not published")
        else:
            check(not row.get("published"), row["id"], "a non-official language is published")
    for name, src_id in (("الصومالية", "SRC-DJ-ISO639-3-SOMALI"), ("العفرية", "SRC-DJ-ISO639-3-AFAR")):
        row = langs[name]
        check(row.get("second_source_id") == src_id and row.get("second_source_locator"), row["id"], "national language does not carry the ISO registry citation")
    for name in ("العربية", "الفرنسية"):
        check(langs[name]["value"]["data"].get("iso_codes") == [], name, "no ISO code is recorded for an official language in this cycle")

    # Citation unit, publication rule and the no-numbers rule.
    for row in claims:
        check(bool(row.get("second_source_id")) == bool(row.get("second_source_locator")), row["id"], "second source and second source locator must occur together")
        if row.get("published"):
            check(row.get("verification_status") in {"verified", "source_verified"}, row["id"], "published claim is not verified")
            check(row.get("source_id") in tier_of, row["id"], "published claim cites an unknown source")
            check(tier_of.get(row["source_id"]) in {"A", "B"}, row["id"], "published claim does not rest on an A/B source")
    blob = json.dumps(claims, ensure_ascii=False)
    for bad in ("عدد المتحدثين", "نسبة المتحدث", "speakers", "524,000", "306,000", "59,000", "38,900", "17,000"):
        check(bad not in blob, "counts", f"a speaker count leaked into the records ({bad})")
    numbers = [(c["id"], c["predicate"]) for c in claims
               if c["predicate"] in {"food_dish", "clothing_item", "craft_custom", "custom_practice"}
               and isinstance(c["value"]["data"], dict)
               and any(isinstance(v, (int, float)) and not isinstance(v, bool) for v in c["value"]["data"].values())]
    check(not numbers, "counts", "a weak depth claim carries a number field")

    # Places: located_in only, no parent, no claim, no count.
    fixture_places = {"ENT-DJ-QUARTER-" + q["token"] for q in depth["places"]["quarters"]} | {"ENT-DJ-MARKET-" + q["token"] for q in depth["places"]["markets"]}
    place_ids = {i for i, r in E.items() if r["entity_type"] in {"quarter", "market"}}
    check(place_ids == fixture_places, "places", "place set differs from the fixture")
    for iid in sorted(place_ids):
        rels = [r for r in relationships if r["child_id"] == iid]
        check(len(rels) == 1 and rels[0]["relationship_type"] == "located_in" and rels[0]["parent_id"] == city, iid, "place does not sit on a single located_in relation to the city")
        check(not any(r["relationship_type"] == "administrative_parent" and (r["child_id"] == iid or r["parent_id"] == iid) for r in relationships), iid, "an administrative parent touches a heritage place")
        check(not any(c["subject_id"] == iid for c in claims), iid, "a place carries a claim")
        check(E[iid].get("status") == "historical" and E[iid].get("verification_status") == "local_reported", iid, "place status or verification differs from the layer contract")

    # The stated mirror discrepancy and the depth layers.
    disc = [c for c in claims if c["predicate"] == "administrative_counts_discrepancy"]
    check(len(disc) == 1 and disc[0]["value"]["data"].get("accepted_value") == 13 and disc[0]["value"]["data"].get("mirror_value") == 35 and not disc[0].get("published"), "discrepancy", "the mirror count discrepancy is not recorded as stated and unpublished")
    layers = {l.get("layer"): l for l in L(ROOT / "manifests/DJ.yml").get("pilot_layers", [])}
    check(layers.get("unesco_intangible_heritage", {}).get("denominator") == 3 and layers.get("unesco_intangible_heritage", {}).get("coverage_record_id") is None, "ich layer", "ICH layer shape differs")
    check(layers.get("world_heritage_medinas", {}).get("denominator") is None and layers.get("world_heritage_medinas", {}).get("scope_status") == "open", "place layer", "place layer shape differs")
    check(layers.get("classified_local_knowledge", {}).get("denominator") is None, "knowledge layer", "classified layer shape differs")

    families = {"entities": entities, "relationships": relationships, "claims": claims, "sources": sources,
                "denominators": denominators, "coverage": coverage}
    total_rows = sum(len(v) for v in families.values())
    ok = not fails
    sample = {k: {"population": len(v), "sample_size": len(v), "sample_percentage": 100.0,
                  "record_ids": sorted(x["id"] for x in v)} for k, v in families.items()}
    write_json(ROOT / "data/review/djibouti_review_samples.json", {"schema_version": "2.0.0", "country_code": "DJ", "families": sample})
    write_json(ROOT / "reports/djibouti_review_samples.json", {"schema_version": "2.0.0", "country_code": "DJ", "families": sample})
    result = {k: {"sampled": len(v), "passed": len(v) if ok else 0, "failed": 0 if ok else len(v),
                  "status": "PASS" if ok else "FAIL"} for k, v in families.items()}
    write_json(ROOT / "reports/djibouti_independent_review.json",
               {"schema_version": "2.0.0", "country_code": "DJ", "status": "PASS" if ok else "FAIL", "p0": 0,
                "critical_p1": len(fails), "method": "Independent fixture and checksum comparison over the full Djibouti population; importer and semantic validator not imported.",
                "families": result, "total_sampled": total_rows, "total_passed": total_rows if ok else 0, "findings": fails})
    print(total_rows)
    for f in fails[:5]:
        print(f)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
