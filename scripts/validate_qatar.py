#!/usr/bin/env python3
import json,hashlib
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='QA'];ids={r['id'] for r in e};sids={'SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020','SRC-QA-QNMP-EIGHT-MUNICIPALITIES-2026','SRC-UNESCO-WHC-QA-1402'}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='QA'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='QA'],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'manifest':L(ROOT/'manifests/QA.yml')}
def validate(d):
 f=L(ROOT/'data/imports/qatar/fixtures/municipalities_census_2020.json');exp={r['name_ar']:(r['name_en'],r['population']) for r in f['records']};E={r['id']:r for r in d['entities']};municip={r['canonical_name']:r for r in E.values() if r['entity_type']=='qa_municipality'};err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 if set(E)!={'ENT-QA-COUNTRY',*(r['id'] for r in E.values() if r['entity_type']=='qa_municipality'),'ENT-QA-ARCHAEOLOGICAL-SITE-AL-ZUBARAH'} or len(E)!=10:x('QA_ENTITY_UNIVERSE','entities','expected country+8 municipalities+Al Zubarah')
 if set(municip)!=set(exp):x('QA_MUNICIPALITY_SET','municipalities','eight-name mismatch')
 for ar,(en,pop) in exp.items():
  r=municip.get(ar,{});eid=r.get('id');
  if not eid:continue
  if not any(a['entity_id']==eid and a['name']==en for a in d['aliases']):x('QA_ALIAS',eid,'alias mismatch')
  if not any(q['child_id']==eid and q['parent_id']=='ENT-QA-COUNTRY' and q['relationship_type']=='administrative_parent' for q in d['relationships']):x('QA_WRONG_PARENT',eid,'wrong parent')
  if not any(c['subject_id']==eid and c['predicate']=='population' and c['value']['data']==pop and c['observed_at']=='2020-12-31' for c in d['claims']):x('QA_POPULATION',eid,'population mismatch')
 if len(d['aliases'])!=9 or len(d['relationships'])!=9 or len(d['claims'])!=10:x('QA_COUNTS','QA','expected 9/9/10')
 for c in d['claims']:
  if c['predicate'].startswith('lexical_'):x('QA_DIALECT',c['id'],'unsupported')
  if c['subject_id'] in {r.get('id') for r in municip.values()} and c['predicate']!='population':x('QA_CITY_LEAKAGE',c['id'],'non-population municipality claim')
 if {r['id'] for r in d['sources']}!={'SRC-QA-PSA-CENSUS-MUNICIPALITIES-2020','SRC-QA-QNMP-EIGHT-MUNICIPALITIES-2026','SRC-UNESCO-WHC-QA-1402'}:x('QA_SOURCES','sources','source set')
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-QA-COUNTRY-SCOPE':1,'DEN-QA-MUNICIPALITIES-2020':8,'DEN-QA-WHC-20260816':1}:x('QA_DENOMINATORS','den','1/8/1 expected')
 m=d['manifest'];g=next(q for q in m['hierarchy'] if q['entity_type']=='qa_municipality')
 if g.get('denominator')!=8 or g.get('scope_status')!='closed':x('QA_MANIFEST','manifest','municipal scope')
 for t in ['qa_zone','qa_district']:
  q=next(z for z in m['hierarchy'] if z['entity_type']==t)
  if q.get('denominator') is not None or q.get('scope_status')!='unavailable':x('QA_LOWER_LAYER',t,'invented lower layer')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','aliases','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/qatar_validation.json',{'schema_version':'2.0.0','country_code':'QA','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
