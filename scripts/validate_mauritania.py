#!/usr/bin/env python3
"""Semantic validator for Mauritania cycle 1: accepted wilaya layer plus the depth layer."""
import hashlib,json,re
from model import ROOT,read_jsonl,write_json
ACCEPTED={'SRC-MR-DGAT-15-63-2026','SRC-MR-ANSADE-RGPH5-2024','SRC-MR-ANSADE-PEER-REVIEW-2024'}
TIER={'local_website':'E','local_press':'B','institutional_page':'A','law':'A','standard':'A','official_report':'A','census':'A','official_register':'A'}
ICH={'00524':(2011,'USL','national',1),'01960':(2023,'RL','national',1),'01692':(2024,'RL','national',1),
     '01602':(2020,'RL','shared',4),'01718':(2021,'RL','shared',16),'01902':(2022,'RL','shared',15),
     '01951':(2023,'RL','shared',10),'02116':(2024,'RL','shared',16),'02283':(2025,'RL','shared',7)}
DEPTH_PREDICATES={'food_dish':12,'language_presence':11,'intangible_cultural_practice':9,'constitutional_provision':5,
 'unesco_pending_nomination':3,'unesco_tentative_listing':3,'custom_practice':2,'world_heritage_property':2,
 'clothing_item':2,'script_profile':1,'craft_custom':1,'place_name_narrative':1,'dialect_profile':1,
 'folk_narrative':1,'city_founding':1,'convention_ratification_date':1}
BANNED=['5.6','5٫6','705,500','70–80','70-80','15%–20%','15%-20%','7%–10%','1%–3%']
FORBIDDEN_KEYS={'population','population_count','speakers','speaker_count','percentage','share','ratio','count','نسبة'}
QTY=re.compile(r'\d[\d.,٫]*\s*(?:%|٪|في المئة|بالمئة|مليون|ألف|آلاف|نسمة|متحدث|ساكن)|\d{1,3}(?:,\d{3})+|\d{5,}')
SKIP_KEYS={'reference','iso_codes','article','url','official_title'}
PLACE_TYPES={'city','archaeological_site'}
# Heritage places: type and the single located_in parent fixed by the fixture text.
PLACE_MAP={'ENT-MR-TOWN-CHINGUETTI':('city','ENT-MR-WILAYA-07'),'ENT-MR-TOWN-OUADANE':('city','ENT-MR-WILAYA-07'),
 'ENT-MR-TOWN-OUALATA':('city','ENT-MR-WILAYA-01'),'ENT-MR-TOWN-TICHITT':('city','ENT-MR-WILAYA-09'),
 'ENT-MR-SITE-AZOUGUI':('archaeological_site','ENT-MR-WILAYA-07'),'ENT-MR-SITE-TEGDAOUST':('archaeological_site','ENT-MR-WILAYA-02'),
 'ENT-MR-SITE-KUMBI-SALEH':('archaeological_site','ENT-MR-COUNTRY')}
LAYERS={'mr_wilaya','mr_wilaya_nouakchott_profile','mr_wilaya_regional_profile','unesco_intangible_heritage','world_heritage_properties','heritage_places','classified_local_knowledge'}
DEPTH_LAYERS={'unesco_intangible_heritage','world_heritage_properties','heritage_places','classified_local_knowledge'}
FIXTURES=(('wilaya_profiles.json','data/imports/mauritania/fixtures/wilaya_profiles.json'),
          ('cultural_depth_2026.json','data/imports/mauritania/fixtures/cultural_depth_2026.json'))
