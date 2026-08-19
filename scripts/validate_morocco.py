#!/usr/bin/env python3
import json
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='MA'];ids={r['id'] for r in e};sids={'SRC-MA-DGCT-DECREE-2-15-10','SRC-MA-DGCT-TERRITORIAL-COUNTS-2026','SRC-MA-HCP-RGPH-2024','SRC-MA-CULTURE-MIRROR-2026'}
 return {'entities':e,'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='MA'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='MA'],'manifest':L(ROOT/'manifests/MA.yml')}
def validate(d):
 f=L(ROOT/'data/imports/morocco/fixtures/territorial_division_2015.json');E={r['id']:r for r in d['entities']};R=d['relationships'];C=d['claims'];err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 cnt={t:sum(r['entity_type']==t for r in E.values()) for t in ['country','ma_region','ma_prefecture','ma_province','ma_commune']}
 if cnt!={'country':1,'ma_region':12,'ma_prefecture':13,'ma_province':62,'ma_commune':0}:x('MA_COUNTS','entities',str(cnt))
 for g in f['regions']:
  gid='ENT-MA-REGION-'+g['token'];children={r['child_id'] for r in R if r['parent_id']==gid};expected={('ENT-MA-PREFECTURE-' if q['entity_type']=='ma_prefecture' else 'ENT-MA-PROVINCE-')+q['token'] for q in g['children']}
  if children!=expected:x('MA_PARENT_SET',gid,'second-level set')
  claim=next((c for c in C if c['subject_id']==gid),None);expected_count={'ma_prefecture':sum(q['entity_type']=='ma_prefecture' for q in g['children']),'ma_province':sum(q['entity_type']=='ma_province' for q in g['children'])}
  if not claim or claim['value']['data']!=expected_count:x('MA_COUNT_CLAIM',gid,'split count')
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-MA-COUNTRY-SCOPE':1,'DEN-MA-REGIONS':12,'DEN-MA-PREFECTURES':13,'DEN-MA-PROVINCES':62}:x('MA_DENOMINATORS','den','1/12/13/62')
 if len(R)!=87 or len(C)!=29:x('MA_RECORD_COUNTS','MA','87/29')
 depth=[c for c in C if c.get('predicate') in {'language_presence','dialect_profile','food_dish','clothing_item'}]
 if len(depth)!=17 or any(c.get('published') for c in depth):x('MA_DEPTH_UNPUBLISHED','claims','17 unpublished cultural depth claims')
 langs=[c for c in depth if c['predicate']=='language_presence']
 if len(langs)!=4 or any(c.get('verification_status')!='probable' for c in langs):x('MA_DEPTH_LANGS','claims','4 probable language-presence claims')
 rest=[c for c in depth if c['predicate']!='language_presence']
 if any(c.get('verification_status')!='local_reported' or not c.get('classification') for c in rest):x('MA_DEPTH_STATUS','claims','dialect/dish/dress stay local_reported with explicit classification')
 cous=next((c for c in depth if c['predicate']=='food_dish' and c['value']['data'].get('name')=='الكسكس'),None)
 if not cous or cous.get('classification')!='shared':x('MA_COUSCOUS_SHARED','claims','couscous must stay shared via the quadripartite UNESCO file')
 if any(r['entity_type']=='ma_commune' for r in E.values()):x('MA_PREMATURE_COMMUNE','entities','communes deferred')
 q=next(r for r in d['manifest']['hierarchy'] if r['entity_type']=='ma_commune')
 if q.get('scope_status')!='open' or q.get('denominator')!=1503:x('MA_COMMUNE_SCOPE','manifest','known open 1503')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/morocco_validation.json',{'schema_version':'2.0.0','country_code':'MA','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
