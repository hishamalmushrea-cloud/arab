#!/usr/bin/env python3
"""Build the complete, offline Android database from authoritative Schema 2.0.0 data.

The database stores both query-friendly columns and each canonical record as compact
JSON so the app never loses fields from the source schema. Country manifests and
cultural-domain status documents are included as project documents. The complete
user-facing legacy encyclopedia (countries, capitals, neighbourhoods, comparisons,
cultural map, references, and place CSVs) is bundled verbatim in a separate labelled
library. Review samples, quarantine rows, and generated duplicate views remain
excluded because they are workflow artefacts rather than publishable content.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from model import COUNTRIES, ROOT, norm_name, read_jsonl

SCHEMA_VERSION = "2.0.0"
DATABASE_VERSION = 2
DATASET_VERSION = "2.0.0-2026.08.17-library.1"
DEFAULT_OUTPUT = ROOT / "android/app/src/main/assets/database/arab_atlas.db"

# User-facing encyclopedic/reference material. These files are bundled verbatim in
# a clearly labelled library; they remain distinct from authoritative Schema 2.0.0.
LIBRARY_ROOTS = [
    ROOT / "الدول",
    ROOT / "العواصم",
    ROOT / "الحارات_والأحياء",
    ROOT / "الخريطة_الثقافية",
    ROOT / "المقارنات",
    ROOT / "قاعدة_بيانات_الأماكن",
    ROOT / "المصادر_والمراجع",
]
LIBRARY_EXTENSIONS = {".md", ".csv"}

NEIGHBORHOOD_COUNTRIES = {
    "القاهرة": "EG", "القرى_الفلسطينية_المدمرة": "PS", "بغداد": "IQ",
    "تونس_العتيقة": "TN", "جدة_التاريخية": "SA", "دمشق_القديمة": "SY",
    "صنعاء_القديمة": "YE", "نابلس_القديمة": "PS",
}

CAPITAL_COUNTRIES = {
    "أبوظبي": "AE", "الجزائر": "DZ", "الخرطوم": "SD", "الدوحة": "QA",
    "الرباط": "MA", "الرياض": "SA", "القاهرة": "EG", "القدس": "PS",
    "المنامة": "BH", "بغداد": "IQ", "بيروت": "LB", "تونس": "TN",
    "جيبوتي": "DJ", "دمشق": "SY", "صنعاء": "YE", "طرابلس": "LY",
    "عمّان": "JO", "مدينة_الكويت": "KW", "مسقط": "OM", "مقديشو": "SO",
    "موروني": "KM", "نواكشوط": "MR",
}

JSONL_INPUTS = {
    "entities": ROOT / "data/entities/entities.jsonl",
    "aliases": ROOT / "data/aliases/aliases.jsonl",
    "relationships": ROOT / "data/relationships/relationships.jsonl",
    "claims": ROOT / "data/claims/claims.jsonl",
    "snapshots": ROOT / "data/snapshots/snapshots.jsonl",
    "denominators": ROOT / "data/coverage/denominators.jsonl",
    "coverage": ROOT / "data/coverage/coverage.jsonl",
}


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return compact_json(value)
    return str(value)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_files() -> list[Path]:
    return sorted((ROOT / "data/sources").glob("*.json"))


def manifest_files() -> list[Path]:
    return sorted((ROOT / "manifests").glob("*.yml"))


def cultural_files() -> list[Path]:
    return sorted((ROOT / "data/cultural").glob("*.json"))


def library_files() -> list[Path]:
    return sorted(
        path for root in LIBRARY_ROOTS for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in LIBRARY_EXTENSIONS
    )


def library_digest(paths: list[Path] | None = None) -> str:
    digest = hashlib.sha256()
    for path in paths or library_files():
        digest.update(str(path.relative_to(ROOT)).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def library_country_and_category(path: Path) -> tuple[str | None, str]:
    collection = path.relative_to(ROOT).parts[0]
    relative_parts = path.relative_to(ROOT / collection).parts
    folder_countries = {name_ar.replace(" ", "_"): iso for iso, (name_ar, _name_en) in COUNTRIES.items()}
    country_code: str | None = None
    remaining = list(relative_parts)
    if collection == "الدول" and remaining:
        country_code = folder_countries.get(remaining.pop(0))
    elif collection == "العواصم" and remaining:
        country_code = CAPITAL_COUNTRIES.get(remaining[0])
    elif collection == "الحارات_والأحياء" and remaining:
        country_code = NEIGHBORHOOD_COUNTRIES.get(remaining[0])
    elif collection == "قاعدة_بيانات_الأماكن" and path.suffix.lower() == ".csv":
        country_code = folder_countries.get(path.stem)

    if collection == "الدول" and remaining:
        first = remaining[0]
        category = Path(first).stem if len(remaining) == 1 else first
    elif collection == "قاعدة_بيانات_الأماكن":
        category = "جداول الأماكن" if path.suffix.lower() == ".csv" else "دليل البيانات"
    elif len(relative_parts) > 1:
        category = relative_parts[0]
    else:
        category = path.stem
    category = category.replace("_", " ")
    if category == "00 الفهرس":
        category = "الفهرس"
    return country_code, category


def library_title(path: Path, content: str) -> str:
    if path.suffix.lower() == ".md":
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip().replace("`", "")
    return path.stem.replace("_", " ")


def all_inputs() -> list[Path]:
    return [*JSONL_INPUTS.values(), *source_files(), *manifest_files(), *cultural_files()]


def load_data() -> dict[str, list[dict[str, Any]]]:
    data = {name: read_jsonl(path) for name, path in JSONL_INPUTS.items()}
    data["sources"] = [json.loads(path.read_text(encoding="utf-8")) for path in source_files()]
    data["sources"].sort(key=lambda row: row["id"])
    return data


SCHEMA_SQL = """
PRAGMA foreign_keys = OFF;
PRAGMA page_size = 4096;
PRAGMA journal_mode = DELETE;

