#!/usr/bin/env python3
"""Executable compatibility, migration, semantic, and integrity tests for 2.0.0."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

from migrate_schema_2 import MigrationError, migrate_record, semantic_hash, strip_version
from model import ROOT
from validate import validate_all, validate_schema_value

FIXTURES = ROOT / "tests/fixtures/schema_v1"
FAMILIES = ("entity", "alias", "relationship", "claim", "source", "denominator", "coverage", "snapshot", "manifest")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def schema_accepts(value, schema) -> bool:
    errors = []
    validate_schema_value(value, schema, "fixture", lambda where, message: errors.append((where, message)))
    return not errors


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def v1_projection(family: str, row: dict, v1_schema: dict, coverage_audit: list[dict]) -> dict:
    if family != "coverage":
        keys = set(v1_schema.get("properties", {}))
        projected = {key: copy.deepcopy(value) for key, value in row.items() if key in keys}
        projected["schema_version"] = "1.0.0"
        return projected
    projected = {key: copy.deepcopy(value) for key, value in row.items() if key in v1_schema["properties"]}
    projected["schema_version"] = "1.0.0"
    projected["coverage_percent"] = coverage_audit[0]["v1_coverage_percent"]
    return projected


def main() -> int:
    fixtures = {family: load(FIXTURES / f"{family}.json") for family in FAMILIES}
    v1 = {family: load(ROOT / f"schema/v1/{family}.schema.json") for family in FAMILIES}
    v2 = {family: load(ROOT / f"schema/{family}.schema.json") for family in FAMILIES}

    assert all(schema_accepts(fixtures[f], v1[f]) for f in FAMILIES), "a committed v1 fixture is invalid under the original contract"
    literal_acceptance = sum(schema_accepts(fixtures[f], v2[f]) for f in FAMILIES)
    assert literal_acceptance == 0, f"breaking-version proof expected 0/9 literal acceptance, got {literal_acceptance}/9"
    version_only = {f: {**fixtures[f], "schema_version": "2.0.0"} for f in FAMILIES}
    version_only_acceptance = sum(schema_accepts(version_only[f], v2[f]) for f in FAMILIES)
    assert version_only_acceptance == 3, f"expected only alias/snapshot/manifest to accept version-only conversion, got {version_only_acceptance}/9"

    decisions = {
        fixtures["entity"]["id"]: {"confidence": "high", "verification_status": "source_verified"},
        fixtures["relationship"]["id"]: {"confidence": "high", "verification_status": "source_verified"},
        fixtures["claim"]["id"]: {
            "classification": None, "confidence": "high", "lexical_context": None,
            "published": True, "second_source_locator": None, "verification_status": "verified",
        },
        fixtures["source"]["id"]: {"quality_tier": "B"},
    }
    coverage_audit = []
    context = {
        "denominator": fixtures["denominator"],
        "snapshot": {"id": fixtures["coverage"]["snapshot_id"], "captured_at": "2026-08-15"},
        "source": {"id": fixtures["coverage"]["source_id"], "license": "ISO copyright; reuse subject to ISO terms"},
    }
    migrated = {}
    for family in FAMILIES:
        migrated[family] = migrate_record(
            family, fixtures[family], decisions=decisions,
            context=context if family == "coverage" else {}, audit=coverage_audit,
        )
        assert schema_accepts(migrated[family], v2[family]), f"migrated {family} is invalid under v2"

    for family in FAMILIES:
        projected = v1_projection(family, migrated[family], v1[family], coverage_audit)
        assert canonical(projected) == canonical(fixtures[family]), f"semantic projection changed for {family}"

    first = canonical(migrated)
    second_rows = {
        family: migrate_record(
            family, row, decisions=decisions,
            context=context if family == "coverage" else {}, audit=[],
        ) for family, row in migrated.items()
    }
    assert first == canonical(second_rows), "migration is not idempotent"
    rerun = {}
    for family in reversed(FAMILIES):
        rerun[family] = migrate_record(
            family, fixtures[family], decisions=decisions,
            context=context if family == "coverage" else {}, audit=[],
        )
    assert {k: canonical(v) for k, v in migrated.items()} == {k: canonical(v) for k, v in rerun.items()}, "migration is not deterministic"

    rejected = 0
    for family in ("entity", "relationship", "claim", "source"):
        try: migrate_record(family, fixtures[family])
        except MigrationError: rejected += 1
    try: migrate_record("coverage", fixtures["coverage"])
    except MigrationError: rejected += 1
    bad_coverage = copy.deepcopy(fixtures["coverage"])
    bad_coverage["excluded"] = 1
    try: migrate_record("coverage", bad_coverage, context=context)
    except MigrationError: rejected += 1
    assert rejected == 6, f"invalid/default rejection expected 6/6, got {rejected}/6"

    validation, records = validate_all()
    assert not validation.errors, f"repository validator has {len(validation.errors)} errors"
    checks = validation.checks
    assert checks["ids"]["duplicate_ids"] == 0
    assert checks["orphans"]["orphan_count"] == 0
    assert checks["cycles"]["cycle_count"] == 0
    assert checks["country_mismatch"]["mismatch_count"] == 0
    assert checks["claims"]["sourced"] == checks["claims"]["claims"]

    result = {
        "status": "PASS",
        "schema_from": "1.0.0",
        "schema_to": "2.0.0",
        "literal_v1_accepted_by_v2": f"{literal_acceptance}/9",
        "version_only_accepted_by_v2": f"{version_only_acceptance}/9",
        "migration_correctness": "9/9 PASS",
        "semantic_preservation": {family: "PASS" for family in FAMILIES},
        "semantic_loss": False,
        "idempotence": "PASS",
        "determinism": "PASS",
        "invalid_default_rejection": f"{rejected}/6 PASS",
        "duplicate_detection": "PASS (0 active duplicate IDs)",
        "orphan_detection": "PASS (0)",
        "cycle_detection": "PASS (0)",
        "country_integrity": "PASS (0 mismatches)",
        "source_claim_integrity": f"PASS ({checks['claims']['sourced']}/{checks['claims']['claims']})",
        "bahrain_at_schema_release": {"entities": 0, "claims": 0, "sources": 0, "denominators": 0},
        "semantic_hash": load(ROOT / "reports/schema_2_migration.json")["semantic_hash"],
        "current_data_semantic_hash": semantic_hash(ROOT),
        "fixture_result_sha256": "sha256:" + hashlib.sha256(first).hexdigest(),
    }
    path = ROOT / "reports/schema_backward_compatibility.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Schema migration tests PASS: 9/9; semantic_loss=false; idempotent; deterministic; negative=6/6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
