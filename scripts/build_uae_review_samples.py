#!/usr/bin/env python3
"""Build deterministic >=10% UAE independent-review samples without importing the UAE importer."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

from model import ROOT, read_jsonl, write_json

OUTPUT = ROOT / "reports/uae_review_samples.json"
SEED = "uae-independent-review-v1"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def choose(family: str, ids: list[str]) -> dict[str, Any]:
    ordered = sorted(ids, key=lambda value: (hashlib.sha256(f"{SEED}|{family}|{value}".encode()).hexdigest(), value))
    minimum = math.ceil(len(ids) * 0.10)
    selected = ordered[:minimum]
    return {
        "population": len(ids),
        "minimum_required": minimum,
        "sample_size": len(selected),
        "sample_percentage": round(len(selected) / len(ids) * 100, 2) if ids else 0.0,
        "record_ids": selected,
    }


def main() -> None:
    entities = [row for row in read_jsonl(ROOT / "data/entities/entities.jsonl") if row.get("country_code") == "AE"]
    entity_ids = {row["id"] for row in entities}
    aliases = [row for row in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if row.get("entity_id") in entity_ids]
    relationships = [row for row in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if row.get("child_id") in entity_ids]
    claims = [row for row in read_jsonl(ROOT / "data/claims/claims.jsonl") if row.get("subject_id") in entity_ids]
    denominators = [row for row in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if row.get("country_code") == "AE"]
    coverage = [row for row in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if row.get("country_code") == "AE"]
    manifest = load_json(ROOT / "manifests/AE.yml")

    source_ids = set()
    for row in entities:
        source_ids.add(row.get("canonical_source_id"))
    for rows in (aliases, relationships, claims, denominators, coverage):
        for row in rows:
            source_ids.add(row.get("source_id"))
            if row.get("second_source_id"):
                source_ids.add(row.get("second_source_id"))
    source_ids.update(manifest.get("official_authority", {}).get("source_ids", []))
    for row in manifest.get("hierarchy", []) + manifest.get("pilot_layers", []):
        source_ids.update(row.get("source_ids", []))
    source_ids.discard(None)

    culture = [row for row in claims if row.get("predicate") != "jurisdiction_semantics"]
    dialect = [row for row in claims if row.get("predicate") == "lexical_form"]
    families = {
        "entities": [row["id"] for row in entities],
        "aliases": [row["id"] for row in aliases],
        "relationships": [row["id"] for row in relationships],
        "claims": [row["id"] for row in claims],
        "sources": sorted(source_ids),
        "denominators": [row["id"] for row in denominators],
        "coverage": [row["id"] for row in coverage],
        "cultural_claims": [row["id"] for row in culture],
        "dialect_claims": [row["id"] for row in dialect],
    }
    samples = {name: choose(name, ids) for name, ids in families.items()}
    report = {
        "schema_version": "1.0.0",
        "country_code": "AE",
        "snapshot_date": "2026-08-15",
        "selection_method": "Sort each record ID by SHA-256(seed|family|ID), then select ceil(10%); no UAE importer module is called or imported.",
        "seed": SEED,
        "families": samples,
        "status": "PASS" if all(row["sample_size"] >= row["minimum_required"] for row in samples.values()) else "FAIL",
        "total_sampled": sum(row["sample_size"] for row in samples.values()),
    }
    write_json(OUTPUT, report)
    for name, row in samples.items():
        print(f"[PASS] {name}: {row['sample_size']}/{row['population']} ({row['sample_percentage']}%)")
    print(f"Built {report['total_sampled']} deterministic UAE review selections across {len(samples)} required families.")


if __name__ == "__main__":
    main()
