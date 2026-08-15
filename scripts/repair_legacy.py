#!/usr/bin/env python3
"""Idempotently repair syntactic legacy CSV defects while preserving before-images."""
from __future__ import annotations

import csv
import io
from collections import defaultdict
from pathlib import Path

from model import AS_OF, ROOT, nfc, write_jsonl

CSV_DIR = ROOT / "قاعدة_بيانات_الأماكن"
QUARANTINE = ROOT / "data" / "quarantine"


def load_files():
    files = []
    for path in sorted(CSV_DIR.glob("*.csv"), key=lambda p: p.as_posix()):
        raw = path.read_bytes()
        has_bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text, newline=""))
        if not reader.fieldnames or "id" not in reader.fieldnames:
            continue
        rows = list(reader)
        line_ending = "\r\n" if b"\r\n" in raw else "\n"
        files.append({"path": path, "fieldnames": reader.fieldnames, "rows": rows, "bom": has_bom, "line_ending": line_ending})
    return files


def main() -> int:
    files = load_files()
    occurrences = defaultdict(list)
    for file_info in files:
        for row_index, row in enumerate(file_info["rows"], 2):
            occurrences[(row.get("id") or "").strip()].append((file_info, row_index, row))

    repairs = []
    changed_paths: set[Path] = set()

    # Repair any excess fields conservatively by joining them back into the final notes column.
    for file_info in files:
        for row_index, row in enumerate(file_info["rows"], 2):
            extras = row.pop(None, None)
            if extras:
                before = dict(row)
                before["__extra_fields__"] = extras
                existing = row.get("ملاحظات") or ""
                row["ملاحظات"] = ",".join([existing, *extras]).strip(",")
                repairs.append({
                    "id": f"REPAIR-CSV-MALFORMED-{file_info['path'].stem}-{row_index}",
                    "date": AS_OF,
                    "action": "join_excess_csv_fields_into_notes",
                    "path": str(file_info["path"].relative_to(ROOT)),
                    "row": row_index,
                    "legacy_id_before": row.get("id"),
                    "legacy_id_after": row.get("id"),
                    "before": before,
                    "after": dict(row),
                    "reason": "CSV row had fields beyond the declared 18-column header; comma-delimited note was not quoted.",
                })
                changed_paths.add(file_info["path"])

    # Recompute IDs after syntactic repairs and rename every global occurrence after the first.
    occurrences = defaultdict(list)
    for file_info in files:
        for row_index, row in enumerate(file_info["rows"], 2):
            occurrences[(row.get("id") or "").strip()].append((file_info, row_index, row))

    used_ids = set(occurrences)
    for old_id in sorted(occurrences):
        items = occurrences[old_id]
        if not old_id or len(items) < 2:
            continue
        for duplicate_number, (file_info, row_index, row) in enumerate(items[1:], 2):
            suffix = duplicate_number
            new_id = f"{old_id}-LEGACY-DUP-{suffix:02d}"
            while new_id in used_ids:
                suffix += 1
                new_id = f"{old_id}-LEGACY-DUP-{suffix:02d}"
            before = dict(row)
            row["id"] = new_id
            used_ids.add(new_id)
            repairs.append({
                "id": f"REPAIR-DUPLICATE-ID-{len(repairs)+1:04d}",
                "date": AS_OF,
                "action": "rename_duplicate_legacy_id",
                "path": str(file_info["path"].relative_to(ROOT)),
                "row": row_index,
                "legacy_id_before": old_id,
                "legacy_id_after": new_id,
                "before": before,
                "after": dict(row),
                "reason": "Global legacy ID collision; the first occurrence was retained and this occurrence received a deterministic legacy suffix. Semantic duplicates are resolved separately during migration.",
            })
            changed_paths.add(file_info["path"])

    for file_info in files:
        path = file_info["path"]
        if path not in changed_paths:
            continue
        output = io.StringIO(newline="")
        writer = csv.DictWriter(output, fieldnames=file_info["fieldnames"], extrasaction="ignore", lineterminator=file_info["line_ending"])
        writer.writeheader()
        for row in file_info["rows"]:
            writer.writerow({key: nfc(row.get(key) or "") for key in file_info["fieldnames"]})
        encoded = output.getvalue().encode("utf-8")
        if file_info["bom"]:
            encoded = b"\xef\xbb\xbf" + encoded
        path.write_bytes(encoded)

    log_path = QUARANTINE / "legacy_repairs.jsonl"
    if repairs:
        write_jsonl(log_path, repairs)
    elif not log_path.exists():
        write_jsonl(log_path, [])

    malformed = sum(1 for r in repairs if r["action"] == "join_excess_csv_fields_into_notes")
    duplicate_ids = sum(1 for r in repairs if r["action"] == "rename_duplicate_legacy_id")
    print(f"legacy repair: malformed_rows={malformed}, renamed_duplicate_occurrences={duplicate_ids}, files_changed={len(changed_paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
