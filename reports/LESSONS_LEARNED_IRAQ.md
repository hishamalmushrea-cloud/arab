# Lessons Learned — Iraq

- Halabja's KRI statistical use predates federal legal status; federal current `valid_from` is 2025-05-05.
- Federal and KRI records refer to one governorate identity, not duplicate entities.
- Current denominator is 19 only after Law 7/2025 and Gazette 4824.
- KRI profile count is four; it is a classification of the federal universe.
- Disputed and de facto geography requires independent dated overlays, never changed parents.
- District/subdistrict semantics remain unavailable until federal/KRI registers are reconciled.

## Depth cycle 1 — qada layer, three documented governorates (2026-08-17)

First Iraq cycle under **Maximum Arabic Knowledge Coverage** (`00_فلسفة_الموسوعة.md`):

- **31 attested qadas**: بغداد 14 (منها الشعب والشعلة 🔴 `unverified` — يردان في بعض القوائم فقط), نينوى 10 (منها سميل 🔴 بخلاف تبعية مسجل نينوى/دهوك), البصرة 7 (كلها 🟡 `probable`).
- The contested national frame (121 official vs 130+ with post-2013 creations vs ~103 pre-2013) is **recorded verbatim, never averaged**; no national qada denominator is invented.
- **3 unpublished Basra qada population claims** from the arithmetically consistent census hadar/rif table (2,362,123+546,368=2,908,491 — verified numerically).
- Disputed-territories notes (سهل نينوى، سنجار، الشيخان) and de-facto administration (مخمور تديرها أربيل عمليًا) stay **notes on the legal frame, never control inference** — the existing `IQ_UNSUPPORTED_OVERLAY` guard still enforces this.
- Status mapping is per-entity: list-dispute entries get `unverified` individually while their siblings stay `probable` — finer granularity than layer-wide status.
- Gate: **12/12 mutations** (4 new incl. upgrading a disputed entry to probable ✋); independent review **156/156**.
