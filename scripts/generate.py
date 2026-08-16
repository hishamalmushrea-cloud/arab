#!/usr/bin/env python3
"""Generate Markdown, HTML, JSON, and CSV views from Schema 2.0.0 data only."""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from model import COUNTRIES, ROOT, read_jsonl

OUT = ROOT / "generated"
DATASETS = {
    "entities": ROOT / "data/entities/entities.jsonl",
    "aliases": ROOT / "data/aliases/aliases.jsonl",
    "relationships": ROOT / "data/relationships/relationships.jsonl",
    "claims": ROOT / "data/claims/claims.jsonl",
    "snapshots": ROOT / "data/snapshots/snapshots.jsonl",
    "denominators": ROOT / "data/coverage/denominators.jsonl",
    "coverage": ROOT / "data/coverage/coverage.jsonl",
}


def load() -> dict[str, list[dict[str, Any]]]:
    data = {name: read_jsonl(path) for name, path in DATASETS.items()}
    data["sources"] = []
    for path in sorted((ROOT / "data/sources").glob("*.json")):
        data["sources"].append(json.loads(path.read_text(encoding="utf-8")))
    data["sources"].sort(key=lambda row: row["id"])
    return data


def jdump(value: Any, *, pretty=False) -> str:
    if pretty:
        return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def csv_text(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    preferred = ["id", "schema_version", "country_code", "canonical_name", "entity_type", "status", "source_id"]
    all_fields = set().union(*(row.keys() for row in rows))
    fields = [field for field in preferred if field in all_fields] + sorted(all_fields - set(preferred))
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: jdump(value) if isinstance(value, (dict, list)) else ("" if value is None else value) for key, value in row.items()})
    return stream.getvalue()


def md_escape(value: Any) -> str:
    if value is None: return "—"
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        return "_لا توجد سجلات في المصدر المنظم._\n"
    result = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    result.extend("| " + " | ".join(md_escape(cell) for cell in row) + " |" for row in rows)
    return "\n".join(result) + "\n"


def coverage_values(cov: dict[str, Any], den: dict[str, Any]) -> list[Any]:
    pct = cov.get("coverage_percentage")
    pct_text = "—" if pct is None else f"{pct:g}%"
    return [
        cov["layer"], den.get("definition"), den.get("value"), cov["matched"], cov["unmatched"],
        cov["excluded"], cov.get("missing"), pct_text, cov.get("snapshot_date"), cov["snapshot_id"], cov.get("source_id"), cov.get("license"),
        "نعم" if cov.get("complete") else "لا", cov.get("missing_reason"),
    ]


