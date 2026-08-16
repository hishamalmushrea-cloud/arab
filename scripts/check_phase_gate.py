#!/usr/bin/env python3
"""Executable baseline and Tunisia, Jordan, Saudi, and UAE country-cycle gates."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from migrate_schema_2 import semantic_hash
from model import COUNTRIES, ROOT, read_jsonl, write_json


class Gate:
    def __init__(self, phase: str):
        self.phase = phase
        self.errors: list[str] = []
        self.checks: dict[str, Any] = {}

    def require(self, condition: bool, name: str, detail: str):
        self.checks[name] = {"status": "pass" if condition else "fail", "detail": detail}
        if not condition: self.errors.append(f"{name}: {detail}")

    def command(self, name: str, command: list[str]):
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        display = ["python3", *command[1:]] if command and command[0] == sys.executable else command
        self.checks[name] = {
            "status": "pass" if result.returncode == 0 else "fail",
            "command": " ".join(display),
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
        if result.returncode:
            self.errors.append(f"{name}: command failed with exit {result.returncode}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def phase2_import_hashes() -> tuple[dict[str, str], str]:
    """Hash importer-managed files and a canonical non-Tunisia projection."""
    managed = [
        "data/entities/entities.jsonl", "data/aliases/aliases.jsonl",
        "data/claims/claims.jsonl", "data/relationships/relationships.jsonl",
        "data/coverage/denominators.jsonl", "data/coverage/coverage.jsonl",
        "data/snapshots/snapshots.jsonl", "manifests/TN.yml",
        "data/cultural/tunisia_domain_status.json",
    ]
    file_hashes = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in managed}
    entities = read_jsonl(ROOT / "data/entities/entities.jsonl")
    tn_ids = {row["id"] for row in entities if row["country_code"] == "TN"}
    projection = {
        "entities": [row for row in entities if row["id"] not in tn_ids],
        "aliases": [row for row in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if row["entity_id"] not in tn_ids],
        "claims": [row for row in read_jsonl(ROOT / "data/claims/claims.jsonl") if row["subject_id"] not in tn_ids],
        "relationships": [row for row in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if row["child_id"] not in tn_ids and row["parent_id"] not in tn_ids],
        "denominators": [row for row in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if row["country_code"] != "TN"],
        "coverage": [row for row in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if row["country_code"] != "TN"],
        "snapshots": [row for row in read_jsonl(ROOT / "data/snapshots/snapshots.jsonl") if row.get("country_code") != "TN"],
    }
    encoded = json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return file_hashes, hashlib.sha256(encoded).hexdigest()


def phase0(gate: Gate) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    legacy_readme = (ROOT / "قاعدة_بيانات_الأماكن/README.md").read_text(encoding="utf-8")
    gate.require("غير مكتملة" in readme and "جميع المدن" in readme and "100%" in readme, "completion_claims", "README declares incomplete local coverage and constrains 100%")
    gate.require("ليست المصدر السلطوي" in legacy_readme and "اكتمال المدن" in legacy_readme, "legacy_authority", "legacy CSV README disclaims authority and completeness")

    required_schemas = ["entity", "alias", "relationship", "source", "claim", "snapshot", "denominator", "coverage"]
    missing = [name for name in required_schemas if not (ROOT / f"schema/{name}.schema.json").is_file()]
    gate.require(not missing and (ROOT / "schema/schema_v2.md").is_file() and (ROOT / "schema/entity_types.md").is_file(), "schema_contract", f"required schemas present; missing={missing}")

    manifests = sorted((ROOT / "manifests").glob("*.yml"))
    manifest_codes = {path.stem for path in manifests}
    gate.require(len(manifests) == 22 and manifest_codes == set(COUNTRIES), "all_manifests", f"manifests={len(manifests)}, ISO set matches={manifest_codes == set(COUNTRIES)}")

    sources = list((ROOT / "data/sources").glob("*.json"))
    gate.require(bool(sources), "atomic_sources", f"atomic source files={len(sources)}")
    country_entities = [row for row in read_jsonl(ROOT / "data/entities/entities.jsonl") if row.get("entity_type") == "country"]
    gate.require(len(country_entities) == 22 and all(row.get("canonical_source_id") for row in country_entities), "country_roots", f"source-backed country roots={len(country_entities)}")

    repairs = read_jsonl(ROOT / "data/quarantine/legacy_repairs.jsonl")
    actions = Counter(row.get("action") for row in repairs)
    links = read_jsonl(ROOT / "data/quarantine/link_repairs.jsonl")
    gate.require(actions["join_excess_csv_fields_into_notes"] == 2, "saudi_rows", f"malformed Saudi row repairs={actions['join_excess_csv_fields_into_notes']}")
    gate.require(actions["rename_duplicate_legacy_id"] == 58, "duplicate_id_repairs", f"renamed duplicate ID occurrences={actions['rename_duplicate_legacy_id']}")
    gate.require(len(links) == 25, "broken_link_repairs", f"logged link repairs={len(links)}")

    workflow = ROOT / ".github/workflows/validate.yml"
    gate.require(workflow.is_file(), "ci_workflow", ".github/workflows/validate.yml exists")
    gate.require((ROOT / "scripts/validate.py").is_file(), "validator", "dependency-free validator exists")
    gate.command("schema_migration_tests", [sys.executable, "scripts/test_schema_migration.py"])
    gate.command("malformed_json_test", [sys.executable, "scripts/test_malformed_json.py"])
    gate.command("validation", [sys.executable, "scripts/validate.py"])


def phase1(gate: Gate) -> None:
    phase0(gate)
    gate.command("generated_freshness", [sys.executable, "scripts/generate.py", "--check"])

    entities = read_jsonl(ROOT / "data/entities/entities.jsonl")
    claims = read_jsonl(ROOT / "data/claims/claims.jsonl")
    relationships = read_jsonl(ROOT / "data/relationships/relationships.jsonl")
    coverage = read_jsonl(ROOT / "data/coverage/coverage.jsonl")
    denominators = read_jsonl(ROOT / "data/coverage/denominators.jsonl")
    ledger = read_jsonl(ROOT / "data/quarantine/migration_ledger.jsonl")
    entity_by_id = {row["id"]: row for row in entities}
    den_by_id = {row["id"]: row for row in denominators}
    cov_by_scope = {(row["country_code"], row["layer"]): row for row in coverage}

    authorized_expansions = {"TN", "LY", "JO", "SA", "AE", "BH"}
    outside_pilots = [row for row in entities if row["country_code"] not in authorized_expansions and row["entity_type"] != "country"]
    gate.require(not outside_pilots, "no_mass_expansion", f"non-country expansion outside accepted pilots and Bahrain production={len(outside_pilots)}")
    gate.require(all(row.get("canonical_source_id") for row in entities), "sourced_entities", f"source-backed entities={len(entities)}")
    gate.require(all(row.get("source_id") for row in claims), "sourced_claims", f"source-backed claims={len(claims)}")

    tn_gov = [row for row in entities if row["country_code"] == "TN" and row["entity_type"] == "tn_governorate"]
    tn_del = [row for row in entities if row["country_code"] == "TN" and row["entity_type"] == "tn_delegation"]
    tn_population_claims = [row for row in claims if entity_by_id[row["subject_id"]]["country_code"] == "TN" and row["predicate"] == "population"]
    gate.require((len(tn_gov), len(tn_del), len(tn_population_claims)) == (24, 264, 24), "tunisia_core", f"governorates={len(tn_gov)}, delegations={len(tn_del)}, accepted population claims={len(tn_population_claims)}")
    tn_mun_cov = cov_by_scope.get(("TN", "municipalities"), cov_by_scope.get(("TN", "municipalities_2018"), {}))
    tn_mun_den = den_by_id.get(tn_mun_cov.get("denominator_id"), {})
    old_municipal_state = tn_mun_den.get("value") == 350 and tn_mun_cov.get("matched") == 0 and tn_mun_cov.get("missing") == 350
    phase2_municipal_state = tn_mun_den.get("value") == 350 and tn_mun_cov.get("matched") == 350 and tn_mun_cov.get("complete")
    gate.require(old_municipal_state or phase2_municipal_state, "tunisia_municipalities", f"accepted Phase 1 state or closed Phase 2 state; matched={tn_mun_cov.get('matched')}, denominator={tn_mun_den.get('value')}")
    tn_imada_den = den_by_id[cov_by_scope[("TN", "imadas")]["denominator_id"]]
    gate.require(tn_imada_den.get("value") is None or (tn_imada_den.get("value") == 2084 and cov_by_scope[("TN", "imadas")].get("complete")), "tunisia_imadas", f"accepted unavailable Phase 1 state or closed dated Phase 2 state; denominator={tn_imada_den.get('value')}")

    ly_current = [row for row in entities if row["country_code"] == "LY" and row["entity_type"] == "ly_municipality"]
    ly_historic = [row for row in entities if row["country_code"] == "LY" and row["entity_type"] == "ly_shabiya_historical"]
    ly_current_den = den_by_id[cov_by_scope[("LY", "current_municipalities")]["denominator_id"]]
    gate.require((len(ly_current), len(ly_historic)) == (93, 22), "libya_layers", f"matched current municipality subset={len(ly_current)}, historical sha‘biyat={len(ly_historic)}")
    gate.require(ly_current_den.get("value") is None and ly_current_den.get("status") == "unavailable", "libya_denominator", "current national municipality denominator remains unresolved")
    historic_ids = {row["id"] for row in ly_historic}
    current_ids = {row["id"] for row in ly_current}
    mixed = [row["id"] for row in relationships if row.get("child_id") in historic_ids and row.get("parent_id") in current_ids]
    gate.require(not mixed, "libya_temporal_separation", f"historical-to-current parent links={len(mixed)}")

    # Ledger must account for every data row, including the one-row CSV template.
    csv_rows = 0
    import csv
    for path in (ROOT / "قاعدة_بيانات_الأماكن").glob("*.csv"):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            csv_rows += sum(1 for _ in csv.DictReader(handle))
    gate.require(len(ledger) == csv_rows, "migration_ledger", f"ledger={len(ledger)}, legacy rows including template={csv_rows}")

    required_outputs = []
    for family in ["entities", "aliases", "relationships", "claims", "sources"]:
        required_outputs += [ROOT / f"generated/json/{family}.json", ROOT / f"generated/csv/{family}.csv"]
    required_outputs += [ROOT / "generated/markdown/README.md", ROOT / "generated/html/index.html"]
    required_outputs += [ROOT / f"generated/markdown/countries/{iso}.md" for iso in COUNTRIES]
    required_outputs += [ROOT / f"generated/html/countries/{iso}.html" for iso in COUNTRIES]
    missing = [str(path.relative_to(ROOT)) for path in required_outputs if not path.is_file()]
    gate.require(not missing, "four_formats", f"required generated files present; missing={missing}")


def phase2(gate: Gate) -> None:
    phase1(gate)
    before_files, before_non_tn = phase2_import_hashes()
    gate.command("tunisia_import_refresh", [sys.executable, "scripts/import_tunisia_phase2.py"])
    after_files, after_non_tn = phase2_import_hashes()
    gate.require(before_files == after_files, "tunisia_import_idempotence", f"all 9 importer-managed hashes unchanged={before_files == after_files}")
    gate.require(before_non_tn == after_non_tn, "non_tunisia_preservation", f"canonical non-Tunisia SHA-256 unchanged={after_non_tn}")
    gate.command("independent_review_refresh", [sys.executable, "scripts/review_tunisia.py"])
    gate.command("validation_after_review", [sys.executable, "scripts/validate.py"])

    entities = read_jsonl(ROOT / "data/entities/entities.jsonl")
    claims = read_jsonl(ROOT / "data/claims/claims.jsonl")
    relationships = read_jsonl(ROOT / "data/relationships/relationships.jsonl")
    coverage = read_jsonl(ROOT / "data/coverage/coverage.jsonl")
    sources = {json.loads(path.read_text(encoding="utf-8"))["id"]: json.loads(path.read_text(encoding="utf-8")) for path in (ROOT / "data/sources").glob("*.json")}
    tn_entities = [row for row in entities if row["country_code"] == "TN"]
    counts = Counter(row["entity_type"] for row in tn_entities)
    gate.require((counts["tn_governorate"], counts["tn_delegation"], counts["tn_municipality"], counts["tn_imada"]) == (24, 264, 350, 2084), "phase2_core_counts", f"24/264/350/2084 actual={counts['tn_governorate']}/{counts['tn_delegation']}/{counts['tn_municipality']}/{counts['tn_imada']}")

    cov = {(row["country_code"], row["layer"]): row for row in coverage}
    expected = {"governorates": 24, "delegations": 264, "municipalities": 350, "imadas": 2084, "world_heritage_properties": 10}
    closed = all((row := cov.get(("TN", layer))) and row.get("denominator") == denominator and row.get("matched") + row.get("excluded") == denominator and row.get("unmatched") == 0 and row.get("complete") and row.get("coverage_percentage") == 100 for layer, denominator in expected.items())
    gate.require(closed, "dated_denominators_closed", "24 governorates, 264 delegations, 350 municipalities, 2,084 imadas, and 10 UNESCO properties close with matched + excluded = denominator")

    tn_ids = {row["id"] for row in tn_entities}
    published = [row for row in claims if row["subject_id"] in tn_ids and row.get("published")]
    ab = [row for row in published if sources[row["source_id"]].get("quality_tier") in {"A", "B"}]
    ratio = len(ab) * 100 / len(published) if published else 0
    gate.require(ratio >= 95, "source_threshold", f"A/B published claims={len(ab)}/{len(published)} ({ratio:.2f}%)")
    sensitive_errors = [row["id"] for row in published if row.get("sensitivity") == "sensitive" and row.get("status") != "disputed" and (not row.get("second_source_id") or row.get("second_source_id") == row.get("source_id"))]
    gate.require(not sensitive_errors, "sensitive_claims", f"non-disputed sensitive claims without two independent sources={len(sensitive_errors)}")

    place_types = {"city", "town", "village", "settlement", "neighborhood", "historical_place"}
    place_count = sum(counts[entity_type] for entity_type in place_types)
    gate.require(place_count >= 6, "populated_place_distinction", f"sourced bounded place records={place_count}, evidenced types={sorted(place_types & set(counts))}")
    gate.require(counts["person"] >= 1 and counts["market"] >= 1 and counts["archaeological_site"] >= 1 and counts["natural_site"] >= 1, "bounded_encyclopedic_pilot", f"persons={counts['person']}, markets={counts['market']}, archaeological={counts['archaeological_site']}, natural={counts['natural_site']}")
    overlaps = [row for row in relationships if row["relationship_type"] == "boundary_intersects"]
    gate.require(len({row["child_id"] for row in overlaps}) == 350 and len({row["parent_id"] for row in overlaps}) == 264, "boundary_overlap_model", f"municipalities={len({row['child_id'] for row in overlaps})}, delegations={len({row['parent_id'] for row in overlaps})}")

    review = load_json(ROOT / "reports/tunisia_independent_review.json")
    gate.require(review.get("passed") and all(rate >= 0.10 for rate in review.get("sample_rates", {}).values()), "independent_review", f"sample={review.get('sample')}, outcomes={review.get('outcomes')}")
    gate.require((ROOT / "reports/PHASE2_TUNISIA_FINAL.md").is_file(), "final_report", "24-section Tunisia final report exists")
    gate.require(not gate.errors, "p0_clear", "all structural and Phase 2 acceptance checks are clear")


def phase3_import_hashes() -> tuple[dict[str, str], str]:
    """Hash Jordan importer outputs and a canonical non-Jordan projection."""
    managed = [
        "data/entities/entities.jsonl", "data/aliases/aliases.jsonl",
        "data/claims/claims.jsonl", "data/relationships/relationships.jsonl",
        "data/coverage/denominators.jsonl", "data/coverage/coverage.jsonl",
        "data/snapshots/snapshots.jsonl", "manifests/JO.yml",
        "data/cultural/jordan_domain_status.json",
    ]
    file_hashes = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in managed}
    entities = read_jsonl(ROOT / "data/entities/entities.jsonl")
    jo_ids = {row["id"] for row in entities if row["country_code"] == "JO"}
    projection = {
        "entities": [row for row in entities if row["id"] not in jo_ids],
        "aliases": [row for row in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if row["entity_id"] not in jo_ids],
        "claims": [row for row in read_jsonl(ROOT / "data/claims/claims.jsonl") if row["subject_id"] not in jo_ids],
        "relationships": [row for row in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if row["child_id"] not in jo_ids and row["parent_id"] not in jo_ids],
        "denominators": [row for row in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if row["country_code"] != "JO"],
        "coverage": [row for row in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if row["country_code"] != "JO"],
        "snapshots": [row for row in read_jsonl(ROOT / "data/snapshots/snapshots.jsonl") if row.get("id") != "SNP-JO-PILOT-2026-08-15"],
    }
    encoded = json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return file_hashes, hashlib.sha256(encoded).hexdigest()


def phase3(gate: Gate) -> None:
    phase2(gate)
    before_files, before_non_jo = phase3_import_hashes()
    gate.command("jordan_import_refresh", [sys.executable, "scripts/import_jordan_phase3.py"])
    after_files, after_non_jo = phase3_import_hashes()
    gate.require(before_files == after_files, "jordan_import_idempotence", f"all 9 importer-managed hashes unchanged={before_files == after_files}")
    gate.require(before_non_jo == after_non_jo, "non_jordan_preservation", f"canonical non-Jordan SHA-256 unchanged={after_non_jo}")
    gate.command("jordan_independent_review", [sys.executable, "scripts/review_jordan.py"])
    gate.command("validation_after_jordan", [sys.executable, "scripts/validate.py"])
    gate.command("jordan_semantic_validation", [sys.executable, "scripts/validate_jordan.py"])
    gate.command("generated_freshness_after_jordan", [sys.executable, "scripts/generate.py", "--check"])

    report = load_json(ROOT / "reports/jordan_validation.json")
    review = load_json(ROOT / "reports/jordan_independent_review.json")
    metrics = report.get("metrics", {})
    gate.require(report.get("status") == "pass" and metrics.get("ab_claim_ratio", 0) >= 95,
                 "jordan_acceptance_metrics", f"status={report.get('status')}, A/B ratio={metrics.get('ab_claim_ratio')}%, sources={metrics.get('atomic_sources')}")
    gate.require(metrics.get("p0") == 0 and metrics.get("critical_p1") == 0,
                 "jordan_findings_closed", f"P0={metrics.get('p0')}, critical P1={metrics.get('critical_p1')}")
    gate.require(review.get("passed") and all(rate >= 0.10 for rate in review.get("sample_rates", {}).values()),
                 "jordan_review_threshold", f"minimum sample rate={min(review.get('sample_rates', {}).values()) if review.get('sample_rates') else None}, negative tests={review.get('negative_test_outcomes')}")
    gate.require((ROOT / "reports/JORDAN_PILOT_FINAL.md").is_file(), "jordan_final_report", "Jordan final report exists; overall PASS remains contingent on separately recorded green remote checks")

    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
    gate.require(not status, "clean_worktree", f"git worktree clean={not status}")


def phase4_import_hashes() -> tuple[dict[str, str], str]:
    """Hash Saudi importer outputs and a canonical non-Saudi projection."""
    managed = [
        "data/entities/entities.jsonl", "data/aliases/aliases.jsonl",
        "data/claims/claims.jsonl", "data/relationships/relationships.jsonl",
        "data/coverage/denominators.jsonl", "data/coverage/coverage.jsonl",
        "data/snapshots/snapshots.jsonl", "manifests/SA.yml",
        "data/imports/saudi/parsed_registry.json",
        "data/imports/saudi/anomaly_ledger.json",
        "data/imports/saudi/import_summary.json",
    ]
    file_hashes = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in managed}
    entities = read_jsonl(ROOT / "data/entities/entities.jsonl")
    sa_ids = {row["id"] for row in entities if row["country_code"] == "SA"}
    projection = {
        "entities": [row for row in entities if row["id"] not in sa_ids],
        "aliases": [row for row in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if row["entity_id"] not in sa_ids],
        "claims": [row for row in read_jsonl(ROOT / "data/claims/claims.jsonl") if row["subject_id"] not in sa_ids],
        "relationships": [row for row in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if row["child_id"] not in sa_ids and row["parent_id"] not in sa_ids],
        "denominators": [row for row in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if row["country_code"] != "SA"],
        "coverage": [row for row in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if row["country_code"] != "SA"],
        "snapshots": [row for row in read_jsonl(ROOT / "data/snapshots/snapshots.jsonl") if row.get("country_code") != "SA"],
    }
    encoded = json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return file_hashes, hashlib.sha256(encoded).hexdigest()


def saudi_source_hashes() -> dict[str, str]:
    """Hash the 34 Saudi-specific atomic source records built by the source builder."""
    hashes = {}
    for path in sorted((ROOT / "data/sources").glob("*.json")):
        row = load_json(path)
        if row.get("country_codes") == ["SA"]:
            hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def phase4(gate: Gate) -> None:
    phase3(gate)

    before_sources = saudi_source_hashes()
    gate.command("saudi_source_refresh", [sys.executable, "scripts/build_saudi_sources.py"])
    after_sources = saudi_source_hashes()
    gate.require(
        len(after_sources) == 34 and before_sources == after_sources,
        "saudi_source_idempotence",
        f"Saudi atomic sources={len(after_sources)}/34, hashes unchanged={before_sources == after_sources}",
    )

    before_files, before_non_sa = phase4_import_hashes()
    gate.command("saudi_import_refresh", [sys.executable, "scripts/import_saudi_phase3.py"])
    after_files, after_non_sa = phase4_import_hashes()
    gate.require(before_files == after_files, "saudi_import_idempotence", f"all 11 importer-managed hashes unchanged={before_files == after_files}")
    gate.require(before_non_sa == after_non_sa, "non_saudi_preservation", f"canonical non-Saudi SHA-256 unchanged={after_non_sa}")

    sample_path = ROOT / "data/review/saudi_review_samples.json"
    sample_before = hashlib.sha256(sample_path.read_bytes()).hexdigest()
    gate.command("saudi_sample_refresh", [sys.executable, "scripts/build_saudi_review_samples.py"])
    sample_after = hashlib.sha256(sample_path.read_bytes()).hexdigest()
    gate.require(sample_before == sample_after, "saudi_sample_idempotence", f"fixed review sample SHA-256 unchanged={sample_before == sample_after}")

    gate.command("saudi_independent_review", [sys.executable, "scripts/review_saudi.py"])
    gate.command("validation_after_saudi", [sys.executable, "scripts/validate.py"])
    gate.command("saudi_semantic_validation", [sys.executable, "scripts/validate_saudi.py"])
    gate.command("generated_freshness_after_saudi", [sys.executable, "scripts/generate.py", "--check"])

    report = load_json(ROOT / "reports/saudi_validation.json")
    review = load_json(ROOT / "reports/saudi_independent_review.json")
    metrics = report.get("metrics", {})
    gate.require(
        report.get("status") == "pass" and metrics.get("ab_claim_ratio", 0) >= 95,
        "saudi_acceptance_metrics",
        f"status={report.get('status')}, A/B ratio={metrics.get('ab_claim_ratio')}%, unique source refs={metrics.get('unique_sources_used_including_shared_iso')}",
    )
    gate.require(
        metrics.get("p0") == 0 and metrics.get("critical_p1") == 0,
        "saudi_findings_closed",
        f"P0={metrics.get('p0')}, critical P1={metrics.get('critical_p1')}",
    )
    rates = review.get("sample_rates", {})
    gate.require(
        review.get("passed") and rates and all(rate >= 0.10 for rate in rates.values()),
        "saudi_review_threshold",
        f"minimum sample rate={min(rates.values()) if rates else None}, negative tests={review.get('negative_test_outcomes')}",
    )
    gate.require(
        (ROOT / "reports/SAUDI_PILOT_FINAL.md").is_file(),
        "saudi_final_report",
        "20-section Saudi final report exists; overall PASS also requires a separately recorded green remote run",
    )

    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
    gate.require(not status, "saudi_clean_worktree", f"git worktree clean={not status}")


def phase5_import_hashes() -> tuple[dict[str, str], str]:
    """Hash UAE importer outputs and a canonical non-UAE projection."""
    managed = [
        "data/entities/entities.jsonl", "data/aliases/aliases.jsonl",
        "data/claims/claims.jsonl", "data/relationships/relationships.jsonl",
        "data/coverage/denominators.jsonl", "data/coverage/coverage.jsonl",
        "data/snapshots/snapshots.jsonl", "manifests/AE.yml",
    ]
    file_hashes = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in managed}
    entities = read_jsonl(ROOT / "data/entities/entities.jsonl")
    ae_ids = {row["id"] for row in entities if row["country_code"] == "AE"}
    projection = {
        "entities": [row for row in entities if row["id"] not in ae_ids],
        "aliases": [row for row in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if row["entity_id"] not in ae_ids],
        "claims": [row for row in read_jsonl(ROOT / "data/claims/claims.jsonl") if row["subject_id"] not in ae_ids],
        "relationships": [row for row in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if row["child_id"] not in ae_ids and row["parent_id"] not in ae_ids],
        "denominators": [row for row in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if row["country_code"] != "AE"],
        "coverage": [row for row in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if row["country_code"] != "AE"],
        "snapshots": [row for row in read_jsonl(ROOT / "data/snapshots/snapshots.jsonl") if row.get("country_code") != "AE"],
    }
    encoded = json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return file_hashes, hashlib.sha256(encoded).hexdigest()


def uae_source_hashes() -> dict[str, str]:
    hashes = {}
    for path in sorted((ROOT / "data/sources").glob("SRC-AE-*.json")):
        hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def phase5(gate: Gate) -> None:
    phase4(gate)

    before_sources = uae_source_hashes()
    gate.command("uae_source_refresh", [sys.executable, "scripts/build_uae_sources.py"])
    after_sources = uae_source_hashes()
    gate.require(
        len(after_sources) == 19 and before_sources == after_sources,
        "uae_source_idempotence",
        f"UAE atomic sources={len(after_sources)}/19, hashes unchanged={before_sources == after_sources}",
    )

    before_files, before_non_ae = phase5_import_hashes()
    gate.command("uae_import_refresh", [sys.executable, "scripts/import_uae_phase5.py"])
    after_files, after_non_ae = phase5_import_hashes()
    gate.require(before_files == after_files, "uae_import_idempotence", f"all 8 importer-managed hashes unchanged={before_files == after_files}")
    gate.require(before_non_ae == after_non_ae, "non_uae_preservation", f"canonical non-UAE SHA-256 unchanged={after_non_ae}")

    evidence_paths = [
        ROOT / "reports/uae_validation.json",
        ROOT / "reports/uae_negative_tests.json",
        ROOT / "reports/uae_review_samples.json",
        ROOT / "reports/uae_independent_review.json",
    ]
    before_evidence = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in evidence_paths}
    gate.command("validation_after_uae", [sys.executable, "scripts/validate.py"])
    gate.command("uae_semantic_validation", [sys.executable, "scripts/validate_uae.py"])
    gate.command("uae_negative_tests", [sys.executable, "scripts/test_uae_negative.py"])
    gate.command("uae_review_sample_refresh", [sys.executable, "scripts/build_uae_review_samples.py"])
    gate.command("uae_independent_review", [sys.executable, "scripts/review_uae.py"])
    after_evidence = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in evidence_paths}
    gate.require(before_evidence == after_evidence, "uae_evidence_idempotence", f"validation, mutation, sample, and review hashes unchanged={before_evidence == after_evidence}")
    gate.command("generated_freshness_after_uae", [sys.executable, "scripts/generate.py", "--check"])
    gate.command("uae_final_report_freshness", [sys.executable, "scripts/generate_uae_report.py", "--check"])

    validation = load_json(ROOT / "reports/uae_validation.json")
    review = load_json(ROOT / "reports/uae_independent_review.json")
    negatives = load_json(ROOT / "reports/uae_negative_tests.json")
    gate.require(
        validation.get("status") == "PASS" and validation.get("p0") == 0 and validation.get("critical_p1") == 0,
        "uae_findings_closed",
        f"status={validation.get('status')}, P0={validation.get('p0')}, critical P1={validation.get('critical_p1')}",
    )
    source_check = validation.get("checks", {}).get("sources", {})
    gate.require(
        source_check.get("ab_ratio", 0) >= 95 and source_check.get("published_claims") == source_check.get("ab_claims"),
        "uae_source_threshold",
        f"A/B published claims={source_check.get('ab_claims')}/{source_check.get('published_claims')} ({source_check.get('ab_ratio')}%)",
    )
    review_families = review.get("families", {})
    gate.require(
        review.get("status") == "PASS" and len(review_families) == 9 and all(row.get("sampled", 0) >= row.get("minimum_required", 1) and row.get("status") == "PASS" for row in review_families.values()),
        "uae_review_threshold",
        f"families={len(review_families)}/9, passed={review.get('total_passed')}/{review.get('total_sampled')}, minimum 10% met for every family",
    )
    expected_mutations = {
        "UAE_WRONG_EMIRATE_PARENT", "UAE_WRONG_LOCAL_TYPE", "UAE_ALIAS_AS_ENTITY",
        "UAE_SHARED_FOOD_AS_EXCLUSIVE", "UAE_NATIONAL_CLAIM_AS_LOCAL",
        "UAE_HISTORIC_AS_CURRENT", "UAE_SAME_NAME_DIFFERENT_PARENT", "UAE_FOREIGN_SOURCE",
    }
    observed_mutations = {row.get("mutation") for row in negatives.get("mutations", []) if row.get("detected")}
    gate.require(
        negatives.get("status") == "PASS" and observed_mutations == expected_mutations,
        "uae_required_mutations",
        f"detected={len(observed_mutations)}/8, exact required set={observed_mutations == expected_mutations}",
    )
    headings = [line[3:] for line in (ROOT / "reports/UAE_PILOT_FINAL.md").read_text(encoding="utf-8").splitlines() if line.startswith("## ")]
    gate.require(
        len(headings) == 22 and headings[0] == "Decision" and headings[-1] == "Final Gate",
        "uae_final_report",
        f"exact section count={len(headings)}, first={headings[0] if headings else None}, last={headings[-1] if headings else None}",
    )

    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
    gate.require(not status, "uae_clean_worktree", f"git worktree clean={not status}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["phase0", "phase1", "phase2", "phase3", "phase4", "phase5"])
    args = parser.parse_args()
    gate = Gate(args.phase)
    {"phase0": phase0, "phase1": phase1, "phase2": phase2, "phase3": phase3, "phase4": phase4, "phase5": phase5}[args.phase](gate)
    report = {
        "phase": args.phase,
        "schema_version": "2.0.0",
        "semantic_hash": semantic_hash(ROOT),
        "status": "pass" if not gate.errors else "fail",
        "checks": gate.checks,
        "errors": gate.errors,
    }
    write_json(ROOT / f"reports/{args.phase}_gate.json", report)
    for name, result in gate.checks.items():
        print(f"[{'PASS' if result['status'] == 'pass' else 'FAIL'}] {name}: {result.get('detail', result.get('command', ''))}")
    if gate.errors:
        print(f"{args.phase} gate failed with {len(gate.errors)} error(s)", file=sys.stderr)
        for error in gate.errors: print(f"- {error}", file=sys.stderr)
        return 1
    print(f"{args.phase} gate passed ({len(gate.checks)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
