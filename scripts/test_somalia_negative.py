#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_somalia import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 def clm(d,pred,**kw):
  for c in d['claims']:
   data_=c['value'].get('data') if isinstance(c['value'].get('data'),dict) else {}
   if c['predicate']==pred and all(c.get(k)==v or data_.get(k)==v for k,v in kw.items()):return c
  raise KeyError((pred,kw))
 r('SO_DROP_NORTHEAST',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x['id']!='ENT-SO-FMS-07']),'SO_COUNTS')
 r('SO_BANADIR_AS_FMS',lambda d:next(x for x in d['entities'] if x['id']=='ENT-SO-REGION-BRA').update(entity_type='so_federal_member_state'),'SO_BANADIR_PARALLEL')
 r('SO_SOMALILAND_NEUTRAL_CURRENT',lambda d:next(x for x in d['entities'] if x['id']=='ENT-SO-FMS-06').update(status='current'),'SO_SOMALILAND_NARRATIVE')
 r('SO_DUPLICATE_SSC',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-SO-FMS-SSC','canonical_name':'SSC-Khaatumo'}),'SO_SSC_DUPLICATE')
 r('SO_NORTHEAST_WRONG_DATE',lambda d:next(x for x in d['entities'] if x['id']=='ENT-SO-FMS-07').update(valid_from='2025-07-30'),'SO_NORTHEAST_TRANSITION')
 r('SO_FIVE_AS_CURRENT_MOP_DENOMINATOR',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-SO-MOP-FMS').update(value=5),'SO_DENOMINATORS')
 r('SO_LEGAL_AS_DE_FACTO',lambda d:next(x for x in d['entities'] if x['id']=='ENT-SO-FMS-01').update(status='de_facto'),'SO_UNSUPPORTED_OVERLAY')
 r('SO_PREMATURE_DISTRICT',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-SO-DISTRICT-X','entity_type':'so_district'}),'SO_PREMATURE_LOWER')
 r('SO_FAKE_REGION_PERCENT',lambda d:next(x for x in d['coverage'] if x['id']=='COV-SO-REGIONS').update(denominator=18,coverage_percentage=5.56),'SO_UNAVAILABLE_LOWER')
 r('SO_WRONG_PARENT',lambda d:next(x for x in d['relationships'] if x['child_id']=='ENT-SO-FMS-07').update(parent_id='ENT-SO-FMS-01'),'SO_PARENT')
 r('SO_DEPTH_PLACE_COORDINATES',lambda d:next(x for x in d['entities'] if x['id']=='ENT-SO-SITE-HOBYO').update(coordinates={'lat':4.435,'lon':47.494}),'SO_DEPTH_PLACE_SHAPE')
 r('SO_DEPTH_PLACE_CLAIM',lambda d:d['claims'].append({**clm(d,'food_dish'),'id':'CLM-SO-DEPTH-FAKE','subject_id':'ENT-SO-QUARTER-HAMAR'}),'SO_DEPTH_PLACE_CLAIMLESS')
 r('SO_DEPTH_PLACE_SECOND_PARENT',lambda d:d['relationships'].append({**next(x for x in d['relationships'] if x['child_id']=='ENT-SO-QUARTER-HAMAR'),'id':'REL-SO-LOCATED-FAKE','parent_id':'ENT-SO-COUNTRY'}),'SO_DEPTH_PLACE_PARENT')
 r('SO_DEPTH_SHARED_AS_NATIONAL',lambda d:next(c for c in d['claims'] if c['predicate']=='intangible_cultural_practice').update(classification='national'),'SO_SHARED_NOT_NATIONAL')
 r('SO_DEPTH_SPEAKER_NUMBER',lambda d:clm(d,'language_presence',name='الصومالية')['value']['data'].update(note='60% من السكان يتحدثونها'),'SO_NO_COUNTS')
 r('SO_DEPTH_TENTATIVE_AS_INSCRIBED',lambda d:clm(d,'world_heritage_inscribed_count').update(value={'type':'integer','data':3}),'SO_WH_ZERO_INSCRIBED')
 r('SO_DEPTH_CAPITAL_INVENTION',lambda d:d['claims'].append({**clm(d,'constitutional_provision'),'id':'CLM-SO-DEPTH-CAPITAL','predicate':'national_capital','value':{'type':'string','data':'مقديشو'}}),'SO_CAPITAL_DEFERRED')
 r('SO_DEPTH_WEAK_PUBLISHED',lambda d:clm(d,'food_dish').update(published=True,status='verified',verification_status='verified'),'SO_DEPTH_PUBLISHED_TIER')
 r('SO_DEPTH_MISSING_ARTICLE',lambda d:d['claims'].__setitem__(slice(None),[c for c in d['claims'] if not (c['predicate']=='constitutional_provision' and c['value']['data']['article']=='9')]),'SO_CONSTITUTION_ARTICLES')
 r('SO_DEPTH_DROP_OFFICIAL_LANGUAGE',lambda d:d['claims'].__setitem__(slice(None),[c for c in d['claims'] if not (c['predicate']=='language_presence' and c['value']['data']['name']=='الصومالية')]),'SO_LANGUAGE_OFFICIAL')
 r('SO_DEPTH_BAD_SOURCE_REF',lambda d:clm(d,'unesco_tentative_listing',reference='6754').update(source_id='SRC-UNESCO-ICH-XEER-CIISE-02087-2024'),'SO_DEPTH_SOURCE_REFS')
 r('SO_DEPTH_MISSING_SOURCE_FILE',lambda d:d['sources'].__setitem__(slice(None),[s for s in d['sources'] if s['id']!='SRC-UNESCO-WH-SO-STATE-2026']),'SO_DEPTH_SOURCE_REFS')
 r('SO_DEPTH_DOMAIN_REGRESSION',lambda d:d['domain_status']['domains']['world_heritage'].update(status='not_imported_in_full_pilot_stage1'),'SO_DOMAIN_STATUS')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/somalia_negative_tests.json',{'schema_version':'2.0.0','country_code':'SO','status':'PASS' if ok else 'FAIL','required':23,'detected':sum(x['detected'] for x in o),'mutations':o});print([(x['mutation'],x['detected']) for x in o if not x['detected']]);print(sum(x['detected'] for x in o),'/',len(o));return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
