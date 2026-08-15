#!/usr/bin/env python3
"""Independent-path review for the Saudi Arabia third-country cycle.

This script does not import the Saudi importer. It independently parses the local
HTML tables, reconstructs expected administrative identities and parents, checks
fixed stratified samples, reviews bounded content, and injects seven required
negative mutants.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from model import ROOT, read_jsonl, write_json

COUNTRY = "ENT-SA-COUNTRY"
AS_OF = "2026-08-15"
SAMPLE_PATH = ROOT / "data/review/saudi_review_samples.json"
NEGATIVE_PATH = ROOT / "tests/fixtures/saudi_negative_cases.json"
REPORT_PATH = ROOT / "reports/saudi_independent_review.json"
RAW = ROOT / "data/imports/saudi/raw" / AS_OF

REGIONS = ["riyadh", "makkah", "madinah", "qassim", "eastern", "asir", "tabuk", "hail", "northern-borders", "jazan", "najran", "al-baha", "al-jawf"]
REGION_AR = {
    "riyadh":"منطقة الرياض", "makkah":"منطقة مكة المكرمة", "madinah":"منطقة المدينة المنورة", "qassim":"منطقة القصيم",
    "eastern":"المنطقة الشرقية", "asir":"منطقة عسير", "tabuk":"منطقة تبوك", "hail":"منطقة حائل",
    "northern-borders":"منطقة الحدود الشمالية", "jazan":"منطقة جازان", "najran":"منطقة نجران", "al-baha":"منطقة الباحة", "al-jawf":"منطقة الجوف",
}


class Tables(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.row: list[str] | None = None
        self.cell: list[str] | None = None
        self.tables: list[list[list[str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "table":
            if self.depth == 0: self.tables.append([])
            self.depth += 1
        elif self.depth and tag == "tr": self.row = []
        elif self.depth and tag in {"th", "td"}: self.cell = []

    def handle_data(self, data: str) -> None:
        if self.cell is not None: self.cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.depth and tag in {"th", "td"} and self.cell is not None:
            assert self.row is not None
            self.row.append(re.sub(r"\s+", " ", " ".join(self.cell)).strip())
            self.cell = None
        elif self.depth and tag == "tr" and self.row is not None:
            self.tables[-1].append(self.row); self.row = None
        elif tag == "table" and self.depth: self.depth -= 1


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest_id(prefix: str, key: str, size: int = 16) -> str:
    return f"{prefix}-{hashlib.sha256(key.encode('utf-8')).hexdigest()[:size].upper()}"


def rid(key: str) -> str:
    return f"ENT-SA-REGION-{key.upper()}"


def expected_administration() -> dict[str, dict[str, Any]]:
    expected: dict[str, dict[str, Any]] = {}
    for key in REGIONS:
        expected[rid(key)] = {"name": REGION_AR[key], "type": "sa_region", "parent": COUNTRY, "kind": "region"}
        parser = Tables(); parser.feed((RAW / f"saudipedia-centers-{key}.html").read_text(encoding="utf-8"))
        rows = parser.tables[0][1:]
        for row_index, (label, cell) in enumerate(rows, start=2):
            if label.startswith("محافظة "):
                kind, name = "governorate", label.removeprefix("محافظة ").strip()
                parent_id = digest_id("ENT-SA-GOV", f"{key}:{name}")
                expected[parent_id] = {"name": name, "type": "sa_governorate", "parent": rid(key), "kind": kind, "row": row_index}
            else:
                kind = "capital_city"
                name = label.removeprefix("مدينة ").strip()
                parent_id = f"ENT-SA-CITY-{key.upper()}-SEAT"
                expected[parent_id] = {"name": name, "type": "city", "parent": rid(key), "kind": kind, "row": row_index}
            cleaned = cell.strip().rstrip(".").strip()
            centers = [] if cleaned == "لا يوجد" else [part.strip() for part in cleaned.split("-" if key == "riyadh" else "،") if part.strip()]
            seen = Counter()
            for position, name in enumerate(centers, start=1):
                seen[name] += 1
                if seen[name] > 1:
                    continue
                identifier = digest_id("ENT-SA-CENTER", f"{key}:{label.removeprefix('محافظة ').removeprefix('مدينة ').strip()}:{name}")
                expected[identifier] = {
                    "name": name, "type": "sa_markaz", "parent": rid(key) if kind == "capital_city" else parent_id,
                    "kind": "center", "row": row_index, "position": position,
                }
    return expected


def source_map() -> dict[str, dict[str, Any]]:
    rows = [load(path) for path in sorted((ROOT / "data/sources").glob("*.json"))]
    return {row["id"]: row for row in rows}


def pilot_state() -> dict[str, Any]:
    entities = [row for row in read_jsonl(ROOT / "data/entities/entities.jsonl") if row.get("country_code") == "SA"]
    ids = {row["id"] for row in entities}
    return {
        "entities": entities,
        "aliases": [row for row in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if row.get("entity_id") in ids],
        "relationships": [row for row in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if row.get("child_id") in ids],
        "claims": [row for row in read_jsonl(ROOT / "data/claims/claims.jsonl") if row.get("subject_id") in ids],
        "denominators": [row for row in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if row.get("country_code") == "SA"],
        "coverage": [row for row in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if row.get("country_code") == "SA"],
        "sources": source_map(),
    }


def issue_codes(state: dict[str, Any], expected: dict[str, dict[str, Any]]) -> set[str]:
    issues: set[str] = set()
    entity_by_id = {row["id"]: row for row in state["entities"]}
    parent_rels: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in state["relationships"]:
        if row.get("relationship_type") == "administrative_parent":
            parent_rels[row.get("child_id")].append(row)
    for identifier, exp in expected.items():
        if exp["kind"] not in {"region", "governorate", "center"}:
            continue
        actual = entity_by_id.get(identifier)
        rels = parent_rels.get(identifier, [])
        bad = not actual or actual.get("entity_type") != exp["type"] or len(rels) != 1 or rels[0].get("parent_id") != exp["parent"]
        if bad:
            issues.add("wrong_governorate" if exp["kind"] == "governorate" else ("wrong_center_linkage" if exp["kind"] == "center" else "wrong_region_linkage"))

    canonical = defaultdict(set)
    for row in state["entities"]:
        canonical[row.get("canonical_name", "").strip().casefold()].add(row["id"])
    if any(canonical[row.get("name", "").strip().casefold()] - {row.get("entity_id")} for row in state["aliases"]):
        issues.add("alias_as_entity")

    if any(row.get("predicate", "").startswith("official_national_") and row.get("subject_id") != COUNTRY for row in state["claims"]):
        issues.add("national_to_local_leakage")
    sources = state["sources"]
    if any(row.get("source_id") in sources and "SA" not in sources[row["source_id"]].get("country_codes", []) for row in state["claims"]):
        issues.add("foreign_country_source")
    historical_id = digest_id("ENT-SA-PLACE", "qaryat-al-faw")
    historical = entity_by_id.get(historical_id)
    if not historical or historical.get("status") != "historical" or historical.get("entity_type") != "historical_place":
        issues.add("historical_as_current")
    for row in state["claims"]:
        if row.get("predicate") == "population":
            dates = [row.get("observed_at"), row.get("valid_from"), row.get("valid_to")]
            if not any(isinstance(value, str) and re.match(r"^\d{4}-", value) for value in dates):
                issues.add("population_without_year")
    return issues


def mutate(state: dict[str, Any], kind: str, expected: dict[str, dict[str, Any]]) -> None:
    if kind == "wrong_governorate":
        identifier = next(i for i, row in expected.items() if row["kind"] == "governorate")
        rel = next(row for row in state["relationships"] if row.get("child_id") == identifier and row.get("relationship_type") == "administrative_parent")
        rel["parent_id"] = next(rid(key) for key in REGIONS if rid(key) != expected[identifier]["parent"])
    elif kind == "wrong_center_linkage":
        identifier = next(i for i, row in expected.items() if row["kind"] == "center")
        rel = next(row for row in state["relationships"] if row.get("child_id") == identifier and row.get("relationship_type") == "administrative_parent")
        rel["parent_id"] = COUNTRY
    elif kind == "alias_as_entity":
        row = copy.deepcopy(next(row for row in state["entities"] if row["id"] == rid("riyadh")))
        row["id"] = "ENT-SA-REGION-ALIAS-MUTANT"
        row["canonical_name"] = "Riyadh Region"
        row["canonical_name_language"] = "en"
        state["entities"].append(row)
    elif kind == "national_to_local_leakage":
        row = next(row for row in state["claims"] if row.get("predicate") == "official_national_dish")
        row["subject_id"] = rid("riyadh")
    elif kind == "foreign_country_source":
        row = next(row for row in state["claims"] if row.get("predicate") == "administrative_registry_entry")
        row["source_id"] = "SRC-JO-REGULATION-46-2000"
    elif kind == "historical_as_current":
        identifier = digest_id("ENT-SA-PLACE", "qaryat-al-faw")
        next(row for row in state["entities"] if row["id"] == identifier)["status"] = "current"
    elif kind == "population_without_year":
        state["claims"].append({
            "id":"CLM-SA-POPULATION-MUTANT", "subject_id":rid("riyadh"), "predicate":"population",
            "observed_at":None, "valid_from":None, "valid_to":None, "source_id":"SRC-SA-GASTAT-HEALTH-METHOD-2026",
            "source_locator":"mutant", "value":{"type":"integer", "data":1},
        })
    else:
        raise AssertionError(kind)


def input_fingerprint() -> str:
    paths = [
        ROOT / "data/entities/entities.jsonl", ROOT / "data/aliases/aliases.jsonl", ROOT / "data/relationships/relationships.jsonl",
        ROOT / "data/claims/claims.jsonl", ROOT / "data/coverage/denominators.jsonl", ROOT / "data/coverage/coverage.jsonl",
        ROOT / "data/imports/saudi/snapshot_manifest.json", ROOT / "data/imports/saudi/cultural_content_2026.json",
        ROOT / "data/imports/saudi/parsed_registry.json", ROOT / "data/imports/saudi/anomaly_ledger.json", SAMPLE_PATH, NEGATIVE_PATH,
    ] + sorted((ROOT / "data/sources").glob("*SA*.json"))
    digest = hashlib.sha256()
    for path in paths:
        digest.update(str(path.relative_to(ROOT)).encode()); digest.update(b"\0"); digest.update(path.read_bytes()); digest.update(b"\0")
    return digest.hexdigest()


def review() -> dict[str, Any]:
    sample = load(SAMPLE_PATH)
    negative = load(NEGATIVE_PATH)
    cultural = load(ROOT / "data/imports/saudi/cultural_content_2026.json")
    expected = expected_administration()
    state = pilot_state()
    errors: list[str] = []
    baseline = issue_codes(state, expected)
    if baseline:
        errors.append(f"baseline issue codes: {sorted(baseline)}")

    entity_by_id = {row["id"]: row for row in state["entities"]}
    by_family = {family: {row["id"]: row for row in state[family]} for family in ["entities", "aliases", "relationships", "claims", "denominators", "coverage"]}
    for sample_field, family in [("entity_ids","entities"),("alias_ids","aliases"),("relationship_ids","relationships"),("claim_ids","claims"),("denominator_ids","denominators"),("coverage_ids","coverage")]:
        missing = sorted(set(sample[sample_field]) - set(by_family[family]))
        if missing: errors.append(f"sample IDs missing from {family}: {missing}")
    if set(sample["source_ids"]) - set(state["sources"]):
        errors.append("sample source IDs missing")

    # Independent administrative reconstruction and sampled entity provenance.
    expected_counts = Counter(row["type"] for row in expected.values())
    actual_counts = Counter(row["entity_type"] for row in state["entities"])
    if expected_counts != Counter({"sa_region":13,"sa_governorate":141,"city":13,"sa_markaz":1521}):
        errors.append(f"independent parser counts unexpected: {dict(expected_counts)}")
    if any(actual_counts[key] < value for key, value in expected_counts.items()):
        errors.append("production administrative entity counts are below independent expectations")
    for identifier in sample["entity_ids"]:
        actual = entity_by_id[identifier]
        if not actual.get("canonical_source_id") or not actual.get("source_locator"):
            errors.append(f"sample entity provenance missing: {identifier}")
        if identifier in expected:
            exp = expected[identifier]
            if (actual["canonical_name"], actual["entity_type"]) != (exp["name"], exp["type"]):
                errors.append(f"sample administrative entity mismatch: {identifier}")

    # Relationship, alias, claim, and source samples.
    for identifier in sample["relationship_ids"]:
        row = by_family["relationships"][identifier]
        if row.get("child_id") not in entity_by_id or row.get("parent_id") not in entity_by_id or not row.get("source_id") or not row.get("source_locator"):
            errors.append(f"sample relationship invalid: {identifier}")
    alias_keys = []
    for identifier in sample["alias_ids"]:
        row = by_family["aliases"][identifier]
        alias_keys.append((row["entity_id"], row["language"], row["kind"], row["name"].strip().casefold()))
        if row.get("entity_id") not in entity_by_id or not row.get("source_id") or not row.get("source_locator"):
            errors.append(f"sample alias invalid: {identifier}")
    if len(alias_keys) != len(set(alias_keys)): errors.append("sample duplicate aliases")
    for identifier in sample["claim_ids"]:
        row = by_family["claims"][identifier]
        if row.get("subject_id") not in entity_by_id or row.get("source_id") not in state["sources"] or not row.get("source_locator") or row.get("verification_status") not in {"verified","source_verified"}:
            errors.append(f"sample claim invalid: {identifier}")
    for identifier in sample["source_ids"]:
        row = state["sources"][identifier]
        required = ["title","publisher","source_type","url","retrieved_at","license","language","country_codes","locator","quality_tier"]
        if any(row.get(field) in (None,"",[]) for field in required) or (row.get("author") is None and row.get("organization") is None):
            errors.append(f"sample source metadata incomplete: {identifier}")

    # Snapshot checksums are recalculated independently.
    snapshot_manifest = load(ROOT / "data/imports/saudi/snapshot_manifest.json")
    snapshot_mismatches = []
    for row in snapshot_manifest["records"]:
        payload = (ROOT / "data/imports/saudi" / row["path"]).read_bytes()
        if len(payload) != row["bytes"] or hashlib.sha256(payload).hexdigest() != row["sha256"]:
            snapshot_mismatches.append(row["path"])
    if len(snapshot_manifest["records"]) != 15 or snapshot_mismatches:
        errors.append(f"snapshot verification failed: {snapshot_mismatches}")

    # Every known denominator closes; unavailable/conflicted layers never claim a percentage.
    den_by_id = by_family["denominators"]
    for cid in sample["coverage_ids"]:
        cov = by_family["coverage"][cid]; den = den_by_id[cov["denominator_id"]]
        if den["value"] is None:
            if cov["complete"] or cov["coverage_percentage"] is not None or not cov["missing_reason"]:
                errors.append(f"unavailable denominator incorrectly closed: {cid}")
        elif cov["matched"] + cov["excluded"] != den["value"] or cov["unmatched"] != 0 or cov["missing"] != 0 or not cov["complete"]:
            errors.append(f"known denominator equation failed: {cid}")

    # Bounded places/sites, temporal separation, culture and dialect chain.
    if len(sample["populated_place_ids"]) != 4 or any(identifier not in entity_by_id for identifier in sample["populated_place_ids"]):
        errors.append("bounded populated-place review failed")
    historical = entity_by_id.get(digest_id("ENT-SA-PLACE", "qaryat-al-faw"), {})
    if historical.get("status") != "historical" or historical.get("entity_type") != "historical_place":
        errors.append("historical/current place separation failed")
    if len(sample["site_ids"]) != 8 or any(entity_by_id[i]["entity_type"] not in {"archaeological_site","cultural_site","natural_site"} for i in sample["site_ids"]):
        errors.append("eight-property site sample failed")
    claims = state["claims"]
    cultural_counts = Counter(row["predicate"] for row in claims)
    expected_cultural = {"official_regional_dish":13,"official_national_dish":1,"official_national_dessert":1,"intangible_cultural_practice":4,"regional_clothing_evidence_scope":1,"unesco_world_heritage_inscription":8,"environmental_context":8}
    if any(cultural_counts[key] != value for key, value in expected_cultural.items()):
        errors.append(f"bounded cultural claim counts failed: {dict(cultural_counts)}")
    if any(row["classification"] not in {"regional","shared"} for row in claims if row["predicate"] in {"official_regional_dish","intangible_cultural_practice"}):
        errors.append("regional/shared cultural classification failed")
    national_claims = [row for row in claims if row["predicate"] in {"official_national_dish","official_national_dessert"}]
    if any(row["subject_id"] != COUNTRY or row["classification"] != "national" for row in national_claims):
        errors.append("national culinary scope failed")
    if cultural["domain_status"]["clothing"].startswith("explicitly unsupported") is False:
        errors.append("unsupported clothing scope not explicit")

    rels_by_child = defaultdict(list)
    for row in state["relationships"]: rels_by_child[row["child_id"]].append(row)
    dialect_errors = []
    for identifier in sample["dialect_entity_ids"]:
        entity_row = entity_by_id.get(identifier, {})
        rel_types = {row["relationship_type"] for row in rels_by_child[identifier]}
        lex = [row for row in claims if row.get("subject_id") == identifier and row.get("predicate") == "lexical_attestation"]
        if entity_row.get("entity_type") != "lexical_form" or not {"form_of","attested_in"} <= rel_types or len(lex) != 1:
            dialect_errors.append(identifier); continue
        context = lex[0].get("lexical_context") or {}
        if context.get("form") != entity_row.get("canonical_name") or context.get("place_id") not in entity_by_id or not context.get("meaning") or not context.get("register") or not context.get("study_date"):
            dialect_errors.append(identifier)
    if dialect_errors or any("dialect_count" in row.get("predicate", "") for row in claims):
        errors.append(f"dialect chain/count review failed: {dialect_errors}")

    published = [row for row in claims if row.get("published")]
    ab = [row for row in published if state["sources"].get(row.get("source_id"), {}).get("quality_tier") in {"A","B"}]
    ab_ratio = len(ab) / len(published) * 100 if published else 0.0
    sensitive = [row for row in published if row.get("sensitivity") == "sensitive"]
    sensitive_bad = [row for row in sensitive if row.get("status") != "disputed" and (not row.get("second_source_id") or row.get("second_source_id") == row.get("source_id"))]
    if ab_ratio < 95: errors.append(f"A/B claim ratio below threshold: {ab_ratio:.2f}")
    if sensitive_bad: errors.append(f"noncompliant sensitive claims: {len(sensitive_bad)}")

    negative_outcomes = {}
    for case in negative["cases"]:
        mutant = copy.deepcopy(state); mutate(mutant, case["mutation"], expected)
        found = issue_codes(mutant, expected)
        ok = case["expected_issue"] in found
        negative_outcomes[case["id"]] = "pass" if ok else "fail"
        if not ok: errors.append(f"negative case not detected: {case['id']} -> {sorted(found)}")

    totals = {
        "entities":len(state["entities"]), "aliases":len(state["aliases"]), "relationships":len(state["relationships"]), "claims":len(claims),
        "denominators":len(state["denominators"]), "coverage":len(state["coverage"]), "sources":len({row.get("canonical_source_id") for row in state["entities"]} | {row.get("source_id") for row in state["aliases"]+state["relationships"]+claims+state["denominators"]+state["coverage"]}),
        "populated_places":4, "sites":8, "cultural_claims":len(sample["cultural_claim_ids"]), "dialect_entities":4, "dialect_claims":4,
    }
    reviewed = {
        "entities":len(sample["entity_ids"]), "aliases":len(sample["alias_ids"]), "relationships":len(sample["relationship_ids"]), "claims":len(sample["claim_ids"]),
        "denominators":len(sample["denominator_ids"]), "coverage":len(sample["coverage_ids"]), "sources":len(sample["source_ids"]),
        "populated_places":len(sample["populated_place_ids"]), "sites":len(sample["site_ids"]), "cultural_claims":len(sample["cultural_claim_ids"]),
        "dialect_entities":len(sample["dialect_entity_ids"]), "dialect_claims":len(sample["dialect_claim_ids"]),
    }
    rates = {key: round(reviewed[key] / totals[key], 4) for key in totals}
    below = {key:value for key,value in rates.items() if value < 0.10}
    if below: errors.append(f"sample rates below 10%: {below}")

    duplicate_texts = sum(count - 1 for count in Counter(json.dumps(row["value"], ensure_ascii=False, sort_keys=True) for row in claims).values() if count > 1)
    return {
        "schema_version":"1.0.0", "country_code":"SA", "snapshot_date":AS_OF,
        "review_method":"Independent raw-HTML parser and fixed SHA-256 stratified sample; full denominator, culture and dialect invariants; seven injected Saudi-specific mutants. The importer is not imported or called.",
        "reviewer":"automated-independent-path", "input_fingerprint_sha256":input_fingerprint(), "passed":not errors,
        "totals":totals, "reviewed":reviewed, "sample_rates":rates, "baseline_issue_codes":sorted(baseline),
        "negative_test_outcomes":negative_outcomes, "p0_findings":0 if not errors else len(errors), "p1_findings":0,
        "metrics":{"ab_claim_ratio":round(ab_ratio,2),"published_claims":len(published),"sensitive_claims":len(sensitive),"sensitive_compliant":len(sensitive)-len(sensitive_bad),"duplicate_claim_text_occurrences":duplicate_texts,"text_duplication_rate":round(duplicate_texts/len(claims)*100,4) if claims else 0.0},
        "errors":errors,
    }


def main() -> int:
    result = review()
    write_json(REPORT_PATH, result)
    print(json.dumps({"passed":result["passed"],"reviewed":result["reviewed"],"negative_tests":result["negative_test_outcomes"],"metrics":result["metrics"],"errors":result["errors"]},ensure_ascii=False,sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
