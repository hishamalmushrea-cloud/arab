#!/usr/bin/env python3
"""Materialize immutable Saudi source metadata from the checked-in snapshot manifest.

The source records are metadata; administrative evidence is checksum-bound to local HTML.
Cultural source locators point to stable institutional or scholarly records and are captured
as bounded assertions in data/imports/saudi/cultural_content_2026.json.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/imports/saudi/snapshot_manifest.json"
OUT = ROOT / "data/sources"

REGION_NAMES = {
    "riyadh": "Riyadh Region",
    "makkah": "Makkah Region",
    "madinah": "Madinah Region",
    "qassim": "Al-Qassim Region",
    "eastern": "Eastern Province",
    "asir": "Asir Region",
    "tabuk": "Tabuk Region",
    "hail": "Hail Region",
    "northern-borders": "Northern Borders Region",
    "jazan": "Jazan Region",
    "najran": "Najran Region",
    "al-baha": "Al-Baha Region",
    "al-jawf": "Al-Jawf Region",
}


def record(source_id: str, title: str, publisher: str, url: str, tier: str,
           *, checksum: str | None = None, notes: str = "",
           source_type: str = "institutional_page", language: str = "ar",
           publication_date: str | None = None, locator: str = "title and cited locator") -> dict:
    if publication_date is None and "Publication date unavailable" not in notes:
        notes = f"{notes} Publication date unavailable on the captured record.".strip()
    return {
        "id": source_id,
        "schema_version": "1.0.0",
        "title": title,
        "author": None,
        "organization": publisher,
        "publisher": publisher,
        "source_type": source_type,
        "url": url,
        "archive_url": None,
        "publication_date": publication_date,
        "retrieved_at": "2026-08-15",
        "license": "Source copyright; factual extraction with attribution",
        "language": language,
        "country_codes": ["SA"],
        "locator": locator,
        "checksum": f"sha256:{checksum}" if checksum else None,
        "quality_tier": tier,
        "notes": notes or None,
    }


def main() -> int:
    snapshot = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_key = {r["source_id"]: r for r in snapshot["records"]}
    records: list[dict] = []

    national = by_key["saudipedia-national-administrative-divisions"]
    records.append(record(
        "SRC-SA-SAUDIPEDIA-ADMIN-2026",
        "Administrative Division of Saudi Arabia",
        "Saudipedia",
        national["url"],
        "A",
        checksum=national["sha256"],
        notes=f"Local snapshot: data/imports/saudi/{national['path']}. Reports 13 regions, 150 governorates and 1,377 centers; governorate and center totals conflict with other/current table evidence and are not adopted as closed national denominators.",
        source_type="institutional_page",
        locator="article body: hierarchy names and reported national aggregate counts",
    ))
    gastat = by_key["gastat-health-determinants-methodology"]
    records.append(record(
        "SRC-SA-GASTAT-HEALTH-METHOD-2026",
        "Methodology and Quality Report of Health Determinants Statistics Publication",
        "General Authority for Statistics (GASTAT)",
        gastat["url"],
        "A",
        checksum=gastat["sha256"],
        notes=f"Local snapshot: data/imports/saudi/{gastat['path']}. Methodology scope reports 13 administrative regions and 151 governorates for 2024 data.",
        source_type="official_report",
        locator="methodology scope: 13 administrative regions and 151 governorates for 2024 data",
    ))

    for slug, name in REGION_NAMES.items():
        raw = by_key[f"saudipedia-centers-{slug}"]
        records.append(record(
            f"SRC-SA-SAUDIPEDIA-CENTERS-{slug.upper()}-2026",
            f"List of Administrative Centers in {name}",
            "Saudipedia",
            raw["url"],
            "A",
            checksum=raw["sha256"],
            notes=f"Local snapshot: data/imports/saudi/{raw['path']}. Parsed deterministically as a dated published-row registry; not asserted to be a complete current-national center registry.",
            source_type="institutional_page",
            locator="first administrative-centers table, all published data rows",
        ))

    snapshot_manifest_checksum = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
    cultural_path = ROOT / "data/imports/saudi/cultural_content_2026.json"
    cultural_checksum = hashlib.sha256(cultural_path.read_bytes()).hexdigest()
    records.append(record(
        "SRC-SA-ADMIN-SNAPSHOT-CATALOG-2026",
        "Saudi administrative source snapshot catalog, 2026-08-15",
        "arab data project",
        "https://github.com/hishamalmushrea-cloud/arab/blob/arena/01a00307-arab/data/imports/saudi/snapshot_manifest.json",
        "B",
        checksum=snapshot_manifest_checksum,
        notes="Project audit catalog binding fifteen local HTML snapshots to retrieval URLs, byte sizes and SHA-256 checksums. Publication date is the snapshot date.",
        source_type="project_audit", language="en", publication_date="2026-08-15",
        locator="records array: all 15 retrieval records",
    ))
    records.append(record(
        "SRC-SA-LAW-OF-PROVINCES-1992",
        "نظام المناطق (Law of Provinces)",
        "هيئة الخبراء بمجلس الوزراء",
        "https://laws.boe.gov.sa/BoeLaws/Laws/LawDetails/93f81644-fbbc-49ca-b33c-a9a700f16701/1",
        "A",
        notes="Royal Order A/92, issued 1992-03-01 and published 1992-03-06; current-status law record. Articles 2, 3 and 13 define region organization, المحافظات, النواحي and المراكز and Interior Ministry roles.",
        source_type="law", language="ar", publication_date="1992-03-06",
        locator="المواد الثانية والثالثة والثالثة عشرة",
    ))
    records.append(record(
        "SRC-SA-CULTURAL-FIXTURE-2026",
        "Saudi bounded cultural-content extraction fixture, 2026-08-15",
        "arab data project",
        "https://github.com/hishamalmushrea-cloud/arab/blob/arena/01a00307-arab/data/imports/saudi/cultural_content_2026.json",
        "B",
        checksum=cultural_checksum,
        notes="Project audit fixture containing only bounded assertions and exact upstream source locators. Publication date is the fixture date.",
        source_type="project_audit", language="en", publication_date="2026-08-15",
        locator="complete JSON document",
    ))

    institutional = [
        ("SRC-UNESCO-WHC-SA-STATE-2026", "Saudi Arabia — properties inscribed on the World Heritage List", "UNESCO World Heritage Centre", "https://whc.unesco.org/en/statesparties/sa", "A", "Institutional live record consulted 2026-08-15; bounded property count and list."),
        ("SRC-UNESCO-WHC-SA-1293", "Hegra Archaeological Site (al-Hijr / Madā’in Ṣāliḥ)", "UNESCO World Heritage Centre", "https://whc.unesco.org/en/list/1293", "A", "Institutional property record, reference 1293."),
        ("SRC-UNESCO-WHC-SA-1329", "At-Turaif District in ad-Dir'iyah", "UNESCO World Heritage Centre", "https://whc.unesco.org/en/list/1329", "A", "Institutional property record, reference 1329."),
        ("SRC-UNESCO-WHC-SA-1361", "Historic Jeddah, the Gate to Makkah", "UNESCO World Heritage Centre", "https://whc.unesco.org/en/list/1361", "A", "Institutional property record, reference 1361."),
        ("SRC-UNESCO-WHC-SA-1472", "Rock Art in the Hail Region of Saudi Arabia", "UNESCO World Heritage Centre", "https://whc.unesco.org/en/list/1472", "A", "Institutional property record, reference 1472."),
        ("SRC-UNESCO-WHC-SA-1563", "Al-Ahsa Oasis, an Evolving Cultural Landscape", "UNESCO World Heritage Centre", "https://whc.unesco.org/en/list/1563", "A", "Institutional property record, reference 1563."),
        ("SRC-UNESCO-WHC-SA-1619", "Ḥimā Cultural Area", "UNESCO World Heritage Centre", "https://whc.unesco.org/en/list/1619", "A", "Institutional property record, reference 1619."),
        ("SRC-UNESCO-WHC-SA-1699", "‘Uruq Bani Ma’arid", "UNESCO World Heritage Centre", "https://whc.unesco.org/en/list/1699", "A", "Institutional property record, reference 1699."),
        ("SRC-UNESCO-WHC-SA-1712", "The Cultural Landscape of Al-Faw Archaeological Area", "UNESCO World Heritage Centre", "https://whc.unesco.org/en/list/1712", "A", "Institutional property record, reference 1712."),
        ("SRC-UNESCO-ICH-SA-01011", "Almezmar, drumming and dancing with sticks", "UNESCO Intangible Cultural Heritage", "https://ich.unesco.org/en/RL/almezmar-drumming-and-dancing-with-sticks-01011", "A", "Institutional Representative List record 01011; multinational/shared status is preserved."),
        ("SRC-UNESCO-ICH-SA-01196", "Alardah Alnajdiyah, dance, drumming and poetry in Saudi Arabia", "UNESCO Intangible Cultural Heritage", "https://ich.unesco.org/en/RL/alardah-alnajdiyah-dance-drumming-and-poetry-in-saudi-arabia-01196", "A", "Institutional Representative List record 01196."),
        ("SRC-UNESCO-ICH-SA-01261", "Al-Qatt Al-Asiri, female traditional interior wall decoration in Asir", "UNESCO Intangible Cultural Heritage", "https://ich.unesco.org/en/RL/al-qatt-al-asiri-female-traditional-interior-wall-decoration-in-asir-saudi-arabia-01261", "A", "Institutional Representative List record 01261."),
        ("SRC-UNESCO-ICH-SA-01863", "Knowledge and practices related to cultivating Khawlani coffee beans", "UNESCO Intangible Cultural Heritage", "https://ich.unesco.org/en/decisions/17.COM/7.B.24", "A", "UNESCO decision 17.COM 7.B.24 and Representative List reference 01863; multinational/shared status is preserved and the Jazan community verification is the regional locator."),
        ("SRC-SA-CULINARY-REGIONAL-DISHES-2024", "Saudi Culinary Arts Commission announces regional dishes for all 13 provinces", "Saudi Gazette", "https://saudigazette.com.sa/article/639431/SAUDI-ARABIA/Saudi-Culinary-Arts-Commission-announces-regional-dishes-for-all-13-provinces-nbsp", "B", "Dated 2024-01-08. Secondary report explicitly attributes selections to the Saudi Culinary Arts Commission and reports commission/emirate alignment; designations are official scope labels, not exclusivity claims."),
        ("SRC-SA-GOV-CULTURE-2026", "Culture", "Unified National Platform, Kingdom of Saudi Arabia", "https://my.gov.sa/en/content/culture", "A", "Government overview supports regional clothing diversity only; no item-to-region garment attribution is extracted."),
        ("SRC-ACADEMIC-SA-DIALECT-CORPUS-2020", "SDCT: Multi-Dialects Corpus Classification for Saudi Dialects", "International Journal of Advanced Computer Science and Applications", "https://thesai.org/Downloads/Volume11No11/Paper_28-SDCT_Multi_Dialects_Corpus_Classification.pdf", "B", "Peer-reviewed article, Vol. 11 No. 11 (2020), DOI 10.14569/IJACSA.2020.0111128. Used only for explicit lexical examples, meanings and informal social-media register; not for a national dialect count."),
    ]
    for args in institutional:
        sid = args[0]
        source_type = "academic" if sid.startswith("SRC-ACADEMIC") else ("archive" if sid.startswith("SRC-SA-CULINARY") else ("official_report" if sid.startswith("SRC-SA-GOV") else "institutional_page"))
        publication_date = "2024-01-08" if sid.startswith("SRC-SA-CULINARY") else ("2020-12" if sid.startswith("SRC-ACADEMIC") else None)
        records.append(record(*args[:5], notes=args[5], source_type=source_type,
                              language="en", publication_date=publication_date))

    OUT.mkdir(parents=True, exist_ok=True)
    for item in records:
        path = OUT / f"{item['id']}.json"
        path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    expected = {f"{item['id']}.json" for item in records}
    print(json.dumps({
        "sources_written": len(records),
        "source_ids": sorted(item["id"] for item in records),
        "catalog_sha256": hashlib.sha256(json.dumps(records, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
        "unexpected_existing_sa_sources": sorted(p.name for p in OUT.glob("SRC-SA-*.json") if p.name not in expected),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
