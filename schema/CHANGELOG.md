# Schema changelog

## 2.0.0 — 2026-08-16

Breaking release from the original 1.0.0 contract.

### Breaking

- All executable schema IDs move from `/schema/v1/` to `/schema/v2/`; active records require `schema_version: 2.0.0`.
- Entity and Relationship require reviewed confidence and verification status.
- Claim requires classification, confidence, lexical context, publication state, second-source locator, and verification status; evidence rules are stronger.
- Source requires a reviewed quality tier.
- Denominator requires explicit denominator and snapshot-date mirrors.
- Coverage replaces `coverage_percent` with semantically different `coverage_percentage`, requires denominator/date/license/exclusion metadata, and defines completion from matched plus reviewed exclusions.
- Non-administrative entities require sourced contextual relationships and cannot use an administrative parent as a shortcut.

### Compatible additions retained

- Entity statuses: `renamed`, `merged`, `abolished`.
- Relationships: `boundary_intersects`, `associated_with`, `variety_of`, `form_of`, `attested_in`.
- Source types: `institutional_dataset`, `institutional_page`.
- Optional Source fields: `author`, `organization`.
- Optional manifest pilot/profile metadata.
- Nineteen accumulated entity types and all prior controlled vocabulary values remain accepted.

### Migration

See `schema/MIGRATION_1_TO_2.md`. Original executable 1.0.0 contracts and representative fixtures are retained for compatibility tests. No country expansion data is part of this release.

## 1.0.0 — 2026-08-15

Initial audited structured-data contract.
