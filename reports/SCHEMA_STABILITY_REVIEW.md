# Schema Stability Review — final release disposition

**Date:** 2026-08-16  
**Baseline:** Schema 1.0.0 at `2040441825abe4b4db96d4990b00007d1db76061`  
**Decision:** **RELEASE 2.0.0**

The earlier provisional 1.1.0 recommendation is superseded by the executable migration review. Comparison against the immutable original schemas proved literal compatibility of 0/9 families and version-only compatibility of only 3/9. Required evidence fields and the changed Coverage formula are breaking semantics, not additive documentation.

## Stability result

The conceptual Entity/Alias/Relationship/Claim/Source/Denominator/Coverage/Snapshot/Manifest core remains stable. Schema 2.0.0 names the accumulated mature contract accurately; it does not redesign identifiers, storage, or the core model.

- 15,262 records migrate with zero count difference.
- No IDs, sources, claims, or relationships are dropped.
- Semantic preservation passes for all nine families.
- Coverage's changed formula is explicitly audited rather than silently renamed.
- Migration is deterministic and idempotent; missing semantic facts are rejected rather than defaulted.
- All original controlled vocabulary values remain accepted; accumulated enum and optional-manifest changes are additive.

The authoritative decision and complete field matrix are in `reports/SCHEMA_MIGRATION_REVIEW.md`. Machine evidence is in `reports/schema_2_migration.json` and `reports/schema_backward_compatibility.json`.

## Remaining evolution policy

A future optional field or enum expansion may be minor only when old records keep the same meaning and remain readable. A required semantic fact, rename, type change, relation-validity change, or formula reinterpretation requires an explicit migration and major-version review. Passing JSON Schema alone is never evidence of semantic compatibility.

No country data is part of this release. Bahrain remains unchanged until separately authorized after release closeout.
