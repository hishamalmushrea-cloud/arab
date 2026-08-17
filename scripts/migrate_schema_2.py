#!/usr/bin/env python3
"""Deterministic, semantic-preserving migration from Schema 1.0.0 to 2.0.0.

The repository's active v1-labelled records already contain reviewed values for the
fields accumulated after the original 1.0.0 contract. This tool never fabricates
those values: a genuinely old record that lacks semantic metadata must receive an
explicit per-record review decision or migration fails.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

OLD_VERSION = "1.0.0"
NEW_VERSION = "2.0.0"
ROOT = Path(__file__).resolve().parents[1]

ACTIVE_JSONL = {
    "entity": "data/entities/entities.jsonl",
    "alias": "data/aliases/aliases.jsonl",
    "relationship": "data/relationships/relationships.jsonl",
    "claim": "data/claims/claims.jsonl",
    "denominator": "data/coverage/denominators.jsonl",
    "coverage": "data/coverage/coverage.jsonl",
    "snapshot": "data/snapshots/snapshots.jsonl",
}
IMPORT_RECORD_JSONL = ["data/imports/tunisia/phase1_population_claims.jsonl"]
IMPORT_RECORD_JSON = [
    "data/imports/jordan/hierarchy_2024.json",
    "data/imports/jordan/world_heritage_2026.json",
    "data/imports/jordan/cultural_content_2026.json",
    "data/imports/jordan/entity_resolution_2026.json",
]
ACTIVE_JSON = {
    "source": "data/sources/*.json",
    "manifest": "manifests/*.yml",
}
SEMANTIC_FIELDS = {
    "entity": ("confidence", "verification_status"),
    "relationship": ("confidence", "verification_status"),
    "claim": (
        "classification", "confidence", "lexical_context", "published",
        "second_source_locator", "verification_status",
    ),
    "source": ("quality_tier",),
}

class MigrationError(ValueError):
    """The input cannot be migrated without inventing or losing meaning."""


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise MigrationError(f"{path}:{number}: malformed JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise MigrationError(f"{path}:{number}: record must be an object")
        rows.append(row)
    return rows


def encoded_json(value: Any, pretty: bool = True) -> bytes:
    if pretty:
        return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def write_json(path: Path, value: Any) -> None:
    path.write_bytes(encoded_json(value))


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    rows = sorted(rows, key=lambda row: str(row.get("id", "")))
    path.write_bytes(b"".join(encoded_json(row, pretty=False) for row in rows))


def decision_for(record: dict[str, Any], decisions: dict[str, Any]) -> dict[str, Any]:
    value = decisions.get(record.get("id", ""), {})
    if not isinstance(value, dict):
        raise MigrationError(f"review decision for {record.get('id')} must be an object")
    return value


def require_reviewed_fields(family: str, record: dict[str, Any], decisions: dict[str, Any]) -> None:
    decision = decision_for(record, decisions)
    for field in SEMANTIC_FIELDS.get(family, ()):
        if field not in record:
            if field not in decision:
                raise MigrationError(
                    f"{family} {record.get('id', '?')} lacks semantic field {field!r}; "
                    "an explicit review decision is required"
                )
            record[field] = copy.deepcopy(decision[field])


def migrate_record(
    family: str,
    original: dict[str, Any],
    *,
    decisions: dict[str, Any] | None = None,
    context: dict[str, Any] | None = None,
    audit: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Migrate one record, rejecting any conversion that needs an invented fact."""
    decisions = decisions or {}
    context = context or {}
    record = copy.deepcopy(original)
    version = record.get("schema_version")
    if version not in {OLD_VERSION, NEW_VERSION}:
        raise MigrationError(f"{family} {record.get('id', '?')} has unsupported schema_version {version!r}")
    require_reviewed_fields(family, record, decisions)

    if family == "denominator":
        record.setdefault("denominator", record.get("value"))
        record.setdefault("snapshot_date", record.get("as_of"))
        if record.get("denominator") != record.get("value"):
            raise MigrationError(f"denominator {record.get('id')} mirror conflicts with value")
        if record.get("snapshot_date") != record.get("as_of"):
            raise MigrationError(f"denominator {record.get('id')} snapshot_date conflicts with as_of")

    if family == "coverage":
        denominator = context.get("denominator")
        snapshot = context.get("snapshot")
        source = context.get("source")
        if "denominator" not in record:
            if not denominator or denominator.get("id") != record.get("denominator_id"):
                raise MigrationError(f"coverage {record.get('id')} requires its denominator record")
            record["denominator"] = denominator.get("value")
        if "snapshot_date" not in record:
            if not snapshot or snapshot.get("id") != record.get("snapshot_id"):
                raise MigrationError(f"coverage {record.get('id')} requires its snapshot record")
            record["snapshot_date"] = snapshot.get("captured_at")
        if "license" not in record:
            if not source or source.get("id") != record.get("source_id") or not source.get("license"):
                raise MigrationError(f"coverage {record.get('id')} requires a documented license")
            record["license"] = source["license"]
        if "exclusion_reasons" not in record:
            if record.get("excluded"):
                decision = decision_for(record, decisions)
                if "exclusion_reasons" not in decision:
                    raise MigrationError(f"coverage {record.get('id')} requires reviewed exclusion reasons")
                record["exclusion_reasons"] = copy.deepcopy(decision["exclusion_reasons"])
            else:
                record["exclusion_reasons"] = []
        if sum(item.get("count", 0) for item in record["exclusion_reasons"]) != record.get("excluded"):
            raise MigrationError(f"coverage {record.get('id')} exclusion reasons do not sum to excluded")

        old_percent = record.pop("coverage_percent", None)
        value = record.get("denominator")
        completed = record.get("matched", 0) + record.get("excluded", 0)
        new_percent = None if value is None else round(completed * 100 / value, 2) if value else (100.0 if completed == 0 else None)
        if old_percent is not None:
            old_expected = None if value is None else round(record.get("matched", 0) * 100 / value, 4) if value else (100.0 if record.get("matched", 0) == 0 else None)
            if old_percent != old_expected:
                raise MigrationError(f"coverage {record.get('id')} v1 percentage is inconsistent ({old_percent} != {old_expected})")
            if audit is not None:
                audit.append({
                    "id": record.get("id"),
                    "v1_coverage_percent": old_percent,
                    "v1_formula": "matched / denominator",
                    "v2_coverage_percentage": new_percent,
                    "v2_formula": "(matched + excluded) / denominator",
                })
        elif "coverage_percentage" in record and record["coverage_percentage"] != new_percent:
            raise MigrationError(f"coverage {record.get('id')} existing v2 percentage is inconsistent")
        record["coverage_percentage"] = new_percent
        if value is None:
            record["missing"] = None
            record["complete"] = False
        else:
            missing = value - completed
            if missing < 0:
                raise MigrationError(f"coverage {record.get('id')} matched + excluded exceeds denominator")
            record["missing"] = missing
            record["unmatched"] = missing
            record["complete"] = completed == value

    record["schema_version"] = NEW_VERSION
    return record


