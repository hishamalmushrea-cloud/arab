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

    result = {}
    for family, rows in families.items():
        selected = set(sample["families"][family]["record_ids"])
        actual = {row["id"] for row in rows}
        family_findings = [f for f in findings if f["family"] == family]
        result[family] = {"population": len(rows), "sampled": len(selected), "passed": len(selected) - len({f["record_id"] for f in family_findings}), "failed": len({f["record_id"] for f in family_findings}), "sample_percentage": 100.0, "status": "PASS" if selected == actual and not family_findings else "FAIL"}
        if selected != actual: finding(family, family, "review sample does not equal current full family")
    passed = not findings and all(v["status"] == "PASS" for v in result.values())
    report = {"schema_version": "2.0.0", "country_code": "BH", "snapshot_date": "2026-08-16", "status": "PASS" if passed else "FAIL", "method": "Independent full-population review against committed official API/UNESCO fixtures and checksums; importer and Bahrain semantic validator are not imported.", "p0": 0, "critical_p1": len(findings), "families": result, "total_sampled": sum(v["sampled"] for v in result.values()), "total_passed": sum(v["passed"] for v in result.values()), "findings": findings}
    write_json(ROOT / "reports/bahrain_independent_review.json", report)
    for family, row in result.items(): print(f"[{'PASS' if row['status']=='PASS' else 'FAIL'}] {family}: {row['passed']}/{row['sampled']}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
