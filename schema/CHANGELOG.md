# Schema changelog

## 2.1.0 — 2026-08-17

Additive, non-breaking release implementing the **Maximum Arabic Knowledge Coverage** policy (`00_فلسفة_الموسوعة.md`). Records keep `schema_version: 2.0.0`; no migration required.

### Added

- New `verification_status` values on Entity, Relationship, and Claim: `probable` (🟡 مرجحة), `local_reported` (🟠 معلومة محلية), `unverified` (🔴 غير موثقة), `folk_narrative` (⚪ رواية شعبية). Existing values remain valid.
- Source `quality_tier` **E** for weak/local/unverified sources (local books, blogs, forums, oral testimony). Tier-E-backed claims may not carry a status above `local_reported`.
- New `source_type` values: `local_book`, `local_press`, `local_website`, `blog`, `forum`, `oral_testimony`, `map`, `heritage_book`.
- New claim `classification` values: `folk_narrative`, `local_reported`.
- `data/backlog/unverified_content/` staging area for previously-dropped unverified material pending re-evaluation.

### Unchanged guarantees

- **No fabrication** — every record, at any confidence level, must trace to a real external origin via `source_id`/`source_locator`.
- `published: true` still requires `verified`/`source_verified`; lower-confidence content is published through dedicated uncertainty-labelled surfaces, never as verified fact.
- Denominator and coverage semantics unchanged; `denominator unavailable` no longer halts collection but never inflates coverage numbers.

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
