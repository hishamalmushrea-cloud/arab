#!/usr/bin/env python3
"""Deterministically materialize Bahrain's first production expansion."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable

from build_bahrain_sources import main as build_sources
from model import ROOT, SCHEMA_VERSION, read_jsonl, record_id, write_json, write_jsonl

IMPORT = ROOT / "data/imports/bahrain"
AREA = IMPORT / "fixtures/area_by_governorate_2024.json"
WHC = IMPORT / "fixtures/world_heritage_2026.json"
SNAPSHOT_MANIFEST = IMPORT / "snapshot_manifest.json"
SNAPSHOT_DATE = "2026-08-16"
SNAPSHOT_ID = "SNP-BH-PRODUCTION-20260816"
AREA_SOURCE = "SRC-BH-SLRB-GOVERNORATE-AREA-2024"
WHC_REGISTER = "SRC-UNESCO-WHC-BH-2026"
OPEN_LICENSE = "Bahrain Open Data Policy: republication and distribution permitted, subject to applicable laws"
WHC_LICENSE = "CC BY-SA 3.0 IGO for property descriptions"
DEPTH = IMPORT / "fixtures/cultural_depth_2026.json"
DEPTH_DATE = "2026-09-20"
ICH_SOURCE = "SRC-BH-UNESCO-ICH-2026"
FJIRI_SOURCE = "SRC-BH-FJIRI-01747"
MUHARRAQ = "ENT-BH-GOVERNORATE-MUHARRAQ"
CITY_MUHARRAQ = "ENT-BH-CITY-MUHARRAQ"
DEPTH_SOURCES = {
    "dialect_mirror": "SRC-BH-DIALECT-MIRROR-2026",
    "cuisine_mirror": "SRC-BH-CUISINE-MIRROR-2026",
    "folk_cloth": "SRC-BH-FOLK-CLOTH-2022",
    "nashil_press": "SRC-BH-NASHIL-PRESS-2018",
    "muharraq_wiki": "SRC-BH-MUHARRAQ-WIKI-2026",
    "firjan_blog": "SRC-BH-FIRJAN-BLOG-2022",
    "firjan_elaph": "SRC-BH-FIRJAN-ELAPH-2023",
    "albilad_press": "SRC-BH-ALBILAD-2021",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def replace(path: Path, predicate: Callable[[dict[str, Any]], bool], additions: list[dict[str, Any]]) -> None:
    write_jsonl(path, [row for row in read_jsonl(path) if not predicate(row)] + additions)


def typed(value: Any) -> dict[str, Any]:
    if isinstance(value, bool): kind = "boolean"
    elif isinstance(value, int): kind = "integer"
    elif isinstance(value, float): kind = "number"
    elif isinstance(value, (dict, list)): kind = "json"
    else: kind = "string"
    return {"type": kind, "data": value}


def claim(key: str, subject: str, predicate: str, value: Any, source: str, locator: str,
          classification: str | None, observed: str, notes: str | None = None, unit: str | None = None) -> dict:
    return {
        "id": record_id("CLM-BH", key), "schema_version": SCHEMA_VERSION,
        "subject_id": subject, "predicate": predicate, "value": typed(value), "unit": unit,
        "status": "verified", "observed_at": observed, "valid_from": None, "valid_to": None,
        "source_id": source, "second_source_id": None, "source_locator": locator,
        "sensitivity": "ordinary", "notes": notes, "verification_status": "source_verified",
        "confidence": "high", "classification": classification, "published": True,
        "second_source_locator": None, "lexical_context": None,
    }


def entity(identifier: str, name: str, entity_type: str, source: str, locator: str, notes: str) -> dict:
    return {
        "id": identifier, "schema_version": SCHEMA_VERSION, "country_code": "BH",
        "canonical_name": name, "canonical_name_language": "ar" if any("\u0600" <= c <= "\u06ff" for c in name) else "en",
        "entity_type": entity_type, "status": "current", "valid_from": None, "valid_to": None,
        "canonical_source_id": source, "source_locator": locator, "legacy_ids": [],
        "coordinates": None, "notes": notes, "verification_status": "source_verified", "confidence": "high",
    }


def alias(entity_id: str, name: str, language: str, source: str, locator: str) -> dict:
    return {
        "id": record_id("ALS-BH", entity_id, name, language), "schema_version": SCHEMA_VERSION,
        "entity_id": entity_id, "name": name, "language": language,
        "script": "Arab" if language == "ar" else "Latn", "kind": "official_variant",
        "status": "current", "source_id": source, "source_locator": locator,
        "valid_from": None, "valid_to": None,
    }


def relationship(child: str, parent: str, kind: str, source: str, locator: str) -> dict:
    return {
        "id": record_id("REL-BH", kind, child, parent), "schema_version": SCHEMA_VERSION,
        "child_id": child, "parent_id": parent, "relationship_type": kind, "status": "current",
        "valid_from": None, "valid_to": None, "source_id": source, "source_locator": locator,
        "notes": "The relation is limited to the source-backed layer; areas, electoral districts, and blocks are not inferred.",
        "verification_status": "source_verified", "confidence": "high",
    }


def denominator(identifier: str, layer: str, value: int, as_of: str, source: str, locator: str,
                license_text: str, definition: str) -> dict:
    return {
        "id": identifier, "schema_version": SCHEMA_VERSION, "country_code": "BH", "layer": layer,
        "definition": definition, "value": value, "as_of": as_of, "status": "official",
        "source_id": source, "source_locator": locator, "license": license_text,
        "missing_reason": None, "notes": definition, "denominator": value, "snapshot_date": as_of,
    }


def coverage(identifier: str, layer: str, denominator_id: str, value: int, source: str,
             license_text: str, notes: str) -> dict:
    return {
        "id": identifier, "schema_version": SCHEMA_VERSION, "country_code": "BH", "layer": layer,
        "snapshot_id": SNAPSHOT_ID, "denominator_id": denominator_id, "source_id": source,
        "matched": value, "unmatched": 0, "excluded": 0, "missing": 0, "complete": True,
        "missing_reason": None, "notes": notes, "denominator": value, "snapshot_date": SNAPSHOT_DATE,
        "license": license_text, "coverage_percentage": 100.0, "exclusion_reasons": [],
    }


def depth_claim(key: str, subject: str, predicate: str, value: Any, source: str, locator: str,
                classification: str, notes: str, verification: str = "local_reported",
                confidence: str = "low", status: str = "reported",
                published: bool = False) -> dict:
    return {
        "id": record_id("CLM-BH-DEPTH", key), "schema_version": SCHEMA_VERSION,
        "subject_id": subject, "predicate": predicate, "value": typed(value), "unit": None,
        "status": status, "observed_at": DEPTH_DATE, "valid_from": None, "valid_to": None,
        "source_id": source, "second_source_id": None, "source_locator": locator,
        "sensitivity": "ordinary", "notes": notes, "verification_status": verification,
        "confidence": confidence, "classification": classification, "published": published,
        "second_source_locator": None, "lexical_context": None,
    }


def locator_text(row: dict) -> str:
    """Every depth row carries its own bounded locator; press/forum rows never become verified facts."""
    return row.get("locator") or row.get("note") or row.get("desc") or row["name"]


def place(identifier: str, name: str, entity_type: str, status: str, source: str, locator: str,
          notes: str) -> dict:
    return {
        "id": identifier, "schema_version": SCHEMA_VERSION, "country_code": "BH",
        "canonical_name": name, "canonical_name_language": "ar", "entity_type": entity_type,
        "status": status, "valid_from": None, "valid_to": None, "canonical_source_id": source,
        "source_locator": locator, "legacy_ids": [], "coordinates": None, "notes": notes,
        "verification_status": "local_reported", "confidence": "low",
    }


def located(child: str, parent: str, status: str, source: str, locator: str, notes: str) -> dict:
    return {
        "id": record_id("REL-BH-LOCATED", child, parent), "schema_version": SCHEMA_VERSION,
        "child_id": child, "parent_id": parent, "relationship_type": "located_in",
        "status": status, "valid_from": None, "valid_to": None, "source_id": source,
        "source_locator": locator, "notes": notes, "verification_status": "local_reported",
        "confidence": "low",
    }


def depth_items(depth: dict) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    """Depth cycle 1: UNESCO list spinal facts stay published; all local material stays classified and unpublished."""
    entities: list[dict] = []
    aliases: list[dict] = []
    relationships: list[dict] = []
    claims: list[dict] = []
    places = depth["places"]
    city_locator = "موسوعة مرآة المحرق (مدينة): توصيف المدينة وأحيائها وفرجانها ومصطلحي الداعوس والزرنوق"
    entities.append(place(CITY_MUHARRAQ, "مدينة المحرق", "city", "current", DEPTH_SOURCES["muharraq_wiki"],
                          city_locator,
                          "مدينة قائمة في جزيرة المحرق؛ أول عقدة مدينة في طبقة العمق البحرينية. لا تُعامل وحدة إدارية ولا يُنسب إليها سكان."))
    relationships.append(located(CITY_MUHARRAQ, MUHARRAQ, "current", DEPTH_SOURCES["muharraq_wiki"], city_locator,
                                 "وقوع مدينة المحرق داخل محافظة المحرق: علاقة مكانية لا إدارية، لعدم وجود إسناد رسمي لطبقة أدنى."))
    firij_ids: dict[str, str] = {}
    for row in places["firjan"]:
        source = DEPTH_SOURCES[row["source"]]
        locator = locator_text(row)
        identifier = record_id("ENT-BH-FIRIJ", row["name"])
        firij_ids[row["name"]] = identifier
        entities.append(place(identifier, row["name"], "quarter", "historical", source, locator,
                              row["note"] + " فريج تاريخي داخل مدينة المحرق بوصف مصدر محلي؛ لا صفة إدارية حالية ولا سكان."))
        relationships.append(located(identifier, CITY_MUHARRAQ, "historical", source, locator,
                                     "فريج تابع تاريخيًا لمدينة المحرق؛ لا أب إداري ولا دعوى سكان."))
    for row in places["villages"] + places["halat"]:
        source = DEPTH_SOURCES[row["source"]]
        locator = locator_text(row)
        identifier = record_id("ENT-BH-VILLAGE", row["name"])
        entities.append(place(identifier, row["name"], "village", "current", source, locator,
                              row["note"] + " مستوطنة قائمة في جزيرة المحرق بوصف صحفي محلي؛ لا صفة إدارية ولا أرقام سكان."))
        relationships.append(located(identifier, MUHARRAQ, "current", source, locator,
                                     "وقوع القرية أو الحالة داخل محافظة المحرق: علاقة مكانية لا إدارية."))
    for element in depth["ich_elements"]:
        source = FJIRI_SOURCE if element["reference"] == "01747" else ICH_SOURCE
        locator = f"قائمة اليونسكو للتراث الثقافي غير المادي: {element['official_title']} ({element['year']}, {element['list']}, ref {element['reference']})"
        claims.append(depth_claim(
            f"ich|{element['name']}", "ENT-BH-COUNTRY", element["predicate"],
            {"name": element["name"], "official_title": element["official_title"], "year": element["year"],
             "list": element["list"], "reference": element["reference"], "description": element["description"]},
            source, locator, element["classification"],
            "عنصر مدرج عند اليونسكو مع البحرين. سنة الإدراج داخل القيمة ولا تُحوَّل إلى يوم كامل، والعناصر المشتركة تحمل shared ولا تُنسب حصريًا.",
            verification="verified", confidence="high", status="verified", published=True))
    for row in depth["languages"]:
        source = DEPTH_SOURCES[row["source"]]
        claims.append(depth_claim(
            f"language|{row['name']}", "ENT-BH-COUNTRY", "language_presence",
            {"language": row["name"], "description": row["description"]}, source, row["locator"],
            row["classification"],
            "حضور لغوي غير عربي بوصف صريح ودرجة ثقة معلنة؛ لا يُنشر عدد متحدثين ولا يُبنى عليه مقام رسمي.",
            verification=row["status"], confidence="low"))
    for row in depth["dialect_profiles"]:
        source = DEPTH_SOURCES[row["source"]]
        for word in row["words"]:
            if len(word) != 2:
                raise SystemExit("Bahrain dialect vocabulary entry lacks a gloss")
        claims.append(depth_claim(
            f"dialect|{row['group']}", "ENT-BH-COUNTRY", "dialect_profile",
            {"group": row["group"], "scope": row["scope"], "features": row["features"],
             "sample_words": row["words"], "researcher": row.get("researcher"),
             "sub_varieties": row.get("sub_varieties", [])},
            source, f"{row['group']}: {row['features'][:120]}", "local",
            "وصف لهجي من مصدر محلي مصنّف؛ المفردات بمعانيها، وتنوع اللهجات يُعرض ظاهرة لا يوحّدها اسم واحد.",
            confidence="low"))
    for row in depth["dishes"]:
        claims.append(depth_claim(
            f"dish|{row['name']}", "ENT-BH-COUNTRY", "food_dish",
            {"name": row["name"], "description": row["desc"], "occasion": row["occasion"]},
            DEPTH_SOURCES["cuisine_mirror"], f"طبق بحريني: {row['name']} — {row['occasion']}",
            row["classification"],
            "معرفة طعام محلية من مصدر مرآة؛ الأطباق المشتركة خليجيًا أو المقتبسة تبقى shared أو regional بلا حصرية.",
            confidence="low"))
    for row in depth["dress"]:
        source = DEPTH_SOURCES["folk_cloth"] if row["name"] in {"النفنوف", "العباءة", "الجلابية", "ثوب النقدة (النغذة)"} else DEPTH_SOURCES["nashil_press"]
        claims.append(depth_claim(
            f"dress|{row['name']}", "ENT-BH-COUNTRY", "clothing_item",
            {"name": row["name"], "gender": row["gender"], "description": row["desc"]},
            source, f"زي شعبي بحريني: {row['name']}", row["classification"],
            "وصف اللباس من مادة تراثية أو صحفية محلية؛ يبقى غير منشور حتى مصدر أقوى.",
            confidence="low"))
    for row in depth["crafts"]:
        claims.append(depth_claim(
            f"craft|{row['name']}", "ENT-BH-COUNTRY", "craft_custom",
            {"name": row["name"], "description": row["desc"]},
            DEPTH_SOURCES[row["source"]], f"حرفة/مهنة محلية: {row['name']}", row["classification"],
            "حرفة أو مهنة محلية من مصدر ضعيف الفئة؛ تُعرض وصفًا محليًا لا إحصاءً.",
            confidence="low"))
    narrative = depth["narrative"]
    claims.append(depth_claim(
        f"narrative|{narrative['subject']}", firij_ids[narrative["subject"]], "name_origin_narrative",
        {"text": narrative["text"]},
        DEPTH_SOURCES[narrative["source"]], narrative["locator"], narrative["classification"],
        "رواية تسمية محلية منسوبة إلى مصدرها بالاسم؛ تُعرض رواية لا حقيقة قطعية.",
        verification="local_reported", confidence="low"))
    return entities, aliases, relationships, claims


def main() -> None:
    build_sources()
    area = load(AREA)
    whc = load(WHC)
    if any(x.get("schema_version") != SCHEMA_VERSION or x.get("country_code") != "BH" for x in (area, whc)):
        raise SystemExit("invalid Bahrain fixture identity/version")
    if len(area["records"]) != 4 or len({row["governorate"] for row in area["records"]}) != 4:
        raise SystemExit("Bahrain governorate fixture is not an exact four-record set")
    if whc.get("denominator") != 3 or len(whc["properties"]) != 3:
        raise SystemExit("Bahrain World Heritage fixture is not an exact three-property set")

    entities, aliases, relationships, claims = [], [], [], []
    for row in area["records"]:
        token = row["governorate"].upper().replace(" ", "-")
        eid = f"ENT-BH-GOVERNORATE-{token}"
        locator = f"2024 API record N={row['n']}: {row['governorate_ar']} / {row['governorate']}; area={row['area_km2']} km²"
        entities.append(entity(eid, row["governorate_ar"], "bh_governorate", AREA_SOURCE, locator,
                               "Current governorate in the official 2024 four-record area dataset; no point coordinate is invented for an administrative polygon."))
        aliases.append(alias(eid, row["governorate"], "en", AREA_SOURCE, locator))
        relationships.append(relationship(eid, "ENT-BH-COUNTRY", "administrative_parent", AREA_SOURCE, locator))
        claims.append(claim(f"AREA-{token}-2024", eid, "area", row["area_km2"], AREA_SOURCE, locator,
                            "official", "2024-01-01", "Year precision normalized to 1 January; source reports square kilometres.", "km2"))

    for row in whc["properties"]:
        sid = f"SRC-UNESCO-WHC-BH-{row['reference']}"
        locator = f"World Heritage property {row['reference']}; {row['name_en']}; inscribed {row['inscription_year']}; category Cultural"
        entities.append(entity(row["entity_id"], row["name_en"], row["entity_type"], sid, locator,
                               "One serial World Heritage property entity, not one entity per component part and not an administrative unit."))
        alias_source = "SRC-BH-BACA-PEARLING-PATH" if row["reference"] == 1364 else sid
        aliases.append(alias(row["entity_id"], row["name_ar"], "ar", alias_source,
                             "official Arabic property/project name"))
        relationships.append(relationship(row["entity_id"], "ENT-BH-COUNTRY", "associated_with", sid,
                                          "Bahrain State Party property record; country-level association only"))
        claims.append(claim(f"WHC-{row['reference']}-YEAR", row["entity_id"], "world_heritage_inscription_year",
                            row["inscription_year"], sid, locator, "official", SNAPSHOT_DATE, unit="year"))
        claims.append(claim(f"WHC-{row['reference']}-CATEGORY", row["entity_id"], "world_heritage_category",
                            "cultural", sid, locator, "official", SNAPSHOT_DATE))

    claims.extend([
        claim("QALAT-CHRONOLOGY", "ENT-BH-ARCHAEOLOGICAL-SITE-QALAT-AL-BAHRAIN", "documented_chronology",
              "continuous human presence from about 2300 BCE to the 16th century CE", "SRC-UNESCO-WHC-BH-1192",
              "property 1192 brief description; occupation chronology", "historical", SNAPSHOT_DATE),
        claim("PEARLING-ROUTE", "ENT-BH-CULTURAL-SITE-PEARLING", "heritage_route_extent",
              "more than 3 kilometres from the pearling oyster beds near Qal’at Bu Mahir to Siyadi House in Muharraq",
              "SRC-BH-BACA-PEARLING-PATH", "official Arabic Pearling Path project description", "official", SNAPSHOT_DATE),
        claim("DILMUN-MOUNDS-CHRONOLOGY", "ENT-BH-ARCHAEOLOGICAL-SITE-DILMUN-BURIAL-MOUNDS", "documented_chronology",
              "built between 2200 and 1750 BCE across 21 archaeological component sites", "SRC-UNESCO-WHC-BH-1542",
              "property 1542 brief description; construction range and serial component count", "historical", SNAPSHOT_DATE),
    ])

    depth = load(DEPTH)
    if depth.get("schema_version") != SCHEMA_VERSION or depth.get("country_code") != "BH":
        raise SystemExit("invalid Bahrain depth fixture identity/version")
    if (len(depth["ich_elements"]), len(depth["languages"]), len(depth["dialect_profiles"]),
            len(depth["dishes"]), len(depth["dress"]), len(depth["crafts"])) != (5, 1, 3, 23, 7, 3):
        raise SystemExit("invalid Bahrain depth fixture counts")
    if len(depth["places"]["firjan"]) != 14 or len(depth["places"]["villages"]) != 6 or len(depth["places"]["halat"]) != 3:
        raise SystemExit("invalid Bahrain firjan/village fixture counts")
    depth_entities, depth_aliases, depth_relationships, depth_claims = depth_items(depth)
    entities.extend(depth_entities)
    aliases.extend(depth_aliases)
    relationships.extend(depth_relationships)
    claims.extend(depth_claims)

    denoms = [
        denominator("DEN-BH-GOVERNORATES-2024", "bh_governorate", 4, "2024-01-01", AREA_SOURCE,
                    "2024 filter returns exactly four named governorate records", OPEN_LICENSE,
                    "All current governorates enumerated by the official 2024 area dataset; Central is absent after the documented 2014 redivision."),
        denominator("DEN-BH-WHC-20260816", "world_heritage_property", 3, SNAPSHOT_DATE, WHC_REGISTER,
                    "Bahrain State Party list: three inscribed properties", WHC_LICENSE,
                    "All inscribed World Heritage properties for Bahrain at the retrieval snapshot; six tentative-list sites are excluded by definition."),
    ]
    covs = [
        coverage("COV-BH-GOVERNORATES-2024", "bh_governorate", "DEN-BH-GOVERNORATES-2024", 4,
                 AREA_SOURCE, OPEN_LICENSE, "Four matched current governorates; no areas, constituencies, or blocks are counted."),
        coverage("COV-BH-WHC-20260816", "world_heritage_property", "DEN-BH-WHC-20260816", 3,
                 WHC_REGISTER, WHC_LICENSE, "Three matched inscribed serial properties; tentative-list sites and component parts are outside this denominator."),
    ]
    snapshot = {
        "id": SNAPSHOT_ID, "schema_version": SCHEMA_VERSION,
        "title": "Bahrain production expansion — governorates and World Heritage",
        "captured_at": SNAPSHOT_DATE, "source_id": AREA_SOURCE,
        "scope": "Four official 2024 governorates and three World Heritage properties on the Bahrain State Party list",
        "method": "Offline deterministic import from checksum-bound exact API records and bounded official/UNESCO extracts.",
        "checksum": "sha256:" + hashlib.sha256(SNAPSHOT_MANIFEST.read_bytes()).hexdigest(),
        "notes": "Governorate data are year-2024 records retrieved 2026-08-16. Areas, blocks, populated places, food, dress, custom, and dialect layers remain unclosed without accepted denominators/evidence.",
    }

    replace(ROOT / "data/entities/entities.jsonl", lambda r: r.get("country_code") == "BH" and r.get("entity_type") != "country", entities)
    bh_ids = {row["id"] for row in entities} | {"ENT-BH-COUNTRY"}
    replace(ROOT / "data/aliases/aliases.jsonl", lambda r: r.get("entity_id", "").startswith("ENT-BH-"), aliases)
    replace(ROOT / "data/relationships/relationships.jsonl", lambda r: r.get("child_id", "").startswith("ENT-BH-"), relationships)
    replace(ROOT / "data/claims/claims.jsonl", lambda r: r.get("subject_id") in bh_ids, claims)
    replace(ROOT / "data/coverage/denominators.jsonl", lambda r: r.get("country_code") == "BH" and r.get("layer") != "country_scope", denoms)
    replace(ROOT / "data/coverage/coverage.jsonl", lambda r: r.get("country_code") == "BH" and r.get("layer") != "country_scope", covs)
    replace(ROOT / "data/snapshots/snapshots.jsonl", lambda r: r.get("id", "").startswith("SNP-BH-"), [snapshot])

    manifest = load(ROOT / "manifests/BH.yml")
    temporal = ["current", "historical", "disputed", "de_facto", "claimed", "proposed", "transitional", "uncertain"]
    manifest.update({
        "status": "pilot_migrated",
        "official_authority": {"name": "Survey and Land Registration Bureau via Bahrain National Open Data Portal", "source_ids": [AREA_SOURCE, "SRC-BH-OPEN-DATA-POLICY-2026"], "verification_status": "verified", "missing_reason": None},
        "snapshot": {"as_of": SNAPSHOT_DATE, "snapshot_id": SNAPSHOT_ID, "status": "verified"},
        "coverage_record_ids": ["COV-BH-COUNTRY-SCOPE", "COV-BH-GOVERNORATES-2024", "COV-BH-WHC-20260816"],
        "caveats": [
            "Production mode is recorded by the closeout; the current manifest status vocabulary retains pilot_migrated as its accepted-data state.",
            "Governorates are not areas, electoral constituencies, or blocks; those layers remain unavailable in this cycle.",
            "World Heritage properties may be serial; component parts are not split into unsupported place entities.",
            "No national denominator is asserted for cities, villages, neighborhoods, culture generally, or dialect vocabulary.",
            "Depth cycle 1 (2026-09-20): the five UNESCO intangible-heritage elements are published facts; language, dialect, food, dress, and craft material from local and press sources stays classified and unpublished.",
            "Muharraq firjan, villages, and halat are places with located_in only: no administrative parent, no population claim, and no percentage, because no dated official lower denominator exists."
        ],
        "next_action": "Maintain Bahrain as production-accepted with the depth cycle 1 heritage layer; expand areas, blocks, or populated places only after an official dated denominator and topology are checksum-bound.",
    })
    hierarchy = manifest["hierarchy"]
    for level in hierarchy:
        if level["entity_type"] == "bh_governorate":
            level.update({"source_ids": [AREA_SOURCE], "verification_status": "verified", "authority_name": "Survey and Land Registration Bureau", "denominator": 4, "denominator_id": "DEN-BH-GOVERNORATES-2024", "coverage_record_id": "COV-BH-GOVERNORATES-2024", "snapshot_date": "2024-01-01", "license": OPEN_LICENSE, "scope_status": "closed", "notes": "Exactly four current governorates in the official 2024 dataset.", "special_cases": ["Central Governorate is historical after the 2014 redivision and is not emitted as current."]})
        elif level["entity_type"] in {"bh_area", "bh_block"}:
            level.update({"verification_status": "pending", "authority_name": None, "denominator": None, "denominator_id": None, "coverage_record_id": None, "snapshot_date": None, "license": None, "scope_status": "unavailable", "notes": "No accepted dated official denominator/topology in this production cycle.", "special_cases": ["Do not infer this layer from governorate, electoral, address, or map labels."]})
    manifest["pilot_layers"] = [
        {"layer": "bh_governorate", "entity_types": ["bh_governorate"], "local_names": ["محافظة"], "authority_name": "Survey and Land Registration Bureau", "denominator": 4, "denominator_id": "DEN-BH-GOVERNORATES-2024", "coverage_record_id": "COV-BH-GOVERNORATES-2024", "snapshot_date": "2024-01-01", "source_ids": [AREA_SOURCE], "license": OPEN_LICENSE, "scope_status": "closed", "notes": "Complete official four-governorate layer.", "special_cases": ["Central Governorate excluded from current layer after 2014 redivision."]},
        {"layer": "world_heritage_property", "entity_types": ["archaeological_site", "cultural_site"], "local_names": ["موقع تراث عالمي"], "authority_name": "UNESCO World Heritage Centre", "denominator": 3, "denominator_id": "DEN-BH-WHC-20260816", "coverage_record_id": "COV-BH-WHC-20260816", "snapshot_date": SNAPSHOT_DATE, "source_ids": [WHC_REGISTER, "SRC-UNESCO-WHC-BH-1192", "SRC-UNESCO-WHC-BH-1364", "SRC-UNESCO-WHC-BH-1542"], "license": WHC_LICENSE, "scope_status": "closed", "notes": "All three inscribed serial properties; not all cultural sites in Bahrain.", "special_cases": ["Tentative-list sites excluded.", "Serial components are not separate entities in this cycle."]},
        {"layer": "unesco_intangible_heritage", "entity_types": ["cultural_site"], "local_names": ["عنصر تراث غير مادي"], "authority_name": "UNESCO Intangible Cultural Heritage", "denominator": 5, "denominator_id": None, "coverage_record_id": None, "snapshot_date": DEPTH_DATE, "source_ids": [ICH_SOURCE, FJIRI_SOURCE], "license": "UNESCO ICH pages; factual extraction with attribution", "scope_status": "closed", "notes": "Five inscribed elements on which Bahrain appears, recorded as claims on the country entity; no separate entity per element in this cycle and no coverage record because the layer itself is the inscription list.", "special_cases": ["Multi-State files carry classification shared and are never exclusive.", "Inscription year stays inside the claim value and is not expanded into an exact day."]},
        {"layer": "muharraq_heritage_places", "entity_types": ["city", "quarter", "village"], "local_names": ["فريج", "قرية", "حالة"], "authority_name": None, "denominator": None, "denominator_id": None, "coverage_record_id": None, "snapshot_date": DEPTH_DATE, "source_ids": [DEPTH_SOURCES["muharraq_wiki"], DEPTH_SOURCES["albilad_press"], DEPTH_SOURCES["firjan_blog"]], "license": "Local heritage mirror, press columns, and a self-published heritage series; factual extraction with attribution", "scope_status": "open", "notes": "Bounded heritage-attested set: Muharraq city, fourteen firjan, six villages, and three halat, entered as local_reported places with located_in only and no denominator.", "special_cases": ["No administrative parent and no population claim for any place in this layer.", "Historical firjan keep status historical; living villages and halat keep status current without any administrative meaning."]},
        {"layer": "classified_local_knowledge", "entity_types": ["cultural_site"], "local_names": ["معرفة محلية مصنّفة"], "authority_name": None, "denominator": None, "denominator_id": None, "coverage_record_id": None, "snapshot_date": DEPTH_DATE, "source_ids": [DEPTH_SOURCES["dialect_mirror"], DEPTH_SOURCES["cuisine_mirror"], DEPTH_SOURCES["folk_cloth"], DEPTH_SOURCES["nashil_press"], DEPTH_SOURCES["firjan_elaph"]], "license": "Local mirror, folklore journal, press, and heritage-blog material; factual extraction with attribution", "scope_status": "open", "notes": "Thirty-four classified and unpublished claims: one language presence, three dialect profiles, twenty-three dishes, seven dress items, and three crafts; no coverage percentage is claimed.", "special_cases": ["Every weak-source claim must declare classification and stay unpublished.", "No speaker counts, no population figures, and no exclusive ownership of shared Gulf heritage."]},
    ]
    write_json(ROOT / "manifests/BH.yml", manifest)
    write_json(ROOT / "data/cultural/bahrain_domain_status.json", {
        "schema_version": SCHEMA_VERSION, "country_code": "BH", "snapshot_date": DEPTH_DATE,
        "domains": {
            "world_heritage": {"status": "documented", "claims": 9, "denominator": 3},
            "intangible_cultural_heritage": {"status": "documented_published_unesco", "claims": 5,
                "elements": ["الفجري 2021 (01747)", "الخط العربي 2021 (01718) مشترك", "نخيل التمر 2022 (01902) مشترك",
                             "الحناء 2024 (02116) مشترك", "البشت 2025 (02233) مشترك"]},
            "languages": {"status": "documented_local_reported_unpublished", "claims": 1},
            "dialect": {"status": "documented_local_reported_unpublished", "claims": 3},
            "food": {"status": "documented_local_reported_unpublished", "claims": 23},
            "dress": {"status": "documented_local_reported_unpublished", "claims": 7},
            "crafts": {"status": "documented_local_reported_unpublished", "claims": 3},
            "custom": {"status": "documented_published_shared_via_unesco", "claims": 1},
            "heritage_places": {"status": "documented_heritage_layer_no_denominator", "entities": 24, "denominator": None}
        },
        "notes": "Depth cycle 1 opens the cultural domains that the bounded first cycle left undocumented: the UNESCO intangible-heritage list is the published spine, and everything from local mirrors, the folklore journal, press, and heritage blogs stays classified and unpublished. The Muharraq heritage layer carries no denominator and no percentage."
    })
    print(json.dumps({"entities_added": len(entities), "aliases_added": len(aliases), "relationships_added": len(relationships), "claims_added": len(claims), "depth_claims": sum(r["id"].startswith("CLM-BH-DEPTH") for r in claims), "depth_places": len(depth_entities), "denominators_added": 2, "coverage_added": 2, "sources": 17}, sort_keys=True))


if __name__ == "__main__":
    main()
