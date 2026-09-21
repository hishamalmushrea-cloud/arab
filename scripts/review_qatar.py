#!/usr/bin/env python3
"""Independent full Qatar review: opens committed evidence and does not import the importer or validator."""
import hashlib
import json

from model import ROOT, read_jsonl, write_json

DEPTH_DATE = "2026-09-20"
DEPTH_SOURCES = {
    "SRC-QA-UNESCO-ICH-2026", "SRC-QA-CUISINE-MIRROR-2026", "SRC-QA-DIALECT-DOHA24-2025",
    "SRC-QA-DIALECT-FORUM-2010", "SRC-QA-DRESS-JAZEERA-2018", "SRC-QA-DRESS-QNA-2023",
    "SRC-QA-DRESS-KHALEEJ-2016", "SRC-QA-FIRJAN-PRESS-2024", "SRC-QA-FIRJAN-NAJADA-2022",
    "SRC-QA-SOUQ-WAQIF-2012",
}
SHARED_DISHES = {"المجبوس", "المحمر", "الشيلاني", "المضروبة", "الهريس", "الجريث", "الجريش",
                 "الثريد", "المرقوقة", "البلاليط", "العصيدة", "اللقيمات", "الخنفروش",
                 "الزلابية", "الرهش", "الكرك", "المشخول"}


def L(p):
    return json.loads(p.read_text(encoding="utf8"))