CREATE TABLE metadata (
    key TEXT PRIMARY KEY NOT NULL,
    value TEXT NOT NULL
) WITHOUT ROWID;

CREATE TABLE countries (
    code TEXT PRIMARY KEY NOT NULL,
    name_ar TEXT NOT NULL,
    name_en TEXT NOT NULL,
    entity_count INTEGER NOT NULL,
    alias_count INTEGER NOT NULL,
    relationship_count INTEGER NOT NULL,
    claim_count INTEGER NOT NULL,
    source_count INTEGER NOT NULL,
    coverage_count INTEGER NOT NULL,
    complete_layers INTEGER NOT NULL
) WITHOUT ROWID;

CREATE TABLE entities (
    id TEXT PRIMARY KEY NOT NULL,
    country_code TEXT NOT NULL,
    canonical_name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    canonical_name_language TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    status TEXT NOT NULL,
    confidence TEXT,
    verification_status TEXT,
    canonical_source_id TEXT NOT NULL,
    source_locator TEXT NOT NULL,
    coordinates_json TEXT,
    notes TEXT,
    valid_from TEXT,
    valid_to TEXT,
    raw_json TEXT NOT NULL
) WITHOUT ROWID;
CREATE INDEX entities_country_idx ON entities(country_code, entity_type, canonical_name);
CREATE INDEX entities_name_idx ON entities(normalized_name);
CREATE INDEX entities_source_idx ON entities(canonical_source_id);

CREATE TABLE aliases (
    id TEXT PRIMARY KEY NOT NULL,
    entity_id TEXT NOT NULL,
    name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    language TEXT NOT NULL,
    kind TEXT NOT NULL,
    status TEXT NOT NULL,
    source_id TEXT NOT NULL,
    source_locator TEXT,
    valid_from TEXT,
    valid_to TEXT,
    raw_json TEXT NOT NULL
) WITHOUT ROWID;
CREATE INDEX aliases_entity_idx ON aliases(entity_id);
CREATE INDEX aliases_name_idx ON aliases(normalized_name);
CREATE INDEX aliases_source_idx ON aliases(source_id);

