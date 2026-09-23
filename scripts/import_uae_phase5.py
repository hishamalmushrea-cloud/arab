#!/usr/bin/env python3
"""Deterministically materialize the bounded UAE fourth-country pilot."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable

from build_uae_sources import main as build_sources
from model import ROOT, SCHEMA_VERSION, read_jsonl, record_id, write_json, write_jsonl


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def deterministic_id(prefix: str, *parts: object) -> str:
    return record_id(prefix, *parts)


SNAPSHOT_DATE = "2026-08-15"
SNAPSHOT_ID = "SNP-AE-PILOT-20260815"
PROFILE_PATH = ROOT / "data/imports/uae/fixtures/administrative_profile.json"
CULTURE_PATH = ROOT / "data/imports/uae/fixtures/cultural_claims.json"
SOURCE_FIXTURE_PATH = ROOT / "data/imports/uae/fixtures/source_catalog.json"
SNAPSHOT_MANIFEST_PATH = ROOT / "data/imports/uae/snapshot_manifest.json"
SNAPSHOT_DATE_DEPTH = "2026-09-23"
DEPTH_SNAPSHOT_ID = "SNP-AE-DEPTH-20260923"
DEPTH_TAGS = {"unesco_intangible_heritage": "ICH", "world_heritage_inscribed": "WH-INSCRIBED",
              "world_heritage_tentative_list": "WH-TENTATIVE", "heritage_places": "PLACES", "classified_local_knowledge": "LOCAL"}
DEPTH_PATH = ROOT / "data/imports/uae/fixtures/cultural_depth_2026.json"
MANIFEST_PATH = ROOT / "manifests/AE.yml"
DOMAIN_STATUS_PATH = ROOT / "data/cultural/uae_domain_status.json"
DEPTH_LAYERS = [
    {"layer": "unesco_intangible_heritage", "entity_types": ["country"], "local_names": ["عنصر تراث غير مادي"],
     "authority_name": "UNESCO Intangible Cultural Heritage", "denominator": 21, "denominator_id": "DEN-AE-ICH", "coverage_record_id": "COV-AE-ICH",
     "snapshot_date": SNAPSHOT_DATE_DEPTH, "source_ids": ["SRC-UNESCO-ICH-AE-STATE-2026", "SRC-UNESCO-ICH-AE-AL-AZI-01268-2017"],
     "license": "UNESCO ICH state and element pages; factual extraction with attribution; CC BY-SA 3.0 IGO for the descriptions", "scope_status": "closed",
     "notes": "واحد وعشرون إدراجًا في القوائم والسجل، سبعة منها مصنَّفة في هذه الدورة.",
     "special_cases": ["العنصر الوطني الوحيد المتحقَّق هو العزي 01268 على قائمة الصون العاجل.",
                       "ثلاثة عشر ملفًا مؤجَّلًا لقائمة الدول المقدِّمة بدل تخمين التصنيف.",
                       "الملفات المشتركة تبقى shared ولا تُرقّى إلى national."]},
    {"layer": "world_heritage_inscribed", "entity_types": ["country"], "local_names": ["موقع تراث عالمي"],
     "authority_name": "UNESCO World Heritage Centre", "denominator": 3, "denominator_id": "DEN-AE-WH-INSCRIBED", "coverage_record_id": "COV-AE-WH-INSCRIBED",
     "snapshot_date": SNAPSHOT_DATE_DEPTH, "source_ids": ["SRC-UNESCO-WH-AE-STATE-2026"],
     "license": "UNESCO World Heritage state page; factual extraction with attribution", "scope_status": "closed",
     "notes": "ثلاثة مواقع مُدرجة (1343 و1735 و1724) من صفحة الدولة.", "special_cases": ["المعايير غير مقروءة فتبقى فارغة.", "الموقع الطبيعي لا تُبنى عليه أوصاف ثقافية."]},
    {"layer": "world_heritage_tentative_list", "entity_types": ["natural_site", "cultural_site"], "local_names": ["القائمة المؤقتة"],
     "authority_name": "UNESCO World Heritage Centre", "denominator": 15, "denominator_id": "DEN-AE-WH-TENTATIVE", "coverage_record_id": "COV-AE-WH-TENTATIVE",
     "snapshot_date": SNAPSHOT_DATE_DEPTH, "source_ids": ["SRC-UNESCO-WH-AE-STATE-2026"],
     "license": "UNESCO World Heritage state page; factual extraction with attribution", "scope_status": "closed",
     "notes": "خمسة عشر ملفًا مؤقتًا بين 2012 و2026.", "special_cases": ["القائمة المؤقتة ليست إدراجًا."]},
    {"layer": "heritage_places", "entity_types": ["cultural_site", "natural_site"], "local_names": ["موقع مُدرج بلا مقام"],
     "authority_name": "UNESCO World Heritage Centre", "denominator": None, "denominator_id": "DEN-AE-PLACES", "coverage_record_id": "COV-AE-PLACES",
     "snapshot_date": SNAPSHOT_DATE_DEPTH, "source_ids": ["SRC-UNESCO-WH-AE-STATE-2026"],
     "license": "UNESCO World Heritage state page; factual extraction with attribution", "scope_status": "open",
     "notes": "ثلاثة أماكن مُدرجة بلا مقام ولا نسبة.", "special_cases": ["located_in فقط: بلا أب إداري وبلا دعوى وبلا إحداثيات.",
                                                                      "إمارة كل موقع لم تُقرأ فتبقى خارج السجل."]},
    {"layer": "classified_local_knowledge", "entity_types": ["country"], "local_names": ["معرفة محلية مصنَّفة"],
     "authority_name": "Wikimedia mirrors (English)", "denominator": None, "denominator_id": "DEN-AE-LOCAL", "coverage_record_id": "COV-AE-LOCAL",
     "snapshot_date": SNAPSHOT_DATE_DEPTH, "source_ids": ["SRC-AE-CUISINE-MIRROR-2026", "SRC-AE-CULTURE-MIRROR-2026", "SRC-AE-ISO639-3-ARABIC"],
     "license": "Wikipedia text, CC BY-SA 4.0; ISO 639-3 registry entry; classification use only", "scope_status": "open",
     "notes": "لغات ولهجة وأطباق وحرف وأعراف وروايات، كلها غير منشورة.", "special_cases": ["لا يُنشر أي ادّعاء ضعيف المصدر.",
                                                                                        "لا تُسجَّل أعداد سكان ولا متحدثين ولا نسب.",
                                                                                        "الرمز اللغوي لا يُسجَّل إلا متحققًا من سجل ISO 639-3."]},
]


def replace_rows(path: Path, remove: Callable[[dict[str, Any]], bool], additions: list[dict[str, Any]]) -> None:
    retained = [row for row in read_jsonl(path) if not remove(row)]
    write_jsonl(path, retained + additions)


def typed_value(value: Any) -> dict[str, Any]:
    if isinstance(value, bool):
        kind = "boolean"
    elif isinstance(value, int):
        kind = "integer"
    elif isinstance(value, float):
        kind = "number"
    elif isinstance(value, (dict, list)):
        kind = "json"
    else:
        kind = "string"
    return {"type": kind, "data": value}


def claim_record(
    key: str,
    subject_id: str,
    predicate: str,
    value: Any,
    source_id: str,
    source_locator: str,
    classification: str | None,
    *,
    notes: str | None = None,
    status: str = "verified",
    lexical_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "id": deterministic_id("CLM-AE", key),
        "schema_version": SCHEMA_VERSION,
        "subject_id": subject_id,
        "predicate": predicate,
        "value": typed_value(value),
        "unit": None,
        "status": status,
        "observed_at": SNAPSHOT_DATE,
        "valid_from": None,
        "valid_to": None,
        "source_id": source_id,
        "second_source_id": None,
        "source_locator": source_locator,
        "sensitivity": "ordinary",
        "notes": notes,
        "verification_status": "source_verified",
        "confidence": "high",
        "classification": classification,
        "published": True,
        "second_source_locator": None,
        "lexical_context": lexical_context,
    }


def main() -> None:
    build_sources()
    profile = load_json(PROFILE_PATH)
    culture = load_json(CULTURE_PATH)
    for fixture in (profile, culture):
        if fixture.get("schema_version") != SCHEMA_VERSION or fixture.get("country_code") != "AE":
            raise SystemExit("invalid UAE fixture identity/version")
        if fixture.get("snapshot_date") != SNAPSHOT_DATE:
            raise SystemExit("UAE fixture snapshot dates differ")

    entities: list[dict[str, Any]] = []
    aliases: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []

    for spec in profile["entities"]:
        entities.append(
            {
                "id": spec["id"],
                "schema_version": SCHEMA_VERSION,
                "country_code": "AE",
                "canonical_name": spec["name"],
                "canonical_name_language": spec["name_language"],
                "entity_type": spec["entity_type"],
                "status": "current",
                "valid_from": None,
                "valid_to": None,
                "canonical_source_id": spec["source_id"],
                "source_locator": spec["source_locator"],
                "coordinates": None,
                "verification_status": "source_verified",
                "confidence": "high",
                "legacy_ids": [],
                "notes": f"Contextual UAE type; layer={spec['layer']}; snapshot={SNAPSHOT_DATE}. Administrative entities do not receive invented point coordinates.",
            }
        )
        aliases.append(
            {
                "id": deterministic_id("ALS-AE", spec["id"], spec["arabic_alias"], "ar", "official_variant"),
                "schema_version": SCHEMA_VERSION,
                "entity_id": spec["id"],
                "name": spec["arabic_alias"],
                "language": "ar",
                "script": "Arab",
                "kind": "official_variant",
                "status": "current",
                "source_id": spec["source_id"],
                "source_locator": spec["source_locator"] + "; parallel Arabic official name",
                "valid_from": None,
                "valid_to": None,
            }
        )
        relationships.append(
            {
                "id": deterministic_id("REL-AE", "administrative_parent", spec["id"], spec["parent_id"]),
                "schema_version": SCHEMA_VERSION,
                "child_id": spec["id"],
                "parent_id": spec["parent_id"],
                "relationship_type": "administrative_parent",
                "status": "current",
                "valid_from": None,
                "valid_to": None,
                "source_id": spec["source_id"],
                "source_locator": spec["source_locator"],
                "notes": "Parent is explicit in the emirate-specific fixture; equal-looking local words in other emirates are not treated as the same type.",
                "verification_status": "source_verified",
                "confidence": "high",
            }
        )
        claims.append(
            claim_record(
                "SEMANTICS-" + spec["id"],
                spec["id"],
                "jurisdiction_semantics",
                {
                    "authority": spec["authority"],
                    "parent_id": spec["parent_id"],
                    "snapshot_date": SNAPSHOT_DATE,
                    "semantic_definition": spec["semantic_definition"],
                    "layer": spec["layer"],
                },
                spec["source_id"],
                spec["source_locator"],
                "official",
                notes="Structured authority, parent, dated snapshot, and contextual semantic definition; it is not a generic UAE lower tier.",
            )
        )

    # Julfar is a historical name for the RAK identity in the bounded source, not a current unit.
    aliases.append(
        {
            "id": deterministic_id("ALS-AE", "ENT-AE-EMIRATE-RAS-AL-KHAIMAH", "Julfar", "en", "historical"),
            "schema_version": SCHEMA_VERSION,
            "entity_id": "ENT-AE-EMIRATE-RAS-AL-KHAIMAH",
            "name": "Julfar",
            "language": "en",
            "script": "Latn",
            "kind": "historical",
            "status": "historical",
            "source_id": "SRC-AE-RAK-GENERAL-2026",
            "source_locator": "history opening: Originally known as Julfar",
            "valid_from": None,
            "valid_to": None,
        }
    )

    for spec in culture["claims"]:
        claims.append(
            claim_record(
                spec["key"],
                spec["subject_id"],
                spec["predicate"],
                spec["value"],
                spec["source_id"],
                spec["source_locator"],
                spec["classification"],
                notes=spec.get("notes"),
                status=spec.get("status", "verified"),
                lexical_context=spec.get("lexical_context"),
            )
        )

    layer_by_name = {row["layer"]: row for row in profile["layers"]}
    denominators: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []
    for layer in profile["layers"]:
        slug = layer["layer"].upper().replace("_", "-")
        den_id = "DEN-AE-COUNTRY-SCOPE" if layer["layer"] == "country_scope" else f"DEN-AE-{slug}"
        cov_id = "COV-AE-COUNTRY-SCOPE" if layer["layer"] == "country_scope" else f"COV-AE-{slug}"
        denominator = layer["denominator"]
        denominators.append(
            {
                "id": den_id,
                "schema_version": SCHEMA_VERSION,
                "country_code": "AE",
                "layer": layer["layer"],
                "definition": layer["definition"],
                "value": denominator,
                "denominator": denominator,
                "as_of": SNAPSHOT_DATE,
                "snapshot_date": SNAPSHOT_DATE,
                "source_id": layer["source_id"],
                "source_locator": layer["source_locator"],
                "license": layer["license"],
                "status": layer["status"],
                "missing_reason": layer["missing_reason"],
                "notes": f"Authority: {layer['authority']}. A bounded official layer is complete only when matched + excluded equals its source-backed denominator.",
            }
        )
        percentage = None if denominator is None else round((layer["matched"] + layer["excluded"]) / denominator * 100, 2) if denominator else 100.0
        coverage.append(
            {
                "id": cov_id,
                "schema_version": SCHEMA_VERSION,
                "country_code": "AE",
                "layer": layer["layer"],
                "snapshot_id": SNAPSHOT_ID,
                "snapshot_date": SNAPSHOT_DATE,
                "source_id": layer["source_id"],
                "denominator_id": den_id,
                "license": layer["license"],
                "denominator": denominator,
                "matched": layer["matched"],
                "unmatched": layer["unmatched"],
                "excluded": layer["excluded"],
                "exclusion_reasons": [],
                "missing": layer["unmatched"] if denominator is not None else None,
                "missing_reason": layer["missing_reason"],
                "coverage_percentage": percentage,
                "complete": denominator is not None and layer["matched"] + layer["excluded"] == denominator and layer["unmatched"] == 0,
                "notes": layer["definition"] + (". No percentage is calculated." if denominator is None else ". Every in-scope row is matched; no exclusions."),
            }
        )

    checksum = hashlib.sha256()
    for path in sorted([PROFILE_PATH, CULTURE_PATH, SOURCE_FIXTURE_PATH, SNAPSHOT_MANIFEST_PATH]):
        checksum.update(path.read_bytes())
    snapshot = {
        "id": SNAPSHOT_ID,
        "schema_version": SCHEMA_VERSION,
        "title": "United Arab Emirates fourth-country contextual hierarchy and cultural sample",
        "captured_at": SNAPSHOT_DATE,
        "source_id": "SRC-AE-FEDERAL-SEVEN-EMIRATES-2026",
        "scope": "Seven emirates; seven different official local hierarchy profiles; bounded all-emirate cultural and small dialect samples",
        "method": "Offline deterministic import from checksum-bound relevant-text extracts and structured fixtures; official layer denominators remain separate and unavailable registries have no percentage.",
        "checksum": "sha256:" + checksum.hexdigest(),
        "notes": "Dubai communities, all-UAE populated places, and neighborhoods remain denominator_unavailable. No fifth country is started.",
    }

    depth_claims: list[dict[str, Any]] = []
    depth = load_json(DEPTH_PATH)
    if depth.get("country_code") != "AE" or depth.get("schema_version") != SCHEMA_VERSION or depth.get("snapshot_date") != SNAPSHOT_DATE_DEPTH:
        raise SystemExit("UAE depth fixture is malformed")
    depth_sources = depth["sources"]

    def depth_claim(key, predicate, value, classification, source_id, locator, published, notes, second_source_id=None, second_source_locator=None):
        return {
            "id": deterministic_id("CLM-AE-DEPTH", key),
            "schema_version": SCHEMA_VERSION,
            "subject_id": "ENT-AE-COUNTRY",
            "predicate": predicate,
            "value": typed_value(value),
            "unit": None,
            "status": "verified" if published else "reported",
            "observed_at": SNAPSHOT_DATE_DEPTH,
            "valid_from": None,
            "valid_to": None,
            "source_id": source_id,
            "second_source_id": second_source_id,
            "source_locator": locator,
            "sensitivity": "ordinary",
            "notes": notes,
            "verification_status": "verified" if published else "local_reported",
            "confidence": "high" if published else "low",
            "classification": classification,
            "published": published,
            "second_source_locator": second_source_locator,
            "lexical_context": None,
        }

    ich = depth["intangible_heritage"]
    for element in ich["published_elements"]:
        depth_claims.append(depth_claim(f"ELEMENT-{element['reference']}", "intangible_cultural_practice",
                                        {"name": element["name"], "official_title": element["official_title"], "reference": element["reference"],
                                         "year": element["year"], "list": element["list"], "classification": element["classification"],
                                         "co_states": element["co_states"]},
                                        element["classification"], depth_sources[element["source"]],
                                        f"عنصر {element['reference']}؛ إدراج {element['year']} على {'قائمة الصون العاجل' if element['list'] == 'USL' else 'القائمة التمثيلية'}",
                                        True, element["note"]))
    entry = ich["register_entry"]
    depth_claims.append(depth_claim(f"REGISTER-{entry['reference']}", "unesco_safeguarding_programme",
                                    {"name": entry["name"], "official_title": entry["official_title"], "reference": entry["reference"], "year": entry["year"]},
                                    "official", depth_sources["ich_state"], f"سجل الممارسات الجيدة {entry['reference']}؛ {entry['year']}", True, entry["note"]))
    for element in ich["deferred_elements"]:
        depth_claims.append(depth_claim(f"DEFERRED-{element['reference']}", "unesco_element_deferred_file",
                                        {"reference": element["reference"], "year": element["year"], "list": element["list"], "name": element["name"]},
                                        "local_reported", depth_sources["ich_state"],
                                        f"عنصر {element['reference']}؛ إدراج {element['year']} من صفحة الدولة", False, ich["deferred_reason"]))
    for nomination in ich["pending_2026"]:
        depth_claims.append(depth_claim(f"NOMINATION-{nomination['name'][:24]}", "unesco_pending_nomination",
                                        {"name": nomination["name"], "year": nomination["year"], "status": nomination["status"]},
                                        "official", depth_sources["ich_state"], f"ترشيح معلن {nomination['year']}: {nomination['name']}", True,
                                        "ترشيح معلن لا يُسجَّل إدراجًا؛ يُنشر بوصفه ترشيحًا في موعده."))
    depth_claims.append(depth_claim("ICH-RATIFICATION", "convention_ratification_date", ich["ratification"], "official",
                                    depth_sources["ich_state"], f"تصديق اتفاقية 2003 في {ich['ratification']}", True,
                                    "تاريخ تصديق من صفحة الدولة؛ يُنشر مرة واحدة ولا يُوسَّع إلى سرد."))
    whc = depth["world_heritage"]
    depth_claims.append(depth_claim("WH-ACCESSION", "world_heritage_convention_accession", whc["accession"], "official",
                                    depth_sources["whc_state"], f"انضمام إلى اتفاقية التراث العالمي في {whc['accession']}", True,
                                    "تاريخ انضمام من صفحة الدولة."))
    depth_claims.append(depth_claim("WH-ASSISTANCE", "world_heritage_assistance_requests", whc["assistance_requests_approved"], "official",
                                    depth_sources["whc_state"], "صفحة الدولة: International assistance requests Approved = 0", True,
                                    "صفر مقصود مقروء من صفحة الدولة يُنشر ليمنع أي تقدير بديل."))
    for property_ in whc["inscribed"]:
        depth_claims.append(depth_claim(f"PROPERTY-{property_['reference']}", "world_heritage_property",
                                        {"name": property_["name"], "official_title": property_["official_title"], "reference": property_["reference"],
                                         "year": property_["year"], "category": property_["category"], "criteria": property_["criteria"]},
                                        "official", depth_sources["whc_state"], f"موقع مُدرج {property_['reference']}؛ {property_['year']} ({property_['category']})", True,
                                        whc["criteria_note"]))
    for site in whc["tentative"]:
        depth_claims.append(depth_claim(f"TENTATIVE-{site['reference']}", "unesco_tentative_listing",
                                        {"name": site["name"], "reference": site["reference"], "year": site["year"], "status": "القائمة المؤقتة"},
                                        "official", depth_sources["whc_state"], f"ملف القائمة المؤقتة {site['reference']}؛ {site['year']}", True,
                                        "القائمة المؤقتة ليست إدراجًا؛ تُنشر بوصفها ملفًا مؤقتًا بسنتها."))
    for language in depth["languages"]:
        depth_claims.append(depth_claim(f"LANGUAGE-{language['name'][:20]}", "language_presence",
                                        {"name": language["name"], "level": language["level"], "official": language["official"], "iso_codes": language["iso_codes"],
                                         "note": language["note"]},
                                        "official" if language["official"] else "local_reported", depth_sources[language["second_source"] or "culture"],
                                        f"مرآة الثقافة الإماراتية: {language['name']}", False, language["note"],
                                        depth_sources[language["second_source"]] if language["second_source"] else None,
                                        "سجل ISO 639-3: ara = Arabic" if language["second_source"] else None))
    for dialect in depth["dialects"]:
        depth_claims.append(depth_claim(f"DIALECT-{dialect['iso']}", "dialect_profile",
                                        {"name": dialect["name"], "group": dialect["group"], "iso": dialect["iso"], "features": dialect["features"]},
                                        "regional", depth_sources["culture"], f"مرآة الثقافة الإماراتية: {dialect['name']}", False, dialect["note"],
                                        depth_sources["iso_ara"], "سجل ISO 639-3: afb = Gulf Arabic"))
    for dish in depth["dishes"]:
        depth_claims.append(depth_claim(f"DISH-{dish['name'][:20]}", "food_dish", {"name": dish["name"], "description": dish["desc"]}, "local",
                                        depth_sources["cuisine"], f"مطبخ الإمارات: {dish['name']}", False,
                                        "طبق محلي من مرآة؛ يُسجَّل مصنَّفًا غير منشور ولا يُنسب إلى إحصاء."))
    for craft in depth["crafts"]:
        depth_claims.append(depth_claim(f"CRAFT-{craft['name'][:20]}", "craft_custom", {"name": craft["name"], "description": craft["desc"]}, "local",
                                        depth_sources["culture"], f"ثقافة الإمارات: {craft['name']}", False,
                                        "حرفة أو رمز من مرآة؛ يُسجَّل مصنَّفًا غير منشور."))
    for custom in depth["customs"]:
        depth_claims.append(depth_claim(f"CUSTOM-{custom['name'][:20]}", "custom_practice", {"name": custom["name"], "description": custom["desc"]}, "popular",
                                        depth_sources["culture"], f"ثقافة الإمارات: {custom['name']}", False,
                                        "عرف من مرآة؛ يُسجَّل مصنَّفًا غير منشور ولا يُقدَّم وصفًا قانونيًا."))
    for narrative in depth["narratives"]:
        depth_claims.append(depth_claim(f"NARRATIVE-{narrative['name'][:24]}", "naming_narrative",
                                        {"name": narrative["name"], "description": narrative["desc"]}, "historical", depth_sources["culture"],
                                        f"ثقافة الإمارات: {narrative['name']}", False, "رواية معلنة من مرآة تُسجَّل روايةً ولا يُحسم فيها."))

    for place in depth["places"]:
        entities.append({
            "id": place["id"], "schema_version": SCHEMA_VERSION, "country_code": "AE", "canonical_name": place["name"], "canonical_name_language": "ar",
            "entity_type": place["kind"], "status": "current", "valid_from": None, "valid_to": None, "canonical_source_id": depth_sources["whc_state"],
            "source_locator": place["note"], "legacy_ids": [], "coordinates": None, "notes": place["note"],
            "verification_status": "source_verified", "confidence": "high"})
        relationships.append({
            "id": deterministic_id("REL-AE-DEPTH", place["id"]), "schema_version": SCHEMA_VERSION, "child_id": place["id"], "parent_id": place["parent"],
            "relationship_type": "located_in", "status": "current", "valid_from": None, "valid_to": None, "source_id": depth_sources["whc_state"],
            "source_locator": place["note"], "notes": "علاقة مكانية واحدة بلا أب إداري وبلا دعوى سكان وبلا نسبة.",
            "verification_status": "source_verified", "confidence": "high"})

    claims.extend(depth_claims)
    depth_checksum = hashlib.sha256()
    for path in sorted([DEPTH_PATH, SNAPSHOT_MANIFEST_PATH]):
        depth_checksum.update(path.read_bytes())
    depth_snapshot = {
        "id": DEPTH_SNAPSHOT_ID,
        "schema_version": SCHEMA_VERSION,
        "title": "United Arab Emirates UNESCO depth cycle 1: ICH state page, Al Azi, World Heritage state page and ISO 639-3",
        "captured_at": SNAPSHOT_DATE_DEPTH,
        "source_id": depth_sources["ich_state"],
        "scope": (f"{len(ich['published_elements'])} classified ICH element files, {len(ich['deferred_elements'])} deferred element files, {len(ich['pending_2026'])} pending nominations, "
                  f"{len(whc['inscribed'])} inscribed properties, {whc['tentative_total']} tentative-list files, {len(depth['languages'])} language rows and one dialect row"),
        "method": ("Offline deterministic import from a checksum-bound depth fixture; depth layers carry no denominator, no percentage and no inherited population, and unread fields stay empty rather than inferred."),
        "checksum": "sha256:" + depth_checksum.hexdigest(),
        "notes": ("Unread and left empty: World Heritage criteria, the emirate of each inscribed property, and the submitting-State list of the thirteen deferred element files. "
                  "The pilot snapshot stays bound to its four 2026-08-15 fixtures."),
    }
    domain_status = {
        "schema_version": SCHEMA_VERSION, "country_code": "AE", "snapshot_date": SNAPSHOT_DATE_DEPTH,
        "domains": {
            "intangible_cultural_heritage": {"status": "documented_seven_classified_one_national_thirteen_deferred", "inscribed_total": ich["inscribed_total"],
                                             "classified": len(ich["published_elements"]), "national": 1, "deferred": len(ich["deferred_elements"]),
                                             "register_entries": 1},
            "world_heritage": {"status": "documented_three_inscribed_criteria_unread", "inscribed": len(whc["inscribed"]),
                               "tentative_list_sites": whc["tentative_total"], "criteria_read": False},
            "languages": {"status": "documented_unpublished_pending_constitution", "claims": len(depth["languages"])},
            "dialect": {"status": "documented_local_reported_unpublished", "claims": len(depth["dialects"])},
            "food": {"status": "documented_local_reported_unpublished", "claims": len(depth["dishes"])},
            "crafts": {"status": "documented_local_reported_unpublished", "claims": len(depth["crafts"])},
            "custom": {"status": "documented_local_reported_unpublished", "claims": len(depth["customs"])},
            "narratives": {"status": "documented_narratives_unpublished", "claims": len(depth["narratives"])},
            "dress": {"status": "not_documented_in_cycle", "claims": 0},
            "heritage_places": {"status": "documented_places_no_denominator", "entities": len(depth["places"]), "denominator": None},
            "populated_places": {"status": "unavailable_in_accepted_layer", "denominator": None},
            "neighborhoods": {"status": "unavailable_in_accepted_layer", "denominator": None},
        },
        "notes": "سبعة عناصر يونسكوية مصنَّفة (واحد وطني وحيد الدولة: العزي على قائمة الصون العاجل) وثلاثة عشر ملفًا مؤجَّلًا لقائمة الدول المقدِّمة، وثلاثة مواقع مُدرجة بمعايير غير مقروءة، وخمسة عشر ملفًا مؤقتًا، ولا يُسجَّل أي عدد سكان أو متحدثين أو نسبة، والصفوف اللغوية تنتظر قراءة الدستور.",
    }
    # The accepted Phase-2 import backfills coverage licenses from the source registry, so the depth
    # layers copy the same source license here instead of inventing a layer-local string.
    source_license_by_id = {row["id"]: row["license"] for row in load_json(SOURCE_FIXTURE_PATH)["sources"]}
    for layer, tag in DEPTH_TAGS.items():
        reason = "knowledge/list layer: no spatial denominator is asserted and no percentage is calculated"
        layer_source = next(layer_row["source_ids"][0] for layer_row in DEPTH_LAYERS if layer_row["layer"] == layer)
        layer_license = source_license_by_id[layer_source]
        denominators.append({"id": f"DEN-AE-{tag}", "schema_version": SCHEMA_VERSION, "country_code": "AE", "layer": layer,
                             "definition": f"{layer} depth layer", "value": None, "as_of": SNAPSHOT_DATE_DEPTH, "status": "unavailable",
                             "source_id": layer_source,
                             "source_locator": f"{layer} depth layer", "license": layer_license,
                             "missing_reason": reason, "notes": reason, "denominator": None, "snapshot_date": SNAPSHOT_DATE_DEPTH})
        coverage.append({"id": f"COV-AE-{tag}", "schema_version": SCHEMA_VERSION, "country_code": "AE", "layer": layer, "snapshot_id": DEPTH_SNAPSHOT_ID,
                         "denominator_id": f"DEN-AE-{tag}", "source_id": layer_source,
                         "matched": 0, "unmatched": 0, "excluded": 0, "missing": None, "complete": False, "missing_reason": reason,
                         "notes": reason, "denominator": None, "snapshot_date": SNAPSHOT_DATE_DEPTH, "license": layer_license,
                         "coverage_percentage": None, "exclusion_reasons": []})

    write_json(DOMAIN_STATUS_PATH, domain_status)
    manifest = load_json(MANIFEST_PATH)
    depth_layer_names = {layer["layer"] for layer in DEPTH_LAYERS}
    manifest["pilot_layers"] = [layer for layer in manifest["pilot_layers"] if layer.get("layer") not in depth_layer_names] + DEPTH_LAYERS
    depth_caveats = [
        "Depth layers carry no denominator and no inherited population; the thirteen deferred element files keep their submitting-State list unread rather than guessed.",
        "World Heritage criteria and the emirate of each inscribed property were not read in cycle 1, so both stay empty.",
    ]
    manifest["caveats"] = [caveat for caveat in manifest["caveats"] if caveat not in depth_caveats] + depth_caveats
    manifest["next_action"] = ("Read the element pages of the thirteen deferred files, the three property pages, and the constitution before extending; keep heritage places located_in-only "
                               "and the three unavailable registries without a percentage.")
    manifest["snapshot"] = {"as_of": SNAPSHOT_DATE, "snapshot_id": SNAPSHOT_ID, "status": "verified"}
    depth_coverage_ids = [f"COV-AE-{tag}" for tag in DEPTH_TAGS.values()]
    stale_coverage_ids = {f"COV-AE-{tag}" for tag in DEPTH_TAGS} | set(depth_coverage_ids)
    for schema_forbidden_key in ("depth_status", "depth_snapshot", "depth_snapshot_id"):
        manifest.pop(schema_forbidden_key, None)
    manifest["coverage_record_ids"] = [cov_id for cov_id in manifest.get("coverage_record_ids", []) if cov_id not in stale_coverage_ids] + depth_coverage_ids
    authority = manifest.get("official_authority", {})
    authority["source_ids"] = sorted(set(authority.get("source_ids", [])) | {
        "SRC-UNESCO-ICH-AE-STATE-2026", "SRC-UNESCO-WH-AE-STATE-2026", "SRC-AE-ISO639-3-ARABIC"})
    manifest["official_authority"] = authority
    write_json(MANIFEST_PATH, manifest)

    replace_rows(
        ROOT / "data/entities/entities.jsonl",
        lambda row: row.get("country_code") == "AE" and row.get("id") != "ENT-AE-COUNTRY",
        entities,
    )
    replace_rows(
        ROOT / "data/aliases/aliases.jsonl",
        lambda row: str(row.get("entity_id", "")).startswith("ENT-AE-") and row.get("entity_id") != "ENT-AE-COUNTRY",
        aliases,
    )
    replace_rows(ROOT / "data/relationships/relationships.jsonl", lambda row: str(row.get("child_id", "")).startswith("ENT-AE-"), relationships)
    replace_rows(ROOT / "data/claims/claims.jsonl", lambda row: str(row.get("subject_id", "")).startswith("ENT-AE-"), claims)
    replace_rows(ROOT / "data/coverage/denominators.jsonl", lambda row: row.get("country_code") == "AE", denominators)
    replace_rows(ROOT / "data/coverage/coverage.jsonl", lambda row: row.get("country_code") == "AE", coverage)
    replace_rows(ROOT / "data/snapshots/snapshots.jsonl", lambda row: str(row.get("id", "")).startswith("SNP-AE-"), [snapshot, depth_snapshot])

    closed = [row for row in profile["layers"] if row["denominator"] is not None]
    unavailable = [row for row in profile["layers"] if row["denominator"] is None]
    assert sum(row["matched"] for row in closed) == 41  # country + 40 pilot entities
    assert len(layer_by_name) == 12 and len(unavailable) == 3
    print(
        "UAE import complete: "
        f"{len(entities) + 1} entities including country, {len(aliases) + 1} aliases including country, "
        f"{len(relationships)} relationships, {len(claims)} claims ({len(depth_claims)} depth claims), "
        f"{len(denominators)} denominators, {len(DEPTH_LAYERS)} depth layers, snapshots SNP-AE-PILOT-20260815 and {DEPTH_SNAPSHOT_ID}."
    )


if __name__ == "__main__":
    main()
