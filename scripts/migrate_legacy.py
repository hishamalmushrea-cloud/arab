#!/usr/bin/env python3
"""Deterministic Phase 1 migration from legacy CSV into Schema v1.

Only source-defensible records enter active data. Every legacy row is recorded in the
migration ledger; questionable or unsupported rows are copied to quarantine.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from model import (
    AS_OF,
    COUNTRIES,
    NAME_TO_ISO,
    ROOT,
    SCHEMA_VERSION,
    entity_id,
    file_sha256,
    norm_name,
    record_id,
    scalar,
    stable_token,
    write_json,
    write_jsonl,
)

LEGACY_DIR = ROOT / "قاعدة_بيانات_الأماكن"
DATA = ROOT / "data"

SRC_ISO = "SRC-ISO-3166-1-2020"
SRC_AUDIT = "SRC-ARAB-FINAL-AUDIT-2026"
SRC_TN_DELEGATIONS = "SRC-TN-MOI-DELEGATIONS-2013"
SRC_TN_POPULATION = "SRC-TN-INS-RGPH-2014"
SRC_TN_MUNICIPALITIES = "SRC-TN-DGCL-MUNICIPALITIES-2018"
SRC_TN_IMADAS = "SRC-TN-MOI-IMADAS-2013"
SRC_LY_MUNICIPALITIES = "SRC-LY-MOLG-MUNICIPALITIES-2026"
SRC_LY_LAW59 = "SRC-LY-LAW-59-2012"
SRC_LY_CENSUS = "SRC-LY-BSC-CENSUS-2006"

SNAPSHOT_MIGRATION = "SNP-MIGRATION-2026-08-15"
SNAPSHOT_TN_ADMIN = "SNP-TN-ADMIN-2026-08-15"
SNAPSHOT_TN_CENSUS = "SNP-TN-RGPH-2014"
SNAPSHOT_LY_CURRENT = "SNP-LY-MUNICIPALITIES-2026-08-15"
SNAPSHOT_LY_HISTORIC = "SNP-LY-CENSUS-2006"


def source_records() -> list[dict[str, Any]]:
    return [
        {
            "id": SRC_ISO,
            "schema_version": SCHEMA_VERSION,
            "title": "ISO 3166-1:2020 — Codes for the representation of names of countries and their subdivisions — Part 1: Country code",
            "publisher": "International Organization for Standardization (ISO)",
            "source_type": "standard",
            "url": "https://www.iso.org/obp/ui/#iso:std:iso:3166:-1:ed-4:v1:en",
            "archive_url": None,
            "publication_date": "2020-08",
            "retrieved_at": AS_OF,
            "license": "ISO copyright; reuse is subject to ISO terms of use",
            "language": "en",
            "country_codes": sorted(COUNTRIES),
            "locator": "Online Browsing Platform country-code entries for the 22 project countries",
            "checksum": None,
            "notes": "Used only for country identities and ISO alpha-2 codes, not for lower administrative denominators.",
        },
        {
            "id": SRC_AUDIT,
            "schema_version": SCHEMA_VERSION,
            "title": "FINAL_AUDIT — accepted project baseline",
            "publisher": "Arab project repository",
            "source_type": "project_audit",
            "url": "https://github.com/hishamalmushrea-cloud/arab/blob/arena/01a00307-arab/audit/FINAL_AUDIT.md",
            "archive_url": None,
            "publication_date": AS_OF,
            "retrieved_at": AS_OF,
            "license": "Repository license not declared; internal project audit use",
            "language": "ar",
            "country_codes": sorted(COUNTRIES),
            "locator": "Complete report; especially the baseline, country assessments, defects, and exit gates",
            "checksum": file_sha256(ROOT / "audit/FINAL_AUDIT.md"),
            "notes": "Authoritative for migration decisions, not an official geographic authority.",
        },
        {
            "id": SRC_TN_DELEGATIONS,
            "schema_version": SCHEMA_VERSION,
            "title": "معتمديات ولايات الجمهورية",
            "publisher": "وزارة الداخلية التونسية — الإدارة العامة للشؤون الجهوية",
            "source_type": "official_dataset",
            "url": "https://opendata.interieur.gov.tn/ar/catalog/delegations-par-gouvernorats-de-la-republique",
            "archive_url": None,
            "publication_date": "2013-06-25",
            "retrieved_at": AS_OF,
            "license": "License not stated on the source page",
            "language": "ar",
            "country_codes": ["TN"],
            "locator": "Table of 24 governorates, per-governorate counts, and delegation names",
            "checksum": None,
            "notes": "Page reported a modification on the retrieval date but left temporal coverage blank. Its detailed table sums to 264; a separate official count page has shown later conflicting totals, so freshness requires reconciliation.",
        },
        {
            "id": SRC_TN_POPULATION,
            "schema_version": SCHEMA_VERSION,
            "title": "Recensement Général de la Population et de l'Habitat 2014 — Volume 3",
            "publisher": "Institut National de la Statistique, Tunisie",
            "source_type": "census",
            "url": "https://www.ins.tn/sites/default/files-ftp1/files/publication/pdf/RGPH%202014-V3.pdf",
            "archive_url": None,
            "publication_date": "2016",
            "retrieved_at": AS_OF,
            "license": "License not stated in the publication metadata",
            "language": "fr-ar",
            "country_codes": ["TN"],
            "locator": "Volume 3, PDF page 47: exact population table by governorate",
            "checksum": None,
            "notes": "Volume 3 supplies exact values. Volume 0 is rounded and must not be used for exact governorate claims.",
        },
        {
            "id": SRC_TN_MUNICIPALITIES,
            "schema_version": SCHEMA_VERSION,
            "title": "Rapport de synthèse sur la nouvelle carte des municipalités",
            "publisher": "Direction Générale des Collectivités Locales, Tunisie",
            "source_type": "official_report",
            "url": "http://www.collectiviteslocales.gov.tn/wp-content/uploads/2018/04/Rapport_synthese_vf-2018.pdf",
            "archive_url": None,
            "publication_date": "2018-04-06",
            "retrieved_at": AS_OF,
            "license": "License not stated in the publication metadata",
            "language": "fr",
            "country_codes": ["TN"],
            "locator": "Administrative overview stating 24 governorates and 350 communes after creation of 86 new municipalities",
            "checksum": None,
            "notes": "Provides a dated 2018 denominator, not proof that the same denominator is current in 2026.",
        },
        {
            "id": SRC_TN_IMADAS,
            "schema_version": SCHEMA_VERSION,
            "title": "Secteurs territoriaux (imadas) par gouvernorat et délégation",
            "publisher": "Ministère de l'Intérieur tunisien — Direction Générale des Affaires Régionales",
            "source_type": "official_dataset",
            "url": "https://opendata.interieur.gov.tn/fr/catalog/secteurs-territoriaux-par-gouvernorat-et-delegation",
            "archive_url": None,
            "publication_date": "2013-07-15",
            "retrieved_at": AS_OF,
            "license": "License not stated on the source page",
            "language": "ar-fr",
            "country_codes": ["TN"],
            "locator": "Dataset metadata and open-format endpoints",
            "checksum": None,
            "notes": "The page leaves temporal coverage blank; no dated national denominator was promoted during this migration.",
        },
        {
            "id": SRC_LY_MUNICIPALITIES,
            "schema_version": SCHEMA_VERSION,
            "title": "قائمة البلديات",
            "publisher": "وزارة الحكم المحلي الليبية",
            "source_type": "official_register",
            "url": "https://www.lgm.gov.ly/municipalities",
            "archive_url": None,
            "publication_date": None,
            "retrieved_at": AS_OF,
            "license": "License not stated on the source page",
            "language": "ar",
            "country_codes": ["LY"],
            "locator": "National municipalities catalogue and municipality profile links",
            "checksum": None,
            "notes": "Publication and content-effective dates are not stated. The map-heavy catalogue extraction was not accepted as a national denominator; retrieval date is not treated as legal commencement date.",
        },
        {
            "id": SRC_LY_LAW59,
            "schema_version": SCHEMA_VERSION,
            "title": "قانون رقم 59 لسنة 2012 بشأن نظام الإدارة المحلية",
            "publisher": "الجهة التشريعية الليبية; published by Ministry of Local Government",
            "source_type": "law",
            "url": "https://www.lgm.gov.ly/Legal/2",
            "archive_url": None,
            "publication_date": "2012",
            "retrieved_at": AS_OF,
            "license": "Public legal text; site reuse terms not stated",
            "language": "ar",
            "country_codes": ["LY"],
            "locator": "Full legal file linked from the Ministry laws register",
            "checksum": None,
            "notes": "Supports the municipality framework, not by itself the identity of each currently listed municipality.",
        },
        {
            "id": SRC_LY_CENSUS,
            "schema_version": SCHEMA_VERSION,
            "title": "التعداد العام للسكان 2006 — النتائج حسب مناطق التعداد",
            "publisher": "مصلحة الإحصاء والتعداد، ليبيا",
            "source_type": "census",
            "url": "https://bsc.ly/demographicl_statist/%D8%A7%D9%84%D8%AA%D8%B9%D8%AF%D8%A7%D8%AF-%D8%A7%D9%84%D8%B9%D8%A7%D9%85-%D9%84%D9%84%D8%B3%D9%83%D8%A7%D9%862006/",
            "archive_url": None,
            "publication_date": "2006",
            "retrieved_at": AS_OF,
            "license": "License not stated on the source page",
            "language": "ar",
            "country_codes": ["LY"],
            "locator": "Official index and tables for the 22 census regions",
            "checksum": None,
            "notes": "Used for a historical 2006 sha‘biya snapshot only; it is not mixed with the current municipality hierarchy.",
        },
    ]


def install_sources() -> list[dict[str, Any]]:
    records = source_records()
    out = DATA / "sources"
    out.mkdir(parents=True, exist_ok=True)
    # Install only missing legacy records. Atomic source files are curated
    # structured inputs and may contain later independent metadata corrections;
    # a repair must not erase those corrections or Phase-specific records.
    for source in records:
        slug = source["id"].lower().replace("src-", "")
        path = out / f"{slug}.json"
        if not path.exists():
            write_json(path, source)
    return records


def load_legacy_rows() -> list[dict[str, Any]]:
    result = []
    for path in sorted(LEGACY_DIR.glob("*.csv"), key=lambda p: p.as_posix()):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or "id" not in reader.fieldnames:
                continue
            for row_no, row in enumerate(reader, 2):
                if None in row:
                    raise ValueError(f"{path}:{row_no}: malformed row remains; run repair_legacy.py")
                clean = {key: (value or "") for key, value in row.items()}
                iso = NAME_TO_ISO.get(clean.get("الدولة", ""))
                result.append({
                    "path": str(path.relative_to(ROOT)),
                    "row": row_no,
                    "iso": iso,
                    "raw": clean,
                })
    return result


def base_entity(iso: str, name: str, entity_type: str, source_id: str, locator: str, *, status: str = "current", legacy_ids: list[str] | None = None, valid_from=None, valid_to=None, notes=None, parent_key="") -> dict[str, Any]:
    return {
        "id": entity_id(iso, entity_type, name, parent_key),
        "schema_version": SCHEMA_VERSION,
        "country_code": iso,
        "canonical_name": name,
        "canonical_name_language": "ar",
        "entity_type": entity_type,
        "status": status,
        "valid_from": valid_from,
        "valid_to": valid_to,
        "canonical_source_id": source_id,
        "source_locator": locator,
        "legacy_ids": sorted(set(legacy_ids or [])),
        "coordinates": None,
        "verification_status": "verified",
        "confidence": "high",
        "notes": notes,
    }


def relation(child: dict[str, Any], parent: dict[str, Any], source_id: str, locator: str, *, status="current", valid_from=None, valid_to=None, notes=None) -> dict[str, Any]:
    return {
        "id": record_id("REL", child["id"], parent["id"], "administrative_parent", status),
        "schema_version": SCHEMA_VERSION,
        "child_id": child["id"],
        "parent_id": parent["id"],
        "relationship_type": "administrative_parent",
        "status": status,
        "valid_from": valid_from,
        "valid_to": valid_to,
        "source_id": source_id,
        "source_locator": locator,
        "verification_status": "verified",
        "confidence": "high",
        "notes": notes,
    }


def alias(entity: dict[str, Any], name: str, source_id: str, locator: str, *, language="en", script="Latn", kind="english", status="current") -> dict[str, Any]:
    return {
        "id": record_id("ALS", entity["id"], name, language, kind),
        "schema_version": SCHEMA_VERSION,
        "entity_id": entity["id"],
        "name": name.strip(),
        "language": language,
        "script": script,
        "kind": kind,
        "status": status,
        "source_id": source_id,
        "source_locator": locator,
        "valid_from": None,
        "valid_to": None,
    }


def migrate() -> dict[str, Any]:
    sources = install_sources()
    source_ids = {source["id"] for source in sources}
    legacy = load_legacy_rows()

    entities: list[dict[str, Any]] = []
    aliases: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    ledger_by_key: dict[tuple[str, int], dict[str, Any]] = {}
    quarantined: list[dict[str, Any]] = []

    country_entities: dict[str, dict[str, Any]] = {}
    for iso, (name_ar, name_en) in COUNTRIES.items():
        entity = base_entity(iso, name_ar, "country", SRC_ISO, f"ISO alpha-2 entry {iso}", notes="Project country scope; this entity does not imply local-place completeness.")
        entities.append(entity)
        country_entities[iso] = entity
        aliases.append(alias(entity, name_en, SRC_ISO, f"ISO alpha-2 entry {iso}"))

    def mark(item, disposition: str, reason_code: str, reason: str, entity_ids: list[str] | None = None, quarantine=False):
        key = (item["path"], item["row"])
        row = item["raw"]
        entry = {
            "id": "MIG-" + stable_token("migration-row", item["path"], item["row"], row.get("id", "")),
            "path": item["path"],
            "row": item["row"],
            "legacy_id": row.get("id"),
            "country_code": item["iso"],
            "disposition": disposition,
            "reason_code": reason_code,
            "reason": reason,
            "entity_ids": sorted(entity_ids or []),
        }
        ledger_by_key[key] = entry
        if quarantine:
            quarantined.append({
                "id": "QUAR-" + stable_token("quarantine-row", item["path"], item["row"], row.get("id", "")),
                "path": item["path"],
                "row": item["row"],
                "legacy_id": row.get("id"),
                "country_code": item["iso"],
                "reason_code": reason_code,
                "reason": reason,
                "raw_record": row,
            })

    # Tunisia: 24 governorates and one 264-delegation representation.
    tn_rows = [item for item in legacy if item["path"].endswith("تونس.csv")]
    tn_gov: dict[str, dict[str, Any]] = {}
    tn_entity_by_legacy: dict[str, dict[str, Any]] = {}
    primary_gov = [item for item in tn_rows if re.fullmatch(r"TN-\d{2}", item["raw"]["id"])]
    for item in primary_gov:
        row = item["raw"]
        name = row["الاسم_المحلي"].strip()
        entity = base_entity("TN", name, "tn_governorate", SRC_TN_DELEGATIONS, f"Governorate row: {name}", legacy_ids=[row["id"]], parent_key="TN")
        entities.append(entity)
        relationships.append(relation(entity, country_entities["TN"], SRC_TN_DELEGATIONS, f"Governorate row: {name}"))
        tn_gov[norm_name(name)] = entity
        tn_entity_by_legacy[row["id"]] = entity
        mark(item, "migrated", "source_defensible_admin_entity", "Governorate identity migrated; any co-located capital implication in the mixed legacy type was not converted to a city entity.", [entity["id"]], quarantine=("+" in row["النوع"]))

        alternative = scalar(row.get("الأسماء_البديلة"))
        if alternative:
            for alt_name in [part.strip() for part in alternative.split("/") if part.strip()]:
                # Promote only Latin-script forms that can be checked against the bilingual
                # census publication; unsupported Arabic regional labels stay in the ledger.
                if re.search(r"[A-Za-z]", alt_name) and norm_name(alt_name) != norm_name(name):
                    aliases.append(alias(entity, alt_name, SRC_TN_POPULATION, f"Legacy governorate row {row['id']}; checked against RGPH bilingual naming", language="und", script="Latn", kind="transliteration"))

        population = scalar(row.get("السكان"))
        if population and population.isdigit():
            # Three legacy rows reproduce rounded/incorrect values. Volume 3, PDF
            # page 47 is the exact table and is authoritative for all 24 claims.
            exact_population = {
                "سوسة": "674818",
                "نابل": "787918",
                "القيروان": "570436",
            }.get(name, population)
            claims.append({
                "id": record_id("CLM", entity["id"], "population", "2014", exact_population),
                "schema_version": SCHEMA_VERSION,
                "subject_id": entity["id"],
                "predicate": "population",
                "value": {"type": "integer", "data": int(exact_population)},
                "unit": "person",
                "status": "verified",
                "observed_at": "2014-04-23",
                "valid_from": None,
                "valid_to": None,
                "source_id": SRC_TN_POPULATION,
                "second_source_id": None,
                "source_locator": f"Volume 3, PDF p. 47, governorate row: {name}",
                "sensitivity": "ordinary",
                "notes": "Exact 2014 governorate total from INS RGPH Volume 3, PDF page 47.",
            })

    tn_delegation: dict[tuple[str, str], dict[str, Any]] = {}
    for item in tn_rows:
        row = item["raw"]
        if row["النوع"] != "معتمدية":
            continue
        parent_key = norm_name(row["الوحدة_الإدارية_العليا"])
        parent = tn_gov.get(parent_key)
        name = row["الاسم_المحلي"].strip()
        if not parent:
            mark(item, "quarantined", "orphan_legacy_parent", "Delegation parent did not match one of the 24 migrated governorates.", quarantine=True)
            continue
        key = (parent_key, norm_name(name))
        if key in tn_delegation:
            mark(item, "merged_duplicate", "duplicate_representation", "Repeated delegation representation merged into the existing entity.", [tn_delegation[key]["id"]], quarantine=True)
            tn_delegation[key]["legacy_ids"] = sorted(set(tn_delegation[key]["legacy_ids"] + [row["id"]]))
            continue
        entity = base_entity("TN", name, "tn_delegation", SRC_TN_DELEGATIONS, f"Governorate {parent['canonical_name']}; delegation {name}", legacy_ids=[row["id"]], parent_key=parent["id"])
        entities.append(entity)
        relationships.append(relation(entity, parent, SRC_TN_DELEGATIONS, f"Governorate {parent['canonical_name']}; delegation {name}"))
        tn_delegation[key] = entity
        tn_entity_by_legacy[row["id"]] = entity
        mark(item, "migrated", "source_defensible_admin_entity", "One canonical delegation representation migrated.", [entity["id"]])

    for item in tn_rows:
        key0 = (item["path"], item["row"])
        if key0 in ledger_by_key:
            continue
        row = item["raw"]
        if row["النوع"] == "معتمدية (المستوى الإداري الثاني)":
            key = (norm_name(row["الوحدة_الإدارية_العليا"]), norm_name(row["الاسم_المحلي"]))
            entity = tn_delegation.get(key)
            if entity:
                entity["legacy_ids"] = sorted(set(entity["legacy_ids"] + [row["id"]]))
                mark(item, "merged_duplicate", "duplicate_representation", "Second 264-row representation merged as a legacy reference, not a second entity or alias.", [entity["id"]], quarantine=True)
            else:
                mark(item, "quarantined", "unmatched_duplicate_representation", "Second-tier representation did not match a canonical delegation.", quarantine=True)
        elif row["id"].startswith("TN-W-") and row["النوع"] == "ولاية":
            entity = tn_gov.get(norm_name(row["الاسم_المحلي"]))
            if entity:
                entity["legacy_ids"] = sorted(set(entity["legacy_ids"] + [row["id"]]))
                mark(item, "merged_duplicate", "duplicate_representation", "Duplicate governorate representation merged into the canonical entity.", [entity["id"]], quarantine=True)
            else:
                mark(item, "quarantined", "unmatched_duplicate_representation", "Governorate representation did not match a canonical governorate.", quarantine=True)
        else:
            code = "unsupported_cultural_or_microplace_record"
            reason = "Historic gates, quarters, passages, neighborhoods, and the project-only city row lack an atomic source and parent chain suitable for active migration."
            mark(item, "quarantined", code, reason, quarantine=True)

    # Libya: current listed municipalities from the legacy subset, plus a separate historical 2006 hierarchy.
    official_ly_names = """أبوسليم|أوباري|أوجلة|اجخرة|إجدابيا|إدري الشاطئ|اسبيعة|الأبرق|الأبيار|الأصابعة|البردي|البريقة|البيضاء|الجفرة|الجميل|الحرابة|الحوامد|الخمس|الرجبان|الرحيبات|الرياينة|الزاوية|الزاوية الجنوب|الزاوية الغرب|الزنتان|الزهراء|الزويتينة سلطان|السائح|الشرقية|الشقيقة|الشويرف|العامرية|العجيلات|العربان|العزيزية|العواته|الغريفة|القبة|القرة بوللي|القرضة الشاطئ|القطرون|القلعة|القواليش|القيقب|الكفرة|الماية|المرج|العوينة|المعمورة|المليطانية|المنشية الجميل|الناصرية|امساعد|انتلات البيضان|بئر الأشهب|باطن الجبل|براك الشاطئ|بنت بية|بنغازي|بني وليد|تاجوراء|تازربو|تاورغاء|تراغن|ترهونة|توكرة|جادو|جالو|جردس العبيد|جنزور|جنوب الجبل الأخضر|حي الأندلس|خليج السدرة|درج|درنة|ربيانة|رقدالين|زلطن|زليتن|زمزم|زوارة|ساحل الجبل|سبها|سرت|سلوق|سواني بن أدم|سوسة|سوق الجمعة|سوق الخميس|شحات|صبراتة|صرمان|طبرق|طرابلس المركز|ظاهر الجبل|عمر المختار|عين زارة|عين غزالة|غات|غدامس|غريان|قصر بن غشير|قصر خيار|قمينس|كاباو|ككلة|مرادة|مرزق|مرسى دفنة|مزدة|مسلاتة|مصراتة|نالوت|نسمة|هراوة|وادي البوانيس|وادي عتبة|وازن|وردامة|يفرن|أم الرزم|الجليدة|الجديدة|مدور الزيتون|العوينات|تجرهي|المردوم|تنيناي|القريات|زلة|برقن|اوال|تهالة|بركت|سيناون|زويلة|راس الطبل|المنطقة الادارية الشعبة|جرمة|قرارة|الرقيبة""".split("|")
    official_ly = {norm_name(name): name for name in official_ly_names}
    ly_rows = [item for item in legacy if item["path"].endswith("ليبيا.csv")]
    ly_current: dict[str, dict[str, Any]] = {}
    ly_unmatched_primary = 0

    for item in ly_rows:
        row = item["raw"]
        if row["النوع"] not in {"شعبية", "شعبية+عاصمة"}:
            continue
        name = row["الاسم_المحلي"].strip()
        entity = base_entity(
            "LY", name, "ly_shabiya_historical", SRC_LY_CENSUS,
            f"2006 census region: {name}", status="historical", legacy_ids=[row["id"]],
            notes="Historical 2006 census-region entity; never a parent in the current municipality hierarchy.", parent_key="LY-2006",
        )
        entities.append(entity)
        relationships.append(relation(entity, country_entities["LY"], SRC_LY_CENSUS, f"2006 census region: {name}", status="historical", notes="Historical hierarchy snapshot only."))
        mark(item, "migrated", "historical_hierarchy_separated", "Migrated as a historical sha‘biya entity in the 2006 snapshot, separate from current municipalities.", [entity["id"]], quarantine=("+" in row["النوع"]))

    for item in ly_rows:
        row = item["raw"]
        if row["النوع"] != "بلدية":
            continue
        legacy_name = row["الاسم_المحلي"].strip()
        normalized = norm_name(legacy_name)
        official_name = official_ly.get(normalized)
        if not official_name and normalized == norm_name("خليج سدرة"):
            official_name = "خليج السدرة"
        if not official_name:
            ly_unmatched_primary += 1
            mark(item, "quarantined", "not_matched_to_current_official_register", "Legacy municipality name was not an unambiguous match to the retrieved official current list.", quarantine=True)
            continue
        key = norm_name(official_name)
        if key in ly_current:
            entity = ly_current[key]
            entity["legacy_ids"] = sorted(set(entity["legacy_ids"] + [row["id"]]))
            mark(item, "merged_duplicate", "duplicate_representation", "Repeated municipality merged into the existing current entity.", [entity["id"]], quarantine=True)
            continue
        entity = base_entity("LY", official_name, "ly_municipality", SRC_LY_MUNICIPALITIES, f"Municipality list entry: {official_name}", legacy_ids=[row["id"]], parent_key="LY-CURRENT", notes="Current-register match as retrieved on 2026-08-15; legal commencement date was not inferred.")
        entities.append(entity)
        relationships.append(relation(entity, country_entities["LY"], SRC_LY_MUNICIPALITIES, f"Municipality list entry: {official_name}"))
        ly_current[key] = entity
        mark(item, "migrated", "matched_current_official_register", "Legacy municipality matched the official current list.", [entity["id"]])
        if norm_name(legacy_name) != norm_name(official_name) or legacy_name != official_name:
            aliases.append(alias(entity, legacy_name, SRC_LY_MUNICIPALITIES, f"Legacy spelling matched to official municipality entry {official_name}", language="ar", script="Arab", kind="official_variant"))

    for item in ly_rows:
        key0 = (item["path"], item["row"])
        if key0 in ledger_by_key:
            continue
        row = item["raw"]
        if row["النوع"] == "بلدية (المستوى الثاني)":
            entity = ly_current.get(norm_name(row["الاسم_المحلي"]))
            if entity:
                entity["legacy_ids"] = sorted(set(entity["legacy_ids"] + [row["id"]]))
                mark(item, "merged_duplicate", "duplicate_representation", "Second-level municipality label merged as another legacy reference, not another entity.", [entity["id"]], quarantine=True)
            else:
                mark(item, "quarantined", "duplicate_of_unmatched_or_noncurrent_record", "Duplicate representation could not be tied to a migrated current municipality.", quarantine=True)
        else:
            mark(item, "quarantined", "unsupported_libya_record", "Record was not part of the separately modeled current-municipality or historical-sha‘biya pilot layers.", quarantine=True)

    # Account for every remaining row without inventing sources or entities.
    for item in legacy:
        key = (item["path"], item["row"])
        if key in ledger_by_key:
            continue
        row = item["raw"]
        if item["path"].endswith("العواصم_والمدن_الكبرى.csv"):
            code = "duplicate_cross_file_representation"
            reason = "Aggregate capital row duplicates country files and is not authoritative under Schema v1."
        elif "+" in row.get("النوع", ""):
            code = "mixed_entity_types"
            reason = "Legacy row conflates more than one entity type and cannot be imported as one Entity."
        elif not scalar(row.get("المصدر")) or row.get("المصدر") == "ملف المدينة في المشروع":
            code = "missing_atomic_canonical_source"
            reason = "No atomic canonical external source is available for this legacy row."
        else:
            code = "country_layer_pending_source_review"
            reason = "Country is outside the Tunisia/Libya pilot and the legacy source label lacks verified atomic metadata and hierarchy mapping."
        mark(item, "quarantined", code, reason, quarantine=True)

    # Atomic source candidates preserve every distinct legacy label without promoting it.
    source_candidates: dict[str, dict[str, Any]] = {}
    for item in legacy:
        label = scalar(item["raw"].get("المصدر"))
        if not label:
            continue
        key = norm_name(label)
        candidate = source_candidates.setdefault(key, {
            "id": "QSRC-" + stable_token("legacy-source-label", label),
            "raw_label": label,
            "occurrences": 0,
            "sample_paths": [],
            "disposition": "not_promoted",
            "reason": "Legacy label is not an atomic bibliographic record with verified title, URL, publication date, retrieval date, license, and locator.",
        })
        candidate["occurrences"] += 1
        sample = f"{item['path']}:{item['row']}"
        if len(candidate["sample_paths"]) < 5 and sample not in candidate["sample_paths"]:
            candidate["sample_paths"].append(sample)

    # Snapshots.
    snapshots = [
        {
            "id": SNAPSHOT_MIGRATION,
            "schema_version": SCHEMA_VERSION,
            "title": "Schema v1 legacy migration baseline",
            "captured_at": AS_OF,
            "source_id": SRC_AUDIT,
            "scope": "All 24 legacy CSV files and 22 country manifests",
            "method": "Dependency-free deterministic migration with row-level disposition ledger",
            "checksum": None,
            "notes": "The checksum is represented by per-file Git history and generated-data freshness checks.",
        },
        {
            "id": SNAPSHOT_TN_ADMIN,
            "schema_version": SCHEMA_VERSION,
            "title": "Tunisia governorates and delegations source retrieval",
            "captured_at": AS_OF,
            "source_id": SRC_TN_DELEGATIONS,
            "scope": "Detailed official table listing 24 governorates and 264 delegations",
            "method": "Matched normalized Arabic name and governorate parent against legacy rows; retained one representation per entity",
            "checksum": None,
            "notes": "Temporal coverage is blank on the official page; current-status interpretation remains subject to denominator reconciliation.",
        },
        {
            "id": SNAPSHOT_TN_CENSUS,
            "schema_version": SCHEMA_VERSION,
            "title": "Tunisia RGPH 2014 governorate population snapshot",
            "captured_at": "2014-04-23",
            "source_id": SRC_TN_POPULATION,
            "scope": "24 governorate population values",
            "method": "Exact values transcribed from INS RGPH Volume 3, PDF page 47; legacy rounded mismatches are corrected deterministically",
            "checksum": None,
            "notes": "Volume 0 is a rounded summary and is not evidence for exact values.",
        },
        {
            "id": SNAPSHOT_LY_CURRENT,
            "schema_version": SCHEMA_VERSION,
            "title": "Libya Ministry of Local Government municipality register retrieval",
            "captured_at": AS_OF,
            "source_id": SRC_LY_MUNICIPALITIES,
            "scope": "Retrieved Ministry municipality catalogue; legacy subset matching only; denominator unresolved",
            "method": "Exact normalized Arabic-name matching, with one explicit article variant",
            "checksum": None,
            "notes": "The extraction was used to match identities, not to accept a national denominator. No legal effective date was inferred from retrieval date.",
        },
        {
            "id": SNAPSHOT_LY_HISTORIC,
            "schema_version": SCHEMA_VERSION,
            "title": "Libya 2006 census-region snapshot",
            "captured_at": "2006-04-15",
            "source_id": SRC_LY_CENSUS,
            "scope": "22 historical sha‘biyat/census regions",
            "method": "Migrated to a historical hierarchy distinct from current municipalities",
            "checksum": None,
            "notes": None,
        },
    ]

    denominators: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []

    def add_coverage(iso: str, layer: str, definition: str, value, denominator_status: str, denominator_source, locator, license_value, snapshot_id: str, matched: int, unmatched: int, excluded: int, missing, complete: bool, missing_reason, notes=None, as_of=AS_OF):
        den_id = f"DEN-{iso}-{layer.replace('_', '-').upper()}"
        cov_id = f"COV-{iso}-{layer.replace('_', '-').upper()}"
        pct = None
        if denominator_status == "official" and isinstance(value, int) and value >= 0:
            pct = round((matched / value * 100), 4) if value else (100.0 if matched == 0 else None)
        denominators.append({
            "id": den_id,
            "schema_version": SCHEMA_VERSION,
            "country_code": iso,
            "layer": layer,
            "definition": definition,
            "value": value,
            "as_of": as_of,
            "status": denominator_status,
            "source_id": denominator_source,
            "source_locator": locator,
            "license": license_value,
            "missing_reason": missing_reason if value is None else None,
            "notes": notes,
        })
        coverage.append({
            "id": cov_id,
            "schema_version": SCHEMA_VERSION,
            "country_code": iso,
            "layer": layer,
            "snapshot_id": snapshot_id,
            "denominator_id": den_id,
            "source_id": denominator_source,
            "matched": matched,
            "unmatched": unmatched,
            "excluded": excluded,
            "missing": missing,
            "coverage_percent": pct,
            "complete": complete,
            "missing_reason": missing_reason,
            "notes": notes,
        })
        return cov_id

    coverage_by_iso: dict[str, list[str]] = defaultdict(list)
    for iso in COUNTRIES:
        coverage_by_iso[iso].append(add_coverage(
            iso, "country_scope", "ISO country entity in the project's 22-country scope", 1, "official", SRC_ISO,
            f"ISO alpha-2 entry {iso}", "ISO copyright; reuse is subject to ISO terms of use", SNAPSHOT_MIGRATION,
            1, 0, 0, 0, True, None,
            notes="This 100% applies only to the one-record country-scope layer, not to cities, villages, neighborhoods, lanes, or administrative tiers.",
        ))

    coverage_by_iso["TN"].extend([
        add_coverage("TN", "governorates", "Governorates listed in the official detailed table", 24, "official", SRC_TN_DELEGATIONS, "24 governorate rows", "License not stated on source page", SNAPSHOT_TN_ADMIN, 24, 0, 24, 0, True, None, "The 24 excluded rows are duplicate legacy representations."),
        add_coverage("TN", "delegations", "Delegations in the official detailed governorate-by-governorate table", 264, "official", SRC_TN_DELEGATIONS, "Detailed table; counts sum to 264", "License not stated on source page", SNAPSHOT_TN_ADMIN, len(tn_delegation), 0, 264, max(0, 264-len(tn_delegation)), len(tn_delegation) == 264, None if len(tn_delegation) == 264 else "Legacy names did not match the full detailed list", "A separate official count page has shown a conflicting later total; the 100% value applies strictly to this dated/retrieved 264-row detailed-table snapshot."),
        add_coverage("TN", "municipalities_2018", "Municipalities after the 2016 national remapping, as reported in the dated 2018 synthesis", 350, "official", SRC_TN_MUNICIPALITIES, "Administrative overview and new municipal map", "License not stated in publication metadata", SNAPSHOT_MIGRATION, 0, 0, 0, 350, False, "No municipality entities were present in a source-compliant legacy layer and none were mass-added.", as_of="2018-04-06"),
        add_coverage("TN", "imadas", "Territorial sectors (imadas) by governorate and delegation", None, "unavailable", SRC_TN_IMADAS, "Dataset metadata; temporal coverage blank", "License not stated on source page", SNAPSHOT_MIGRATION, 0, 0, 0, None, False, "No dated national denominator was verified and no imada rows were imported."),
        add_coverage("TN", "cities", "Officially delimited city/place layer", None, "unavailable", None, None, None, SNAPSHOT_MIGRATION, 0, 1, 0, None, False, "No official national city denominator and no canonical source for the lone legacy Djerba city row."),
        add_coverage("TN", "populated_settlements", "Officially available populated settlements below the declared administrative tiers", None, "unavailable", None, None, None, SNAPSHOT_MIGRATION, 0, 0, 57, None, False, "No official dated denominator; legacy microplace/cultural rows remain quarantined pending atomic place-level sources."),
    ])

    ly_current_count = len(ly_current)
    coverage_by_iso["LY"].extend([
        add_coverage("LY", "current_municipalities", "Current municipalities in the Ministry of Local Government register", None, "unavailable", SRC_LY_MUNICIPALITIES, "Map-heavy national catalogue; extracted sequence has gaps and was not accepted as a denominator", "License not stated on source page", SNAPSHOT_LY_CURRENT, ly_current_count, ly_unmatched_primary, 90, None, False, "A dated, reproducible national denominator remains unresolved; legacy material is only a matched subset and missing municipalities were not guessed or mass-added."),
        add_coverage("LY", "historical_shabiyat_2006", "Historical census regions represented in the 2006 Bureau of Statistics tables", 22, "official", SRC_LY_CENSUS, "22 regional census tables/entries", "License not stated on source page", SNAPSHOT_LY_HISTORIC, 22, 0, 0, 0, True, None, "This 100% is a historical 2006 layer only and says nothing about current municipalities." , as_of="2006-04-15"),
        add_coverage("LY", "mahallas", "Current mahallas beneath municipalities", None, "unavailable", SRC_LY_MUNICIPALITIES, "Municipality profile pages list mahallas unevenly", "License not stated on source page", SNAPSHOT_LY_CURRENT, 0, 0, 0, None, False, "No dated national denominator or complete source snapshot was verified."),
    ])

    manifests = make_manifests(coverage_by_iso)

    # Persist active and quarantine data.
    write_jsonl(DATA / "entities/entities.jsonl", entities)
    write_jsonl(DATA / "aliases/aliases.jsonl", aliases)
    write_jsonl(DATA / "relationships/relationships.jsonl", relationships)
    write_jsonl(DATA / "claims/claims.jsonl", claims)
    write_jsonl(DATA / "snapshots/snapshots.jsonl", snapshots)
    write_jsonl(DATA / "coverage/denominators.jsonl", denominators)
    write_jsonl(DATA / "coverage/coverage.jsonl", coverage)
    write_jsonl(DATA / "quarantine/migration_ledger.jsonl", ledger_by_key.values())
    write_jsonl(DATA / "quarantine/legacy_rows.jsonl", quarantined)
    write_jsonl(DATA / "quarantine/legacy_source_candidates.jsonl", source_candidates.values())

    dispositions = Counter(entry["disposition"] for entry in ledger_by_key.values())
    reasons = Counter(entry["reason_code"] for entry in ledger_by_key.values())
    summary = {
        "schema_version": SCHEMA_VERSION,
        "as_of": AS_OF,
        "legacy_rows": len(legacy),
        "ledger_rows": len(ledger_by_key),
        "quarantined_copies": len(quarantined),
        "dispositions": dict(sorted(dispositions.items())),
        "reasons": dict(sorted(reasons.items())),
        "active_counts": {
            "entities": len(entities),
            "aliases": len(aliases),
            "relationships": len(relationships),
            "claims": len(claims),
            "sources": len(sources),
            "snapshots": len(snapshots),
            "denominators": len(denominators),
            "coverage": len(coverage),
        },
        "pilot_counts": {
            "tunisia_governorates": len(tn_gov),
            "tunisia_delegations": len(tn_delegation),
            "libya_current_legacy_matches": ly_current_count,
            "libya_current_legacy_unmatched": ly_unmatched_primary,
            "libya_historical_shabiyat": 22,
        },
    }
    write_json(DATA / "quarantine/quarantine_summary.json", summary)
    return summary


# Local hierarchy definitions: every country records its own names; pending means not yet source-verified.
HIERARCHIES = {
    "JO": [("jo_governorate", ["محافظة"], ["country"]), ("jo_liwa", ["لواء"], ["jo_governorate"]), ("jo_qada", ["قضاء"], ["jo_liwa"]), ("jo_municipality", ["بلدية"], ["jo_governorate", "jo_liwa"])],
    "AE": [("ae_emirate", ["إمارة"], ["country"]), ("ae_municipal_region", ["منطقة بلدية"], ["ae_emirate"]), ("ae_sector", ["قطاع"], ["ae_emirate", "ae_municipal_region"]), ("ae_district", ["منطقة/حي وفق نظام الإمارة"], ["ae_sector", "ae_municipal_region"])],
    "BH": [("bh_governorate", ["محافظة"], ["country"]), ("bh_area", ["منطقة"], ["bh_governorate"]), ("bh_block", ["مجمّع"], ["bh_area"])],
    "DZ": [("dz_wilaya", ["ولاية"], ["country"]), ("dz_daira", ["دائرة"], ["dz_wilaya"]), ("dz_commune", ["بلدية"], ["dz_daira"])],
    "SA": [("sa_region", ["منطقة إدارية"], ["country"]), ("sa_governorate", ["محافظة"], ["sa_region"]), ("sa_markaz", ["مركز"], ["sa_governorate"])],
    "SD": [("sd_state", ["ولاية"], ["country"]), ("sd_locality", ["محلية"], ["sd_state"]), ("sd_administrative_unit", ["وحدة إدارية"], ["sd_locality"])],
    "SO": [("so_federal_member_state", ["ولاية/عضو اتحادي"], ["country"]), ("so_region", ["غوبول/إقليم"], ["country", "so_federal_member_state"]), ("so_district", ["دِغمو/مقاطعة"], ["so_region"])],
    "IQ": [("iq_governorate", ["محافظة"], ["country"]), ("iq_district", ["قضاء"], ["iq_governorate"]), ("iq_subdistrict", ["ناحية"], ["iq_district"])],
    "KW": [("kw_governorate", ["محافظة"], ["country"]), ("kw_area", ["منطقة"], ["kw_governorate"]), ("kw_block", ["قطعة"], ["kw_area"])],
    "MA": [("ma_region", ["جهة"], ["country"]), ("ma_prefecture", ["عمالة"], ["ma_region"]), ("ma_province", ["إقليم"], ["ma_region"]), ("ma_commune", ["جماعة"], ["ma_prefecture", "ma_province"])],
    "YE": [("ye_governorate", ["محافظة"], ["country"]), ("ye_capital_municipality", ["أمانة العاصمة"], ["country"]), ("ye_district", ["مديرية"], ["ye_governorate", "ye_capital_municipality"]), ("ye_uzla", ["عزلة"], ["ye_district"])],
    "TN": [("tn_governorate", ["ولاية"], ["country"]), ("tn_delegation", ["معتمدية"], ["tn_governorate"]), ("tn_imada", ["عمادة/قطاع ترابي"], ["tn_delegation"]), ("tn_municipality", ["بلدية"], ["country", "tn_governorate"])],
    "KM": [("km_island", ["جزيرة ذاتية الحكم"], ["country"]), ("km_prefecture", ["محافظة/Préfecture"], ["km_island"]), ("km_commune", ["بلدية/Commune"], ["km_prefecture"])],
    "DJ": [("dj_region", ["إقليم"], ["country"]), ("djibouti_city", ["مدينة جيبوتي ذات وضع خاص"], ["country"]), ("dj_subprefecture", ["مقاطعة فرعية"], ["dj_region"]), ("dj_commune", ["بلدية"], ["djibouti_city", "dj_region"])],
    "SY": [("sy_governorate", ["محافظة"], ["country"]), ("sy_district", ["منطقة"], ["sy_governorate"]), ("sy_subdistrict", ["ناحية"], ["sy_district"])],
    "OM": [("om_governorate", ["محافظة"], ["country"]), ("om_wilaya", ["ولاية"], ["om_governorate"]), ("om_niyaba", ["نيابة"], ["om_wilaya"])],
    "PS": [("ps_governorate", ["محافظة"], ["country"]), ("ps_local_government_unit", ["هيئة محلية/بلدية/مجلس قروي"], ["ps_governorate"])],
    "QA": [("qa_municipality", ["بلدية"], ["country"]), ("qa_zone", ["منطقة مرقمة"], ["qa_municipality"]), ("qa_district", ["حي/فريج"], ["qa_zone"])],
    "LB": [("lb_governorate", ["محافظة"], ["country"]), ("lb_district", ["قضاء"], ["lb_governorate"]), ("lb_municipality", ["بلدية"], ["lb_district"])],
    "LY": [("ly_municipality", ["بلدية"], ["country"]), ("ly_mahalla", ["محلة"], ["ly_municipality"]), ("ly_shabiya_historical", ["شعبية تاريخية"], ["country"])],
    "EG": [("eg_governorate", ["محافظة"], ["country"]), ("eg_markaz", ["مركز"], ["eg_governorate"]), ("eg_qism", ["قسم"], ["eg_governorate"]), ("eg_local_unit", ["وحدة محلية"], ["eg_markaz"]), ("eg_shiyakha", ["شياخة"], ["eg_qism"])],
    "MR": [("mr_wilaya", ["ولاية"], ["country"]), ("mr_moughataa", ["مقاطعة"], ["mr_wilaya"]), ("mr_commune", ["بلدية"], ["mr_moughataa"])],
}

AUTHORITIES = {
    "JO": "وزارة الداخلية الأردنية / دائرة الإحصاءات العامة",
    "AE": "الهيئة الاتحادية للتنافسية والإحصاء والسلطات المحلية لكل إمارة",
    "BH": "هيئة المعلومات والحكومة الإلكترونية",
    "DZ": "وزارة الداخلية والجماعات المحلية والتهيئة العمرانية",
    "SA": "وزارة الداخلية / الهيئة العامة للإحصاء",
    "SD": "الجهاز المركزي للإحصاء والسلطات الإدارية المختصة",
    "SO": "وزارة الداخلية والشؤون الفيدرالية وسلطات الولايات؛ الاختصاص متنازع/متغير",
    "IQ": "وزارة التخطيط / الجهاز المركزي للإحصاء",
    "KW": "الهيئة العامة للمعلومات المدنية",
    "MA": "وزارة الداخلية / المندوبية السامية للتخطيط",
    "YE": "وزارة الإدارة المحلية / الجهاز المركزي للإحصاء",
    "TN": "وزارة الداخلية / الإدارة العامة للشؤون الجهوية / المعهد الوطني للإحصاء",
    "KM": "وزارة الداخلية / المعهد الوطني للإحصاء والدراسات الاقتصادية والديمغرافية",
    "DJ": "المعهد الوطني للإحصاء / وزارة الداخلية",
    "SY": "وزارة الإدارة المحلية والبيئة / المكتب المركزي للإحصاء",
    "OM": "وزارة الداخلية / المركز الوطني للإحصاء والمعلومات",
    "PS": "وزارة الحكم المحلي / الجهاز المركزي للإحصاء الفلسطيني",
    "QA": "وزارة البلدية / جهاز التخطيط والإحصاء",
    "LB": "المديرية العامة للإدارات والمجالس المحلية / وزارة الداخلية والبلديات",
    "LY": "وزارة الحكم المحلي / مصلحة الإحصاء والتعداد",
    "EG": "وزارة التنمية المحلية / الجهاز المركزي للتعبئة العامة والإحصاء",
    "MR": "وزارة الداخلية / الوكالة الوطنية للإحصاء والتحليل الديمغرافي والاقتصادي",
}

CAVEATS = {
    "JO": "تحتاج أعداد الألوية والأقضية والبلديات إلى لقطة رسمية مؤرخة قبل الترقية.",
    "AE": "لا يوجد هرم سفلي اتحادي موحد؛ يجب نمذجة نظام كل إمارة على حدة.",
    "BH": "يجب عدم مساواة المحافظات بالمناطق أو الدوائر الانتخابية أو المجمعات.",
    "DZ": "الولايات المنتقلة إلى كامل الصلاحيات في 2027 يجب تمييزها كمرحلة انتقالية حتى النفاذ.",
    "SA": "المدينة والمحافظة والمركز كيانات مختلفة؛ الصفوف المركبة القديمة محجورة.",
    "SD": "الحرب منذ 2023 وتغير السيطرة يفرضان فصل القانوني والفعلي واللقطات الزمنية.",
    "SO": "البنية الاتحادية والتقسيمات القانونية والفعلية والمتنازع عليها لا تُدمج في شجرة واحدة.",
    "IQ": "حلبجة أصبحت محافظة في 2025؛ يلزم مصدر رسمي مؤرخ لمسارها الحالي.",
    "KW": "المنطقة والقطعة وحدات عنونة/إحصاء ولا تُعاملان تلقائيًا كبلديات.",
    "MA": "تعارض مقامات الجماعات في المصادر الثانوية يمنع أي ادعاء اكتمال قبل سجل رسمي مؤرخ.",
    "YE": "أمانة العاصمة وضع خاص موازٍ للمحافظات؛ الحرب تفرض فصل القانوني والفعلي.",
    "TN": "جدول الوزارة التفصيلي يسرد 264 معتمدية بينما ظهرت أعداد رسمية أحدث متعارضة؛ يلزم reconciliation قبل وصف الطبقة بأنها حالية بلا قيد.",
    "KM": "تتعارض المراجع حول عدد المحافظات/البلديات؛ لا يُملأ المقام بالتخمين.",
    "DJ": "وضع مدينة جيبوتي والبلديات/المقاطعات الفرعية يحتاج مسارات اختصاص منفصلة.",
    "SY": "أعداد المناطق والنواحي والتغيرات الفعلية متعارضة؛ لا تخلط السيطرة الفعلية بالقانونية.",
    "OM": "المحافظة والولاية والنيابة درجات مختلفة، ولا يُشتق اكتمالها من وجود ملفات.",
    "PS": "يجب فصل المحافظة والهيئة المحلية والمخيم والتجمع، مع توثيق القيود والسيطرة دون تسوية النزاع.",
    "QA": "البلدية والمنطقة المرقمة والفريج ليست مترادفات.",
    "LB": "محافظة كسروان-جبيل المنفذة حديثًا تغيّر المقام؛ يلزم snapshot رسمي موحد.",
    "LY": "الشعبيات التاريخية منفصلة كليًا عن البلديات الحالية؛ القائمة الحالية متغيرة والمواد القديمة تغطي subset فقط.",
    "EG": "المركز والقسم مساران ريفي/حضري متوازيان، والشياخة لا توضع تحت المركز تلقائيًا.",
    "MR": "تعارض أعداد المقاطعات والبلديات يمنع النسبة حتى توثيق مقام رسمي مؤرخ.",
}


def make_manifests(coverage_by_iso: dict[str, list[str]]) -> dict[str, dict[str, Any]]:
    out = ROOT / "manifests"
    out.mkdir(parents=True, exist_ok=True)
    manifests = {}
    for iso, (name_ar, _name_en) in COUNTRIES.items():
        pilot = iso in {"TN", "LY"}
        if iso == "TN":
            authority_sources = [SRC_TN_DELEGATIONS, SRC_TN_POPULATION, SRC_TN_MUNICIPALITIES, SRC_TN_IMADAS]
            authority_status = "conflicted"
            missing_reason = None
        elif iso == "LY":
            authority_sources = [SRC_LY_MUNICIPALITIES, SRC_LY_LAW59, SRC_LY_CENSUS]
            authority_status = "partial"
            missing_reason = None
        else:
            authority_sources = []
            authority_status = "pending"
            missing_reason = "Authority name is recorded, but no atomic official hierarchy source has yet passed source metadata and snapshot review."

        hierarchy = [{
            "level": 0,
            "entity_type": "country",
            "local_names": ["دولة"],
            "allowed_parent_types": [],
            "temporal_statuses": ["current", "historical", "disputed", "de_facto", "claimed"],
            "source_ids": [SRC_ISO],
            "verification_status": "verified",
            "caveat": "Country scope only; not a local coverage assertion.",
        }]
        for level, (etype, local_names, parents) in enumerate(HIERARCHIES[iso], 1):
            if iso == "TN":
                ids = [SRC_TN_DELEGATIONS] if etype in {"tn_governorate", "tn_delegation"} else ([SRC_TN_IMADAS] if etype == "tn_imada" else [SRC_TN_MUNICIPALITIES])
                verification = "verified" if etype in {"tn_governorate", "tn_delegation"} else "partial"
            elif iso == "LY":
                ids = [SRC_LY_CENSUS] if etype == "ly_shabiya_historical" else [SRC_LY_MUNICIPALITIES]
                verification = "historical" if etype == "ly_shabiya_historical" else ("verified" if etype == "ly_municipality" else "partial")
            else:
                ids = []
                verification = "pending"
            hierarchy.append({
                "level": level,
                "entity_type": etype,
                "local_names": local_names,
                "allowed_parent_types": parents,
                "temporal_statuses": ["current", "historical", "destroyed", "displaced", "disputed", "de_facto", "claimed", "proposed", "transitional", "uncertain"],
                "source_ids": ids,
                "verification_status": verification,
                "caveat": CAVEATS[iso] if verification != "verified" else None,
            })

        manifest = {
            "schema_version": SCHEMA_VERSION,
            "country": {"iso2": iso, "name_ar": name_ar, "entity_id": f"ENT-{iso}-COUNTRY"},
            "status": "pilot_migrated" if pilot else "baseline_only",
            "official_authority": {
                "name": AUTHORITIES[iso],
                "source_ids": authority_sources,
                "verification_status": authority_status,
                "missing_reason": missing_reason,
            },
            "snapshot": {
                "as_of": AS_OF,
                "snapshot_id": SNAPSHOT_TN_ADMIN if iso == "TN" else (SNAPSHOT_LY_CURRENT if iso == "LY" else SNAPSHOT_MIGRATION),
                "status": "partial" if pilot else "baseline",
            },
            "hierarchy": hierarchy,
            "coverage_record_ids": coverage_by_iso[iso],
            "caveats": [CAVEATS[iso], "Local coverage remains incomplete; file or directory existence is not a denominator."],
            "next_action": "Reconcile pilot denominators and missing official tiers before local expansion." if pilot else "Register an atomic official hierarchy source and dated denominators before migrating local legacy rows.",
        }
        manifests[iso] = manifest
        # JSON is valid YAML 1.2 and keeps validation dependency-free.
        write_json(out / f"{iso}.yml", manifest)
    return manifests


def main() -> int:
    summary = migrate()
    print(json.dumps(summary["active_counts"], ensure_ascii=False, sort_keys=True))
    print(json.dumps(summary["pilot_counts"], ensure_ascii=False, sort_keys=True))
    print(f"legacy rows accounted: {summary['ledger_rows']}/{summary['legacy_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
