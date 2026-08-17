#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p): return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='YE']; ids={r['id'] for r in e}; sids={'SRC-YE-CSO-ADMIN-DEFINITION-LEGACY','SRC-YE-NIC-GOVERNORATES-LEGACY','SRC-YE-LAW-31-SOCOTRA-REPORT-2013'}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='YE'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='YE'],'manifest':L(ROOT/'manifests/YE.yml')}
def validate(d):
 f=L(ROOT/'data/imports/yemen/fixtures/first_level_2026.json'); E={r['id']:r for r in d['entities']}; C=d['claims']; err=[]
 def x(c,l,m): err.append({'code':c,'location':l,'message':m})
 gov=[r for r in E.values() if r['entity_type']=='ye_governorate']; cap=[r for r in E.values() if r['entity_type']=='ye_capital_municipality']
 if len(E)!=23 or len(gov)!=21 or len(cap)!=1: x('YE_COUNTS','entities','country + 21 governorates + 1 capital municipality')
 if cap and (cap[0]['canonical_name']!='أمانة العاصمة' or cap[0]['id']!='ENT-YE-CAPITAL-MUNICIPALITY-01'): x('YE_AMANAT_IDENTITY','Amanat Al Asimah','distinct capital municipality required')
 if any(a.get('entity_id')=='ENT-YE-CAPITAL-MUNICIPALITY-01' and 'محافظة' in a.get('name','') for a in d['aliases']): x('YE_AMANAT_ALIAS','aliases','Amanat cannot be governorate alias')
 for q in f['units']:
  eid='ENT-YE-'+('CAPITAL-MUNICIPALITY' if q['kind']=='capital_municipality' else 'GOVERNORATE')+'-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name_ar'] or not any(c['subject_id']==eid and c['predicate']=='administrative_profile' and c['value']['data']==q['kind'] for c in C): x('YE_FIXTURE_IDENTITY',eid,'fixture identity/profile mismatch')
 soc=E.get('ENT-YE-GOVERNORATE-22',{}); law=next((c for c in C if c.get('subject_id')==soc.get('id') and c.get('predicate')=='establishment_instrument'),None)
 if soc.get('valid_from')!='2013-12-18' or not law or law['value']['data'].get('law_number')!=31 or law['value']['data'].get('effective_clause_verified') is not False: x('YE_SOCOTRA_LAW','Socotra','Law 31/2013 issuance and unverified effective clause required')
 expected={'DEN-YE-COUNTRY-SCOPE':1,'DEN-YE-FIRST-LEVEL':22,'DEN-YE-GOVERNORATES':21,'DEN-YE-CAPITAL-MUNICIPALITY':1,'DEN-YE-LEGACY-FIRST-LEVEL':21}
 if {r['id']:r['value'] for r in d['denominators']}!=expected: x('YE_DENOMINATORS','denominators','1/22/21/1/21 required')
 if any(r['entity_type'] in {'ye_district','ye_uzla'} for r in E.values()): x('YE_PREMATURE_LOWER','entities','district/uzla deferred')
 if any(r.get('status') in {'de_facto','destroyed','displaced','disputed'} for r in E.values()): x('YE_UNSUPPORTED_OVERLAY','entities','legal list cannot imply conflict overlay')
 rel=[r for r in d['relationships'] if r.get('child_id')!='ENT-YE-COUNTRY']
 if len(rel)!=22 or any(r.get('parent_id')!='ENT-YE-COUNTRY' for r in rel): x('YE_PARENT','relationships','all 22 first-level units parent to country')
 cov={r['id']:r for r in d['coverage']}
 if cov.get('COV-YE-FIRST-LEVEL',{}).get('matched')!=22 or cov.get('COV-YE-FIRST-LEVEL',{}).get('snapshot_date')!='2026-08-17': x('YE_COVERAGE_FRESHNESS','coverage','22 matched at snapshot date')
 return err
def main():
 d=data(); e=validate(d); met={k:len(d[k]) for k in ['entities','aliases','relationships','claims','sources','denominators','coverage']}; write_json(ROOT/'reports/yemen_validation.json',{'schema_version':'2.0.0','country_code':'YE','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e}); print(met); return 0 if not e else 1
if __name__=='__main__': raise SystemExit(main())