def country_markdown(iso: str, data: dict[str, list[dict[str, Any]]]) -> str:
    name_ar = COUNTRIES[iso][0]
    entities = [row for row in data["entities"] if row["country_code"] == iso]
    entity_ids = {row["id"] for row in entities}
    aliases = [row for row in data["aliases"] if row["entity_id"] in entity_ids]
    relations = [row for row in data["relationships"] if row["child_id"] in entity_ids]
    claims = [row for row in data["claims"] if row["subject_id"] in entity_ids]
    covs = [row for row in data["coverage"] if row["country_code"] == iso]
    den_by_id = {row["id"]: row for row in data["denominators"]}
    needed_sources = {row.get("canonical_source_id") for row in entities}
    needed_sources |= {row.get("source_id") for family in [aliases, relations, claims, covs] for row in family}
    sources = [row for row in data["sources"] if row["id"] in needed_sources]
    source_by_id = {row["id"]: row for row in data["sources"]}
    published = [row for row in claims if row.get("published")]
    ab_count = sum(source_by_id[row["source_id"]].get("quality_tier") in {"A", "B"} for row in published)
    ab_ratio = (ab_count * 100 / len(published)) if published else 0

    out = [
        f"# {name_ar} ({iso}) — عرض مولّد من Schema 2.0.0",
        "",
        "> **حدود التغطية:** التغطية المحلية غير مكتملة. لا تمثل هذه الصفحة جميع المدن أو القرى أو الأحياء أو الحارات، ولا يُستدل على التغطية من وجود ملف. البيانات المنظمة هي المصدر؛ هذه الصفحة عرض مولّد.",
        "",
        "## التغطية والمقامات",
        "",
        "أي نسبة 100% أدناه مقيدة بالدولة والطبقة والمقام المؤرخ واللقطة والمصدر الظاهرة في الصف نفسه؛ ولا تمتد إلى طبقة أخرى.",
        "",
        markdown_table(
            ["الطبقة", "تعريف المقام", "المقام", "مطابق", "غير مطابق", "مستبعد", "مفقود", "النسبة", "تاريخ اللقطة", "اللقطة", "المصدر", "الترخيص", "مكتمل", "سبب النقص"],
            [coverage_values(cov, den_by_id[cov["denominator_id"]]) for cov in covs],
        ),
        "## الكيانات",
        "",
        markdown_table(
            ["المعرّف", "الاسم", "النوع", "الحالة", "المصدر القانوني/المرجعي", "المحدد داخل المصدر"],
            [[row["id"], row["canonical_name"], row["entity_type"], row["status"], row["canonical_source_id"], row["source_locator"]] for row in entities],
        ),
        "## الأسماء البديلة",
        "",
        markdown_table(
            ["المعرّف", "الكيان", "الاسم", "اللغة", "النوع", "المصدر"],
            [[row["id"], row["entity_id"], row["name"], row["language"], row["kind"], row["source_id"]] for row in aliases],
        ),
        "## علاقات الإدارة/الموقع",
        "",
        markdown_table(
            ["المعرّف", "الابن", "الأب", "العلاقة", "الحالة", "المصدر"],
            [[row["id"], row["child_id"], row["parent_id"], row["relationship_type"], row["status"], row["source_id"]] for row in relations],
        ),
        "## الادعاءات",
        "",
        markdown_table(
            ["المعرّف", "الموضوع", "المحمول", "القيمة", "التصنيف", "الثقة", "الحالة", "المصدر", "المحدد"],
            [[row["id"], row["subject_id"], row["predicate"], row["value"]["data"], row.get("classification"), row.get("confidence"), row["status"], row["source_id"], row["source_locator"]] for row in claims],
        ),
        "## جودة مصادر الادعاءات المنشورة",
        "",
        f"ادعاءات A/B: {ab_count} من {len(published)} ({ab_ratio:.2f}%).",
        "",
        "## المصادر الذرية المستخدمة",
        "",
        markdown_table(
            ["المعرّف", "الفئة", "العنوان", "الناشر", "تاريخ النشر", "تاريخ الاسترجاع", "الترخيص", "الرابط"],
            [[row["id"], row["quality_tier"], row["title"], row["publisher"], row["publication_date"], row["retrieved_at"], row["license"], row["url"]] for row in sources],
        ),
        "---",
        "_مولّد آليًا؛ لا تعدّل هذا الملف مباشرة._",
        "",
    ]
    return "\n".join(out)


def html_table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows: return '<p class="empty">لا توجد سجلات في المصدر المنظم.</p>'
    head = "".join(f"<th>{html.escape(str(h))}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{html.escape('—' if c is None else str(c))}</td>" for c in row) + "</tr>" for row in rows)
    return f"<div class=table-wrap><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def page_html(title: str, main: str, *, parent=False) -> str:
    home = "../index.html" if parent else "index.html"
    return f"""<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>
:root{{--ink:#192229;--muted:#60727d;--line:#d9e1e5;--paper:#fff;--accent:#0a6c69;--wash:#f4f8f7}}*{{box-sizing:border-box}}body{{margin:0;background:var(--wash);color:var(--ink);font:16px/1.7 system-ui,-apple-system,"Segoe UI",Tahoma,sans-serif}}main{{max-width:1180px;margin:28px auto;background:var(--paper);padding:clamp(18px,4vw,52px);box-shadow:0 12px 36px #17353a16;border-radius:18px}}h1,h2{{line-height:1.25}}h1{{font-size:clamp(1.7rem,4vw,2.8rem);margin-top:0}}h2{{margin-top:2.4rem;border-bottom:2px solid var(--accent);padding-bottom:.35rem}}a{{color:var(--accent)}}.notice{{border-right:5px solid var(--accent);background:#eaf5f3;padding:14px 18px}}.table-wrap{{overflow:auto;border:1px solid var(--line);border-radius:10px}}table{{border-collapse:collapse;width:100%;font-size:.88rem}}th,td{{border-bottom:1px solid var(--line);padding:9px 11px;vertical-align:top;text-align:right;white-space:nowrap}}th{{background:#eef4f3;position:sticky;top:0}}.empty{{color:var(--muted)}}footer{{margin-top:3rem;color:var(--muted);font-size:.9rem}}code{{direction:ltr;unicode-bidi:embed}}</style></head>
<body><main><nav><a href="{home}">فهرس البيانات المولّدة</a></nav>{main}<footer>مولّد آليًا من Schema 2.0.0؛ لا تعدّل هذا الملف مباشرة.</footer></main></body></html>\n"""


