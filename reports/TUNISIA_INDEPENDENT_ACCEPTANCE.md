# Tunisia independent methodological acceptance

**Audit date:** 2026-08-15  
**Accepted technical baseline reviewed:** `3410ef06188e133e5aa5e3cb9cde58d41900682f`  
**Country:** Tunisia (`TN`)

This is a content gate, not a restatement of schema, validator, build, or GitHub status. The immutable before-images are in `data/quarantine/tunisia_independent_audit_before.jsonl`; the machine-readable sample and every claim trace are in `reports/tunisia_independent_acceptance_sample.json`; repairs are recorded in `data/quarantine/tunisia_independent_audit_repairs.json`.

## Decision

**PASS**

Tunisia is ready to serve as the accepted model for a staged next-country cycle. The independent review found serious but remediable source-selection, locator, entity-classification, coordinate-provenance, and geographic-scope errors. All six grouped P1 findings were repaired in structured data and producer scripts; the 28 sampled claim traces now resolve to supported replacement records, with no open P0 or P1 finding. The faults did not require a schema change. They do require every future country to repeat this evidence-opening independent gate rather than treating technical CI as content acceptance.

## Independent method

### Reproducible claim sample

The sample was drawn from the 69 Tunisia claims in the accepted snapshot, before repair. Seed: `tn-independent-2026-08-15-v1`. Records were ordered by ascending SHA-256 of:

```text
seed + NUL + stratum + NUL + claim_id
```

The sample contains 28 claims: eight population, four site-description, three cultural, three place-classification, three significance, three place-connection, one custom-practice, one craft-practice, one condition, and one period claim. This stratification prevents the larger population and heritage families from displacing the smaller cultural and person families.

For every selected record, the reviewer followed Entity → Claim → Source → locator, opened the referenced source, compared the exact value and geographic/temporal scope, and used only the five required classifications. The complete ordered list of claim IDs, source URLs, locators, values, reasons, and replacement IDs is in the machine-readable sample.

### Independent rules

The content review separately tested for:

- wrong administrative parent or layer;
- unsupported exact values and aliases attached to the wrong entity;
- national claims localized without locality evidence;
- historical/archaeological descriptions modeled as current populated places;
- cultural claims generalized below the source's geographic scope;
- inflated source tiers or metadata that points to the wrong document;
- source conflict, unavailable pages, and missing row/page locators;
- coordinates whose source represents a heritage site rather than the modeled place; and
- dialect/lexical publication without form, meaning, geography, source, study or speaker, date, register, and IPA where needed.

These rules are independent of `scripts/validate.py`. The existing 598-record structural second pass was retained as a separate check and is not counted as source-content verification.

## Claim results at audit entry

These are the required five-way results against the accepted before-image, prior to remediation.

| Classification | Count | Percentage |
|---|---:|---:|
| supported | 13 | 46.43% |
| partially supported | 9 | 32.14% |
| unsupported | 6 | 21.43% |
| ambiguous | 0 | 0.00% |
| source unavailable | 0 | 0.00% |
| **Total** | **28** | **100.00%** |

Fifteen of 28 sampled claims were therefore not fully supported at audit entry. Six exact population values had only a rounded cited table even though a different INS volume confirmed them; two sampled values, Kairouan and Nabeul, were contradicted by the exact table. The other defects were the wrong Sidi Bou Saïd World Heritage property and unsupported period wording, a generic El Jem type despite an explicit village description, two cultural claims localized to municipality boundaries not stated by UNESCO, Magon represented as a current neighborhood rather than an archaeological quarter, and two Ibn Khaldun claims pointing to the adjacent wrong article.

After source-exact remediation, all 28 tracked traces map to supported canonical records. This recheck closes the sampled defects but does not rewrite the before-image percentages.

## Administrative hierarchy research check

The independently selected hierarchy sample contains 42 records:

| Layer | Reviewed | Errors | Evidence check |
|---|---:|---:|---|
| governorates | 6 | 0 | name, type, country parent, date, official hierarchy source |
| delegations | 12 | 0 | name and governorate parent against the Interior Ministry table |
| imadas | 12 | 0 | Arabic row and delegation parent against the Interior Ministry imada catalog |
| municipalities | 12 | 0 | name, governorate association, type, date, and coded register source |
| **Total** | **42** | **0** | |

Sampling used the same seed and hash rule with layer-specific strata and source external codes. All 12 sampled imadas received row-level official corroboration. Municipalities remain separate legal entities parented to governorates, with `boundary_intersects` relationships where boundaries cross delegation geometry; they were not forced into a false delegation tree.

The dated modeled denominators remain 24 governorates, 264 delegations, and 350 municipalities. The 2,084 imadas are a dated imported layer, but the project correctly retains `denominator_status = unavailable` because no reusable official denominator register was established. No completeness claim is inferred from file existence.

## A/B source audit

All eight Tier A/B sources referenced by the claim sample were reviewed for publisher authority, URL, title, publication year, Tunisia relevance, claimed domain, availability, and an actionable page, table, record, or row locator.

| Result | Count |
|---|---:|
| Tier A reviewed | 5 |
| Tier B reviewed | 3 |
| metadata errors | 2 |
| tier changes | 0 |
| unavailable sources | 0 |

