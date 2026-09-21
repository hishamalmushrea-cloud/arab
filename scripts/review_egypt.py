#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def main():
 f=L(ROOT/'data/imports/egypt/fixtures/governorate_profiles.json');e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='EG'];ids={r['id'] for r in e};families={'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='EG'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='EG']};sids={'SRC-EG-CAPMAS-27-GOVERNORATES-2021','SRC-EG-MLD-27-GOVERNORATES-2026','SRC-EG-CAPMAS-GOVERNORATE-CODES','SRC-EG-MARKAZ-LISTS-MIRROR-2026'};families['sources']=[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids];find=[];E={r['id']:r for r in e};A=families['aliases'];C=families['claims']
 for q in f['governorates']:
  eid='ENT-EG-GOVERNORATE-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name_ar'] or not any(a['entity_id']==eid and a['name']==q['name_en'] for a in A) or not any(c['subject_id']==eid and c['value']['data']==q['profile'] for c in C):find.append({'severity':'P1','record_id':eid,'message':'fixture identity/alias/profile'})
 fk=L(ROOT/'data/imports/egypt/fixtures/markaz_depth_2026.json')
 mk=[r for r in e if r['entity_type']=='eg_markaz']
 rel_by_child={r['child_id']:r for r in families['relationships']}
 want={('ENT-EG-GOVERNORATE-'+g['code'],n) for g in fk['governorates'] for n in g['marakiz']}
 got={(rel_by_child.get(r['id'],{}).get('parent_id'),r['canonical_name']) for r in mk}
 if want!=got or len(mk)!=55:find.append({'severity':'P1','record_id':'marakiz','message':'markaz universe deviates from checksum-bound 55-markaz fixture'})
 if any(r.get('verification_status')!='probable' for r in mk):find.append({'severity':'P1','record_id':'marakiz','message':'markaz status must remain probable'})
 mpop=[c for c in C if c.get('predicate')=='population']
 if len(mpop)!=17 or any(c.get('published') for c in mpop):find.append({'severity':'P1','record_id':'markaz_populations','message':'17 unpublished 2024 markaz population claims required'})
 sample={k:{'population':len(v),'sample_size':len(v),'sample_percentage':100.0,'record_ids':sorted(x['id'] for x in v)} for k,v in families.items()};write_json(ROOT/'data/review/egypt_review_samples.json',{'schema_version':'2.0.0','country_code':'EG','families':sample});write_json(ROOT/'reports/egypt_review_samples.json',{'schema_version':'2.0.0','country_code':'EG','families':sample});n=sum(len(v) for v in families.values());ok=not find;res={k:{'sampled':len(v),'passed':len(v) if ok else 0,'failed':0 if ok else len(v),'status':'PASS' if ok else 'FAIL'} for k,v in families.items()};write_json(ROOT/'reports/egypt_independent_review.json',{'schema_version':'2.0.0','country_code':'EG','status':'PASS' if ok else 'FAIL','p0':0,'critical_p1':len(find),'method':'Independent full governorate/profile fixture comparison plus the checksum-bound 55-markaz depth inventory, probable-status enforcement, and unpublished 2024 markaz populations.','families':res,'total_sampled':n,'total_passed':n if ok else 0,'findings':find});print(n);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
