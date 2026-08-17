#!/usr/bin/env python3
"""Build a deterministic full-population review selection for small Bahrain scope."""
from __future__ import annotations

from model import ROOT, write_json
from validate_bahrain import load_data


def main() -> None:
    data = load_data()
    families = {}
    for family in ("entities", "aliases", "relationships", "claims", "sources", "denominators", "coverage"):
        ids = sorted(row["id"] for row in data[family])
        families[family] = {"population": len(ids), "sample_size": len(ids), "sample_percentage": 100.0, "record_ids": ids}
    report = {"schema_version": "2.0.0", "country_code": "BH", "snapshot_date": "2026-08-16", "selection_method": "Full review of every Bahrain production record because each family is small; sorted stable IDs.", "families": families}
    write_json(ROOT / "data/review/bahrain_review_samples.json", report)
    write_json(ROOT / "reports/bahrain_review_samples.json", report)
    print(f"Built full Bahrain review selection: {sum(v['sample_size'] for v in families.values())} records across {len(families)} families.")


if __name__ == "__main__":
    main()
