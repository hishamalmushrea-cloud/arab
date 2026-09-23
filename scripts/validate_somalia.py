#!/usr/bin/env python3
import json,re
from model import ROOT,read_jsonl,write_json
def L(p):return json.loads(p.read_text(encoding='utf8'))
BASE_SIDS=['SRC-SO-MOP-FMS-2026','SRC-SO-MOIFAR-NORTHEAST-2026','SRC-SO-SONNA-NORTHEAST-DECLARATION-2026','SRC-SO-SENATE-CONSTITUENCY','SRC-SO-MPWR-FIVE-FMS-2025']
DEPTH_SIDS=['SRC-UNESCO-ICH-SO-STATE-2026','SRC-UNESCO-ICH-SO-XEER-CIISE-02087-2024','SRC-UNESCO-ICH-SO-ZAFFA-02283-2025','SRC-UNESCO-WH-SO-STATE-2026','SRC-UNESCO-WH-SO-BUSHBUSHLE-6752-2024','SRC-UNESCO-WH-SO-HOBYO-6753-2024','SRC-UNESCO-WH-SO-LIGHTHOUSE-6754-2025','SRC-SO-CONSTITUTION-2012','SRC-SO-ISO639-3-SOMALI','SRC-SO-LANGUAGES-MIRROR-2026','SRC-SO-CUISINE-MIRROR-2026','SRC-SO-CULTURE-MIRROR-2026','SRC-SO-MOGADISHU-MIRROR-2026']
SIDS=set(BASE_SIDS+DEPTH_SIDS)
TENTATIVE={'6752','6753','6754'}
ARTICLES={'1','2','5','6','7','9','15'}
PLACE_PARENT={'ENT-SO-SITE-BUSHBUSHLE':'ENT-SO-COUNTRY','ENT-SO-SITE-HOBYO':'ENT-SO-COUNTRY','ENT-SO-SITE-LIGHTHOUSE':'ENT-SO-REGION-BRA','ENT-SO-QUARTER-HAMAR':'ENT-SO-REGION-BRA'}
NO_COUNT_PREDICATES={'language_presence','dialect_profile','food_dish','craft_custom','custom_practice','language_institution','place_name_narrative'}
COUNT_KEYS={'speakers','speaker_count','speaker_share','population','pop','count','number','qty','percentage','share','ratio','total'}
COUNT_WORDS='عدد|نسبة|سكان|متحدث|متحدثون|مليون|ألف|نسمة|إحصاء|تعداد'
def count_leak(blob):
 if re.search(r'[0-9٠-٩]\s*[%٪]',blob) or re.search('(?:'+COUNT_WORDS+r')[^،.؛]{0,14}[0-9٠-٩]',blob) or re.search(r'[0-9٠-٩][^،.؛]{0,14}(?:'+COUNT_WORDS+')',blob):return True
 def walk(x):
  if isinstance(x,dict):return any(str(k).lower() in COUNT_KEYS or walk(v) for k,v in x.items())
  if isinstance(x,list):return any(walk(v) for v in x)
  return False
 return walk(json.loads(blob))
