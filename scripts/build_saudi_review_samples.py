#!/usr/bin/env python3
"""Build the fixed, stratified Saudi independent-review sample fixture."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

from model import ROOT, read_jsonl, write_json

OUT = ROOT / "data/review/saudi_review_samples.json"


def ranked(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda row: hashlib.sha256(row["id"].encode()).hexdigest())


def stratified(rows: list[dict[str, Any]], field: str, minimum_rate: float = 0.10) -> list[str]:
    target = max(1, math.ceil(len(rows) * minimum_rate))
    selected: dict[str, dict[str, Any]] = {}
    for value in sorted({str(row.get(field)) for row in rows}):
        group = ranked([row for row in rows if str(row.get(field)) == value])
        if group:
            selected[group[0]["id"]] = group[0]
    for row in ranked(rows):
        if len(selected) >= target:
            break
        selected[row["id"]] = row
    return sorted(selected)


def main() -> int:
    entities = [row for row in read_jsonl(ROOT / "data/entities/entities.jsonl") if row.get("country_code") == "SA"]
    ids = {row["id"] for row in entities}
    aliases = [row for row in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if row.get("entity_id") in ids]
    relationships = [row for row in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if row.get("child_id") in ids]
    claims = [row for row in read_jsonl(ROOT / "data/claims/claims.jsonl") if row.get("subject_id") in ids]
    denominators = [row for row in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if row.get("country_code") == "SA"]
    coverage = [row for row in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if row.get("country_code") == "SA"]
    sources = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((ROOT / "data/sources").glob("*.json"))]
    source_ids = {row.get("canonical_source_id") for row in entities} | {row.get("source_id") for row in aliases + relationships + claims + denominators + coverage}
    sources = [row for row in sources if row["id"] in source_ids]

    context_place_names = {"جدة", "الدرعية", "الهفوف", "قرية الفاو"}
    populated = sorted(row["id"] for row in entities if row["canonical_name"] in context_place_names and row["entity_type"] in {"city", "historical_place"})
    sites = sorted(row["id"] for row in entities if row["entity_type"] in {"archaeological_site", "cultural_site", "natural_site"})
    lexical = sorted(row["id"] for row in entities if row["entity_type"] == "lexical_form")
    cultural_claims = sorted(row["id"] for row in claims if row["predicate"] in {"official_regional_dish", "official_national_dish", "official_national_dessert", "intangible_cultural_practice", "regional_clothing_evidence_scope", "unesco_world_heritage_inscription", "environmental_context"})
    dialect_claims = sorted(row["id"] for row in claims if row["predicate"].startswith("lexical_"))
    selected_sources = sorted({
        "SRC-SA-LAW-OF-PROVINCES-1992", "SRC-SA-GASTAT-HEALTH-METHOD-2026", "SRC-SA-SAUDIPEDIA-ADMIN-2026",
        "SRC-SA-SAUDIPEDIA-CENTERS-RIYADH-2026", "SRC-SA-SAUDIPEDIA-CENTERS-EASTERN-2026",
        "SRC-UNESCO-WHC-SA-1712", "SRC-UNESCO-ICH-SA-01863", "SRC-SA-CULINARY-REGIONAL-DISHES-2024",
        "SRC-SA-GOV-CULTURE-2026", "SRC-ACADEMIC-SA-DIALECT-CORPUS-2020", "SRC-SA-ADMIN-SNAPSHOT-CATALOG-2026",
    })
    result = {
        "schema_version": "2.0.0",
        "country_code": "SA",
        "snapshot_date": "2026-08-15",
        "selection_method": "Fixed SHA-256-ranked sample of at least 10% per major record family, forced to span every entity type, relationship type, alias kind, claim predicate, all denominator records, all bounded context places, all UNESCO sites, and all lexical forms.",
        "entity_ids": stratified(entities, "entity_type"),
        "alias_ids": stratified(aliases, "kind"),
        "relationship_ids": stratified(relationships, "relationship_type"),
        "claim_ids": stratified(claims, "predicate"),
        "denominator_ids": sorted(row["id"] for row in denominators),
        "coverage_ids": sorted(row["id"] for row in coverage),
        "source_ids": selected_sources,
        "populated_place_ids": populated,
        "site_ids": sites,
        "cultural_claim_ids": cultural_claims,
        "dialect_entity_ids": lexical,
        "dialect_claim_ids": dialect_claims,
        "totals_at_selection": {
            "entities": len(entities), "aliases": len(aliases), "relationships": len(relationships), "claims": len(claims),
            "denominators": len(denominators), "coverage": len(coverage), "referenced_sources": len(sources),
            "bounded_populated_places": len(populated), "sites": len(sites), "cultural_claims": len(cultural_claims), "dialect_entities": len(lexical), "dialect_claims": len(dialect_claims),
        },
    }
    write_json(OUT, result)
    print(json.dumps({key: len(value) for key, value in result.items() if key.endswith("_ids")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
