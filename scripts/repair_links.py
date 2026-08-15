#!/usr/bin/env python3
"""Repair the 25 known broken local links, logging each before/after edit."""
from __future__ import annotations

from pathlib import Path

from model import AS_OF, ROOT, write_jsonl


def main() -> int:
    replacements: list[tuple[Path, str, str, str]] = []

    capitals = ROOT / "العواصم" / "README.md"
    if capitals.exists():
        text = capitals.read_text(encoding="utf-8")
        for line in text.splitlines():
            marker = "](العواصم/"
            if marker in line:
                old_target = line.split(marker, 1)[1].split(")", 1)[0]
                replacements.append((capitals, f"](العواصم/{old_target})", f"]({old_target})", "remove duplicated directory prefix from link inside العواصم/README.md"))

    replacements.extend([
        (
            ROOT / "الدول/سوريا/المناطق/دمشق/README.md",
            "](../../../العواصم/)",
            "](../../../../العواصم/)",
            "add the missing parent traversal to the capitals directory",
        ),
        (
            ROOT / "الدول/فلسطين/المحافظات/README.md",
            "](طوباس/طوباس.md)",
            "](طوباس_والأغوار_الشمالية/طوباس_والأغوار_الشمالية.md)",
            "use the actual Tubas and Northern Valleys directory and file name",
        ),
        (
            ROOT / "الدول/مصر/المحافظات/README.md",
            "](../../العواصم/القاهرة/القاهرة.md)",
            "](../../../العواصم/القاهرة/القاهرة.md)",
            "add the missing parent traversal to the Cairo capital file",
        ),
    ])

    grouped: dict[Path, list[tuple[str, str, str]]] = {}
    for path, old, new, reason in replacements:
        grouped.setdefault(path, []).append((old, new, reason))

    log = []
    for path, edits in grouped.items():
        text = path.read_text(encoding="utf-8")
        changed = False
        for old, new, reason in edits:
            if old not in text:
                continue
            line_no = text[: text.index(old)].count("\n") + 1
            text = text.replace(old, new, 1)
            changed = True
            log.append({
                "id": f"REPAIR-LINK-{len(log)+1:03d}",
                "date": AS_OF,
                "action": "repair_broken_local_markdown_link",
                "path": str(path.relative_to(ROOT)),
                "line_before": line_no,
                "before": old,
                "after": new,
                "reason": reason,
            })
        if changed:
            path.write_text(text, encoding="utf-8")

    log_path = ROOT / "data/quarantine/link_repairs.jsonl"
    if log:
        write_jsonl(log_path, log)
    elif not log_path.exists():
        write_jsonl(log_path, [])
    print(f"link repair: repaired={len(log)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
