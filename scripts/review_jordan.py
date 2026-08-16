#!/usr/bin/env python3
"""Independent-path, fixture-based review for the Jordan transferability pilot.

This reviewer does not call the Jordan importer. It reconstructs expected IDs,
parents, types, status, cultural scope, and coordinates from the checksum-bound
source fixtures, checks fixed stratified samples, and proves seven negative
mutants are rejected.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from model import ROOT, entity_id, read_jsonl, write_json

COUNTRY = "ENT-JO-COUNTRY"
SAMPLE_PATH = ROOT / "data/review/jordan_review_samples.json"
NEGATIVE_PATH = ROOT / "tests/fixtures/jordan_negative_cases.json"
REPORT_PATH = ROOT / "reports/jordan_independent_review.json"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def source_map() -> dict[str, dict[str, Any]]:
    rows = [load(path) for path in sorted((ROOT / "data/sources").glob("*.json"))]
    return {row["id"]: row for row in rows}


def expected_records() -> dict[str, Any]:
    hierarchy = load(ROOT / "data/imports/jordan/hierarchy_2024.json")
    heritage = load(ROOT / "data/imports/jordan/world_heritage_2026.json")
    admin: dict[str, dict[str, Any]] = {}
    site_place: dict[str, dict[str, Any]] = {}
    ids: dict[str, str] = {"country": COUNTRY}

    for governorate in hierarchy["governorates"]:
        gid = entity_id("JO", "jo_governorate", governorate["name_ar"], COUNTRY)
        ids[f"governorate:{governorate['key']}"] = gid
        admin[gid] = {"name": governorate["name_ar"], "type": "jo_governorate", "parent": COUNTRY, "status": "current"}
        for liwa in governorate["liwa"]:
            lid = entity_id("JO", "jo_liwa", liwa["name_ar"], governorate["key"])
            ids[f"liwa:{governorate['key']}:{liwa['key']}"] = lid
            admin[lid] = {"name": liwa["name_ar"], "type": "jo_liwa", "parent": gid, "status": "current", "valid_from": liwa["valid_from"]}
            for qada in liwa["qada"]:
                qid = entity_id("JO", "jo_qada", qada["name_ar"], f"{governorate['key']}:{liwa['key']}")
                ids[f"qada:{governorate['key']}:{liwa['key']}:{qada['key']}"] = qid
                admin[qid] = {"name": qada["name_ar"], "type": "jo_qada", "parent": lid, "status": "current"}

    for row in heritage["properties"]:
        identifier = entity_id("JO", row["entity_type"], row["name_ar"], f"world-heritage:{row['key']}")
        ids[f"site:{row['key']}"] = identifier
        site_place[identifier] = {
            "name": row["name_ar"], "type": row["entity_type"], "status": "current", "source_id": row["source_id"],
            "parent": ids[f"governorate:{row['parent_governorate']}"], "latitude": row["latitude"], "longitude": row["longitude"], "kind": "site", "key": row["key"],
        }
    for row in heritage["bounded_populated_places"]["places"]:
        identifier = entity_id("JO", row["entity_type"], row["name_ar"], f"bounded-place:{row['key']}")
        ids[f"place:{row['key']}"] = identifier
        site_place[identifier] = {
            "name": row["name_ar"], "type": row["entity_type"], "status": row["status"], "source_id": row["source_id"],
            "parent": ids[f"governorate:{row['parent_governorate']}"], "latitude": row["latitude"], "longitude": row["longitude"], "kind": "place", "key": row["key"],
            "property": ids[f"site:{row['property_key']}"],
        }
    return {"admin": admin, "site_place": site_place, "ids": ids, "hierarchy": hierarchy, "heritage": heritage}


def pilot_state() -> dict[str, Any]:
    entities = [row for row in read_jsonl(ROOT / "data/entities/entities.jsonl") if row.get("country_code") == "JO"]
    entity_ids = {row["id"] for row in entities}
    aliases = [row for row in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if row.get("entity_id") in entity_ids]
    relationships = [row for row in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if row.get("child_id") in entity_ids]
    claims = [row for row in read_jsonl(ROOT / "data/claims/claims.jsonl") if row.get("subject_id") in entity_ids]
    denominators = [row for row in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if row.get("country_code") == "JO" and row.get("layer") != "country_scope"]
    coverage = [row for row in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if row.get("country_code") == "JO" and row.get("layer") != "country_scope"]
    return {"entities": entities, "aliases": aliases, "relationships": relationships, "claims": claims, "denominators": denominators, "coverage": coverage, "sources": source_map()}


def issue_codes(state: dict[str, Any], expected: dict[str, Any]) -> set[str]:
    issues: set[str] = set()
    entities = state["entities"]
    aliases = state["aliases"]
    relationships = state["relationships"]
    claims = state["claims"]
    sources = state["sources"]
    entity_by_id = {row["id"]: row for row in entities}

    if any(not row.get("source_id") or row.get("source_id") not in sources or not row.get("source_locator") or row.get("verification_status") not in {"verified", "disputed"} for row in claims):
        issues.add("unsupported_claim")

    admin_rels: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in relationships:
        if row.get("relationship_type") == "administrative_parent":
            admin_rels[row["child_id"]].append(row)
    for identifier, exp in expected["admin"].items():
        actual = entity_by_id.get(identifier)
        rels = admin_rels.get(identifier, [])
        if not actual or actual.get("entity_type") != exp["type"] or len(rels) != 1 or rels[0].get("parent_id") != exp["parent"]:
            issues.add("wrong_parent_type")

    for identifier, exp in expected["site_place"].items():
        actual = entity_by_id.get(identifier)
        if not actual:
            continue
        if exp["kind"] == "place" and (actual.get("status") != exp["status"] or actual.get("entity_type") != exp["type"]):
            issues.add("historical_current_confusion")
        coords = actual.get("coordinates") or {}
        if abs(float(coords.get("latitude", 999)) - exp["latitude"]) > 0.000001 or abs(float(coords.get("longitude", 999)) - exp["longitude"]) > 0.000001 or coords.get("source_id") != exp["source_id"]:
            issues.add("coordinate_mismatch")

    national_predicates = {"food_practice", "performance_practice"}
    if any(row.get("predicate") in national_predicates and row.get("subject_id") != COUNTRY for row in claims):
        issues.add("national_to_local_leakage")
    allowed_bedu = {expected["ids"]["site:petra"], expected["ids"]["site:wadi-rum"]}
    if any(row.get("source_id") == "SRC-UNESCO-ICH-JO-00122" and row.get("subject_id") not in allowed_bedu for row in claims):
        issues.add("cultural_misattribution")

    alias_keys = [(row.get("entity_id"), row.get("language"), row.get("kind"), row.get("name", "").strip().casefold()) for row in aliases]
    if len(alias_keys) != len(set(alias_keys)):
        issues.add("duplicate_alias")
    return issues


def mutate(state: dict[str, Any], kind: str, expected: dict[str, Any]) -> None:
    if kind == "unsupported_claim":
        state["claims"][0]["source_id"] = "SRC-MISSING-NEGATIVE"
    elif kind == "wrong_parent_type":
        qada = next(identifier for identifier, row in expected["admin"].items() if row["type"] == "jo_qada")
        next(row for row in state["relationships"] if row.get("child_id") == qada and row.get("relationship_type") == "administrative_parent")["parent_id"] = COUNTRY
    elif kind == "historical_current_confusion":
        historical = next(identifier for identifier, row in expected["site_place"].items() if row["kind"] == "place" and row["status"] == "historical")
        next(row for row in state["entities"] if row["id"] == historical)["status"] = "current"
    elif kind == "national_to_local_leakage":
        row = next(row for row in state["claims"] if row.get("predicate") == "food_practice")
        row["subject_id"] = expected["ids"]["place:as-salt-city"]
    elif kind == "cultural_misattribution":
        row = next(row for row in state["claims"] if row.get("source_id") == "SRC-UNESCO-ICH-JO-00122")
        row["subject_id"] = expected["ids"]["place:as-salt-city"]
    elif kind == "duplicate_alias":
        duplicate = copy.deepcopy(state["aliases"][0])
        duplicate["id"] = "ALS-NEGATIVE-DUPLICATE"
        state["aliases"].append(duplicate)
    elif kind == "coordinate_mismatch":
        identifier = next(identifier for identifier, row in expected["site_place"].items() if row["kind"] == "site")
        next(row for row in state["entities"] if row["id"] == identifier)["coordinates"]["latitude"] += 1.0
    else:
        raise AssertionError(f"unknown mutation {kind}")


def input_fingerprint() -> str:
    paths = [
        ROOT / "data/entities/entities.jsonl", ROOT / "data/aliases/aliases.jsonl", ROOT / "data/relationships/relationships.jsonl",
        ROOT / "data/claims/claims.jsonl", ROOT / "data/coverage/denominators.jsonl", ROOT / "data/coverage/coverage.jsonl",
        ROOT / "data/imports/jordan/hierarchy_2024.json", ROOT / "data/imports/jordan/world_heritage_2026.json",
        ROOT / "data/imports/jordan/cultural_content_2026.json", ROOT / "data/imports/jordan/entity_resolution_2026.json",
        SAMPLE_PATH, NEGATIVE_PATH,
    ] + sorted((ROOT / "data/sources").glob("*JO*.json"))
    digest = hashlib.sha256()
    for path in paths:
        digest.update(str(path.relative_to(ROOT)).encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def review() -> dict[str, Any]:
    sample = load(SAMPLE_PATH)
    negative = load(NEGATIVE_PATH)
    expected = expected_records()
    state = pilot_state()
    errors: list[str] = []

    baseline_issues = issue_codes(state, expected)
    if baseline_issues:
        errors.append(f"baseline issue codes: {sorted(baseline_issues)}")

    by_family = {family: {row["id"]: row for row in state[family]} for family in ["entities", "aliases", "relationships", "claims", "denominators", "coverage"]}
    for sample_field, family in [
        ("entity_ids", "entities"), ("alias_ids", "aliases"), ("relationship_ids", "relationships"),
        ("claim_ids", "claims"), ("denominator_ids", "denominators"), ("coverage_ids", "coverage"),
    ]:
        missing = sorted(set(sample[sample_field]) - set(by_family[family]))
        if missing:
            errors.append(f"{sample_field} missing from {family}: {missing}")
    missing_sources = sorted(set(sample["source_ids"]) - set(state["sources"]))
    if missing_sources:
        errors.append(f"sample sources missing: {missing_sources}")

    # Sampled field review against independently reconstructed fixture expectations.
    entity_by_id = by_family["entities"]
    expected_entities = {**expected["admin"], **expected["site_place"]}
    for identifier in sample["entity_ids"]:
        actual = entity_by_id.get(identifier, {})
        exp = expected_entities.get(identifier, {})
        if actual.get("canonical_name") != exp.get("name") or actual.get("entity_type") != exp.get("type") or actual.get("status") != exp.get("status"):
            errors.append(f"sample entity mismatch: {identifier}")
        if not actual.get("canonical_source_id") or not actual.get("source_locator"):
            errors.append(f"sample entity lacks source/locator: {identifier}")
    for identifier in sample["coordinate_entity_ids"]:
        if "coordinate_mismatch" in issue_codes({**state, "entities": [entity_by_id[identifier]] + [row for row in state["entities"] if row["id"] not in expected["site_place"]]}, expected):
            errors.append(f"sample coordinate mismatch: {identifier}")

    for identifier in sample["source_ids"]:
        source = state["sources"][identifier]
        required = ["title", "publisher", "retrieved_at", "url", "locator", "source_type", "quality_tier", "license", "language", "country_codes"]
        if any(source.get(field) in (None, "", []) for field in required):
            errors.append(f"sample source metadata incomplete: {identifier}")
        if source.get("author") is None and source.get("organization") is None:
            errors.append(f"sample source lacks both author and organization: {identifier}")

    coverage_by_id = by_family["coverage"]
    den_by_id = by_family["denominators"]
    for identifier in sample["coverage_ids"]:
        cov = coverage_by_id[identifier]
        den = den_by_id[cov["denominator_id"]]
        if cov["matched"] + cov["excluded"] != den["value"] or cov["unmatched"] != 0 or not cov["complete"]:
            errors.append(f"coverage equation not closed: {identifier}")

    resolution = load(ROOT / "data/imports/jordan/entity_resolution_2026.json")
    if not resolution.get("method", "").startswith("Before insertion") or resolution.get("existing_jordan_records_before_import") != [COUNTRY] or len(resolution.get("candidate_decisions", [])) != 12:
        errors.append("entity resolution phase/order or denominator failed")
    resolved_candidates = {row["candidate"] for row in resolution["candidate_decisions"]}
    expected_candidates = {row["name_en"] for row in expected["heritage"]["properties"]} | {row["name_en"] for row in expected["heritage"]["bounded_populated_places"]["places"]}
    if resolved_candidates != expected_candidates:
        errors.append("entity resolution does not cover all 12 site/place candidates")

    domain = load(ROOT / "data/cultural/jordan_domain_status.json")
    dialect_claims = [row for row in state["claims"] if row.get("predicate") in {"dialect_form", "lexical_form", "pronunciation"}]
    if domain.get("domains", {}).get("dialect", {}).get("status") != "not_documented" or dialect_claims:
        errors.append("dialect absence/status review failed")

    negative_outcomes: dict[str, str] = {}
    for case in negative["cases"]:
        mutant = copy.deepcopy(state)
        mutate(mutant, case["mutation"], expected)
        found = issue_codes(mutant, expected)
        passed = case["expected_issue"] in found
        negative_outcomes[case["id"]] = "pass" if passed else "fail"
        if not passed:
            errors.append(f"negative case not rejected: {case['id']} (issues={sorted(found)})")

    totals = {
        "hierarchy": len(expected["admin"]),
        "entities": len(state["entities"]) - 1,
        "aliases": len(state["aliases"]) - 1,
        "relationships": len(state["relationships"]),
        "claims": len(state["claims"]),
        "sources": len([identifier for identifier in state["sources"] if "-JO-" in identifier or identifier.endswith("-JO-2026")]),
        "populated_places": len([row for row in state["entities"] if row["entity_type"] in {"city", "historical_place"}]),
        "cultural_attribution": len([row for row in state["claims"] if row.get("source_id", "").startswith("SRC-UNESCO-ICH-JO-")]),
        "entity_resolution": 12,
        "coordinate_entities": len(expected["site_place"]),
        "denominators": len(state["denominators"]),
        "coverage": len(state["coverage"]),
        "dialect_attribution": 1,
    }
    reviewed = {
        "hierarchy": len(sample["hierarchy_entity_ids"]), "entities": len(sample["entity_ids"]), "aliases": len(sample["alias_ids"]),
        "relationships": len(sample["relationship_ids"]), "claims": len(sample["claim_ids"]), "sources": len(sample["source_ids"]),
        "populated_places": len(sample["populated_place_ids"]), "cultural_attribution": len(sample["cultural_claim_ids"]),
        "entity_resolution": 12, "coordinate_entities": len(sample["coordinate_entity_ids"]),
        "denominators": len(sample["denominator_ids"]), "coverage": len(sample["coverage_ids"]), "dialect_attribution": 1,
    }
    rates = {name: round(reviewed[name] / total, 4) for name, total in totals.items()}
    below = {name: rate for name, rate in rates.items() if rate < 0.10}
    if below:
        errors.append(f"sample rates below 10%: {below}")

    return {
        "schema_version": "2.0.0", "country_code": "JO", "snapshot_date": "2026-08-15",
        "review_method": "Separate reviewer; fixed stratified samples checked against source fixtures, plus full invariant checks and seven injected negative mutants. No Tunisia samples or fixtures are reused.",
        "reviewer": "automated-independent-path",
        "input_fingerprint_sha256": input_fingerprint(),
        "passed": not errors,
        "totals": totals,
        "reviewed": reviewed,
        "sample_rates": rates,
        "baseline_issue_codes": sorted(baseline_issues),
        "negative_test_outcomes": negative_outcomes,
        "p0_findings": 0 if not errors else len(errors),
        "p1_findings": 0,
        "errors": errors,
    }


def main() -> int:
    report = review()
    write_json(REPORT_PATH, report)
    print(json.dumps({"passed": report["passed"], "reviewed": report["reviewed"], "negative_tests": report["negative_test_outcomes"], "errors": report["errors"]}, ensure_ascii=False, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
