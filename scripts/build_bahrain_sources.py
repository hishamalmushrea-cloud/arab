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
DEPTH_RETRIEVED = "2026-09-20"


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
           publication_date: str | None = None, tier: str = "A",
           retrieved: str = RETRIEVED) -> dict:
    return {
        "id": identifier,
        "schema_version": SCHEMA_VERSION,
        "title": title,
        "publisher": publisher,
        "source_type": source_type,
        "url": url,
        "archive_url": None,
        "publication_date": publication_date,
        "retrieved_at": retrieved,
        "license": license_text,
        "language": language,
        "country_codes": ["BH"],
        "locator": locator,
        "checksum": checksum(ROOT / fixture),
        "quality_tier": tier,
        "notes": notes,
    }


def base_records() -> list[dict]:
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


def depth_records() -> list[dict]:
    """Depth cycle 1 sources: a UNESCO intangible-heritage spine plus classified local material."""
    depth_fixture = "data/imports/bahrain/fixtures/cultural_depth_2026.json"
    ich_license = "UNESCO ICH pages; factual extraction with attribution"
    mirror_license = "CC BY-SA 4.0 for the mirror text"
    press_license = "Local press column; factual extraction with attribution; reuse terms not stated"
    local_notes = "Publication date unavailable on the live page. Depth-cycle tier-E material: claims stay local_reported and unpublished."
    return [
        source(
            "SRC-BH-UNESCO-ICH-2026", "Elements on the Lists — Bahrain State Party",
            "UNESCO Intangible Cultural Heritage", "institutional_dataset",
            "https://ich.unesco.org/en/state/bahrain-BH?info=elements-on-the-lists", "en",
            "inscribed elements: Fjiri 2021 ref 01747, Arabic calligraphy 2021 ref 01718, Date palm 2022 ref 01902, Henna 2024 ref 02116, Bisht 2025 ref 02233",
            ich_license, depth_fixture,
            "Publication date unavailable on the live State Party list page. Only elements on which Bahrain appears are imported; multi-State files stay shared and are never asserted as exclusively Bahraini.",
            retrieved=DEPTH_RETRIEVED,
        ),
        source(
            "SRC-BH-FJIRI-01747", "Fjiri",
            "UNESCO Intangible Cultural Heritage", "institutional_page",
            "https://ich.unesco.org/en/RL/fjiri-01747", "en",
            "inscription year 2021 on the Representative List; description of the circle performance, drums, finger chimes, jahl clay pot, durs, and the Muharraq pearling origin",
            ich_license, depth_fixture,
            "Element description is the same UNESCO record used for the inscription claim. Publication date unavailable.",
            retrieved=DEPTH_RETRIEVED,
        ),
        source(
            "SRC-BH-DIALECT-MIRROR-2026", "لهجة بحرينية — موسوعة مرآة",
            "ويكيبيديا العربية (نسخة مرآة)", "local_website",
            "https://ar.wikipedia.org/wiki/لهجة_بحرينية", "ar",
            "تصنيف لهجات البحرين الثلاث (البحرانية، المحرقية، الخليجية) وقول المصدر صراحةً إنه لا توجد لهجة بحرينية واحدة",
            mirror_license, depth_fixture,
            local_notes, tier="E", retrieved=DEPTH_RETRIEVED,
        ),
        source(
            "SRC-BH-CUISINE-MIRROR-2026", "مطبخ بحريني — موسوعة مرآة",
            "ويكيبيديا العربية (نسخة مرآة)", "local_website",
            "https://ar.wikipedia.org/wiki/مطبخ_بحريني", "ar",
            "أقسام أطباق الأرز والوجبات البحرية والوجبات الخالية من الأرز والإفطار البحريني مع وصف كل طبق",
            mirror_license, depth_fixture,
            local_notes, tier="E", retrieved=DEPTH_RETRIEVED,
        ),
        source(
            "SRC-BH-FOLK-CLOTH-2022", "القماش وتجارته في البحرين",
            "مجلة الثقافة الشعبية (البحرين) — العدد 58", "heritage_book",
            "https://www.folkculturebh.org/ar/index.php?issue=58&page=article&id=1113", "ar",
            "أسماء الأقمشة ومصطلحات التجارة والخياطة (خلق، طاقة، جفير، الكراخانة) وأسماء الزي الشعبي: العباءة، ثوب النشل، البخنق، النفنوف، الجلابية، ثوب النقدة، ومناطق النسيج: بني جمرة والجسرة والمحرق",
            "Bahraini folklore journal article by خميس البنكي; factual extraction with attribution; reuse terms not stated",
            depth_fixture,
            "Article page dated July 2022 in the journal index. Tier-E heritage journal material: claims stay local_reported and unpublished.",
            publication_date="2022-07-01", tier="E", retrieved=DEPTH_RETRIEVED,
        ),
        source(
            "SRC-BH-NASHIL-PRESS-2018", "البحرين.. مملكة الموروث التراثي الثقافي",
            "صحيفة الاتحاد", "local_press",
            "https://www.aletihad.ae/article/78925/2018/", "ar",
            "تقرير عن ثوب النشل وأنواعه وطريقة لبسه، والبخنق الأسود للفتيات، والدراعة تحته، ومناسبات اللبس (الجلوه، اليلوه، ليلة الحناء، الناصفة، القرقيعان)",
            press_license, depth_fixture,
            "Report dated 2018-12-09. Tier-E press material: dress details stay local_reported and unpublished.",
            publication_date="2018-12-09", tier="E", retrieved=DEPTH_RETRIEVED,
        ),
        source(
            "SRC-BH-MUHARRAQ-WIKI-2026", "المحرق (مدينة) — موسوعة مرآة",
            "ويكيبيديا العربية (نسخة مرآة)", "local_website",
            "https://ar.wikipedia.org/wiki/المحرق_(مدينة)", "ar",
            "قسم مناطق المحرق: أسماء الفرجان (الحياك، الصاغة، السكران، البنائين، الزياني، الصنقل، آل بن علي، البن هندي، المري، الزياينة، بن رشدان، البن خاطر، البوخميس) ومصطلحا الداعوس والزرنوق، وتكوين السكان: قبائل عربية سنية وهولة وبستكية وعجم وبحارنة",
            mirror_license, depth_fixture,
            local_notes, tier="E", retrieved=DEPTH_RETRIEVED,
        ),
        source(
            "SRC-BH-FIRJAN-BLOG-2022", "فرجان المحرق القديمة",
            "موقع الشيخ صلاح الجودر (سلسلة محلية)", "blog",
            "https://www.salahaljowder.com/2022/06/blog-post_9.html", "ar",
            "الحلقة 3: معنى الفريج والداعوس والزرنوق، واعتبارات تسمية الفرجان (القبيلة، التاجر، علامة المكان) وأمثلة: فريج الشيوخ، فريج المحميد، فريج بن هندي، فريج الغاوي، فريج ستسيشن، فريج عين سمادو، وتشكل التسمية مع استيطان المحرق سنة 1796",
            "Self-published local heritage series; factual extraction with attribution; reuse terms not stated",
            depth_fixture,
            "Page dated 2022-06-09. Tier-E blog material used only for naming narratives at local_reported.",
            publication_date="2022-06-09", tier="E", retrieved=DEPTH_RETRIEVED,
        ),
        source(
            "SRC-BH-FIRJAN-ELAPH-2023", "الحنين إلى الماضي.. الفرجان القديمة جزء من الهوية",
            "إيلاف", "local_press",
            "https://elaph.com/Web/NewsPapers/2023/12/1521289.html", "ar",
            "مقال عن فرجان المحرق والمنامة القديمة ودواعيسها وأسواقها ومقاهيها وبيوتها الطينية والحجرية وحضور أسماء الطواويش والنواخذة والبحارة في الذاكرة المحلية",
            press_license, depth_fixture,
            "Column dated 2023-12-03. Tier-E press material: memory and craft framing stays local_reported and unpublished.",
            publication_date="2023-12-03", tier="E", retrieved=DEPTH_RETRIEVED,
        ),
        source(
            "SRC-BH-ALBILAD-2021", "عمارة المحرق التقليدية وفرجانها",
            "جريدة البلاد", "local_press",
            "https://albiladpress.com/news/2021/4508/columns/693672.html", "ar",
            "عمود يقرر أن عمرانية الجزيرة تتشكل من مدينة المحرق ومن قرى وحالات وأحياء أو فرجان: القرى الدير وسماهيج وقلالي والحد والبسيتين وعراد بقلعتها البرتغالية (القرن 16م)، والحالات كحالة بوماهر والنعيم والسلطة، وفرجان المهن (البنائين والحياك والصاغة) وفرجان العوائل (الشيوخ والبنعلي والمناعي)، وبيوت تراثية: بيت الشيخ عيسى بن علي وبيت ومجلس سيادي وبيت الشيخ سلمان بن حمد",
            press_license, depth_fixture,
            "Column dated 2021-02-16. Tier-E press material: village/hala and farij names enter as local_reported places with located_in only.",
            publication_date="2021-02-16", tier="E", retrieved=DEPTH_RETRIEVED,
        ),
    ]


def records() -> list[dict]:
    return base_records() + depth_records()


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
