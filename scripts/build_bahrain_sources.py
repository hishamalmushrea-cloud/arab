#!/usr/bin/env python3
"""Materialize atomic Bahrain sources from checksum-bound production fixtures."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from model import ROOT, SCHEMA_VERSION, write_json

IMPORT = ROOT / "data/imports/bahrain"
CATALOG = IMPORT / "source_catalog.json"
MANIFEST = IMPORT / "snapshot_manifest.json"
SOURCES = ROOT / "data/sources"
RETRIEVED = "2026-08-16"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def checksum(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest() -> None:
    manifest = load(MANIFEST)
    if manifest.get("schema_version") != SCHEMA_VERSION or manifest.get("country_code") != "BH":
        raise SystemExit("invalid Bahrain snapshot manifest identity/version")
    for row in manifest["records"]:
        path = ROOT / row["path"]
        payload = path.read_bytes()
        if len(payload) != row["bytes"] or hashlib.sha256(payload).hexdigest() != row["sha256"]:
            raise SystemExit(f"Bahrain fixture checksum changed: {row['path']}")


def source(identifier: str, title: str, publisher: str, source_type: str, url: str,
           language: str, locator: str, license_text: str, fixture: str, notes: str,
           publication_date: str | None = None) -> dict:
    return {
        "id": identifier,
        "schema_version": SCHEMA_VERSION,
        "title": title,
        "publisher": publisher,
        "source_type": source_type,
        "url": url,
        "archive_url": None,
        "publication_date": publication_date,
        "retrieved_at": RETRIEVED,
        "license": license_text,
        "language": language,
        "country_codes": ["BH"],
        "locator": locator,
        "checksum": checksum(ROOT / fixture),
        "quality_tier": "A",
        "notes": notes,
    }


def records() -> list[dict]:
    area_fixture = "data/imports/bahrain/fixtures/area_by_governorate_2024.json"
    whc_fixture = "data/imports/bahrain/fixtures/world_heritage_2026.json"
    policy_fixture = "data/imports/bahrain/raw/2026-08-16/open_data_policy.txt"
    pearling_fixture = "data/imports/bahrain/raw/2026-08-16/pearling_baca.txt"
    open_license = "Bahrain Open Data Policy: republication and distribution permitted, subject to applicable laws"
    whc_license = "CC BY-SA 3.0 IGO for property descriptions"
    common_unesco_note = "Checksum binds the committed Bahrain World Heritage selection fixture. Publication date unavailable on the live record; inscription year is data, not publication date."
    return [
        source(
            "SRC-BH-SLRB-GOVERNORATE-AREA-2024", "Area by Governorate — 2024 records",
            "Survey and Land Registration Bureau", "official_dataset",
            "https://www.data.gov.bh/explore/dataset/02-area-by-governorate-2023/", "ar-en",
            "2024 filter: four records, N 76–79; governorate Arabic/English name and area value",
            open_license, area_fixture,
            "Official national portal metadata identifies the publisher and states that Bahrain was redivided into four governorates instead of five in 2014. Checksum binds the exact four-record persisted extraction. Publication date unavailable; portal metadata/data were modified 2025-12-24.",
        ),
        source(
            "SRC-BH-OPEN-DATA-POLICY-2026", "Bahrain Open Data Policy",
            "Information & eGovernment Authority", "institutional_page",
            "https://www.api.data.gov.bh/en/ODPolicy", "en",
            "paragraph permitting republication/distribution and describing National Open Data Portal availability",
            open_license, policy_fixture,
            "Relevant policy excerpt persisted locally. Publication date unavailable on captured policy page.",
        ),
        source(
            "SRC-UNESCO-WHC-BH-2026", "World Heritage List — Bahrain properties",
            "UNESCO World Heritage Centre", "institutional_dataset",
            "https://whc.unesco.org/en/statesparties/bh", "en",
            "Bahrain State Party list: three inscribed cultural properties; tentative list excluded",
            whc_license, whc_fixture, common_unesco_note,
        ),
        source(
            "SRC-UNESCO-WHC-BH-1192", "Qal’at al-Bahrain – Ancient Harbour and Capital of Dilmun",
            "UNESCO World Heritage Centre", "institutional_page",
            "https://whc.unesco.org/en/list/1192", "ar-en",
            "property 1192; official name, Arabic name, cultural category, inscription year 2005",
            whc_license, whc_fixture, common_unesco_note,
        ),
        source(
            "SRC-UNESCO-WHC-BH-1364", "Pearling, Testimony of an Island Economy",
            "UNESCO World Heritage Centre", "institutional_page",
            "https://whc.unesco.org/en/list/1364", "en",
            "property 1364; official name, cultural category, inscription year 2012",
            whc_license, whc_fixture, common_unesco_note,
        ),
        source(
            "SRC-UNESCO-WHC-BH-1542", "Dilmun Burial Mounds",
            "UNESCO World Heritage Centre", "institutional_page",
            "https://whc.unesco.org/en/list/1542", "ar-en",
            "property 1542; official name, Arabic name, cultural category, inscription year 2019",
            whc_license, whc_fixture, common_unesco_note,
        ),
        source(
            "SRC-BH-BACA-PEARLING-PATH", "طريق اللؤلؤ",
            "هيئة البحرين للثقافة والآثار", "institutional_page",
            "https://www.culture.gov.bh/ar/authority/infra_projects/Name,14932,ar.php", "ar",
            "official Arabic project name and bounded route description",
            "Bahrain Authority for Culture and Antiquities; factual extraction with attribution",
            pearling_fixture,
            "Relevant exact excerpt persisted locally. Publication date unavailable on captured authority page.",
        ),
    ]


def main() -> None:
    verify_manifest()
    rows = records()
    expected = {row["id"] for row in rows}
    for path in SOURCES.glob("*.json"):
        try: existing = load(path)
        except Exception: continue
        if existing.get("country_codes") == ["BH"] and existing.get("id") not in expected:
            raise SystemExit(f"unexpected Bahrain-only source: {existing.get('id')}")
    for row in rows:
        write_json(SOURCES / f"{row['id']}.json", row)
    write_json(CATALOG, {"schema_version": SCHEMA_VERSION, "country_code": "BH", "sources": rows})
    print(f"Materialized {len(rows)} Bahrain atomic sources.")


if __name__ == "__main__":
    main()
