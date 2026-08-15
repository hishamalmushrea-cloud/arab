#!/usr/bin/env python3
"""Jordan-specific semantic and acceptance validator."""
from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from model import ROOT, read_jsonl, write_json
from review_jordan import input_fingerprint

REPORT = ROOT / "reports/jordan_validation.json"
COUNTRY = "ENT-JO-COUNTRY"
SNAPSHOT_DATE = "2026-08-15"


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


def main() -> int:
    result = Validation()
    manifest = load(ROOT / "manifests/JO.yml")
    hierarchy = load(ROOT / "data/imports/jordan/hierarchy_2024.json")
    heritage = load(ROOT / "data/imports/jordan/world_heritage_2026.json")
    cultural = load(ROOT / "data/imports/jordan/cultural_content_2026.json")
    resolution = load(ROOT / "data/imports/jordan/entity_resolution_2026.json")
    checksum_manifest = load(ROOT / "data/imports/jordan/snapshot_manifest.json")

    all_entities = read_jsonl(ROOT / "data/entities/entities.jsonl")
    entities = [row for row in all_entities if row.get("country_code") == "JO"]
    ids = {row["id"] for row in entities}
    entity_by_id = {row["id"]: row for row in entities}
    aliases = [row for row in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if row.get("entity_id") in ids]
    relationships = [row for row in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if row.get("child_id") in ids]
    claims = [row for row in read_jsonl(ROOT / "data/claims/claims.jsonl") if row.get("subject_id") in ids]
    denominators = [row for row in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if row.get("country_code") == "JO"]
    coverage = [row for row in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if row.get("country_code") == "JO"]
    sources = {load(path)["id"]: load(path) for path in sorted((ROOT / "data/sources").glob("*.json"))}
    jo_source_paths = sorted((ROOT / "data/sources").glob("*JO*.json"))
    jo_sources = {load(path)["id"]: load(path) for path in jo_source_paths}

    # Checksum-bound inputs and country-specific build.
    checksum_errors = []
    for row in checksum_manifest["files"]:
        path = ROOT / row["path"]
        payload = path.read_bytes() if path.is_file() else b""
        if len(payload) != row["bytes"] or hashlib.sha256(payload).hexdigest() != row["sha256"]:
            checksum_errors.append(row["path"])
    result.check("checksum_bound_inputs", len(checksum_manifest["files"]) == 25 and not checksum_errors,
                 f"files={len(checksum_manifest['files'])}, mismatches={checksum_errors}")
    jordan_files = [ROOT / "scripts/import_jordan_phase3.py", ROOT / "scripts/review_jordan.py", ROOT / "data/imports/jordan/hierarchy_2024.json"]
    no_tunisia_copy = all("import_tunisia" not in path.read_text(encoding="utf-8").casefold() and "data/imports/tunisia" not in path.read_text(encoding="utf-8").casefold() for path in jordan_files)
    no_tn_refs = all("-TN-" not in json.dumps(row, ensure_ascii=False) and not str(row.get("entity_type", "")).startswith("tn_") for row in entities + aliases + relationships + claims)
    result.check("country_specific_method", no_tunisia_copy and no_tn_refs,
                 "Jordan importer/reviewer/fixture contain no Tunisia assumptions and Jordan records contain no TN references")

    counts = Counter(row["entity_type"] for row in entities)
    expected_counts = {"country": 1, "jo_governorate": 12, "jo_liwa": 55, "jo_qada": 36,
                       "archaeological_site": 4, "cultural_site": 2, "natural_site": 2, "city": 1, "historical_place": 3}
    result.check("entity_counts", dict(counts) == expected_counts, f"actual={dict(sorted(counts.items()))}")
    result.check("record_family_counts", (len(entities), len(aliases), len(relationships), len(claims)) == (116, 116, 119, 135),
                 f"entities/aliases/relationships/claims={len(entities)}/{len(aliases)}/{len(relationships)}/{len(claims)}")

    # Exact administrative closure and topology.
    actual_admin = [row for row in entities if row["entity_type"] in {"jo_governorate", "jo_liwa", "jo_qada"}]
    fixture_counts = {
        "jo_governorate": len(hierarchy["governorates"]),
        "jo_liwa": sum(len(g["liwa"]) for g in hierarchy["governorates"]),
        "jo_qada": sum(len(l["qada"]) for g in hierarchy["governorates"] for l in g["liwa"]),
    }
    expected_by_governorate = {
        "amman": (9, 4), "irbid": (10, 0), "balqa": (5, 3), "karak": (8, 2),
        "maan": (4, 4), "zarqa": (3, 3), "mafraq": (5, 9), "tafilah": (3, 0),
        "madaba": (2, 5), "jerash": (2, 2), "ajloun": (2, 2), "aqaba": (2, 2),
    }
    actual_by_governorate = {
        g["key"]: (len(g["liwa"]), sum(len(liwa["qada"]) for liwa in g["liwa"]))
        for g in hierarchy["governorates"]
    }
    result.check("legal_derivation", hierarchy["derivation"] == {
        "pre_amendment": {"governorates": 12, "liwa": 51, "qada": 38},
        "amendment_effect": {"liwa": 4, "qada": -2},
        "current": {"governorates": 12, "liwa": 55, "qada": 36},
    } and fixture_counts == {"jo_governorate": 12, "jo_liwa": 55, "jo_qada": 36}
    and actual_by_governorate == expected_by_governorate,
                 f"fixture_counts={fixture_counts}; by_governorate={actual_by_governorate}; 51/38 +4/-2 = 55/36")
    admin_rels = [row for row in relationships if row["relationship_type"] == "administrative_parent"]
    parents = defaultdict(list)
    for row in admin_rels:
        parents[row["child_id"]].append(row["parent_id"])
    allowed = {"jo_governorate": {"country"}, "jo_liwa": {"jo_governorate"}, "jo_qada": {"jo_liwa"}}
    topology_errors = []
    for row in actual_admin:
        parent_ids = parents[row["id"]]
        if len(parent_ids) != 1 or entity_by_id.get(parent_ids[0], {}).get("entity_type") not in allowed[row["entity_type"]]:
            topology_errors.append(row["id"])
    result.check("administrative_topology", len(admin_rels) == 103 and not topology_errors,
                 f"parent_relationships={len(admin_rels)}, errors={len(topology_errors)}")
    all_linked = all(any(rel["child_id"] == row["id"] for rel in relationships) for row in entities if row["id"] != COUNTRY)
    result.check("all_entities_parented", all_linked, "every non-country administrative/site/place entity has an explicit relationship")

    # IDs, orphans, cycles, aliases, and country integrity.
    global_ids = []
    for path in ["data/entities/entities.jsonl", "data/aliases/aliases.jsonl", "data/relationships/relationships.jsonl", "data/claims/claims.jsonl", "data/snapshots/snapshots.jsonl", "data/coverage/denominators.jsonl", "data/coverage/coverage.jsonl"]:
        global_ids.extend(row["id"] for row in read_jsonl(ROOT / path))
    duplicate_ids = [identifier for identifier, count in Counter(global_ids).items() if count > 1]
    orphan_rels = [row["id"] for row in relationships if row["child_id"] not in ids or row["parent_id"] not in ids]
    country_mismatch = [row["id"] for row in relationships if entity_by_id[row["child_id"]]["country_code"] != entity_by_id[row["parent_id"]]["country_code"]]
    graph = defaultdict(list)
    for row in admin_rels:
        graph[row["child_id"]].append(row["parent_id"])
    cycles = []
    for start in graph:
        seen = set()
        node = start
        while node in graph and graph[node]:
            if node in seen:
                cycles.append(start); break
            seen.add(node); node = graph[node][0]
    result.check("identity_integrity", not duplicate_ids and not orphan_rels and not country_mismatch and not cycles,
                 f"duplicate_ids={len(duplicate_ids)}, orphans={len(orphan_rels)}, country_mismatch={len(country_mismatch)}, cycles={len(cycles)}")
    alias_keys = [(row["entity_id"], row["language"], row["kind"], row["name"].strip().casefold()) for row in aliases]
    result.check("aliases_unique", len(alias_keys) == len(set(alias_keys)), f"aliases={len(alias_keys)}, duplicates={len(alias_keys)-len(set(alias_keys))}")

    # Sources and claim quality.
    required_source_fields = ["title", "author", "organization", "publisher", "publication_date", "retrieved_at", "url", "locator", "source_type", "quality_tier", "license", "language", "country_codes"]
    source_errors = []
    for identifier, row in jo_sources.items():
        always = [field for field in required_source_fields if field not in {"author", "publication_date"}]
        if any(field not in row or row[field] in ("", []) for field in always) or (row.get("author") is None and row.get("organization") is None):
            source_errors.append(identifier)
        if row.get("publication_date") is None and "Publication" not in (row.get("notes") or ""):
            source_errors.append(identifier)
    result.check("atomic_source_registry", len(jo_sources) == 21 and not source_errors,
                 f"atomic Jordan records={len(jo_sources)}, metadata_errors={sorted(set(source_errors))}")
    claim_ref_errors = [row["id"] for row in claims if row.get("source_id") not in sources or not row.get("source_locator") or row.get("verification_status") not in {"verified", "disputed"}]
    published = [row for row in claims if row.get("published")]
    ab_claims = [row for row in published if sources[row["source_id"]]["quality_tier"] in {"A", "B"}]
    ratio = len(ab_claims) * 100 / len(published) if published else 0.0
    result.check("claims_supported", not claim_ref_errors, f"claims={len(claims)}, unsupported={len(claim_ref_errors)}")
    result.check("ab_source_threshold", ratio >= 95, f"A/B published claims={len(ab_claims)}/{len(published)} ({ratio:.2f}%)")
    sensitive = [row for row in published if row.get("sensitivity") == "sensitive"]
    sensitive_errors = [row["id"] for row in sensitive if row.get("status") != "disputed" and (not row.get("second_source_id") or row.get("second_source_id") == row.get("source_id"))]
    result.check("sensitive_claim_rule", not sensitive_errors, f"sensitive={len(sensitive)}, noncompliant={len(sensitive_errors)}")

    # Manifest declarations and denominator equations.
    layers = {row["layer"]: row for row in manifest["pilot_layers"]}
    expected_denoms = {"jo_governorate": 12, "jo_liwa": 55, "jo_qada": 36, "world_heritage_property": 8, "bounded_populated_place": 4}
    manifest_ok = manifest["country"]["iso2"] == "JO" and manifest["snapshot"]["as_of"] == SNAPSHOT_DATE and manifest["status"] == "pilot_migrated" and set(layers) == set(expected_denoms)
    for layer, value in expected_denoms.items():
        row = layers.get(layer, {})
        manifest_ok = manifest_ok and row.get("denominator") == value and row.get("source_ids") and row.get("license") and row.get("authority_name") and row.get("local_names") and row.get("scope_status") in {"closed", "bounded"}
    result.check("country_manifest", bool(manifest_ok), f"declared_layers={sorted(layers)}, dated={manifest.get('snapshot',{}).get('as_of')}")
    den_by_id = {row["id"]: row for row in denominators}
    cov_by_id = {row["id"]: row for row in coverage}
    closure_errors = []
    for layer, value in expected_denoms.items():
        declaration = layers[layer]
        den = den_by_id.get(declaration["denominator_id"], {})
        cov = cov_by_id.get(declaration["coverage_record_id"], {})
        if den.get("value") != value or den.get("as_of") != SNAPSHOT_DATE or cov.get("matched", -1) + cov.get("excluded", -1) != value or cov.get("unmatched") != 0 or cov.get("missing") != 0 or not cov.get("complete") or cov.get("snapshot_date") != SNAPSHOT_DATE:
            closure_errors.append(layer)
    result.check("denominator_closure", not closure_errors, f"five declared layers; failed={closure_errors}; matched + excluded = denominator")

    # Bounded places, coordinates, resolution, culture, and temporality.
    pilot_places = [row for row in entities if row["entity_type"] in {"city", "historical_place"}]
    site_types = {"archaeological_site", "cultural_site", "natural_site"}
    sites = [row for row in entities if row["entity_type"] in site_types]
    geonames_refs = [row["id"] for row in entities + aliases + relationships + claims if row.get("canonical_source_id") == "SRC-GEONAMES-JO-CROSSCHECK-2026" or row.get("source_id") == "SRC-GEONAMES-JO-CROSSCHECK-2026"]
    result.check("bounded_places", len(pilot_places) == 4 and len(sites) == 8 and not geonames_refs,
                 f"places={len(pilot_places)}/4, sites={len(sites)}/8, authoritative GeoNames references={len(geonames_refs)}")
    heritage_rows = heritage["properties"] + heritage["bounded_populated_places"]["places"]
    coordinate_errors = []
    for source_row in heritage_rows:
        candidates = [row for row in entities if row.get("canonical_name") == source_row["name_ar"] and row.get("entity_type") == source_row["entity_type"]]
        if len(candidates) != 1:
            coordinate_errors.append(source_row["key"]); continue
        coords = candidates[0].get("coordinates") or {}
        if coords.get("latitude") != source_row["latitude"] or coords.get("longitude") != source_row["longitude"] or coords.get("source_id") != source_row["source_id"]:
            coordinate_errors.append(source_row["key"])
    historical_errors = [row["id"] for row in pilot_places if row["entity_type"] == "historical_place" and row["status"] != "historical"]
    result.check("coordinates_and_temporality", not coordinate_errors and not historical_errors,
                 f"coordinate_mismatches={coordinate_errors}, historical_status_errors={historical_errors}")
    result.check("entity_resolution_before_places", resolution["method"].startswith("Before insertion") and resolution["existing_jordan_records_before_import"] == [COUNTRY] and len(resolution["candidate_decisions"]) == 12,
                 f"decisions={len(resolution['candidate_decisions'])}, pre-existing={resolution['existing_jordan_records_before_import']}")

    ich = [row for row in claims if row.get("source_id", "").startswith("SRC-UNESCO-ICH-JO-")]
    national = [row for row in ich if row["predicate"] in {"food_practice", "performance_practice"}]
    bedu = [row for row in ich if row["predicate"] == "cultural_space"]
    petra_rum_names = {"البتراء", "منطقة وادي رم المحمية"}
    bedu_names = {entity_by_id[row["subject_id"]]["canonical_name"] for row in bedu}
    culture_ok = len(ich) == 4 and len(national) == 2 and all(row["subject_id"] == COUNTRY for row in national) and len(bedu) == 2 and bedu_names == petra_rum_names
    result.check("cultural_scope", culture_ok, f"national={len(national)} at country; Bedu subjects={sorted(bedu_names)}")
    domain = load(ROOT / "data/cultural/jordan_domain_status.json")["domains"]
    dialect_claims = [row for row in claims if row["predicate"] in {"dialect_form", "lexical_form", "pronunciation"}]
    domain_ok = domain["dialect"]["status"] == "not_documented" and domain["dress"]["status"] == "not_found" and domain["people"]["status"] == "N/A" and not dialect_claims
    result.check("missing_domains_not_forced", domain_ok, f"dialect={domain['dialect']['status']}, dress={domain['dress']['status']}, people={domain['people']['status']}, dialect_claims={len(dialect_claims)}")

    # Independent review freshness and finding closure.
    review = load(ROOT / "reports/jordan_independent_review.json") if (ROOT / "reports/jordan_independent_review.json").is_file() else {}
    rates = review.get("sample_rates", {})
    review_ok = review.get("passed") and rates and all(rate >= 0.10 for rate in rates.values()) and review.get("input_fingerprint_sha256") == input_fingerprint()
    result.check("independent_review", bool(review_ok), f"passed={review.get('passed')}, minimum_rate={min(rates.values()) if rates else None}, fresh={review.get('input_fingerprint_sha256') == input_fingerprint() if review else False}")
    negative = review.get("negative_test_outcomes", {})
    result.check("negative_tests", len(negative) == 7 and set(negative.values()) == {"pass"}, f"outcomes={negative}")
    result.check("finding_closure", review.get("p0_findings") == 0 and review.get("p1_findings") == 0,
                 f"P0={review.get('p0_findings')}, critical P1={review.get('p1_findings')}")

    report = {
        "schema_version": "1.0.0", "country_code": "JO", "snapshot_date": SNAPSHOT_DATE,
        "status": "pass" if not result.errors else "fail", "checks": result.checks, "errors": result.errors,
        "metrics": {"entities": len(entities), "aliases": len(aliases), "relationships": len(relationships), "claims": len(claims),
                    "ab_claim_ratio": round(ratio, 2), "sensitive_claims": len(sensitive), "atomic_sources": len(jo_sources), "p0": 0 if not result.errors else len(result.errors), "critical_p1": 0},
    }
    write_json(REPORT, report)
    for name, row in result.checks.items():
        print(f"[{'PASS' if row['status'] == 'pass' else 'FAIL'}] {name}: {row['detail']}")
    if result.errors:
        print(f"Jordan validation failed with {len(result.errors)} error(s):", file=sys.stderr)
        for error in result.errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Jordan validation passed ({len(result.checks)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
