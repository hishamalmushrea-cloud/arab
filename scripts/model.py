#!/usr/bin/env python3
"""Shared, dependency-free helpers for Schema v1 tooling."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
import uuid
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "1.0.0"
AS_OF = "2026-08-15"
NAMESPACE = uuid.UUID("8a8357de-0f93-5d8c-bfe7-5a0bb84bbff6")

COUNTRIES = {
    "JO": ("الأردن", "Jordan"),
    "AE": ("الإمارات", "United Arab Emirates"),
    "BH": ("البحرين", "Bahrain"),
    "DZ": ("الجزائر", "Algeria"),
    "SA": ("السعودية", "Saudi Arabia"),
    "SD": ("السودان", "Sudan"),
    "SO": ("الصومال", "Somalia"),
    "IQ": ("العراق", "Iraq"),
    "KW": ("الكويت", "Kuwait"),
    "MA": ("المغرب", "Morocco"),
    "YE": ("اليمن", "Yemen"),
    "TN": ("تونس", "Tunisia"),
    "KM": ("جزر القمر", "Comoros"),
    "DJ": ("جيبوتي", "Djibouti"),
    "SY": ("سوريا", "Syrian Arab Republic"),
    "OM": ("عُمان", "Oman"),
    "PS": ("فلسطين", "State of Palestine"),
    "QA": ("قطر", "Qatar"),
    "LB": ("لبنان", "Lebanon"),
    "LY": ("ليبيا", "Libya"),
    "EG": ("مصر", "Egypt"),
    "MR": ("موريتانيا", "Mauritania"),
}
NAME_TO_ISO = {ar: iso for iso, (ar, _en) in COUNTRIES.items()}
NAME_TO_ISO.update({"الإمارات العربية المتحدة": "AE", "المملكة العربية السعودية": "SA"})

ARABIC_MARKS = re.compile(r"[\u064b-\u065f\u0670\u06d6-\u06ed]")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def norm_name(value: str) -> str:
    """Comparison key only; never emitted as a display name."""
    value = nfc(value).strip()
    value = ARABIC_MARKS.sub("", value)
    value = value.translate(str.maketrans({
        "أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ة": "ه",
        "ؤ": "و", "ئ": "ي", "ـ": "", "’": "'", "‘": "'", "–": "-",
    }))
    value = re.sub(r"[^\w\u0600-\u06ff]+", " ", value, flags=re.UNICODE)
    return " ".join(value.casefold().split())


def stable_token(kind: str, *parts: object, length: int = 16) -> str:
    key = "|".join([kind, *(norm_name(str(p)) for p in parts)])
    return uuid.uuid5(NAMESPACE, key).hex[:length].upper()


def entity_id(iso: str, entity_type: str, name: str, parent_key: str = "") -> str:
    if entity_type == "country":
        return f"ENT-{iso}-COUNTRY"
    family = entity_type.split("_", 1)[-1].replace("_", "-").upper()[:18]
    return f"ENT-{iso}-{family}-{stable_token('entity', iso, entity_type, name, parent_key, length=12)}"


def record_id(prefix: str, *parts: object) -> str:
    return f"{prefix}-{stable_token(prefix, *parts)}"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    result = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(obj, dict):
            raise ValueError(f"{path}:{line_no}: record must be an object")
        result.append(obj)
    return result


def write_jsonl(path: Path, records: Iterable[dict[str, Any]], *, sort_key: str = "id") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(records)
    if sort_key and all(sort_key in row for row in rows):
        rows.sort(key=lambda row: str(row[sort_key]))
    text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for row in rows)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(value: str | None) -> str | None:
    if value is None:
        return None
    value = nfc(value).strip()
    return None if value in {"", "—", "-", "غير متاح", "N/A"} else value


def assert_clean_text(value: Any, location: str = "value") -> None:
    if isinstance(value, str):
        if value != nfc(value):
            raise ValueError(f"{location}: text is not Unicode NFC")
        if CONTROL_RE.search(value):
            raise ValueError(f"{location}: forbidden control character")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            assert_clean_text(item, f"{location}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            assert_clean_text(key, f"{location}.key")
            assert_clean_text(item, f"{location}.{key}")
