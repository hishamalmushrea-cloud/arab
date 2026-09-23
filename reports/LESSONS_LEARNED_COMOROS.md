# Lessons Learned — Comoros

- Current Union administration contains three autonomous islands; Mayotte must not enter current coverage.
- Island, prefecture, commune, and village are separate levels.
- Law/INSEED enumeration reconciles 3/16/54 despite a secondary document typo stating 58 communes while listing 28+20+6.
- The 2026 UNESCO inscription supersedes older zero-property metadata.
- One serial World Heritage property is not six unrelated entities.
- Territorial claims require a separate future/disputed scope rather than alteration of current administrative parents.

## Depth cycle 1 lessons (2026-09-20)

7. A State Party list can hold exactly **one** element that is nevertheless a **seven-State file**: Comoros published the zaffa as `shared`, and the validator refuses to let any country in that file claim it alone.
8. A constitution is an A-tier source for facts about the State's own declarations — including a claim the project does not model as administration (Mayotte). The rule used here: the same record that reports the constitutional position must state that Mayotte is outside current administration, so the claim cannot be misread as an entity.
9. Language depth without numbers is still useful: three official languages are published with a source, two minority languages stay unpublished, and **no speaker count or share is recorded anywhere** — the validators reject the field outright.
10. A serial World Heritage property can be enriched without fragmenting it: criteria, area and buffer became published claims on the one property entity, while the six component names stayed an unpublished list until the property page itself enumerates them.
11. Six inscribed medinas are `quarter` places with `located_in` to the island only: the accepted 54-commune set does not contain every historic toponym (نتسودجيني، إتساندرا، إيكوني), so inferring a commune parent would have been fabrication.
12. Vocabulary can be recorded honestly when the source's limits are stated in the record: the numeral table and six phrases are marked as coming from a learner set that does not distinguish varieties and includes Swahili-influenced items.
13. A source pair is one citation unit: `second_source_id` without `second_source_locator` is not a weaker citation, it is a broken one. The general validator rejects it (`second source and second source locator must occur together`), and the country validator now enforces the same rule as `KM_SECOND_SOURCE_PAIR` with mutations in both directions.
14. `scripts/validate.py` prints its error list **above** the per-check report, so a clean `tail` is not a clean run: the gate must be judged by exit code and by the `claims:` line, not by the last lines of stdout. This is what let six bad claims survive the first cycle-1 pass while the tail looked green.
