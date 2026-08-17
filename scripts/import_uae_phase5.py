#!/usr/bin/env python3
"""Deterministically materialize the bounded UAE fourth-country pilot."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable

from build_uae_sources import main as build_sources
from model import ROOT, SCHEMA_VERSION, read_jsonl, record_id, write_jsonl


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def deterministic_id(prefix: str, *parts: object) -> str:
    return record_id(prefix, *parts)


SNAPSHOT_DATE = "2026-08-15"
SNAPSHOT_ID = "SNP-AE-PILOT-20260815"
PROFILE_PATH = ROOT / "data/imports/uae/fixtures/administrative_profile.json"
CULTURE_PATH = ROOT / "data/imports/uae/fixtures/cultural_claims.json"
SOURCE_FIXTURE_PATH = ROOT / "data/imports/uae/fixtures/source_catalog.json"
SNAPSHOT_MANIFEST_PATH = ROOT / "data/imports/uae/snapshot_manifest.json"


def replace_rows(path: Path, remove: Callable[[dict[str, Any]], bool], additions: list[dict[str, Any]]) -> None:
    retained = [row for row in read_jsonl(path) if not remove(row)]
    write_jsonl(path, retained + additions)


def typed_value(value: Any) -> dict[str, Any]:
    if isinstance(value, bool):
        kind = "boolean"
    elif isinstance(value, int):
        kind = "integer"
    elif isinstance(value, float):
        kind = "number"
    elif isinstance(value, (dict, list)):
        kind = "json"
    else:
        kind = "string"
    return {"type": kind, "data": value}


def claim_record(
    key: str,
    subject_id: str,
    predicate: str,
    value: Any,
    source_id: str,
    source_locator: str,
    classification: str | None,
    *,
    notes: str | None = None,
    status: str = "verified",
    lexical_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "id": deterministic_id("CLM-AE", key),
        "schema_version": SCHEMA_VERSION,
        "subject_id": subject_id,
        "predicate": predicate,
        "value": typed_value(value),
        "unit": None,
        "status": status,
        "observed_at": SNAPSHOT_DATE,
        "valid_from": None,
        "valid_to": None,
        "source_id": source_id,
        "second_source_id": None,
        "source_locator": source_locator,
        "sensitivity": "ordinary",
        "notes": notes,
        "verification_status": "source_verified",
        "confidence": "high",
        "classification": classification,
        "published": True,
        "second_source_locator": None,
        "lexical_context": lexical_context,
    }


def main() -> None:
    build_sources()
    profile = load_json(PROFILE_PATH)
    culture = load_json(CULTURE_PATH)
    for fixture in (profile, culture):
        if fixture.get("schema_version") != SCHEMA_VERSION or fixture.get("country_code") != "AE":
            raise SystemExit("invalid UAE fixture identity/version")
        if fixture.get("snapshot_date") != SNAPSHOT_DATE:
            raise SystemExit("UAE fixture snapshot dates differ")

    entities: list[dict[str, Any]] = []
    aliases: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []

    for spec in profile["entities"]:
        entities.append(
            {
                "id": spec["id"],
                "schema_version": SCHEMA_VERSION,
                "country_code": "AE",
                "canonical_name": spec["name"],
                "canonical_name_language": spec["name_language"],
                "entity_type": spec["entity_type"],
                "status": "current",
                "valid_from": None,
                "valid_to": None,
                "canonical_source_id": spec["source_id"],
                "source_locator": spec["source_locator"],
                "coordinates": None,
                "verification_status": "source_verified",
                "confidence": "high",
                "legacy_ids": [],
                "notes": f"Contextual UAE type; layer={spec['layer']}; snapshot={SNAPSHOT_DATE}. Administrative entities do not receive invented point coordinates.",
            }
        )
        aliases.append(
            {
                "id": deterministic_id("ALS-AE", spec["id"], spec["arabic_alias"], "ar", "official_variant"),
                "schema_version": SCHEMA_VERSION,
                "entity_id": spec["id"],
                "name": spec["arabic_alias"],
                "language": "ar",
                "script": "Arab",
                "kind": "official_variant",
                "status": "current",
                "source_id": spec["source_id"],
                "source_locator": spec["source_locator"] + "; parallel Arabic official name",
                "valid_from": None,
                "valid_to": None,
            }
        )
        relationships.append(
            {
                "id": deterministic_id("REL-AE", "administrative_parent", spec["id"], spec["parent_id"]),
                "schema_version": SCHEMA_VERSION,
                "child_id": spec["id"],
                "parent_id": spec["parent_id"],
                "relationship_type": "administrative_parent",
                "status": "current",
                "valid_from": None,
                "valid_to": None,
                "source_id": spec["source_id"],
                "source_locator": spec["source_locator"],
                "notes": "Parent is explicit in the emirate-specific fixture; equal-looking local words in other emirates are not treated as the same type.",
                "verification_status": "source_verified",
                "confidence": "high",
            }
        )
        claims.append(
            claim_record(
                "SEMANTICS-" + spec["id"],
                spec["id"],
                "jurisdiction_semantics",
                {
                    "authority": spec["authority"],
                    "parent_id": spec["parent_id"],
                    "snapshot_date": SNAPSHOT_DATE,
                    "semantic_definition": spec["semantic_definition"],
                    "layer": spec["layer"],
                },
                spec["source_id"],
                spec["source_locator"],
                "official",
                notes="Structured authority, parent, dated snapshot, and contextual semantic definition; it is not a generic UAE lower tier.",
            )
        )

    # Julfar is a historical name for the RAK identity in the bounded source, not a current unit.
    aliases.append(
        {
            "id": deterministic_id("ALS-AE", "ENT-AE-EMIRATE-RAS-AL-KHAIMAH", "Julfar", "en", "historical"),
            "schema_version": SCHEMA_VERSION,
            "entity_id": "ENT-AE-EMIRATE-RAS-AL-KHAIMAH",
            "name": "Julfar",
            "language": "en",
            "script": "Latn",
            "kind": "historical",
            "status": "historical",
            "source_id": "SRC-AE-RAK-GENERAL-2026",
            "source_locator": "history opening: Originally known as Julfar",
            "valid_from": None,
            "valid_to": None,
        }
    )

    for spec in culture["claims"]:
        claims.append(
            claim_record(
                spec["key"],
                spec["subject_id"],
                spec["predicate"],
                spec["value"],
                spec["source_id"],
                spec["source_locator"],
                spec["classification"],
                notes=spec.get("notes"),
                status=spec.get("status", "verified"),
                lexical_context=spec.get("lexical_context"),
            )
        )

    layer_by_name = {row["layer"]: row for row in profile["layers"]}
    denominators: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []
    for layer in profile["layers"]:
        slug = layer["layer"].upper().replace("_", "-")
        den_id = "DEN-AE-COUNTRY-SCOPE" if layer["layer"] == "country_scope" else f"DEN-AE-{slug}"
        cov_id = "COV-AE-COUNTRY-SCOPE" if layer["layer"] == "country_scope" else f"COV-AE-{slug}"
        denominator = layer["denominator"]
        denominators.append(
            {
                "id": den_id,
                "schema_version": SCHEMA_VERSION,
                "country_code": "AE",
                "layer": layer["layer"],
                "definition": layer["definition"],
                "value": denominator,
                "denominator": denominator,
                "as_of": SNAPSHOT_DATE,
                "snapshot_date": SNAPSHOT_DATE,
                "source_id": layer["source_id"],
                "source_locator": layer["source_locator"],
                "license": layer["license"],
                "status": layer["status"],
                "missing_reason": layer["missing_reason"],
                "notes": f"Authority: {layer['authority']}. A bounded official layer is complete only when matched + excluded equals its source-backed denominator.",
            }
        )
        percentage = None if denominator is None else round((layer["matched"] + layer["excluded"]) / denominator * 100, 2) if denominator else 100.0
        coverage.append(
            {
                "id": cov_id,
                "schema_version": SCHEMA_VERSION,
                "country_code": "AE",
                "layer": layer["layer"],
                "snapshot_id": SNAPSHOT_ID,
                "snapshot_date": SNAPSHOT_DATE,
                "source_id": layer["source_id"],
                "denominator_id": den_id,
                "license": layer["license"],
                "denominator": denominator,
                "matched": layer["matched"],
                "unmatched": layer["unmatched"],
                "excluded": layer["excluded"],
                "exclusion_reasons": [],
                "missing": layer["unmatched"] if denominator is not None else None,
                "missing_reason": layer["missing_reason"],
                "coverage_percentage": percentage,
                "complete": denominator is not None and layer["matched"] + layer["excluded"] == denominator and layer["unmatched"] == 0,
                "notes": layer["definition"] + (". No percentage is calculated." if denominator is None else ". Every in-scope row is matched; no exclusions."),
            }
        )

    checksum = hashlib.sha256()
    for path in sorted([PROFILE_PATH, CULTURE_PATH, SOURCE_FIXTURE_PATH, SNAPSHOT_MANIFEST_PATH]):
        checksum.update(path.read_bytes())
    snapshot = {
        "id": SNAPSHOT_ID,
        "schema_version": SCHEMA_VERSION,
        "title": "United Arab Emirates fourth-country contextual hierarchy and cultural sample",
        "captured_at": SNAPSHOT_DATE,
        "source_id": "SRC-AE-FEDERAL-SEVEN-EMIRATES-2026",
        "scope": "Seven emirates; seven different official local hierarchy profiles; bounded all-emirate cultural and small dialect samples",
        "method": "Offline deterministic import from checksum-bound relevant-text extracts and structured fixtures; official layer denominators remain separate and unavailable registries have no percentage.",
        "checksum": "sha256:" + checksum.hexdigest(),
        "notes": "Dubai communities, all-UAE populated places, and neighborhoods remain denominator_unavailable. No fifth country is started.",
    }

    replace_rows(
        ROOT / "data/entities/entities.jsonl",
        lambda row: row.get("country_code") == "AE" and row.get("id") != "ENT-AE-COUNTRY",
        entities,
    )
    replace_rows(
        ROOT / "data/aliases/aliases.jsonl",
        lambda row: str(row.get("entity_id", "")).startswith("ENT-AE-") and row.get("entity_id") != "ENT-AE-COUNTRY",
        aliases,
    )
    replace_rows(ROOT / "data/relationships/relationships.jsonl", lambda row: str(row.get("child_id", "")).startswith("ENT-AE-"), relationships)
    replace_rows(ROOT / "data/claims/claims.jsonl", lambda row: str(row.get("subject_id", "")).startswith("ENT-AE-"), claims)
    replace_rows(ROOT / "data/coverage/denominators.jsonl", lambda row: row.get("country_code") == "AE", denominators)
    replace_rows(ROOT / "data/coverage/coverage.jsonl", lambda row: row.get("country_code") == "AE", coverage)
    replace_rows(ROOT / "data/snapshots/snapshots.jsonl", lambda row: str(row.get("id", "")).startswith("SNP-AE-"), [snapshot])

    closed = [row for row in profile["layers"] if row["denominator"] is not None]
    unavailable = [row for row in profile["layers"] if row["denominator"] is None]
    assert sum(row["matched"] for row in closed) == 41  # country + 40 pilot entities
    assert len(layer_by_name) == 12 and len(unavailable) == 3
    print(
        "UAE import complete: "
        f"{len(entities) + 1} entities including country, {len(aliases) + 1} aliases including country, "
        f"{len(relationships)} relationships, {len(claims)} claims, {len(denominators)} denominators."
    )


if __name__ == "__main__":
    main()
