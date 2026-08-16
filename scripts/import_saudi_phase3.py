#!/usr/bin/env python3
"""Deterministic Saudi Arabia phase-3 parser and importer.

Administrative scope is parsed only from the checksum-verified local HTML set. The
141 governorate rows and 1,523 center occurrences are source-row registries, not a
claim that conflicting current-national aggregates have been reconciled.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from model import ROOT, SCHEMA_VERSION, read_jsonl, write_json, write_jsonl

AS_OF = "2026-08-15"
IMPORT_DIR = ROOT / "data/imports/saudi"
RAW_DIR = IMPORT_DIR / "raw" / AS_OF
SNAPSHOT_MANIFEST = IMPORT_DIR / "snapshot_manifest.json"
CULTURAL_FIXTURE = IMPORT_DIR / "cultural_content_2026.json"

ENTITY_PATH = ROOT / "data/entities/entities.jsonl"
ALIAS_PATH = ROOT / "data/aliases/aliases.jsonl"
REL_PATH = ROOT / "data/relationships/relationships.jsonl"
CLAIM_PATH = ROOT / "data/claims/claims.jsonl"
SNAPSHOT_PATH = ROOT / "data/snapshots/snapshots.jsonl"
DENOM_PATH = ROOT / "data/coverage/denominators.jsonl"
COVERAGE_PATH = ROOT / "data/coverage/coverage.jsonl"

REGIONS = [
    ("riyadh", "منطقة الرياض", "Riyadh Region", 500),
    ("makkah", "منطقة مكة المكرمة", "Makkah Region", 134),
    ("madinah", "منطقة المدينة المنورة", "Madinah Region", 101),
    ("qassim", "منطقة القصيم", "Al-Qassim Region", 152),
    ("eastern", "المنطقة الشرقية", "Eastern Province", 116),
    ("asir", "منطقة عسير", "Asir Region", 131),
    ("tabuk", "منطقة تبوك", "Tabuk Region", 72),
    ("hail", "منطقة حائل", "Hail Region", 108),
    ("northern-borders", "منطقة الحدود الشمالية", "Northern Borders Region", 28),
    ("jazan", "منطقة جازان", "Jazan Region", 47),
    ("najran", "منطقة نجران", "Najran Region", 65),
    ("al-baha", "منطقة الباحة", "Al-Baha Region", 42),
    ("al-jawf", "منطقة الجوف", "Al-Jawf Region", 32),
]
REGION_BY_KEY = {row[0]: row for row in REGIONS}


class TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.row: list[str] | None = None
        self.cell: list[str] | None = None
        self.tables: list[list[list[str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "table":
            if self.depth == 0:
                self.tables.append([])
            self.depth += 1
        elif self.depth and tag == "tr":
            self.row = []
        elif self.depth and tag in {"th", "td"}:
            self.cell = []
        elif self.cell is not None and tag == "br":
            self.cell.append(" ")

    def handle_data(self, data: str) -> None:
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.depth and tag in {"th", "td"} and self.cell is not None:
            assert self.row is not None
            self.row.append(re.sub(r"\s+", " ", " ".join(self.cell)).strip())
            self.cell = None
        elif self.depth and tag == "tr" and self.row is not None:
            self.tables[-1].append(self.row)
            self.row = None
        elif tag == "table" and self.depth:
            self.depth -= 1


def digest_id(prefix: str, key: str, size: int = 16) -> str:
    return f"{prefix}-{hashlib.sha256(key.encode('utf-8')).hexdigest()[:size].upper()}"


def region_id(key: str) -> str:
    return f"ENT-SA-REGION-{key.upper().replace('-', '-')}"


def source_id(key: str) -> str:
    return f"SRC-SA-SAUDIPEDIA-CENTERS-{key.upper()}-2026"


def verify_snapshots() -> dict[str, dict[str, Any]]:
    manifest = json.loads(SNAPSHOT_MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("snapshot_date") != AS_OF or len(manifest.get("records", [])) != 15:
        raise ValueError("Saudi snapshot manifest must contain exactly 15 records dated 2026-08-15")
    indexed = {}
    for record in manifest["records"]:
        path = IMPORT_DIR / record["path"]
        payload = path.read_bytes()
        actual = hashlib.sha256(payload).hexdigest()
        if len(payload) != record["bytes"] or actual != record["sha256"]:
            raise ValueError(f"snapshot mismatch: {path}")
        indexed[record["source_id"]] = record
    return indexed


def split_centers(region_key: str, value: str) -> list[str]:
    cleaned = value.strip().rstrip(".").strip()
    if cleaned == "لا يوجد":
        return []
    delimiter = "-" if region_key == "riyadh" else "،"
    return [part.strip() for part in cleaned.split(delimiter) if part.strip()]


def strip_parent_prefix(label: str) -> tuple[str, str]:
    if label.startswith("محافظة "):
        return "governorate", label.removeprefix("محافظة ").strip()
    if label.startswith("مدينة "):
        return "capital_city", label.removeprefix("مدينة ").strip()
    # The Madinah capital row is printed without the word مدينة.
    return "capital_city", label.strip()


def parse_registry() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    parsed_regions = []
    anomalies: list[dict[str, Any]] = []
    occurrence_total = 0
    unique_total = 0
    governorate_total = 0
    capital_total = 0

    for key, name_ar, name_en, declared_centers in REGIONS:
        path = RAW_DIR / f"saudipedia-centers-{key}.html"
        parser = TableParser()
        parser.feed(path.read_text(encoding="utf-8"))
        if not parser.tables or len(parser.tables[0]) < 2:
            raise ValueError(f"no administrative table in {path}")
        table = parser.tables[0]
        if len(table[0]) != 2 or "المراكز" not in table[0][1]:
            raise ValueError(f"unexpected table header in {path}: {table[0]}")
        rows = []
        region_occurrences = 0
        region_unique = 0
        for row_index, cells in enumerate(table[1:], start=2):
            if len(cells) != 2:
                raise ValueError(f"unexpected row width in {path}, table 1 row {row_index}")
            parent_label, center_cell = cells
            parent_kind, parent_name = strip_parent_prefix(parent_label)
            centers = split_centers(key, center_cell)
            frequencies = Counter(centers)
            seen: Counter[str] = Counter()
            parsed_centers = []
            for position, center_name in enumerate(centers, start=1):
                seen[center_name] += 1
                excluded = seen[center_name] > 1
                parsed_centers.append({
                    "name_ar": center_name,
                    "position": position,
                    "occurrence": seen[center_name],
                    "excluded": excluded,
                    "exclusion_reason": "exact duplicate occurrence within the same source row" if excluded else None,
                    "locator": f"first table, row {row_index}, administrative-centers cell, item {position}",
                })
                region_occurrences += 1
                occurrence_total += 1
                if excluded:
                    anomalies.append({
                        "anomaly_id": digest_id("ANOM-SA-DUPLICATE", f"{key}|{parent_name}|{center_name}|{seen[center_name]}", 12),
                        "severity": "P2",
                        "region_key": key,
                        "source_id": source_id(key),
                        "source_row": row_index,
                        "parent_label": parent_label,
                        "value": center_name,
                        "occurrence": seen[center_name],
                        "action": "excluded_from_entity_materialization",
                        "reason": "Exact duplicate within one parent-scoped source row; the first occurrence is retained.",
                    })
                else:
                    region_unique += 1
                    unique_total += 1
            rows.append({
                "row_index": row_index,
                "parent_label": parent_label,
                "parent_kind": parent_kind,
                "parent_name_ar": parent_name,
                "centers_cell": center_cell,
                "centers": parsed_centers,
                "within_row_duplicates": sorted(name for name, count in frequencies.items() if count > 1),
            })
        governorates = sum(row["parent_kind"] == "governorate" for row in rows)
        capitals = sum(row["parent_kind"] == "capital_city" for row in rows)
        governorate_total += governorates
        capital_total += capitals
        parsed_regions.append({
            "key": key,
            "name_ar": name_ar,
            "name_en": name_en,
            "source_id": source_id(key),
            "source_path": str(path.relative_to(ROOT)),
            "declared_center_total": declared_centers,
            "parsed_center_occurrences": region_occurrences,
            "materialized_unique_centers": region_unique,
            "declared_minus_parsed": declared_centers - region_occurrences,
            "governorate_rows": governorates,
            "capital_city_rows": capitals,
            "rows": rows,
        })

    if (governorate_total, capital_total, occurrence_total, unique_total, len(anomalies)) != (141, 13, 1523, 1521, 2):
        raise ValueError("Saudi parser invariant failed")
    return ({
        "schema_version": "2.0.0",
        "snapshot_date": AS_OF,
        "scope": "dated Saudipedia published-row registry; not current-national completeness",
        "totals": {
            "regions": 13,
            "governorate_rows": governorate_total,
            "capital_city_rows": capital_total,
            "center_occurrences": occurrence_total,
            "excluded_duplicate_occurrences": len(anomalies),
            "unique_parent_scoped_centers": unique_total,
            "sum_of_page_declared_center_totals": sum(row[3] for row in REGIONS),
        },
        "regions": parsed_regions,
    }, anomalies)


def entity(identifier: str, name: str, entity_type: str, source: str, locator: str,
           *, status: str = "current", notes: str | None = None) -> dict[str, Any]:
    return {
        "id": identifier,
        "schema_version": SCHEMA_VERSION,
        "canonical_name": name,
        "canonical_name_language": "ar",
        "canonical_source_id": source,
        "source_locator": locator,
        "entity_type": entity_type,
        "country_code": "SA",
        "status": status,
        "valid_from": None,
        "valid_to": None,
        "coordinates": None,
        "confidence": "high",
        "verification_status": "source_verified",
        "legacy_ids": [],
        "notes": notes,
    }


def relationship(child: str, parent: str, rel_type: str, source: str, locator: str,
                 key: str) -> dict[str, Any]:
    return {
        "id": digest_id("REL-SA", key),
        "schema_version": SCHEMA_VERSION,
        "child_id": child,
        "parent_id": parent,
        "relationship_type": rel_type,
        "status": "current",
        "valid_from": None,
        "valid_to": None,
        "source_id": source,
        "source_locator": locator,
        "confidence": "high",
        "verification_status": "source_verified",
        "notes": None,
    }


def claim(subject: str, topic: str, value: str, source: str, locator: str,
          key: str, *, classification: str | None = "official", tier: str = "A",
          claim_status: str = "verified", temporal: str | None = AS_OF,
          lexical_context: dict[str, Any] | None = None) -> dict[str, Any]:
    # ``tier`` is accepted at call sites to make the intended source-quality audit
    # readable; canonical quality is resolved from the atomic source record.
    del tier
    return {
        "id": digest_id("CLM-SA", key),
        "schema_version": SCHEMA_VERSION,
        "subject_id": subject,
        "predicate": topic,
        "value": {"type": "string", "data": value},
        "unit": None,
        "classification": classification,
        "observed_at": temporal,
        "valid_from": None,
        "valid_to": None,
        "status": claim_status,
        "source_id": source,
        "source_locator": locator,
        "second_source_id": None,
        "second_source_locator": None,
        "sensitivity": "ordinary",
        "published": True,
        "lexical_context": lexical_context,
        "confidence": "high",
        "verification_status": "source_verified",
        "notes": None,
    }


def alias(identifier_key: str, entity_id: str, name: str, language: str, kind: str,
          source: str, locator: str) -> dict[str, Any]:
    return {
        "id": digest_id("ALS-SA", identifier_key),
        "schema_version": SCHEMA_VERSION,
        "entity_id": entity_id,
        "name": name,
        "language": language,
        "script": "Arab" if language == "ar" else "Latn",
        "kind": kind,
        "status": "current",
        "valid_from": None,
        "valid_to": None,
        "source_id": source,
        "source_locator": locator,
    }


def materialize(parsed: dict[str, Any], cultural: dict[str, Any]) -> tuple[list[dict], list[dict], list[dict], list[dict], dict[str, str], dict[str, str], dict[str, str]]:
    entities: list[dict] = []
    aliases: list[dict] = []
    relationships: list[dict] = []
    claims: list[dict] = []
    governorate_ids: dict[str, str] = {}
    place_ids: dict[str, str] = {}
    site_ids: dict[str, str] = {}

    # Regions close a current-national denominator accepted by both aggregate sources.
    for region in parsed["regions"]:
        key = region["key"]
        rid = region_id(key)
        loc = "article body: list of the 13 administrative regions"
        entities.append(entity(rid, region["name_ar"], "sa_region", "SRC-SA-SAUDIPEDIA-ADMIN-2026", loc,
                               notes="Current first-order administrative region (منطقة إدارية)."))
        relationships.append(relationship(rid, "ENT-SA-COUNTRY", "administrative_parent", "SRC-SA-SAUDIPEDIA-ADMIN-2026", loc, f"region|{key}|country"))
        aliases.append(alias(f"region-en|{key}", rid, region["name_en"], "en", "english", "SRC-SA-GASTAT-HEALTH-METHOD-2026", "methodology geographic scope and region labels"))
        claims.append(claim(rid, "administrative_registry_entry", region["name_ar"], "SRC-SA-SAUDIPEDIA-ADMIN-2026", loc, f"region-entry|{key}"))

    for region in parsed["regions"]:
        key = region["key"]
        rid = region_id(key)
        sid = region["source_id"]
        for row in region["rows"]:
            row_loc = f"first table, row {row['row_index']}, first column"
            parent_key = f"{key}:{row['parent_name_ar']}"
            if row["parent_kind"] == "governorate":
                parent_id = digest_id("ENT-SA-GOV", parent_key)
                governorate_ids[parent_key] = parent_id
                entities.append(entity(parent_id, row["parent_name_ar"], "sa_governorate", sid, row_loc,
                                       notes=f"Source row label: {row['parent_label']}. Current dated published-row registry scope."))
                aliases.append(alias(f"gov-full|{parent_key}", parent_id, row["parent_label"], "ar", "official_variant", sid, row_loc))
                relationships.append(relationship(parent_id, rid, "administrative_parent", sid, row_loc, f"gov|{parent_key}|{key}"))
                claims.append(claim(parent_id, "administrative_registry_entry", row["parent_label"], sid, row_loc, f"gov-entry|{parent_key}"))
            else:
                parent_id = f"ENT-SA-CITY-{key.upper()}-SEAT"
                place_ids[f"{key}-seat"] = parent_id
                entities.append(entity(parent_id, row["parent_name_ar"], "city", sid, row_loc,
                                       notes="Regional-capital city row; modeled as a city/emirate seat, not as a governorate."))
                if row["parent_label"] != row["parent_name_ar"]:
                    aliases.append(alias(f"seat-full|{key}", parent_id, row["parent_label"], "ar", "official_variant", sid, row_loc))
                relationships.append(relationship(parent_id, rid, "located_in", sid, row_loc, f"seat-location|{key}"))
                relationships.append(relationship(parent_id, rid, "seat_of", sid, row_loc, f"seat-of|{key}"))
                claims.append(claim(parent_id, "regional_capital_row", row["parent_label"], sid, row_loc, f"seat-entry|{key}"))

            for center in row["centers"]:
                if center["excluded"]:
                    continue
                center_key = f"{parent_key}:{center['name_ar']}"
                center_id = digest_id("ENT-SA-CENTER", center_key)
                entities.append(entity(center_id, center["name_ar"], "sa_markaz", sid, center["locator"],
                                       notes=f"Administrative center (مركز) in a parent-scoped dated source row; source occurrence {center['occurrence']}."))
                relationships.append(relationship(center_id, rid if row["parent_kind"] == "capital_city" else parent_id,
                                                    "administrative_parent", sid, center["locator"], f"center|{center_key}|parent"))
                claims.append(claim(center_id, "administrative_registry_entry", center["name_ar"], sid, center["locator"], f"center-entry|{center_key}"))

    # Bounded populated-place anchors are added only after administrative materialization.
    for place in cultural["bounded_populated_places"]["places"]:
        existing = place_ids.get(place["key"])
        if existing:
            continue
        pid = digest_id("ENT-SA-PLACE", place["key"])
        place_ids[place["key"]] = pid
        entities.append(entity(pid, place["name_ar"], place["entity_type"], place["source_id"], place["locator"],
                               status=place["status"], notes=f"Bounded context anchor: {place['context']}; no populated-place completeness claim."))
        aliases.append(alias(f"place-en|{place['key']}", pid, place["name_en"], "en", "english", place["source_id"], place["locator"]))
        if place.get("parent_governorate"):
            parent_id = governorate_ids[place["parent_governorate"]]
        else:
            parent_id = region_id(place["parent_region"])
        relationships.append(relationship(pid, parent_id, "located_in", place["source_id"], place["locator"], f"place-location|{place['key']}"))
        claims.append(claim(pid, "bounded_place_context", place["context"], place["source_id"], place["locator"], f"place-context|{place['key']}", temporal=None,
                            claim_status="historical" if place["status"] == "historical" else "verified",
                            classification="historical" if place["status"] == "historical" else "regional"))

    # UNESCO property entities are sites, never administrative areas.
    for prop in cultural["properties"]:
        pid = f"ENT-SA-SITE-{prop['key'].upper().replace('-', '-')}"
        site_ids[prop["key"]] = pid
        entities.append(entity(pid, prop["name_ar"], prop["entity_type"], prop["source_id"], prop["locator"],
                               notes="UNESCO World Heritage property; semantic site type is kept distinct from administrative and populated-place layers."))
        aliases.append(alias(f"site-en|{prop['key']}", pid, prop["name_en"], "en", "english", prop["source_id"], prop["locator"]))
        if prop["parent_kind"] == "governorate":
            parent_id = governorate_ids[prop["parent_key"]]
        elif prop["parent_kind"] == "region":
            parent_id = region_id(prop["parent_key"])
        else:
            parent_id = "ENT-SA-COUNTRY"
        relationships.append(relationship(pid, parent_id, "located_in", prop["source_id"], prop["locator"], f"site-location|{prop['key']}"))
        claims.append(claim(pid, "unesco_world_heritage_inscription", str(prop["inscription_year"]), prop["source_id"], prop["locator"], f"wh-inscription|{prop['key']}", classification="official", temporal=AS_OF))
        claims.append(claim(pid, "environmental_context", ", ".join(prop["contexts"]), "SRC-SA-CULTURAL-FIXTURE-2026", f"properties[{prop['key']}].contexts (analytical sampling labels, not heritage designations)", f"site-context|{prop['key']}", classification="regional", tier="B"))

    # Regional and national culinary designations are claims, not inferred place identity.
    for item in cultural["regional_dishes"]:
        claims.append(claim(region_id(item["region_key"]), "official_regional_dish", item["value_ar"], cultural["dish_source_id"], cultural["dish_locator"], f"dish|{item['region_key']}|{item['value_ar']}", classification="regional", tier="B", temporal="2024-01-08"))
    claims.append(claim("ENT-SA-COUNTRY", "official_national_dish", cultural["national_dish"]["dish_ar"], cultural["dish_source_id"], cultural["dish_locator"], "national-dish", classification="national", tier="B", temporal=AS_OF))
    claims.append(claim("ENT-SA-COUNTRY", "official_national_dessert", cultural["national_dish"]["dessert_ar"], cultural["dish_source_id"], cultural["dish_locator"], "national-dessert", classification="national", tier="B", temporal=AS_OF))

    for practice in cultural["intangible_practices"]:
        shared = practice["source_id"] in {"SRC-UNESCO-ICH-SA-01011", "SRC-UNESCO-ICH-SA-01196", "SRC-UNESCO-ICH-SA-01863"}
        claims.append(claim(region_id(practice["region_key"]), "intangible_cultural_practice", practice["value_ar"], practice["source_id"], practice["locator"], f"ich|{practice['region_key']}|{practice['value_ar']}", classification="shared" if shared else "regional"))

    claims.append(claim("ENT-SA-COUNTRY", "regional_clothing_evidence_scope", "تنوع الأزياء التقليدية بين المناطق؛ لا يدعم المصدر إسناد قطع محددة إلى منطقة بعينها", "SRC-SA-GOV-CULTURE-2026", "traditional dress section; scope boundary recorded in fixture domain_status.clothing", "clothing-scope", classification="regional"))

    # Explicit language → variety → region → place → form → meaning/register/source/date chains.
    language_id = "ENT-SA-LANGUAGE-ARABIC"
    entities.append(entity(language_id, "العربية", "language", "SRC-ACADEMIC-SA-DIALECT-CORPUS-2020", "paper title, abstract and Saudi Arabic dialect framing", notes="Language root used only to model the bounded lexical chains; no national variety count is asserted."))
    relationships.append(relationship(language_id, "ENT-SA-COUNTRY", "associated_with", "SRC-ACADEMIC-SA-DIALECT-CORPUS-2020", "Saudi Arabic dialect corpus scope", "arabic-associated-sa"))
    variety_ids = {}
    for variety_key, name_ar, region_key in [("hijazi", "الحجازية", "makkah"), ("najdi", "النجدية", "riyadh")]:
        vid = f"ENT-SA-VARIETY-{variety_key.upper()}"
        variety_ids[variety_key] = vid
        entities.append(entity(vid, name_ar, "language_variety", "SRC-ACADEMIC-SA-DIALECT-CORPUS-2020", f"p. 220, {variety_key.title()} examples", notes="Bounded Arabic language variety record; not a denominator item."))
        relationships.append(relationship(vid, language_id, "variety_of", "SRC-ACADEMIC-SA-DIALECT-CORPUS-2020", f"p. 220, {variety_key.title()} examples", f"variety-of|{variety_key}"))
        relationships.append(relationship(vid, region_id(region_key), "associated_with", "SRC-ACADEMIC-SA-DIALECT-CORPUS-2020", f"paper dialect label and bounded regional sample mapping", f"variety-region|{variety_key}|{region_key}"))
    for form in cultural["lexical_forms"]:
        fid = digest_id("ENT-SA-LEXEME", f"{form['variety_key']}|{form['form']}")
        entities.append(entity(fid, form["form"], "lexical_form", form["source_id"], form["locator"], notes="Attested lexical form; not a place and not a claim about a national dialect count."))
        relationships.append(relationship(fid, variety_ids[form["variety_key"]], "form_of", form["source_id"], form["locator"], f"form-variety|{form['variety_key']}|{form['form']}"))
        place_id = place_ids[form["place_key"]]
        relationships.append(relationship(fid, place_id, "attested_in", form["source_id"], form["locator"], f"form-place|{form['variety_key']}|{form['form']}|{form['place_key']}"))
        value = f"meaning={form['meaning']}; register={form['register']}; study_date={form['study_date']}"
        context = {
            "form": form["form"],
            "meaning": form["meaning"],
            "place_id": place_id,
            "language": "Arabic",
            "dialect": form["variety_key"],
            "variety": form["variety_key"],
            "register": form["register"],
            "study_date": form["study_date"],
            "speaker_or_study": "SDCT corpus classification study",
            "ipa": None,
        }
        claims.append(claim(fid, "lexical_attestation", value, form["source_id"], form["locator"], f"lexical|{form['variety_key']}|{form['form']}", classification="regional", tier="B", temporal=form["study_date"], lexical_context=context))

    return entities, aliases, relationships, claims, governorate_ids, place_ids, site_ids


def coverage_records() -> tuple[list[dict], list[dict], list[dict]]:
    checksum = hashlib.sha256(SNAPSHOT_MANIFEST.read_bytes()).hexdigest()
    snapshot = {
        "id": "SNP-SA-ADMIN-20260815", "schema_version": SCHEMA_VERSION,
        "title": "Saudi administrative and bounded-content evidence snapshot",
        "captured_at": AS_OF, "source_id": "SRC-SA-ADMIN-SNAPSHOT-CATALOG-2026",
        "scope": "15 checksum-verified administrative HTML snapshots plus bounded institutional/scholarly content locators",
        "method": "GitHub Actions retrieval for administrative HTML; deterministic local parsing; bounded manual extraction for institutional content",
        "checksum": f"sha256:{checksum}",
        "notes": "Administrative records are immutable local inputs. Remote cultural records are bounded by atomic source metadata and exact locators.",
    }
    missing_gov = "Current-national governorate denominator is conflicted: Saudipedia reports 150 while GASTAT methodology for 2024 reports 151; 141 dated table rows are materialized separately."
    missing_centers = "Current-national center denominator is conflicted: Saudipedia reports 1,377 nationally while regional pages declare 1,528 and yield 1,523 parsed occurrences; 1,521 unique parent-scoped rows are materialized separately."
    no_places = "No dated, atomic, current official national populated-place registry was accepted; four bounded context anchors do not form a completeness denominator."
    no_neighborhoods = "No dated, atomic, current official national neighborhood registry was accepted in this cycle."
    no_nawahi = "The current Law of Provinces names النواحي as a legal component, but no dated enumerable official national registry of active nawahi was accepted in this cycle."
    specs = [
        ("REGIONS", "sa_region", "13 current first-order administrative regions", 13, "official", "SRC-SA-SAUDIPEDIA-ADMIN-2026", "article body: 13 regions", None, 13, 0, []),
        ("GOVERNORATE-ROWS", "sa_governorate_published_rows", "Governorate rows in the 13 dated regional administrative-center tables; excludes the separately printed regional-capital city row on each page", 141, "official", "SRC-SA-ADMIN-SNAPSHOT-CATALOG-2026", "13 first tables; rows labelled محافظة", None, 141, 0, []),
        ("CENTER-OCCURRENCES", "sa_markaz_published_occurrences", "Center occurrences in all 13 dated regional tables before exact within-row duplicate exclusion", 1523, "official", "SRC-SA-ADMIN-SNAPSHOT-CATALOG-2026", "13 first tables; split administrative-centers cells", None, 1521, 2, [{"count": 2, "reason": "Exact repeated occurrence under the same source parent: الرقعي in حفر الباطن and الربواء in الرين; first occurrence retained."}]),
        ("CURRENT-GOVERNORATES", "sa_governorate_current_national", "Current national governorates", None, "conflicted", "SRC-SA-SAUDIPEDIA-ADMIN-2026", "Saudipedia 150 versus GASTAT 151", missing_gov, 141, 0, []),
        ("CURRENT-CENTERS", "sa_markaz_current_national", "Current national administrative centers", None, "conflicted", "SRC-SA-SAUDIPEDIA-ADMIN-2026", "Saudipedia national 1,377 versus regional declared 1,528 and parsed 1,523", missing_centers, 1521, 0, []),
        ("CURRENT-NAWAHI", "sa_nahiya_current_national", "Current national nawahi (النواحي) named as a legal component in Article 3 of the Law of Provinces", None, "unavailable", "SRC-SA-LAW-OF-PROVINCES-1992", "المادة الثالثة", no_nawahi, 0, 0, []),
        ("POPULATED-PLACES", "populated_places", "Current national populated places", None, "unavailable", "SRC-SA-CULTURAL-FIXTURE-2026", "bounded_populated_places", no_places, 4, 0, []),
        ("NEIGHBORHOODS", "neighborhoods", "Current national neighborhoods", None, "unavailable", "SRC-SA-CULTURAL-FIXTURE-2026", "domain_status and explicit non-population", no_neighborhoods, 0, 0, []),
        ("WORLD-HERITAGE", "unesco_world_heritage_properties", "Saudi properties inscribed on the UNESCO World Heritage List as of snapshot date", 8, "official", "SRC-UNESCO-WHC-SA-STATE-2026", "Properties inscribed: 8", None, 8, 0, []),
    ]
    denominators, coverages = [], []
    for key, layer, definition, value, status, sid, locator, missing_reason, matched, excluded, reasons in specs:
        did = f"DEN-SA-{key}-20260815"
        cid = f"COV-SA-{key}-20260815"
        denominator = {
            "id": did, "schema_version": SCHEMA_VERSION, "country_code": "SA", "layer": layer,
            "definition": definition, "value": value, "as_of": AS_OF, "status": status,
            "source_id": sid, "source_locator": locator,
            "license": "Source copyright; factual extraction with attribution",
            "missing_reason": missing_reason,
            "notes": "A 100% value applies only to this exact denominator definition." if value is not None else "No coverage percentage is asserted.",
            "denominator": value, "snapshot_date": AS_OF,
        }
        complete = value is not None and matched + excluded == value
        percentage = round((matched + excluded) / value * 100, 2) if value else (100.0 if value == 0 and matched + excluded == 0 else None)
        missing = value - matched - excluded if value is not None else None
        coverage = {
            "id": cid, "schema_version": SCHEMA_VERSION, "country_code": "SA", "layer": layer,
            "snapshot_id": snapshot["id"], "denominator_id": did, "source_id": sid,
            "matched": matched, "unmatched": missing if missing is not None else 0, "excluded": excluded,
            "missing": missing, "complete": complete, "missing_reason": missing_reason,
            "notes": denominator["notes"], "denominator": value, "snapshot_date": AS_OF,
            "license": denominator["license"], "coverage_percentage": percentage,
            "exclusion_reasons": reasons,
        }
        denominators.append(denominator)
        coverages.append(coverage)
    return [snapshot], denominators, coverages


def replace_country(path: Path, new_rows: list[dict], *, preserve_ids: set[str] | None = None) -> None:
    preserve_ids = preserve_ids or set()
    old = read_jsonl(path)
    prefixes = ("REL-SA-", "CLM-SA-", "ALS-SA-", "SNP-SA-", "DEN-SA-", "COV-SA-")
    kept = [
        row for row in old
        if row.get("id") not in preserve_ids
        and row.get("country_code") != "SA"
        and not row.get("id", "").startswith(prefixes)
        and not row.get("entity_id", "").startswith("ENT-SA-")
        and not row.get("subject_id", "").startswith("ENT-SA-")
        and not row.get("child_id", "").startswith("ENT-SA-")
    ]
    preserved = {}
    for row in old:
        if row.get("id") in preserve_ids:
            preserved[row["id"]] = row
    kept.extend(preserved[key] for key in sorted(preserved))
    write_jsonl(path, kept + new_rows)


def main() -> int:
    verify_snapshots()
    parsed, anomalies = parse_registry()
    cultural = json.loads(CULTURAL_FIXTURE.read_text(encoding="utf-8"))
    entities, aliases, relationships, claims, _govs, _places, _sites = materialize(parsed, cultural)
    snapshots, denominators, coverages = coverage_records()

    write_json(IMPORT_DIR / "parsed_registry.json", parsed)
    write_json(IMPORT_DIR / "anomaly_ledger.json", {
        "schema_version": "2.0.0", "snapshot_date": AS_OF,
        "anomaly_count": len(anomalies), "unresolved_p0": 0, "unresolved_p1": 0,
        "records": anomalies,
    })
    replace_country(ENTITY_PATH, entities, preserve_ids={"ENT-SA-COUNTRY"})
    replace_country(ALIAS_PATH, aliases, preserve_ids={"ALS-79915F345A575A61"})
    replace_country(REL_PATH, relationships)
    replace_country(CLAIM_PATH, claims)
    replace_country(SNAPSHOT_PATH, snapshots)
    replace_country(DENOM_PATH, denominators)
    replace_country(COVERAGE_PATH, coverages)

    summary = {
        "snapshot_date": AS_OF,
        "entities_written": len(entities),
        "entities_including_existing_country": len(entities) + 1,
        "aliases_written": len(aliases),
        "relationships_written": len(relationships),
        "claims_written": len(claims),
        "snapshots_written": len(snapshots),
        "denominators_written": len(denominators),
        "coverage_records_written": len(coverages),
        "parser_totals": parsed["totals"],
        "anomalies": len(anomalies),
    }
    write_json(IMPORT_DIR / "import_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
