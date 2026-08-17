#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='KM'];ids={r['id'] for r in e};sids={'SRC-KM-LAW-11-006-AU-2011','SRC-KM-INSEED-RGPH17-ADMIN','SRC-UNESCO-WHC-KM-1768-2026'}
 return {'entities':e,'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='KM'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='KM'],'manifest':L(ROOT/'manifests/KM.yml')}
def validate(d):
 f=L(ROOT/'data/imports/comoros/fixtures/current_hierarchy_2026.json');E={r['id']:r for r in d['entities']};R=d['relationships'];err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 cnt={t:sum(r['entity_type']==t for r in E.values()) for t in ['country','km_island','km_prefecture','km_commune','cultural_site']}
 if cnt!={'country':1,'km_island':3,'km_prefecture':16,'km_commune':54,'cultural_site':1}:x('KM_COUNTS','entities',str(cnt))
 for island in f['islands']:
  iid='ENT-KM-ISLAND-'+island['token']
  for p in island['prefectures']:
   pid='ENT-KM-PREFECTURE-'+p['token']
   if not any(r['child_id']==pid and r['parent_id']==iid for r in R):x('KM_PREFECTURE_PARENT',pid,'island parent')
   for q in p['communes']:
    cid='ENT-KM-COMMUNE-'+q['token']
    if E.get(cid,{}).get('canonical_name')!=q['name'] or not any(r['child_id']==cid and r['parent_id']==pid for r in R):x('KM_COMMUNE_PARENT',cid,'prefecture parent')
 if any('MAYOTTE' in r['id'] or r.get('canonical_name')=='Mayotte' for r in E.values()):x('KM_MAYOTTE_CURRENT','entities','Mayotte excluded')
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-KM-COUNTRY-SCOPE':1,'DEN-KM-ISLANDS':3,'DEN-KM-PREFECTURES':16,'DEN-KM-COMMUNES':54,'DEN-KM-WHC':1}:x('KM_DENOMINATORS','den','1/3/16/54/1')
 w='ENT-KM-CULTURAL-SITE-HISTORIC-SULTANATES-MEDINAS'
 if w not in E or not any(c['subject_id']==w and c['predicate']=='world_heritage_inscription_year' and c['value']['data']==2026 for c in d['claims']):x('KM_WHC_2026',w,'current inscription')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/comoros_validation.json',{'schema_version':'2.0.0','country_code':'KM','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
