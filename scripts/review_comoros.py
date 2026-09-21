#!/usr/bin/env python3
"""Independent full Comoros review: opens the committed evidence and does not import the importer or validator."""
import hashlib
import json

from model import ROOT, read_jsonl, write_json

DEPTH_SOURCES = {
    "SRC-UNESCO-ICH-KM-ZAFFA-2025", "SRC-KM-CONSTITUTION-2018", "SRC-KM-ISO639-3-COMORIAN",
    "SRC-KM-MEDINAS-WIKI-2026", "SRC-KM-LANGUAGES-MIRROR-2026", "SRC-KM-COMORIAN-LANGS-WIKI-2026",
    "SRC-KM-CUISINE-MIRROR-2026", "SRC-KM-FOOD-TRAVEL-2021", "SRC-KM-FOOD-YOUM7-2022",
    "SRC-KM-CULTURE-RASEEF22-2023", "SRC-KM-CUSTOM-JAZEERA-2025", "SRC-KM-CUSTOM-MIDAD-2016",
    "SRC-KM-ECONOMY-MIRROR-2015", "SRC-KM-VOCAB-QUIZLET-2016", "SRC-KM-CULTURE-ALAYYAM-2024",
}
BASE_SOURCES = {"SRC-KM-LAW-11-006-AU-2011", "SRC-KM-INSEED-RGPH17-ADMIN", "SRC-UNESCO-WHC-KM-1768-2026"}


def L(p):
    return json.loads(p.read_text(encoding="utf8"))


