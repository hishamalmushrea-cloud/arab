# Migration from Schema 1.0.0 to 2.0.0

Schema 2.0.0 is a breaking release. The immutable original contracts are retained in `schema/v1/`; executable current contracts are under `schema/*.schema.json` and identify `/schema/v2/`.

## Run

```bash
python3 scripts/migrate_schema_2.py
python3 scripts/test_schema_migration.py
python3 scripts/test_malformed_json.py
```

The migration is deterministic and idempotent. It changes `schema_version`, derives only mathematical mirrors, and refuses records that need an unknown fact. It never invents confidence, verification status, publication status, source quality, lexical context, a license, or an exclusion reason.

## Required reviewed decisions

Original 1.0.0 records lacking the following values require an explicit record-ID decision:

- Entity and Relationship: `confidence`, `verification_status`.
- Claim: `classification`, `confidence`, `lexical_context`, `published`, `second_source_locator`, `verification_status`.
- Source: `quality_tier`.
- Coverage: license and non-zero exclusion reasons must be documented by evidence.

The release tree had already received these reviews during accepted pilot cycles, so no synthetic defaults were used for active records.

## Deterministic derivations

- Denominator `denominator` mirrors `value`.
- Denominator `snapshot_date` mirrors `as_of`.
- Coverage `denominator` and `snapshot_date` come from referenced records.
- Coverage `missing = unmatched = denominator - matched - excluded`.
- Coverage `complete` means `matched + excluded == denominator`.

## Coverage semantic conversion

1.0.0 used `coverage_percent = matched / denominator` (four-decimal historical precision). 2.0.0 uses `coverage_percentage = (matched + excluded) / denominator` (two decimals). The migration first verifies the old formula, records both formulas/values in its audit, then calculates the new value. This is not a silent rename. An unavailable denominator continues to produce `null`, never a fabricated percentage.

## Scope and evidence

The release migrates 15,234 authoritative records plus 28 checksum-bound importer records: 15,262 total. Thirty checksum bindings are recomputed mechanically. Counts, semantic hash, failures, quarantine, and loss are recorded in `reports/schema_2_migration.json`.
