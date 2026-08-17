#!/usr/bin/env python3
"""Independent deterministic 10% second-pass review for the Tunisia pilot.

This intentionally does not import the importer or validator.  It samples each
record family with a fixed seed, then independently checks source binding,
identity, hierarchy/context links, typed claims, and required locators.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SEED = "tunisia-phase2-independent-review-2026-08-15-v1"
RATE = 0.10
OUT = ROOT / "reports/tunisia_independent_review.json"


def jsonl(path: str) -> list[dict[str, Any]]:
    return [json.loads(line) for line in (ROOT / path).read_text(encoding="utf-8").splitlines() if line.strip()]


def choose(records: list[dict[str, Any]], key: str, family: str, stratum=None) -> list[dict[str, Any]]:
    """At least ceil(10%), with one random record per required stratum."""
    if not records:
        return []
    rng = random.Random(f"{SEED}:{family}")
    ordered = sorted(records, key=lambda row: row[key])
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in ordered:
        groups[str(stratum(row) if stratum else "all")].append(row)
    count = max(math.ceil(len(records) * RATE), len(groups))
    picked = [rng.choice(groups[name]) for name in sorted(groups)]
    picked_ids = {row[key] for row in picked}
    remaining = [row for row in ordered if row[key] not in picked_ids]
    picked.extend(rng.sample(remaining, count - len(picked)))
    return picked


def result(family: str, row: dict[str, Any], checks: list[tuple[bool, str]]) -> dict[str, Any]:
    failures = [label for passed, label in checks if not passed]
    outcome = "correct" if not failures else "incorrect"
    identifier = row.get("id", "?")
    return {
        "review_id": "REV-" + hashlib.sha256(f"{family}:{identifier}".encode()).hexdigest()[:16].upper(),
        "family": family, "record_id": identifier, "outcome": outcome,
        "checks": [label for passed, label in checks if passed], "failures": failures,
        "reviewer": "independent_second_pass_v1", "reviewed_at": "2026-08-15",
    }


def main() -> int:
    entities = jsonl("data/entities/entities.jsonl")
    aliases = jsonl("data/aliases/aliases.jsonl")
    relationships = jsonl("data/relationships/relationships.jsonl")
    claims = jsonl("data/claims/claims.jsonl")
    sources = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((ROOT / "data/sources").glob("*.json"))]
    tn_entities = [row for row in entities if row["country_code"] == "TN"]
    tn_ids = {row["id"] for row in tn_entities}
    tn_relationships = [row for row in relationships if row["child_id"] in tn_ids]
    tn_claims = [row for row in claims if row["subject_id"] in tn_ids and row.get("published")]
    referenced_sources = {
        *(row["canonical_source_id"] for row in tn_entities),
        *(row["source_id"] for row in tn_relationships),
        *(row["source_id"] for row in tn_claims),
        *(row["second_source_id"] for row in tn_claims if row.get("second_source_id")),
    }
    tn_sources = [row for row in sources if row["id"] in referenced_sources]

    entity_by_id = {row["id"]: row for row in entities}
    source_by_id = {row["id"]: row for row in sources}
    links_by_child: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for rel in relationships:
        links_by_child[rel["child_id"]].append(rel)
    reviews: list[dict[str, Any]] = []

    for row in choose(tn_entities, "id", "entity", lambda row: row["entity_type"]):
        links = links_by_child[row["id"]]
        has_context = row["entity_type"] == "country" or any(rel["relationship_type"] in {"administrative_parent", "located_in", "associated_with"} for rel in links)
        reviews.append(result("entity", row, [
            (row["id"].startswith("ENT-TN-"), "Tunisia ID prefix and country binding"),
            (row["canonical_source_id"] in source_by_id, "canonical source exists"),
            (bool(row.get("source_locator")), "canonical source locator is present"),
            (has_context, "administrative or contextual hierarchy link exists"),
            (row.get("verification_status") in {"verified", "source_verified"}, "verification is publishable"),
        ]))

    def claim_domain(row):
        predicate = row["predicate"]
        if predicate == "population": return "population"
        if predicate == "place_classification": return "populated_place"
        if predicate in {"place_connection", "significance"}: return "person"
        if predicate.endswith("_practice") or predicate == "traditional_clothing_goods": return "culture"
        return "site"
    for row in choose(tn_claims, "id", "claim", claim_domain):
        value = row.get("value", {})
        sensitive_ok = row.get("sensitivity") != "sensitive" or row.get("status") == "disputed" or (
            row.get("second_source_id") in source_by_id and bool(row.get("second_source_locator"))
        )
        reviews.append(result("claim", row, [
            (row["subject_id"] in entity_by_id, "claim subject exists"),
            (row["source_id"] in source_by_id, "claim source exists"),
            (bool(row.get("source_locator")), "claim source locator is present"),
            (isinstance(value, dict) and {"type", "data"} <= set(value), "claim value is typed"),
            (sensitive_ok, "sensitive-claim two-source/disputed policy"),
            (row.get("published") is True, "claim is explicitly published"),
        ]))

    for row in choose(tn_sources, "id", "source", lambda row: row["quality_tier"]):
        reviews.append(result("source", row, [
            (row.get("quality_tier") in {"A", "B", "C", "D"}, "quality tier is classified"),
            (bool(row.get("publisher")), "publisher is present"),
            (bool(row.get("url")), "URL is present"),
            (bool(row.get("retrieved_at")), "retrieval date is present"),
            (bool(row.get("license")), "license/reuse statement is present"),
            (bool(row.get("locator")), "source locator is present"),
        ]))

    for row in choose(tn_relationships, "id", "hierarchy", lambda row: row["relationship_type"]):
        child = entity_by_id.get(row["child_id"])
        parent = entity_by_id.get(row["parent_id"])
        correct_country = bool(child and parent and child["country_code"] == parent["country_code"] == "TN")
        boundary_ok = row["relationship_type"] != "boundary_intersects" or (
            child and parent and child["entity_type"] == "tn_municipality" and parent["entity_type"] == "tn_delegation" and row["source_id"] == "SRC-TN-RESEARCH-GEOMETRY-2018"
        )
        reviews.append(result("hierarchy", row, [
            (child is not None, "child exists"), (parent is not None, "parent exists"),
            (correct_country, "child and parent remain in Tunisia"),
            (row["source_id"] in source_by_id, "relationship source exists"),
            (bool(row.get("source_locator")), "relationship locator is present"),
            (boundary_ok, "boundary-overlap semantics and Tier C provenance are explicit"),
        ]))

    universes = {
        "entity": len(tn_entities), "claim": len(tn_claims),
        "source": len(tn_sources), "hierarchy": len(tn_relationships),
    }
    samples = Counter(row["family"] for row in reviews)
    outcomes = Counter(row["outcome"] for row in reviews)
    by_entity_type = Counter(entity_by_id[row["record_id"]]["entity_type"] for row in reviews if row["family"] == "entity")
    claims_by_id = {row["id"]: row for row in tn_claims}
    sources_by_id = {row["id"]: row for row in tn_sources}
    relationships_by_id = {row["id"]: row for row in tn_relationships}
    by_claim_domain = Counter(claim_domain(claims_by_id[row["record_id"]]) for row in reviews if row["family"] == "claim")
    by_source_tier = Counter(sources_by_id[row["record_id"]]["quality_tier"] for row in reviews if row["family"] == "source")
    by_relationship_type = Counter(relationships_by_id[row["record_id"]]["relationship_type"] for row in reviews if row["family"] == "hierarchy")
    report = {
        "schema_version": "2.0.0", "country_code": "TN", "review_date": "2026-08-15",
        "method": "Fixed-seed stratified random sample independently drawn within entity, published claim, referenced source, and Tunisia relationship families; at least 10% per family with every entity type, claim domain, source tier, and relationship type represented; independent second-pass rules do not import validator or importer code.",
        "independence": "Independent automated code path and seed; not an external human review. Source content candidates were separately inspected during Phase 2 research.",
        "seed": SEED, "target_rate": RATE, "allowed_outcomes": ["correct", "incorrect", "unsupported", "ambiguous", "needs_review"],
        "universe": universes, "sample": dict(samples),
        "sample_rates": {family: round(samples[family] / total, 4) if total else 0 for family, total in universes.items()},
        "outcomes": dict(outcomes), "passed": set(outcomes) <= {"correct"},
        "span": {
            "entity_types_sampled": dict(sorted(by_entity_type.items())),
            "claim_domains_sampled": dict(sorted(by_claim_domain.items())),
            "source_tiers_sampled": dict(sorted(by_source_tier.items())),
            "relationship_types_sampled": dict(sorted(by_relationship_type.items())),
        },
        "reviews": sorted(reviews, key=lambda row: (row["family"], row["record_id"])),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"universe": universes, "sample": dict(samples), "outcomes": dict(outcomes), "passed": report["passed"]}, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