CREATE TABLE relationships (
    id TEXT PRIMARY KEY NOT NULL,
    child_id TEXT NOT NULL,
    parent_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    status TEXT NOT NULL,
    confidence TEXT,
    verification_status TEXT,
    source_id TEXT NOT NULL,
    source_locator TEXT NOT NULL,
    notes TEXT,
    valid_from TEXT,
    valid_to TEXT,
    raw_json TEXT NOT NULL
) WITHOUT ROWID;
CREATE INDEX relationships_child_idx ON relationships(child_id);
CREATE INDEX relationships_parent_idx ON relationships(parent_id);
CREATE INDEX relationships_source_idx ON relationships(source_id);

CREATE TABLE claims (
    id TEXT PRIMARY KEY NOT NULL,
    subject_id TEXT NOT NULL,
    predicate TEXT NOT NULL,
    value_display TEXT NOT NULL,
    value_type TEXT NOT NULL,
    unit TEXT,
    classification TEXT,
    confidence TEXT,
    status TEXT NOT NULL,
    verification_status TEXT,
    published INTEGER NOT NULL,
    sensitivity TEXT,
    source_id TEXT NOT NULL,
    source_locator TEXT NOT NULL,
    observed_at TEXT,
    valid_from TEXT,
    valid_to TEXT,
    notes TEXT,
    raw_json TEXT NOT NULL
) WITHOUT ROWID;
CREATE INDEX claims_subject_idx ON claims(subject_id, predicate);
CREATE INDEX claims_source_idx ON claims(source_id);

CREATE TABLE sources (
    id TEXT PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    publisher TEXT NOT NULL,
    organization TEXT,
    author TEXT,
    source_type TEXT NOT NULL,
    url TEXT NOT NULL,
    archive_url TEXT,
    publication_date TEXT,
    retrieved_at TEXT NOT NULL,
    license TEXT NOT NULL,
    language TEXT NOT NULL,
    quality_tier TEXT NOT NULL,
    country_codes_json TEXT NOT NULL,
    locator TEXT NOT NULL,
    notes TEXT,
    raw_json TEXT NOT NULL
) WITHOUT ROWID;
CREATE INDEX sources_tier_idx ON sources(quality_tier, title);

CREATE TABLE country_sources (
    country_code TEXT NOT NULL,
    source_id TEXT NOT NULL,
    PRIMARY KEY (country_code, source_id)
) WITHOUT ROWID;
CREATE INDEX country_sources_source_idx ON country_sources(source_id);

CREATE TABLE snapshots (
    id TEXT PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    captured_at TEXT NOT NULL,
    scope TEXT NOT NULL,
    method TEXT NOT NULL,
    source_id TEXT NOT NULL,
    checksum TEXT,
    notes TEXT,
    raw_json TEXT NOT NULL
) WITHOUT ROWID;

CREATE TABLE denominators (
    id TEXT PRIMARY KEY NOT NULL,
    country_code TEXT NOT NULL,
    layer TEXT NOT NULL,
    definition TEXT NOT NULL,
    value INTEGER,
    status TEXT NOT NULL,
    snapshot_date TEXT,
    source_id TEXT NOT NULL,
    source_locator TEXT NOT NULL,
    license TEXT NOT NULL,
    missing_reason TEXT,
    notes TEXT,
    raw_json TEXT NOT NULL
) WITHOUT ROWID;
CREATE INDEX denominators_country_idx ON denominators(country_code, layer);

