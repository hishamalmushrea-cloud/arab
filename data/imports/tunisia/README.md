# Tunisia Phase 2 import snapshots

These files are deterministic **reconstructed import snapshots**, not byte-for-byte mirrors of upstream workbooks or shapefiles. They are committed so the canonical import is reproducible without a network request.

## Authority and licensing

| File | Canonical facts | Authority | Reuse statement |
|---|---|---|---|
| `official_municipalities_2024.csv` | 350 municipality codes and Arabic/French names | January 2024 Tunisian Collectivités Locales workbook (`SRC-TN-DGCL-MUNICIPALITIES-2024`, Tier A) | The resource does not state a specific license. This snapshot transcribes factual register fields only. Approximate centroids and `research_mun_uid` links are separately attributed to the ODbL research geometry source. |
| `institutional_admin_2022.csv` | 24 governorates, 264 delegations, 2,084 imadas and their dated hierarchy | HDX COD-AB v01 with INS lineage, valid from 2022-11-15 (`SRC-TN-HDX-CODAB-2022`, Tier B) | CC BY 3.0 IGO. Approximate coordinates are separately attributed to the Tier C research geometry source. |
| `municipality_delegation_overlap_evidence.csv` | Approximate municipality/delegation intersections, using the dated 2014 delegation codes | jmgclark research reconstruction (`SRC-TN-RESEARCH-GEOMETRY-2018`, Tier C) | ODbL 1.0 / DbCL. This evidence must not be treated as an official boundary. |
| `mapping_overrides.csv` | Eight explicitly reviewed residual links between official municipality codes and research geometry IDs | Internal matching review over the Tier A labels and Tier C candidate set | Decision metadata only; it does not create or replace an official name or boundary. |
| `phase1_population_claims.jsonl` | The 24 accepted Phase 1 governorate population claims, with Phase 2 evidence fields backfilled | INS RGPH 2014 (`SRC-TN-INS-RGPH-2014`, Tier A) and accepted commit `2040441` | Values and locators are preserved from the accepted claims; this immutable input prevents a Tunisia rebuild from depending on mutable canonical output. |

Exact upstream workbook bytes could not be archived in this environment. `snapshot_manifest.json` therefore hashes all five committed import inputs and makes no upstream checksum claim.

## Reconstruction and review rules

- Official/institutional labels and codes remain the naming authority. Research labels never overwrite them.
- The municipality mapping is bijective: 350 official codes map to 350 unique research municipality IDs.
- All 24 governorate and 264 delegation IDs from the accepted Phase 1 model are explicitly preserved.
- The eight non-greedy residual municipality links are recorded in `mapping_overrides.csv`. Eighteen additional label variations are marked `reviewed_label_match` in the main CSV.
- Municipality boundaries and delegation boundaries do not form a strict tree. Municipalities therefore have a governorate administrative parent and `boundary_intersects` evidence to one or more delegations. No singular delegation parent is invented.
- Only `delegation_2014_code` binds to the dated 264-delegation denominator. The 2018 field belongs to a later 274-delegation research topology and is retained only as research evidence.
- Arabic labels are NFC-normalized official transcriptions. Missing values are never inferred.

## Deterministic import

Run:

```bash
python3 scripts/import_tunisia_phase2.py
```

The importer verifies row counts, uniqueness, bijections, embedded Phase 1 IDs, and snapshot hashes before replacing Tunisia's canonical rows. It preserves every non-Tunisia row and is idempotent.
