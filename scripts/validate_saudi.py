#!/usr/bin/env python3
"""Saudi-specific semantic and acceptance validator for the third-country cycle."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from model import ROOT, read_jsonl, write_json

REPORT = ROOT / "reports/saudi_validation.json"
COUNTRY = "ENT-SA-COUNTRY"
SNAPSHOT_DATE = "2026-08-15"
EXPECTED_NEGATIVE_IDS = {
    "NEG-SA-WRONG-GOVERNORATE",
    "NEG-SA-WRONG-CENTER-LINKAGE",
    "NEG-SA-ALIAS-AS-ENTITY",
    "NEG-SA-NATIONAL-TO-LOCAL-LEAKAGE",
    "NEG-SA-FOREIGN-COUNTRY-SOURCE",
    "NEG-SA-HISTORICAL-AS-CURRENT",
    "NEG-SA-POPULATION-WITHOUT-YEAR",
}


class Validation:
    def __init__(self) -> None:
        self.checks: dict[str, dict[str, Any]] = {}
        self.errors: list[str] = []

    def check(self, name: str, condition: bool, detail: str) -> None:
        self.checks[name] = {"status": "pass" if condition else "fail", "detail": detail}
        if not condition:
            self.errors.append(f"{name}: {detail}")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def review_input_fingerprint() -> str:
    """Recompute the review fingerprint without executing or importing the reviewer."""
    paths = [
        ROOT / "data/entities/entities.jsonl",
        ROOT / "data/aliases/aliases.jsonl",
        ROOT / "data/relationships/relationships.jsonl",
        ROOT / "data/claims/claims.jsonl",
        ROOT / "data/coverage/denominators.jsonl",
        ROOT / "data/coverage/coverage.jsonl",
        ROOT / "data/imports/saudi/snapshot_manifest.json",
        ROOT / "data/imports/saudi/cultural_content_2026.json",
        ROOT / "data/imports/saudi/parsed_registry.json",
        ROOT / "data/imports/saudi/anomaly_ledger.json",
        ROOT / "data/review/saudi_review_samples.json",
        ROOT / "tests/fixtures/saudi_negative_cases.json",
    ] + sorted((ROOT / "data/sources").glob("*SA*.json"))
    digest = hashlib.sha256()
    for path in paths:
        digest.update(str(path.relative_to(ROOT)).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def main() -> int:
    result = Validation()
    manifest = load(ROOT / "manifests/SA.yml")
    snapshots = load(ROOT / "data/imports/saudi/snapshot_manifest.json")
    parsed = load(ROOT / "data/imports/saudi/parsed_registry.json")
    summary = load(ROOT / "data/imports/saudi/import_summary.json")
    anomalies = load(ROOT / "data/imports/saudi/anomaly_ledger.json")
    cultural = load(ROOT / "data/imports/saudi/cultural_content_2026.json")

    all_entities = read_jsonl(ROOT / "data/entities/entities.jsonl")
    entities = [row for row in all_entities if row.get("country_code") == "SA"]
    ids = {row["id"] for row in entities}
    entity_by_id = {row["id"]: row for row in entities}
    aliases = [row for row in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if row.get("entity_id") in ids]
    relationships = [row for row in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if row.get("child_id") in ids]
    claims = [row for row in read_jsonl(ROOT / "data/claims/claims.jsonl") if row.get("subject_id") in ids]
    denominators = [row for row in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if row.get("country_code") == "SA"]
    coverage = [row for row in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if row.get("country_code") == "SA"]
    sources = {load(path)["id"]: load(path) for path in sorted((ROOT / "data/sources").glob("*.json"))}
    sa_sources = {identifier: row for identifier, row in sources.items() if row.get("country_codes") == ["SA"]}

    # Immutable retrieval evidence and a country-specific build path.
    checksum_errors: list[str] = []
    for row in snapshots.get("records", []):
        path = ROOT / "data/imports/saudi" / row["path"]
        payload = path.read_bytes() if path.is_file() else b""
        if len(payload) != row["bytes"] or hashlib.sha256(payload).hexdigest() != row["sha256"]:
            checksum_errors.append(row["path"])
    result.check(
        "checksum_bound_inputs",
        len(snapshots.get("records", [])) == 15 and not checksum_errors,
        f"snapshots={len(snapshots.get('records', []))}/15, mismatches={checksum_errors}",
    )
    country_paths = [
        ROOT / "scripts/import_saudi_phase3.py",
        ROOT / "scripts/review_saudi.py",
        ROOT / "scripts/build_saudi_review_samples.py",
        ROOT / "data/imports/saudi/cultural_content_2026.json",
    ]
    no_prior_country_import = all(
        "import_tunisia" not in path.read_text(encoding="utf-8").casefold()
        and "import_jordan" not in path.read_text(encoding="utf-8").casefold()
        for path in country_paths
    )
    foreign_refs = [
        row["id"]
        for row in entities + aliases + relationships + claims
        if "-TN-" in json.dumps(row, ensure_ascii=False) or "-JO-" in json.dumps(row, ensure_ascii=False)
    ]
    # The reviewer intentionally contains one JO source ID only as a negative mutant.
    result.check(
        "country_specific_method",
        no_prior_country_import and not foreign_refs,
        f"Saudi production path does not call prior-country importers; production foreign refs={len(foreign_refs)}",
    )

    # Exact record-family inventory.
    counts = Counter(row["entity_type"] for row in entities)
    expected_counts = {
        "country": 1,
        "sa_region": 13,
        "sa_governorate": 141,
        "sa_markaz": 1521,
        "city": 16,
        "historical_place": 1,
        "archaeological_site": 4,
        "cultural_site": 3,
        "natural_site": 1,
        "language": 1,
        "language_variety": 2,
        "lexical_form": 4,
    }
    result.check("entity_counts", dict(counts) == expected_counts, f"actual={dict(sorted(counts.items()))}")
    result.check(
        "record_family_counts",
        (len(entities), len(aliases), len(relationships), len(claims)) == (1708, 179, 1726, 1732),
        f"entities/aliases/relationships/claims={len(entities)}/{len(aliases)}/{len(relationships)}/{len(claims)}",
    )
    parser_totals = summary.get("parser_totals", {})
    expected_parser_totals = {
        "regions": 13,
        "governorate_rows": 141,
        "capital_city_rows": 13,
        "center_occurrences": 1523,
        "unique_parent_scoped_centers": 1521,
        "excluded_duplicate_occurrences": 2,
        "sum_of_page_declared_center_totals": 1528,
    }
    result.check(
        "registry_parse_totals",
        parser_totals == expected_parser_totals,
        f"actual={parser_totals}; parsed 1,523 rather than inventing the five-record declared-total gap",
    )

    # Administrative topology; seats are cities, not an invented administrative tier.
    admin_types = {"sa_region", "sa_governorate", "sa_markaz"}
    admin_rels = [row for row in relationships if row.get("relationship_type") == "administrative_parent"]
    parents: dict[str, list[str]] = defaultdict(list)
    for row in admin_rels:
        parents[row["child_id"]].append(row["parent_id"])
    allowed_parent_types = {
        "sa_region": {"country"},
        "sa_governorate": {"sa_region"},
        "sa_markaz": {"sa_region", "sa_governorate", "sa_nahiya"},
    }
    topology_errors = []
    for row in entities:
        if row["entity_type"] not in admin_types:
            continue
        parent_ids = parents.get(row["id"], [])
        actual_parent_types = {entity_by_id.get(parent_id, {}).get("entity_type") for parent_id in parent_ids}
        if len(parent_ids) != 1 or not actual_parent_types <= allowed_parent_types[row["entity_type"]]:
            topology_errors.append(row["id"])
    child_counts = Counter(entity_by_id[row["child_id"]]["entity_type"] for row in admin_rels)
    result.check(
        "administrative_topology",
        not topology_errors and child_counts == Counter({"sa_region": 13, "sa_governorate": 141, "sa_markaz": 1521}),
        f"parent links by type={dict(child_counts)}, errors={len(topology_errors)}; direct region→center is legal/source-backed",
    )
    seat_ids = {row["id"] for row in entities if row["id"].endswith("-SEAT") and row["entity_type"] == "city"}
    seat_rels = [row for row in relationships if row.get("relationship_type") == "seat_of" and row.get("child_id") in seat_ids]
    seat_claims = [row for row in claims if row.get("predicate") == "regional_capital_row"]
    result.check(
        "regional_seat_semantics",
        len(seat_ids) == len(seat_rels) == len(seat_claims) == 13
        and not any(row["id"].endswith("-SEAT") and row["entity_type"] in admin_types for row in entities),
        f"capital cities={len(seat_ids)}, seat relationships={len(seat_rels)}, capital-row claims={len(seat_claims)}",
    )

    # Identity, graph, aliases and source-country integrity.
    global_ids: list[str] = []
    for path in [
        "data/entities/entities.jsonl",
        "data/aliases/aliases.jsonl",
        "data/relationships/relationships.jsonl",
        "data/claims/claims.jsonl",
        "data/snapshots/snapshots.jsonl",
        "data/coverage/denominators.jsonl",
        "data/coverage/coverage.jsonl",
    ]:
        global_ids.extend(row["id"] for row in read_jsonl(ROOT / path))
    duplicate_ids = [identifier for identifier, count in Counter(global_ids).items() if count > 1]
    orphan_rels = [row["id"] for row in relationships if row.get("child_id") not in ids or row.get("parent_id") not in ids]
    country_mismatch = [
        row["id"]
        for row in relationships
        if row.get("parent_id") in entity_by_id
        and entity_by_id[row["child_id"]].get("country_code") != entity_by_id[row["parent_id"]].get("country_code")
    ]
    graph = defaultdict(list)
    for row in admin_rels:
        graph[row["child_id"]].append(row["parent_id"])
    cycles = []
    for start in graph:
        seen: set[str] = set()
        node = start
        while graph.get(node):
            if node in seen:
                cycles.append(start)
                break
            seen.add(node)
            node = graph[node][0]
    result.check(
        "identity_integrity",
        not duplicate_ids and not orphan_rels and not country_mismatch and not cycles,
        f"duplicate_ids={len(duplicate_ids)}, orphans={len(orphan_rels)}, country_mismatch={len(country_mismatch)}, cycles={len(cycles)}",
    )
    alias_keys = [(row["entity_id"], row["language"], row["kind"], row["name"].strip().casefold()) for row in aliases]
    canonical_names: dict[str, set[str]] = defaultdict(set)
    for row in entities:
        canonical_names[row["canonical_name"].strip().casefold()].add(row["id"])
    alias_entity_collisions = [
        row["id"]
        for row in aliases
        if canonical_names[row["name"].strip().casefold()] - {row["entity_id"]}
    ]
    result.check(
        "alias_resolution",
        len(alias_keys) == len(set(alias_keys)) and not alias_entity_collisions,
        f"aliases={len(alias_keys)}, duplicate keys={len(alias_keys)-len(set(alias_keys))}, alias-as-entity collisions={len(alias_entity_collisions)}",
    )

    # Atomic source metadata, source tiers and traceability.
    required_source_fields = [
        "title", "publisher", "retrieved_at", "url", "locator", "source_type",
        "quality_tier", "license", "language", "country_codes",
    ]
    source_errors = []
    for identifier, row in sa_sources.items():
        if any(row.get(field) in (None, "", []) for field in required_source_fields):
            source_errors.append(identifier)
        if row.get("author") is None and row.get("organization") is None:
            source_errors.append(identifier)
        if row.get("publication_date") is None and "Publication date unavailable" not in (row.get("notes") or ""):
            source_errors.append(identifier)
    tier_counts = Counter(row["quality_tier"] for row in sa_sources.values())
    result.check(
        "atomic_source_registry",
        len(sa_sources) == 34 and not source_errors and tier_counts == Counter({"A": 30, "B": 4}),
        f"Saudi-specific sources={len(sa_sources)}, tiers={dict(tier_counts)}, metadata errors={sorted(set(source_errors))}",
    )
    trace_errors = [
        row["id"]
        for row in claims
        if row.get("source_id") not in sources
        or not row.get("source_locator")
        or row.get("verification_status") not in {"verified", "source_verified", "disputed"}
    ]
    published = [row for row in claims if row.get("published")]
    ab_claims = [row for row in published if sources.get(row.get("source_id"), {}).get("quality_tier") in {"A", "B"}]
    ab_ratio = len(ab_claims) * 100 / len(published) if published else 0.0
    result.check("claim_traceability", not trace_errors, f"claims={len(claims)}, traceability errors={len(trace_errors)}")
    result.check("ab_source_threshold", ab_ratio >= 95.0, f"A/B published claims={len(ab_claims)}/{len(published)} ({ab_ratio:.2f}%)")
    sensitive = [row for row in published if row.get("sensitivity") == "sensitive"]
    sensitive_errors = [
        row["id"]
        for row in sensitive
        if row.get("status") != "disputed"
        and (not row.get("second_source_id") or row.get("second_source_id") == row.get("source_id"))
    ]
    result.check(
        "sensitive_claim_rule",
        not sensitive_errors,
        f"sensitive claims={len(sensitive)}, compliant={len(sensitive)-len(sensitive_errors)}; zero-case policy is vacuously satisfied",
    )

    # Manifest, legal hierarchy and all nine denominator declarations.
    hierarchy = manifest.get("hierarchy", [])
    hierarchy_types = [row.get("entity_type") for row in hierarchy]
    expected_hierarchy = ["country", "sa_region", "sa_governorate", "sa_nahiya", "sa_markaz"]
    layers = {row["layer"]: row for row in manifest.get("pilot_layers", [])}
    expected_layers = {
        "sa_region",
        "sa_governorate_published_rows",
        "sa_markaz_published_occurrences",
        "sa_governorate_current_national",
        "sa_markaz_current_national",
        "sa_nahiya_current_national",
        "populated_places",
        "neighborhoods",
        "unesco_world_heritage_properties",
    }
    manifest_ok = (
        manifest.get("country", {}).get("iso2") == "SA"
        and manifest.get("snapshot", {}).get("as_of") == SNAPSHOT_DATE
        and manifest.get("status") == "pilot_migrated"
        and hierarchy_types == expected_hierarchy
        and set(layers) == expected_layers
        and "ناحية" in hierarchy[3].get("local_names", [])
        and "مركز" in hierarchy[4].get("local_names", [])
        and "SRC-SA-LAW-OF-PROVINCES-1992" in manifest.get("official_authority", {}).get("source_ids", [])
        and all(row.get("source_ids") and row.get("snapshot_date") == SNAPSHOT_DATE and row.get("license") for row in layers.values())
    )
    result.check(
        "country_manifest",
        manifest_ok,
        f"hierarchy={hierarchy_types}, declared layers={sorted(layers)}, snapshot={manifest.get('snapshot', {}).get('as_of')}",
    )
    den_by_id = {row["id"]: row for row in denominators}
    cov_by_id = {row["id"]: row for row in coverage}
    closure_errors = []
    unknown_errors = []
    for layer_name, declaration in layers.items():
        den = den_by_id.get(declaration.get("denominator_id"), {})
        cov = cov_by_id.get(declaration.get("coverage_record_id"), {})
        if den.get("value") is None:
            if (
                declaration.get("denominator") is not None
                or cov.get("coverage_percentage") is not None
                or cov.get("complete") is not False
                or not den.get("missing_reason")
                or not cov.get("missing_reason")
            ):
                unknown_errors.append(layer_name)
        elif (
            declaration.get("denominator") != den.get("value")
            or cov.get("matched", -1) + cov.get("excluded", -1) != den.get("value")
            or cov.get("unmatched") != 0
            or cov.get("missing") != 0
            or cov.get("complete") is not True
            or cov.get("coverage_percentage") != 100.0
        ):
            closure_errors.append(layer_name)
    result.check(
        "denominator_accounting",
        len(denominators) == len(coverage) == 9 and not closure_errors and not unknown_errors,
        f"records=9+9, closed failures={closure_errors}, unavailable-scope failures={unknown_errors}",
    )
    expected_equations = {
        "sa_region": (13, 0, 13),
        "sa_governorate_published_rows": (141, 0, 141),
        "sa_markaz_published_occurrences": (1521, 2, 1523),
        "unesco_world_heritage_properties": (8, 0, 8),
    }
    actual_equations = {
        layer: (
            cov_by_id[layers[layer]["coverage_record_id"]]["matched"],
            cov_by_id[layers[layer]["coverage_record_id"]]["excluded"],
            den_by_id[layers[layer]["denominator_id"]]["value"],
        )
        for layer in expected_equations
    }
    result.check(
        "declared_scope_closure",
        actual_equations == expected_equations,
        f"matched/excluded/denominator={actual_equations}",
    )

    # Explicit conflict/anomaly accounting and no fabricated nawahi.
    anomaly_records = anomalies.get("records", [])
    anomaly_names = {row.get("value") for row in anomaly_records}
    no_critical = anomalies.get("unresolved_p0") == 0 and anomalies.get("unresolved_p1") == 0
    conflict_text = " ".join(row.get("missing_reason") or "" for row in denominators)
    result.check(
        "conflicts_and_exclusions",
        len(anomaly_records) == 2
        and anomaly_names == {"الرقعي", "الربواء"}
        and no_critical
        and all(token in conflict_text for token in ["150", "151", "1,377", "1,528", "1,523"]),
        f"duplicate exclusions={sorted(anomaly_names)}, unresolved P0/P1={anomalies.get('unresolved_p0')}/{anomalies.get('unresolved_p1')}",
    )
    result.check(
        "legal_nahiya_without_fabrication",
        counts.get("sa_nahiya", 0) == 0
        and layers.get("sa_nahiya_current_national", {}).get("scope_status") == "unavailable",
        f"materialized nawahi={counts.get('sa_nahiya', 0)}, manifest status={layers.get('sa_nahiya_current_national', {}).get('scope_status')}",
    )

    # Bounded places, history, culture and dialect chain.
    bounded_place_types = {"city", "historical_place"}
    seat_id_count = len(seat_ids)
    bounded_places = [row for row in entities if row["entity_type"] in bounded_place_types and row["id"] not in seat_ids]
    sites = [row for row in entities if row["entity_type"] in {"archaeological_site", "cultural_site", "natural_site"}]
    population_claims = [row for row in claims if row.get("predicate") == "population"]
    geonames_refs = [
        row["id"]
        for row in entities + aliases + relationships + claims
        if row.get("canonical_source_id", "").startswith("SRC-GEONAMES") or row.get("source_id", "").startswith("SRC-GEONAMES")
    ]
    result.check(
        "bounded_places_and_sites",
        len(bounded_places) == 4 and len(sites) == 8 and not geonames_refs and not population_claims,
        f"bounded places={len(bounded_places)}, regional seats={seat_id_count}, sites={len(sites)}, GeoNames refs={len(geonames_refs)}, population claims={len(population_claims)}",
    )
    historical = [row for row in bounded_places if row["entity_type"] == "historical_place"]
    current = [row for row in bounded_places if row["entity_type"] == "city"]
    result.check(
        "temporal_separation",
        len(historical) == 1 and historical[0].get("status") == "historical" and len(current) == 3 and all(row.get("status") == "current" for row in current),
        f"historical={[(row['canonical_name'], row.get('status')) for row in historical]}, current cities={len(current)}",
    )
    contexts = {context for row in cultural.get("properties", []) for context in row.get("contexts", [])}
    required_contexts = {"coastal", "mountain", "desert", "oasis", "major-city", "historical-city", "rural"}
    cultural_predicates = Counter(row["predicate"] for row in claims)
    culture_ok = (
        required_contexts <= contexts
        and cultural_predicates["official_regional_dish"] == 13
        and cultural_predicates["official_national_dish"] == 1
        and cultural_predicates["official_national_dessert"] == 1
        and cultural_predicates["intangible_cultural_practice"] == 4
        and cultural_predicates["regional_clothing_evidence_scope"] == 1
    )
    result.check(
        "representative_culture",
        culture_ok,
        f"required contexts covered={sorted(required_contexts & contexts)}; selected claim counts={{dish: {cultural_predicates['official_regional_dish']}, ICH: {cultural_predicates['intangible_cultural_practice']}, clothing-scope: {cultural_predicates['regional_clothing_evidence_scope']}}}",
    )
    national_claims = [row for row in claims if row["predicate"] in {"official_national_dish", "official_national_dessert"}]
    local_leaks = [row["id"] for row in national_claims if row["subject_id"] != COUNTRY or row.get("classification") != "national"]
    unsupported_language = [row["id"] for row in entities if row["entity_type"] == "language" and row["id"] != "ENT-SA-LANGUAGE-ARABIC"]
    forbidden_words = re.compile(r"\b(unique|only|oldest|largest|first)\b|(?:الوحيد|الأقدم|الأكبر|الأول)", re.IGNORECASE)
    unsupported_superlatives = [
        row["id"] for row in claims if forbidden_words.search(json.dumps(row.get("value"), ensure_ascii=False))
    ]
    result.check(
        "attribution_scope",
        not local_leaks and not unsupported_language and not unsupported_superlatives,
        f"national-to-local leaks={len(local_leaks)}, unsupported other languages={len(unsupported_language)}, unsupported superlatives={len(unsupported_superlatives)}",
    )

    varieties = [row for row in entities if row["entity_type"] == "language_variety"]
    lexical_forms = [row for row in entities if row["entity_type"] == "lexical_form"]
    rels_by_child: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in relationships:
        rels_by_child[row["child_id"]].append(row)
    lexical_errors = []
    for entity in lexical_forms:
        rel_types = {row["relationship_type"] for row in rels_by_child[entity["id"]]}
        attestations = [row for row in claims if row["subject_id"] == entity["id"] and row["predicate"] == "lexical_attestation"]
        if len(attestations) != 1 or not {"form_of", "attested_in"} <= rel_types:
            lexical_errors.append(entity["id"])
            continue
        context = attestations[0].get("lexical_context") or {}
        if (
            context.get("form") != entity.get("canonical_name")
            or context.get("place_id") not in ids
            or not context.get("meaning")
            or not context.get("register")
            or not context.get("study_date")
        ):
            lexical_errors.append(entity["id"])
    dialect_count_claims = [row["id"] for row in claims if "dialect_count" in row.get("predicate", "")]
    variety_parent_errors = [
        row["id"]
        for row in varieties
        if {rel["relationship_type"] for rel in rels_by_child[row["id"]]} < {"variety_of", "associated_with"}
    ]
    result.check(
        "dialect_evidence_chain",
        len(varieties) == 2 and len(lexical_forms) == 4 and not lexical_errors and not dialect_count_claims and not variety_parent_errors,
        f"varieties={len(varieties)}, forms={len(lexical_forms)}, chain errors={lexical_errors}, count claims={len(dialect_count_claims)}",
    )

    # Independent review must be passing, fresh and mutation-complete.
    review_path = ROOT / "reports/saudi_independent_review.json"
    review = load(review_path) if review_path.is_file() else {}
    rates = review.get("sample_rates", {})
    fresh_fingerprint = review_input_fingerprint()
    review_ok = (
        review.get("passed") is True
        and rates
        and all(rate >= 0.10 for rate in rates.values())
        and review.get("input_fingerprint_sha256") == fresh_fingerprint
        and not review.get("errors")
    )
    result.check(
        "independent_review",
        bool(review_ok),
        f"passed={review.get('passed')}, minimum rate={min(rates.values()) if rates else None}, fresh={review.get('input_fingerprint_sha256') == fresh_fingerprint if review else False}",
    )
    negative = review.get("negative_test_outcomes", {})
    result.check(
        "negative_tests",
        set(negative) == EXPECTED_NEGATIVE_IDS and set(negative.values()) == {"pass"},
        f"outcomes={negative}",
    )
    result.check(
        "finding_closure",
        review.get("p0_findings") == 0
        and review.get("p1_findings") == 0
        and anomalies.get("unresolved_p0") == 0
        and anomalies.get("unresolved_p1") == 0,
        f"review P0/P1={review.get('p0_findings')}/{review.get('p1_findings')}; anomaly P0/P1={anomalies.get('unresolved_p0')}/{anomalies.get('unresolved_p1')}",
    )

    # Quantitative complexity metrics (records, not file count).
    repeated_claim_values = sum(
        count - 1
        for count in Counter(json.dumps(row["value"], ensure_ascii=False, sort_keys=True) for row in claims).values()
        if count > 1
    )
    duplicate_claim_keys = len(claims) - len(
        {
            (
                row["subject_id"],
                row["predicate"],
                json.dumps(row["value"], ensure_ascii=False, sort_keys=True),
                row["source_id"],
                row["source_locator"],
            )
            for row in claims
        }
    )
    all_source_refs = (
        {row.get("canonical_source_id") for row in entities}
        | {row.get("source_id") for row in aliases + relationships + claims + denominators + coverage}
    ) - {None}
    primary_records = len(entities) + len(aliases) + len(relationships) + len(claims)
    report = {
        "schema_version": "1.0.0",
        "country_code": "SA",
        "snapshot_date": SNAPSHOT_DATE,
        "status": "pass" if not result.errors else "fail",
        "checks": result.checks,
        "errors": result.errors,
        "metrics": {
            "entities": len(entities),
            "aliases": len(aliases),
            "relationships": len(relationships),
            "claims": len(claims),
            "primary_records": primary_records,
            "saudi_specific_atomic_sources": len(sa_sources),
            "unique_sources_used_including_shared_iso": len(all_source_refs),
            "ab_claim_ratio": round(ab_ratio, 4),
            "sensitive_claims": len(sensitive),
            "sensitive_noncompliant": len(sensitive_errors),
            "duplicate_claims": duplicate_claim_keys,
            "repeated_claim_value_occurrences": repeated_claim_values,
            "text_duplication_rate": round(repeated_claim_values * 100 / len(claims), 4) if claims else 0.0,
            "records_per_entity": round(primary_records / len(entities), 4) if entities else None,
            "records_per_unique_source": round(primary_records / len(all_source_refs), 4) if all_source_refs else None,
            "p0": 0 if not result.errors else len(result.errors),
            "critical_p1": 0,
        },
    }
    write_json(REPORT, report)
    for name, row in result.checks.items():
        print(f"[{'PASS' if row['status'] == 'pass' else 'FAIL'}] {name}: {row['detail']}")
    if result.errors:
        print(f"Saudi validation failed with {len(result.errors)} error(s):", file=sys.stderr)
        for error in result.errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Saudi validation passed ({len(result.checks)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
