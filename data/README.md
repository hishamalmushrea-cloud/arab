# المصدر المنظم — Schema v1

هذا المجلد هو مصدر الحقيقة للمشروع. التغطية المحلية غير مكتملة ولا تمثل جميع المدن
أو القرى أو التجمعات أو الأحياء أو الحارات.

| المجلد | المحتوى |
|---|---|
| `entities/` | هويات الأماكن والوحدات الإدارية ذات مصدر قانوني/مرجعي |
| `aliases/` | الأسماء البديلة لنفس الكيان |
| `relationships/` | التبعية والعلاقات المكانية والزمنية ذات المصدر |
| `claims/` | ادعاءات قابلة للفحص؛ لا سجل بلا `source_id` |
| `sources/` | ملف JSON ذري لكل مادة منشورة |
| `snapshots/` | لقطات مؤرخة وقابلة لإعادة الإنتاج |
| `coverage/` | المقامات وسجلات matched/unmatched/excluded/missing |
| `quarantine/` | مواد قديمة غير مرقاة وسجلات الإصلاح والهجرة |

العقد الكامل في [`../schema/schema_v1.md`](../schema/schema_v1.md)، والـmanifests في
[`../manifests/`](../manifests/)، والعروض المولدة في
[`../generated/markdown/README.md`](../generated/markdown/README.md).

```bash
python3 scripts/validate.py
python3 scripts/generate.py --check
```

تُشغّل الأوامر من جذر المستودع.
