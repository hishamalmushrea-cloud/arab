#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='DJ'];ids={r['id'] for r in e};sids={'SRC-DJ-PRESIDENCY-REGIONS-2026','SRC-DJ-LAW-122-CITY-2005','SRC-DJ-INSTAD-RGPH3-2024','SRC-DJ-DECENTRALISATION-ROADMAP-2020','SRC-DJ-INTERIOR-PREFECTURES-2026'}
 return {'entities':e,'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='DJ'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='DJ'],'manifest':L(ROOT/'manifests/DJ.yml')}
def validate(d):
 f=L(ROOT/'data/imports/djibouti/fixtures/topology_2024.json');E={r['id']:r for r in d['entities']};R=d['relationships'];C=d['claims'];err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 counts={t:sum(r['entity_type']==t for r in E.values()) for t in ['country','dj_region','djibouti_city','dj_commune','dj_subprefecture']}
 if counts!={'country':1,'dj_region':5,'djibouti_city':1,'dj_commune':3,'dj_subprefecture':13}:x('DJ_COUNTS','entities',str(counts))
 city='ENT-DJ-DJIBOUTI-CITY'
 if not any(r['child_id']==city and r['parent_id']=='ENT-DJ-COUNTRY' for r in R):x('DJ_CITY_PARENT',city,'special city parent')
 for q in f['city']['communes']:
  cid='ENT-DJ-COMMUNE-'+q['token']
  if not any(r['child_id']==cid and r['parent_id']==city for r in R):x('DJ_COMMUNE_PATH',cid,'commune not under city')
 for g in f['regions']:
  gid='ENT-DJ-REGION-'+g['token'];children={r['child_id'] for r in R if r['parent_id']==gid};expected={'ENT-DJ-SUBPREFECTURE-'+q['token'] for q in g['subprefectures']}
  if children!=expected:x('DJ_SUBPREFECTURE_PATH',gid,'regional child set')
  if not any(c['subject_id']==gid and c['predicate']=='population' and c['value']['data']==g['population'] for c in C):x('DJ_POPULATION',gid,'RGPH population')
 if not any(c['subject_id']==city and c['value']['data']==f['city_population'] for c in C):x('DJ_POPULATION',city,'city population')
 if sum(c['value']['data'] for c in C)!=f['population_total']:x('DJ_POP_RECONCILIATION','claims','national total')
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-DJ-COUNTRY-SCOPE':1,'DEN-DJ-REGIONS':5,'DEN-DJ-SPECIAL-CITY':1,'DEN-DJ-CITY-COMMUNES':3,'DEN-DJ-SUBPREFECTURES':13}:x('DJ_DENOMINATORS','den','1/5/1/3/13')
 if len(R)!=22 or len(C)!=6:x('DJ_RECORD_COUNTS','DJ','22 rel/6 claims')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/djibouti_validation.json',{'schema_version':'2.0.0','country_code':'DJ','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
