#!/usr/bin/env python3
"""Dependency-free Phase 0/1/2 validator for canonical and repaired legacy data."""
from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from model import COUNTRIES, NAME_TO_ISO, ROOT, assert_clean_text, norm_name, read_jsonl, scalar, write_json

SCHEMA_FILES = {
    "entities": (ROOT / "schema/entity.schema.json", ROOT / "data/entities/entities.jsonl"),
    "aliases": (ROOT / "schema/alias.schema.json", ROOT / "data/aliases/aliases.jsonl"),
    "relationships": (ROOT / "schema/relationship.schema.json", ROOT / "data/relationships/relationships.jsonl"),
    "claims": (ROOT / "schema/claim.schema.json", ROOT / "data/claims/claims.jsonl"),
    "snapshots": (ROOT / "schema/snapshot.schema.json", ROOT / "data/snapshots/snapshots.jsonl"),
    "denominators": (ROOT / "schema/denominator.schema.json", ROOT / "data/coverage/denominators.jsonl"),
    "coverage": (ROOT / "schema/coverage.schema.json", ROOT / "data/coverage/coverage.jsonl"),
}
LEGACY_FIELDS = [
    "id", "الدولة", "الوحدة_الإدارية_العليا", "المستوى_الثاني",
    "المدينة_أو_القرية", "الحي_أو_الحارة", "الاسم_المحلي",
    "الأسماء_البديلة", "النوع", "خط_العرض", "خط_الطول", "الارتفاع_م",
    "السكان", "سنة_السكان", "المصدر", "تاريخ_المصدر", "درجة_الثقة", "ملاحظات",
]
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class Validation:
    def __init__(self):
        self.errors: list[dict[str, str]] = []
        self.checks: dict[str, dict[str, Any]] = {}

    def error(self, check: str, location: str, message: str):
        self.errors.append({"check": check, "location": location, "message": message})

    def result(self, check: str, **details: Any):
        self.checks[check] = {"status": "fail" if any(e["check"] == check for e in self.errors) else "pass", **details}


def json_type_ok(value: Any, wanted: str) -> bool:
    if wanted == "null": return value is None
    if wanted == "object": return isinstance(value, dict)
    if wanted == "array": return isinstance(value, list)
    if wanted == "string": return isinstance(value, str)
    if wanted == "boolean": return isinstance(value, bool)
    if wanted == "integer": return isinstance(value, int) and not isinstance(value, bool)
    if wanted == "number": return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
    return True


