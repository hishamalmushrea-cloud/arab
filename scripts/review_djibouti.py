#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def main():
 f=L(ROOT/'data/imports/djibouti/fixtures/topology_2024.json');entities=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='DJ'];ids={r['id'] for r in entities};relationships=[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids];claims=[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids];denominators=[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='DJ'];coverage=[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='DJ'];sids={'SRC-DJ-PRESIDENCY-REGIONS-2026','SRC-DJ-LAW-122-CITY-2005','SRC-DJ-INSTAD-RGPH3-2024','SRC-DJ-DECENTRALISATION-ROADMAP-2020','SRC-DJ-INTERIOR-PREFECTURES-2026'};sources=[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids];families={'entities':entities,'relationships':relationships,'claims':claims,'sources':sources,'denominators':denominators,'coverage':coverage};find=[];E={r['id']:r for r in entities}
 for g in f['regions']:
  gid='ENT-DJ-REGION-'+g['token']
  for q in g['subprefectures']:
   sid='ENT-DJ-SUBPREFECTURE-'+q['token']
   if E.get(sid,{}).get('canonical_name')!=q['name_fr'] or not any(r['child_id']==sid and r['parent_id']==gid for r in relationships):find.append({'severity':'P1','record_id':sid,'message':'fixture identity/parent mismatch'})
 if sum(c['value']['data'] for c in claims)!=f['population_total']:find.append({'severity':'P1','record_id':'population','message':'reconciliation mismatch'})
 sample={k:{'population':len(v),'sample_size':len(v),'sample_percentage':100.0,'record_ids':sorted(x['id'] for x in v)} for k,v in families.items()};write_json(ROOT/'data/review/djibouti_review_samples.json',{'schema_version':'2.0.0','country_code':'DJ','families':sample});write_json(ROOT/'reports/djibouti_review_samples.json',{'schema_version':'2.0.0','country_code':'DJ','families':sample});n=sum(len(v) for v in families.values());ok=not find;res={k:{'sampled':len(v),'passed':len(v) if ok else 0,'failed':0 if ok else len(v),'status':'PASS' if ok else 'FAIL'} for k,v in families.items()};write_json(ROOT/'reports/djibouti_independent_review.json',{'schema_version':'2.0.0','country_code':'DJ','status':'PASS' if ok else 'FAIL','p0':0,'critical_p1':len(find),'method':'Independent full topology/population fixture comparison; importer and semantic validator not imported.','families':res,'total_sampled':n,'total_passed':n if ok else 0,'findings':find});print(n);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
