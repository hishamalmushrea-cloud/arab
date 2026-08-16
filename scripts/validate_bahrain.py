#!/usr/bin/env python3
"""Bahrain production semantic validator independent of the importer."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from model import ROOT, read_jsonl, write_json

SNAPSHOT_DATE = "2026-08-16"
GOVERNORATES = {
    "ENT-BH-GOVERNORATE-CAPITAL": ("العاصمة", "Capital", 79.23),
    "ENT-BH-GOVERNORATE-MUHARRAQ": ("المحرق", "Muharraq", 74.1),
    "ENT-BH-GOVERNORATE-NORTHERN": ("الشمالية", "Northern", 145.69),
    "ENT-BH-GOVERNORATE-SOUTHERN": ("الجنوبية", "Southern", 488.77),
}
HERITAGE = {
    "ENT-BH-ARCHAEOLOGICAL-SITE-QALAT-AL-BAHRAIN": (1192, 2005),
    "ENT-BH-CULTURAL-SITE-PEARLING": (1364, 2012),
    "ENT-BH-ARCHAEOLOGICAL-SITE-DILMUN-BURIAL-MOUNDS": (1542, 2019),
}
BH_SOURCE_IDS = {
    "SRC-BH-SLRB-GOVERNORATE-AREA-2024", "SRC-BH-OPEN-DATA-POLICY-2026",
    "SRC-UNESCO-WHC-BH-2026", "SRC-UNESCO-WHC-BH-1192",
    "SRC-UNESCO-WHC-BH-1364", "SRC-UNESCO-WHC-BH-1542",
    "SRC-BH-BACA-PEARLING-PATH",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_data() -> dict[str, Any]:
    entities = [r for r in read_jsonl(ROOT / "data/entities/entities.jsonl") if r.get("country_code") == "BH"]
    ids = {r["id"] for r in entities}
    return {
        "entities": entities,
        "aliases": [r for r in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if r.get("entity_id") in ids],
        "relationships": [r for r in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if r.get("child_id") in ids],
        "claims": [r for r in read_jsonl(ROOT / "data/claims/claims.jsonl") if r.get("subject_id") in ids],
        "denominators": [r for r in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if r.get("country_code") == "BH"],
        "coverage": [r for r in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if r.get("country_code") == "BH"],
        "snapshots": [r for r in read_jsonl(ROOT / "data/snapshots/snapshots.jsonl") if r.get("id", "").startswith("SNP-BH-")],
        "sources": [load_json(p) for p in sorted((ROOT / "data/sources").glob("*.json")) if load_json(p).get("id") in BH_SOURCE_IDS],
        "manifest": load_json(ROOT / "manifests/BH.yml"),
    }


def validate_data(data: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    def error(code: str, location: str, message: str): errors.append({"code": code, "location": location, "message": message})
    entities = {r["id"]: r for r in data["entities"]}
    aliases = data["aliases"]
    relationships = data["relationships"]
    claims = data["claims"]
    sources = {r["id"]: r for r in data["sources"]}
    denominators = {r["id"]: r for r in data["denominators"]}
    coverage = {r["id"]: r for r in data["coverage"]}

    if set(entities) != {"ENT-BH-COUNTRY", *GOVERNORATES, *HERITAGE}:
        error("BH_ENTITY_UNIVERSE", "entities", "Bahrain entity universe differs from country + 4 governorates + 3 inscribed properties")
    if "ENT-BH-GOVERNORATE-CENTRAL" in entities:
        error("BH_HISTORICAL_AS_CURRENT", "ENT-BH-GOVERNORATE-CENTRAL", "Central Governorate must not be emitted as a current 2024 governorate")
    alias_by_entity = {r["entity_id"]: r for r in aliases}
    for eid, (arabic, english, area) in GOVERNORATES.items():
        row = entities.get(eid, {})
        if row.get("entity_type") != "bh_governorate" or row.get("canonical_name") != arabic or row.get("status") != "current":
            error("BH_GOVERNORATE_IDENTITY", eid, "governorate type/name/status mismatch")
        if alias_by_entity.get(eid, {}).get("name") != english:
            error("BH_GOVERNORATE_ALIAS", eid, "official English alias mismatch")
        parents = [r for r in relationships if r.get("child_id") == eid]
        if len(parents) != 1 or parents[0].get("parent_id") != "ENT-BH-COUNTRY" or parents[0].get("relationship_type") != "administrative_parent":
            error("BH_WRONG_PARENT", eid, "governorate requires exactly one country administrative parent")
        area_claims = [r for r in claims if r.get("subject_id") == eid and r.get("predicate") == "area"]
        if len(area_claims) != 1 or area_claims[0].get("value", {}).get("data") != area or area_claims[0].get("unit") != "km2" or area_claims[0].get("observed_at") != "2024-01-01":
            error("BH_AREA_VALUE", eid, "official 2024 area claim mismatch")

    for eid, (reference, year) in HERITAGE.items():
        row = entities.get(eid, {})
        if row.get("entity_type") not in {"archaeological_site", "cultural_site"}:
            error("BH_HERITAGE_TYPE", eid, "World Heritage property has wrong type")
        links = [r for r in relationships if r.get("child_id") == eid]
        if len(links) != 1 or links[0].get("parent_id") != "ENT-BH-COUNTRY" or links[0].get("relationship_type") != "associated_with":
            error("BH_HERITAGE_RELATION", eid, "serial property needs country association, not invented administrative parent")
        years = [r for r in claims if r.get("subject_id") == eid and r.get("predicate") == "world_heritage_inscription_year"]
        if len(years) != 1 or years[0].get("value", {}).get("data") != year:
            error("BH_HERITAGE_YEAR", eid, f"property {reference} inscription year mismatch")
        categories = [r for r in claims if r.get("subject_id") == eid and r.get("predicate") == "world_heritage_category"]
        if len(categories) != 1 or categories[0].get("value", {}).get("data") != "cultural":
            error("BH_HERITAGE_CATEGORY", eid, "UNESCO category mismatch")

    if len(aliases) != 7 or len(relationships) != 7 or len(claims) != 13:
        error("BH_COUNTS", "Bahrain", f"expected aliases/relationships/claims 7/7/13, got {len(aliases)}/{len(relationships)}/{len(claims)}")
    if len({r["id"] for r in aliases}) != len(aliases) or len({r["id"] for r in claims}) != len(claims):
        error("BH_DUPLICATES", "Bahrain", "duplicate Bahrain record IDs")
    for row in claims:
        if row.get("source_id") not in sources or not row.get("source_locator"):
            error("BH_CLAIM_SOURCE", row.get("id", "?"), "claim source/locator missing or outside accepted Bahrain catalog")
        if row.get("predicate", "").startswith("lexical_"):
            error("BH_UNSUPPORTED_DIALECT", row.get("id", "?"), "no dialect corpus was accepted in this cycle")
        if row.get("subject_id") in GOVERNORATES and row.get("predicate") not in {"area"}:
            error("BH_CULTURAL_LEAKAGE", row.get("id", "?"), "cultural/general claim leaked onto a governorate")
    if set(sources) != BH_SOURCE_IDS or any(r.get("quality_tier") != "A" for r in sources.values()):
        error("BH_SOURCE_CATALOG", "sources", "expected seven exact A-tier Bahrain production sources")

    expected_den = {"DEN-BH-COUNTRY-SCOPE": 1, "DEN-BH-GOVERNORATES-2024": 4, "DEN-BH-WHC-20260816": 3}
    if {k: v.get("value") for k, v in denominators.items()} != expected_den:
        error("BH_DENOMINATORS", "denominators", "country/governorate/World Heritage denominators must be exactly 1/4/3")
    expected_cov = {"COV-BH-COUNTRY-SCOPE": 1, "COV-BH-GOVERNORATES-2024": 4, "COV-BH-WHC-20260816": 3}
    if set(coverage) != set(expected_cov):
        error("BH_COVERAGE_SET", "coverage", "unexpected Bahrain coverage layer")
    for cid, value in expected_cov.items():
        row = coverage.get(cid, {})
        if row.get("matched") != value or row.get("denominator") != value or row.get("excluded") != 0 or row.get("unmatched") != 0 or not row.get("complete") or row.get("coverage_percentage") != 100.0:
            error("BH_COVERAGE_ARITHMETIC", cid, "coverage is not an exact closed layer")

    manifest = data["manifest"]
    if manifest.get("snapshot", {}).get("snapshot_id") != "SNP-BH-PRODUCTION-20260816" or manifest.get("official_authority", {}).get("verification_status") != "verified":
        error("BH_MANIFEST", "manifests/BH.yml", "production snapshot/authority is not verified")
    gov_level = next((r for r in manifest.get("hierarchy", []) if r.get("entity_type") == "bh_governorate"), {})
    if gov_level.get("scope_status") != "closed" or gov_level.get("denominator") != 4:
        error("BH_MANIFEST_GOVERNORATE", "manifests/BH.yml", "governorate layer is not closed at four")
    for kind in ("bh_area", "bh_block"):
        level = next((r for r in manifest.get("hierarchy", []) if r.get("entity_type") == kind), {})
        if level.get("scope_status") != "unavailable" or level.get("denominator") is not None:
            error("BH_NO_FAKE_LOWER_DENOMINATOR", kind, "lower layer must remain unavailable without an accepted denominator")

    snapshot = data["snapshots"]
    if len(snapshot) != 1 or snapshot[0].get("captured_at") != SNAPSHOT_DATE:
        error("BH_SNAPSHOT", "snapshots", "expected one dated Bahrain production snapshot")
    else:
        actual = "sha256:" + hashlib.sha256((ROOT / "data/imports/bahrain/snapshot_manifest.json").read_bytes()).hexdigest()
        if snapshot[0].get("checksum") != actual:
            error("BH_SNAPSHOT_CHECKSUM", snapshot[0]["id"], "snapshot manifest checksum mismatch")
    return errors


def main() -> int:
    data = load_data()
    errors = validate_data(data)
    entity_types = Counter(r["entity_type"] for r in data["entities"])
    report = {
        "schema_version": "2.0.0", "country_code": "BH", "snapshot_date": SNAPSHOT_DATE,
        "status": "PASS" if not errors else "FAIL", "p0": len(errors), "critical_p1": 0,
        "metrics": {
            "entities": len(data["entities"]), "new_entities": len(data["entities"]) - 1,
            "entity_types": dict(sorted(entity_types.items())), "aliases": len(data["aliases"]),
            "relationships": len(data["relationships"]), "claims": len(data["claims"]),
            "sources": len(data["sources"]), "denominators": len(data["denominators"]),
            "coverage_records": len(data["coverage"]), "published_claims": sum(bool(r.get("published")) for r in data["claims"]),
            "ab_claims": sum(r.get("source_id") in {s["id"] for s in data["sources"] if s.get("quality_tier") in {"A", "B"}} for r in data["claims"]),
            "dialect_claims": sum(r.get("predicate", "").startswith("lexical_") for r in data["claims"]),
        },
        "errors": errors,
    }
    write_json(ROOT / "reports/bahrain_validation.json", report)
    for name, value in report["metrics"].items(): print(f"[{'PASS' if not errors else 'FAIL'}] {name}: {value}")
    if errors:
        for row in errors: print(f"- {row['code']} {row['location']}: {row['message']}")
        return 1
    print("Bahrain production semantic validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
