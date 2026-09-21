#!/usr/bin/env python3
"""Independent Bahrain review: opens committed evidence and does not call the importer/validator."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from model import ROOT, read_jsonl, write_json


def load(path: Path): return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    sample = load(ROOT / "data/review/bahrain_review_samples.json")
    area = load(ROOT / "data/imports/bahrain/fixtures/area_by_governorate_2024.json")
    whc = load(ROOT / "data/imports/bahrain/fixtures/world_heritage_2026.json")
    depth = load(ROOT / "data/imports/bahrain/fixtures/cultural_depth_2026.json")
    depth_source_ids = {"SRC-BH-UNESCO-ICH-2026", "SRC-BH-FJIRI-01747", "SRC-BH-DIALECT-MIRROR-2026",
                        "SRC-BH-CUISINE-MIRROR-2026", "SRC-BH-FOLK-CLOTH-2022", "SRC-BH-NASHIL-PRESS-2018",
                        "SRC-BH-MUHARRAQ-WIKI-2026", "SRC-BH-FIRJAN-BLOG-2022", "SRC-BH-FIRJAN-ELAPH-2023",
                        "SRC-BH-ALBILAD-2021"}
    manifest = load(ROOT / "data/imports/bahrain/snapshot_manifest.json")
    entities = {r["id"]: r for r in read_jsonl(ROOT / "data/entities/entities.jsonl") if r.get("country_code") == "BH"}
    ids = set(entities)
    families = {
        "entities": list(entities.values()),
        "aliases": [r for r in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if r.get("entity_id") in ids],
        "relationships": [r for r in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if r.get("child_id") in ids],
        "claims": [r for r in read_jsonl(ROOT / "data/claims/claims.jsonl") if r.get("subject_id") in ids],
        "denominators": [r for r in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if r.get("country_code") == "BH"],
        "coverage": [r for r in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if r.get("country_code") == "BH"],
    }
    source_ids = set(sample["families"]["sources"]["record_ids"])
    families["sources"] = [load(p) for p in (ROOT / "data/sources").glob("*.json") if load(p).get("id") in source_ids]
    findings = []
    def finding(family, identifier, message): findings.append({"severity": "P1", "family": family, "record_id": identifier, "message": message})

    # Evidence files are independently checksum-opened.
    for item in manifest["records"]:
        path = ROOT / item["path"]
        payload = path.read_bytes()
        if len(payload) != item["bytes"] or hashlib.sha256(payload).hexdigest() != item["sha256"]:
            finding("sources", item["path"], "fixture checksum/size mismatch")

    expected_gov = {r["governorate_ar"]: (r["governorate"], r["area_km2"]) for r in area["records"]}
    actual_gov = {r["canonical_name"]: r for r in entities.values() if r["entity_type"] == "bh_governorate"}
    if set(actual_gov) != set(expected_gov): finding("entities", "BH-governorates", "official four-name set mismatch")
    claims = families["claims"]
    aliases = families["aliases"]
    rels = families["relationships"]
    for arabic, (english, value) in expected_gov.items():
        entity = actual_gov.get(arabic, {})
        eid = entity.get("id")
        if not eid: continue
        if not any(a["entity_id"] == eid and a["name"] == english for a in aliases): finding("aliases", eid, "English name differs from bilingual API record")
        if not any(r["child_id"] == eid and r["parent_id"] == "ENT-BH-COUNTRY" and r["relationship_type"] == "administrative_parent" for r in rels): finding("relationships", eid, "country parent missing")
        if not any(c["subject_id"] == eid and c["predicate"] == "area" and c["value"]["data"] == value for c in claims): finding("claims", eid, "2024 area differs from exact API record")

    expected_properties = {r["entity_id"]: r for r in whc["properties"]}
    actual_properties = {eid: entities.get(eid) for eid in expected_properties}
    if any(v is None for v in actual_properties.values()) or whc["denominator"] != 3: finding("entities", "BH-WHC", "three-property State Party set mismatch")
    for eid, spec in expected_properties.items():
        if not any(c["subject_id"] == eid and c["predicate"] == "world_heritage_inscription_year" and c["value"]["data"] == spec["inscription_year"] for c in claims): finding("claims", eid, "inscription year mismatch")
        if not any(r["child_id"] == eid and r["relationship_type"] == "associated_with" and r["parent_id"] == "ENT-BH-COUNTRY" for r in rels): finding("relationships", eid, "serial property improperly parented")

    for row in claims:
        if not row.get("source_locator") or row.get("source_id") not in source_ids: finding("claims", row["id"], "source or locator missing from reviewed source population")
    if any(r.get("predicate", "").startswith("lexical_") for r in claims): finding("claims", "BH-dialect", "unsupported dialect claim present")
    if any(r.get("entity_id") == "ENT-BH-COUNTRY" for r in aliases): finding("aliases", "ENT-BH-COUNTRY", "baseline alias unexpectedly replaced by production evidence")

    # Depth cycle 1 reviewed against the checksum-bound depth fixture, independently of the importer and validator.
    depth_claims = [r for r in claims if str(r.get("id", "")).startswith("CLM-BH-DEPTH")]
    if len(depth_claims) != 43: finding("claims", "BH-depth", "depth claim count differs from the fixture contract")
    ich_claims = [r for r in depth_claims if r.get("source_id") in {"SRC-BH-UNESCO-ICH-2026", "SRC-BH-FJIRI-01747"}]
    if {r["value"]["data"].get("reference") for r in ich_claims} != {e["reference"] for e in depth["ich_elements"]}:
        finding("claims", "BH-ich", "UNESCO element references differ from the fixture list")
    for row in ich_claims:
        if not row.get("published") or row.get("verification_status") != "verified" or row.get("classification") not in {"shared", "national"}:
            finding("claims", row["id"], "UNESCO element is not published as verified shared/national")
    fjiri = next((r for r in ich_claims if r["value"]["data"].get("reference") == "01747"), None)
    if not fjiri or fjiri.get("classification") != "national":
        finding("claims", "BH-ich-01747", "Fjiri must be recorded as the national element")
    weak = [r for r in depth_claims if r.get("source_id") in depth_source_ids and r.get("source_id") not in {"SRC-BH-UNESCO-ICH-2026", "SRC-BH-FJIRI-01747"}]
    if len(weak) != 38: finding("claims", "BH-depth", "weak depth claim count differs from the fixture contract")
    if any(r.get("published") for r in weak): finding("claims", "BH-depth", "a weak-source claim is published")
    if any(r.get("verification_status") not in {"probable", "local_reported", "unverified", "folk_narrative"} for r in weak):
        finding("claims", "BH-depth", "a weak-source claim exceeds the local_reported cap")
    if any(not r.get("classification") for r in weak): finding("claims", "BH-depth", "a weak-source claim lacks classification")
    for name in ("المموش", "الثريد", "الهريسة", "المضروبة", "الكرك", "السمبوسة", "المجبوس", "القوزي", "الصالونة", "المرقوق"):
        row = next((r for r in depth_claims if r["predicate"] == "food_dish" and r["value"]["data"].get("name") == name), None)
        if row and row.get("classification") != "shared": finding("claims", "BH-shared", f"{name} is not classified shared")
    for row in depth_claims:
        if row["predicate"] == "dialect_profile":
            for word in row["value"]["data"].get("sample_words", []):
                if len(word) != 2 or not word[1]: finding("claims", row["id"], "dialect vocabulary entry lacks a gloss")
    places = [r for r in entities.values() if r["entity_type"] in {"city", "quarter", "village"}]
    if len(places) != len(depth["places"]["firjan"]) + len(depth["places"]["villages"]) + len(depth["places"]["halat"]) + 1:
        finding("entities", "BH-places", "heritage place count differs from the fixture list")
    for row in places:
        if row.get("verification_status") != "local_reported" or row.get("canonical_source_id") not in depth_source_ids:
            finding("entities", row["id"], "heritage place is not local_reported on a depth source")
        links = [r for r in rels if r["child_id"] == row["id"]]
        if len(links) != 1 or links[0]["relationship_type"] != "located_in":
            finding("relationships", row["id"], "heritage place must have exactly one located_in relation")
        if any(r["subject_id"] == row["id"] and r["predicate"] == "population" for r in claims):
            finding("claims", row["id"], "population claim invented for a heritage place")
        if any(a["entity_id"] == row["id"] for a in aliases):
            finding("aliases", row["id"], "heritage place carries an alias without an accepted alias source")

    result = {}
    for family, rows in families.items():
        selected = set(sample["families"][family]["record_ids"])
        actual = {row["id"] for row in rows}
        family_findings = [f for f in findings if f["family"] == family]
        result[family] = {"population": len(rows), "sampled": len(selected), "passed": len(selected) - len({f["record_id"] for f in family_findings}), "failed": len({f["record_id"] for f in family_findings}), "sample_percentage": 100.0, "status": "PASS" if selected == actual and not family_findings else "FAIL"}
        if selected != actual: finding(family, family, "review sample does not equal current full family")
    passed = not findings and all(v["status"] == "PASS" for v in result.values())
    report = {"schema_version": "2.0.0", "country_code": "BH", "snapshot_date": "2026-09-20", "status": "PASS" if passed else "FAIL", "method": "Independent full-population review against committed official API/UNESCO fixtures and checksums; importer and Bahrain semantic validator are not imported.", "p0": 0, "critical_p1": len(findings), "families": result, "total_sampled": sum(v["sampled"] for v in result.values()), "total_passed": sum(v["passed"] for v in result.values()), "findings": findings}
    write_json(ROOT / "reports/bahrain_independent_review.json", report)
    for family, row in result.items(): print(f"[{'PASS' if row['status']=='PASS' else 'FAIL'}] {family}: {row['passed']}/{row['sampled']}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