def country_html(iso: str, data: dict[str, list[dict[str, Any]]]) -> str:
    name_ar = COUNTRIES[iso][0]
    entities = [row for row in data["entities"] if row["country_code"] == iso]
    ids = {row["id"] for row in entities}
    aliases = [row for row in data["aliases"] if row["entity_id"] in ids]
    relations = [row for row in data["relationships"] if row["child_id"] in ids]
    claims = [row for row in data["claims"] if row["subject_id"] in ids]
    covs = [row for row in data["coverage"] if row["country_code"] == iso]
    den_by_id = {row["id"]: row for row in data["denominators"]}
    source_ids = {row.get("canonical_source_id") for row in entities} | {row.get("source_id") for family in [aliases, relations, claims, covs] for row in family}
    sources = [row for row in data["sources"] if row["id"] in source_ids]
    source_by_id = {row["id"]: row for row in data["sources"]}
    published = [row for row in claims if row.get("published")]
    ab_count = sum(source_by_id[row["source_id"]].get("quality_tier") in {"A", "B"} for row in published)
    ab_ratio = (ab_count * 100 / len(published)) if published else 0
    parts = [
        f"<h1>{html.escape(name_ar)} <small>({iso})</small></h1>",
        '<p class="notice"><strong>حدود التغطية:</strong> التغطية المحلية غير مكتملة. لا تمثل هذه الصفحة جميع المدن أو القرى أو الأحياء أو الحارات، والبيانات المنظمة هي المصدر.</p>',
        "<h2>التغطية والمقامات</h2><p>أي نسبة 100% مقيدة بالدولة والطبقة والمقام المؤرخ واللقطة والمصدر في الصف نفسه.</p>",
        html_table(["الطبقة", "التعريف", "المقام", "مطابق", "غير مطابق", "مستبعد", "مفقود", "النسبة", "التاريخ", "اللقطة", "المصدر", "الترخيص", "مكتمل", "سبب النقص"], [coverage_values(c, den_by_id[c["denominator_id"]]) for c in covs]),
        "<h2>الكيانات</h2>", html_table(["المعرّف", "الاسم", "النوع", "الحالة", "المصدر", "المحدد"], [[r["id"], r["canonical_name"], r["entity_type"], r["status"], r["canonical_source_id"], r["source_locator"]] for r in entities]),
        "<h2>الأسماء البديلة</h2>", html_table(["المعرّف", "الكيان", "الاسم", "اللغة", "النوع", "المصدر"], [[r["id"], r["entity_id"], r["name"], r["language"], r["kind"], r["source_id"]] for r in aliases]),
        "<h2>العلاقات</h2>", html_table(["المعرّف", "الابن", "الأب", "العلاقة", "الحالة", "المصدر"], [[r["id"], r["child_id"], r["parent_id"], r["relationship_type"], r["status"], r["source_id"]] for r in relations]),
        "<h2>الادعاءات</h2>", html_table(["المعرّف", "الموضوع", "المحمول", "القيمة", "التصنيف", "الثقة", "الحالة", "المصدر", "المحدد"], [[r["id"], r["subject_id"], r["predicate"], r["value"]["data"], r.get("classification"), r.get("confidence"), r["status"], r["source_id"], r["source_locator"]] for r in claims]),
        "<h2>جودة مصادر الادعاءات المنشورة</h2>", f"<p>ادعاءات A/B: {ab_count} من {len(published)} ({ab_ratio:.2f}%).</p>",
        "<h2>المصادر الذرية</h2>", html_table(["المعرّف", "الفئة", "العنوان", "الناشر", "النشر", "الاسترجاع", "الترخيص", "الرابط"], [[r["id"], r["quality_tier"], r["title"], r["publisher"], r["publication_date"], r["retrieved_at"], r["license"], r["url"]] for r in sources]),
    ]
    return page_html(f"{name_ar} — Schema 2.0.0", "".join(parts), parent=True)


