'use client';
import { useEffect, useState } from 'react';
import { db } from '@/data/db';
import Link from 'next/link';

export default function SourcesPage() {
  const [sources, setSources] = useState<any[]>([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    (async () => {
      const srcs = await db.sources.toArray();
      setSources(srcs.sort((a,b)=> a.raw.quality_tier.localeCompare(b.raw.quality_tier)));
    })();
  }, []);

  const filtered = sources.filter(s => !filter || s.qualityTier===filter);

  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">المصادر — 151 مصدر ذري</h1>
      <p className="text-sm text-gray-600">كل مصدر ملف JSON ذري، مع quality_tier, license, locator, checksum. لا يوجد مصدر بدون locator.</p>

      <div className="flex gap-2">
        {['','A','B','C','D'].map(t=> <button key={t} onClick={()=>setFilter(t)} className={`px-3 py-1 rounded-full text-xs border ${filter===t?'bg-black text-white':''}`}>{t||'الكل'}</button>)}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((s:any)=>(
          <div key={s.id} className="card text-xs">
            <div className="flex justify-between">
              <div className="font-bold text-sm">{s.raw.title}</div>
              <div className="badge badge-verified">{s.qualityTier}</div>
            </div>
            <div className="font-mono ltr text-[10px]">{s.id}</div>
            <div>الناشر: {s.raw.publisher || '—'} — النوع: {s.raw.source_type}</div>
            <div>الترخيص: {s.raw.license?.slice(0,80) || '—'}</div>
            <div>تاريخ النشر: {s.raw.publication_date || '—'} — الاسترجاع: {s.raw.retrieved_at || '—'}</div>
            <div className="mt-2 flex gap-2">
              {s.raw.url && <a href={s.raw.url} target="_blank" className="text-blue-600 underline">URL</a>}
              {s.raw.archive_url && <a href={s.raw.archive_url} target="_blank" className="text-green-600 underline">Archive</a>}
            </div>
            <div className="text-[10px] text-gray-500 mt-1">locator: {s.raw.locator} — checksum: {s.raw.checksum?.slice(0,16)}</div>
            <Link href={`/sources/${s.id}`} className="text-blue-600 text-xs mt-2 block">التفاصيل + الكيانات التي تستخدمه</Link>
          </div>
        ))}
      </div>
    </div>
  );
}
