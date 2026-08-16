# Lessons Learned — Bahrain Production Expansion

## What transferred cleanly

Schema 2.0.0 represented a compact four-governorate system and serial cultural properties without new fields or entity types. Existing administrative parents, contextual associations, typed Claims, atomic Sources, snapshots, denominators, and coverage arithmetic were sufficient.

## New operational lessons

1. **Current list from time series:** filter an official time-series dataset to one explicit year, preserve the year as `as_of`, and preserve retrieval separately.
2. **Historical absence is not deletion:** the source states redivision from five to four in 2014. Central Governorate must not appear as current, but a historical entity needs a separate atomic historical topology source before creation.
3. **Bilingual enumeration is identity evidence:** Arabic and English values from the same official row form one entity plus Alias, not two entities.
4. **Administrative polygon is not a point:** no centroid coordinate was invented.
5. **Serial heritage properties:** one UNESCO property may contain many buildings, mounds, beds, or component sites. Do not multiply entities without a component-level scope and identity decision.
6. **Country association can be safer than a false local parent:** serial properties were linked to Bahrain via `associated_with`; governorate assignment was not guessed.
7. **Cultural restraint:** a complete three-property World Heritage layer does not imply cultural completeness. Food, dress, custom, and dialect remained `not_documented_in_cycle`.
8. **Open-data licensing is separate evidence:** the official Open Data Policy was captured atomically rather than treating portal availability as an unstated license.

## Rules promoted to automation

The Bahrain validator and nine mutations now enforce: exact four-governorate identity, country parents, official areas, exclusion of Central as current, serial-property association, no cultural leakage to governorates, no unsupported dialect Claim, no foreign source, no denominator inflation, and no Alias-as-Entity promotion.

## Next-country implication

Kuwait should reuse the discipline, not Bahrain's hierarchy: establish its own governorate authority and denominator, then explicitly prevent address areas and blocks from being modeled as municipalities or governorates.