def L(p):return json.loads(p.read_text(encoding='utf8'))
def data():
 E=[r for r in read_jsonl(ROOT/'data/entities/entities.jsonl') if r.get('country_code')=='MR'];ids={r['id'] for r in E}
 return {'entities':E,'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r.get('child_id') in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r.get('subject_id') in ids],'sources':[L(p) for p in sorted((ROOT/'data/sources').glob('*.json')) if L(p).get('country_codes')==['MR']],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r.get('country_code')=='MR'],'manifest':L(ROOT/'manifests/MR.yml')}
def validate(d):
 f=L(ROOT/'data/imports/mauritania/fixtures/wilaya_profiles.json');m=L(ROOT/'data/imports/mauritania/snapshot_manifest.json')
 E={r['id']:r for r in d['entities']};C=d['claims'];R=d['relationships'];S={s['id']:s for s in d['sources']};err=[]
 def x(c,l,msg):err.append({'code':c,'location':l,'message':msg})
 def tier(cid):return S.get(cid,{}).get('quality_tier')
 depth=[c for c in C if c['id'].startswith('CLM-MR-DEPTH')]
 # fixtures are checksum-bound to the manifest
 for name,rel in FIXTURES:
  blob=(ROOT/rel).read_bytes();rec=next((r for r in m['records'] if r['path']==rel),None)
  if not rec or rec['sha256']!=hashlib.sha256(blob).hexdigest() or rec['bytes']!=len(blob):x('MR_FIXTURE_SHA',name,'fixture checksum mismatch')
 wil=[e for e in E.values() if e['entity_type']=='mr_wilaya']
 if len(E)!=23 or len(wil)!=15 or sum(e['entity_type']=='country' for e in E.values())!=1 or len(C)!=73:x('MR_COUNTS','entities',f'{len(E)}/{len(wil)}/{len(C)}')
 for q in f['wilayas']:
  eid='ENT-MR-WILAYA-'+q['code']
  if E.get(eid,{}).get('canonical_name')!=q['name_fr'] or not any(c['subject_id']==eid and c['predicate']=='administrative_profile' and c['value']['data']==q['profile'] for c in C):x('MR_ACCEPTED',eid,'identity/profile')
 if {r['id']:r['value'] for r in d['denominators']}!={'DEN-MR-COUNTRY-SCOPE':1,'DEN-MR-WILAYAS':15,'DEN-MR-NOUAKCHOTT-WILAYAS':3,'DEN-MR-REGIONAL-WILAYAS':12}:x('MR_DENOMINATORS','denominators','1/15/3/12')
 if any(r['entity_type'] in {'mr_moughataa','mr_commune'} for r in E.values()):x('MR_LOWER','entities','moughataa/commune records deferred')
 # source tiers are derived from the source type, never inflated
 for s in d['sources']:
  if TIER.get(s['source_type'])!=s['quality_tier']:x('MR_SOURCES',s['id'],f"{s['source_type']} must be tier {TIER.get(s['source_type'])}")
  if not s.get('retrieved_at') or not s.get('license'):x('MR_SOURCES',s['id'],'retrieved_at/license required')
 # depth shape
 if len(depth)!=56:x('MR_DEPTH_COUNTS','claims',f'{len(depth)} depth claims')
 seen={}
 for c in depth:seen[c['predicate']]=seen.get(c['predicate'],0)+1
 for p,n in DEPTH_PREDICATES.items():
  if seen.get(p)!=n:x('MR_DEPTH_COUNTS',p,f'{seen.get(p)} != {n}')
 for c in depth:
  has,loc=bool(c.get('second_source_id')),bool(c.get('second_source_locator'))
  if has!=loc:x('MR_SECOND_SOURCE_PAIR',c['id'],'second source needs id and locator together')
  if c.get('published') and tier(c['source_id'])!='A':x('MR_WEAK_DEPTH_PUBLISHED',c['id'],'only tier-A depth claims are published in this cycle')
 # intangible heritage
 ich=[c for c in C if c['predicate']=='intangible_cultural_practice']
 if len(ich)!=9:x('MR_ICH_CONTRACT','claims',f'{len(ich)} elements')
 for c in ich:
  v=c['value']['data'];ref=str(v.get('reference'));exp=ICH.get(ref)
  if not exp:x('MR_ICH_CONTRACT',c['id'],f'unknown reference {ref}')
  elif (v.get('year'),v.get('list'),c['classification'],len(v.get('co_states',[])))!=exp:x('MR_ICH_CONTRACT',c['id'],f'{ref} shape mismatch')
  elif not c.get('published') or c['verification_status']!='verified':x('MR_ICH_CONTRACT',c['id'],'element must be published verified')
  elif tier(c['source_id'])!='A':x('MR_ICH_CONTRACT',c['id'],'element source must be tier A')
  elif 'موريتانيا' not in v.get('co_states',[]):x('MR_ICH_CONTRACT',c['id'],'MR must appear among the co-states')
 pend=[c for c in C if c['predicate']=='unesco_pending_nomination']
 if len(pend)!=3:x('MR_PENDING_NOMINATION','claims',f'{len(pend)} nominations')
 for c in pend:
  if not c.get('published') or c['value']['data'].get('status')!='قيد النظر' or c['verification_status']!='verified':x('MR_PENDING_NOMINATION',c['id'],'nomination stays pending, official and published')
 names=' '.join(c['value']['data'].get('name','') for c in ich)
 if 'العود' in names or 'السعفيات' in names:x('MR_PENDING_NOMINATION','claims','a pending nomination is recorded as inscribed')
 rat=[c for c in C if c['predicate']=='convention_ratification_date']
 if len(rat)!=1 or rat[0]['value']['data']['date']!='2006-11-15' or not rat[0].get('published'):x('MR_CONVENTION_CONTRACT','claims','2006-11-15 stays published')
 const={c['value']['data']['article']:c for c in C if c['predicate']=='constitutional_provision'}
 if set(const)!= {'1','5','6','7','9'}:x('MR_CONSTITUTION_CONTRACT','claims',sorted(const))
 else:
  if not all(c.get('published') and c['verification_status']=='verified' for c in const.values()):x('MR_CONSTITUTION_CONTRACT','claims','articles stay published verified')
  if 'الرسمية هي العربية' not in const['6']['value']['data']['summary']:x('MR_CONSTITUTION_CONTRACT','claims','article 6 official-language wording')
  if 'نواكشوط' not in const['7']['value']['data']['summary']:x('MR_CONSTITUTION_CONTRACT','claims','article 7 capital')
  if 'الإسلام' not in const['5']['value']['data']['summary']:x('MR_CONSTITUTION_CONTRACT','claims','article 5 religion')
 # world heritage and the tentative list
 wh={str(c['value']['data']['reference']):c for c in C if c['predicate']=='world_heritage_property'}
 if set(wh)!={'750','506'}:x('MR_WH_CONTRACT','claims',sorted(wh))
 else:
  a,b=wh['750']['value']['data'],wh['506']['value']['data']
  if (a['year'],a['category'],a['criteria'])!=(1996,'ثقافي',['iii','iv','v']):x('MR_WH_CONTRACT','claims','ksour shape')
  if (b['year'],b['category'],b['criteria'])!=(1989,'طبيعي',[]):x('MR_WH_CONTRACT','claims','the natural property carries no criteria')
  for k,c in wh.items():
   if not c.get('published') or c['verification_status']!='verified':x('MR_WH_CONTRACT',c['id'],'property stays published verified')
 tent=[c for c in C if c['predicate']=='unesco_tentative_listing']
 if {str(c['value']['data']['reference']) for c in tent}!={'1545','1546','1547'} or any(c['classification']!='official' or not c.get('published') for c in tent):x('MR_TENTATIVE_CONTRACT','claims',f'{len(tent)} tentative sites')
 if any(c['predicate']=='world_heritage_property' and str(c['value']['data']['reference']) in {'1545','1546','1547'} for c in C):x('MR_TENTATIVE_CONTRACT','claims','tentative site recorded as inscribed')
 # languages
 lang={c['value']['data']['name']:c for c in C if c['predicate']=='language_presence'}
 if len(lang)!=11:x('MR_LANGUAGE_CONTRACT','claims',f'{len(lang)} presences')
 ar=lang.get('العربية')
 if not ar or not ar.get('published') or not ar['value']['data']['official'] or ar['value']['data']['level']!='official':x('MR_LANGUAGE_CONTRACT','claims','Arabic stays the published official language')
 for n in ('البولارية (بولاار)','السوننكية','الولوفية'):
  c=lang.get(n)
  if not c or not c.get('published') or c['value']['data']['level']!='national' or c['value']['data']['official']:x('MR_LANGUAGE_CONTRACT',n,'national language stays non-official and published')
  elif c['source_id'] not in ACCEPTED and tier(c['source_id'])!='A':x('MR_LANGUAGE_CONTRACT',n,'constitutional source expected')
  elif not c.get('second_source_id') or not c.get('second_source_locator'):x('MR_LANGUAGE_CONTRACT',n,'ISO 639-3 second source required')
 for n,c in lang.items():
  v=c['value']['data']
  if v.get('level')=='signed' and v.get('iso_codes'):x('MR_LANGUAGE_CONTRACT',c['id'],'signed language must claim no ISO code')
  if c.get('published') and v.get('level') not in ('official','national'):x('MR_LANGUAGE_CONTRACT',c['id'],'weak-level presence stays unpublished')
  if c.get('published') and not v.get('iso_codes') and v.get('level')!='official':x('MR_LANGUAGE_CONTRACT',c['id'],'published language needs a verified ISO code')
 if len([c for c in C if c['predicate']=='dialect_profile'])!=1:x('MR_DIALECT_CONTRACT','claims','one dialect profile')
 if len([c for c in C if c['predicate']=='script_profile'])!=1:x('MR_SCRIPT_CONTRACT','claims','one script profile')
 # no counts anywhere in the depth body
 blob=json.dumps(depth,ensure_ascii=False)
 for token in BANNED:
  if token in blob:x('MR_NO_COUNTS','depth',f'banned token {token}')
 for c in depth:
  v=c['value']['data']
  if isinstance(v,dict):
   for k in FORBIDDEN_KEYS:
    if k in v:x('MR_NO_COUNTS',c['id'],f'count key {k}')
  scan={k:val for k,val in v.items() if k not in SKIP_KEYS} if isinstance(v,dict) else v
  q=QTY.search(json.dumps({'data':scan,'notes':c.get('notes')},ensure_ascii=False))
  if q:x('MR_NO_COUNTS',c['id'],f'quantity phrase {q.group(0)!r}')
 # narrative stays narrative and unpublished
 folk=[c for c in C if c['verification_status']=='folk_narrative']
 if len(folk)!=1 or folk[0].get('published') or folk[0]['classification']!='folk_narrative' or folk[0]['predicate']!='folk_narrative':x('MR_FOLK_NARRATIVE','claims',f'{len(folk)} folk narratives')
 for c in C:
  if c['predicate']=='place_name_narrative' and (c.get('published') or c['verification_status']!='local_reported'):x('MR_FOLK_NARRATIVE',c['id'],'naming narrative stays unpublished local_reported')
 if not any(c['predicate']=='place_name_narrative' for c in C):x('MR_FOLK_NARRATIVE','claims','naming narrative missing')
 # the commune count stays an open conflict
 dis=[c for c in C if c['predicate']=='commune_count_candidates']
 if len(dis)!=1 or sorted(dis[0]['value']['data'])!=[219,220] or dis[0]['classification']!='disputed' or dis[0]['verification_status']!='source_verified' or not dis[0].get('published'):x('MR_DISCREPANCY','claims','219/220 stays a published disputed pair')
 # places carry a location and nothing else
 pid={e['id'] for e in E.values() if e['entity_type'] in PLACE_TYPES}
 places=[e for e in E.values() if e['entity_type'] in PLACE_TYPES]
 if len(places)!=7:x('MR_PLACE_CONTRACT','entities',f'{len(places)} places')
 for e in places:
  exp=PLACE_MAP.get(e['id'])
  if not exp or e['entity_type']!=exp[0]:x('MR_PLACE_CONTRACT',e['id'],f"type must be {exp[0] if exp else 'mapped'}")
  rels=[r for r in R if r['child_id']==e['id']]
  if exp and (len(rels)!=1 or rels[0]['parent_id']!=exp[1]):x('MR_PLACE_LOCATED_IN',e['id'],f"parent must be {exp[1]}")
  if len(rels)!=1 or rels[0]['relationship_type']!='located_in' or rels[0]['parent_id'] not in E:x('MR_PLACE_LOCATED_IN',e['id'],'exactly one located_in into a known parent')
  if any(c['subject_id']==e['id'] for c in C):x('MR_PLACE_CLAIMS',e['id'],'places carry no claims in this cycle')
  if e.get('coordinates'):x('MR_PLACE_CONTRACT',e['id'],'no coordinates in this cycle')
  st=tier(e['canonical_source_id'])
  if st not in ('A','B','E'):x('MR_PLACE_CONTRACT',e['id'],'unknown canonical source')
  elif st in ('E',) and (e['verification_status']!='local_reported' or e['confidence']!='low'):x('MR_PLACE_CONTRACT',e['id'],'mirror-sourced place stays local_reported/low')
  elif st=='A' and (e['verification_status']!='source_verified' or e['confidence']!='high'):x('MR_PLACE_CONTRACT',e['id'],'UNESCO-sourced place stays source_verified/high')
  if not e.get('source_locator') or e['source_locator']!=e.get('notes'):x('MR_PLACE_CONTRACT',e['id'],'source locator required and must match the note')
 if any(r['relationship_type']=='administrative_parent' for r in R if r['child_id'] in pid):x('MR_PLACE_LOCATED_IN','relations','places must not have administrative parents')
 if any(r['parent_id'] in pid for r in R):x('MR_PLACE_LOCATED_IN','relations','no child may hang under a heritage place')
 if not any(r['child_id']=='ENT-MR-SITE-KUMBI-SALEH' and r['parent_id']=='ENT-MR-COUNTRY' for r in R):x('MR_PLACE_LOCATED_IN','relations','Kumbi Saleh is located at country level')
 # publishing rules
 pub=[c for c in C if c.get('published')]
 if any(c['verification_status'] not in ('verified','source_verified') for c in pub):x('MR_PUBLISH','claims','published requires verified/source_verified')
 tiers=[tier(c['source_id']) for c in pub]
 if any(t is None for t in tiers):x('MR_PUBLISH','claims','published claim with unknown source')
 elif round(100*sum(t in ('A','B') for t in tiers)/len(tiers),2)<95:x('MR_PUBLISH','claims','A/B ratio below 95')
 if sum(1 for c in depth if c.get('published'))!=27:x('MR_PUBLISH','depth',f"{sum(1 for c in depth if c.get('published'))} published depth claims")
 # manifest layers
 lay={l['layer']:l for l in d['manifest'].get('pilot_layers',[])}
 if set(lay)!=LAYERS:x('MR_ICH_LAYER','manifest',sorted(lay))
 else:
  if (lay['unesco_intangible_heritage']['denominator'],lay['unesco_intangible_heritage']['scope_status'],lay['unesco_intangible_heritage']['coverage_record_id'])!=(9,'closed',None):x('MR_ICH_LAYER','manifest','ICH layer is 9/closed with no coverage record')
  if (lay['world_heritage_properties']['denominator'],lay['world_heritage_properties']['scope_status'],lay['world_heritage_properties']['coverage_record_id'])!=(2,'closed',None):x('MR_WH_CONTRACT','manifest','WH layer is 2/closed with no coverage record')
  for k in ('heritage_places','classified_local_knowledge'):
   if lay[k].get('denominator') is not None or lay[k]['scope_status']!='open' or lay[k].get('coverage_record_id'):x('MR_PLACE_LAYER','manifest',f'{k} is an open layer with no denominator')
  for k in DEPTH_LAYERS:
   if not lay[k]['special_cases']:x('MR_PLACE_LAYER','manifest',f'{k} needs a caveat')
 hier={h['entity_type']:h for h in d['manifest']['hierarchy']}
 if (hier['mr_moughataa'].get('denominator'),hier['mr_moughataa'].get('scope_status'))!=(63,'open'):x('MR_MOUGHATAA_SCOPE','manifest','63 stay open')
 mough=[c for c in C if c['predicate']=='moughataa_count']
 if len(mough)!=1 or mough[0]['value']['data']!=hier['mr_moughataa'].get('denominator') or not mough[0].get('published'):x('MR_MOUGHATAA_SCOPE','claims','the 63 count must match the manifest and stay published')
 if hier['mr_commune'].get('denominator') is not None or hier['mr_commune'].get('scope_status')!='open':x('MR_COMMUNE_CONFLICT','manifest','commune layer stays open at country level')
 return err
def main():
 d=data();e=validate(d);met={k:len(d[k]) for k in ['entities','relationships','claims','sources','denominators']}
 write_json(ROOT/'reports/mauritania_validation.json',{'schema_version':'2.0.0','country_code':'MR','status':'PASS' if not e else 'FAIL','p0':len(e),'critical_p1':0,'metrics':met,'errors':e});print(met,'errors',len(e));return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
