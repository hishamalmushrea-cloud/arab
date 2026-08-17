'use client';
import { useEffect, useState } from 'react';
import { db } from '@/data/db';
import Link from 'next/link';

export default function CountryPage({ params }: { params: { iso2: string } }) {
  const iso2 = params.iso2.toUpperCase();
  const [countryEnt, setCountryEnt] = useState<any>(null);
  const [entities, setEntities] = useState<any[]>([]);
  const [coverage, setCoverage] = useState<any[]>([]);
  const [manifest, setManifest] = useState<any>(null);
  const [sources, setSources] = useState<any[]>([]);
  const [tab, setTab] = useState('overview');

  useEffect(() => {
    (async () => {
      const country = await db.entities.where('countryCode').equals(iso2).filter(e=>e.raw.entity_type==='country').first();
      if (!country) {
        // fallback search by id contains iso2
        const all = await db.entities.toArray();
        const found = all.find((e:any)=> e.id.includes(`-${iso2}-`) && e.raw.entity_type==='country') || all.find((e:any)=> e.countryCode===iso2);
        setCountryEnt(found || null);
      } else {
        setCountryEnt(country);
      }
      const ents = await db.entities.where('countryCode').equals(iso2).toArray();
      setEntities(ents);
      const cov = await db.coverage.where('countryCode').equals(iso2).toArray();
      setCoverage(cov);
      const mf = await db.manifests.where('iso2').equals(iso2).first() || (await db.manifests.toArray()).find((m:any)=> m.raw.country?.iso2===iso2);
      setManifest(mf?.raw || null);

      // sources related to this country
      const allSources = await db.sources.toArray();
      const relatedSourceIds = new Set<string>();
      ents.forEach((e:any)=> relatedSourceIds.add(e.raw.canonical_source_id));
      const rels = await db.relationships.toArray();
      rels.filter(r=> ents.some((e:any)=> e.id===r.childId || e.id===r.parentId)).forEach(r=> relatedSourceIds.add(r.raw.source_id));
      const claims = await db.claims.toArray();
      claims.filter(c=> ents.some((e:any)=> e.id===c.subjectId)).forEach(c=> relatedSourceIds.add(c.raw.source_id));
      const srcs = allSources.filter(s=> relatedSourceIds.has(s.id) || (s.raw.country_codes && s.raw.country_codes.includes(iso2)));
      setSources(srcs);
    })();
  }, [iso2]);

  if (!countryEnt && entities.length===0) {
    return <div className="p-8"><div className="text-lg">جاري تحميل بيانات {iso2}... إذا بقي فارغاً، تأكد من تشغيل import في الرئيسية.</div><Link href="/" className="text-blue-600 underline">الرئيسية</Link></div>;
  }

  const types = Array.from(new Set(entities.map((e:any)=> e.raw.entity_type))).sort();

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 text-sm text-gray-500">
        <Link href="/" className="hover:underline">الرئيسية</Link>
        <span>/</span>
        <Link href="/countries" className="hover:underline">الدول</Link>
        <span>/</span>
        <span className="font-bold">{countryEnt?.canonicalName || iso2}</span>
      </div>

      <div className="bg-white rounded-xl border p-6">
        <h1 className="text-3xl font-bold">{countryEnt?.canonicalName || iso2} — {iso2}</h1>
        <div className="text-xs font-mono ltr">{countryEnt?.id || '—'}</div>
        {manifest?.caveats && <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded p-3 text-xs"><div className="font-bold">تنبيهات منهجية:</div><ul className="list-disc pr-4">{manifest.caveats.map((c:string,i:number)=><li key={i}>{c}</li>)}</ul></div>}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 text-sm">
          <div>كيانات: {entities.length}</div>
          <div>طبقات تغطية: {coverage.length}</div>
          <div>مكتملة: {coverage.filter(c=>c.raw.complete).length}</div>
          <div>مصادر: {sources.length}</div>
        </div>
      </div>

      <div className="flex gap-2 flex-wrap border-b pb-2">
        {[
          ['overview','نظرة عامة'],
          ['admin','التقسيم الإداري'],
          ['layers','الطبقات'],
          ['places','الأماكن'],
          ['sources','المصادر'],
          ['coverage','التغطية والقيود'],
          ['raw','البيانات الخام']
        ].map(([k,label])=> <button key={k} onClick={()=>setTab(k)} className={`px-4 py-2 rounded-full text-sm border ${tab===k?'bg-black text-white':''}`}>{label}</button>)}
      </div>

      {tab==='overview' && (
        <div className="space-y-4">
          <div className="card"><div className="font-bold">الهرم الإداري من Manifest</div><pre className="text-[10px] font-mono ltr bg-gray-50 p-2 rounded overflow-auto">{JSON.stringify(manifest?.hierarchy?.slice(0,5)||[], null,2)}</pre></div>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {types.map(t=> <div key={t} className="card text-xs">{t}: {entities.filter((e:any)=>e.raw.entity_type===t).length}</div>)}
          </div>
        </div>
      )}

      {tab==='admin' && (
        <div className="space-y-2">
          {manifest?.hierarchy?.map((h:any,i:number)=>(
            <div key={i} className="card text-xs">
              <div className="font-bold">المستوى {h.level}: {h.entity_type} — {h.local_names?.join('/')} — السلطة: {h.authority_name}</div>
              <div>المقام: {h.denominator ?? '—'} — الحالة: {h.scope_status} — الترخيص: {h.license?.slice(0,80)}</div>
              <div>مصادر: {h.source_ids?.join(', ')}</div>
              <div>ملاحظة: {h.caveat || h.notes || '—'}</div>
            </div>
          ))}
        </div>
      )}

      {tab==='layers' && (
        <div className="space-y-2">
          {coverage.map((c:any)=>(
            <div key={c.id} className="card text-xs">
              <div className="font-bold">{c.raw.layer} — {c.raw.definition?.slice(0,200)}</div>
              <div>المقام: {c.raw.denominator ?? '—'} — مطابق: {c.raw.matched} — غير مطابق: {c.raw.unmatched} — مستبعد: {c.raw.excluded} — ناقص: {c.raw.missing ?? '—'}</div>
              <div>النسبة: {c.raw.coverage_percentage ?? '— (لا تُحسب: '} {c.raw.missing_reason ? `السبب: ${c.raw.missing_reason}` : ''} — مكتمل: {c.raw.complete?'نعم':'لا'}</div>
              <div>المصدر: {c.raw.source_id} — اللقطة: {c.raw.snapshot_id} — الترخيص: {c.raw.license?.slice(0,80)}</div>
              <div className="text-[10px] text-gray-500">{c.raw.notes}</div>
            </div>
          ))}
        </div>
      )}

      {tab==='places' && (
        <div>
          <div className="text-xs text-gray-500 mb-2">فلترة حسب النوع:</div>
          <div className="flex gap-2 flex-wrap mb-4">
            {types.map(t=> <Link key={t} href={`/${iso2}?type=${t}`} className="px-2 py-1 border rounded-full text-[10px]">{t}</Link>)}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
            {entities.slice(0,200).map((e:any)=>(
              <Link key={e.id} href={`/${iso2}/${e.id}`} className="card text-xs">
                <div className="font-bold">{e.canonicalName}</div>
                <div className="font-mono ltr text-[10px]">{e.id}</div>
                <div>{e.raw.entity_type} — {e.status} — {e.raw.confidence}</div>
                <div className="text-[10px] text-gray-500">{e.raw.notes?.slice(0,80)}</div>
              </Link>
            ))}
          </div>
          <div className="text-xs mt-2">عرض 200 من {entities.length} — استخدم البحث للوصول للباقي</div>
        </div>
      )}

      {tab==='sources' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {sources.map((s:any)=>(
            <div key={s.id} className="card text-xs">
              <div className="font-bold">{s.raw.title}</div>
              <div className="font-mono ltr text-[10px]">{s.id} — {s.raw.quality_tier} — {s.raw.source_type}</div>
              <div>الترخيص: {s.raw.license?.slice(0,100)}</div>
              <div>locator: {s.raw.locator}</div>
            </div>
          ))}
        </div>
      )}

      {tab==='coverage' && (
        <div className="space-y-2">
          {coverage.filter(c=>!c.raw.complete).map((c:any)=>(
            <div key={c.id} className="card bg-orange-50 border-orange-200 text-xs">
              <div className="font-bold">قيود طبقة {c.raw.layer}</div>
              <div>missing_reason: {c.raw.missing_reason || '—'}</div>
              <div>notes: {c.raw.notes}</div>
            </div>
          ))}
          {coverage.filter(c=>!c.raw.complete).length===0 && <div className="card">جميع الطبقات لهذه الدولة مكتملة حسب تعريف المقام المؤرخ.</div>}
        </div>
      )}

      {tab==='raw' && (
        <div className="space-y-2">
          <div className="card"><div className="font-bold text-xs">Manifest Raw</div><pre className="text-[10px] font-mono ltr bg-gray-50 p-2 rounded overflow-auto max-h-96">{JSON.stringify(manifest, null,2)}</pre></div>
          <div className="card"><div className="font-bold text-xs">Country Entity Raw</div><pre className="text-[10px] font-mono ltr bg-gray-50 p-2 rounded overflow-auto max-h-96">{JSON.stringify(countryEnt?.raw, null,2)}</pre></div>
        </div>
      )}
    </div>
  );
}
