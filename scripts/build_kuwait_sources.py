#!/usr/bin/env python3
"""Build checksum-bound Kuwait production sources."""
import hashlib,json
from pathlib import Path
from model import ROOT,SCHEMA_VERSION,write_json
IMPORT=ROOT/'data/imports/kuwait'; MANIFEST=IMPORT/'snapshot_manifest.json'; RETRIEVED='2026-08-16'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def digest(p): return 'sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=load(MANIFEST)
 for r in m['records']:
  p=ROOT/r['path']; b=p.read_bytes()
  if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']: raise SystemExit('Kuwait fixture checksum changed: '+r['path'])
 census='data/imports/kuwait/fixtures/census_governorates_2021.json'; whc='data/imports/kuwait/fixtures/world_heritage_scope_2026.json'
 rows=[
 {'id':'SRC-KW-CSB-CENSUS-GOVERNORATES-2021','title':'Kuwait Registration Census 2021 — population by governorate','publisher':'Central Statistical Bureau','source_type':'census','url':'https://census.csb.gov.kw/Census_Gov','archive_url':None,'publication_date':None,'retrieved_at':RETRIEVED,'license':'Kuwait government statistical publication; factual extraction with attribution; reuse terms not stated','language':'ar-en','country_codes':['KW'],'locator':'downloadable Table 1/chart: six governorates, Not Stated row, and total population','checksum':digest(ROOT/census),'quality_tier':'A','notes':'Checksum binds the reconciled exact table fixture. Publication date unavailable. Census index identifies the registration census as 2021; year precision is normalized to 2021-01-01. Differing prominent widgets are excluded; table/chart rows reconcile exactly to total with Not Stated.'},
 {'id':'SRC-KW-CSB-CENSUS-METHODOLOGY-2021','title':'Kuwait Registration Census 2021','publisher':'Central Statistical Bureau','source_type':'official_report','url':'https://census.csb.gov.kw/index','archive_url':None,'publication_date':None,'retrieved_at':RETRIEVED,'license':'Kuwait government statistical publication; factual extraction with attribution; reuse terms not stated','language':'ar','country_codes':['KW'],'locator':'heading and methodology paragraphs identifying the first registration census of Kuwait 2021 and total 4,385,717','checksum':digest(ROOT/census),'quality_tier':'A','notes':'Checksum binds the structured census fixture cross-checked against the official index. Publication date unavailable.'},
 {'id':'SRC-UNESCO-WHC-KW-2026','title':'World Heritage List — Kuwait State Party','publisher':'UNESCO World Heritage Centre','source_type':'institutional_dataset','url':'https://whc.unesco.org/en/statesparties/kw','archive_url':None,'publication_date':None,'retrieved_at':RETRIEVED,'license':'CC BY-SA 3.0 IGO for property descriptions','language':'en','country_codes':['KW'],'locator':'State Party summary: 0 inscribed properties and 6 tentative-list sites','checksum':digest(ROOT/whc),'quality_tier':'A','notes':'Checksum binds exact inscribed/tentative counts. Publication date unavailable on live State Party page; tentative sites are not treated as inscribed.'}
 ]
 expected={r['id'] for r in rows}
 for p in (ROOT/'data/sources').glob('*.json'):
  x=load(p)
  if x.get('country_codes')==['KW'] and x.get('id') not in expected: raise SystemExit('unexpected Kuwait-only source '+x.get('id','?'))
 for r in rows: r['schema_version']=SCHEMA_VERSION; write_json(ROOT/'data/sources'/f"{r['id']}.json",r)
 write_json(IMPORT/'source_catalog.json',{'schema_version':SCHEMA_VERSION,'country_code':'KW','sources':rows})
 print('Materialized 3 Kuwait atomic sources.')
if __name__=='__main__': main()
