'use client';
import { useEffect, useState } from 'react';
import { db } from '@/data/db';

export default function CoveragePage() {
  const [coverage, setCoverage] = useState<any[]>([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    (async () => {
      const cov = await db.coverage.toArray();
      setCoverage(cov.sort((a,b)=> a.countryCode.localeCompare(b.countryCode) || a.raw.layer.localeCompare(b.raw.layer)));
    })();
  }, []);

  const filtered = coverage.filter(c => !filter || c.countryCode===filter);

  const countries = Array.from(new Set(coverage.map(c=>c.countryCode))).sort();

  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">التغطية والقيود — 112 طبقة</h1>
      <p className="text-sm text-gray-600">كل نسبة 100% مقيدة بالدولة والطبقة والمقام المؤرخ واللقطة والمصدر. لا ننقل النسبة إلى بلد كامل. إذا coverage_percentage=null نعرض missing_reason.</p>

      <div className="flex gap-2 flex-wrap">
        <button onClick={()=>setFilter('')} className={`px-3 py-1 rounded-full text-xs border ${!filter?'bg-black text-white':''}`}>الكل</button>
        {countries.map(cc=> <button key={cc} onClick={()=>setFilter(cc)} className={`px-3 py-1 rounded-full text-xs border ${filter===cc?'bg-black text-white':''}`}>{cc}</button>)}
      </div>

      <div className="overflow-auto border rounded-xl">
        <table className="min-w-full text-xs">
          <thead className="bg-gray-50">
            <tr>
              <th className="p-2 text-right">الدولة</th>
              <th className="p-2 text-right">الطبقة</th>
              <th className="p-2">المقام</th>
              <th className="p-2">مطابق</th>
              <th className="p-2">مستبعد</th>
              <th className="p-2">النسبة</th>
              <th className="p-2">مكتمل</th>
              <th className="p-2">missing_reason</th>
              <th className="p-2">المصدر</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((c:any)=>(
              <tr key={c.id} className="border-t hover:bg-gray-50">
                <td className="p-2 font-mono">{c.countryCode}</td>
                <td className="p-2">{c.raw.layer}</td>
                <td className="p-2">{c.raw.denominator ?? '—'}</td>
                <td className="p-2">{c.raw.matched}</td>
                <td className="p-2">{c.raw.excluded}</td>
                <td className="p-2">{c.raw.coverage_percentage != null ? `${c.raw.coverage_percentage}%` : '—'}</td>
                <td className="p-2">{c.raw.complete ? '✅' : '❌'}</td>
                <td className="p-2 text-[10px]">{c.raw.missing_reason || c.raw.notes?.slice(0,100) || '—'}</td>
                <td className="p-2 font-mono text-[10px]">{c.raw.source_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="text-xs text-gray-500">العدد: {filtered.length} / {coverage.length}</div>
    </div>
  );
}