def strip_version(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: strip_version(child) for key, child in sorted(value.items()) if key != "schema_version"}
    if isinstance(value, list):
        return [strip_version(child) for child in value]
    return value


def authoritative_records(root: Path) -> dict[str, list[dict[str, Any]]]:
    result = {family: read_jsonl(root / rel) for family, rel in ACTIVE_JSONL.items()}
    result["source"] = [read_json(path) for path in sorted((root / "data/sources").glob("*.json"))]
    result["manifest"] = [read_json(path) for path in sorted((root / "manifests").glob("*.yml"))]
    return result


def semantic_hash(root: Path) -> str:
    payload = strip_version(authoritative_records(root))
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def refresh_checksum_manifest(root: Path, relative: str) -> int:
    path = root / relative
    manifest = read_json(path)
    rows = manifest.get("files", [])
    for row in rows:
        target = root / row["path"]
        payload = target.read_bytes()
        row["bytes"] = len(payload)
        row["sha256"] = hashlib.sha256(payload).hexdigest()
    if "schema_version" in manifest:
        manifest["schema_version"] = NEW_VERSION
    write_json(path, manifest)
    return len(rows)


def migrate_tree(root: Path, decisions: dict[str, Any] | None = None) -> dict[str, Any]:
    decisions = decisions or {}
    before_hash = semantic_hash(root)
    coverage_audit: list[dict[str, Any]] = []
    records = authoritative_records(root)
    den = {row["id"]: row for row in records["denominator"]}
    snap = {row["id"]: row for row in records["snapshot"]}
    source = {row["id"]: row for row in records["source"]}

    for family, rel in ACTIVE_JSONL.items():
        migrated = []
        for row in records[family]:
            context = {}
            if family == "coverage":
                context = {
                    "denominator": den.get(row.get("denominator_id")),
                    "snapshot": snap.get(row.get("snapshot_id")),
                    "source": source.get(row.get("source_id")),
                }
            migrated.append(migrate_record(family, row, decisions=decisions, context=context, audit=coverage_audit))
        write_jsonl(root / rel, migrated)

    for family, pattern in ACTIVE_JSON.items():
        for path in sorted(root.glob(pattern)):
            write_json(path, migrate_record(family, read_json(path), decisions=decisions))

    # Exactly 28 schema-bearing importer records were part of the audited release scope.
    for rel in IMPORT_RECORD_JSON:
        path = root / rel
        document = read_json(path)
        if document.get("schema_version") not in {OLD_VERSION, NEW_VERSION}:
            raise MigrationError(f"{rel}: unsupported importer schema version")
        document["schema_version"] = NEW_VERSION
        write_json(path, document)
    for rel in IMPORT_RECORD_JSONL:
        path = root / rel
        rows = read_jsonl(path)
        for row in rows:
            if row.get("schema_version") not in {OLD_VERSION, NEW_VERSION}:
                raise MigrationError(f"{rel}: unsupported importer record version")
            row["schema_version"] = NEW_VERSION
        write_jsonl(path, rows)

    # Non-record importer wrappers and generated metadata carry the release label too.
    for path in sorted((root / "data/imports").glob("**/*.json")):
        document = read_json(path)
        if isinstance(document, dict) and document.get("schema_version") in {OLD_VERSION, NEW_VERSION}:
            document["schema_version"] = NEW_VERSION
            write_json(path, document)

    checksum_bindings = 0
    checksum_bindings += refresh_checksum_manifest(root, "data/imports/jordan/snapshot_manifest.json")
    checksum_bindings += refresh_checksum_manifest(root, "data/imports/tunisia/snapshot_manifest.json")
    after_hash = semantic_hash(root)
    if before_hash != after_hash:
        raise MigrationError(f"semantic hash changed: {before_hash} -> {after_hash}")

    counts = {family: len(rows) for family, rows in authoritative_records(root).items()}
    authoritative_count = sum(counts.values())
    importer_count = sum(len(read_jsonl(root / rel)) for rel in IMPORT_RECORD_JSONL) + len(IMPORT_RECORD_JSON)
    return {
        "schema_from": OLD_VERSION,
        "schema_to": NEW_VERSION,
        "status": "PASS",
        "authoritative_records": authoritative_count,
        "importer_records": importer_count,
        "records_migrated": authoritative_count + importer_count,
        "failed": 0,
        "quarantined": 0,
        "information_lost": 0,
        "semantic_changes_unreviewed": 0,
        "schema_normalizations": authoritative_count + importer_count,
        "checksum_bindings_refreshed": checksum_bindings,
        "counts": counts,
        "coverage_conversion_audit": coverage_audit,
        "semantic_loss": False,
        "semantic_hash": after_hash,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--decisions", type=Path)
    parser.add_argument("--report", type=Path, default=Path("reports/schema_2_migration.json"))
    args = parser.parse_args()
    decisions = read_json(args.decisions) if args.decisions else {}
    report = migrate_tree(args.root.resolve(), decisions)
    report_path = args.report if args.report.is_absolute() else args.root.resolve() / args.report
    write_json(report_path, report)
    print(f"Schema {OLD_VERSION} -> {NEW_VERSION}: PASS; records={report['records_migrated']}; semantic_loss=false")
    print(f"semantic_hash={report['semantic_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
