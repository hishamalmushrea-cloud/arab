#!/usr/bin/env python3
"""Deterministically rebuild the Jordan Phase 3 transferability pilot.

The importer reads only committed, checksum-bound fixtures. It replaces Jordan
pilot rows, preserves every non-Jordan record, and retains the pre-existing
Jordan country entity and country alias.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from model import AS_OF, ROOT, SCHEMA_VERSION, entity_id, file_sha256, read_jsonl, record_id, write_json, write_jsonl

IMPORT = ROOT / "data/imports/jordan"
ENTITY_PATH = ROOT / "data/entities/entities.jsonl"
ALIAS_PATH = ROOT / "data/aliases/aliases.jsonl"
REL_PATH = ROOT / "data/relationships/relationships.jsonl"
CLAIM_PATH = ROOT / "data/claims/claims.jsonl"
SNAPSHOT_PATH = ROOT / "data/snapshots/snapshots.jsonl"
DENOM_PATH = ROOT / "data/coverage/denominators.jsonl"
COVERAGE_PATH = ROOT / "data/coverage/coverage.jsonl"
MANIFEST_PATH = ROOT / "manifests/JO.yml"
DOMAIN_STATUS_PATH = ROOT / "data/cultural/jordan_domain_status.json"
COUNTRY = "ENT-JO-COUNTRY"
SNAPSHOT = "SNP-JO-PILOT-2026-08-15"
BASELINE = "SRC-JO-REGULATION-46-2000"
AMENDMENT = "SRC-JO-REGULATION-29-2024"
GAZETTE = "SRC-JO-GAZETTE-5931-2024"
RUWAYSHID = "SRC-JO-MOI-RUWAYSHID-2026"
WHC_REGISTER = "SRC-UNESCO-WHC-JO-2026"
LEGAL_LICENSE = "Publicly accessible factual record; resource-specific reuse terms not stated"
WHC_LICENSE = "UNESCO website terms; individual descriptions are separately licensed CC BY-SA 3.0 IGO"


def load_json(name: str) -> dict[str, Any]:
    return json.loads((IMPORT / name).read_text(encoding="utf-8"))


def verify_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    manifest = load_json("snapshot_manifest.json")
    assert manifest["country_code"] == "JO" and manifest["snapshot_date"] == AS_OF
    assert len(manifest["files"]) == 25
    for item in manifest["files"]:
        path = ROOT / item["path"]
        payload = path.read_bytes()
        assert len(payload) == item["bytes"], f"byte count changed: {path}"
        assert hashlib.sha256(payload).hexdigest() == item["sha256"], f"checksum changed: {path}"

    hierarchy = load_json("hierarchy_2024.json")
    heritage = load_json("world_heritage_2026.json")
    cultural = load_json("cultural_content_2026.json")
    resolution = load_json("entity_resolution_2026.json")

    assert hierarchy["derivation"] == {
        "pre_amendment": {"governorates": 12, "liwa": 51, "qada": 38},
        "amendment_effect": {"liwa": 4, "qada": -2},
        "current": {"governorates": 12, "liwa": 55, "qada": 36},
    }
    governors = hierarchy["governorates"]
    counts = Counter({
        "governorates": len(governors),
        "liwa": sum(len(g["liwa"]) for g in governors),
        "qada": sum(len(l["qada"]) for g in governors for l in g["liwa"]),
    })
    assert counts == Counter({"governorates": 12, "liwa": 55, "qada": 36})
    expected_by_governorate = {
        "amman": (9, 4), "irbid": (10, 0), "balqa": (5, 3), "karak": (8, 2),
        "maan": (4, 4), "zarqa": (3, 3), "mafraq": (5, 9), "tafilah": (3, 0),
        "madaba": (2, 5), "jerash": (2, 2), "ajloun": (2, 2), "aqaba": (2, 2),
    }
    actual_by_governorate = {
        g["key"]: (len(g["liwa"]), sum(len(l["qada"]) for l in g["liwa"])) for g in governors
    }
    assert actual_by_governorate == expected_by_governorate
    assert heritage["denominator"] == len(heritage["properties"]) == 8
    assert heritage["bounded_populated_places"]["denominator"] == len(heritage["bounded_populated_places"]["places"]) == 4
    assert len(cultural["claims"]) == 4
    assert cultural["domain_status"]["dialect"]["status"] == "not_documented"
    assert len(resolution["candidate_decisions"]) == 12
    assert all(row["existing_match"] is None for row in resolution["candidate_decisions"])
    return hierarchy, heritage, cultural, resolution


def entity(identifier: str, name: str, entity_type: str, source_id: str, locator: str, *,
           status: str = "current", valid_from: str | None = None,
           coordinates: dict[str, Any] | None = None, notes: str | None = None) -> dict[str, Any]:
    return {
        "id": identifier,
        "schema_version": SCHEMA_VERSION,
        "country_code": "JO",
        "canonical_name": name,
        "canonical_name_language": "ar",
        "entity_type": entity_type,
        "status": status,
        "valid_from": valid_from,
        "valid_to": None,
        "canonical_source_id": source_id,
        "source_locator": locator,
        "legacy_ids": [],
        "coordinates": coordinates,
        "notes": notes,
        "verification_status": "verified",
        "confidence": "high",
    }


def alias(entity_identifier: str, name: str, source_id: str, locator: str, *, kind: str = "transliteration") -> dict[str, Any]:
    return {
        "id": record_id("ALS", entity_identifier, "en", kind, name),
        "schema_version": SCHEMA_VERSION,
        "entity_id": entity_identifier,
        "name": name,
        "language": "en",
        "script": "Latn",
        "kind": kind,
        "status": "current",
        "source_id": source_id,
        "source_locator": locator,
        "valid_from": None,
        "valid_to": None,
    }


def relationship(child: str, parent: str, relationship_type: str, source_id: str, locator: str, *,
                 status: str = "current", valid_from: str | None = None, notes: str | None = None) -> dict[str, Any]:
    return {
        "id": record_id("REL", child, parent, relationship_type),
        "schema_version": SCHEMA_VERSION,
        "child_id": child,
        "parent_id": parent,
        "relationship_type": relationship_type,
        "status": status,
        "valid_from": valid_from,
        "valid_to": None,
        "source_id": source_id,
        "source_locator": locator,
        "notes": notes,
        "verification_status": "verified",
        "confidence": "high",
    }


def claim(subject: str, predicate: str, value: Any, source_id: str, locator: str, *,
          classification: str | None = None, status: str = "verified", valid_from: str | None = None,
          notes: str | None = None) -> dict[str, Any]:
    value_type = "boolean" if isinstance(value, bool) else "integer" if isinstance(value, int) else "number" if isinstance(value, float) else "string"
    return {
        "id": record_id("CLM", subject, predicate, json.dumps(value, ensure_ascii=False, sort_keys=True)),
        "schema_version": SCHEMA_VERSION,
        "subject_id": subject,
        "predicate": predicate,
        "value": {"type": value_type, "data": value},
        "unit": None,
        "status": status,
        "observed_at": AS_OF,
        "valid_from": valid_from,
        "valid_to": None,
        "source_id": source_id,
        "second_source_id": None,
        "source_locator": locator,
        "second_source_locator": None,
        "sensitivity": "ordinary",
        "notes": notes,
        "verification_status": "verified",
        "confidence": "high",
        "classification": classification,
        "published": True,
        "lexical_context": None,
    }


def source_for_liwa(row: dict[str, Any]) -> tuple[str, str]:
    if row["source"] == "amendment":
        return AMENDMENT, f"Regulation No. 29 of 2024; replacement clause creating or promoting Liwa {row['name_ar']}"
    if row["source"] == "ruwayshid":
        return RUWAYSHID, "Current Ministry of Interior page identifying Liwa Ruwayshid in Mafraq Governorate"
    return BASELINE, ""


def build_admin(hierarchy: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, str]]:
    entities: list[dict[str, Any]] = []
    aliases: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    ids: dict[str, str] = {"country": COUNTRY}

    for governorate in hierarchy["governorates"]:
        locator = f"Regulation No. 46 of 2000, Article 2 and {governorate['article']}"
        governorate_id = entity_id("JO", "jo_governorate", governorate["name_ar"], COUNTRY)
        ids[f"governorate:{governorate['key']}"] = governorate_id
        entities.append(entity(governorate_id, governorate["name_ar"], "jo_governorate", BASELINE, locator,
                               notes="Current legal governorate; a governorate is not conflated with its same-name city or administrative seat."))
        aliases.append(alias(governorate_id, governorate["name_en"], BASELINE, locator))
        relationships.append(relationship(governorate_id, COUNTRY, "administrative_parent", BASELINE, locator))
        claims.append(claim(governorate_id, "administrative_center", governorate["center_ar"], BASELINE, locator,
                            classification="official"))

        for liwa in governorate["liwa"]:
            source_id, special_locator = source_for_liwa(liwa)
            liwa_locator = special_locator or f"Regulation No. 46 of 2000, {governorate['article']}; Liwa {liwa['name_ar']} clause"
            liwa_id = entity_id("JO", "jo_liwa", liwa["name_ar"], governorate["key"])
            ids[f"liwa:{governorate['key']}:{liwa['key']}"] = liwa_id
            liwa_notes = "Current legal liwa; administrative center is represented as a sourced claim, not as an administrative child."
            if liwa["source"] == "ruwayshid":
                liwa_notes += " Exact commencement date is not_documented."
            entities.append(entity(liwa_id, liwa["name_ar"], "jo_liwa", source_id, liwa_locator,
                                   valid_from=liwa["valid_from"], notes=liwa_notes))
            aliases.append(alias(liwa_id, liwa["name_en"], source_id, liwa_locator))
            relationships.append(relationship(liwa_id, governorate_id, "administrative_parent", source_id, liwa_locator,
                                              valid_from=liwa["valid_from"]))
            claims.append(claim(liwa_id, "administrative_center", liwa["center_ar"], source_id, liwa_locator,
                                classification="official", valid_from=liwa["valid_from"]))

            for qada in liwa["qada"]:
                qada_locator = f"Regulation No. 46 of 2000, {governorate['article']}; Qada {qada['name_ar']} clause under Liwa {liwa['name_ar']}"
                qada_id = entity_id("JO", "jo_qada", qada["name_ar"], f"{governorate['key']}:{liwa['key']}")
                ids[f"qada:{governorate['key']}:{liwa['key']}:{qada['key']}"] = qada_id
                entities.append(entity(qada_id, qada["name_ar"], "jo_qada", BASELINE, qada_locator,
                                       notes="Current subordinate legal qada. Same-name statistical qada rows are not additional legal entities."))
                aliases.append(alias(qada_id, qada["name_en"], BASELINE, qada_locator))
                relationships.append(relationship(qada_id, liwa_id, "administrative_parent", BASELINE, qada_locator))
                claims.append(claim(qada_id, "administrative_center", qada["center_ar"], BASELINE, qada_locator,
                                    classification="official"))

    assert Counter(row["entity_type"] for row in entities) == Counter({"jo_governorate": 12, "jo_liwa": 55, "jo_qada": 36})
    return entities, aliases, relationships, claims, ids


def build_heritage(heritage: dict[str, Any], ids: dict[str, str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    entities: list[dict[str, Any]] = []
    aliases: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    site_ids: dict[str, str] = {}

    for row in heritage["properties"]:
        identifier = entity_id("JO", row["entity_type"], row["name_ar"], f"world-heritage:{row['key']}")
        site_ids[row["key"]] = identifier
        ids[f"site:{row['key']}"] = identifier
        coordinates = {"latitude": row["latitude"], "longitude": row["longitude"], "source_id": row["source_id"]}
        entities.append(entity(identifier, row["name_ar"], row["entity_type"], row["source_id"], row["source_locator"],
                               coordinates=coordinates,
                               notes="Bounded UNESCO World Heritage property entity; kept separate from administrative and populated-place concepts."))
        aliases.append(alias(identifier, row["name_en"], row["source_id"], row["source_locator"], kind="english"))
        relationships.append(relationship(identifier, ids[f"governorate:{row['parent_governorate']}"], "located_in",
                                          row["source_id"], row["source_locator"],
                                          notes="Governorate-level containment only; no unsourced finer administrative parent is asserted."))
        claims.extend([
            claim(identifier, "world_heritage_category", row["category"], row["source_id"], row["source_locator"], classification="official"),
            claim(identifier, "world_heritage_inscription_year", row["inscription_year"], row["source_id"], row["source_locator"], classification="official"),
            claim(identifier, "heritage_scope", row["scope"], row["source_id"], row["source_locator"]),
        ])

    for row in heritage["bounded_populated_places"]["places"]:
        identifier = entity_id("JO", row["entity_type"], row["name_ar"], f"bounded-place:{row['key']}")
        ids[f"place:{row['key']}"] = identifier
        coordinates = {"latitude": row["latitude"], "longitude": row["longitude"], "source_id": row["source_id"]}
        status = row["status"]
        notes = "Bounded populated/historical-place pilot entity; not an administrative unit."
        if status == "historical":
            notes += " The source gives a historical characterization but no exact ISO end date, so valid_to remains null rather than guessed."
        entities.append(entity(identifier, row["name_ar"], row["entity_type"], row["source_id"], row["source_locator"],
                               status=status, coordinates=coordinates, notes=notes))
        aliases.append(alias(identifier, row["name_en"], row["source_id"], row["source_locator"], kind="english"))
        relationships.append(relationship(identifier, ids[f"governorate:{row['parent_governorate']}"], "located_in",
                                          row["source_id"], row["source_locator"], status=status))
        relationships.append(relationship(identifier, site_ids[row["property_key"]], "associated_with",
                                          row["source_id"], row["source_locator"], status=status,
                                          notes="Entity-resolution decision keeps the place concept distinct from the World Heritage property."))
        claims.append(claim(identifier, "place_classification", row["entity_type"], row["source_id"], row["source_locator"],
                            classification="historical" if status == "historical" else "official",
                            status="historical" if status == "historical" else "verified"))

    assert len(site_ids) == 8 and len(heritage["bounded_populated_places"]["places"]) == 4
    return entities, aliases, relationships, claims


def build_cultural(cultural: dict[str, Any], ids: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in cultural["claims"]:
        subject = ids[row["subject_key"]]
        rows.append(claim(subject, row["predicate"], row["value"], row["source_id"], row["source_locator"],
                          classification=row["classification"], status=row["status"], notes=row["notes"]))
    return rows


def denominator(identifier: str, layer: str, value: int, source_id: str, locator: str, license_text: str, *, status: str = "official", notes: str) -> dict[str, Any]:
    return {
        "id": identifier, "schema_version": SCHEMA_VERSION, "country_code": "JO", "layer": layer,
        "definition": notes, "value": value, "as_of": AS_OF, "status": status, "source_id": source_id,
        "source_locator": locator, "license": license_text, "missing_reason": None, "notes": notes,
        "denominator": value, "snapshot_date": AS_OF,
    }


def coverage(identifier: str, layer: str, denominator_id: str, value: int, source_id: str, license_text: str, notes: str) -> dict[str, Any]:
    return {
        "id": identifier, "schema_version": SCHEMA_VERSION, "country_code": "JO", "layer": layer,
        "snapshot_id": SNAPSHOT, "denominator_id": denominator_id, "source_id": source_id,
        "matched": value, "unmatched": 0, "excluded": 0, "missing": 0, "complete": True,
        "missing_reason": None, "notes": notes, "denominator": value, "snapshot_date": AS_OF,
        "license": license_text, "coverage_percentage": 100.0, "exclusion_reasons": [],
    }


def build_coverage() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    legal_locator = "Regulation No. 46 of 2000, Articles 2 and 4–15, after Regulation No. 29 of 2024: 51 liwa/38 qada +4 liwa/−2 qada"
    specs = [
        ("JO-GOVERNORATE-2026", "jo_governorate", 12, AMENDMENT, legal_locator, LEGAL_LICENSE, "official", "All twelve legal governorates in the current amended regulation."),
        ("JO-LIWA-2026", "jo_liwa", 55, AMENDMENT, legal_locator, LEGAL_LICENSE, "official", "All current legal liwa: pre-amendment 51 plus four created/promoted in 2024."),
        ("JO-QADA-2026", "jo_qada", 36, AMENDMENT, legal_locator, LEGAL_LICENSE, "official", "All current subordinate legal qada: pre-amendment 38 less Moab and Bal'ama promoted to liwa."),
        ("JO-WHC-2026", "world_heritage_property", 8, WHC_REGISTER, "Jordan State Party register; all eight linked properties", WHC_LICENSE, "official", "All World Heritage properties on Jordan's State Party register at the snapshot date."),
        ("JO-BOUNDED-PLACES-2026", "bounded_populated_place", 4, WHC_REGISTER, "Eight-property register plus four linked descriptions explicitly classifying a city, town/caravan-city, or rural settlement", WHC_LICENSE, "official", "Closed pilot extraction from the eight in-scope property descriptions; it is not a denominator for all populated places in Jordan."),
    ]
    denominators = []
    coverages = []
    for token, layer, value, source_id, locator, license_text, status, notes in specs:
        den_id = f"DEN-{token}"
        cov_id = f"COV-{token}"
        denominators.append(denominator(den_id, layer, value, source_id, locator, license_text, status=status, notes=notes))
        coverages.append(coverage(cov_id, layer, den_id, value, source_id, license_text,
                                  notes + " Equation closed: matched + excluded = denominator; unmatched and missing are zero."))
    snapshot = {
        "id": SNAPSHOT, "schema_version": SCHEMA_VERSION,
        "title": "Jordan Phase 3 legal hierarchy and bounded content snapshot",
        "captured_at": AS_OF, "source_id": AMENDMENT,
        "scope": "Jordan: 12 governorates, 55 liwa, 36 qada, eight UNESCO World Heritage properties, and four bounded populated/historical places",
        "method": "Offline deterministic import from checksum-bound legal, institutional, entity-resolution, and cultural fixtures; current hierarchy derived by applying Regulation No. 29 of 2024 to Regulation No. 46 of 2000.",
        "checksum": file_sha256(IMPORT / "snapshot_manifest.json"),
        "notes": "Municipalities are a parallel local-administration scope and are not declared complete. DoS statistical qada are not imported as extra legal qada.",
    }
    return denominators, coverages, snapshot


def build_manifest() -> dict[str, Any]:
    legal_sources = [BASELINE, AMENDMENT, GAZETTE]
    hierarchy_common = {
        "temporal_statuses": ["current", "historical", "disputed", "de_facto", "claimed", "proposed", "transitional", "uncertain"],
        "verification_status": "verified",
        "authority_name": "وزارة الداخلية الأردنية / رئاسة الوزراء / ديوان التشريع والرأي",
        "snapshot_date": AS_OF,
        "license": LEGAL_LICENSE,
        "scope_status": "closed",
        "notes": "Current legal hierarchy at the dated snapshot.",
        "special_cases": [],
    }
    hierarchy = [
        {
            "level": 0, "entity_type": "country", "local_names": ["دولة"], "allowed_parent_types": [],
            "temporal_statuses": ["current", "historical", "disputed", "de_facto", "claimed"],
            "source_ids": ["SRC-ISO-3166-1-2020"], "verification_status": "verified",
            "caveat": "One country-scope entity; this is not a local coverage assertion.",
            "authority_name": "International Organization for Standardization", "denominator": 1,
            "denominator_id": "DEN-JO-COUNTRY-SCOPE", "coverage_record_id": "COV-JO-COUNTRY-SCOPE",
            "snapshot_date": AS_OF, "license": "ISO copyright; reuse subject to ISO terms", "scope_status": "closed",
            "notes": "Existing country entity retained.", "special_cases": [],
        },
        {
            **hierarchy_common, "level": 1, "entity_type": "jo_governorate", "local_names": ["محافظة"],
            "allowed_parent_types": ["country"], "source_ids": legal_sources, "denominator": 12,
            "denominator_id": "DEN-JO-GOVERNORATE-2026", "coverage_record_id": "COV-JO-GOVERNORATE-2026",
            "caveat": "Administrative seats are claims, not governorate child entities.",
        },
        {
            **hierarchy_common, "level": 2, "entity_type": "jo_liwa", "local_names": ["لواء"],
            "allowed_parent_types": ["jo_governorate"], "source_ids": legal_sources + [RUWAYSHID], "denominator": 55,
            "denominator_id": "DEN-JO-LIWA-2026", "coverage_record_id": "COV-JO-LIWA-2026",
            "caveat": "Ruwayshid is current but its exact commencement date is not_documented.",
            "special_cases": ["West Irbid, Moab, Mi'rad, and Bal'ama are current from 2024-06-06.", "Petra reports 11 West Irbid towns, while the controlling amendment enumerates ten localities."],
        },
        {
            **hierarchy_common, "level": 3, "entity_type": "jo_qada", "local_names": ["قضاء"],
            "allowed_parent_types": ["jo_liwa"], "source_ids": legal_sources, "denominator": 36,
            "denominator_id": "DEN-JO-QADA-2026", "coverage_record_id": "COV-JO-QADA-2026",
            "caveat": "Only subordinate legal qada are counted; same-name DoS statistical rows are not extra legal qada.",
            "special_cases": ["Moab and Bal'ama are no longer qada after promotion to liwa.", "Article 8 controls Ma'an at four qada; the Ministry summary's 4/7 count is recorded as a conflict and not imported."],
        },
    ]
    pilot_layers = [
        {"layer": "jo_governorate", "entity_types": ["jo_governorate"], "local_names": ["محافظة"], "authority_name": hierarchy_common["authority_name"], "denominator": 12, "denominator_id": "DEN-JO-GOVERNORATE-2026", "coverage_record_id": "COV-JO-GOVERNORATE-2026", "snapshot_date": AS_OF, "source_ids": legal_sources, "license": LEGAL_LICENSE, "scope_status": "closed", "notes": "Current legal layer.", "special_cases": []},
        {"layer": "jo_liwa", "entity_types": ["jo_liwa"], "local_names": ["لواء"], "authority_name": hierarchy_common["authority_name"], "denominator": 55, "denominator_id": "DEN-JO-LIWA-2026", "coverage_record_id": "COV-JO-LIWA-2026", "snapshot_date": AS_OF, "source_ids": legal_sources + [RUWAYSHID], "license": LEGAL_LICENSE, "scope_status": "closed", "notes": "Current legal layer; 51 pre-amendment plus four 2024 creations/promotions.", "special_cases": ["Ruwayshid commencement date not_documented."]},
        {"layer": "jo_qada", "entity_types": ["jo_qada"], "local_names": ["قضاء"], "authority_name": hierarchy_common["authority_name"], "denominator": 36, "denominator_id": "DEN-JO-QADA-2026", "coverage_record_id": "COV-JO-QADA-2026", "snapshot_date": AS_OF, "source_ids": legal_sources, "license": LEGAL_LICENSE, "scope_status": "closed", "notes": "Current subordinate legal qada only.", "special_cases": ["DoS statistical same-name qada excluded from the legal-unit concept."]},
        {"layer": "world_heritage_property", "entity_types": ["archaeological_site", "cultural_site", "natural_site"], "local_names": ["موقع تراث عالمي"], "authority_name": "UNESCO World Heritage Centre", "denominator": 8, "denominator_id": "DEN-JO-WHC-2026", "coverage_record_id": "COV-JO-WHC-2026", "snapshot_date": AS_OF, "source_ids": [WHC_REGISTER] + [f"SRC-UNESCO-WHC-JO-{x}" for x in [689,326,327,1093,1377,1446,1721,1742]], "license": WHC_LICENSE, "scope_status": "closed", "notes": "Every property has an atomic source and published coordinates.", "special_cases": ["Wadi Rum is mixed but represented by the available natural_site type with a mixed-category claim."]},
        {"layer": "bounded_populated_place", "entity_types": ["city", "historical_place"], "local_names": ["مدينة", "مكان تاريخي"], "authority_name": "UNESCO World Heritage Centre", "denominator": 4, "denominator_id": "DEN-JO-BOUNDED-PLACES-2026", "coverage_record_id": "COV-JO-BOUNDED-PLACES-2026", "snapshot_date": AS_OF, "source_ids": ["SRC-UNESCO-WHC-JO-689", "SRC-UNESCO-WHC-JO-326", "SRC-UNESCO-WHC-JO-1093", "SRC-UNESCO-WHC-JO-1721"], "license": WHC_LICENSE, "scope_status": "bounded", "notes": "Closed extraction from descriptions of the eight World Heritage properties; not a national populated-place denominator.", "special_cases": ["Site/property entities remain separate from city and historical-place entities."]},
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "country": {"iso2": "JO", "name_ar": "الأردن", "entity_id": COUNTRY},
        "status": "pilot_migrated",
        "official_authority": {"name": hierarchy_common["authority_name"], "source_ids": legal_sources, "verification_status": "verified", "missing_reason": None},
        "snapshot": {"as_of": AS_OF, "snapshot_id": SNAPSHOT, "status": "verified"},
        "hierarchy": hierarchy,
        "pilot_layers": pilot_layers,
        "coverage_record_ids": ["COV-JO-COUNTRY-SCOPE", "COV-JO-GOVERNORATE-2026", "COV-JO-LIWA-2026", "COV-JO-QADA-2026", "COV-JO-WHC-2026", "COV-JO-BOUNDED-PLACES-2026"],
        "caveats": [
            "Municipalities and special local authorities are parallel scopes and are not declared complete in this pilot.",
            "No national populated-place completeness is claimed; the four-place denominator is explicitly bounded to an eight-property extraction rule.",
            "Dialect scope is not_documented; no lexical entry is imported without the required place, register, study/speaker, date, and form evidence.",
            "The Ministry Ma'an summary and Petra West Irbid report are retained as conflicts but do not override controlling legal clauses.",
        ],
        "next_action": "Maintain dated legal amendments and institutional property registers; do not expand another country under this Jordan pilot.",
    }


def replace_jordan(path: Path, new_rows: list[dict[str, Any]], family: str) -> None:
    old_rows = read_jsonl(path)
    if family == "entities":
        keep = [row for row in old_rows if row.get("country_code") != "JO" or row.get("id") == COUNTRY]
    elif family == "aliases":
        keep = [row for row in old_rows if not row.get("entity_id", "").startswith("ENT-JO-") or row.get("entity_id") == COUNTRY]
    elif family == "relationships":
        keep = [row for row in old_rows if not row.get("child_id", "").startswith("ENT-JO-") and not row.get("parent_id", "").startswith("ENT-JO-")]
    elif family == "claims":
        keep = [row for row in old_rows if not row.get("subject_id", "").startswith("ENT-JO-")]
    else:
        raise ValueError(family)
    write_jsonl(path, keep + new_rows)


def main() -> None:
    hierarchy, heritage, cultural, _resolution = verify_inputs()
    admin_entities, admin_aliases, admin_relationships, admin_claims, ids = build_admin(hierarchy)
    site_entities, site_aliases, site_relationships, site_claims = build_heritage(heritage, ids)
    cultural_claims = build_cultural(cultural, ids)
    denominators, coverages, snapshot = build_coverage()

    replace_jordan(ENTITY_PATH, admin_entities + site_entities, "entities")
    replace_jordan(ALIAS_PATH, admin_aliases + site_aliases, "aliases")
    replace_jordan(REL_PATH, admin_relationships + site_relationships, "relationships")
    replace_jordan(CLAIM_PATH, admin_claims + site_claims + cultural_claims, "claims")

    snapshots = [row for row in read_jsonl(SNAPSHOT_PATH) if row.get("id") != SNAPSHOT]
    write_jsonl(SNAPSHOT_PATH, snapshots + [snapshot])
    old_denominators = [row for row in read_jsonl(DENOM_PATH) if row.get("country_code") != "JO" or row.get("layer") == "country_scope"]
    old_coverages = [row for row in read_jsonl(COVERAGE_PATH) if row.get("country_code") != "JO" or row.get("layer") == "country_scope"]
    write_jsonl(DENOM_PATH, old_denominators + denominators)
    write_jsonl(COVERAGE_PATH, old_coverages + coverages)
    write_json(MANIFEST_PATH, build_manifest())
    write_json(DOMAIN_STATUS_PATH, {
        "schema_version": SCHEMA_VERSION,
        "country_code": "JO",
        "snapshot_date": AS_OF,
        "source_fixture": "data/imports/jordan/cultural_content_2026.json",
        "domains": cultural["domain_status"],
    })

    print(json.dumps({
        "country": "JO",
        "entities_added": len(admin_entities) + len(site_entities),
        "aliases_added": len(admin_aliases) + len(site_aliases),
        "relationships_added": len(admin_relationships) + len(site_relationships),
        "claims_added": len(admin_claims) + len(site_claims) + len(cultural_claims),
        "denominators_added": len(denominators),
        "coverage_added": len(coverages),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
