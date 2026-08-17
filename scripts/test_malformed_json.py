#!/usr/bin/env python3
"""Independent negative test: malformed JSON must be rejected by the parser pipeline."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from migrate_schema_2 import MigrationError, read_jsonl
from model import ROOT


def main() -> int:
    malformed = '{"id":"BROKEN","schema_version":"1.0.0",}\n'
    with tempfile.TemporaryDirectory(prefix="schema-malformed-") as directory:
        path = Path(directory) / "malformed.jsonl"
        path.write_text(malformed, encoding="utf-8")
        rejected = False
        try:
            read_jsonl(path)
        except MigrationError:
            rejected = True
    if not rejected:
        raise AssertionError("malformed JSON was accepted")
    report = {
        "status": "PASS",
        "test": "malformed JSON syntax rejection",
        "input": "deliberately invalid trailing comma",
        "parser_pipeline_rejected": True,
    }
    (ROOT / "reports/schema_malformed_json_test.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("Malformed JSON negative test PASS: parser rejected invalid syntax")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
