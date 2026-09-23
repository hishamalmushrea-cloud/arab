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

## Depth cycle 1 lessons (2026-09-20)

14. A country whose first layer had zero cultural domains can open depth with a **published spine and an unpublished body** in one cycle: the UNESCO intangible-heritage list is authoritative and publishable, while everything from mirrors, the folklore journal, press, and blogs stays classified and unpublished in the same file.
15. The folklore journal of the country itself (مجلة الثقافة الشعبية) is a better dress/lexicon source than generic encyclopedic mirrors: it supplies names, local terms (خلق، طاقة، جفير، الكراخانة), and regional craft geography (بني جمرة، الجسرة، المحرق) without inventing anything.
16. A national element and shared files must be split inside the same predicate: الفجري carries `national`, while الخط العربي والنخلة والحناء والبشت carry `shared`. A blanket classification is a review failure.
17. Villages and حالات can enter as `current` places while فرجان enter as `historical`, provided both carry only `located_in` and no administrative parent; currentness is a settlement fact from a local source, not an administrative claim.
18. A locally documented non-Arabic presence (الفارسية via العجم والهولة) must be recorded without a speaker count: the mirror's 1995 figure was deliberately not used.
19. Press and blog sources for naming narratives are usable at tier E when the narrator is named (الشيخ صلاح الجودر) and the claim stays `local_reported`.

## Next-country implication

Kuwait should reuse the discipline, not Bahrain's hierarchy: establish its own governorate authority and denominator, then explicitly prevent address areas and blocks from being modeled as municipalities or governorates.
