#!/usr/bin/env python3
"""Build the Yemen depth-cycle-2 urban-sections fixture from checksum-bound OSM extracts.

The extracts under ``data/imports/yemen/raw/2026-09-23/`` are one file per Amanat
Al Asimah district and carry, in plain text, the exact fields this project needs:
the query that produced them, the OSM base timestamp, and one line per named
place feature. Nothing here invents a name: a district appears in the fixture
only when its extract file exists, and the fixture records every district whose
extract is still missing, with the reason.
"""
import json
import re
import pathlib

from model import ROOT, read_jsonl, write_json

RAW = ROOT / "data/imports/yemen/raw/2026-09-23"
FIXTURE = ROOT / "data/imports/yemen/fixtures/amanat_urban_sections_2026.json"
ACCEPTED = ROOT / "data/imports/yemen/fixtures/amanat_lanes_2026.json"
FRAME_LAYER = "ye_amanat_urban_sections_2026"
CAPTURED_AT = "2026-09-23"
URBAN_CLASSES = {"neighbourhood", "quarter", "suburb", "city_block"}
EXTRACT_PATTERN = re.compile(r"osm-amanat-(?P<slug>[a-z0-9-]+)-(?P<date>\d{8})\.txt$")
SLUG_DIRECT = {
    "شعوب": "SHUUB",
    "أزال": "AZAL",
    "الصافية": "SAFIYA",
    "السبعين": "SABEEN",
    "الوحدة": "WAHDA",
    "معين": "MAEEN",
    "الثورة": "THAWRA",
    "بني الحارث": "BANI-HARITH",
    "صنعاء القديمة": "OLD-SANAA",
    "التحرير": "TAHRIR",
}
ACCEPTED_DISTRICTS = {
    "صنعاء القديمة": "Old Sanaa 69-lane inventory (accepted depth level 1)",
    "التحرير": "Tahrir 35-lane hay tables (accepted depth level 1)",
}


def district_entity_ids() -> dict[str, str]:
    rows = [r for r in read_jsonl(ROOT / "data/entities/entities.jsonl") if r.get("entity_type") == "ye_district"]
    return {r["canonical_name"]: r["id"] for r in rows}


def frame() -> dict[str, dict]:
    data = json.loads(ACCEPTED.read_text(encoding="utf8"))
    out = {}
    for row in data["amanat_2004_frame"]["district_lane_counts"]:
        out[row["district"]] = row
    return out


def parse_extract(path: pathlib.Path) -> dict:
    header, sections, district_node = {}, [], None
    for line in path.read_text(encoding="utf8").splitlines():
        if "|" in line and not line.startswith(("Fields:", "OSM Overpass", "Data:", "Query:", "Retrieved:")):
            if line.startswith("District node"):
                district_node = line
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 4 or parts[1] not in URBAN_CLASSES:
                continue
            sections.append(
                {
                    "name": parts[0],
                    "place": parts[1],
                    "object": parts[2],
                    "gns": None if parts[3] in {"-", ""} else parts[3],
                    "name_source": parts[4] if len(parts) > 4 else "",
                }
            )
            continue
        key, _, value = line.partition(": ")
        if key.startswith("OSM Overpass"):
            header["title"] = line
        elif key in {"Query", "Retrieved", "Fields"}:
            header[key] = value
        elif key.startswith("Data:"):
            header["license"] = value
    header["district"] = re.search(r"— district: (?P<name>.+)$", header.get("title", "")).group("name").strip()
    stamp = re.search(r"OSM base timestamp: (?P<stamp>[0-9T:Z-]+)", header.get("Retrieved", ""))
    header["osm_base_timestamp"] = stamp.group("stamp") if stamp else None
    header["returned"] = re.search(r"(place nodes returned|named place features returned|elements returned): (?P<n>\d+)", header.get("Retrieved", ""))
    header["returned"] = int(header["returned"].group("n")) if header["returned"] else None
    header["path"] = str(path.relative_to(ROOT / "data/imports/yemen"))
    header["sections"] = sections
    header["district_node"] = district_node
    return header


