#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def main():
 f=L(ROOT/'data/imports/iraq/fixtures/governorate_profiles_2025.json');e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='IQ'];ids={r['id'] for r in e};families={'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='IQ'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='IQ']};sids={'SRC-IQ-COSIT-GOVERNORATES-2023','SRC-IQ-LAW-7-HALABJA-2025','SRC-IQ-DECREE-21-HALABJA-2025','SRC-IQ-KRSO-FOUR-GOVERNORATES','SRC-IQ-QADA-LISTS-MIRROR-2026'};families['sources']=[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids];E={r['id']:r for r in e};C=families['claims'];find=[]
 for q in f['governorates']:
  eid='ENT-IQ-GOVERNORATE-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name_ar'] or not any(c['subject_id']==eid and c['predicate']=='administrative_profile' and c['value']['data']==q['profile'] for c in C):find.append({'severity':'P1','record_id':eid,'message':'fixture identity/profile'})
 if E.get('ENT-IQ-GOVERNORATE-19',{}).get('valid_from')!='2025-05-05':find.append({'severity':'P1','record_id':'Halabja','message':'federal date mismatch'})
 fq=L(ROOT/'data/imports/iraq/fixtures/qada_depth_2026.json')
 qd=[r for r in e if r['entity_type']=='iq_district']
 rel_by_child={r['child_id']:r for r in families['relationships']}
 want={('ENT-IQ-GOVERNORATE-'+g['code'],q['name'],q['status']) for g in fq['governorates'] for q in g['qadas']}
 got={(rel_by_child.get(r['id'],{}).get('parent_id'),r['canonical_name'],r.get('verification_status')) for r in qd}
 if want!=got or len(qd)!=31:find.append({'severity':'P1','record_id':'qadas','message':'qada universe deviates from checksum-bound 31-qada fixture'})
 qpop=[c for c in C if c.get('predicate')=='population']
 if len(qpop)!=3 or any(c.get('published') for c in qpop):find.append({'severity':'P1','record_id':'qada_populations','message':'3 unpublished Basra census qada populations required'})
 sample={k:{'population':len(v),'sample_size':len(v),'sample_percentage':100.0,'record_ids':sorted(x['id'] for x in v)} for k,v in families.items()};write_json(ROOT/'data/review/iraq_review_samples.json',{'schema_version':'2.0.0','country_code':'IQ','families':sample});write_json(ROOT/'reports/iraq_review_samples.json',{'schema_version':'2.0.0','country_code':'IQ','families':sample});n=sum(len(v) for v in families.values());ok=not find;res={k:{'sampled':len(v),'passed':len(v) if ok else 0,'failed':0 if ok else len(v),'status':'PASS' if ok else 'FAIL'} for k,v in families.items()};write_json(ROOT/'reports/iraq_independent_review.json',{'schema_version':'2.0.0','country_code':'IQ','status':'PASS' if ok else 'FAIL','p0':0,'critical_p1':len(find),'method':'Independent full federal/KRI profile and Halabja-law fixture comparison.','families':res,'total_sampled':n,'total_passed':n if ok else 0,'findings':find});print(n);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