def main():
    f = L(ROOT / "data/imports/comoros/fixtures/current_hierarchy_2026.json")
    dd = L(ROOT / "data/imports/comoros/fixtures/cultural_depth_2026.json")
    manifest = L(ROOT / "data/imports/comoros/snapshot_manifest.json")
    e = [r for r in read_jsonl(ROOT / "data/entities/entities.jsonl") if r.get("country_code") == "KM"]
    ids = {r["id"] for r in e}
    families = {
        "entities": e,
        "relationships": [r for r in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if r.get("child_id") in ids],
        "claims": [r for r in read_jsonl(ROOT / "data/claims/claims.jsonl") if r.get("subject_id") in ids],
        "denominators": [r for r in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if r.get("country_code") == "KM"],
        "coverage": [r for r in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if r.get("country_code") == "KM"],
    }
    source_rows = [L(p) for p in (ROOT / "data/sources").glob("*.json") if L(p).get("country_codes") == ["KM"]]
    families["sources"] = source_rows
    tiers = {r["id"]: r.get("quality_tier") for r in source_rows}
    E = {r["id"]: r for r in e}
    R = families["relationships"]
    C = families["claims"]
    find = []

    def bad(fam, rid, msg):
        find.append({"severity": "P1", "family": fam, "record_id": rid, "message": msg})

    # Evidence files are independently checksum-opened.
    for item in manifest["records"]:
        path = ROOT / item["path"]
        payload = path.read_bytes()
        if len(payload) != item["bytes"] or hashlib.sha256(payload).hexdigest() != item["sha256"]:
            bad("sources", item["path"], "fixture checksum/size mismatch")

    # Accepted hierarchy against the law/INSEED fixture.
    for island in f["islands"]:
        iid = "ENT-KM-ISLAND-" + island["token"]
        if E.get(iid, {}).get("canonical_name") != island["name"]:
            bad("entities", iid, "island name differs from the fixture")
        for p in island["prefectures"]:
            pid = "ENT-KM-PREFECTURE-" + p["token"]
            if not any(r["child_id"] == pid and r["parent_id"] == iid and r["relationship_type"] == "administrative_parent" for r in R):
                bad("relationships", pid, "island parent missing")
            for q in p["communes"]:
                cid = "ENT-KM-COMMUNE-" + q["token"]
                if E.get(cid, {}).get("canonical_name") != q["name"] or not any(r["child_id"] == cid and r["parent_id"] == pid for r in R):
                    bad("entities", cid, "commune identity or parent differs from the fixture")
    if any("MAYOTTE" in rid or row.get("canonical_name") == "Mayotte" for rid, row in E.items()):
        bad("entities", "Mayotte", "Mayotte must not exist as a current entity")
    if sum(len(p["communes"]) for i in f["islands"] for p in i["prefectures"]) != f["denominators"]["communes"]:
        bad("denominators", "KM-communes", "row set does not reconcile with the accepted denominator")

    # Published spine.
    published = [r for r in C if r.get("published")]
    for r in published:
        if tiers.get(r.get("source_id")) not in {"A", "B"}:
            bad("claims", r["id"], "published claim rests on a weak source")
        if r.get("verification_status") not in {"verified", "source_verified"}:
            bad("claims", r["id"], "published claim is not verified")
    whc = f["world_heritage"]["entity_id"]
    for pred, want in [("world_heritage_inscription_year", 2026), ("world_heritage_category", "cultural"),
                       ("serial_component_count", 6), ("world_heritage_criteria", dd["world_heritage_extra"]["criteria"]),
                       ("world_heritage_area_hectares", dd["world_heritage_extra"]["area_hectares"]),
                       ("world_heritage_buffer_zone_hectares", dd["world_heritage_extra"]["buffer_zone_hectares"])]:
        if not any(r["subject_id"] == whc and r["predicate"] == pred and r["value"]["data"] == want for r in C):
            bad("claims", f"{whc}:{pred}", "property claim differs from the checksum-bound fixtures")
    el = dd["ich_elements"][0]
    ich = [r for r in C if r["predicate"] == "intangible_cultural_practice"]
    if len(ich) != 1:
        bad("claims", "KM-ich", "expected exactly one inscribed element")
    else:
        row = ich[0]
        data = row["value"]["data"]
        if data.get("reference") != el["reference"] or data.get("year") != el["year"] or sorted(data.get("co_states", [])) != sorted(el["co_states"]):
            bad("claims", row["id"], "element reference, year or submitting States differ")
        if row.get("classification") != "shared" or not row.get("published"):
            bad("claims", row["id"], "seven-State element must be published as shared, never exclusive")
    arts = {str(r["value"]["data"].get("article")) for r in C if r["predicate"] == "constitutional_provision"}
    if arts != {"6", "9", "10"}:
        bad("claims", "KM-constitution", f"constitution articles differ: {sorted(arts)}")
    terr = next((r for r in C if r["predicate"] == "constitutional_provision" and str(r["value"]["data"].get("article")) == "6"), None)
    if terr and "مايوت" not in (terr.get("notes") or "") + (terr["value"]["data"].get("note") or ""):
        bad("claims", terr["id"], "territorial provision does not separate Mayotte from current administration")
    official = [r for r in C if r["predicate"] == "language_presence" and r["value"]["data"].get("official")]
    minority = [r for r in C if r["predicate"] == "language_presence" and not r["value"]["data"].get("official")]
    if len(official) != 3 or len(minority) != 2:
        bad("claims", "KM-languages", "official/minority language split differs")
    for r in official:
        if not r.get("published") or r.get("source_id") != "SRC-KM-CONSTITUTION-2018":
            bad("claims", r["id"], "official language must be published from the constitution")
    for r in minority:
        if r.get("published"):
            bad("claims", r["id"], "minority language must stay unpublished")
    comorian = next((r for r in official if "شيكومور" in r["value"]["data"].get("name", "")), None)
    if not comorian or set(comorian["value"]["data"].get("iso_codes", [])) != {"zdj", "wni", "swb", "wlc"}:
        bad("claims", "KM-iso", "Comorian ISO 639-3 code set is incomplete")
    for r in C:
        blob = json.dumps(r["value"], ensure_ascii=False)
        if any(t in blob for t in ('"speakers"', "نسبة المتحدث")):
            bad("claims", r["id"], "speaker count or share recorded although none was accepted")

    # Unpublished classified body.
    weak = [r for r in C if str(r.get("id", "")).startswith("CLM-KM-DEPTH") and r.get("source_id") not in {el and "SRC-UNESCO-ICH-KM-ZAFFA-2025", "SRC-KM-CONSTITUTION-2018", "SRC-UNESCO-WHC-KM-1768-2026"}]
    if any(r.get("published") for r in weak):
        bad("claims", "KM-depth", "a weak-source depth claim is published")
    for r in weak:
        if r.get("verification_status") not in {"probable", "local_reported", "unverified", "folk_narrative"}:
            bad("claims", r["id"], "weak-source claim exceeds the local_reported cap")
        if not r.get("classification") or r["classification"] not in {"local", "regional", "shared", "historical"}:
            bad("claims", r["id"], "weak-source claim lacks an accepted classification")
    for r in C:
        if r["predicate"] == "dialect_profile":
            for word in r["value"]["data"].get("phrases", []):
                if len(word) != 2 or not word[1]:
                    bad("claims", r["id"], "phrase entry lacks its meaning")
            for num in r["value"]["data"].get("numerals", []):
                if len(num) != 2 or not num[1]:
                    bad("claims", r["id"], "numeral entry lacks its form")

    # Heritage medinas: places with located_in only.
    medinas = {r["id"]: r for r in e if r["entity_type"] == "quarter"}
    fixture_map = {c["token"]: c for c in dd["places"]["medinas"]}
    if len(medinas) != len(fixture_map) or {r["canonical_name"] for r in medinas.values()} != {c["name"] for c in fixture_map.values()}:
        bad("entities", "KM-medinas", "medina set differs from the fixture list")
    for token, c in fixture_map.items():
        iid = "ENT-KM-MEDINA-" + token
        row = medinas.get(iid, {})
        if row.get("status") != "historical" or row.get("verification_status") != "local_reported" or row.get("canonical_source_id") not in DEPTH_SOURCES:
            bad("entities", iid, "medina must stay historical and local_reported on a depth source")
        links = [r for r in R if r["child_id"] == iid]
        if len(links) != 1 or links[0]["relationship_type"] != "located_in" or links[0]["parent_id"] != "ENT-KM-ISLAND-" + c["island"]:
            bad("relationships", iid, "medina must have exactly one located_in relation to its island")
        if any(r2["subject_id"] == iid for r2 in C):
            bad("claims", iid, "no claim may be attached to a heritage place in this cycle")
    tiers_count = {}
    for r in source_rows:
        tiers_count[r.get("quality_tier")] = tiers_count.get(r.get("quality_tier"), 0) + 1
    if tiers_count != {"A": 6, "B": 1, "E": 11}:
        bad("sources", "KM", f"source-tier mix differs: {tiers_count}")
    if {r["id"] for r in source_rows} != BASE_SOURCES | DEPTH_SOURCES:
        bad("sources", "KM", "source population differs from the accepted catalog")

    result = {}
    for family, rows in families.items():
        family_findings = [x for x in find if x["family"] == family]
        failed_ids = {x["record_id"] for x in family_findings}
        actual_ids = {row["id"] for row in rows}
        result[family] = {
            "population": len(rows), "sampled": len(actual_ids),
            "passed": len(actual_ids - failed_ids), "failed": len(failed_ids & actual_ids),
            "sample_percentage": 100.0, "status": "PASS" if not family_findings else "FAIL",
        }
    passed = not find and all(v["status"] == "PASS" for v in result.values())
    report = {
        "schema_version": "2.0.0", "country_code": "KM", "snapshot_date": "2026-09-20",
        "status": "PASS" if passed else "FAIL",
        "method": "Independent full-population review against the checksum-bound law/INSEED hierarchy fixture and the depth fixture; neither the importer nor the Comoros semantic validator is imported.",
        "p0": 0, "critical_p1": len(find), "families": result,
        "total_sampled": sum(v["sampled"] for v in result.values()),
        "total_passed": sum(v["passed"] for v in result.values()),
        "findings": find,
    }
    write_json(ROOT / "reports/comoros_independent_review.json", report)
    sample = {k: {"population": len({r["id"] for r in v}), "sample_size": len({r["id"] for r in v}), "sample_percentage": 100.0,
                  "record_ids": sorted({r["id"] for r in v})} for k, v in families.items()}
    write_json(ROOT / "data/review/comoros_review_samples.json", {"schema_version": "2.0.0", "country_code": "KM", "snapshot_date": "2026-09-20",
                                                                  "selection_method": "Full review of every Comoros record because each family is small; sorted stable IDs.", "families": sample})
    write_json(ROOT / "reports/comoros_review_samples.json", {"schema_version": "2.0.0", "country_code": "KM", "snapshot_date": "2026-09-20", "families": sample})
    for family, row in result.items():
        print(f"[{'PASS' if row['status'] == 'PASS' else 'FAIL'}] {family}: {row['passed']}/{row['sampled']}")
    print(f"total {report['total_passed']}/{report['total_sampled']}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
