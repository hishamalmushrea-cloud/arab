#!/usr/bin/env python3
"""Semantic validation for the bounded UAE fourth-country pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from model import ROOT, read_jsonl, write_json

REPORT = ROOT / "reports/uae_validation.json"
GENERIC_UAE_TYPES = {"ae_municipal_region", "ae_sector", "ae_district"}
CONTEXTUAL_TYPES = {
    "ae_abu_dhabi_municipality_jurisdiction",
    "ae_dubai_planning_sector",
    "ae_dubai_planning_community",
    "ae_sharjah_municipality_jurisdiction",
    "ae_ajman_constituent",
    "ae_uaq_municipal_authority",
    "ae_rak_administrative_area",
    "ae_fujairah_municipal_authority",
}
EXPECTED_TYPE_COUNTS = {
    "country": 1,
    "ae_emirate": 7,
    "ae_abu_dhabi_municipality_jurisdiction": 3,
    "ae_dubai_planning_sector": 9,
    "ae_sharjah_municipality_jurisdiction": 9,
    "ae_ajman_constituent": 3,
    "ae_uaq_municipal_authority": 2,
    "ae_rak_administrative_area": 5,
    "ae_fujairah_municipal_authority": 2,
}
REQUIRED_CONTEXT_WORDS = {
    "coastal": ("coast", "creek", "beach", "mangrove"),
    "desert": ("desert", "dune"),
    "mountain": ("mountain", "jebel", "foothill"),
    "oasis": ("oasis", "oases"),
    "urban": ("city centre", "urban"),
    "historical": ("historic", "historical", "heritage", "past", "originally"),
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_bundle() -> dict[str, Any]:
    entities = [row for row in read_jsonl(ROOT / "data/entities/entities.jsonl") if row.get("country_code") == "AE"]
    entity_ids = {row["id"] for row in entities}
    return {
        "entities": entities,
        "aliases": [row for row in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if row.get("entity_id") in entity_ids],
        "relationships": [row for row in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if row.get("child_id") in entity_ids],
        "claims": [row for row in read_jsonl(ROOT / "data/claims/claims.jsonl") if row.get("subject_id") in entity_ids],
        "denominators": [row for row in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if row.get("country_code") == "AE"],
        "coverage": [row for row in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if row.get("country_code") == "AE"],
        "snapshots": [row for row in read_jsonl(ROOT / "data/snapshots/snapshots.jsonl") if str(row.get("id", "")).startswith("SNP-AE-")],
        "sources": {record["id"]: record for path in sorted((ROOT / "data/sources").glob("*.json")) for record in [load_json(path)]},
        "manifest": load_json(ROOT / "manifests/AE.yml"),
        "raw_manifest": load_json(ROOT / "data/imports/uae/snapshot_manifest.json"),
        "culture_fixture": load_json(ROOT / "data/imports/uae/fixtures/cultural_claims.json"),
    }


def norm(value: str) -> str:
    return " ".join(value.casefold().split())


def validate_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    checks: dict[str, dict[str, Any]] = {}

    def error(code: str, message: str, severity: str = "P1") -> None:
        errors.append({"code": code, "severity": severity, "message": message})

    def check(name: str, **metrics: Any) -> None:
        checks[name] = {"status": "PASS", **metrics}

    entities = bundle["entities"]
    aliases = bundle["aliases"]
    relationships = bundle["relationships"]
    claims = bundle["claims"]
    denominators = bundle["denominators"]
    coverage = bundle["coverage"]
    sources = bundle["sources"]
    manifest = bundle["manifest"]
    entity_by_id = {row["id"]: row for row in entities}
    if len(entity_by_id) != len(entities):
        error("UAE_IDENTITY_COLLAPSE", "duplicate UAE entity IDs indicate collapsed identities")

    type_counts = Counter(row.get("entity_type") for row in entities)
    if dict(type_counts) != EXPECTED_TYPE_COUNTS:
        error("UAE_ENTITY_COUNTS", f"expected {EXPECTED_TYPE_COUNTS}, got {dict(type_counts)}")
    if any(row.get("entity_type") in GENERIC_UAE_TYPES for row in entities):
        error("UAE_LOCAL_TYPE", "deprecated generic UAE lower type used by a new pilot entity")
    if any(row.get("entity_type", "").startswith("ae_") and row.get("entity_type") not in CONTEXTUAL_TYPES | {"ae_emirate"} for row in entities):
        error("UAE_LOCAL_TYPE", "unrecognized UAE contextual type")
    check("entities", entities=len(entities), contextual_types=len(CONTEXTUAL_TYPES), type_counts=dict(sorted(type_counts.items())))

    profiles = manifest.get("emirate_profiles", [])
    if len(profiles) != 7 or len({row.get("emirate_id") for row in profiles}) != 7:
        error("UAE_EMIRATE_PROFILES", "manifest must contain seven unique emirate profiles")
    expected_by_id: dict[str, dict[str, Any]] = {}
    expected_parent: dict[str, str] = {}
    for profile in profiles:
        eid = profile.get("emirate_id")
        expected_by_id[eid] = {"entity_type": "ae_emirate", "layer": "emirates"}
        expected_parent[eid] = "ENT-AE-COUNTRY"
        if profile.get("parent_id") != "ENT-AE-COUNTRY" or profile.get("snapshot_date") != "2026-08-15":
            error("UAE_EMIRATE_PROFILES", f"invalid parent/snapshot for {eid}")
        for layer in profile.get("lower_layers", []):
            for child_id in layer.get("entity_ids", []):
                if child_id in expected_by_id:
                    error("UAE_IDENTITY_COLLAPSE", f"{child_id} appears in multiple emirate/layer profiles")
                expected_by_id[child_id] = layer
                expected_parent[child_id] = eid
    if set(expected_by_id) != (set(entity_by_id) - {"ENT-AE-COUNTRY"}):
        missing = sorted(set(expected_by_id) - set(entity_by_id))
        extra = sorted((set(entity_by_id) - {"ENT-AE-COUNTRY"}) - set(expected_by_id))
        error("UAE_PROFILE_MEMBERSHIP", f"manifest/entity mismatch missing={missing}, extra={extra}")
    for eid, expected in expected_by_id.items():
        entity = entity_by_id.get(eid)
        if entity and entity.get("entity_type") != expected.get("entity_type"):
            error("UAE_LOCAL_TYPE", f"{eid} expected {expected.get('entity_type')}, got {entity.get('entity_type')}")
    check("emirate_profiles", profiles=len(profiles), profiled_entities=len(expected_by_id))

    admin = [row for row in relationships if row.get("relationship_type") == "administrative_parent"]
    parents: dict[str, list[str]] = defaultdict(list)
    for row in admin:
        parents[row.get("child_id")].append(row.get("parent_id"))
    for child_id, expected in expected_parent.items():
        actual = parents.get(child_id, [])
        if actual != [expected]:
            if len(set(actual)) > 1:
                error("UAE_IDENTITY_COLLAPSE", f"{child_id} was collapsed across parents {sorted(set(actual))}")
            error("UAE_PARENT_PROFILE", f"{child_id} expected parent {expected}, got {actual}")
    if any(row.get("child_id") == "ENT-AE-COUNTRY" for row in admin):
        error("UAE_PARENT_PROFILE", "country cannot have an administrative parent")
    check("relationships", relationships=len(relationships), administrative_parents=len(admin), orphans=0 if not any(e["code"] == "UAE_PARENT_PROFILE" for e in errors) else None)

    alias_by_entity: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in aliases:
        alias_by_entity[row.get("entity_id")].append(row)
        if row.get("kind") in {"historical", "former"} and row.get("status") == "current":
            error("UAE_TEMPORAL_STATUS", f"historical/former alias marked current: {row.get('id')}")
    for eid in expected_by_id:
        arabic = [row for row in alias_by_entity[eid] if row.get("language") == "ar" and row.get("status") == "current"]
        if len(arabic) != 1:
            error("UAE_ALIAS_POLICY", f"{eid} requires exactly one current Arabic alias; got {len(arabic)}")
    julfar = [row for row in aliases if norm(row.get("name", "")) == "julfar"]
    if len(julfar) != 1 or julfar[0].get("kind") != "historical" or julfar[0].get("status") != "historical":
        error("UAE_TEMPORAL_STATUS", "Julfar must be one historical alias, never current")

    # An alias promoted to another entity under the same parent is a duplicate identity.
    canonical_context = {(norm(row.get("canonical_name", "")), tuple(parents.get(row["id"], []))): row["id"] for row in entities}
    for alias in aliases:
        subject = alias.get("entity_id")
        key = (norm(alias.get("name", "")), tuple(parents.get(subject, [])))
        other = canonical_context.get(key)
        if other and other != subject:
            error("UAE_ALIAS_ENTITY", f"alias {alias.get('id')} was promoted to entity {other} in the same parent scope")
    check("aliases", aliases=len(aliases), historical_aliases=sum(row.get("status") == "historical" for row in aliases))

    semantics = [row for row in claims if row.get("predicate") == "jurisdiction_semantics"]
    if len(semantics) != len(expected_by_id):
        error("UAE_SEMANTICS", f"expected {len(expected_by_id)} semantics claims, got {len(semantics)}")
    for row in semantics:
        data = row.get("value", {}).get("data", {})
        subject = row.get("subject_id")
        if not isinstance(data, dict) or not all(data.get(field) for field in ("authority", "parent_id", "snapshot_date", "semantic_definition", "layer")):
            error("UAE_SEMANTICS", f"incomplete semantics claim {row.get('id')}")
        elif data.get("parent_id") != expected_parent.get(subject) or data.get("snapshot_date") != "2026-08-15":
            error("UAE_SEMANTICS", f"semantics parent/snapshot mismatch for {subject}")

    food_art_sources = {"SRC-AE-UAE-FOOD-2024", "SRC-AE-UAE-ART-2024"}
    for row in claims:
        value_text = json.dumps(row.get("value", {}).get("data"), ensure_ascii=False).casefold()
        predicate = row.get("predicate", "")
        if "exclusive" in predicate or "exclusive" in value_text:
            if row.get("second_source_id") is None or row.get("classification") in {"shared", "regional", "national", "emirate_specific", "local"}:
                error("UAE_EXCLUSIVITY", f"unsupported exclusive cultural claim {row.get('id')}")
        if row.get("source_id") in food_art_sources and ("food" in predicate or "performance" in predicate or "craft" in predicate):
            if row.get("subject_id") != "ENT-AE-COUNTRY":
                error("UAE_NATIONAL_SCOPE", f"federal national cultural evidence localized in {row.get('id')}")
        if row.get("sensitivity") == "sensitive" and row.get("status") != "disputed":
            if not row.get("second_source_id") or row.get("second_source_id") == row.get("source_id"):
                error("UAE_SENSITIVE_SOURCE", f"sensitive claim lacks two independent sources: {row.get('id')}")

    culture = [row for row in claims if row.get("predicate") != "jurisdiction_semantics"]
    represented = {row.get("subject_id") for row in culture if str(row.get("subject_id", "")).startswith("ENT-AE-EMIRATE-")}
    required_emirates = {row["emirate_id"] for row in profiles}
    if represented != required_emirates:
        error("UAE_CULTURAL_SAMPLE", f"emirate cultural coverage differs: {sorted(represented)}")
    corpus = " ".join(json.dumps(row.get("value", {}).get("data"), ensure_ascii=False).casefold() for row in culture)
    context_hits = {name: any(word in corpus for word in words) for name, words in REQUIRED_CONTEXT_WORDS.items()}
    if not all(context_hits.values()):
        error("UAE_CULTURAL_SAMPLE", f"missing contexts: {[k for k, value in context_hits.items() if not value]}")
    dress_claims = [row for row in culture if "dress" in row.get("predicate", "") or "clothing" in row.get("predicate", "")]
    unsupported = bundle["culture_fixture"].get("unsupported_domains", [])
    if dress_claims or not any(row.get("domain") == "dress" and row.get("reason") for row in unsupported):
        error("UAE_CULTURAL_SAMPLE", "unsupported dress fields must remain empty with an explicit fixture reason")

    lexical = [row for row in claims if row.get("predicate") == "lexical_form"]
    if len(lexical) != 3:
        error("UAE_DIALECT", f"expected three bounded lexical claims, got {len(lexical)}")
    for row in lexical:
        context = row.get("lexical_context") or {}
        required = ("language", "variety", "place_id", "form", "meaning", "register", "study_date")
        if not all(context.get(field) for field in required):
            error("UAE_DIALECT", f"incomplete lexical context {row.get('id')}")
        if context.get("place_id") != "ENT-AE-COUNTRY" or context.get("study_date") != "2020-12-18":
            error("UAE_DIALECT", f"lexical place/date mismatch {row.get('id')}")
    waid_shoo = [row for row in lexical if row.get("value", {}).get("data") in {"وايد", "شو"}]
    if len(waid_shoo) != 2 or any(row.get("classification") != "regional" for row in waid_shoo):
        error("UAE_DIALECT", "Gulf/Levantine shared forms must remain regional, not uniquely Emirati")
    check("claims", claims=len(claims), semantics=len(semantics), cultural=len(culture), dialect=len(lexical), sensitive=sum(row.get("sensitivity") == "sensitive" for row in claims), contexts=context_hits)

    source_refs = set()
    for row in entities:
        source_refs.add(row.get("canonical_source_id"))
    for family in (aliases, relationships, claims, denominators, coverage, bundle["snapshots"]):
        for row in family:
            source_refs.add(row.get("source_id"))
            if row.get("second_source_id"):
                source_refs.add(row.get("second_source_id"))
    source_refs.update(manifest.get("official_authority", {}).get("source_ids", []))
    for row in manifest.get("hierarchy", []) + manifest.get("pilot_layers", []):
        source_refs.update(row.get("source_ids", []))
    for profile in manifest.get("emirate_profiles", []):
        source_refs.update(profile.get("source_ids", []))
        for layer in profile.get("lower_layers", []):
            source_refs.update(layer.get("source_ids", []))
    source_refs.discard(None)
    for sid in source_refs:
        source = sources.get(sid)
        if not source:
            error("UAE_SOURCE_MISSING", f"missing source {sid}")
            continue
        codes = set(source.get("country_codes", []))
        if codes and "AE" not in codes:
            error("UAE_FOREIGN_SOURCE", f"UAE record references foreign-only source {sid}: {sorted(codes)}")
    published = [row for row in claims if row.get("published")]
    ab = [row for row in published if sources.get(row.get("source_id"), {}).get("quality_tier") in {"A", "B"}]
    ab_ratio = round(len(ab) / len(published) * 100, 2) if published else 0.0
    if ab_ratio < 95:
        error("UAE_SOURCE_QUALITY", f"A/B published claim sourcing is {ab_ratio}%, below 95%")

    raw_manifest = bundle["raw_manifest"]
    for capture in raw_manifest.get("records", []):
        path = ROOT / "data/imports/uae" / capture["path"]
        payload = path.read_bytes() if path.exists() else b""
        if len(payload) != capture.get("bytes") or hashlib.sha256(payload).hexdigest() != capture.get("sha256"):
            error("UAE_SOURCE_CHECKSUM", f"capture mismatch: {capture.get('path')}", "P0")
    if len(raw_manifest.get("records", [])) != 19:
        error("UAE_SOURCE_CHECKSUM", "expected 19 persisted UAE evidence extracts", "P0")
    check("sources", referenced=len(source_refs), pilot_specific=sum(sid.startswith("SRC-AE-") for sid in source_refs), ab_claims=len(ab), published_claims=len(published), ab_ratio=ab_ratio, evidence_extracts=len(raw_manifest.get("records", [])))

    den_by_id = {row["id"]: row for row in denominators}
    cov_by_id = {row["id"]: row for row in coverage}
    if len(den_by_id) != 12 or len(cov_by_id) != 12:
        error("UAE_COVERAGE", f"expected 12 denominator/coverage pairs, got {len(den_by_id)}/{len(cov_by_id)}")
    closed = unavailable = 0
    for layer in manifest.get("pilot_layers", []):
        den = den_by_id.get(layer.get("denominator_id"))
        cov = cov_by_id.get(layer.get("coverage_record_id"))
        if not den or not cov:
            error("UAE_COVERAGE", f"missing records for manifest layer {layer.get('layer')}")
            continue
        if den.get("layer") != layer.get("layer") or cov.get("layer") != layer.get("layer"):
            error("UAE_COVERAGE", f"layer mismatch for {layer.get('layer')}")
        if den.get("source_id") != layer.get("source_ids", [None])[0] or cov.get("source_id") != den.get("source_id"):
            error("UAE_COVERAGE", f"source mismatch for {layer.get('layer')}")
        if den.get("denominator") is None:
            unavailable += 1
            if den.get("status") != "unavailable" or not den.get("missing_reason") or cov.get("coverage_percentage") is not None or cov.get("complete"):
                error("UAE_COVERAGE", f"unavailable layer incorrectly quantified: {layer.get('layer')}")
        else:
            closed += 1
            if cov.get("matched") + cov.get("excluded") != den.get("denominator") or cov.get("unmatched") != 0 or cov.get("coverage_percentage") != 100.0 or not cov.get("complete"):
                error("UAE_COVERAGE", f"closed layer does not balance: {layer.get('layer')}")
    expected_denominators = {"emirates": 7, "abu_dhabi_municipality_jurisdictions": 3, "dubai_planning_sectors": 9, "sharjah_municipality_jurisdictions": 9, "ajman_constituents": 3, "uaq_municipal_authorities": 2, "rak_administrative_areas": 5, "fujairah_municipal_authorities": 2}
    actual_denominators = {row["layer"]: row["denominator"] for row in denominators if row["layer"] in expected_denominators}
    if actual_denominators != expected_denominators:
        error("UAE_COVERAGE", f"bounded denominator mismatch: {actual_denominators}")
    check("coverage", denominators=len(denominators), coverage_records=len(coverage), closed_layers=closed, unavailable_layers=unavailable, bounded_denominators=expected_denominators)

    # Additive schema contract.
    vocab = load_json(ROOT / "schema/vocabularies.json")
    if not CONTEXTUAL_TYPES <= set(vocab.get("entity_types", [])):
        error("UAE_SCHEMA", "contextual UAE types missing from controlled vocabulary")
    if not {"renamed", "merged", "abolished"} <= set(vocab.get("entity_statuses", [])):
        error("UAE_SCHEMA", "explicit former-unit statuses missing")
    if "emirate_specific" not in vocab.get("claim_classifications", []):
        error("UAE_SCHEMA", "emirate_specific classification missing")
    if manifest.get("schema_version") != "1.0.0":
        error("UAE_SCHEMA", "additive pilot must remain Schema v1.0.0")
    check("schema", schema_version="1.0.0", additive_entity_types=8, additive_entity_statuses=3, additive_claim_classifications=1, optional_manifest_properties=1, deprecated_generic_types_retained=sorted(GENERIC_UAE_TYPES))

    # Mark checks that own at least one error as FAIL without making reports time-dependent.
    ownership = {
        "entities": {"UAE_ENTITY_COUNTS", "UAE_LOCAL_TYPE", "UAE_IDENTITY_COLLAPSE"},
        "emirate_profiles": {"UAE_EMIRATE_PROFILES", "UAE_PROFILE_MEMBERSHIP"},
        "relationships": {"UAE_PARENT_PROFILE", "UAE_IDENTITY_COLLAPSE"},
        "aliases": {"UAE_ALIAS_POLICY", "UAE_ALIAS_ENTITY", "UAE_TEMPORAL_STATUS"},
        "claims": {"UAE_SEMANTICS", "UAE_EXCLUSIVITY", "UAE_NATIONAL_SCOPE", "UAE_SENSITIVE_SOURCE", "UAE_CULTURAL_SAMPLE", "UAE_DIALECT"},
        "sources": {"UAE_SOURCE_MISSING", "UAE_FOREIGN_SOURCE", "UAE_SOURCE_QUALITY", "UAE_SOURCE_CHECKSUM"},
        "coverage": {"UAE_COVERAGE"},
        "schema": {"UAE_SCHEMA"},
    }
    codes = {row["code"] for row in errors}
    for name, owned in ownership.items():
        if codes & owned:
            checks[name]["status"] = "FAIL"

    p0 = sum(row["severity"] == "P0" for row in errors)
    p1 = sum(row["severity"] == "P1" for row in errors)
    return {
        "schema_version": "1.0.0",
        "country_code": "AE",
        "snapshot_date": "2026-08-15",
        "status": "PASS" if not errors else "FAIL",
        "checks": checks,
        "errors": errors,
        "p0": p0,
        "critical_p1": p1,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=REPORT)
    args = parser.parse_args()
    result = validate_bundle(load_bundle())
    write_json(args.report, result)
    for name, detail in result["checks"].items():
        metrics = ", ".join(f"{key}={value}" for key, value in detail.items() if key != "status")
        print(f"[{detail['status']}] {name}: {metrics}")
    if result["errors"]:
        print(f"UAE semantic validation failed with {len(result['errors'])} error(s).")
        for row in result["errors"]:
            print(f"- {row['severity']} {row['code']}: {row['message']}")
        return 1
    print("UAE semantic validation passed with zero P0/critical P1 findings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
