# Schema 2.0.0 Release Closeout

## Decision

**RELEASE CANDIDATE — final PASS requires the clean committed gate and GitHub Push/PR Actions.**

## Schema

- Version: **2.0.0**
- Migration: **1.0.0 → 2.0.0**
- Exact release commit: pending release commit
- Scope: schema, migration, documentation, validators, tests, fixtures, reports, and generated metadata only

## Migration

- Records migrated: **15,262** (15,234 authoritative + 28 checksum-bound importer records)
- Failed: **0**
- Quarantined by this migration: **0**
- Information lost: **0**
- Unreviewed semantic changes: **0**
- Count differences: **0** across all nine families
- Checksum bindings refreshed: **30**

## Semantic preservation

**PASS locally; `semantic_loss=false`.** Entity, Alias, Relationship, Claim, Source, Denominator, Coverage, Snapshot, and Manifest each pass. Coverage uses an explicit checked formula conversion; it is not a silent rename.

Semantic hash: `sha256:708af89b2f122f8b9adca65baf79770a08ff51407dc549abb2381f7fb4549b74`

## Tests

- Original v1 fixtures valid: PASS 9/9
- Literal backward compatibility: expected breaking result, 0/9 accepted
- Version-only conversion: 3/9 accepted
- Migration correctness: PASS 9/9
- Semantic preservation: PASS 9/9
- Invalid/default rejection: PASS 6/6
- Determinism: PASS
- Idempotence: PASS
- Malformed JSON independent negative test: PASS
- Duplicate IDs: 0
- Orphans: 0
- Cycles: 0
- Country mismatches: 0
- Source-backed Claims: 2,012/2,012

## Final gate and CI

- Final `make check`: pending clean release commit
- Final phase gate: pending clean release commit
- Generated freshness: locally PASS
- GitHub Push Action: pending
- GitHub PR Action: pending
- Working tree: pending release commit

## Remaining limitations

No semantic migration limitation is open. Remote CI and exact-commit evidence are intentionally not marked PASS before they exist. Live source freshness remains a separate review activity and is not converted into a nondeterministic build dependency.

## Bahrain

No Bahrain expansion was performed: **0 new Bahrain entities, 0 claims, 0 sources, and 0 non-country-scope denominators**. Bahrain is not authorized to start until this document records final PASS.
