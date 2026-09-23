# Mauritania Production Expansion Closeout

## Decision
**PASS.** Mauritania Production Micro Pilot accepted on exact commit `74103bf411933018e467c24261035e2fbddbff8d`.
## Scope
15 wilayas profiled; 63 moughataas known/open; communes conflicted 219/220.
## Snapshot
`SNP-MR-PRODUCTION-20260816`.
## Manifest
Wilayas closed; moughataas open; commune denominator withheld.
## Denominators
Country 1; wilayas 15; Nouakchott wilayas 3; regional wilayas 12.
## Entities
16 total; 15 new.
## Aliases
0; official French forms canonical.
## Relationships
15 country parents.
## Claims
15 profile Claims plus moughataa count and disputed commune candidates: 17.
## Sources
3 A-tier DGAT/ANSADE sources.
## Coverage
15/15 wilayas; 3/3 Nouakchott profiles; 12/12 regional profiles.
## Cultural coverage
Not imported.
## Dialect coverage
0 Claims.
## Independent review
PASS locally: 59/59.
## Negative tests
PASS locally 8/8 profile/count/conflict/premature-lower mutations.
## P0/P1
0/0.
## make check
PASS: Phase 5 88/88 plus nine production gates 21/21; full `make check` = 277 checks.
## GitHub CI
PASS: Push Action `31972325450` and PR Action `31972327386`.
## Remaining limitations
63 moughataa records deferred; commune denominator unresolved 219/220; culture/dialect deferred.
## Lessons learned
Known count is not closed coverage; conflicting lower counts require a disputed Claim and no denominator.
## Transferability
Schema 2.0.0 supports conflicted/open lower scope without change.
## Recommended next country
Lebanon Micro Pilot for recent governorate timing and district/municipality separation.

## Depth cycle 1 (2026-09-21)

The accepted layer is untouched (15 wilayas — three Nouakchott and twelve regional — with 63 moughataas known/open and the commune count still conflicted 219/220), and the depth cycle adds **56 claims and 7 places** on top of it: 73 claims, 23 entities, 22 relationships, 32 sources (24 A · 1 B · 7 E, counting the three accepted official sources).

**Published spine (27 claims, all verified, all on tier-A sources).** Nine inscribed UNESCO elements — **T'heydinn 00524 (2011, Urgent Safeguarding List; Mauritania is the only submitting State, so it is one of the three that may carry `national`)**, **المحضرة 01960 (2023, sole submission, `national`)** and **ملحمة سامبا غيلاديو 01692 (2024, sole submission, `national`)** — plus six shared elements where Mauritania appears among the submitting States (الكسكس 01602 بأربع دول · الخط العربي 01718 بست عشرة · النخلة 01902 بخمس عشرة · النقش على المعادن 01951 بعشر · الحناء 02116 بست عشرة · الزفّة 02283 بسبع). The 15 November 2006 ratification of the 2003 Convention is recorded once, and the three declared 2026 nominations (العود · السعفيات وألياف النباتات · الحناء) are recorded as **pending nominations** — published as stated nominations, never as inscriptions. The cultural spine closes with the two inscribed World Heritage properties — **قصور وادان وشنقيط وتشيت وولاتة (750، ثقافي 1996، المعايير iii/iv/v)** and **محمية بانك دارغان (506، طبيعي 1989؛ لم تُقرأ معاييره في هذه الدورة فتُسجَّل فارغة ولا يُبنى عليها وصف ثقافي)** — the three **tentative-list** sites of 2001 (أزوكي 1545 · كمبي صالح 1546 · تگداوست 1547), five articles of the 1991 (rev. 2012) Constitution (1 الطابع الإسلامي · 5 الدين · 6 العربية رسمية والبولارية والسوننكية والولوفية وطنية · 7 العاصمة نواكشوط · 9 الشعار), and four language rows: Arabic official, plus Pulaar `fuc`, Soninke `snk` and Wolof `wol` as national languages with the ISO 639-3 registry as a second source.

**Classified body (29 unpublished claims).** 7 remaining language rows (الحسانية `mey` · الزناغة `zen` · البمبارا `bam` · الطوارقية `taq` · السيريرية `srr` · لغة إشارة إفريقية فرنكوفونية بلا رمز · الفرنسية لغة عمل بحكم الأمر الواقع), a Hassaniya dialect profile and a script profile, 1 craft (السعفيات وألياف النباتات — the 2026 nomination recorded as a candidate craft, not an inscribed element), 2 customs, 12 dishes (مارو والحوت · زرق · مافي · الشاي الأخضر بالنعناع · لاخ · شوباجين · دجاج ياسا · الكسكس باللحم · بنافة · التيشطار · مشوي · بوليت), 2 dress items (الملحفة والدراعة), the capital-founding account (اختيار الموقع 1957 والحجر الأساس 5 مارس 1958) and two narratives — the declared **folk narrative** (رواية العالم وبئر نواكشوط من تقرير صحافي مؤرخ 2010-03-25، مصنَّفة `folk_narrative`) and the naming narrative (نوق الشط / نوكشوظ).

**No numbers.** No speaker count, no share, no population and no percentage anywhere: the mirrors print a speaker table and a 2013 estimate, both deliberately excluded, and the validator, the 78-mutation negative suite and the independent review all reject any count or share field — including a count hidden in claim notes.

**Places — no denominator.** Seven heritage places carry **one `located_in` relation each** and no other claim: four cities (شنقيط ووادان في آدرار · ولاتة في الحوض الشرقي · تيشيت في تكانت) sourced to the World Heritage property page and kept `source_verified`, and three archaeological sites (أزوكي في آدرار · تگداوست في الحوض الغربي · **كمبي صالح بلا ولاية متحقَّقة فتُسجَّل على موريتانيا وحدها**) from mirror summaries and kept `local_reported`. No administrative parent, no population, no coordinates and no new administrative level.

**Two open counts, both withheld from coverage.** The 63 moughataas stay a known open count with no records and no denominator claim, and the commune register conflict (219 or 220) stays a published **disputed** claim with a `commune` unit and no denominator — a mutation fails if either value is adopted as the denominator by default.
