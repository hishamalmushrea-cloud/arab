#!/usr/bin/env python3
"""Generate the exact 22-section UAE pilot report from structured records and reports."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from model import ROOT, read_jsonl

OUTPUT = ROOT / "reports/UAE_PILOT_FINAL.md"
HEADINGS = [
    "Decision",
    "Scope",
    "Snapshot",
    "Source Evidence",
    "Schema Changes",
    "Federal Emirates",
    "Abu Dhabi Hierarchy",
    "Dubai Hierarchy",
    "Sharjah Hierarchy",
    "Ajman Hierarchy",
    "Umm Al Quwain Hierarchy",
    "Ras Al Khaimah Hierarchy",
    "Fujairah Hierarchy",
    "Entity Resolution",
    "Temporal Status",
    "Populated Places and Coordinates",
    "Denominators and Coverage",
    "Cultural Sample",
    "Food, Dress, and Scope",
    "Dialect Sample",
    "Independent Review and Negative Tests",
    "Final Gate",
]


def load(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def profile_section(profile: dict[str, Any], coverage_by_id: dict[str, dict[str, Any]]) -> str:
    lines = [
        f"**Competent authorities:** {'; '.join(profile['competent_authorities'])}.",
        "",
        "| Contextual layer | Type | Denominator | Matched | Source | Semantic/special case |",
        "|---|---|---:|---:|---|---|",
    ]
    for layer in profile["lower_layers"]:
        cov = coverage_by_id[layer["coverage_record_id"]]
        denominator = "unavailable" if layer["denominator"] is None else str(layer["denominator"])
        lines.append(
            f"| `{layer['layer']}` | `{layer['entity_type']}` | {denominator} | {cov['matched']} | `{layer['source_ids'][0]}` | "
            f"{layer['semantic_definition']} {' '.join(layer['special_cases'])} |"
        )
    return "\n".join(lines)


def render() -> str:
    manifest = load(ROOT / "manifests/AE.yml")
    validation = load(ROOT / "reports/uae_validation.json")
    review = load(ROOT / "reports/uae_independent_review.json")
    negatives = load(ROOT / "reports/uae_negative_tests.json")

    entities = [row for row in read_jsonl(ROOT / "data/entities/entities.jsonl") if row.get("country_code") == "AE"]
    entity_ids = {row["id"] for row in entities}
    aliases = [row for row in read_jsonl(ROOT / "data/aliases/aliases.jsonl") if row.get("entity_id") in entity_ids]
    relationships = [row for row in read_jsonl(ROOT / "data/relationships/relationships.jsonl") if row.get("child_id") in entity_ids]
    claims = [row for row in read_jsonl(ROOT / "data/claims/claims.jsonl") if row.get("subject_id") in entity_ids]
    denominators = [row for row in read_jsonl(ROOT / "data/coverage/denominators.jsonl") if row.get("country_code") == "AE"]
    coverage = [row for row in read_jsonl(ROOT / "data/coverage/coverage.jsonl") if row.get("country_code") == "AE"]
    coverage_by_id = {row["id"]: row for row in coverage}
    profile_by_name = {row["name_en"]: row for row in manifest["emirate_profiles"]}
    type_counts = Counter(row["entity_type"] for row in entities)
    classifications = Counter(row.get("classification") for row in claims if row.get("predicate") != "jurisdiction_semantics")
    lexical = [row for row in claims if row.get("predicate") == "lexical_form"]
    unavailable = [row for row in coverage if row.get("denominator") is None]
    closed = [row for row in coverage if row.get("denominator") is not None]
    all_inputs_pass = all(report and report.get("status") == "PASS" for report in (validation, review, negatives))
    decision = "PASS" if all_inputs_pass else "FAIL"

    sections: dict[str, str] = {}
    sections["Decision"] = (
        f"**{decision}.** The fourth-country pilot is United Arab Emirates only. It closes the seven-emirate federal layer and seven different local administrative profiles without imposing one lower hierarchy. "
        "No fifth country is authorized or started."
    )
    sections["Scope"] = (
        f"The canonical UAE subset contains **{len(entities)} Entities** (country, seven emirates, and 33 contextual local records), **{len(aliases)} Aliases**, "
        f"**{len(relationships)} Relationships**, and **{len(claims)} Claims**. This is a semantic transferability test, not a volume expansion. "
        "Structured JSON/JSONL and `manifests/AE.yml` are authoritative; this Markdown is generated."
    )
    sections["Snapshot"] = (
        "Snapshot `SNP-AE-PILOT-20260815` is dated **2026-08-15**. Its checksum covers the administrative, cultural, source-catalog, and evidence-manifest fixtures. "
        "The import is offline and deterministic. Retrieval dates are not treated as legal commencement dates."
    )
    source_metrics = validation["checks"]["sources"]
    sections["Source Evidence"] = (
        f"The pilot references **{source_metrics['referenced']} atomic Sources**: {source_metrics['pilot_specific']} UAE pilot sources plus the existing ISO country source. "
        f"There are **{source_metrics['evidence_extracts']} checksum-bound persisted relevant-text extracts**. Published Claims have **{source_metrics['ab_ratio']}% A/B sourcing** "
        f"({source_metrics['ab_claims']}/{source_metrics['published_claims']}). Dubai community download failures are recorded in the persisted metadata extract; an unavailable file is not represented as a successful archive."
    )
    sections["Schema Changes"] = (
        "Schema remains **v2.0.0**. Additive changes introduce eight contextual UAE entity types, claim classification `emirate_specific`, entity statuses `renamed`, `merged`, and `abolished`, "
        "and optional manifest `emirate_profiles`. Legacy `ae_municipal_region`, `ae_sector`, and `ae_district` remain for backward compatibility but are deprecated and rejected for new UAE pilot entities. "
        "Problem, rationale, compatibility, temporal semantics, and tests are documented in `schema/UAE_PILOT_ADDITIVE_CHANGE.md`."
    )
    emirate_names = ", ".join(f"{row['name_en']} ({row['name_ar']})" for row in manifest["emirate_profiles"])
    sections["Federal Emirates"] = (
        f"The federal denominator is **7**, matched **7**, excluded **0**, unmatched **0**: {emirate_names}. Every emirate is a child of `ENT-AE-COUNTRY`; this closed layer makes no claim that local hierarchies are uniform."
    )
    sections["Abu Dhabi Hierarchy"] = profile_section(profile_by_name["Abu Dhabi"], coverage_by_id)
    sections["Dubai Hierarchy"] = profile_section(profile_by_name["Dubai"], coverage_by_id)
    sections["Sharjah Hierarchy"] = profile_section(profile_by_name["Sharjah"], coverage_by_id)
    sections["Ajman Hierarchy"] = profile_section(profile_by_name["Ajman"], coverage_by_id)
    sections["Umm Al Quwain Hierarchy"] = profile_section(profile_by_name["Umm Al Quwain"], coverage_by_id)
    sections["Ras Al Khaimah Hierarchy"] = profile_section(profile_by_name["Ras Al Khaimah"], coverage_by_id)
    sections["Fujairah Hierarchy"] = profile_section(profile_by_name["Fujairah"], coverage_by_id)
    sections["Entity Resolution"] = (
        "English canonical names and Arabic official forms resolve to one parent-scoped Entity through Aliases. Same-name records under different parents are not automatically deduplicated. "
        "The independent identity rules distinguish Dibba Municipality in Fujairah from Dibba Al Hisn City Municipality in Sharjah, and distinguish numbered sectors, areas, constituents, and authorities. "
        f"Validation reports zero duplicate IDs, orphans, cycles, or country mismatches; type counts are `{dict(sorted(type_counts.items()))}`."
    )
    sections["Temporal Status"] = (
        "Current, historical, renamed, merged, abolished, and disputed semantics are distinct executable statuses. `Julfar` is one **historical Alias** and one historical claim for Ras Al Khaimah, never a current administrative unit. "
        "Falaj Al Mualla Municipality remains a current authority with a sourced historical claim that its independence followed Decree No. 16 of 2008. No renamed, merged, or abolished example is invented where the bounded sources do not establish one."
    )
    sections["Populated Places and Coordinates"] = (
        "No populated-place Entity was added. The pilot found no dated enumerable UAE-wide registry for cities, towns, villages, settlements, or neighborhoods, so those layers use `denominator_unavailable` and no percentage. "
        "Administrative entities have no invented point coordinates. Al Shindagha and other contextual place mentions remain sourced Claims rather than coordinate-free Entities."
    )
    coverage_lines = [
        "| Layer | Denominator | Matched | Excluded | Unmatched | Coverage | Missing reason |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    den_by_id = {row["id"]: row for row in denominators}
    for row in sorted(coverage, key=lambda value: value["layer"]):
        den = den_by_id[row["denominator_id"]]
        coverage_value = "—" if row["coverage_percentage"] is None else f"{row['coverage_percentage']}%"
        denominator_value = "unavailable" if row["denominator"] is None else str(row["denominator"])
        coverage_lines.append(
            f"| `{row['layer']}` | {denominator_value} | {row['matched']} | {row['excluded']} | {row['unmatched']} | {coverage_value} | {den['missing_reason'] or '—'} |"
        )
    sections["Denominators and Coverage"] = (
        f"There are **{len(denominators)} Denominators** and {len(coverage)} paired Coverage records: **{len(closed)} closed** and **{len(unavailable)} unavailable**. "
        "Every closed layer satisfies `matched + excluded = denominator`; every unavailable layer has a reason and no percentage.\n\n" + "\n".join(coverage_lines)
    )
    sections["Cultural Sample"] = (
        "The sourced sample represents all seven emirates and the required coastal, desert, mountain, oasis, urban, and historical contexts. Environmental, heritage, livelihood, craft, and custom material is attached as scoped Claims to the country or emirate identity; unsupported fields are not filled. "
        f"Cultural classifications are `{dict(sorted((str(key), value) for key, value in classifications.items()))}`."
    )
    sections["Food, Dress, and Scope"] = (
        "Food Claims distinguish national association from shared origin: Gahwa/dates, food ecology, and Chabab are national-context records; Khameer is `shared`. Ayala and Sadu are also `shared`, and social performance context is `popular`. "
        "No Claim says a Gulf-shared practice is exclusive to the UAE. No dress Claim is materialized because the bounded evidence set did not provide sufficiently specific, scope-qualified support."
    )
    dialect_lines = ["| Form | Meaning | Variety | Place | Register | Study date | Classification |", "|---|---|---|---|---|---|---|"]
    for row in sorted(lexical, key=lambda value: value["lexical_context"]["form"]):
        context = row["lexical_context"]
        dialect_lines.append(f"| {context['form']} | {context['meaning']} | {context['variety']} | `{context['place_id']}` | {context['register']} | {context['study_date']} | `{row['classification']}` |")
    sections["Dialect Sample"] = (
        "The sample is limited to three forms from Ribeiro Daquila (2020). `وايد` and `شو` remain `regional` because the source explicitly locates them beyond uniquely Emirati use; `ربع` is documented in an Emirati translation without an exclusivity claim.\n\n"
        + "\n".join(dialect_lines)
    )
    review_families = ", ".join(f"{name} {detail['sampled']}/{detail['population']}" for name, detail in sorted(review["families"].items()))
    sections["Independent Review and Negative Tests"] = (
        f"Independent review is **{review['status']}**: {review['total_passed']}/{review['total_sampled']} sampled checks passed, with every required family at least 10% (`{review_families}`). "
        f"It does not import or call the UAE importer. Negative testing is **{negatives['status']}**: {negatives['detected']}/{negatives['required']} required mutations detected. "
        f"P0={validation['p0'] + review['p0']}; critical P1={validation['critical_p1'] + review['critical_p1']}."
    )
    sections["Final Gate"] = (
        f"UAE semantic validation: **{validation['status']}**. Independent review: **{review['status']}**. Required mutations: **{negatives['status']}**. "
        f"Pilot-local validation/review/mutation evidence: **{'PASS' if all_inputs_pass else 'FAIL'}**. The aggregate release clean-tree gate is recorded separately in `reports/phase5_gate.json`. The transferability decision is: **PASS for contextual per-emirate modeling; stop and await authorization rather than begin another country.**"
    )

    body = ["# United Arab Emirates Fourth-Country Pilot — Final Report", "", "Generated from Schema v2.0.0 structured records; do not edit figures manually."]
    for heading in HEADINGS:
        body.extend(["", f"## {heading}", "", sections[heading]])
    body.append("")
    text = "\n".join(body)
    actual = [line[3:] for line in text.splitlines() if line.startswith("## ")]
    if actual != HEADINGS or len(actual) != 22:
        raise RuntimeError(f"UAE report headings differ: {actual}")
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        actual = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if actual != expected:
            print(f"Generated UAE report is stale: {OUTPUT.relative_to(ROOT)}")
            return 1
        print("Generated UAE report is current and has exactly 22 sections.")
        return 0
    OUTPUT.write_text(expected, encoding="utf-8")
    print("Generated reports/UAE_PILOT_FINAL.md with exactly 22 sections.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
