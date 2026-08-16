#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='LB'];ids={r['id'] for r in e};sids={'SRC-LB-CAS-26-DISTRICTS-2019','SRC-LB-MOIM-ADMINISTRATION-2026','SRC-LB-LAW-52-2017'}
 return {'entities':e,'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='LB'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='LB'],'manifest':L(ROOT/'manifests/LB.yml')}
def validate(d):
 f=L(ROOT/'data/imports/lebanon/fixtures/current_hierarchy.json');E={r['id']:r for r in d['entities']};R=d['relationships'];C=d['claims'];err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 if sum(r['entity_type']=='lb_governorate' for r in E.values())!=9 or sum(r['entity_type']=='lb_district' for r in E.values())!=26 or len(E)!=36:x('LB_COUNTS','entities','country+9+26')
 for g in f['current_governorates']:
  gid='ENT-LB-GOVERNORATE-'+g['token'];children={r['child_id'] for r in R if r['parent_id']==gid};expected={'ENT-LB-DISTRICT-'+q['token'] for q in g['districts']}
  if children!=expected:x('LB_PARENT_SET',gid,'district set')
 for name in ['KESERWAN','JBEIL']:
  did='ENT-LB-DISTRICT-'+name;rels=[r for r in R if r['child_id']==did]
  if len(rels)!=1 or rels[0]['parent_id']!='ENT-LB-GOVERNORATE-KESERWAN-JBEIL':x('LB_CURRENT_PARENT',did,'must current new parent only')
  if not any(c['subject_id']==did and c['predicate']=='previous_governorate' and c['value']['data']=='Mount Lebanon' for c in C):x('LB_HISTORICAL_PARENT',did,'historical claim missing')
 vals={c['predicate']:c['value']['data'] for c in C if c['subject_id']=='ENT-LB-COUNTRY'}
 if vals!={'current_governorate_count':9,'survey_governorate_count':8}:x('LB_TEMPORAL_COUNTS','claims',str(vals))
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-LB-COUNTRY-SCOPE':1,'DEN-LB-GOVERNORATES-CURRENT':9,'DEN-LB-DISTRICTS-CURRENT':26,'DEN-LB-GOVERNORATES-SURVEY-2019':8}:x('LB_DENOMINATORS','den','1/9/26/8')
 if any(r['entity_type']=='lb_municipality' for r in E.values()):x('LB_PREMATURE_MUNICIPALITY','entities','deferred')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/lebanon_validation.json',{'schema_version':'2.0.0','country_code':'LB','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