CREATE TABLE coverage (
    id TEXT PRIMARY KEY NOT NULL,
    country_code TEXT NOT NULL,
    layer TEXT NOT NULL,
    denominator_id TEXT NOT NULL,
    denominator INTEGER,
    matched INTEGER NOT NULL,
    unmatched INTEGER NOT NULL,
    excluded INTEGER NOT NULL,
    missing INTEGER,
    coverage_percentage REAL,
    complete INTEGER NOT NULL,
    snapshot_date TEXT,
    snapshot_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    license TEXT NOT NULL,
    missing_reason TEXT,
    notes TEXT,
    raw_json TEXT NOT NULL
) WITHOUT ROWID;
CREATE INDEX coverage_country_idx ON coverage(country_code, complete, layer);

CREATE TABLE search_index (
    row_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT NOT NULL,
    country_code TEXT NOT NULL,
    display_name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    language TEXT NOT NULL,
    is_canonical INTEGER NOT NULL
);
CREATE INDEX search_normalized_idx ON search_index(normalized_name, country_code);
CREATE INDEX search_entity_idx ON search_index(entity_id);

CREATE TABLE project_documents (
    id TEXT PRIMARY KEY NOT NULL,
    country_code TEXT,
    kind TEXT NOT NULL,
    title TEXT NOT NULL,
    content_type TEXT NOT NULL,
    content TEXT NOT NULL
) WITHOUT ROWID;
CREATE INDEX project_documents_country_idx ON project_documents(country_code, kind);