CAPITAL_PREDICATES={'capital_of','national_capital','capital_city'}
DEPTH_LAYERS=['unesco_intangible_heritage','world_heritage_inscribed','world_heritage_tentative_list','heritage_places','classified_local_knowledge']
def data():
 e=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='SO'];ids={r['id'] for r in e}
 return {'entities':e,'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r.get('entity_id') in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in (ROOT/'data/sources').glob('*.json') if L(p).get('id') in SIDS],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='SO'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r.get('country_code')=='SO'],'manifest':L(ROOT/'manifests/SO.yml'),'domain_status':L(ROOT/'data/cultural/somalia_domain_status.json'),'source_catalog':L(ROOT/'data/imports/somalia/source_catalog.json')}
def validate(d):
 f=L(ROOT/'data/imports/somalia/fixtures/federal_frames_2026.json');x_=L(ROOT/'data/imports/somalia/fixtures/cultural_depth_2026.json');E={r['id']:r for r in d['entities']};C=d['claims'];err=[]
 def x(c,l,m):err.append({'code':c,'location':l,'message':m})
 def pred(p):return [c for c in C if c['predicate']==p]
 fs=[r for r in E.values() if r['entity_type']=='so_federal_member_state'];regions=[r for r in E.values() if r['entity_type']=='so_region'];places=[r for r in E.values() if r['id'] in PLACE_PARENT]
 if len(E)!=13 or len(fs)!=7 or len(regions)!=1 or len(places)!=4:x('SO_COUNTS','entities','country+7 MOP-frame FMS+Banadir+four heritage places')
 for q in f['federal_member_states']:
  eid='ENT-SO-FMS-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name'] or not any(c['subject_id']==eid and c['predicate']=='federal_planning_profile' and c['value']['data']==q['profile'] for c in C):x('SO_FRAME_PROFILE',eid,'identity/profile')
 if E.get('ENT-SO-REGION-BRA',{}).get('canonical_name')!='Banadir Regional Administration' or E.get('ENT-SO-REGION-BRA',{}).get('entity_type')!='so_region':x('SO_BANADIR_PARALLEL','Banadir','must remain regional administration')
 sl=E.get('ENT-SO-FMS-06',{});slc=next((c for c in C if c.get('subject_id')==sl.get('id') and c.get('predicate')=='federal_planning_profile'),{})
 if sl.get('status')!='claimed' or slc.get('classification')!='disputed':x('SO_SOMALILAND_NARRATIVE','Somaliland','claimed entity and disputed narrative required')
 ne=E.get('ENT-SO-FMS-07',{});tr=next((c for c in C if c.get('predicate')=='federal_member_transition'),None)
 if ne.get('valid_from')!='2026-01-17' or not tr or tr['value']['data'].get('predecessor_name')!='SSC-Khaatumo' or tr['value']['data'].get('full_member_declaration')!='2026-01-17':x('SO_NORTHEAST_TRANSITION','North East','transition dates/provenance')
 if any('SSC' in r.get('canonical_name','') or 'Khaatumo' in r.get('canonical_name','') for r in E.values()):x('SO_SSC_DUPLICATE','entities','SSC is predecessor, not duplicate current entity')
 expected={'DEN-SO-COUNTRY-SCOPE':1,'DEN-SO-MOP-FMS':7,'DEN-SO-STANDARD-FIVE':5,'DEN-SO-SOMALILAND-NARRATIVE':1,'DEN-SO-NORTHEAST':1,'DEN-SO-BANADIR':1,'DEN-SO-REGIONS':None,'DEN-SO-DISTRICTS':None}
 if {r['id']:r['value'] for r in d['denominators']}!=expected:x('SO_DENOMINATORS','denominators','authority-specific and unavailable layers')
 if any(r['entity_type']=='so_district' for r in E.values()):x('SO_PREMATURE_LOWER','entities','districts unavailable')
 if any(r.get('status') in {'de_facto','destroyed','displaced','disputed'} for r in E.values()):x('SO_UNSUPPORTED_OVERLAY','entities','no control/condition overlay')
 rel=[r for r in d['relationships'] if r.get('child_id')!='ENT-SO-COUNTRY'];admin=[r for r in rel if r.get('relationship_type')=='administrative_parent']
 if len(admin)!=8 or any(r.get('parent_id')!='ENT-SO-COUNTRY' for r in admin):x('SO_PARENT','relationships','frame entities parent to country only')
 cov={r['id']:r for r in d['coverage']}
 if cov.get('COV-SO-MOP-FMS',{}).get('matched')!=7 or cov.get('COV-SO-MOP-FMS',{}).get('snapshot_date')!='2026-08-17':x('SO_COVERAGE_FRESHNESS','coverage','7/7 current MOP frame')
 for i in ['COV-SO-REGIONS','COV-SO-DISTRICTS']:
  r=cov.get(i,{})
  if r.get('denominator') is not None or r.get('coverage_percentage') is not None or r.get('complete') is not False:x('SO_UNAVAILABLE_LOWER',i,'null denominator and no percentage')
 src={r['id']:r for r in d['sources']};catalog={r['id'] for r in d['source_catalog']['sources']}
 if set(src)!=SIDS or catalog!=SIDS or len(d['source_catalog']['sources'])!=18:x('SO_DEPTH_SOURCE_REFS','sources',f'18 per-country sources expected, got {len(src)}')
 for r in d['sources']:
  if r['country_codes']!=['SO']:x('SO_DEPTH_SOURCE_REFS',r['id'],'source must stay country-scoped to Somalia')
 for c in C:
  for k in ('source_id','second_source_id'):
   if c.get(k) and c[k] not in SIDS:x('SO_DEPTH_SOURCE_REFS',c['id'],f'unresolved {k}={c.get(k)}')
 for c in C:
  if c.get('published'):
   q=src.get(c['source_id'],{})
   if q.get('quality_tier')!='A' or c.get('verification_status')!='verified' or c.get('status')!='verified':x('SO_DEPTH_PUBLISHED_TIER',c['id'],'published claims need tier A and verified status')
 ich=pred('intangible_cultural_practice')
 if len(ich)!=2 or any(c.get('classification')!='shared' for c in ich) or any(c.get('classification')=='national' for c in ich):x('SO_SHARED_NOT_NATIONAL','claims','two shared ICH elements, never national')
 if sorted(c['value']['data']['reference'] for c in ich)!=['02087','02283']:x('SO_SHARED_NOT_NATIONAL','claims','references 02087 and 02283')
 wc=pred('world_heritage_inscribed_count')
 if len(wc)!=1 or wc[0]['value']['data']!=0 or not wc[0]['published']:x('SO_WH_ZERO_INSCRIBED','claims','deliberate zero inscribed count, published')
 tl=pred('unesco_tentative_listing')
 if len(tl)!=3 or {c['value']['data']['reference'] for c in tl}!=TENTATIVE or any(c['value']['data'].get('status')!='القائمة المؤقتة' or not c['published'] for c in tl):x('SO_TENTATIVE_THREE','claims','three tentative-list submissions, published, never styled as inscribed')
 cp=pred('constitutional_provision')
 if len(cp)!=7 or {c['value']['data']['article'] for c in cp}!=ARTICLES:x('SO_CONSTITUTION_ARTICLES','claims','seven articles 1,2,5,6,7,9,15')
 art9=next((c for c in cp if c['value']['data']['article']=='9'),{})
 if any(p in CAPITAL_PREDICATES for p in (c['predicate'] for c in C)) or re.search(r'مقديشو|Muqdisho|Mogadishu',art9.get('value',{}).get('data',{}).get('summary','')):x('SO_CAPITAL_DEFERRED','claims','constitution defers capital status; no capital claim may be sourced from it')
 lp=pred('language_presence');pub_lang=[c for c in lp if c['published']]
 som=next((c for c in lp if c['value']['data']['name']=='الصومالية'),None)
 if len(lp)!=14 or len(pub_lang)!=2 or not som or som['value']['data'].get('iso_codes')!=['som'] or som.get('second_source_id')!='SRC-SO-ISO639-3-SOMALI' or not som['published'] or som['value']['data'].get('level')!='official':x('SO_LANGUAGE_OFFICIAL','claims','Somali official with ISO `som` second source, Arabic second, rest unpublished')
 for c in C:
  if c['predicate'] in NO_COUNT_PREDICATES and count_leak(json.dumps(c['value']['data'],ensure_ascii=False)):x('SO_NO_COUNTS',c['id'],'no speaker, population or share numbers may be recorded')
 ids={r['id'] for r in d['entities']}
 for eid,parent in PLACE_PARENT.items():
  e=E.get(eid,{});own=[r for r in rel if r.get('child_id')==eid]
  if e.get('coordinates') is not None or e.get('verification_status')!='source_verified' or not e.get('source_locator') or not e.get('notes'):x('SO_DEPTH_PLACE_SHAPE',eid,'places carry no coordinates and one source locator')
  if any(a.get('entity_id')==eid for a in d['aliases']):x('SO_DEPTH_PLACE_SHAPE',eid,'places carry no aliases')
  if any(c.get('subject_id')==eid for c in C):x('SO_DEPTH_PLACE_CLAIMLESS',eid,'places stay claim-free')
  if len(own)!=1 or own[0].get('relationship_type')!='located_in' or own[0].get('parent_id')!=parent:x('SO_DEPTH_PLACE_PARENT',eid,f'exactly one located_in to {parent}')
 ds=d['domain_status']['domains']
 if ds.get('world_heritage',{}).get('inscribed')!=0 or ds.get('world_heritage',{}).get('tentative_list_sites')!=3 or 'not_imported' in json.dumps(ds.get('world_heritage',{}),ensure_ascii=False) or ds.get('intangible_cultural_heritage',{}).get('national')!=0 or ds.get('dialect',{}).get('claims')!=3 or ds.get('food',{}).get('claims')!=12:x('SO_DOMAIN_STATUS','domain_status','depth domains documented, zero national ICH, zero inscribed')
 layers=[l['layer'] for l in d['manifest']['pilot_layers']]
 if not set(DEPTH_LAYERS)<=set(layers) or any(l.get('snapshot_date')!='2026-09-23' or l.get('denominator_id') is not None or l.get('coverage_record_id') is not None for l in d['manifest']['pilot_layers'] if l.get('layer') in DEPTH_LAYERS):x('SO_MANIFEST_LAYERS','manifest','depth layers declared with no denominator')
 if len(x_['ich_elements'])!=2 or any(e['classification']!='shared' for e in x_['ich_elements']):x('SO_SHARED_NOT_NATIONAL','fixture','fixture keeps both ICH elements shared')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','aliases','relationships','claims','sources','denominators','coverage']};met['published']=sum(1 for c in d['claims'] if c['published']);write_json(ROOT/'reports/somalia_validation.json',{'schema_version':'2.0.0','country_code':'SO','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met);return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