def render(data: dict[str, list[dict[str, Any]]]) -> dict[Path, bytes]:
    files: dict[Path, bytes] = {}
    for name, rows in data.items():
        files[Path("json") / f"{name}.json"] = jdump(rows, pretty=True).encode()
        files[Path("csv") / f"{name}.csv"] = csv_text(rows).encode()
    files[Path("json/canonical_bundle.json")] = jdump({"schema_version": "2.0.0", **data}, pretty=True).encode()

    md_index = [
        "# العروض المولّدة من Schema 2.0.0", "",
        "> البيانات المنظمة تحت `data/` هي المصدر الوحيد. التغطية المحلية غير مكتملة، ولا تمثل جميع المدن أو القرى أو الأحياء أو الحارات.", "",
        "| ISO | الدولة | الكيانات | الادعاءات | الصفحة |", "|---|---|---:|---:|---|",
    ]
    entity_counts = CounterBy(data["entities"], "country_code")
    entity_iso = {r["id"]: r["country_code"] for r in data["entities"]}
    claim_counts = defaultdict(int)
    for claim in data["claims"]: claim_counts[entity_iso[claim["subject_id"]]] += 1
    for iso, (name_ar, _name_en) in COUNTRIES.items():
        md_index.append(f"| {iso} | {name_ar} | {entity_counts[iso]} | {claim_counts[iso]} | [{iso}](countries/{iso}.md) |")
        files[Path("markdown/countries") / f"{iso}.md"] = country_markdown(iso, data).encode()
        files[Path("html/countries") / f"{iso}.html"] = country_html(iso, data).encode()
    files[Path("markdown/README.md")] = ("\n".join(md_index) + "\n").encode()

    html_rows = [[iso, name_ar, entity_counts[iso], claim_counts[iso], f"countries/{iso}.html"] for iso, (name_ar, _name_en) in COUNTRIES.items()]
    body_rows = "".join(f'<tr><td>{iso}</td><td>{html.escape(name)}</td><td>{ec}</td><td>{cc}</td><td><a href="{url}">فتح</a></td></tr>' for iso, name, ec, cc, url in html_rows)
    index_main = '<h1>العروض المولّدة من Schema 2.0.0</h1><p class="notice">البيانات المنظمة هي المصدر. التغطية المحلية غير مكتملة ولا تمثل جميع المدن أو القرى أو الأحياء أو الحارات.</p><h2>الدول</h2><div class=table-wrap><table><thead><tr><th>ISO</th><th>الدولة</th><th>الكيانات</th><th>الادعاءات</th><th>الصفحة</th></tr></thead><tbody>' + body_rows + "</tbody></table></div>"
    files[Path("html/index.html")] = page_html("Schema 2.0.0 — الفهرس", index_main).encode()

    input_hashes = {str(path.relative_to(ROOT)): "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest() for path in DATASETS.values()}
    input_hashes.update({str(path.relative_to(ROOT)): "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted((ROOT / "data/sources").glob("*.json"))})
    metadata = {
        "schema_version": "2.0.0", "generator": "scripts/generate.py", "inputs": input_hashes,
        "counts": {name: len(rows) for name, rows in data.items()},
        "outputs": sorted(str(path) for path in files),
    }
    files[Path("metadata.json")] = jdump(metadata, pretty=True).encode()
    return files


class CounterBy(defaultdict):
    def __init__(self, rows, field):
        super().__init__(int)
        for row in rows: self[row[field]] += 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated output is stale")
    args = parser.parse_args()
    files = render(load())
    if args.check:
        expected = set(files)
        actual = {path.relative_to(OUT) for path in OUT.rglob("*") if path.is_file()} if OUT.exists() else set()
        stale = [str(rel) for rel, content in files.items() if not (OUT / rel).exists() or (OUT / rel).read_bytes() != content]
        extra = sorted(str(rel) for rel in actual - expected)
        if stale or extra:
            print(f"generated output is stale: changed/missing={stale}, extra={extra}", file=sys.stderr)
            return 1
        print(f"generated output is current ({len(files)} files)")
        return 0
    if OUT.exists(): shutil.rmtree(OUT)
    for rel, content in files.items():
        path = OUT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    print(f"generated {len(files)} files in Markdown, HTML, JSON, and CSV")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
