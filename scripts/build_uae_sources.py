#!/usr/bin/env python3
"""Materialize checksum-bound UAE pilot Source records from offline fixtures."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from model import ROOT, SCHEMA_VERSION, write_json


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

CATALOG = ROOT / "data/imports/uae/fixtures/source_catalog.json"
SNAPSHOT_MANIFEST = ROOT / "data/imports/uae/snapshot_manifest.json"
IMPORT_ROOT = ROOT / "data/imports/uae"
SOURCE_DIR = ROOT / "data/sources"


def main() -> None:
    catalog = load_json(CATALOG)
    snapshot = load_json(SNAPSHOT_MANIFEST)
    if catalog.get("schema_version") != SCHEMA_VERSION or snapshot.get("schema_version") != SCHEMA_VERSION:
        raise SystemExit("UAE source fixtures use an unsupported schema version")

    captures = {row["source_id"]: row for row in snapshot["records"]}
    expected_ids = {row["id"] for row in catalog["sources"]}
    if expected_ids != set(captures):
        raise SystemExit("UAE source catalog and snapshot manifest IDs differ")

    for old in SOURCE_DIR.glob("SRC-AE-*.json"):
        if old.stem not in expected_ids:
            old.unlink()

    for row in catalog["sources"]:
        capture = captures[row["id"]]
        path = IMPORT_ROOT / capture["path"]
        payload = path.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        if len(payload) != capture["bytes"] or digest != capture["sha256"]:
            raise SystemExit(f"checksum/size mismatch for {path.relative_to(ROOT)}")
        if row["checksum"] != "sha256:" + digest:
            raise SystemExit(f"source checksum differs from snapshot manifest for {row['id']}")
        record = dict(row)
        record["schema_version"] = SCHEMA_VERSION
        write_json(SOURCE_DIR / f"{row['id']}.json", record)

    print(f"Materialized {len(expected_ids)} UAE source records from checksum-bound extracts.")


if __name__ == "__main__":
    main()
