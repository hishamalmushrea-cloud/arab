'use client';
import { useEffect, useState } from 'react';
import { db } from '@/data/db';
import Link from 'next/link';

export default function EntityPage({ params }: { params: { iso2: string; entityId: string } }) {
  const { iso2, entityId } = params;
  const decodedId = decodeURIComponent(entityId);
  const [entity, setEntity] = useState<any>(null);
  const [aliases, setAliases] = useState<any[]>([]);
  const [relationships, setRelationships] = useState<any[]>([]);
  const [claims, setClaims] = useState<any[]>([]);
  const [parent, setParent] = useState<any>(null);
  const [children, setChildren] = useState<any[]>([]);
  const [sources, setSources] = useState<any[]>([]);
  const [tab, setTab] = useState('identity');

  useEffect(() => {
    (async () => {
      const ent = await db.entities.get(decodedId) || (await db.entities.toArray()).find((e:any)=> e.id===decodedId);
      if (!ent) return;
      setEntity(ent);
      const als = await db.aliases.where('entityId').equals(ent.id).toArray();
      setAliases(als);
      const rels = await db.relationships.toArray();
      const related = rels.filter((r:any)=> r.childId===ent.id || r.parentId===ent.id);
      setRelationships(related);
      const parentRel = related.find((r:any)=> r.childId===ent.id && r.raw.relationship_type==='administrative_parent');
      if (parentRel) {
        const p = await db.entities.get(parentRel.parentId);
        setParent(p || null);
      }
      const childRels = related.filter((r:any)=> r.parentId===ent.id && r.raw.relationship_type==='administrative_parent');
      const childEnts = await Promise.all(childRels.map(async (r:any)=> await db.entities.get(r.childId)));
      setChildren(childEnts.filter(Boolean) as any[]);

      const cls = await db.claims.where('subjectId').equals(ent.id).toArray();
      setClaims(cls);

      // sources
      const allSources = await db.sources.toArray();
      const sourceIds = new Set<string>();
      sourceIds.add(ent.raw.canonical_source_id);
      als.forEach(a=> sourceIds.add(a.raw.source_id));
      related.forEach(r=> sourceIds.add(r.raw.source_id));
      cls.forEach(c=> { sourceIds.add(c.raw.source_id); if (c.raw.second_source_id) sourceIds.add(c.raw.second_source_id); });
      const srcs = allSources.filter(s=> sourceIds.has(s.id));
      setSources(srcs);
    })();
  }, [decodedId]);

  if (!entity) return <div className="p-8">جاري تحميل الكيان {decodedId}... <Link href={`/${iso2}`} className="text-blue-600 underline">رجوع للدولة</Link></div>;

  const hasCoords = !!entity.raw.coordinates || (entity.raw.notes && entity.raw.notes.includes('coordinates'));

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 text-sm text-gray-500">
        <Link href="/" className="hover:underline">الرئيسية</Link><span>/</span>
        <Link href="/countries" className="hover:underline">الدول</Link><span>/</span>
        <Link href={`/${iso2}`} className="hover:underline">{iso2}</Link><span>/</span>
        <span className="font-bold">{entity.canonicalName}</span>
      </div>

      <div className="bg-white rounded-xl border p-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold">{entity.canonicalName}</h1>
            <div className="text-sm text-gray-600">اللغة: {entity.raw.canonical_name_language} — النوع: {entity.raw.entity_type}</div>
            <div className="text-xs font-mono ltr bg-gray-50 px-2 py-1 rounded mt-2 inline-block">{entity.id}</div>
            <div className="mt-2 flex gap-2">
              <span className={`badge ${entity.status==='current'?'badge-verified': entity.status==='historical'?'badge-historical' : 'badge-disputed'}`}>{entity.status}</span>
              <span className="badge badge-partial">{entity.raw.verification_status}</span>
              <span className="badge badge-unverified">{entity.raw.confidence}</span>
            </div>
          </div>
          <div className="text-4xl">{entity.raw.entity_type.includes('governorate')?'🏛️': entity.raw.entity_type==='country'?'🌍':'📍'}</div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 text-sm">
          <div>الدولة: {entity.countryCode}</div>
          <div>الوالد: {parent ? <Link href={`/${iso2}/${parent.id}`} className="text-blue-600 underline">{parent.canonicalName}</Link> : '— (دولة أو جذر)'}</div>
          <div>الأبناء: {children.length}</div>
          <div>الأسماء البديلة: {aliases.length}</div>
          <div>العلاقات: {relationships.length}</div>
          <div>المعلومات: {claims.length}</div>
          <div>الإحداثيات: {entity.raw.coordinates ? `${JSON.stringify(entity.raw.coordinates).slice(0,60)}` : 'غير متوفرة (لا نخترع)'}</div>
          <div> الفترة: {entity.raw.valid_from || '—'} → {entity.raw.valid_to || 'حتى الآن'}</div>
        </div>
      </div>

      <div className="flex gap-2 flex-wrap border-b pb-2">
        {[
          ['identity','الهوية'],
          ['names','الأسماء البديلة'],
          ['claims','المعلومات'],
          ['relations','العلاقات'],
          ['sources','المصادر'],
          ['map','الخريطة'],
          ['raw','البيانات الخام']
        ].map(([k,l])=> <button key={k} onClick={()=>setTab(k)} className={`px-4 py-2 rounded-full text-sm border ${tab===k?'bg-black text-white':''}`}>{l}</button>)}
      </div>

      {tab==='identity' && (
        <div className="space-y-3">
          <div className="card text-sm">
            <div className="font-bold mb-2">الهوية الأساسية — كل الحقول محفوظة</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              <div>canonical_name: {entity.raw.canonical_name}</div>
              <div>canonical_name_language: {entity.raw.canonical_name_language}</div>
              <div>canonical_source_id: <Link href={`/sources/${entity.raw.canonical_source_id}`} className="text-blue-600 underline font-mono ltr text-xs">{entity.raw.canonical_source_id}</Link></div>
              <div>source_locator: {entity.raw.source_locator}</div>
              <div>country_code: {entity.countryCode}</div>
              <div>entity_type: {entity.raw.entity_type}</div>
              <div>status: {entity.status}</div>
              <div>valid_from: {entity.raw.valid_from || 'null'}</div>
              <div>valid_to: {entity.raw.valid_to || 'null'}</div>
              <div>verification_status: {entity.raw.verification_status}</div>
              <div>confidence: {entity.raw.confidence}</div>
              <div>legacy_ids: {entity.raw.legacy_ids?.join(', ') || '[]'}</div>
              <div className="md:col-span-2">notes: {entity.raw.notes || '—'}</div>
              <div>schema_version: {entity.raw.schema_version}</div>
            </div>
          </div>

          {parent && <div className="card text-sm"><div className="font-bold">الوالد الإداري</div><Link href={`/${iso2}/${parent.id}`} className="text-blue-600 underline">{parent.canonicalName} — {parent.id}</Link><div className="text-xs">عبر علاقة administrative_parent موثقة</div></div>}

          <div className="card text-sm">
            <div className="font-bold mb-2">الأبناء المباشرون ({children.length})</div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
              {children.slice(0,50).map((ch:any)=> <Link key={ch.id} href={`/${iso2}/${ch.id}`} className="border rounded p-2 hover:bg-gray-50"><div className="font-bold text-xs">{ch.canonicalName}</div><div className="font-mono ltr text-[10px]">{ch.id}</div><div className="text-[10px]">{ch.raw.entity_type}</div></Link>)}
            </div>
            {children.length>50 && <div className="text-xs text-gray-500 mt-2">عرض 50 من {children.length} — استخدم البحث للباقي</div>}
          </div>
        </div>
      )}

      {tab==='names' && (
        <div className="space-y-2">
          <div className="text-sm text-gray-600">جميع الأسماء البديلة — حتى التاريخي واللاتيني — قابلة للبحث. مثال البحث عن "مقشن" يجد هذا الكيان لو كان alias.</div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {aliases.map((a:any)=>(
              <div key={a.id} className="card text-xs">
                <div className="font-bold">{a.raw.name}</div>
                <div className="font-mono ltr text-[10px]">{a.id} — entity_id: {a.entityId}</div>
                <div>language: {a.raw.language} — script: {a.raw.script} — kind: {a.raw.kind} — status: {a.raw.status}</div>
                <div>valid: {a.raw.valid_from||'—'} → {a.raw.valid_to||'—'} — source: {a.raw.source_id} — locator: {a.raw.source_locator}</div>
              </div>
            ))}
            {aliases.length===0 && <div className="card text-sm">لا توجد أسماء بديلة لهذا الكيان في Release Dataset.</div>}
          </div>
        </div>
      )}

      {tab==='claims' && (
        <div className="space-y-3">
          <div className="text-xs text-gray-600">جميع Claims حيث subject_id = هذا الكيان. حتى المتنازع وغير المؤكد يظهر مع سبب.</div>
          {claims.length===0 && <div className="card text-sm">لا توجد Claims لهذا الكيان في اللقطة الحالية — هذا طبيعي للكيانات الإدارية الصرفة التي لها فقط علاقات.</div>}
          <div className="space-y-2">
            {claims.map((c:any)=>(
              <div key={c.id} className={`card text-xs ${c.raw.status==='disputed'?'border-red-300 bg-red-50': c.raw.status==='uncertain'?'border-gray-300 bg-gray-50':''}`}>
                <div className="flex justify-between">
                  <div className="font-bold">{c.raw.predicate} — {c.raw.value?.type}: {JSON.stringify(c.raw.value?.data).slice(0,200)}</div>
                  <div className="flex gap-1">
                    <span className={`badge ${c.raw.status==='verified'?'badge-verified': c.raw.status==='disputed'?'badge-disputed':'badge-historical'}`}>{c.raw.status}</span>
                    <span className="badge badge-unverified">{c.raw.classification}</span>
                  </div>
                </div>
                <div className="font-mono ltr text-[10px]">{c.id} — verification: {c.raw.verification_status} — confidence: {c.raw.confidence} — published: {String(c.raw.published)}</div>
                <div>source: {c.raw.source_id} — locator: {c.raw.source_locator} — second: {c.raw.second_source_id||'—'} — unit: {c.raw.unit||'—'}</div>
                {c.raw.lexical_context && <div className="bg-gray-50 p-2 rounded mt-1">lexical_context: form={c.raw.lexical_context.form} meaning={c.raw.lexical_context.meaning} language={c.raw.lexical_context.language} dialect={c.raw.lexical_context.dialect} ipa={c.raw.lexical_context.ipa}</div>}
                <div className="text-[10px] text-gray-500">observed_at: {c.raw.observed_at} — valid: {c.raw.valid_from||'—'}→{c.raw.valid_to||'—'} — notes: {c.raw.notes||'—'}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {tab==='relations' && (
        <div className="space-y-2">
          <div className="text-xs">جميع العلاقات — لا نخفي أي علاقة، حتى boundary_intersects التي هي تقاطع حدودي وليست والد إداري.</div>
          {relationships.map((r:any)=>(
            <div key={r.id} className={`card text-xs ${r.raw.relationship_type==='boundary_intersects'?'bg-blue-50 border-blue-200':''}`}>
              <div className="font-bold">{r.raw.relationship_type} — {r.raw.status}</div>
              <div className="font-mono ltr text-[10px]">{r.id}: {r.childId} → {r.parentId}</div>
              <div>valid: {r.raw.valid_from||'—'}→{r.raw.valid_to||'—'} — confidence: {r.raw.confidence} — verification: {r.raw.verification_status}</div>
              <div>source: {r.raw.source_id} — locator: {r.raw.source_locator}</div>
              <div>notes: {r.raw.notes||'—'}</div>
              {r.raw.relationship_type==='boundary_intersects' && <div className="text-blue-700 text-[10px] mt-1">تنبيه: هذه علاقة تقاطع حدودي (boundary_intersects) وليست والد إداري (administrative_parent)</div>}
            </div>
          ))}
        </div>
      )}

      {tab==='sources' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {sources.map((s:any)=>(
            <div key={s.id} className="card text-xs">
              <div className="font-bold">{s.raw.title}</div>
              <div className="font-mono ltr text-[10px]">{s.id} — {s.raw.quality_tier} — {s.raw.source_type}</div>
              <div>publisher: {s.raw.publisher||'—'} — organization: {s.raw.organization||'—'}</div>
              <div>license: {s.raw.license?.slice(0,120)}</div>
              <div>publication_date: {s.raw.publication_date||'—'} — retrieved_at: {s.raw.retrieved_at||'—'}</div>
              <div>locator: {s.raw.locator}</div>
              <div className="flex gap-2 mt-1">
                {s.raw.url && <a href={s.raw.url} target="_blank" className="text-blue-600 underline">URL (يتطلب إنترنت)</a>}
                {s.raw.archive_url && <a href={s.raw.archive_url} target="_blank" className="text-green-600 underline">Archive</a>}
              </div>
              <div className="text-[10px] text-gray-500">checksum: {s.raw.checksum?.slice(0,20)} — notes: {s.raw.notes?.slice(0,100)}</div>
            </div>
          ))}
        </div>
      )}

      {tab==='map' && (
        <div className="space-y-3">
          {entity.raw.coordinates ? (
            <div className="card">
              <div className="font-bold">الإحداثيات الموثقة</div>
              <div className="font-mono ltr">{JSON.stringify(entity.raw.coordinates)}</div>
              <div className="mt-2">
                <a href={`https://www.openstreetmap.org/?mlat=${entity.raw.coordinates.lat || entity.raw.coordinates.latitude}&mlon=${entity.raw.coordinates.lon || entity.raw.coordinates.longitude}#map=12/${entity.raw.coordinates.lat || entity.raw.coordinates.latitude}/${entity.raw.coordinates.lon || entity.raw.coordinates.longitude}`} target="_blank" className="text-blue-600 underline">فتح في OpenStreetMap (يتطلب إنترنت)</a>
              </div>
              <div className="text-xs text-gray-500 mt-2">لا نخترع موقعاً مفقوداً. هذه الإحداثيات من المصدر الرسمي فقط.</div>
            </div>
          ) : (
            <div className="card bg-gray-50">
              <div className="font-bold">لا توجد إحداثيات موثقة لهذا الكيان في هذه اللقطة</div>
              <div className="text-xs text-gray-600">حسب schema_v2.md: "الإحداثيات اختيارية لا تخمينية" — لا نعرض موقعاً وهمياً.</div>
            </div>
          )}
          <div className="card text-xs">
            <div className="font-bold">ملاحظة الخرائط</div>
            <div>Phase APP-1 يعرض الإحداثيات النقطية فقط. Polygons ستضاف لاحقاً عندما تتوفر من مصدر رسمي بترخيص واضح. لا تخترع هندسة.</div>
          </div>
        </div>
      )}

      {tab==='raw' && (
        <div className="space-y-2">
          <div className="card"><div className="font-bold text-xs">Entity Raw JSON — كل الحقول محفوظة</div><pre className="text-[10px] font-mono ltr bg-gray-50 p-2 rounded overflow-auto max-h-96">{JSON.stringify(entity.raw, null,2)}</pre></div>
          <div className="card"><div className="font-bold text-xs">Aliases Raw ({aliases.length})</div><pre className="text-[10px] font-mono ltr bg-gray-50 p-2 rounded overflow-auto max-h-96">{JSON.stringify(aliases.map(a=>a.raw), null,2)}</pre></div>
          <div className="card"><div className="font-bold text-xs">Claims Raw ({claims.length})</div><pre className="text-[10px] font-mono ltr bg-gray-50 p-2 rounded overflow-auto max-h-96">{JSON.stringify(claims.map(c=>c.raw), null,2)}</pre></div>
          <div className="card"><div className="font-bold text-xs">Relationships Raw ({relationships.length})</div><pre className="text-[10px] font-mono ltr bg-gray-50 p-2 rounded overflow-auto max-h-96">{JSON.stringify(relationships.map(r=>r.raw), null,2)}</pre></div>
        </div>
      )}
    </div>
  );
}
