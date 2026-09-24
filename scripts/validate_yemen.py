#!/usr/bin/env python3
import hashlib,json
from model import ROOT,read_jsonl,write_json
def L(p): return json.loads(p.read_text(encoding='utf8'))
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='YE']; ids={r['id'] for r in e}; sids={'SRC-YE-CSO-ADMIN-DEFINITION-LEGACY','SRC-YE-NIC-GOVERNORATES-LEGACY','SRC-YE-LAW-31-SOCOTRA-REPORT-2013','SRC-YE-NIC-DISTRICT-CATALOGUE-MIRROR','SRC-YE-CENSUS-2004-LEGACY-FRAME','SRC-YE-NIC-AMANAT-CENSUS-2004','SRC-YE-LANE-PAGES-MIRROR','SRC-YE-CUISINE-PAGES-MIRROR','SRC-YE-DIALECT-PAGES-MIRROR','SRC-YE-DRESS-PAGES-MIRROR','SRC-YE-CRAFTS-MARKETS-MIRROR','SRC-OSM-AMANAT-SECTIONS-2026'}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in sids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='YE'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='YE'],'manifest':L(ROOT/'manifests/YE.yml'),'snapshots':read_jsonl(ROOT/'data/snapshots/snapshots.jsonl')}
def validate(d):
 f=L(ROOT/'data/imports/yemen/fixtures/first_level_2026.json'); fu=L(ROOT/'data/imports/yemen/fixtures/amanat_urban_sections_2026.json'); E={r['id']:r for r in d['entities']}; C=d['claims']; err=[]
 def x(c,l,m): err.append({'code':c,'location':l,'message':m})
 gov=[r for r in E.values() if r['entity_type']=='ye_governorate']; cap=[r for r in E.values() if r['entity_type']=='ye_capital_municipality']; dis=[r for r in E.values() if r['entity_type']=='ye_district']; lanes=[r for r in E.values() if r['entity_type']=='lane']; hays=[r for r in E.values() if r['entity_type']=='neighborhood' and r.get('canonical_source_id')=='SRC-YE-NIC-AMANAT-CENSUS-2004']
 want_sections=sum(len(t['sections']) for t in fu['districts']); secs=[r for r in E.values() if r.get('canonical_source_id')=='SRC-OSM-AMANAT-SECTIONS-2026']
 if len(E)!=463+want_sections or len(gov)!=21 or len(cap)!=1 or len(dis)!=333 or len(lanes)!=104 or len(hays)!=3 or len(secs)!=want_sections: x('YE_COUNTS','entities',f"country + 21 governorates + 1 capital municipality + 333 districts + 3 hays + 104 lanes + {want_sections} attested urban sections")
 fd=L(ROOT/'data/imports/yemen/fixtures/districts_2026.json'); code2eid={q['code']:('ENT-YE-'+('CAPITAL-MUNICIPALITY' if q['kind']=='capital_municipality' else 'GOVERNORATE')+'-'+q['code']) for q in f['units']}
 want={(code2eid[g['code']],n) for g in fd['governorates'] for n in g['districts']}
 rel_by_child={r['child_id']:r for r in d['relationships']}
 got={(rel_by_child.get(r['id'],{}).get('parent_id'),r['canonical_name']) for r in dis}
 if want!=got: x('YE_DISTRICT_FIXTURE','districts','district (parent,name) set must equal the checksum-bound 333-district fixture')
 if any(r.get('verification_status')!='probable' for r in dis): x('YE_DISTRICT_STATUS','districts','district identities carry probable status pending an atomic official coded register')
 fl=L(ROOT/'data/imports/yemen/fixtures/amanat_lanes_2026.json')
 qa_names={q['name'] for h in fl['tahrir']['hays'] if h['name']=='القاع' for q in h['lanes']}
 rel_lane={r['child_id']:r for r in d['relationships'] if r.get('relationship_type')=='located_in'}
 if any(r['id'] not in rel_lane for r in lanes+hays): x('YE_LANE_CONTEXT','lanes','every lane and hay requires a sourced located_in relationship')
 bad=[r['id'] for r in lanes if (r['canonical_name'] in qa_names and rel_lane.get(r['id'],{}).get('parent_id','').startswith('ENT-YE-NEIGHBORHOOD') and r.get('verification_status')!='unverified')]
 if any(r.get('verification_status') not in {'probable','unverified'} for r in lanes): x('YE_LANE_STATUS','lanes','lane identities stay probable or unverified pending a primary lane register')
 lane_pops=[c for c in C if c.get('predicate')=='population' and c.get('subject_id') in {r['id'] for r in lanes}]
 if len(lane_pops)!=33 or any(c.get('observed_at')!='2004-12-16' or c.get('published') for c in lane_pops): x('YE_LANE_POP','claims','33 unpublished 2004 lane population claims; no projection, no publication')
 narr=[c for c in C if c.get('predicate')=='name_origin_narrative']
 if len(narr)!=3 or any(c.get('verification_status')!='local_reported' or c.get('published') for c in narr): x('YE_LANE_NARRATIVE','claims','naming narratives stay local_reported and unpublished')
 dishes=[c for c in C if c.get('predicate')=='food_dish']; dial=[c for c in C if c.get('predicate')=='dialect_profile']; langs=[c for c in C if c.get('predicate')=='language_presence']
 if len(dishes)!=12 or any(c.get('verification_status')!='local_reported' or c.get('published') or not c.get('classification') for c in dishes): x('YE_CULTURE_DISHES','claims','12 unpublished local_reported dish claims with explicit classification')
 mandi=next((c for c in dishes if c['value']['data'].get('name')=='المندي'),None)
 if not mandi or mandi.get('classification')!='shared': x('YE_SHARED_NOT_EXCLUSIVE','claims','cross-border dishes must stay classified shared, never exclusively national')
 if len(dial)!=5 or any(c.get('verification_status')!='local_reported' or c.get('published') for c in dial): x('YE_CULTURE_DIALECTS','claims','5 unpublished local_reported dialect profiles')
 if len(langs)!=2 or any(c.get('verification_status')!='probable' or c.get('published') for c in langs): x('YE_CULTURE_LANGUAGES','claims','2 unpublished probable language-presence claims')
 dress=[c for c in C if c.get('predicate')=='clothing_item']; crafts=[c for c in C if c.get('predicate')=='craft_custom']; markets=[c for c in C if c.get('predicate')=='market_presence']
 if len(dress)!=7 or any(c.get('verification_status')!='local_reported' or c.get('published') or not c.get('classification') for c in dress): x('YE_CULTURE_DRESS','claims','7 unpublished local_reported dress claims with explicit classification')
 if len(crafts)!=4 or len(markets)!=3 or any(c.get('verification_status')!='local_reported' or c.get('published') for c in crafts+markets): x('YE_CULTURE_CRAFTS_MARKETS','claims','4 craft and 3 market unpublished local_reported claims')
 if cap and (cap[0]['canonical_name']!='أمانة العاصمة' or cap[0]['id']!='ENT-YE-CAPITAL-MUNICIPALITY-01'): x('YE_AMANAT_IDENTITY','Amanat Al Asimah','distinct capital municipality required')
 if any(a.get('entity_id')=='ENT-YE-CAPITAL-MUNICIPALITY-01' and 'محافظة' in a.get('name','') for a in d['aliases']): x('YE_AMANAT_ALIAS','aliases','Amanat cannot be governorate alias')
 for q in f['units']:
  eid='ENT-YE-'+('CAPITAL-MUNICIPALITY' if q['kind']=='capital_municipality' else 'GOVERNORATE')+'-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name_ar'] or not any(c['subject_id']==eid and c['predicate']=='administrative_profile' and c['value']['data']==q['kind'] for c in C): x('YE_FIXTURE_IDENTITY',eid,'fixture identity/profile mismatch')
 soc=E.get('ENT-YE-GOVERNORATE-22',{}); law=next((c for c in C if c.get('subject_id')==soc.get('id') and c.get('predicate')=='establishment_instrument'),None)
 if soc.get('valid_from')!='2013-12-18' or not law or law['value']['data'].get('law_number')!=31 or law['value']['data'].get('effective_clause_verified') is not False: x('YE_SOCOTRA_LAW','Socotra','Law 31/2013 issuance and unverified effective clause required')
 expected={'DEN-YE-COUNTRY-SCOPE':1,'DEN-YE-FIRST-LEVEL':22,'DEN-YE-GOVERNORATES':21,'DEN-YE-CAPITAL-MUNICIPALITY':1,'DEN-YE-LEGACY-FIRST-LEVEL':21,'DEN-YE-DISTRICTS':333,'DEN-YE-AMANAT-LANES':791}; expected.update({'DEN-YE-URBAN-SECTIONS-'+t['code']:t['frame_lanes_2004'] for t in fu['districts']})
 if {r['id']:r['value'] for r in d['denominators']}!=expected: x('YE_DENOMINATORS','denominators','1/22/21/1/21/333/791 required')
 if any(r['entity_type']=='ye_uzla' for r in E.values()): x('YE_PREMATURE_LOWER','entities','uzla deferred until an authoritative register')
 if any(r.get('status') in {'de_facto','destroyed','displaced','disputed'} for r in E.values()): x('YE_UNSUPPORTED_OVERLAY','entities','legal list cannot imply conflict overlay')
 first={r['id'] for r in E.values() if r['entity_type'] in {'ye_governorate','ye_capital_municipality'}}
 rel1=[r for r in d['relationships'] if r.get('child_id') in first]
 if len(rel1)!=22 or any(r.get('parent_id')!='ENT-YE-COUNTRY' for r in rel1): x('YE_PARENT','relationships','all 22 first-level units parent to country')
 rel2=[r for r in d['relationships'] if r.get('child_id') in {e['id'] for e in dis}]
 if len(rel2)!=333 or any(r.get('parent_id') not in first for r in rel2): x('YE_DISTRICT_PARENT','relationships','all 333 districts parent to a first-level unit')
 cov={r['id']:r for r in d['coverage']}
 if cov.get('COV-YE-FIRST-LEVEL',{}).get('matched')!=22 or cov.get('COV-YE-FIRST-LEVEL',{}).get('snapshot_date')!='2026-08-17': x('YE_COVERAGE_FRESHNESS','coverage','22 matched at snapshot date')
 if cov.get('COV-YE-DISTRICTS',{}).get('matched')!=333 or cov.get('COV-YE-DISTRICTS',{}).get('snapshot_date')!='2026-08-17': x('YE_DISTRICT_COVERAGE','coverage','333 matched at snapshot date')
 lc=cov.get('COV-YE-AMANAT-LANES',{})
 if lc.get('matched')!=104 or lc.get('missing')!=687 or lc.get('complete') or not lc.get('missing_reason'): x('YE_LANE_COVERAGE','coverage','104/791 matched, 687 documented missing, incomplete with explicit reason')

 # Depth cycle 2: named urban sections are bounded, unpublished places from a dated snapshot.
 sec_by_name={(r['canonical_name'],r.get('source_locator')) for r in secs}
 rel_by_child={r['child_id']:r for r in d['relationships']}
 for t in fu['districts']:
  text=(ROOT/'data/imports/yemen'/t['extract']).read_text(encoding='utf8')
  for q in t['sections']:
   if f"{q['name']}|{q['place']}|{q['object']}|{q['gns'] or '-'}" not in text: x('YE_SECTION_EVIDENCE',q['name'],f"section must appear in its checksum-bound extract {t['extract']}")
  if len([q for q in t['sections']])<1: x('YE_SECTION_COUNTS',t['district'],'a completed district needs at least one attested section')
  have=[r for r in secs if (rel_by_child.get(r['id']) or {}).get('parent_id')==t['district_id']]
  if len(have)!=len(t['sections']): x('YE_SECTION_COUNTS',t['district'],'section entities must equal the checksum-bound fixture list for this district')
 for r in secs:
  if r.get('coordinates') is not None or r.get('status')!='current': x('YE_SECTION_STATUS',r['id'],'urban sections carry no coordinate and stay current places')
  if r.get('verification_status') not in {'probable','unverified'}: x('YE_SECTION_STATUS',r['id'],'urban sections stay probable (gazetteer-tagged) or unverified (community-mapped)')
  rel=rel_by_child.get(r['id'])
  if not rel or rel.get('relationship_type')!='located_in': x('YE_SECTION_CONTEXT',r['id'],'every urban section needs exactly one located_in relationship')
  else:
   t=next((t for t in fu['districts'] if t['district_id']==rel.get('parent_id')),None)
   if t is None or r['canonical_name'] not in {q['name'] for q in t['sections']}: x('YE_SECTION_CONTEXT',r['id'],'section parent must be the district named in the fixture')
  if any(c['subject_id']==r['id'] for c in C): x('YE_SECTION_CLAIMLESS',r['id'],'this cycle imports no population, no narrative and no scope label for an urban section')
 ids_sec={r['id'] for r in secs}
 if len(fu['districts'])+len(fu['open_districts'])+len(fu['accepted_districts'])!=10: x('YE_OPEN_DISTRICTS','fixture','every Amanat district must be either completed, previously accepted, or recorded open with its retrieval failure')
 for o in fu['open_districts']:
  if not o.get('reason'): x('YE_OPEN_DISTRICTS',o['district'],'an open district needs its recorded reason')
  for r in E.values():
   if r['id']==o.get('district_id') or r.get('entity_type') in {'ye_district','ye_governorate','ye_capital_municipality','country'}: continue
   text=(r.get('source_locator') or '')+' '+(r.get('notes') or '')
   if o['district'] in text: x('YE_OPEN_DISTRICTS',o['district'],f"no entity may be attributed to a district whose extract was not retrieved ({r['id']})")
 dens={r['id']:r for r in d['denominators']}; covs={r['id']:r for r in d['coverage']}
 for t in fu['districts']:
  den=dens.get('DEN-YE-URBAN-SECTIONS-'+t['code']); cov=covs.get('COV-YE-URBAN-SECTIONS-'+t['code'])
  matched=len(t['sections'])
  if not den or den.get('value')!=t['frame_lanes_2004'] or den.get('layer')!='ye_amanat_urban_sections_2026': x('YE_SECTION_COVERAGE',t['code'],'district denominator must equal the 2004 frame count on the depth layer')
  if not cov or cov.get('matched')!=matched or cov.get('complete') or cov.get('coverage_percentage')!=round(100.0*matched/t['frame_lanes_2004'],2): x('YE_SECTION_COVERAGE',t['code'],'coverage must be the bounded attested count on the district frame, never complete')
  elif not cov.get('missing_reason'): x('YE_SECTION_COVERAGE',t['code'],'incomplete district row needs an explicit missing reason')
  elif len(fu['open_districts'])>0 and not any(o['district'] in cov['missing_reason'] for o in fu['open_districts']): x('YE_SECTION_COVERAGE',t['code'],'open districts must be named in the missing reason')
 snaps={r['id']:r for r in d['snapshots']}
 s2=snaps.get('SNP-YE-URBAN-SECTIONS-20260923'); s1=snaps.get('SNP-YE-PRODUCTION-20260817')
 if not s2 or s2.get('captured_at')!='2026-09-23' or s2.get('checksum')!='sha256:'+hashlib.sha256((ROOT/'data/imports/yemen/fixtures/amanat_urban_sections_2026.json').read_bytes()).hexdigest(): x('YE_URBAN_SNAPSHOT','snapshots','the urban-section snapshot is dated 2026-09-23 and bound to the fixture checksum')
 if not s1 or s1.get('captured_at')!='2026-08-17': x('YE_URBAN_SNAPSHOT','snapshots','the accepted production snapshot keeps its own date')
 return err
def main():
 d=data(); e=validate(d); met={k:len(d[k]) for k in ['entities','aliases','relationships','claims','sources','denominators','coverage']}; write_json(ROOT/'reports/yemen_validation.json',{'schema_version':'2.0.0','country_code':'YE','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e}); print(met); return 0 if not e else 1
if __name__=='__main__': raise SystemExit(main())
