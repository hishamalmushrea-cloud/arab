# Schema Migration Review — 1.0.0 → 2.0.0

## Decision

**Recommended Version: RELEASE 2.0.0.** The original contracts at commit `2040441825abe4b4db96d4990b00007d1db76061` are retained in `schema/v1/`. Literal backward compatibility is 0/9 record families; only Alias, Snapshot, and Manifest accept a version-only conversion (3/9). Required semantic facts and the Coverage meaning cannot be hidden in a minor release.

## Change inventory and classification

| Schema/file | Field/rule | Old | New | Required | Old-data impact | Semantics/type/name/relations | Classification | Migration |
|---|---|---|---|---|---|---|---|---|
| all schemas | `$id`, `schema_version` | `/v1/`, `1.0.0` | `/v2/`, `2.0.0` | required | literal v1 rejected | version dispatch | BREAKING | migrate only after family conversion succeeds |
| Entity | `confidence` | absent | high/medium/low | required | unknowable from shape | new evidence meaning | BREAKING | explicit record review |
| Entity | `verification_status` | absent | controlled status | required | unknowable from shape | new review meaning | BREAKING | explicit record review |
| Relationship | `confidence`, `verification_status` | absent | controlled values | required | unknowable from shape | evidence/review meaning | BREAKING | explicit review |
| relationship validator | contextual topology | weak/no equivalent | non-admin entity needs sourced context; wrong admin parent rejected | required rule | some old graphs rejected | changes relation validity | BREAKING | add evidenced context or reject |
| Claim | `classification` | absent | controlled nullable classification | required | domain classification may be unknown | new semantics | BREAKING | explicit review; null only when reviewed/applicable |
| Claim | `confidence` | absent | controlled level | required | unknown | new evidence meaning | BREAKING | explicit review |
| Claim | `lexical_context` | absent | object/null | required | linguistic context cannot be inferred | new meaning/type | BREAKING | documented review or reject |
| Claim | `published` | absent | boolean | required | status does not uniquely imply publication | new workflow meaning/type | BREAKING | explicit review |
| Claim | `second_source_locator` | absent | string/null | required | source ID does not imply locator | stronger provenance | BREAKING | documented locator or reviewed null |
| Claim | `verification_status` | absent | controlled status | required | unknown | new review meaning | BREAKING | explicit review |
| Claim validator | evidence rules | weaker | paired locators, two sources for sensitive claims, required classifications/lexical dates | rule | weak old claims rejected | stronger semantics | BREAKING | supply evidence or reject |
| Source | `quality_tier` | absent | A/B/C/D | required | rubric decision unknown | new quality semantics | BREAKING | explicit quality review |
| Denominator | `denominator` | value only | mirror of `value` | required | old record fails literally | same meaning/type | MIGRATABLE | deterministic checked copy |
| Denominator | `snapshot_date` | `as_of` only | mirror of `as_of` | required | old record fails literally | same meaning/type | MIGRATABLE | deterministic checked copy |
| Coverage | field/formula | `coverage_percent = matched/denominator` | `coverage_percentage = (matched+excluded)/denominator` | required | name and value may differ | name + semantic change | BREAKING | verify v1 formula, audit old value, calculate v2 |
| Coverage | denominator/date | only referenced | explicit mirrors | required | old record fails | same meaning | MIGRATABLE | checked referenced copies |
| Coverage | `license` | absent | string/null plus non-empty validator rule | required | cannot be invented | new provenance meaning | BREAKING | documented source license or reject |
| Coverage | `exclusion_reasons` | absent | counts sum to excluded | required | nonzero exclusions unknown | new meaning | BREAKING | `[]` only for zero; otherwise explicit review |
| Coverage validator | missing/unmatched/complete | matched-oriented | based on matched + excluded; over-count rejected | rule | values may change | arithmetic semantics | BREAKING | checked recalculation |
| Alias | structure | baseline | unchanged except version | — | no semantic change | none | MIGRATABLE | version normalization |
| Snapshot | structure | baseline | unchanged except version | — | no semantic change | none | MIGRATABLE | version normalization |
| Manifest | required set | baseline | unchanged required set | — | old semantics retained | optional additions only | ADDITIVE | version normalization |
| Entity vocab | statuses/types | baseline set | 3 statuses + 19 accumulated types | optional values | old values retained | enum expansion | ADDITIVE | none |
| Relationship vocab | types | baseline set | 5 accumulated relation types | optional values | old values retained | enum expansion | ADDITIVE | none |
| Source | `author`, `organization`; types | absent/baseline enum | optional fields; 2 enum values | optional | old records valid structurally | additive | ADDITIVE | none |
| Manifest | pilot/profile metadata | absent | optional properties | optional | old required set retained | additive | ADDITIVE | none |

No controlled vocabulary value was removed.

## Migration matrix

| Schema | Old → New compatibility | Migration result |
|---|---|---|
| Entity | breaking required evidence | reviewed values preserved; PASS |
| Alias | version-only semantic compatibility | PASS |
| Relationship | breaking required evidence/topology | reviewed evidence and links preserved; PASS |
| Claim | breaking required evidence/workflow | reviewed values preserved; PASS |
| Source | breaking quality review | reviewed tier preserved; PASS |
| Denominator | deterministic mirrors | PASS |
| Coverage | breaking name/formula/provenance | explicit audited conversion; PASS |
| Snapshot | version-only semantic compatibility | PASS |
| Manifest | optional additions; version change | PASS |

## Executable results

- Authoritative records: **15,234**; checksum-bound importer records: **28**; total: **15,262**.
- Failed: **0**; newly quarantined: **0**; information lost: **0**; unreviewed semantic changes: **0**.
- Counts before/after are identical: Entity 4,741; Alias 3,116; Relationship 5,130; Claim 2,012; Source 90; Denominator 56; Coverage 56; Snapshot 11; Manifest 22.
- Literal old acceptance: **0/9**. Version-only acceptance: **3/9**. Migrated acceptance: **9/9**.
- Invalid/default rejection: **6/6**. Determinism: **PASS**. Idempotence: **PASS**.
- Semantic preservation: **PASS** for all nine families; `semantic_loss=false`.
- Coverage is PASS only through the explicit formula audit; no silent rename is permitted.
- Semantic hash: `sha256:708af89b2f122f8b9adca65baf79770a08ff51407dc549abb2381f7fb4549b74`.

Machine evidence: `reports/schema_2_migration.json`, `reports/schema_backward_compatibility.json`, and `reports/schema_malformed_json_test.json`.