CREATE TABLE library_documents (
    id TEXT PRIMARY KEY NOT NULL,
    collection TEXT NOT NULL,
    country_code TEXT,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    relative_path TEXT NOT NULL UNIQUE,
    parent_path TEXT NOT NULL,
    file_type TEXT NOT NULL,
    content TEXT NOT NULL,
    normalized_title TEXT NOT NULL,
    byte_size INTEGER NOT NULL,
    content_sha256 TEXT NOT NULL
) WITHOUT ROWID;
CREATE INDEX library_collection_idx ON library_documents(collection, country_code, category, title);
CREATE INDEX library_country_idx ON library_documents(country_code, category, title);
CREATE INDEX library_title_idx ON library_documents(normalized_title);
"""


def insert_many(connection: sqlite3.Connection, sql: str, rows: Iterable[tuple[Any, ...]]) -> None:
    connection.executemany(sql, rows)


def build_database(output: Path) -> None:
    data = load_data()
    entities = data["entities"]
    aliases = data["aliases"]
    relationships = data["relationships"]
    claims = data["claims"]
    sources = data["sources"]
    snapshots = data["snapshots"]
    denominators = data["denominators"]
    coverage = data["coverage"]
    library_paths = library_files()

    output.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix="arab_atlas_", suffix=".db", dir=output.parent)
    os.close(handle)
    temporary = Path(temporary_name)
    temporary.unlink()

    try:
        connection = sqlite3.connect(temporary)
        connection.executescript(SCHEMA_SQL)
        connection.execute(f"PRAGMA user_version = {DATABASE_VERSION}")
        connection.execute("BEGIN")

        insert_many(connection, """INSERT INTO entities VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            (
                row["id"], row["country_code"], row["canonical_name"], norm_name(row["canonical_name"]),
                row["canonical_name_language"], row["entity_type"], row["status"], row.get("confidence"),
                row.get("verification_status"), row["canonical_source_id"], row["source_locator"],
                text(row.get("coordinates")), row.get("notes"), row.get("valid_from"), row.get("valid_to"),
                compact_json(row),
            ) for row in entities
        ))
        insert_many(connection, """INSERT INTO aliases VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", (
            (
                row["id"], row["entity_id"], row["name"], norm_name(row["name"]), row["language"],
                row["kind"], row["status"], row["source_id"], row.get("source_locator"),
                row.get("valid_from"), row.get("valid_to"), compact_json(row),
            ) for row in aliases
        ))
        insert_many(connection, """INSERT INTO relationships VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            (
                row["id"], row["child_id"], row["parent_id"], row["relationship_type"], row["status"],
                row.get("confidence"), row.get("verification_status"), row["source_id"],
                row["source_locator"], row.get("notes"), row.get("valid_from"), row.get("valid_to"),
                compact_json(row),
            ) for row in relationships
        ))
        insert_many(connection, """INSERT INTO claims VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            (
                row["id"], row["subject_id"], row["predicate"], text(row["value"].get("data")) or "—",
                row["value"]["type"], row.get("unit"), row.get("classification"), row.get("confidence"),
                row["status"], row.get("verification_status"), int(bool(row.get("published"))),
                row.get("sensitivity"), row["source_id"], row["source_locator"], row.get("observed_at"),
                row.get("valid_from"), row.get("valid_to"), row.get("notes"), compact_json(row),
            ) for row in claims
        ))
        insert_many(connection, """INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            (
                row["id"], row["title"], row["publisher"], row.get("organization"), row.get("author"),
                row["source_type"], row["url"], row.get("archive_url"), row.get("publication_date"),
                row["retrieved_at"], row["license"], row["language"], row["quality_tier"],
                compact_json(row["country_codes"]), row["locator"], row.get("notes"), compact_json(row),
            ) for row in sources
        ))
        insert_many(connection, """INSERT INTO snapshots VALUES (?,?,?,?,?,?,?,?,?)""", (
            (
                row["id"], row["title"], row["captured_at"], row["scope"], row["method"], row["source_id"],
                row.get("checksum"), row.get("notes"), compact_json(row),
            ) for row in snapshots
        ))
        insert_many(connection, """INSERT INTO denominators VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            (
                row["id"], row["country_code"], row["layer"], row["definition"], row.get("value"),
                row["status"], row.get("snapshot_date"), row["source_id"], row["source_locator"],
                row["license"], row.get("missing_reason"), row.get("notes"), compact_json(row),
            ) for row in denominators
        ))
        insert_many(connection, """INSERT INTO coverage VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            (
                row["id"], row["country_code"], row["layer"], row["denominator_id"], row.get("denominator"),
                row["matched"], row["unmatched"], row["excluded"], row.get("missing"),
                row.get("coverage_percentage"), int(bool(row["complete"])), row.get("snapshot_date"),
                row["snapshot_id"], row["source_id"], row["license"], row.get("missing_reason"),
                row.get("notes"), compact_json(row),
            ) for row in coverage
        ))

        entity_country = {row["id"]: row["country_code"] for row in entities}
        used_sources: dict[str, set[str]] = defaultdict(set)
        entity_counts: dict[str, int] = defaultdict(int)
        alias_counts: dict[str, int] = defaultdict(int)
        relationship_counts: dict[str, int] = defaultdict(int)
        claim_counts: dict[str, int] = defaultdict(int)
        coverage_counts: dict[str, int] = defaultdict(int)
        complete_counts: dict[str, int] = defaultdict(int)

        search_rows: list[tuple[Any, ...]] = []
        for row in entities:
            iso = row["country_code"]
            entity_counts[iso] += 1
            used_sources[iso].add(row["canonical_source_id"])
            search_rows.append((row["id"], iso, row["canonical_name"], norm_name(row["canonical_name"]), row["canonical_name_language"], 1))
        for row in aliases:
            iso = entity_country[row["entity_id"]]
            alias_counts[iso] += 1
            used_sources[iso].add(row["source_id"])
            search_rows.append((row["entity_id"], iso, row["name"], norm_name(row["name"]), row["language"], 0))
        for row in relationships:
            iso = entity_country[row["child_id"]]
            relationship_counts[iso] += 1
            used_sources[iso].add(row["source_id"])
        for row in claims:
            iso = entity_country[row["subject_id"]]
            claim_counts[iso] += 1
            used_sources[iso].add(row["source_id"])
        for row in coverage:
            iso = row["country_code"]
            coverage_counts[iso] += 1
            complete_counts[iso] += int(bool(row["complete"]))
            used_sources[iso].add(row["source_id"])

        insert_many(connection, """INSERT INTO search_index(entity_id,country_code,display_name,normalized_name,language,is_canonical) VALUES (?,?,?,?,?,?)""", search_rows)
        insert_many(connection, "INSERT INTO country_sources VALUES (?,?)", (
            (iso, source_id) for iso in COUNTRIES for source_id in sorted(used_sources[iso])
        ))
        insert_many(connection, """INSERT INTO countries VALUES (?,?,?,?,?,?,?,?,?,?)""", (
            (
                iso, names[0], names[1], entity_counts[iso], alias_counts[iso], relationship_counts[iso],
                claim_counts[iso], len(used_sources[iso]), coverage_counts[iso], complete_counts[iso],
            ) for iso, names in COUNTRIES.items()
        ))

        for path in manifest_files():
            iso = path.stem
            connection.execute(
                "INSERT INTO project_documents VALUES (?,?,?,?,?,?)",
                (f"manifest-{iso}", iso, "manifest", f"بيان بيانات {COUNTRIES[iso][0]}", "text/yaml", path.read_text(encoding="utf-8")),
            )
        for path in cultural_files():
            document = json.loads(path.read_text(encoding="utf-8"))
            iso = document["country_code"]
            connection.execute(
                "INSERT INTO project_documents VALUES (?,?,?,?,?,?)",
                (f"cultural-{iso}", iso, "cultural_status", f"حالة المجالات الثقافية — {COUNTRIES[iso][0]}", "application/json", compact_json(document)),
            )

        library_rows = []
        for path in library_paths:
            raw = path.read_bytes()
            content = raw.decode("utf-8")
            relative_path = str(path.relative_to(ROOT))
            country_code, category = library_country_and_category(path)
            title = library_title(path, content)
            document_id = "LIB-" + hashlib.sha256(relative_path.encode("utf-8")).hexdigest()[:20].upper()
            library_rows.append((
                document_id,
                path.relative_to(ROOT).parts[0],
                country_code,
                category,
                title,
                relative_path,
                str(path.parent.relative_to(ROOT)),
                "markdown" if path.suffix.lower() == ".md" else "csv",
                content,
                norm_name(title + " " + relative_path),
                len(raw),
                hashlib.sha256(raw).hexdigest(),
            ))
        insert_many(connection, "INSERT INTO library_documents VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", library_rows)

        counts = {
            "countries": len(COUNTRIES), "entities": len(entities), "aliases": len(aliases),
            "relationships": len(relationships), "claims": len(claims), "sources": len(sources),
            "snapshots": len(snapshots), "denominators": len(denominators), "coverage": len(coverage),
            "search_index": len(search_rows),
            "country_sources": sum(len(values) for values in used_sources.values()),
            "project_documents": len(manifest_files()) + len(cultural_files()),
            "library_documents": len(library_rows),
        }
        metadata = {
            "app_database_version": str(DATABASE_VERSION),
            "dataset_version": DATASET_VERSION,
            "schema_version": SCHEMA_VERSION,
            "as_of": "2026-08-17",
            "notice_ar": "التغطية المحلية غير مكتملة ولا تمثل جميع المدن أو القرى أو الأحياء أو الحارات.",
            "library_notice_ar": "المكتبة الموسوعية مواد مرجعية محفوظة من ملفات المشروع، وليست كلها بيانات سلطوية مقبولة في Schema 2.0.0.",
            "library_bytes": str(sum(path.stat().st_size for path in library_paths)),
            "library_collections": str(len(LIBRARY_ROOTS)),
            "input.library_digest": library_digest(library_paths),
            **{f"count.{name}": str(count) for name, count in counts.items()},
            **{f"input.{path.relative_to(ROOT)}": sha256(path) for path in all_inputs()}, 
        }
        insert_many(connection, "INSERT INTO metadata VALUES (?,?)", sorted(metadata.items()))
        connection.commit()

        failures = connection.execute("PRAGMA foreign_key_check").fetchall()
        if failures:
            raise RuntimeError(f"database foreign-key failures: {failures[:5]}")
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"database integrity check failed: {integrity}")
        connection.execute("VACUUM")
        connection.close()
        os.replace(temporary, output)
        print(f"built Android database: {output.relative_to(ROOT)} ({output.stat().st_size:,} bytes, {sum(counts.values()):,} indexed records)")
    finally:
        if temporary.exists():
            temporary.unlink()


