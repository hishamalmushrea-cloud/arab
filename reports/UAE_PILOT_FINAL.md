# United Arab Emirates Fourth-Country Pilot — Final Report

Generated from Schema v1.0.0 structured records; do not edit figures manually.

## Decision

**PASS.** The fourth-country pilot is United Arab Emirates only. It closes the seven-emirate federal layer and seven different local administrative profiles without imposing one lower hierarchy. No fifth country is authorized or started.

## Scope

The canonical UAE subset contains **41 Entities** (country, seven emirates, and 33 contextual local records), **42 Aliases**, **40 Relationships**, and **76 Claims**. This is a semantic transferability test, not a volume expansion. Structured JSON/JSONL and `manifests/AE.yml` are authoritative; this Markdown is generated.

## Snapshot

Snapshot `SNP-AE-PILOT-20260815` is dated **2026-08-15**. Its checksum covers the administrative, cultural, source-catalog, and evidence-manifest fixtures. The import is offline and deterministic. Retrieval dates are not treated as legal commencement dates.

## Source Evidence

The pilot references **20 atomic Sources**: 19 UAE pilot sources plus the existing ISO country source. There are **19 checksum-bound persisted relevant-text extracts**. Published Claims have **100.0% A/B sourcing** (76/76). Dubai community download failures are recorded in the persisted metadata extract; an unavailable file is not represented as a successful archive.

## Schema Changes

Schema remains **v1.0.0**. Additive changes introduce eight contextual UAE entity types, claim classification `emirate_specific`, entity statuses `renamed`, `merged`, and `abolished`, and optional manifest `emirate_profiles`. Legacy `ae_municipal_region`, `ae_sector`, and `ae_district` remain for backward compatibility but are deprecated and rejected for new UAE pilot entities. Problem, rationale, compatibility, temporal semantics, and tests are documented in `schema/UAE_PILOT_ADDITIVE_CHANGE.md`.

## Federal Emirates

The federal denominator is **7**, matched **7**, excluded **0**, unmatched **0**: Abu Dhabi (أبو ظبي), Dubai (دبي), Sharjah (الشارقة), Ajman (عجمان), Umm Al Quwain (أم القيوين), Ras Al Khaimah (رأس الخيمة), Fujairah (الفجيرة). Every emirate is a child of `ENT-AE-COUNTRY`; this closed layer makes no claim that local hierarchies are uniform.

## Abu Dhabi Hierarchy

**Competent authorities:** Department of Municipalities and Transport; Abu Dhabi City Municipality; Al Ain City Municipality; Al Dhafra Region Municipality.

| Contextual layer | Type | Denominator | Matched | Source | Semantic/special case |
|---|---|---:|---:|---|---|
| `abu_dhabi_municipality_jurisdictions` | `ae_abu_dhabi_municipality_jurisdiction` | 3 | 3 | `SRC-AE-DMT-THREE-MUNICIPALITIES-2026` | Three Abu Dhabi municipality jurisdictions named as DMT sub-sector regulatory authorities DMT calls the municipalities sub-sector regulatory authorities and refers to geographic jurisdiction; the pilot does not equate them with sectors. |

## Dubai Hierarchy

**Competent authorities:** Dubai Statistics Center; Dubai Municipality.

| Contextual layer | Type | Denominator | Matched | Source | Semantic/special case |
|---|---|---:|---:|---|---|
| `dubai_planning_sectors` | `ae_dubai_planning_sector` | 9 | 9 | `SRC-AE-DSC-SECTORS-2022` | Nine official numbered planning/statistical sectors of Dubai Sector numbers 1–9 are represented; Dubai Municipality metadata defines sec_num as the legal sector number. |
| `dubai_planning_communities` | `ae_dubai_planning_community` | unavailable | 0 | `SRC-AE-DUBAI-PULSE-COMMUNITIES-2025` | Dubai three-digit planning communities; official layer available but enumerable denominator unavailable in this snapshot Community.kml is official and updated 2025-11-03, but download failures prevented enumeration; denominator and percentage are null. |

## Sharjah Hierarchy

**Competent authorities:** Sharjah City Municipality; Al Hamriyah Region Municipality; Al Dhaid City Municipality; Mleiha Region Municipality; Al Madam Region Municipality; Al Batayeh Region Municipality; Dibba Al Hisn City Municipality; Kalba City Municipality; Khorfakkan City Municipality.