def validate_schema_value(value: Any, schema: dict[str, Any], location: str, emit) -> None:
    if not schema:
        return
    if "oneOf" in schema:
        matches = []
        for branch in schema["oneOf"]:
            branch_errors = []
            validate_schema_value(value, branch, location, lambda _loc, msg: branch_errors.append(msg))
            if not branch_errors:
                matches.append(branch)
        if len(matches) != 1:
            emit(location, f"oneOf expected exactly one match, got {len(matches)}")
        return
    if "const" in schema and value != schema["const"]:
        emit(location, f"expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        emit(location, f"value {value!r} is not in enum")
    types = schema.get("type")
    if types:
        choices = [types] if isinstance(types, str) else types
        if not any(json_type_ok(value, choice) for choice in choices):
            emit(location, f"expected type {choices}, got {type(value).__name__}")
            return
    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                emit(location, f"missing required property {key!r}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    emit(f"{location}.{key}", "additional property is not allowed")
        for key, child in value.items():
            if key in properties:
                validate_schema_value(child, properties[key], f"{location}.{key}", emit)
    elif isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            emit(location, f"requires at least {schema['minItems']} items")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in value]
            if len(serialized) != len(set(serialized)):
                emit(location, "array items are not unique")
        if "items" in schema:
            for index, item in enumerate(value):
                validate_schema_value(item, schema["items"], f"{location}[{index}]", emit)
    elif isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            emit(location, f"requires minimum length {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            emit(location, f"does not match pattern {schema['pattern']}")
        fmt = schema.get("format")
        if fmt == "date":
            try:
                if not DATE_RE.fullmatch(value): raise ValueError
                date.fromisoformat(value)
            except ValueError:
                emit(location, "is not an ISO YYYY-MM-DD date")
        elif fmt == "uri":
            parsed = urlparse(value)
            if not parsed.scheme or (parsed.scheme in {"http", "https"} and not parsed.netloc):
                emit(location, "is not an absolute URI")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            emit(location, f"is less than minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            emit(location, f"is greater than maximum {schema['maximum']}")


def load_json(path: Path, validation: Validation, check="structured_data") -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        validation.error(check, str(path.relative_to(ROOT)), f"cannot parse JSON: {exc}")
        return None


def validate_all() -> tuple[Validation, dict[str, list[dict[str, Any]]]]:
    v = Validation()
    records: dict[str, list[dict[str, Any]]] = {}

    # Executable schema artifacts and record-level schema checks.
    schema_paths = sorted((ROOT / "schema").glob("*.schema.json"))
    expected = {"entity", "alias", "relationship", "source", "claim", "snapshot", "denominator", "coverage", "manifest"}
    present = {path.name.removesuffix(".schema.json") for path in schema_paths}
    for missing in sorted(expected - present):
        v.error("schemas", "schema", f"missing executable schema {missing}.schema.json")
    schema_ids = []
    for path in schema_paths:
        schema = load_json(path, v, "schemas")
        if not isinstance(schema, dict):
            continue
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            v.error("schemas", str(path.relative_to(ROOT)), "must declare JSON Schema draft 2020-12")
        if not schema.get("$id"):
            v.error("schemas", str(path.relative_to(ROOT)), "missing $id")
        schema_ids.append(schema.get("$id"))
    if len(schema_ids) != len(set(schema_ids)):
        v.error("schemas", "schema", "duplicate schema $id")
    v.result("schemas", executable_schemas=len(schema_paths))

    for family, (schema_path, data_path) in SCHEMA_FILES.items():
        schema = load_json(schema_path, v)
        try:
            family_records = read_jsonl(data_path)
        except (OSError, UnicodeError, ValueError) as exc:
            v.error("structured_data", str(data_path.relative_to(ROOT)), str(exc))
            family_records = []
        records[family] = family_records
        if isinstance(schema, dict):
            for index, record in enumerate(family_records, 1):
                loc = f"{data_path.relative_to(ROOT)}:{index}"
                validate_schema_value(record, schema, loc, lambda where, msg: v.error("structured_data", where, msg))
                try:
                    assert_clean_text(record, loc)
                except ValueError as exc:
                    v.error("unicode", loc, str(exc))

    source_schema = load_json(ROOT / "schema/source.schema.json", v)
    source_files = sorted((ROOT / "data/sources").glob("*.json"))
    source_records = []
    for path in source_files:
        source = load_json(path, v)
        if isinstance(source, dict):
            source_records.append(source)
            validate_schema_value(source, source_schema, str(path.relative_to(ROOT)), lambda where, msg: v.error("structured_data", where, msg))
            try: assert_clean_text(source, str(path.relative_to(ROOT)))
            except ValueError as exc: v.error("unicode", str(path.relative_to(ROOT)), str(exc))
    records["sources"] = source_records

    manifest_schema = load_json(ROOT / "schema/manifest.schema.json", v)
    manifests = []
    for path in sorted((ROOT / "manifests").glob("*.yml")):
        manifest = load_json(path, v)
        if isinstance(manifest, dict):
            manifests.append(manifest)
            validate_schema_value(manifest, manifest_schema, str(path.relative_to(ROOT)), lambda where, msg: v.error("manifests", where, msg))
            if path.stem != manifest.get("country", {}).get("iso2"):
                v.error("manifests", str(path.relative_to(ROOT)), "filename and country ISO do not match")
    records["manifests"] = manifests
    v.result("structured_data", record_families=len(SCHEMA_FILES) + 1, records=sum(len(records[k]) for k in SCHEMA_FILES) + len(source_records))

    # Global IDs and controlled entity types.
    all_ids: list[tuple[str, str]] = []
    for family in [*SCHEMA_FILES, "sources"]:
        for row in records[family]:
            if row.get("id"):
                all_ids.append((row["id"], family))
    counts = Counter(identifier for identifier, _ in all_ids)
    for identifier, count in counts.items():
        if count > 1:
            v.error("ids", identifier, f"global ID appears {count} times")
    vocab = load_json(ROOT / "schema/vocabularies.json", v)
    allowed_types = set(vocab.get("entity_types", [])) if isinstance(vocab, dict) else set()
    forbidden_types = set(vocab.get("forbidden_active_types", [])) if isinstance(vocab, dict) else set()
    for entity in records["entities"]:
        if entity.get("entity_type") not in allowed_types or entity.get("entity_type") in forbidden_types:
            v.error("entity_types", entity.get("id", "?"), f"uncontrolled or forbidden type {entity.get('entity_type')!r}")
        if len(entity.get("canonical_name", "")) > 120 or "\n" in entity.get("canonical_name", ""):
            v.error("entity_types", entity.get("id", "?"), "canonical name looks like prose rather than an entity name")
        if entity.get("id", "").split("-")[1:2] != [entity.get("country_code")]:
            v.error("country_mismatch", entity.get("id", "?"), "entity ID ISO prefix and country_code differ")
    v.result("ids", global_ids=len(all_ids), duplicate_ids=sum(count - 1 for count in counts.values() if count > 1))
    v.result("entity_types", allowed_types=len(allowed_types), active_types=len({e.get("entity_type") for e in records["entities"]}))

    entity_by_id = {row["id"]: row for row in records["entities"] if "id" in row}
    source_by_id = {row["id"]: row for row in records["sources"] if "id" in row}
    snapshot_by_id = {row["id"]: row for row in records["snapshots"] if "id" in row}
    denominator_by_id = {row["id"]: row for row in records["denominators"] if "id" in row}
    coverage_by_id = {row["id"]: row for row in records["coverage"] if "id" in row}
    manifest_by_iso = {m.get("country", {}).get("iso2"): m for m in manifests}

    # Source integrity and complete metadata.
    refs: list[tuple[str, str, str | None]] = []
    for entity in records["entities"]:
        refs.append((entity["id"], "canonical_source_id", entity.get("canonical_source_id")))
        if entity.get("coordinates"):
            refs.append((entity["id"], "coordinates.source_id", entity["coordinates"].get("source_id")))
    for family in ["aliases", "relationships", "claims", "snapshots", "denominators", "coverage"]:
        for row in records[family]:
            refs.append((row.get("id", "?"), "source_id", row.get("source_id")))
            if family == "claims" and row.get("second_source_id"):
                refs.append((row["id"], "second_source_id", row["second_source_id"]))
    for identifier, field, source_id in refs:
        if source_id is not None and source_id not in source_by_id:
            v.error("sources", identifier, f"{field} references missing {source_id}")
    for source in records["sources"]:
        for field in ["title", "publisher", "url", "retrieved_at", "license", "language", "locator"]:
            if not source.get(field):
                v.error("sources", source.get("id", "?"), f"atomic source metadata missing {field}")
        if source.get("publication_date") is None and "Publication" not in (source.get("notes") or ""):
            v.error("sources", source.get("id", "?"), "unavailable publication_date requires an explicit reason in notes")
        if not set(source.get("country_codes", [])) <= set(COUNTRIES):
            v.error("sources", source.get("id", "?"), "source country_codes contain an out-of-scope code")
    v.result("sources", atomic_files=len(source_files), sources=len(source_records), references=len(refs))

    # Parent links, country integrity, manifest hierarchy, and cycles.
    admin_rels = [row for row in records["relationships"] if row.get("relationship_type") == "administrative_parent"]
    parents_by_child: dict[str, list[str]] = defaultdict(list)
    graph: dict[str, list[str]] = defaultdict(list)
    hierarchy_pairs = {}
    for iso, manifest in manifest_by_iso.items():
        for level in manifest.get("hierarchy", []):
            hierarchy_pairs[(iso, level.get("entity_type"))] = set(level.get("allowed_parent_types", []))
    for rel in records["relationships"]:
        child = entity_by_id.get(rel.get("child_id"))
        parent = entity_by_id.get(rel.get("parent_id"))
        if not child:
            v.error("orphans", rel.get("id", "?"), f"missing child entity {rel.get('child_id')}")
        if not parent:
            v.error("orphans", rel.get("id", "?"), f"missing parent entity {rel.get('parent_id')}")
        if not child or not parent:
            continue
        if child["country_code"] != parent["country_code"]:
            v.error("country_mismatch", rel["id"], "child and parent countries differ")
        if rel.get("relationship_type") == "administrative_parent":
            parents_by_child[child["id"]].append(parent["id"])
            graph[child["id"]].append(parent["id"])
            allowed = hierarchy_pairs.get((child["country_code"], child["entity_type"]))
            if allowed is None:
                v.error("hierarchy", rel["id"], "child type is absent from its country manifest")
            elif parent["entity_type"] not in allowed:
                v.error("hierarchy", rel["id"], f"parent type {parent['entity_type']} not allowed for {child['entity_type']}")
    administrative_types = {entity_type for (_iso, entity_type) in hierarchy_pairs}
    contextual_links: dict[str, int] = defaultdict(int)
    for rel in records["relationships"]:
        if rel.get("relationship_type") in {"located_in", "associated_with"}:
            contextual_links[rel.get("child_id", "")] += 1
    for entity in records["entities"]:
        count = len(parents_by_child.get(entity["id"], []))
        if entity["entity_type"] == "country":
            if count:
                v.error("hierarchy", entity["id"], "country must not have administrative parent")
        elif entity["entity_type"] in administrative_types:
            if count != 1:
                v.error("orphans", entity["id"], f"administrative entity must have exactly one administrative parent, got {count}")
        else:
            if count:
                v.error("hierarchy", entity["id"], "non-administrative entity must use located_in/associated_with, not administrative_parent")
            if contextual_links.get(entity["id"], 0) < 1:
                v.error("orphans", entity["id"], "non-administrative entity requires a sourced located_in or associated_with relationship")

    visiting, visited = set(), set()
    def visit(node: str, trail: list[str]):
        if node in visiting:
            v.error("cycles", node, "administrative cycle: " + " -> ".join(trail + [node]))
            return
        if node in visited: return
        visiting.add(node)
        for parent in graph.get(node, []): visit(parent, trail + [node])
        visiting.remove(node); visited.add(node)
    for node in entity_by_id: visit(node, [])
    v.result("parents", administrative_relationships=len(admin_rels))
    v.result("orphans", orphan_count=sum(1 for e in v.errors if e["check"] == "orphans"))
    v.result("cycles", cycle_count=sum(1 for e in v.errors if e["check"] == "cycles"))
    v.result("country_mismatch", mismatch_count=sum(1 for e in v.errors if e["check"] == "country_mismatch"))
    v.result("hierarchy", declared_pairs=len(hierarchy_pairs))

    # Aliases: references, country, normalized duplication, and canonical-name collision.
    alias_keys: dict[tuple[str, str, str, str], str] = {}
    alias_norm = lambda value: " ".join(value.casefold().split())
    for row in records["aliases"]:
        entity = entity_by_id.get(row.get("entity_id"))
        if not entity:
            v.error("aliases", row.get("id", "?"), "alias subject entity does not exist")
            continue
        # Preserve meaningful Arabic orthographic variants (for example hamza forms);
        # duplicate detection therefore folds case/spacing, not Arabic letters.
        key = (row["entity_id"], row.get("language", ""), row.get("kind", ""), alias_norm(row.get("name", "")))
        if key in alias_keys:
            v.error("aliases", row["id"], f"duplicate normalized alias of {alias_keys[key]}")
        alias_keys[key] = row["id"]
        if alias_norm(row["name"]) == alias_norm(entity["canonical_name"]):
            v.error("aliases", row["id"], "alias duplicates the entity canonical name")
    v.result("aliases", aliases=len(records["aliases"]), duplicate_aliases=sum(1 for e in v.errors if e["check"] == "aliases" and "duplicate" in e["message"]))

    # Claims and coordinates.
    for row in records["claims"]:
        if row.get("subject_id") not in entity_by_id:
            v.error("claims", row.get("id", "?"), "claim subject does not exist")
        if not row.get("source_id"):
            v.error("claims", row.get("id", "?"), "claim lacks source_id")
        if not row.get("source_locator"):
            v.error("claims", row.get("id", "?"), "claim lacks source_locator")
        if bool(row.get("second_source_id")) != bool(row.get("second_source_locator")):
            v.error("claims", row.get("id", "?"), "second source and second source locator must occur together")
        if row.get("sensitivity") == "sensitive" and row.get("status") != "disputed":
            if not row.get("second_source_id") or row.get("second_source_id") == row.get("source_id"):
                v.error("claims", row["id"], "sensitive non-disputed claim requires two independent sources")
        if row.get("published") and row.get("verification_status") not in {"verified", "source_verified"}:
            v.error("claims", row["id"], "published claim must have a publishable verification status")
        if any(token in row.get("predicate", "") for token in {"food", "clothing", "custom"}) and not row.get("classification"):
            v.error("claims", row["id"], "food, clothing, and custom claims require explicit classification")
        if row.get("predicate", "").startswith("lexical_"):
            context = row.get("lexical_context")
            if not context:
                v.error("claims", row["id"], "lexical claim requires lexical_context")
            elif not context.get("study_date") or context.get("place_id") not in entity_by_id:
                v.error("claims", row["id"], "lexical claim requires a study date and existing place")
        typed = row.get("value", {})
        data = typed.get("data")
        expected = typed.get("type")
        if expected == "integer" and not json_type_ok(data, "integer"):
            v.error("claims", row["id"], "claim typed as integer but data is not an integer")
        if expected == "number" and not json_type_ok(data, "number"):
            v.error("claims", row["id"], "claim typed as number but data is not numeric")
        if expected == "boolean" and not json_type_ok(data, "boolean"):
            v.error("claims", row["id"], "claim typed as boolean but data is not boolean")
    for entity in records["entities"]:
        coords = entity.get("coordinates")
        if coords and not (-90 <= coords["latitude"] <= 90 and -180 <= coords["longitude"] <= 180):
            v.error("coordinates", entity["id"], "coordinates out of bounds")
    # Published Tunisia claim quality, entity deduplication, and Phase 2 invariants.
    tn_ids = {row["id"] for row in records["entities"] if row.get("country_code") == "TN"}
    tn_published = [row for row in records["claims"] if row.get("subject_id") in tn_ids and row.get("published")]
    ab_claims = [row for row in tn_published if source_by_id.get(row.get("source_id"), {}).get("quality_tier") in {"A", "B"}]
    ab_ratio = round(len(ab_claims) / len(tn_published) * 100, 2) if tn_published else 0.0
    if ab_ratio < 95:
        v.error("source_quality", "TN", f"published A/B claim ratio is {ab_ratio}%; minimum is 95%")
    v.result("source_quality", tunisia_published_claims=len(tn_published), ab_claims=len(ab_claims), ab_ratio=ab_ratio)

    aliases_by_entity: dict[str, set[str]] = defaultdict(set)
    for row in records["aliases"]:
        aliases_by_entity[row["entity_id"]].add(norm_name(row["name"]))
    context_targets: dict[str, set[str]] = defaultdict(set)
    for row in records["relationships"]:
        if row.get("relationship_type") in {"administrative_parent", "located_in", "associated_with"}:
            context_targets[row["child_id"]].add(row["parent_id"])
    tn_entities = [row for row in records["entities"] if row.get("country_code") == "TN"]
    duplicate_candidates = 0
    by_type_parent: dict[tuple[str, tuple[str, ...]], list[dict[str, Any]]] = defaultdict(list)
    for row in tn_entities:
        by_type_parent[(row["entity_type"], tuple(sorted(context_targets[row["id"]])))].append(row)
    for (_type, _parents), group in by_type_parent.items():
        for index, left in enumerate(group):
            left_names = {norm_name(left["canonical_name"])} | aliases_by_entity[left["id"]]
            for right in group[index + 1:]:
                right_names = {norm_name(right["canonical_name"])} | aliases_by_entity[right["id"]]
                if not left_names & right_names:
                    continue
                lc, rc = left.get("coordinates"), right.get("coordinates")
                close = not lc or not rc or (abs(lc["latitude"] - rc["latitude"]) <= 0.02 and abs(lc["longitude"] - rc["longitude"]) <= 0.02)
                if close and left.get("status") == right.get("status"):
                    duplicate_candidates += 1
                    v.error("duplicates", f"{left['id']} / {right['id']}", "same type, context, name/alias, status, and compatible coordinates")
    claim_keys: dict[tuple[str, str, str], str] = {}
    for row in records["claims"]:
        key = (row["subject_id"], row["predicate"], json.dumps(row["value"], ensure_ascii=False, sort_keys=True))
        if key in claim_keys:
            v.error("duplicates", row["id"], f"duplicate claim content of {claim_keys[key]}")
        claim_keys[key] = row["id"]
    v.result("duplicates", entity_candidates=duplicate_candidates, duplicate_claims=sum(1 for e in v.errors if e["check"] == "duplicates" and "claim" in e["message"]))

    tn_counts = Counter(row["entity_type"] for row in tn_entities)
    expected_counts = {"tn_governorate": 24, "tn_delegation": 264, "tn_municipality": 350, "tn_imada": 2084}
    for entity_type, expected_count in expected_counts.items():
        if tn_counts[entity_type] != expected_count:
            v.error("phase2_tunisia", entity_type, f"expected {expected_count}, got {tn_counts[entity_type]}")
    municipality_ids = {row["id"] for row in tn_entities if row["entity_type"] == "tn_municipality"}
    delegation_ids = {row["id"] for row in tn_entities if row["entity_type"] == "tn_delegation"}
    overlap_rels = [row for row in records["relationships"] if row.get("relationship_type") == "boundary_intersects" and row.get("child_id") in municipality_ids]
    if {row["child_id"] for row in overlap_rels} != municipality_ids or {row["parent_id"] for row in overlap_rels} != delegation_ids:
        v.error("phase2_tunisia", "boundary_intersects", "overlap evidence must span all 350 municipalities and all 264 dated delegations")
    place_types = {"city", "town", "village", "settlement", "neighborhood", "historical_place"}
    if not place_types <= {row["entity_type"] for row in tn_entities}:
        v.error("phase2_tunisia", "populated_places", "bounded pilot must keep all six requested place classifications distinct")
    if tn_counts["person"] < 1 or not ({"archaeological_site", "market", "landmark", "natural_site"} <= set(tn_counts)):
        v.error("phase2_tunisia", "pilot_entities", "person and archaeological/market/landmark/natural entities are required")
    review_path = ROOT / "reports/tunisia_independent_review.json"
    review = load_json(review_path, v, "independent_review") if review_path.is_file() else None
    if not isinstance(review, dict):
        v.error("independent_review", str(review_path.relative_to(ROOT)), "review artifact is missing or invalid")
    else:
        allowed_outcomes = {"correct", "incorrect", "unsupported", "ambiguous", "needs_review"}
        if not review.get("passed") or any(rate < 0.10 for rate in review.get("sample_rates", {}).values()):
            v.error("independent_review", "TN", "every record family requires at least a 10% sample and a passing review")
        if set(review.get("sample_rates", {})) != {"entity", "claim", "source", "hierarchy"}:
            v.error("independent_review", "TN", "review must span entity, claim, source, and hierarchy families")
        if any(item.get("outcome") not in allowed_outcomes for item in review.get("reviews", [])):
            v.error("independent_review", "TN", "review contains an uncontrolled outcome")
        if any(outcome != "correct" and count for outcome, count in review.get("outcomes", {}).items()):
            v.error("independent_review", "TN", "only correct outcomes may remain in a passing review")
        span = review.get("span", {})
        tn_relationships = [row for row in records["relationships"] if row["child_id"] in tn_ids]
        tn_source_ids = {
            *(row["canonical_source_id"] for row in tn_entities),
            *(row["source_id"] for row in tn_relationships),
            *(row["source_id"] for row in tn_published),
            *(row["second_source_id"] for row in tn_published if row.get("second_source_id")),
        }
        expected_span = {
            "entity_types_sampled": {row["entity_type"] for row in tn_entities},
            "claim_domains_sampled": {"population", "populated_place", "person", "culture", "site"},
            "source_tiers_sampled": {source_by_id[source_id]["quality_tier"] for source_id in tn_source_ids},
            "relationship_types_sampled": {row["relationship_type"] for row in tn_relationships},
        }
        for key, expected in expected_span.items():
            if set(span.get(key, {})) != expected:
                v.error("independent_review", "TN", f"review stratum {key} does not span its universe")
    v.result("independent_review", sampled=(sum(review.get("sample", {}).values()) if isinstance(review, dict) else 0), passed=bool(review and review.get("passed")))
    v.result("phase2_tunisia", **{key: tn_counts[key] for key in expected_counts}, populated_place_types=len(place_types & set(tn_counts)), sites=sum(tn_counts[t] for t in {"archaeological_site", "market", "landmark", "natural_site", "cultural_site"}), persons=tn_counts["person"], boundary_intersections=len(overlap_rels))

    v.result("claims", claims=len(records["claims"]), sourced=sum(bool(row.get("source_id")) for row in records["claims"]))
    v.result("coordinates", coordinate_records=sum(bool(row.get("coordinates")) for row in records["entities"]))

    # Coverage arithmetic, dates, denominators, exclusions, and constrained 100% assertions.
    for den in records["denominators"]:
        if den.get("denominator") != den.get("value"):
            v.error("coverage", den.get("id", "?"), "denominator mirror must equal value")
        if den.get("snapshot_date") != den.get("as_of"):
            v.error("coverage", den.get("id", "?"), "snapshot_date mirror must equal as_of")
    for row in records["coverage"]:
        den = denominator_by_id.get(row.get("denominator_id"))
        snap = snapshot_by_id.get(row.get("snapshot_id"))
        if not den: v.error("coverage", row.get("id", "?"), "denominator does not exist")
        if not snap: v.error("coverage", row.get("id", "?"), "snapshot does not exist")
        if not den: continue
        if (row.get("country_code"), row.get("layer")) != (den.get("country_code"), den.get("layer")):
            v.error("coverage", row["id"], "coverage and denominator scope differ")
        if row.get("denominator") != den.get("value"):
            v.error("coverage", row["id"], "coverage denominator mirror differs from denominator record")
        if snap and row.get("snapshot_date") != snap.get("captured_at"):
            v.error("coverage", row["id"], "snapshot_date differs from snapshot captured_at")
        if not row.get("license"):
            v.error("coverage", row["id"], "layer record requires an explicit license/reuse statement")
        if sum(item.get("count", 0) for item in row.get("exclusion_reasons", [])) != row.get("excluded"):
            v.error("coverage", row["id"], "exclusion reason counts must sum to excluded")
        value = den.get("value")
        if value is None:
            if row.get("coverage_percentage") is not None or row.get("complete"):
                v.error("coverage", row["id"], "unavailable denominator cannot have a percentage or complete=true")
            if not row.get("missing_reason") or not den.get("missing_reason"):
                v.error("coverage", row["id"], "unavailable denominator requires missing_reason in both records")
            if row.get("missing") is not None:
                v.error("coverage", row["id"], "unavailable denominator requires missing=null")
        else:
            completed = row["matched"] + row["excluded"]
            expected_percent = round(completed / value * 100, 2) if value else (100.0 if completed == 0 else None)
            expected_missing = value - completed
            if expected_missing < 0:
                v.error("coverage", row["id"], "matched + excluded exceeds denominator")
            if row.get("coverage_percentage") != expected_percent:
                v.error("coverage", row["id"], f"coverage_percentage should be {expected_percent}")
            if row.get("missing") != expected_missing or row.get("unmatched") != expected_missing:
                v.error("coverage", row["id"], "missing and unmatched must equal denominator - matched - excluded")
            expected_complete = completed == value
            if row.get("complete") != expected_complete:
                v.error("coverage", row["id"], "complete must equal (matched + excluded == denominator)")
            if not expected_complete and not row.get("missing_reason"):
                v.error("coverage", row["id"], "incomplete known-denominator layer requires missing_reason")
        if row.get("coverage_percentage") == 100:
            if not (row.get("country_code") and row.get("layer") and row.get("snapshot_date") and row.get("snapshot_id") and row.get("source_id") and row.get("license")):
                v.error("coverage", row["id"], "100% lacks country, layer, date, denominator, snapshot, source, or license")
            if den.get("status") != "official" or not row.get("complete") or row.get("missing") != 0:
                v.error("coverage", row["id"], "100% requires official denominator, complete=true, and missing=0")
    v.result("coverage", denominators=len(records["denominators"]), coverage_records=len(records["coverage"]), complete_layers=sum(bool(row.get("complete")) for row in records["coverage"]))

    # Manifest coverage and hierarchy source references.
    if set(manifest_by_iso) != set(COUNTRIES):
        v.error("manifests", "manifests", f"expected exactly {sorted(COUNTRIES)}, got {sorted(manifest_by_iso)}")
    if len(manifests) != 22:
        v.error("manifests", "manifests", f"expected 22 manifests, got {len(manifests)}")
    for iso, manifest in manifest_by_iso.items():
        country_id = manifest.get("country", {}).get("entity_id")
        if country_id not in entity_by_id or entity_by_id[country_id].get("country_code") != iso:
            v.error("manifests", iso or "?", "country entity missing or mismatched")
        for sid in manifest.get("official_authority", {}).get("source_ids", []):
            if sid not in source_by_id: v.error("manifests", iso, f"authority source missing: {sid}")
        if manifest.get("snapshot", {}).get("snapshot_id") not in snapshot_by_id:
            v.error("manifests", iso, "manifest snapshot missing")
        for level in manifest.get("hierarchy", []):
            if level.get("entity_type") not in allowed_types:
                v.error("manifests", iso, f"hierarchy uses uncontrolled type {level.get('entity_type')}")
            for sid in level.get("source_ids", []):
                if sid not in source_by_id: v.error("manifests", iso, f"hierarchy source missing: {sid}")
        for cid in manifest.get("coverage_record_ids", []):
            if cid not in coverage_by_id:
                v.error("manifests", iso, f"coverage record missing: {cid}")
            elif coverage_by_id[cid].get("country_code") != iso:
                v.error("manifests", iso, f"coverage country mismatch: {cid}")
    v.result("manifests", manifests=len(manifests), countries=len(manifest_by_iso), pilot_migrated=sum(m.get("status") == "pilot_migrated" for m in manifests))

    # Legacy CSV syntax, global IDs, coordinates, known repairs, and row ledger.
    legacy_ids: dict[str, list[str]] = defaultdict(list)
    csv_rows = []
    csv_files = sorted((ROOT / "قاعدة_بيانات_الأماكن").glob("*.csv"))
    for path in csv_files:
        rel = str(path.relative_to(ROOT))
        try:
            with path.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.reader(handle)
                rows = list(reader)
        except (OSError, UnicodeError, csv.Error) as exc:
            v.error("csv", rel, f"cannot parse: {exc}")
            continue
        if not rows:
            v.error("csv", rel, "empty CSV")
            continue
        if rows[0] != LEGACY_FIELDS:
            v.error("csv", f"{rel}:1", f"unexpected header or field order ({len(rows[0])} fields)")
        for row_no, row in enumerate(rows[1:], 2):
            if len(row) != len(LEGACY_FIELDS):
                v.error("csv", f"{rel}:{row_no}", f"malformed row has {len(row)} fields; expected {len(LEGACY_FIELDS)}")
                continue
            data = dict(zip(LEGACY_FIELDS, row))
            csv_rows.append((rel, row_no, data))
            legacy_ids[data["id"]].append(f"{rel}:{row_no}")
            is_template = path.name == "قالب_السجل.csv"
            if not is_template and data["الدولة"] and data["الدولة"] not in NAME_TO_ISO:
                v.error("csv", f"{rel}:{row_no}", f"unrecognized country {data['الدولة']!r}")
            lat, lon = scalar(data["خط_العرض"]), scalar(data["خط_الطول"])
            if bool(lat) != bool(lon):
                v.error("coordinates", f"{rel}:{row_no}", "legacy latitude and longitude must occur together")
            if lat and lon:
                try:
                    if not (-90 <= float(lat) <= 90 and -180 <= float(lon) <= 180): raise ValueError
                except ValueError:
                    v.error("coordinates", f"{rel}:{row_no}", "invalid legacy coordinates")
            try: assert_clean_text(data, f"{rel}:{row_no}")
            except ValueError as exc: v.error("unicode", f"{rel}:{row_no}", str(exc))
    for identifier, locations in legacy_ids.items():
        if len(locations) > 1:
            v.error("csv", identifier, f"duplicate legacy ID remains at {locations}")
    ledger = read_jsonl(ROOT / "data/quarantine/migration_ledger.jsonl")
    ledger_keys = {(row.get("path"), row.get("row")) for row in ledger}
    csv_keys = {(rel, row_no) for rel, row_no, _ in csv_rows}
    if ledger_keys != csv_keys:
        v.error("migration", "migration_ledger", f"ledger keys differ from CSV rows: missing={len(csv_keys-ledger_keys)}, extra={len(ledger_keys-csv_keys)}")
    repair_log = read_jsonl(ROOT / "data/quarantine/legacy_repairs.jsonl")
    link_log = read_jsonl(ROOT / "data/quarantine/link_repairs.jsonl")
    malformed_repairs = sum(row.get("action") == "join_excess_csv_fields_into_notes" for row in repair_log)
    duplicate_repairs = sum(row.get("action") == "rename_duplicate_legacy_id" for row in repair_log)
    if (malformed_repairs, duplicate_repairs) != (2, 58):
        v.error("migration", "legacy_repairs.jsonl", f"expected 2 malformed-row and 58 duplicate-occurrence repairs, got {malformed_repairs} and {duplicate_repairs}")
    if len(link_log) != 25:
        v.error("migration", "link_repairs.jsonl", f"expected 25 link repairs, got {len(link_log)}")
    v.result("csv", files=len(csv_files), rows=len(csv_rows), duplicate_ids=sum(len(x)-1 for x in legacy_ids.values() if len(x)>1), malformed_rows=sum(1 for e in v.errors if e["check"] == "csv" and "malformed" in e["message"]))
    v.result("unicode", checked="active JSON, source JSON, and legacy CSV")
    v.result("migration", ledger_rows=len(ledger), legacy_rows=len(csv_rows), malformed_repairs=malformed_repairs, duplicate_id_repairs=duplicate_repairs, link_repairs=len(link_log))

    # Markdown links: local targets must exist; external targets must be syntactically valid.
    checked_links = 0
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        try: text = path.read_text(encoding="utf-8")
        except UnicodeError as exc:
            v.error("unicode", str(path.relative_to(ROOT)), str(exc)); continue
        for line_no, line in enumerate(text.splitlines(), 1):
            for match in LINK_RE.finditer(line):
                checked_links += 1
                target = match.group(1).strip().split()[0].strip("<>")
                if not target or target.startswith("#"): continue
                parsed = urlparse(target)
                if parsed.scheme:
                    if parsed.scheme not in {"http", "https", "mailto"} or (parsed.scheme in {"http", "https"} and not parsed.netloc):
                        v.error("links", f"{path.relative_to(ROOT)}:{line_no}", f"invalid external link {target}")
                    continue
                local = unquote(target.split("#", 1)[0])
                if not local: continue
                resolved = (path.parent / local).resolve()
                try: resolved.relative_to(ROOT.resolve())
                except ValueError:
                    v.error("links", f"{path.relative_to(ROOT)}:{line_no}", f"link escapes repository: {target}"); continue
                if not resolved.exists():
                    v.error("links", f"{path.relative_to(ROOT)}:{line_no}", f"broken local link: {target}")
    v.result("links", checked_links=checked_links, broken_links=sum(1 for e in v.errors if e["check"] == "links"))

    return v, records


def main() -> int:
    validation, records = validate_all()
    report = {
        "status": "pass" if not validation.errors else "fail",
        "errors": validation.errors,
        "checks": validation.checks,
        "counts": {family: len(items) for family, items in records.items()},
    }
    write_json(ROOT / "reports/validation.json", report)
    for name, result in validation.checks.items():
        details = ", ".join(f"{k}={value}" for k, value in result.items() if k != "status")
        print(f"[{result['status'].upper():4}] {name}: {details}")
    if validation.errors:
        print(f"\n{len(validation.errors)} validation error(s):", file=sys.stderr)
        for error in validation.errors[:100]:
            print(f"- {error['check']} {error['location']}: {error['message']}", file=sys.stderr)
        if len(validation.errors) > 100:
            print(f"... {len(validation.errors)-100} more", file=sys.stderr)
        return 1
    print("\nSchema v1 validation passed with zero errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