The two repaired metadata errors were consequential:

1. `SRC-TN-INS-RGPH-2014` cited rounded Volume 0 for exact values. It now cites INS Volume 3, publication year 2016, PDF page 47.
2. `SRC-UNESCO-IBN-KHALDUN` pointed to `pf0000068103`. It now cites “Tradition and experiment in Arabic letters,” January 1986, `pf0000068104`, pp. 17–18.

No A/B classification was inflated enough to require a tier change. The separately used Tier C geometry source remains explicitly limited to approximate coordinate/boundary cross-checking and is not treated as an official administrative authority.

## Populated places and entity boundaries

Six accepted populated-place records were audited for canonical name, aliases, current versus historical status, controlled type, parent/context, coordinates, and source. Nine erroneous fields were found across source locators, classifications/current-versus-archaeological scope, and coordinate provenance.

Repairs replaced current Sousse `town` with a sourced city, El Jem `settlement` with the source's village classification, and current Magon `neighborhood` with an archaeological site under the separate Carthage site entity. Unsupported points were removed where the cited tourism or heritage locator did not establish the represented place's coordinates. The validator no longer forces six different populated-place classes; that rule encouraged template-shaped coverage rather than evidence-shaped data. The resulting six records use three evidenced place types and remain a bounded pilot, not a claim of complete populated-place coverage.

Names shared with governorates, delegations, heritage properties, or archaeological quarters were not treated as proof of entity identity. Administrative entities, current populated places, and historical/archaeological sites remain separate.

## Cultural and dialect/lexical audit

Four cultural claims were reviewed. Two geographic-attribution errors were found and repaired:

- Sejnane women's pottery moved from legal-municipality scope to a sourced Sejnane village entity.
- Charfia fishing moved from legal-municipality scope to the Kerkennah Islands geographic entity.

The Tunisia-wide harissa claim remains national because its source is national. No national content was copied into a city or village.

Canonical data publishes zero lexical or dialect claims. Lexical status remains `not_found`; dialect status remains `not_documented`; dialect-attribution errors are zero. No example was invented to fill the category because no candidate had the required form, meaning, region, source, study/speaker, date, register, and IPA package.

## Error ledger and severity

| Error family | Count at audit entry | Current open count |
|---|---:|---:|
| claim records not fully supported | 15 | 0 |
| hierarchy errors | 0 | 0 |
| source metadata errors | 2 | 0 |
| source tier changes | 0 | 0 |
| cultural-attribution errors | 2 | 0 |
| dialect-attribution errors | 0 | 0 |
| populated-place erroneous fields | 9 | 0 |
| P0 findings | 0 | 0 |
| grouped P1 findings | 6 | 0 |

The six P1 groups were: exact-population source/value integrity; Sidi Bou Saïd property/period integrity; Ibn Khaldun source identity; current-place versus historical-site classification; coordinate provenance; and cultural geographic scope. Before-images were preserved rather than deleted.

## Schema and workflow conclusion

**Schema change needed:** no. Existing entity types, relationship vocabulary, temporal/status fields, source records, locators, geographic entities, verification state, and quarantine mechanism represented every evidence-exact correction.

Producer/workflow repairs were needed. Legacy migration now emits required verification fields; Tunisia regeneration preserves curated atomic source records; exact population claims and IDs are deterministic; the Phase 2 importer rebuilds the repaired entities and claims; and `make repair` is stable on repeated execution. A second full repair compared 72 canonical/generated/review files and changed none. The local technical gate must still be reported separately from this independent content conclusion.

## Limitations

- This was a reproducible sample, not a census of all 2,743 Tunisia entities or every upstream row.
- The municipality label artifact is a reviewed reconstruction from rendered institutional evidence rather than a byte-faithful copy of the transient upstream workbook.
- Municipal boundaries are not a strict subdivision of delegations; relationships correctly preserve that limitation.
- No reusable official imada denominator was found, so administrative completeness is not claimed for that layer.
- Source availability and register content were checked as of 2026-08-15 and can change.
- Six populated places are sufficient only for the bounded pilot test; they do not constitute national settlement coverage.
- The absence of publishable dialect/lexical records means the workflow's abstention behavior was tested, not the quality of a positive lexical corpus.

## Staged expansion recommendation

Do not start another country in this task. For the next single full denominator-to-independent-gate cycle, use **Jordan**: its country-specific administrative nomenclature and source landscape provide a useful test of whether the repaired source/locator and geographic-scope controls transfer without copying Tunisia's hierarchy. Create a Jordan-specific Manifest before import, and repeat the same independent content gate before any further scale-out.

Only after that single-country cycle should expansion proceed in these requested groups:

- **A** — Bahrain, Kuwait, Qatar, Jordan, Oman, Lebanon, UAE
- **B** — Tunisia, Morocco, Egypt, Saudi Arabia, Algeria, Mauritania
- **C** — Palestine, Iraq, Syria, Yemen, Sudan, Somalia, Libya, Comoros, Djibouti

Each country must use its own Manifest and nomenclature. No group ordering authorizes mass place generation, downward localization of national content, or progression past a failed country gate.
