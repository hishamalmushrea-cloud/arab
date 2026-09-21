#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_palestine import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('PS_GOVERNORATE_15',lambda d:d['entities'].pop(),'PS_COUNTS')
 r('PS_GAZA_AS_DEFACTO',lambda d:next(x for x in d['entities'] if x['id']=='ENT-PS-GOVERNORATE-60').update(status='de_facto'),'PS_UNSUPPORTED_STATUS')
 r('PS_DESTROYED_WITHOUT_SOURCE',lambda d:next(x for x in d['entities'] if x['id']=='ENT-PS-GOVERNORATE-55').update(status='destroyed'),'PS_UNSUPPORTED_STATUS')
 r('PS_WRONG_REGION',lambda d:next(x for x in d['claims'] if x['predicate']=='statistical_region')['value'].update(data='gaza_strip'),'PS_GOVERNORATE')
 r('PS_WHC_5_STALE',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-PS-WHC').update(value=5),'PS_DENOMINATORS')
 r('PS_SEBASTIA_NOT_DANGER',lambda d:next(x for x in d['claims'] if x['predicate']=='world_heritage_in_danger')['value'].update(data=False),'PS_SEBASTIA_STATUS')
 r('PS_SEBASTIA_UNDATED',lambda d:next(x for x in d['claims'] if x['predicate']=='emergency_inscription').update(observed_at=None),'PS_SEBASTIA_STATUS')
 r('PS_FAKE_LOCAL_AUTHORITY',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-PS-LOCAL-X','entity_type':'ps_local_government_unit'}),'PS_PREMATURE_LOCAL')
 r('PS_FABRICATED_SITE',lambda d:d['entities'].append({**next(x for x in d['entities'] if x['entity_type']=='historical_place'),'id':'ENT-PS-SITE-X','canonical_name':'قرية مختلقة'}),'PS_COUNTS')
 r('PS_SITE_MARKED_DESTROYED',lambda d:next(x for x in d['entities'] if x['entity_type']=='historical_place').update(status='destroyed'),'PS_HIST_FRAME')
 r('PS_SITE_PROMOTED_TO_VERIFIED',lambda d:next(x for x in d['entities'] if x['entity_type']=='historical_place').update(verification_status='verified'),'PS_HIST_FRAME')
 r('PS_SITE_ATTACHED_TO_CURRENT_TREE',lambda d:next(x for x in d['relationships'] if x.get('relationship_type')=='located_in').update(parent_id='ENT-PS-GOVERNORATE-01'),'PS_SITE_FIXTURE')
 r('PS_NAKBA_FRAME_PUBLISHED',lambda d:next(x for x in d['claims'] if x.get('predicate')=='depopulation_frame_1948').update(published=True),'PS_NAKBA_CLAIMS')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/palestine_negative_tests.json',{'schema_version':'2.0.0','country_code':'PS','status':'PASS' if ok else 'FAIL','required':13,'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
