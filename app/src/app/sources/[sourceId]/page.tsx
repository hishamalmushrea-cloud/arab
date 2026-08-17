'use client';
import { useEffect, useState } from 'react';
import { db } from '@/data/db';
import Link from 'next/link';

export default function SourceDetailPage({ params }: { params: { sourceId: string } }) {
  const sourceId = decodeURIComponent(params.sourceId);
  const [source, setSource] = useState<any>(null);
  const [entities, setEntities] = useState<any[]>([]);
  const [claims, setClaims] = useState<any[]>([]);

  useEffect(() => {
    (async () => {
      const s = await db.sources.get(sourceId);
      setSource(s || null);
      const ents = await db.entities.toArray();
      const relatedEnts = ents.filter((e:any)=> e.raw.canonical_source_id===sourceId);
      setEntities(relatedEnts);
      const cls = await db.claims.where('subjectId').equals(sourceId).toArray(); // wrong, claims where sourceId==sourceId
      const allClaims = await db.claims.toArray();
      setClaims(allClaims.filter((c:any)=> c.raw.source_id===sourceId || c.raw.second_source_id===sourceId));
    })();
  }, [sourceId]);

  if (!source) return <div className="p-8">جاري تحميل المصدر {sourceId}... <Link href="/sources" className="text-blue-600 underline">رجوع</Link></div>;

  return (
    <div className="space-y-6">
      <div className="text-sm text-gray-500"><Link href="/sources" className="hover:underline">المصادر</Link> / {sourceId}</div>
      <div className="bg-white border rounded-xl p-6">
        <h1 className="text-2xl font-bold">{source.raw.title}</h1>
        <div className="text-xs font-mono ltr">{source.id}</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-4 text-sm">
          <div>الناشر: {source.raw.publisher || '—'}</div>
          <div>المنظمة: {source.raw.organization || '—'}</div>
          <div>النوع: {source.raw.source_type}</div>
          <div>الجودة: {source.raw.quality_tier}</div>
          <div>اللغة: {source.raw.language || '—'}</div>
          <div>البلدان: {source.raw.country_codes?.join(', ') || '—'}</div>
          <div>تاريخ النشر: {source.raw.publication_date || '—'}</div>
          <div>تاريخ الاسترجاع: {source.raw.retrieved_at || '—'}</div>
          <div className="md:col-span-2">الترخيص: {source.raw.license || '—'}</div>
          <div className="md:col-span-2">locator: {source.raw.locator || '—'}</div>
          <div className="md:col-span-2">notes: {source.raw.notes || '—'}</div>
          <div>checksum: {source.raw.checksum || '—'}</div>
        </div>
        <div className="flex gap-2 mt-4">
          {source.raw.url && <a href={source.raw.url} target="_blank" className="bg-blue-600 text-white px-4 py-2 rounded text-xs">فتح URL (إنترنت)</a>}
          {source.raw.archive_url && <a href={source.raw.archive_url} target="_blank" className="bg-green-600 text-white px-4 py-2 rounded text-xs">Archive</a>}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="card"><div className="font-bold">كيانات تستخدم هذا المصدر كـ canonical ({entities.length})</div><div className="space-y-1 mt-2 max-h-96 overflow-auto">{entities.slice(0,100).map((e:any)=> <Link key={e.id} href={`/${e.countryCode}/${e.id}`} className="block text-xs hover:bg-gray-50 border-b py-1"><span className="font-bold">{e.canonicalName}</span> <span className="font-mono ltr text-[10px]">{e.id}</span></Link>)}</div></div>
        <div className="card"><div className="font-bold">Claims تستخدم هذا المصدر ({claims.length})</div><div className="space-y-1 mt-2 max-h-96 overflow-auto">{claims.slice(0,100).map((c:any)=> <div key={c.id} className="text-xs border-b py-1"><span className="font-bold">{c.raw.predicate}</span> {JSON.stringify(c.raw.value?.data).slice(0,80)} <span className="font-mono ltr text-[10px]">{c.id}</span></div>)}</div></div>
      </div>

      <div className="card"><div className="font-bold text-xs">Raw JSON</div><pre className="text-[10px] font-mono ltr bg-gray-50 p-2 rounded overflow-auto max-h-96">{JSON.stringify(source.raw, null,2)}</pre></div>
    </div>
  );
}