def main():
    f = L(ROOT / "data/imports/qatar/fixtures/municipalities_census_2020.json")
    scope = L(ROOT / "data/imports/qatar/fixtures/official_scope_2026.json")
    depth = L(ROOT / "data/imports/qatar/fixtures/cultural_depth_2026.json")
    manifest = L(ROOT / "data/imports/qatar/snapshot_manifest.json")
    e = [r for r in read_jsonl(ROOT / "data/entities/entities.jsonl") if r.get("country_code") == "QA"]
    ids = {r["id"] for r in e}
    families = {
        "entities": e,
        "aliases": [r for r in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if r.get("entity_id") in ids],
        "relationships": [r for r in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if r.get("child_id") in ids],
        "claims": [r for r in read_jsonl(ROOT / "data/claims/claims.jsonl") if r.get("subject_id") in ids],
        "denominators": [r for r in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if r.get("country_code") == "QA"],
        "coverage": [r for r in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if r.get("country_code") == "QA"],
    }
    sids = {L(p).get("id") for p in (ROOT / "data/sources").glob("*.json")}
    source_rows = [L(p) for p in (ROOT / "data/sources").glob("*.json") if L(p).get("country_codes") == ["QA"]]
    families["sources"] = source_rows
    sids = {r["id"] for r in source_rows}
    claims = families["claims"]
    rels = families["relationships"]
    aliases = families["aliases"]
    find = []

    def bad(fam, rid, msg):
        find.append({"severity": "P1", "family": fam, "record_id": rid, "message": msg})

    # Evidence files are independently checksum-opened.
    for item in manifest["records"]:
        path = ROOT / item["path"]
        payload = path.read_bytes()
        if len(payload) != item["bytes"] or hashlib.sha256(payload).hexdigest() != item["sha256"]:
            bad("sources", item["path"], "fixture checksum/size mismatch")
    if any(r.get("predicate") == "language_presence" for r in claims):
        bad("claims", "QA-language", "language presence claim exists although none was accepted")

    # Base layer against the PSA census fixture.
    expected = {r["name_ar"]: (r["name_en"], r["population"]) for r in f["records"]}
    actual = {r["canonical_name"]: r for r in e if r["entity_type"] == "qa_municipality"}
    if set(actual) != set(expected) or len(actual) != 8:
        bad("entities", "QA-municipalities", "eight-municipality set mismatch")
    for ar, (en, pop) in expected.items():
        eid = actual.get(ar, {}).get("id")
        if not eid:
            continue
        if not any(a["entity_id"] == eid and a["name"] == en for a in aliases):
            bad("aliases", eid, "English alias differs from the census row")
        if not any(q["child_id"] == eid and q["parent_id"] == "ENT-QA-COUNTRY" and q["relationship_type"] == "administrative_parent" for q in rels):
            bad("relationships", eid, "country parent missing")
        if not any(c["subject_id"] == eid and c["predicate"] == "population" and c["value"]["data"] == pop and c["observed_at"] == "2020-12-31" for c in claims):
            bad("claims", eid, "population differs from the exact census row")
    if sum(r["population"] for r in f["records"]) != f["total_population"]:
        bad("claims", "QA-total", "census rows do not reconcile to the published total")
    zubarah = scope["world_heritage"]
    if not any(c["subject_id"] == zubarah["entity_id"] and c["predicate"] == "world_heritage_inscription_year" and c["value"]["data"] == zubarah["inscription_year"] for c in claims):
        bad("claims", zubarah["entity_id"], "Al Zubarah inscription year mismatch")

    # Depth cycle 1 against the checksum-bound depth fixture.
    depth_claims = [r for r in claims if str(r.get("id", "")).startswith("CLM-QA-DEPTH")]
    if len(depth_claims) != 40:
        bad("claims", "QA-depth", "depth claim count differs from the fixture contract")
    ich = [r for r in depth_claims if r.get("source_id") == "SRC-QA-UNESCO-ICH-2026"]
    if {r["value"]["data"].get("reference") for r in ich} != {x["reference"] for x in depth["ich_elements"]}:
        bad("claims", "QA-ich", "UNESCO element references differ from the fixture list")
    for row in ich:
        if not row.get("published") or row.get("verification_status") != "verified" or row.get("classification") != "shared":
            bad("claims", row["id"], "UNESCO element is not published as a verified shared file")
        if row["value"]["data"].get("year") != next(x["year"] for x in depth["ich_elements"] if x["reference"] == row["value"]["data"]["reference"]):
            bad("claims", row["id"], "inscription year differs from the fixture")
    weak = [r for r in depth_claims if r.get("source_id") != "SRC-QA-UNESCO-ICH-2026"]
    if len(weak) != 33:
        bad("claims", "QA-depth", "weak depth claim count differs from the fixture contract")
    if any(r.get("published") for r in weak):
        bad("claims", "QA-depth", "a weak-source claim is published")
    if any(r.get("verification_status") not in {"probable", "local_reported", "unverified", "folk_narrative"} for r in weak):
        bad("claims", "QA-depth", "a weak-source claim exceeds the local_reported cap")
    if any(not r.get("classification") for r in weak):
        bad("claims", "QA-depth", "a weak-source claim lacks classification")
    for name in SHARED_DISHES:
        row = next((r for r in depth_claims if r["predicate"] == "food_dish" and r["value"]["data"].get("name") == name), None)
        if row and row.get("classification") != "shared":
            bad("claims", "QA-shared", f"{name} is not classified shared")
    for row in depth_claims:
        if row["predicate"] == "dialect_profile":
            words = row["value"]["data"].get("sample_words", [])
            if not words or any(len(w) != 2 or not w[1] for w in words):
                bad("claims", row["id"], "dialect vocabulary entry lacks a gloss")
    places = [r for r in e if r["entity_type"] in {"quarter", "market"}]
    fixture_places = len(depth["places"]["quarters"]) + len(depth["places"]["markets"])
    if len(places) != fixture_places:
        bad("entities", "QA-places", "old-Doha place count differs from the fixture list")
    if {r["canonical_name"] for r in places} != {q["name"] for q in depth["places"]["quarters"]} | {q["name"] for q in depth["places"]["markets"]}:
        bad("entities", "QA-places", "old-Doha place names differ from the fixture list")
    for row in places:
        if row.get("status") != "historical" or row.get("verification_status") != "local_reported" or row.get("canonical_source_id") not in DEPTH_SOURCES:
            bad("entities", row["id"], "old-Doha place is not historical/local_reported on a depth source")
        links = [r for r in rels if r["child_id"] == row["id"]]
        if len(links) != 1 or links[0]["relationship_type"] != "located_in" or links[0]["parent_id"] != "ENT-QA-MUNICIPALITY-DOHA":
            bad("relationships", row["id"], "place must have exactly one located_in relation to Doha municipality")
        if any(a["entity_id"] == row["id"] for a in aliases):
            bad("aliases", row["id"], "place carries an alias without an accepted alias source")
        if any(c["subject_id"] == row["id"] and c["predicate"] == "population" for c in claims):
            bad("claims", row["id"], "population claim invented for an old-Doha place")
    for row in claims:
        if not row.get("source_locator") or row.get("source_id") not in sids:
            bad("claims", row["id"], "source or locator missing from the reviewed source population")
    for row in source_rows:
        if row.get("quality_tier") not in {"A", "E"}:
            bad("sources", row["id"], "unexpected source tier")

    result = {}
    for family, rows in families.items():
        actual_ids = {row["id"] for row in rows}
        family_findings = [f for f in find if f["family"] == family]
        failed_ids = {f["record_id"] for f in family_findings}
        result[family] = {
            "population": len(rows), "sampled": len(actual_ids),
            "passed": len(actual_ids - failed_ids), "failed": len(failed_ids & actual_ids),
            "sample_percentage": 100.0,
            "status": "PASS" if not family_findings else "FAIL",
        }
    passed = not find and all(v["status"] == "PASS" for v in result.values())
    report = {
        "schema_version": "2.0.0", "country_code": "QA", "snapshot_date": DEPTH_DATE,
        "status": "PASS" if passed else "FAIL",
        "method": "Independent full-population review against the checksum-bound PSA census, QNMP/UNESCO scope, and depth fixtures; importer and Qatar semantic validator are not imported.",
        "p0": 0, "critical_p1": len(find), "families": result,
        "total_sampled": sum(v["sampled"] for v in result.values()),
        "total_passed": sum(v["passed"] for v in result.values()),
        "findings": find,
    }
    write_json(ROOT / "reports/qatar_independent_review.json", report)
    sample = {k: {"population": len({r["id"] for r in v}), "sample_size": len({r["id"] for r in v}), "sample_percentage": 100.0,
                  "record_ids": sorted({r["id"] for r in v})} for k, v in families.items()}
    write_json(ROOT / "data/review/qatar_review_samples.json", {"schema_version": "2.0.0", "country_code": "QA", "snapshot_date": DEPTH_DATE, "selection_method": "Full review of every Qatar record because each family is small; sorted stable IDs.", "families": sample})
    write_json(ROOT / "reports/qatar_review_samples.json", {"schema_version": "2.0.0", "country_code": "QA", "snapshot_date": DEPTH_DATE, "families": sample})
    for family, row in result.items():
        print(f"[{'PASS' if row['status'] == 'PASS' else 'FAIL'}] {family}: {row['passed']}/{row['sampled']}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
