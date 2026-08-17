#!/usr/bin/env python3
import hashlib,json
from model import ROOT,read_jsonl,write_json,norm_name
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='LY'];ids={r['id'] for r in e};sids={'SRC-LY-BSC-CENSUS-2006','SRC-LY-LAW-59-2012','SRC-LY-MOLG-MUNICIPALITIES-2026'}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='LY'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='LY'],'manifest':L(ROOT/'manifests/LY.yml')}
def validate(d):
 f=L(ROOT/'data/imports/libya/fixtures/current_municipalities_2026.json');E=d['entities'];R=d['relationships'];err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 cur=[r for r in E if r['entity_type']=='ly_municipality'];hist=[r for r in E if r['entity_type']=='ly_shabiya_historical']
 if len(cur)!=141 or len(hist)!=22 or len(E)!=164:x('LY_COUNTS','entities','country+141+22')
 if {norm_name(r['canonical_name']) for r in cur}!={norm_name(q['name_ar']) for q in f['municipalities']}:x('LY_MUNICIPALITY_SET','entities','exact 141 names')
 if any(r.get('status')!='current' or r.get('canonical_source_id')!='SRC-LY-MOLG-MUNICIPALITIES-2026' for r in cur):x('LY_CURRENT_SEMANTICS','municipalities','source/status')
 if any(r.get('status')!='historical' for r in hist):x('LY_HISTORICAL_SEMANTICS','shabiyat','must historical')
 if any(r.get('parent_id')!='ENT-LY-COUNTRY' for r in R):x('LY_PARENT','relationships','country only')
 if any(r['entity_type']=='ly_mahalla' for r in E):x('LY_PREMATURE_MAHALLA','entities','unavailable')
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-LY-COUNTRY-SCOPE':1,'DEN-LY-CURRENT-MUNICIPALITIES':141,'DEN-LY-HISTORICAL-SHABIYAT-2006':22,'DEN-LY-MAHALLAS':None}:x('LY_DENOMINATORS','den','1/141/22/null')
 c=next(r for r in d['coverage'] if r['id']=='COV-LY-CURRENT-MUNICIPALITIES')
 if c['matched']!=141 or not c['complete'] or c['coverage_percentage']!=100.0:x('LY_CURRENT_COVERAGE','coverage','141/141')
 if any(r.get('status') in {'de_facto','disputed'} for r in cur):x('LY_UNSUPPORTED_OVERLAY','municipalities','no control inference')
 s=next(r for r in d['sources'] if r['id']=='SRC-LY-MOLG-MUNICIPALITIES-2026');expected='sha256:'+hashlib.sha256((ROOT/'data/imports/libya/fixtures/current_municipalities_2026.json').read_bytes()).hexdigest()
 if s.get('checksum')!=expected:x('LY_SOURCE_FRESHNESS','source','checksum')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','aliases','relationships','claims','sources','denominators','coverage']};write_json(ROOT/'reports/libya_validation.json',{'schema_version':'2.0.0','country_code':'LY','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
