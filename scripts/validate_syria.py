#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='SY'];ids={r['id'] for r in e};sids={'SRC-SY-SIA-ADMIN-DIVISIONS-2026','SRC-SY-SANA-GOVERNORATE-NAV-2026','SRC-SY-CBS-GOVERNORATES-2010'}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='SY'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='SY'],'manifest':L(ROOT/'manifests/SY.yml')}
def validate(d):
 f=L(ROOT/'data/imports/syria/fixtures/governorates_2026.json');E={r['id']:r for r in d['entities']};C=d['claims'];err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 gov=[r for r in E.values() if r['entity_type']=='sy_governorate']
 if len(E)!=15 or len(gov)!=14:x('SY_COUNTS','entities','country + 14 governorates')
 for q in f['governorates']:
  eid='ENT-SY-GOVERNORATE-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name_ar'] or not any(c['subject_id']==eid and c['predicate']=='administrative_profile' and c['value']['data']==q['profile'] for c in C):x('SY_FIXTURE_PROFILE',eid,'identity/profile mismatch')
 names={r['canonical_name']:r['id'] for r in gov}
 if names.get('دمشق')==names.get('ريف دمشق') or not {'دمشق','ريف دمشق'}<=set(names):x('SY_DAMASCUS_DISTINCTION','entities','Damascus and Rural Damascus distinct')
 den={r['id']:r['value'] for r in d['denominators']};expected={'DEN-SY-COUNTRY-SCOPE':1,'DEN-SY-GOVERNORATES':14,'DEN-SY-DAMASCUS-SPECIAL':1,'DEN-SY-OTHER-GOVERNORATES':13,'DEN-SY-DISTRICTS':68,'DEN-SY-SUBDISTRICTS':227}
 if den!=expected:x('SY_DENOMINATORS','denominators','1/14/1/13/68/227 required')
 if any(r['entity_type'] in {'sy_district','sy_subdistrict'} for r in E.values()):x('SY_PREMATURE_LOWER','entities','lower record layers open')
 if any(r.get('status') in {'de_facto','destroyed','displaced','disputed'} for r in E.values()):x('SY_UNSUPPORTED_OVERLAY','entities','legal identities cannot encode control/condition')
 rel=[r for r in d['relationships'] if r.get('child_id')!='ENT-SY-COUNTRY']
 if len(rel)!=14 or any(r.get('parent_id')!='ENT-SY-COUNTRY' for r in rel):x('SY_PARENT','relationships','14 country parents required')
 cov={r['id']:r for r in d['coverage']}
 if cov.get('COV-SY-GOVERNORATES',{}).get('matched')!=14 or cov.get('COV-SY-GOVERNORATES',{}).get('snapshot_date')!='2026-08-17':x('SY_COVERAGE_FRESHNESS','coverage','14 matched current snapshot')
 for i,n in [('COV-SY-DISTRICTS',68),('COV-SY-SUBDISTRICTS',227)]:
  r=cov.get(i,{})
  if r.get('matched')!=0 or r.get('unmatched')!=n or r.get('missing')!=n or r.get('complete') is not False:x('SY_OPEN_LOWER',i,'known denominator must remain open 0/n')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','aliases','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/syria_validation.json',{'schema_version':'2.0.0','country_code':'SY','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
