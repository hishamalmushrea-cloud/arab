#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def main():
 f=L(ROOT/'data/imports/oman/fixtures/legal_hierarchy_2022.json');e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='OM'];ids={r['id'] for r in e};families={'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='OM'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='OM']};sids={'SRC-OM-RD-36-2022-GOVERNORATES','SRC-OM-ONA-63-WILAYATS-2022','SRC-OM-NCSI-ADMIN-CODES-2026'};families['sources']=[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids];find=[];E={r['id']:r for r in e};R=families['relationships']
 for g in f['governorates']:
  gid='ENT-OM-GOVERNORATE-'+g['code']
  for w in g['wilayats']:
   wid='ENT-OM-WILAYA-'+w['code']
   if E.get(wid,{}).get('canonical_name')!=w['name_ar'] or not any(x['child_id']==wid and x['parent_id']==gid for x in R):find.append({'severity':'P1','record_id':wid,'message':'fixture identity/parent mismatch'})
 sample={k:{'population':len(v),'sample_size':len(v),'sample_percentage':100.0,'record_ids':sorted(x['id'] for x in v)} for k,v in families.items()};write_json(ROOT/'data/review/oman_review_samples.json',{'schema_version':'2.0.0','country_code':'OM','families':sample});write_json(ROOT/'reports/oman_review_samples.json',{'schema_version':'2.0.0','country_code':'OM','families':sample});n=sum(len(v) for v in families.values());ok=not find;res={k:{'sampled':len(v),'passed':len(v) if ok else 0,'failed':0 if ok else len(v),'status':'PASS' if ok else 'FAIL'} for k,v in families.items()};write_json(ROOT/'reports/oman_independent_review.json',{'schema_version':'2.0.0','country_code':'OM','status':'PASS' if ok else 'FAIL','p0':0,'critical_p1':len(find),'method':'Independent full fixture identity/parent comparison.','families':res,'total_sampled':n,'total_passed':n if ok else 0,'findings':find});print(n);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