def main() -> int:
    ids, framef = district_entity_ids(), frame()
    extracted = {}
    for path in sorted(RAW.glob("osm-amanat-*-20260923.txt")):
        parsed = parse_extract(path)
        assert EXTRACT_PATTERN.match(path.name), path.name
        assert parsed["district"] in framef, parsed["district"]
        assert parsed["district"] in ids, parsed["district"]
        assert parsed["sections"], f"no urban sections parsed from {path.name}"
        assert len({(s["name"], s["object"]) for s in parsed["sections"]}) == len(parsed["sections"]), path.name
        extracted[parsed["district"]] = parsed

    districts = []
    for name, row in framef.items():
        if name not in extracted:
            continue
        parsed = extracted[name]
        sections = parsed["sections"]
        classes: dict[str, int] = {}
        for section in sections:
            classes[section["place"]] = classes.get(section["place"], 0) + 1
        districts.append(
            {
                "district": name,
                "code": SLUG_DIRECT[name],
                "district_id": ids[name],
                "frame_lanes_2004": row["lanes"],
                "frame_neighborhoods_2004": row["neighborhoods"],
                "extract": parsed["path"],
                "extract_query": parsed["Query"],
                "osm_base_timestamp": parsed["osm_base_timestamp"],
                "classes": dict(sorted(classes.items())),
                "sections": sections,
            }
        )

    open_districts = []
    for name, row in framef.items():
        if name in extracted or name in ACCEPTED_DISTRICTS:
            continue
        open_districts.append(
            {
                "district": name,
                "code": SLUG_DIRECT[name],
                "frame_lanes_2004": row["lanes"],
                "frame_neighborhoods_2004": row["neighborhoods"],
                "status": "not_retrieved",
                "reason": "Overpass API returned a runtime read timeout on every 2026-09-23 retry for this district area; no name is fabricated and the frame count stays the denominator.",
            }
        )

    fixture = {
        "schema_version": "2.0.0",
        "country_code": "YE",
        "cycle": "second_degree_depth_cycle_2",
        "layer": FRAME_LAYER,
        "captured_at": CAPTURED_AT,
        "method": (
            "Named urban sections (حي / حارة / محلة) enumerated per Amanat Al Asimah district from a dated OpenStreetMap "
            "Overpass snapshot; every extract is mirrored under raw/2026-09-23/ and bound by checksum in the snapshot "
            "manifest. Rural place classes (village, hamlet, farm, locality, isolated_dwelling) are excluded and left to a "
            "later settlement layer; no coordinate, population or share is imported from this source."
        ),
        "source": {
            "endpoint": "https://overpass-api.de/api/interpreter",
            "license": "ODbL 1.0 — © OpenStreetMap contributors (https://www.openstreetmap.org/copyright)",
            "gazetteer": (
                "Features tagged source:name=GNS carry the public-domain NGA GEOnet Names Server id; the GNS tag 'PPLX' "
                "means 'section of populated place'. Features without that tag are community-mapped and stay unverified."
            ),
            "canonical_name_rule": "the Arabic value wins; when both name and name:ar are Arabic and differ, the name tag is canonical and the other rendering is recorded in the extract line.",
        },
        "districts": districts,
        "open_districts": open_districts,
        "accepted_districts": ACCEPTED_DISTRICTS,
        "absences": [
            "لا إحداثيات: المصدر يقدّم مركز كل عنصر لكن الطبقة تُبقي الإحداثيات فارغة مثل سابقتها.",
            "لا سكان ولا أعداد: أرقام 2004 تبقى كما هي في الطبقة المقبولة ولا تُسحب من هذه اللقطة.",
            "لا نسبة مُستنتَجة: التغطية تُحسب فقط لكل مديرية على حِدة مقابل إطار 2004، ولا تُعمّم على المديريات غير المسترجَعة.",
            "لا وسوم نطاق: عناصر يونسكو أو التراث العالمي ليست في هذه الطبقة.",
            "لا تصنيف للطبقة الريفية: القرى والنجوع والمزارع مستبعدة صراحةً ولم تُدرَج باسم حيّ.",
        ],
    }
    fixture["summary"] = {
        "districts_completed": len(districts),
        "sections": sum(len(d["sections"]) for d in districts),
        "districts_open": len(open_districts),
        "sections_per_district": {d["district"]: len(d["sections"]) for d in districts},
    }
    write_json(FIXTURE, fixture)
    print(json.dumps(fixture["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