| Contextual layer | Type | Denominator | Matched | Source | Semantic/special case |
|---|---|---:|---:|---|---|
| `sharjah_municipality_jurisdictions` | `ae_sharjah_municipality_jurisdiction` | 9 | 9 | `SRC-AE-SGMB-MUNICIPALITIES-2023` | Nine municipality jurisdictions explicitly enumerated by Sharjah Government City/region wording is preserved in each official authority name. |

## Ajman Hierarchy

**Competent authorities:** Government of Ajman; Department of Digital Ajman.

| Contextual layer | Type | Denominator | Matched | Source | Semantic/special case |
|---|---|---:|---:|---|---|
| `ajman_constituents` | `ae_ajman_constituent` | 3 | 3 | `SRC-AE-AJMAN-ABOUT-2026` | Three named Ajman constituents with source-mixed city/area wording The source calls Manama and Masfout cities in the overview but uses area headings; ae_ajman_constituent preserves the mixed semantics. |

## Umm Al Quwain Hierarchy

**Competent authorities:** Municipality of Umm Al Quwain; Municipality of Falaj Al Mualla.

| Contextual layer | Type | Denominator | Matched | Source | Semantic/special case |
|---|---|---:|---:|---|---|
| `uaq_municipal_authorities` | `ae_uaq_municipal_authority` | 2 | 2 | `SRC-AE-UAQ-EXECUTIVE-COUNCIL-2026` | Two municipal authorities explicitly named by the Umm Al Quwain Executive Council Falaj Al Mualla Municipality is independently current under Decree No. 16 of 2008; no settlement layer is inferred. |

## Ras Al Khaimah Hierarchy

**Competent authorities:** Government of Ras Al Khaimah.

| Contextual layer | Type | Denominator | Matched | Source | Semantic/special case |
|---|---|---:|---:|---|---|
| `rak_administrative_areas` | `ae_rak_administrative_area` | 5 | 5 | `SRC-AE-RAK-GENERAL-2026` | Five numbered administrative areas of Ras Al Khaimah The fifth area has an official descriptive extent rather than a concise English proper name; source-faithful descriptive wording is retained. |

## Fujairah Hierarchy

**Competent authorities:** Government of Fujairah; Fujairah GIS Center; Fujairah Municipality; Dibba Municipality.

| Contextual layer | Type | Denominator | Matched | Source | Semantic/special case |
|---|---|---:|---:|---|---|
| `fujairah_municipal_authorities` | `ae_fujairah_municipal_authority` | 2 | 2 | `SRC-AE-FUJAIRAH-GIS-2017` | Two municipality authorities named as official GIS integration counterparts The denominator is bounded to municipality authorities named as GIS integration counterparts, not subordinate places. |

## Entity Resolution

English canonical names and Arabic official forms resolve to one parent-scoped Entity through Aliases. Same-name records under different parents are not automatically deduplicated. The independent identity rules distinguish Dibba Municipality in Fujairah from Dibba Al Hisn City Municipality in Sharjah, and distinguish numbered sectors, areas, constituents, and authorities. Validation reports zero duplicate IDs, orphans, cycles, or country mismatches; type counts are `{'ae_abu_dhabi_municipality_jurisdiction': 3, 'ae_ajman_constituent': 3, 'ae_dubai_planning_sector': 9, 'ae_emirate': 7, 'ae_fujairah_municipal_authority': 2, 'ae_rak_administrative_area': 5, 'ae_sharjah_municipality_jurisdiction': 9, 'ae_uaq_municipal_authority': 2, 'country': 1}`.

## Temporal Status

Current, historical, renamed, merged, abolished, and disputed semantics are distinct executable statuses. `Julfar` is one **historical Alias** and one historical claim for Ras Al Khaimah, never a current administrative unit. Falaj Al Mualla Municipality remains a current authority with a sourced historical claim that its independence followed Decree No. 16 of 2008. No renamed, merged, or abolished example is invented where the bounded sources do not establish one.

## Populated Places and Coordinates

No populated-place Entity was added. The pilot found no dated enumerable UAE-wide registry for cities, towns, villages, settlements, or neighborhoods, so those layers use `denominator_unavailable` and no percentage. Administrative entities have no invented point coordinates. Al Shindagha and other contextual place mentions remain sourced Claims rather than coordinate-free Entities.