def check_database(output: Path) -> int:
    if not output.exists():
        print(f"Android database is missing: {output}")
        return 1
    connection = sqlite3.connect(f"file:{output}?mode=ro", uri=True)
    errors: list[str] = []
    integrity = connection.execute("PRAGMA quick_check").fetchone()[0]
    if integrity != "ok":
        errors.append(f"quick_check={integrity}")
    user_version = connection.execute("PRAGMA user_version").fetchone()[0]
    if user_version != DATABASE_VERSION:
        errors.append(f"user_version={user_version}, expected {DATABASE_VERSION}")
    metadata = dict(connection.execute("SELECT key,value FROM metadata"))
    for key, expected in {
        "schema_version": SCHEMA_VERSION,
        "dataset_version": DATASET_VERSION,
        "app_database_version": str(DATABASE_VERSION),
    }.items():
        if metadata.get(key) != expected:
            errors.append(f"metadata {key}={metadata.get(key)!r}, expected {expected!r}")
    for path in all_inputs():
        key = f"input.{path.relative_to(ROOT)}"
        actual = sha256(path)
        if metadata.get(key) != actual:
            errors.append(f"stale input checksum: {path.relative_to(ROOT)}")
    current_library_files = library_files()
    if metadata.get("input.library_digest") != library_digest(current_library_files):
        errors.append("stale encyclopedic library digest")
    if metadata.get("library_bytes") != str(sum(path.stat().st_size for path in current_library_files)):
        errors.append("encyclopedic library byte count mismatch")
    for table in ["countries", "entities", "aliases", "relationships", "claims", "sources", "country_sources", "snapshots", "denominators", "coverage", "search_index", "project_documents", "library_documents"]:
        actual = connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        expected = metadata.get(f"count.{table}")
        if expected != str(actual):
            errors.append(f"count mismatch for {table}: metadata={expected}, actual={actual}")
    orphan_checks = {
        "alias entities": "SELECT count(*) FROM aliases a LEFT JOIN entities e ON e.id=a.entity_id WHERE e.id IS NULL",
        "claim subjects": "SELECT count(*) FROM claims c LEFT JOIN entities e ON e.id=c.subject_id WHERE e.id IS NULL",
        "relationship children": "SELECT count(*) FROM relationships r LEFT JOIN entities e ON e.id=r.child_id WHERE e.id IS NULL",
        "relationship parents": "SELECT count(*) FROM relationships r LEFT JOIN entities e ON e.id=r.parent_id WHERE e.id IS NULL",
        "entity sources": "SELECT count(*) FROM entities e LEFT JOIN sources s ON s.id=e.canonical_source_id WHERE s.id IS NULL",
    }
    for label, sql in orphan_checks.items():
        count = connection.execute(sql).fetchone()[0]
        if count:
            errors.append(f"{label}: {count} orphan records")
    library_hash_failures = 0
    for relative_path, content, byte_size, expected_hash in connection.execute(
        "SELECT relative_path,content,byte_size,content_sha256 FROM library_documents"
    ):
        encoded = content.encode("utf-8")
        if len(encoded) != byte_size or hashlib.sha256(encoded).hexdigest() != expected_hash:
            library_hash_failures += 1
    if library_hash_failures:
        errors.append(f"encyclopedic library content failures: {library_hash_failures}")
    connection.close()
    if errors:
        print("Android database check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Android database is current and valid ({output.stat().st_size:,} bytes)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="validate the committed database and source checksums")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if args.check:
        return check_database(output)
    build_database(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
