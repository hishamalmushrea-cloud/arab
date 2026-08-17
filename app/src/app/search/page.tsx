'use client';
import { useState, useEffect } from 'react';
import { searchEntities, buildSearchIndex } from '@/data/search';
import Link from 'next/link';
import { db } from '@/data/db';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [indexReady, setIndexReady] = useState(false);

  useEffect(() => {
    buildSearchIndex().then(()=>setIndexReady(true));
  }, []);

  useEffect(() => {
    if (!indexReady) return;
    const t = setTimeout(async () => {
      setLoading(true);
      try {
        const res = await searchEntities(query);
        // enrich with entities
        const enriched = await Promise.all(res.map(async (r:any) => {
          const ent = await db.entities.get(r.item.id);
          return { ...r, entity: ent };
        }));
        setResults(enriched);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }, 300);
    return () => clearTimeout(t);
  }, [query, indexReady]);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">البحث الشامل</h1>
      <p className="text-gray-600 text-sm">يبحث في: الاسم الرسمي، الاسم البديل (عربي/إنجليزي/تاريخي/محلي)، النوع، الدولة. مثال: ابحث عن "مقشن" حتى لو كان Alias.</p>

      <div className="flex gap-2">
        <input value={query} onChange={e=>setQuery(e.target.value)} placeholder="ابحث مثل: مقشن، الرياض، حلبجة، طرابلس" className="flex-1 border border-gray-300 rounded-xl px-4 py-3 text-lg" />
        <Link href="/" className="px-4 py-3 border rounded-xl">الرئيسية</Link>
      </div>

      {!indexReady && <div className="text-sm text-gray-500">جاري بناء فهرس البحث Offline من 5317 كيان + 3261 اسم بديل...</div>}
      {loading && <div className="text-sm">جاري البحث...</div>}

      <div className="text-sm text-gray-500">{results.length} نتيجة {query && `لـ "${query}"`}</div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {results.map((r:any) => (
          <Link key={r.item.id} href={`/${r.entity?.countryCode || 'XX'}/${r.item.id}`} className="card">
            <div className="font-bold">{r.item.canonicalName}</div>
            <div className="text-xs font-mono ltr">{r.item.id} — score {r.score?.toFixed(3)}</div>
            <div className="text-xs mt-1">النوع: {r.entity?.raw.entity_type} — الدولة: {r.entity?.countryCode} — الحالة: {r.entity?.status}</div>
            {r.item.aliases?.length>0 && <div className="text-xs text-gray-500 mt-1">أسماء بديلة: {r.item.aliases.slice(0,3).join(', ')}</div>}
          </Link>
        ))}
      </div>

      {query && results.length===0 && !loading && <div className="text-center py-12 text-gray-500">لا توجد نتائج لـ "{query}". جرب بدون تشكيل أو جرب اسم بديل.</div>}
    </div>
  );
}