## Denominators and Coverage

There are **12 Denominators** and 12 paired Coverage records: **9 closed** and **3 unavailable**. Every closed layer satisfies `matched + excluded = denominator`; every unavailable layer has a reason and no percentage.

| Layer | Denominator | Matched | Excluded | Unmatched | Coverage | Missing reason |
|---|---:|---:|---:|---:|---:|---|
| `abu_dhabi_municipality_jurisdictions` | 3 | 3 | 0 | 0 | 100.0% | — |
| `ajman_constituents` | 3 | 3 | 0 | 0 | 100.0% | — |
| `country_scope` | 1 | 1 | 0 | 0 | 100.0% | — |
| `dubai_planning_communities` | unavailable | 0 | 0 | 0 | — | denominator_unavailable: official Community.kml metadata was found, but the file could not be retrieved or enumerated; no web list or selected statistical rows were treated as a denominator |
| `dubai_planning_sectors` | 9 | 9 | 0 | 0 | 100.0% | — |
| `emirates` | 7 | 7 | 0 | 0 | 100.0% | — |
| `fujairah_municipal_authorities` | 2 | 2 | 0 | 0 | 100.0% | — |
| `neighborhoods` | unavailable | 0 | 0 | 0 | — | denominator_unavailable: no dated enumerable official cross-emirate neighborhood registry was established; no percentage is calculated |
| `populated_places` | unavailable | 0 | 0 | 0 | — | denominator_unavailable: no dated enumerable official UAE-wide registry of cities, towns, villages, or settlements was established; contextual page mentions are not a denominator |
| `rak_administrative_areas` | 5 | 5 | 0 | 0 | 100.0% | — |
| `sharjah_municipality_jurisdictions` | 9 | 9 | 0 | 0 | 100.0% | — |
| `uaq_municipal_authorities` | 2 | 2 | 0 | 0 | 100.0% | — |

## Cultural Sample

The sourced sample represents all seven emirates and the required coastal, desert, mountain, oasis, urban, and historical contexts. Environmental, heritage, livelihood, craft, and custom material is attached as scoped Claims to the country or emirate identity; unsupported fields are not filled. Cultural classifications are `{'emirate_specific': 14, 'historical': 3, 'local': 7, 'national': 5, 'popular': 2, 'regional': 2, 'shared': 3}`.

## Food, Dress, and Scope

Food Claims distinguish national association from shared origin: Gahwa/dates, food ecology, and Chabab are national-context records; Khameer is `shared`. Ayala and Sadu are also `shared`, and social performance context is `popular`. No Claim says a Gulf-shared practice is exclusive to the UAE. No dress Claim is materialized because the bounded evidence set did not provide sufficiently specific, scope-qualified support.

## Dialect Sample

The sample is limited to three forms from Ribeiro Daquila (2020). `وايد` and `شو` remain `regional` because the source explicitly locates them beyond uniquely Emirati use; `ربع` is documented in an Emirati translation without an exclusivity claim.

| Form | Meaning | Variety | Place | Register | Study date | Classification |
|---|---|---|---|---|---|---|
| ربع | friends | Emirati Arabic sample as used in the study | `ENT-AE-COUNTRY` | colloquial | 2020-12-18 | `national` |
| شو | what | Emirati Arabic sample as used in the study | `ENT-AE-COUNTRY` | colloquial | 2020-12-18 | `regional` |
| وايد | very much; a lot | Emirati Arabic sample as used in the study | `ENT-AE-COUNTRY` | colloquial | 2020-12-18 | `regional` |

## Independent Review and Negative Tests

Independent review is **PASS**: 33/33 sampled checks passed, with every required family at least 10% (`aliases 5/42, claims 8/76, coverage 2/12, cultural_claims 4/36, denominators 2/12, dialect_claims 1/3, entities 5/41, relationships 4/40, sources 2/20`). It does not import or call the UAE importer. Negative testing is **PASS**: 8/8 required mutations detected. P0=0; critical P1=0.

## Final Gate

UAE semantic validation: **PASS**. Independent review: **PASS**. Required mutations: **PASS**. Phase 5 clean-tree gate evidence: **PASS**. The transferability decision is: **PASS for contextual per-emirate modeling; stop and await authorization rather than begin another country.**
