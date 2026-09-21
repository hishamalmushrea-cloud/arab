# Lessons Learned — Kuwait Production Expansion

1. The six-governorate denominator is supported by a bilingual official census table; address areas and blocks remain different concepts.
2. Official pages can contain stale/prominent widgets that conflict with their own downloadable table. The accepted rows must reconcile arithmetically to the official total and the rejected display must be documented.
3. The six geographic rows sum to 4,381,139; adding Not Stated 4,578 yields 4,385,717. Not Stated is provenance/accounting, not an Entity.
4. Census year and retrieval date are separate. Without an official day/month, use year precision normalization and say so.
5. Zero is a valid official denominator: Kuwait has zero UNESCO-inscribed properties at snapshot while six sites are tentative. Tentative is not inscribed, and zero inscribed does not mean zero culture.
6. Population Claims benefit from two sources within one authority chain: exact table plus methodology/index context.
7. New automated mutations now reject area/block promotion, undated population, tentative-site promotion, and population tampering.

## Depth cycle 1 lessons (2026-09-20)

8. A country can enter depth with **zero** weak-source material published: the UNESCO inscription list is the authoritative spine (7 elements published at `verified`), and everything else stays classified and unpublished. This gives Kuwait a published/unpublished split that needs no tier downgrade of any official fact.
9. Shared Gulf heritage must be split *inside* the dish list, not after it: مجبوس/مرقوق/هريس/جريش/تشريبة/القيمات carry `shared`, while قبوط/محروق صبعه/مطبق زبيدي/مموش stay local. A single blanket classification is a review failure.
10. Historical quarters and فرجان are places, not tiers. They enter as `quarter`/`lane` entities with `status: historical`, exactly one `located_in`, **no** administrative parent, and **no** population claim — which is what keeps a heritage layer from leaking into the administrative hierarchy.
11. The first lane outside Sanaa (سكة عنزة) proves the lane layer is portable: any country with a documented سكة/زقاق inventory can open `lane` entities without a municipal denominator, provided the bounded-set statement is written down.
12. A zero-denominator heritage layer must say so in the manifest: `historic_city_quarters` declares `denominator: null`, `coverage_record_id: null`, and no percentage, while the ICH layer declares its own 7-element denominator as the inscription list itself.
13. Tier B is allowed for state news agency material with named researchers (كونا): it is stronger than a heritage forum but still capped at `local_reported` for naming narratives.

Qatar must retain these controls while defining municipality/zone/district/fareej from Qatar-specific authorities rather than copying Kuwait's hierarchy.
