#!/usr/bin/env python3
"""Deterministically rebuild the Tunisia Phase 2 pilot from committed snapshots.

The importer never reads the network.  It validates every input snapshot before
replacing Tunisia rows and leaves the other 21 countries byte-for-byte equivalent
at the record level.  Re-running it produces the same canonical JSONL.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from model import AS_OF, ROOT, SCHEMA_VERSION, read_jsonl, record_id, write_json, write_jsonl

IMPORT = ROOT / "data/imports/tunisia"
ENTITY_PATH = ROOT / "data/entities/entities.jsonl"
ALIAS_PATH = ROOT / "data/aliases/aliases.jsonl"
REL_PATH = ROOT / "data/relationships/relationships.jsonl"
CLAIM_PATH = ROOT / "data/claims/claims.jsonl"
SNAPSHOT_PATH = ROOT / "data/snapshots/snapshots.jsonl"
DENOM_PATH = ROOT / "data/coverage/denominators.jsonl"
COVERAGE_PATH = ROOT / "data/coverage/coverage.jsonl"
COUNTRY = "ENT-TN-COUNTRY"
OFFICIAL_MUNICIPALITIES = "SRC-TN-DGCL-MUNICIPALITIES-2024"
INSTITUTIONAL_ADMIN = "SRC-TN-HDX-CODAB-2022"
RESEARCH_GEOMETRY = "SRC-TN-RESEARCH-GEOMETRY-2018"
UNESCO_WHC = "SRC-UNESCO-WHC-TN-2026"
UNESCO_ICH = "SRC-UNESCO-ICH-TN-2026"
ONTT = "SRC-TN-ONTT-PLACES-2018"
IBN_SOURCE = "SRC-UNESCO-IBN-KHALDUN"


def load_csv(name: str) -> list[dict[str, str]]:
    with (IMPORT / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def verify_inputs() -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    manifest = json.loads((IMPORT / "snapshot_manifest.json").read_text(encoding="utf-8"))
    for item in manifest["files"]:
        path = ROOT / item["path"]
        payload = path.read_bytes()
        assert len(payload) == item["bytes"], f"byte count changed: {path}"
        assert hashlib.sha256(payload).hexdigest() == item["sha256"], f"checksum changed: {path}"

    municipalities = load_csv("official_municipalities_2024.csv")
    admin = load_csv("institutional_admin_2022.csv")
    overlaps = load_csv("municipality_delegation_overlap_evidence.csv")
    overrides = load_csv("mapping_overrides.csv")
    assert len(municipalities) == 350
    assert len({r["municipality_code"] for r in municipalities}) == 350
    assert len({r["research_mun_uid"] for r in municipalities}) == 350
    assert Counter(r["layer"] for r in admin) == {"governorate": 24, "delegation": 264, "imada": 2084}
    assert len({r["research_code"] for r in admin if r["layer"] == "imada"}) == 2084
    assert len(overlaps) == 2084
    assert len({r["research_sector_code"] for r in overlaps}) == 2084
    assert {r["delegation_2014_code"] for r in overlaps} == {
        r["research_code"] for r in admin if r["layer"] == "delegation"
    }
    expected = {"2223": "105", "2224": "107", "3429": "215", "3432": "219", "3433": "214", "4127": "240", "4129": "236", "5317": "317"}
    assert {r["municipality_code"]: r["research_mun_uid"] for r in overrides} == expected
    assert {r["municipality_code"]: r["research_mun_uid"] for r in municipalities if r["mapping_review"] == "explicit_reviewed_residual"} == expected
    assert all(r["existing_entity_id"] for r in admin if r["layer"] in {"governorate", "delegation"})
    assert len({r["existing_entity_id"] for r in admin if r["layer"] in {"governorate", "delegation"}}) == 288
    return municipalities, admin, overlaps


def entity(identifier: str, name: str, entity_type: str, source_id: str, locator: str, *,
           language: str = "ar", status: str = "current", coordinates: dict[str, Any] | None = None,
           notes: str | None = None, confidence: str = "high", verification: str = "verified") -> dict[str, Any]:
    return {
        "id": identifier, "schema_version": SCHEMA_VERSION, "country_code": "TN",
        "canonical_name": name, "canonical_name_language": language, "entity_type": entity_type,
        "status": status, "valid_from": None, "valid_to": None,
        "canonical_source_id": source_id, "source_locator": locator,
        "legacy_ids": [], "coordinates": coordinates, "notes": notes,
        "verification_status": verification, "confidence": confidence,
    }


def alias(entity_id: str, name: str, language: str, source_id: str, locator: str, *, kind: str = "alternative") -> dict[str, Any]:
    return {
        "id": record_id("ALS", entity_id, language, kind, name), "schema_version": SCHEMA_VERSION,
        "entity_id": entity_id, "name": name, "language": language,
        "script": "Arab" if language == "ar" else "Latn", "kind": kind,
        "status": "current", "source_id": source_id, "source_locator": locator,
        "valid_from": None, "valid_to": None,
    }


def relationship(child: str, parent: str, rel_type: str, source_id: str, locator: str, *,
                 status: str = "current", notes: str | None = None,
                 confidence: str = "high", verification: str = "verified") -> dict[str, Any]:
    return {
        "id": record_id("REL", child, parent, rel_type), "schema_version": SCHEMA_VERSION,
        "child_id": child, "parent_id": parent, "relationship_type": rel_type,
        "status": status, "valid_from": None, "valid_to": None,
        "source_id": source_id, "source_locator": locator, "notes": notes,
        "verification_status": verification, "confidence": confidence,
    }


def claim(subject: str, predicate: str, value: Any, source_id: str, locator: str, *,
          classification: str | None = None, status: str = "verified", confidence: str = "high",
          notes: str | None = None, second_source_id: str | None = None,
          second_locator: str | None = None, sensitivity: str = "ordinary") -> dict[str, Any]:
    return {
        "id": record_id("CLM", subject, predicate, json.dumps(value, ensure_ascii=False, sort_keys=True)),
        "schema_version": SCHEMA_VERSION, "subject_id": subject, "predicate": predicate,
        "value": {"type": ("boolean" if isinstance(value, bool) else "integer" if isinstance(value, int) else "number" if isinstance(value, float) else "string"), "data": value},
        "unit": None, "status": status, "observed_at": None, "valid_from": None, "valid_to": None,
        "source_id": source_id, "second_source_id": second_source_id,
        "source_locator": locator, "second_source_locator": second_locator,
        "sensitivity": sensitivity, "notes": notes, "verification_status": "verified",
        "confidence": confidence, "classification": classification, "published": True,
        "lexical_context": None,
    }


def coords(row: dict[str, str], source: str = RESEARCH_GEOMETRY) -> dict[str, Any] | None:
    if not row.get("latitude") or not row.get("longitude"):
        return None
    return {"latitude": float(row["latitude"]), "longitude": float(row["longitude"]), "source_id": source}


def build_core(municipalities: list[dict[str, str]], admin: list[dict[str, str]],
               overlaps: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    entities: list[dict[str, Any]] = []
    aliases: list[dict[str, Any]] = []
    rels: list[dict[str, Any]] = []
    rows_by_layer = {layer: [r for r in admin if r["layer"] == layer] for layer in ("governorate", "delegation", "imada")}
    id_by_code: dict[str, str] = {}

    for row in rows_by_layer["governorate"]:
        identifier = row["existing_entity_id"]
        id_by_code[row["research_code"]] = identifier
        entities.append(entity(identifier, row["name_ar"], "tn_governorate", INSTITUTIONAL_ADMIN,
                               row["source_locator"], coordinates=coords(row),
                               notes="Dated COD-AB record valid from 2022-11-15; coordinates are approximate Tier C centroids."))
        if row["name_fr"].casefold() != row["name_ar"].casefold():
            aliases.append(alias(identifier, row["name_fr"], "fr", INSTITUTIONAL_ADMIN, row["source_locator"], kind="official_variant"))
        rels.append(relationship(identifier, COUNTRY, "administrative_parent", INSTITUTIONAL_ADMIN, row["source_locator"]))

    for row in rows_by_layer["delegation"]:
        identifier = row["existing_entity_id"]
        id_by_code[row["research_code"]] = identifier
        entities.append(entity(identifier, row["name_ar"], "tn_delegation", INSTITUTIONAL_ADMIN,
                               row["source_locator"], coordinates=coords(row),
                               notes="Dated COD-AB record valid from 2022-11-15; coordinates are approximate Tier C centroids."))
        aliases.append(alias(identifier, row["name_fr"], "fr", INSTITUTIONAL_ADMIN, row["source_locator"], kind="official_variant"))
        rels.append(relationship(identifier, id_by_code[row["parent_research_code"]], "administrative_parent", INSTITUTIONAL_ADMIN, row["source_locator"]))

    for row in rows_by_layer["imada"]:
        identifier = f"ENT-TN-IMADA-{row['research_code']}"
        id_by_code[row["research_code"]] = identifier
        entities.append(entity(identifier, row["name_ar"], "tn_imada", INSTITUTIONAL_ADMIN,
                               row["source_locator"], coordinates=coords(row),
                               notes="Dated imada/sector record valid from 2022-11-15; coordinates are approximate Tier C centroids."))
        aliases.append(alias(identifier, row["name_fr"], "fr", INSTITUTIONAL_ADMIN, row["source_locator"], kind="official_variant"))
        rels.append(relationship(identifier, id_by_code[row["parent_research_code"]], "administrative_parent", INSTITUTIONAL_ADMIN, row["source_locator"]))

    gov_id = {r["research_code"]: r["existing_entity_id"] for r in rows_by_layer["governorate"]}
    mun_by_uid: dict[str, str] = {}
    for row in municipalities:
        identifier = f"ENT-TN-MUNICIPALITY-{row['municipality_code']}"
        mun_by_uid[row["research_mun_uid"]] = identifier
        entities.append(entity(identifier, row["official_name_ar"], "tn_municipality", OFFICIAL_MUNICIPALITIES,
                               row["source_locator"], coordinates=coords(row),
                               notes=("Official January 2024 register. Approximate Tier C centroid; reviewed mapping status: "
                                      + row["mapping_review"]),
                               confidence="medium" if row["mapping_review"] == "explicit_reviewed_residual" else "high",
                               verification="source_verified" if row["mapping_review"] == "explicit_reviewed_residual" else "verified"))
        aliases.append(alias(identifier, row["official_name_fr"], "fr", OFFICIAL_MUNICIPALITIES, row["source_locator"], kind="official_variant"))
        rels.append(relationship(identifier, gov_id[row["governorate_code"]], "administrative_parent",
                                 OFFICIAL_MUNICIPALITIES, row["source_locator"]))

    evidence: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in overlaps:
        evidence[(row["research_mun_uid"], row["delegation_2014_code"])].append(row["research_sector_code"])
    for (uid, delegation_code), sectors in sorted(evidence.items(), key=lambda item: (int(item[0][0]), item[0][1])):
        locator = f"sector evidence rows: {','.join(sorted(sectors))}"
        rels.append(relationship(mun_by_uid[uid], id_by_code[delegation_code], "boundary_intersects",
                                 RESEARCH_GEOMETRY, locator,
                                 notes="Approximate research topology only; this is not an administrative parent relationship.",
                                 confidence="medium", verification="source_verified"))
    return entities, aliases, rels


PLACE_ROWS = [
    # id, Arabic, type, English, French, container, source, source locator, optional coordinates
    ("ENT-TN-CITY-CARTHAGE", "قرطاج", "city", "Carthage", "Carthage", "ENT-TN-MUNICIPALITY-1115", ONTT, "Around Carthage and Sidi Bou Said: modern Carthage described as a fashionable city", None),
    ("ENT-TN-CITY-SOUSSE", "سوسة", "city", "Sousse", "Sousse", "ENT-TN-MUNICIPALITY-3111", ONTT, "Around Sousse and Port El Kantaoui: Sousse is Tunisia's third biggest city", None),
    ("ENT-TN-VILLAGE-SIDI-BOU-SAID", "سيدي بوسعيد", "village", "Sidi Bou Said", "Sidi Bou Saïd", "ENT-TN-MUNICIPALITY-1116", UNESCO_WHC, "World Heritage property 1769: Village of Sidi Bou Saïd", (36.871028, 10.348639)),
    ("ENT-TN-VILLAGE-EL-JEM", "الجم", "village", "El Jem", "El Jem", "ENT-TN-MUNICIPALITY-3318", UNESCO_WHC, "World Heritage property 38: small village of El Jem", None),
    ("ENT-TN-SITE-MAGON", "حي ماغون الأثري", "archaeological_site", "Magon archaeological quarter", "Quartier archéologique Magon", "ENT-TN-SITE-CARTHAGE", ONTT, "Around Carthage and Sidi Bou Said: remains of the Magon quarter", None),
    ("ENT-TN-HISTORICAL-PLACE-KERKUANE", "كركوان", "historical_place", "Kerkuane", "Kerkouane", "ENT-TN-GOVERNORATE-EA30E853F598", UNESCO_WHC, "World Heritage property 332: Punic Town of Kerkuane", (36.9464, 11.0992)),
    ("ENT-TN-VILLAGE-SEJNANE", "سجنان", "village", "Sejnane", "Sejnane", "ENT-TN-GOVERNORATE-B1787F907937", UNESCO_ICH, "ICH element 01406: the village of Sejnane", None),
]

SITE_ROWS = [
    # id, ar, type, en, fr, container, coordinate, period, condition, protection, locator
    ("ENT-TN-SITE-MEDINA-TUNIS", "مدينة تونس العتيقة", "cultural_site", "Medina of Tunis", "Médina de Tunis", "ENT-TN-MUNICIPALITY-1111", (36.8164, 10.1700), "Islamic city founded in 698; major Almohad and Hafsid period", "Historic urban fabric with numerous monuments", "UNESCO World Heritage property, inscribed 1979", "World Heritage property 36"),
    ("ENT-TN-SITE-CARTHAGE", "موقع قرطاج الأثري", "archaeological_site", "Archaeological Site of Carthage", "Site archéologique de Carthage", "ENT-TN-MUNICIPALITY-1115", (36.8528, 10.3233), "Phoenician foundation traditionally dated to the 9th century BCE; later Roman city", "Dispersed archaeological remains", "UNESCO World Heritage property, inscribed 1979", "World Heritage property 37"),
    ("ENT-TN-SITE-AMPHITHEATRE-EL-JEM", "مدرج الجم", "landmark", "Amphitheatre of El Jem", "Amphithéâtre d’El Jem", "ENT-TN-MUNICIPALITY-3318", (35.2964, 10.7069), "Third century CE Roman amphitheatre", "Monumental stone amphitheatre remains", "UNESCO World Heritage property, inscribed 1979", "World Heritage property 38"),
    ("ENT-TN-SITE-ICHKEUL", "الحديقة الوطنية بإشكل", "natural_site", "Ichkeul National Park", "Parc national de l’Ichkeul", "ENT-TN-GOVERNORATE-B1787F907937", (37.1636, 9.6747), "Natural wetland and lake ecosystem", "Integrity depends on freshwater inflow; restoration and monitoring documented", "National park and UNESCO World Heritage property, inscribed 1980", "World Heritage property 8"),
    ("ENT-TN-SITE-KERKUANE", "مدينة كركوان البونية", "archaeological_site", "Punic Town of Kerkuane and its Necropolis", "Cité punique de Kerkouane et sa nécropole", "ENT-TN-GOVERNORATE-EA30E853F598", (36.9464, 11.0992), "Punic city abandoned during the First Punic War, about 250 BCE", "Archaeological town and necropolis remains", "UNESCO World Heritage property, inscribed 1985", "World Heritage property 332"),
    ("ENT-TN-SITE-KAIROUAN", "مدينة القيروان التاريخية", "cultural_site", "Kairouan", "Kairouan", "ENT-TN-MUNICIPALITY-4111", (35.6814, 10.1044), "Founded in 670 CE", "Historic medina and major monuments", "UNESCO World Heritage property, inscribed 1988", "World Heritage property 499"),
    ("ENT-TN-SITE-MEDINA-SOUSSE", "مدينة سوسة العتيقة", "cultural_site", "Medina of Sousse", "Médina de Sousse", "ENT-TN-MUNICIPALITY-3111", (35.8278, 10.6386), "Early Islamic coastal town, particularly 9th century", "Fortified medina fabric and monuments", "UNESCO World Heritage property, inscribed 1988", "World Heritage property 498"),
    ("ENT-TN-SITE-DOUGGA", "دقّة", "archaeological_site", "Dougga / Thugga", "Dougga / Thugga", "ENT-TN-MUNICIPALITY-2115", (36.4236, 9.2203), "Numidian settlement and Romanized town", "Extensive archaeological ruins retaining urban components", "UNESCO World Heritage property, inscribed 1997; protected under national heritage law", "World Heritage property 794 and maps"),
    ("ENT-TN-SITE-DJERBA", "جربة: شاهد على نمط تعمير", "cultural_site", "Djerba: Testimony to a settlement pattern in an island territory", "Djerba : témoignage d’un mode d’occupation d’un territoire insulaire", "ENT-TN-GOVERNORATE-902616FE3988", (33.8070, 10.8500), "Island settlement pattern documented from around the 9th century", "Dispersed island cultural landscape", "UNESCO World Heritage property, inscribed 2023", "World Heritage property 1640"),
    ("ENT-TN-SITE-SIDI-BOU-SAID", "قرية سيدي بوسعيد", "cultural_site", "Village of Sidi Bou Saïd", "Village de Sidi Bou Saïd", "ENT-TN-MUNICIPALITY-1116", (36.871028, 10.348639), "Settlement developed around the tomb of the Sufi master Sidi Bou Said in the 13th century", "Picturesque cliff-top village whose architecture and urban planning integrate with its natural environment", "UNESCO World Heritage property, inscribed 2026", "World Heritage property 1769"),
]


def build_pilot() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    entities: list[dict[str, Any]] = []
    aliases: list[dict[str, Any]] = []
    rels: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    for identifier, ar, place_type, en, fr, container, source, locator, point in PLACE_ROWS:
        coordinates = ({"latitude": point[0], "longitude": point[1], "source_id": source}
                       if point is not None else None)
        notes = ("Bounded populated-place pilot entity; not an administrative entity."
                 if place_type in {"city", "town", "village", "settlement", "neighborhood", "historical_place"}
                 else "Bounded archaeological entity; not a current neighborhood or administrative entity.")
        entities.append(entity(identifier, ar, place_type, source, locator,
                               coordinates=coordinates, notes=notes))
        aliases.append(alias(identifier, en, "en", source, locator, kind="english"))
        if fr != en:
            aliases.append(alias(identifier, fr, "fr", source, locator, kind="official_variant"))
        rels.append(relationship(identifier, container, "located_in", source, locator))
        claims.append(claim(identifier, "place_classification", place_type, source, locator, classification="official"))

    for identifier, ar, site_type, en, fr, container, point, period, condition, protection, locator in SITE_ROWS:
        entities.append(entity(identifier, ar, site_type, UNESCO_WHC, locator,
                               coordinates={"latitude": point[0], "longitude": point[1], "source_id": UNESCO_WHC},
                               notes="Site entity kept separate from any administrative or populated-place entity."))
        aliases.append(alias(identifier, en, "en", UNESCO_WHC, locator, kind="english"))
        if fr != en:
            aliases.append(alias(identifier, fr, "fr", UNESCO_WHC, locator, kind="official_variant"))
        rels.append(relationship(identifier, container, "located_in", UNESCO_WHC, locator))
        claims.extend([
            claim(identifier, "period", period, UNESCO_WHC, locator, classification="historical"),
            claim(identifier, "condition", condition, UNESCO_WHC, locator),
            claim(identifier, "protection_status", protection, UNESCO_WHC, locator, classification="official"),
        ])

    market = "ENT-TN-MARKET-MEDINA-CENTRAL-SOUKS"
    market_locator = "Around Tunis: central souks of the medina; Souk Medina attraction page"
    entities.append(entity(market, "أسواق مدينة تونس المركزية", "market", ONTT, market_locator,
                           coordinates=None,
                           notes="Bounded market entity, not a municipality or neighborhood; no coordinate is published without a source locator for the point."))
    aliases.extend([
        alias(market, "Central Souks of the Medina of Tunis", "en", ONTT, market_locator, kind="english"),
        alias(market, "Souks centraux de la médina de Tunis", "fr", ONTT, market_locator, kind="official_variant"),
    ])
    rels.append(relationship(market, "ENT-TN-MUNICIPALITY-1111", "located_in", ONTT, market_locator))
    claims.extend([
        claim(market, "market_character", "Covered streets historically organized by trade and craft", ONTT, market_locator, classification="historical"),
        claim(market, "traditional_clothing_goods", "Traditional clothing and chechias are among the goods described in the souks", ONTT, market_locator, classification="popular"),
        claim(market, "protection_context", "Located within the Medina of Tunis World Heritage property", UNESCO_WHC, "World Heritage property 36", classification="official"),
    ])

    person = "ENT-TN-PERSON-IBN-KHALDUN"
    person_locator = "UNESCO Courier, 1986-01, pp. 17–18; p. 17: Tunisian historian born in 1332"
    entities.append(entity(person, "ابن خلدون", "person", IBN_SOURCE, person_locator, status="historical",
                           notes="Person entity with an explicitly sourced Tunis connection."))
    aliases.extend([
        alias(person, "Ibn Khaldun", "en", IBN_SOURCE, person_locator, kind="english"),
        alias(person, "Ibn Khaldoun", "fr", IBN_SOURCE, person_locator, kind="alternative"),
    ])
    rels.append(relationship(person, "ENT-TN-MUNICIPALITY-1111", "associated_with", IBN_SOURCE, person_locator, status="historical"))
    claims.extend([
        claim(person, "place_connection", "Born in Tunis in 1332", IBN_SOURCE, person_locator, classification="historical"),
        claim(person, "significance", "Historian and author whose work developed a major analysis of society and history", IBN_SOURCE, "UNESCO Courier, 1986-01, p. 17: principal work and theory of society and history", classification="historical"),
    ])

    kerkennah = "ENT-TN-NATURAL-SITE-KERKENNAH-ISLANDS"
    kerkennah_locator = "ICH element 01566: Kerkennah Islands and the entire local community"
    entities.append(entity(kerkennah, "جزر قرقنة", "natural_site", UNESCO_ICH, kerkennah_locator,
                           coordinates=None,
                           notes="Geographic island-group scope for the sourced practice; not a legal municipality."))
    aliases.extend([
        alias(kerkennah, "Kerkennah Islands", "en", UNESCO_ICH, kerkennah_locator, kind="english"),
        alias(kerkennah, "Îles Kerkennah", "fr", UNESCO_ICH, kerkennah_locator, kind="official_variant"),
    ])
    rels.append(relationship(kerkennah, COUNTRY, "located_in", UNESCO_ICH, kerkennah_locator))

    claims.extend([
        claim("ENT-TN-VILLAGE-SEJNANE", "craft_practice", "Pottery skills of the women of Sejnane", UNESCO_ICH,
              "ICH element 01406: women from the Sejnane community and village", classification="regional"),
        claim(kerkennah, "custom_practice", "Charfia fishing in the Kerkennah Islands", UNESCO_ICH,
              kerkennah_locator, classification="regional"),
        claim(COUNTRY, "food_practice", "Harissa knowledge, skills and culinary and social practices", UNESCO_ICH,
              "ICH element 01710: Tunisia", classification="popular"),
    ])
    return entities, aliases, rels, claims


def coverage_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    denoms = [r for r in read_jsonl(DENOM_PATH) if r["country_code"] != "TN"]
    coverage = [r for r in read_jsonl(COVERAGE_PATH) if r["country_code"] != "TN"]
    snapshots = [r for r in read_jsonl(SNAPSHOT_PATH) if r["id"] not in {
        "SNP-TN-CODAB-2022-11-15", "SNP-TN-MUNICIPALITIES-2024-01", "SNP-TN-UNESCO-WHC-2026-08-15"
    }]
    snapshots.extend([
        {"id": "SNP-TN-CODAB-2022-11-15", "schema_version": SCHEMA_VERSION, "title": "Tunisia COD-AB v01 dated administrative snapshot", "captured_at": "2022-11-15", "source_id": INSTITUTIONAL_ADMIN, "scope": "24 governorates, 264 delegations, and 2,084 imadas", "method": "Deterministic reconstruction from rendered institutional workbook, metadata totals, and reviewed transcription", "checksum": "sha256:7edfdf49eeb93d1cd7c1443f2fec0a57ade847bae2b08450cc3d99138d5ddac9", "notes": "Checksum is for the committed reconstructed CSV, not the unavailable upstream XLSX bytes."},
        {"id": "SNP-TN-MUNICIPALITIES-2024-01", "schema_version": SCHEMA_VERSION, "title": "Tunisia official municipality register, January 2024", "captured_at": "2024-01-01", "source_id": OFFICIAL_MUNICIPALITIES, "scope": "350 coded municipalities", "method": "Deterministic transcription of official bilingual workbook with reviewed one-to-one geometry links", "checksum": "sha256:b53d328fca053c49c1ee46b6b9e95bfe8cb7ca4a41abc81ce9c37bfe918fe1ad", "notes": "Date is month precision normalized to its first day. Checksum is for the committed reconstructed CSV."},
        {"id": "SNP-TN-UNESCO-WHC-2026-08-15", "schema_version": SCHEMA_VERSION, "title": "UNESCO World Heritage properties in Tunisia", "captured_at": AS_OF, "source_id": UNESCO_WHC, "scope": "Ten World Heritage properties listed for Tunisia", "method": "State Party list count and individual property records", "checksum": None, "notes": "Live institutional register retrieved on the snapshot date."},
    ])

    definitions = [
        ("COUNTRY-SCOPE", "country_scope", 1, AS_OF, "SRC-ISO-3166-1-2020", "ISO copyright; reuse is subject to ISO terms of use", "ISO country entity in the project's 22-country scope", "SNP-MIGRATION-2026-08-15", 1, None),
        ("GOVERNORATES", "governorates", 24, "2022-11-15", INSTITUTIONAL_ADMIN, "Creative Commons Attribution 3.0 IGO", "Governorates in COD-AB v01 valid from 2022-11-15", "SNP-TN-CODAB-2022-11-15", 24, None),
        ("DELEGATIONS", "delegations", 264, "2022-11-15", INSTITUTIONAL_ADMIN, "Creative Commons Attribution 3.0 IGO", "Delegations in COD-AB v01 valid from 2022-11-15", "SNP-TN-CODAB-2022-11-15", 264, None),
        ("IMADAS", "imadas", 2084, "2022-11-15", INSTITUTIONAL_ADMIN, "Creative Commons Attribution 3.0 IGO", "Imadas/sectors in COD-AB v01 valid from 2022-11-15", "SNP-TN-CODAB-2022-11-15", 2084, None),
        ("MUNICIPALITIES-2024", "municipalities", 350, "2024-01-01", OFFICIAL_MUNICIPALITIES, "Resource-specific license not stated; factual register transcription only", "Coded municipalities in the January 2024 official register", "SNP-TN-MUNICIPALITIES-2024-01", 350, None),
        ("WORLD-HERITAGE-2026", "world_heritage_properties", 10, AS_OF, UNESCO_WHC, "CC BY-SA 3.0 IGO for property descriptions", "World Heritage properties on UNESCO's Tunisia State Party list", "SNP-TN-UNESCO-WHC-2026-08-15", 10, None),
        ("CITIES", "cities", None, AS_OF, ONTT, "Copyright ONTT; factual extraction only", "National register of places explicitly classified as cities", "SNP-MIGRATION-2026-08-15", 2, "No dated official national city denominator was found; two sourced cities are a bounded pilot and no completion is claimed."),
        ("POPULATED-PLACES", "populated_places", None, AS_OF, ONTT, "Copyright ONTT; factual extraction only", "National register of cities, towns, villages, settlements, neighborhoods, and historical places", "SNP-MIGRATION-2026-08-15", 6, "No dated official national populated-place denominator was found; six sourced populated or historical places form a bounded pilot only."),
    ]
    for suffix, layer, value, date, source, license_text, definition, snapshot, matched, reason in definitions:
        did = f"DEN-TN-{suffix}"
        status = "official" if value is not None else "unavailable"
        denoms.append({
            "id": did, "schema_version": SCHEMA_VERSION, "country_code": "TN", "layer": layer,
            "definition": definition, "value": value, "denominator": value, "status": status,
            "as_of": date, "snapshot_date": date, "source_id": source,
            "source_locator": definition, "license": license_text, "missing_reason": reason,
            "notes": None,
        })
        unmatched = 0
        excluded = 0
        complete = value is not None and matched + excluded == value
        pct = round((matched + excluded) * 100 / value, 2) if value else None
        coverage.append({
            "id": f"COV-TN-{suffix}", "schema_version": SCHEMA_VERSION, "country_code": "TN",
            "layer": layer, "snapshot_id": snapshot, "snapshot_date": date,
            "denominator_id": did, "denominator": value, "source_id": source, "license": license_text,
            "matched": matched, "unmatched": unmatched, "excluded": excluded,
            "exclusion_reasons": [], "missing": (value - matched - excluded) if value is not None else None,
            "coverage_percentage": pct, "complete": complete, "missing_reason": reason,
            "notes": ("Completion means matched + excluded equals this dated denominator only."
                      if complete else "Bounded pilot count; not a national coverage percentage."),
        })
    return denoms, coverage, snapshots


def mirror_coverage_fields(denoms: list[dict[str, Any]], coverage: list[dict[str, Any]], snapshots: list[dict[str, Any]]) -> None:
    """Backfill explicit layer fields on accepted Phase 0/1 records too."""
    source_licenses = {json.loads(p.read_text(encoding="utf-8"))["id"]: json.loads(p.read_text(encoding="utf-8"))["license"] for p in (ROOT / "data/sources").glob("*.json")}
    snapshot_dates = {r["id"]: r["captured_at"] for r in snapshots}
    by_denom = {r["id"]: r for r in denoms}
    for d in denoms:
        d.setdefault("denominator", d.get("value"))
        d.setdefault("snapshot_date", d.get("as_of"))
    for c in coverage:
        d = by_denom[c["denominator_id"]]
        value = d.get("value")
        c["denominator"] = value
        c["snapshot_date"] = snapshot_dates[c["snapshot_id"]]
        c["license"] = source_licenses.get(c.get("source_id")) if c.get("source_id") else d["license"]
        c.setdefault("exclusion_reasons", [])
        if c.get("excluded", 0) and not c["exclusion_reasons"]:
            c["exclusion_reasons"] = [{"count": c["excluded"], "reason": "Legacy rows were retained in quarantine because they lack an atomic canonical source; these are audit exclusions, not evidence of a national denominator."}]
        if value is None:
            c["coverage_percentage"] = None
            c["complete"] = False
            c["missing"] = None
        else:
            c["missing"] = value - c["matched"] - c["excluded"]
            c["unmatched"] = c["missing"]
            completed = c["matched"] + c["excluded"]
            c["coverage_percentage"] = round(completed * 100 / value, 2) if value else (100.0 if completed == 0 else None)
            c["complete"] = completed == value
        c.pop("coverage_percent", None)


def update_manifest() -> None:
    path = ROOT / "manifests/TN.yml"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["status"] = "pilot_migrated"
    manifest["official_authority"] = {
        "name": "المعهد الوطني للإحصاء / بوابة الجماعات المحلية / OCHA HDX",
        "source_ids": [INSTITUTIONAL_ADMIN, OFFICIAL_MUNICIPALITIES],
        "verification_status": "verified", "missing_reason": None,
    }
    manifest["snapshot"] = {"as_of": AS_OF, "snapshot_id": "SNP-TN-CODAB-2022-11-15", "status": "verified"}
    temporal = ["current", "historical", "destroyed", "displaced", "disputed", "de_facto", "claimed", "proposed", "transitional", "uncertain"]
    manifest["hierarchy"] = [
        {"level": 0, "entity_type": "country", "local_names": ["دولة"], "allowed_parent_types": [], "temporal_statuses": temporal, "source_ids": ["SRC-ISO-3166-1-2020"], "verification_status": "verified", "caveat": "Country scope only."},
        {"level": 1, "entity_type": "tn_governorate", "local_names": ["ولاية"], "allowed_parent_types": ["country"], "temporal_statuses": temporal, "source_ids": [INSTITUTIONAL_ADMIN], "verification_status": "verified", "caveat": "Dated COD-AB v01 layer valid from 2022-11-15."},
        {"level": 2, "entity_type": "tn_delegation", "local_names": ["معتمدية"], "allowed_parent_types": ["tn_governorate"], "temporal_statuses": temporal, "source_ids": [INSTITUTIONAL_ADMIN], "verification_status": "verified", "caveat": "Dated 264-row layer; no claim about later delegation counts."},
        {"level": 3, "entity_type": "tn_imada", "local_names": ["عمادة", "قطاع ترابي"], "allowed_parent_types": ["tn_delegation"], "temporal_statuses": temporal, "source_ids": [INSTITUTIONAL_ADMIN], "verification_status": "verified", "caveat": "Dated 2,084-row reusable institutional layer; no claim that it is the current 2026 register."},
        {"level": 3, "entity_type": "tn_municipality", "local_names": ["بلدية"], "allowed_parent_types": ["tn_governorate"], "temporal_statuses": temporal, "source_ids": [OFFICIAL_MUNICIPALITIES], "verification_status": "verified", "caveat": "Municipalities overlap delegations; boundary_intersects is used instead of a false singular delegation parent."},
    ]
    manifest["coverage_record_ids"] = [
        "COV-TN-COUNTRY-SCOPE", "COV-TN-GOVERNORATES", "COV-TN-DELEGATIONS",
        "COV-TN-IMADAS", "COV-TN-MUNICIPALITIES-2024", "COV-TN-WORLD-HERITAGE-2026",
        "COV-TN-CITIES", "COV-TN-POPULATED-PLACES",
    ]
    manifest["caveats"] = [
        "All complete percentages are limited to the named dated denominator and source.",
        "Municipality coordinates and boundary intersections are approximate Tier C research evidence.",
        "Populated places and cultural domains are bounded sourced pilots with no national denominator.",
    ]
    manifest["next_action"] = "Hold expansion outside Tunisia until the Phase 2 Tunisia gate is independently reviewed and accepted."
    write_json(path, manifest)


def write_domain_status() -> None:
    write_json(ROOT / "data/cultural/tunisia_domain_status.json", {
        "schema_version": SCHEMA_VERSION, "country_code": "TN", "as_of": AS_OF,
        "scope": "Bounded Phase 2 pilot; absence statuses are research-workflow states, not claims that a practice does not exist.",
        "domains": [
            {"domain": "food", "status": "documented", "claim_ids": [record_id("CLM", COUNTRY, "food_practice", json.dumps("Harissa knowledge, skills and culinary and social practices", ensure_ascii=False, sort_keys=True))], "notes": "National claim only; not copied to localities."},
            {"domain": "clothing", "status": "documented", "claim_ids": [record_id("CLM", "ENT-TN-MARKET-MEDINA-CENTRAL-SOUKS", "traditional_clothing_goods", json.dumps("Traditional clothing and chechias are among the goods described in the souks", ensure_ascii=False, sort_keys=True))], "notes": "Market-goods claim only."},
            {"domain": "custom", "status": "documented", "claim_ids": [record_id("CLM", "ENT-TN-NATURAL-SITE-KERKENNAH-ISLANDS", "custom_practice", json.dumps("Charfia fishing in the Kerkennah Islands", ensure_ascii=False, sort_keys=True))], "notes": "Attached to the sourced island-group/community geography, not a legal municipality."},
            {"domain": "craft", "status": "documented", "claim_ids": [record_id("CLM", "ENT-TN-VILLAGE-SEJNANE", "craft_practice", json.dumps("Pottery skills of the women of Sejnane", ensure_ascii=False, sort_keys=True))], "notes": "Attached to the sourced village/community, not municipal boundaries."},
            {"domain": "lexical", "status": "not_found", "claim_ids": [], "notes": "No Phase 2-ready A/B source with form, meaning, place, register, date, and study/speaker metadata was identified in the bounded review; no lexical claim is published."},
            {"domain": "dialect", "status": "not_documented", "claim_ids": [], "notes": "Language, dialect, variety, and register remain distinct schema fields; no locality claim is inferred."},
            {"domain": "exclusive_local_practices", "status": "N/A", "claim_ids": [], "notes": "No comparative evidence was reviewed, so no exclusivity claim is in scope."},
        ],
    })


def main() -> None:
    municipalities, admin, overlaps = verify_inputs()
    country_rows = [r for r in read_jsonl(ENTITY_PATH) if r["id"] == COUNTRY]
    assert len(country_rows) == 1
    country_rows[0]["verification_status"] = "verified"
    country_rows[0]["confidence"] = "high"
    core_e, core_a, core_r = build_core(municipalities, admin, overlaps)
    pilot_e, pilot_a, pilot_r, pilot_c = build_pilot()

    entities = [r for r in read_jsonl(ENTITY_PATH) if r["country_code"] != "TN"] + country_rows + core_e + pilot_e
    aliases = [r for r in read_jsonl(ALIAS_PATH) if not r["entity_id"].startswith("ENT-TN-")] + core_a + pilot_a
    rels = [r for r in read_jsonl(REL_PATH) if not r["child_id"].startswith("ENT-TN-")] + core_r + pilot_r
    non_tn_claims = [r for r in read_jsonl(CLAIM_PATH) if not r["subject_id"].startswith("ENT-TN-")]
    phase1_population = read_jsonl(IMPORT / "phase1_population_claims.jsonl")
    assert len(phase1_population) == 24 and all(r["predicate"] == "population" for r in phase1_population)
    claims = non_tn_claims + phase1_population + pilot_c

    denoms, coverage, snapshots = coverage_records()
    mirror_coverage_fields(denoms, coverage, snapshots)
    write_jsonl(ENTITY_PATH, entities)
    write_jsonl(ALIAS_PATH, aliases)
    write_jsonl(REL_PATH, rels)
    write_jsonl(CLAIM_PATH, claims)
    write_jsonl(DENOM_PATH, denoms)
    write_jsonl(COVERAGE_PATH, coverage)
    write_jsonl(SNAPSHOT_PATH, snapshots)
    update_manifest()
    write_domain_status()
    print(json.dumps({
        "tunisia_entities": sum(r["country_code"] == "TN" for r in entities),
        "governorates": sum(r["entity_type"] == "tn_governorate" for r in entities),
        "delegations": sum(r["entity_type"] == "tn_delegation" for r in entities),
        "imadas": sum(r["entity_type"] == "tn_imada" for r in entities),
        "municipalities": sum(r["entity_type"] == "tn_municipality" for r in entities),
        "populated_places": sum(r["entity_type"] in {"city", "town", "village", "settlement", "neighborhood", "historical_place"} for r in entities if r["country_code"] == "TN"),
        "sites": sum(r["entity_type"] in {"archaeological_site", "market", "landmark", "natural_site", "cultural_site"} for r in entities if r["country_code"] == "TN"),
        "claims": sum(r["subject_id"].startswith("ENT-TN-") for r in claims),
    }, indent=2))


if __name__ == "__main__":
    main()
