'use client';
import { useEffect, useState } from 'react';
import { db } from '@/data/db';
import Link from 'next/link';

const REGIONAL_GROUPS: Record<string, string[]> = {
  'شبه الجزيرة العربية': ['YE','SA','AE','OM','QA','BH','KW'],
  'الهلال الخصيب': ['IQ','JO','PS','SY','LB'],
  'وادي النيل': ['EG','SD'],
  'المغرب العربي': ['LY','TN','DZ','MA','MR'],
  'القرن الإفريقي والمحيط الهندي': ['SO','DJ','KM']
};

export default function CountriesPage() {
  const [countries, setCountries] = useState<any[]>([]);
  const [stats, setStats] = useState<Record<string, any>>({});

  useEffect(() => {
    (async () => {
      const countryEnts = await db.entities.where('entityType').equals('country').toArray();
      const allEnts = await db.entities.toArray();
      const coverage = await db.coverage.toArray();
      const claims = await db.claims.toArray();
      const sources = await db.sources.toArray();
      const snapshots = await db.snapshots.toArray();

      const statsMap: Record<string, any> = {};
      for (const c of countryEnts) {
        const code = c.countryCode;
        statsMap[code] = {
          entities: allEnts.filter(e=>e.countryCode===code).length,
          claims: claims.filter(cl=> {
            const subj = allEnts.find(e=>e.id===cl.subjectId);
            return subj?.countryCode===code;
          }).length,
          coverage: coverage.filter(co=>co.countryCode===code),
          completeLayers: coverage.filter(co=>co.countryCode===code && co.raw.complete).length,
          snapshots: snapshots.filter(s=> s.raw.scope?.includes(code) || s.raw.id.includes(code)).length
        };
      }
      setCountries(countryEnts);
      setStats(statsMap);
    })();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">الدول العربية الـ22</h1>
      <p className="text-gray-600">كل دولة تعرض عدد الكيانات، المعلومات، المصادر، حالة التغطية، وآخر لقطة — بدون نسبة اكتمال مصطنعة للدولة كاملة، بل لكل طبقة على حدة.</p>

      {Object.entries(REGIONAL_GROUPS).map(([group, codes]) => (
        <div key={group}>
          <h2 className="text-xl font-bold mb-3">{group}</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {codes.map(code => {
              const ent = countries.find(c=>c.countryCode===code);
              const st = stats[code];
              if (!ent) return <div key={code} className="card opacity-50"><div className="font-bold">{code}</div><div className="text-xs">جاري التحميل أو غير موجود في DB</div></div>;
              return (
                <Link key={code} href={`/${code}`} className="card hover:border-green-400">
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-bold text-lg">{ent.canonicalName}</div>
                      <div className="text-xs font-mono ltr">{code} — {ent.id}</div>
                    </div>
                    <div className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">{st?.completeLayers || 0} طبقة مكتملة</div>
                  </div>
                  <div className="mt-3 grid grid-cols-3 gap-2 text-xs">
                    <div>كيانات: {st?.entities||0}</div>
                    <div>معلومات: {st?.claims||0}</div>
                    <div>تغطية: {st?.coverage?.length||0}</div>
                  </div>
                  <div className="text-xs text-gray-500 mt-2">تغطية: {st?.coverage?.map((c:any)=>c.raw.layer).slice(0,3).join(', ')}...</div>
                </Link>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
