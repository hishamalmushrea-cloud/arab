#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_algeria import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('DZ_FUTURE_AS_CURRENT',lambda d:next(x for x in d['entities'] if x.get('status')=='proposed').update(status='current'),'DZ_COUNTS')
 r('DZ_WRONG_EFFECTIVE_DATE',lambda d:next(x for x in d['entities'] if x.get('status')=='proposed').update(valid_from='2026-01-01'),'DZ_FUTURE_DATE')
 r('DZ_CURRENT_69',lambda d:next(x for x in d['manifest']['hierarchy'] if x['entity_type']=='dz_wilaya').update(denominator=69),'DZ_CURRENT_MANIFEST')
 r('DZ_DROP_FUTURE',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x.get('status')!='proposed']),'DZ_COUNTS')
 r('DZ_CLAIM_TAMPER',lambda d:next(x for x in d['claims'] if x['predicate']=='current_wilaya_count')['value'].update(data=69),'DZ_CLAIMS')
 r('DZ_DENOM_TAMPER',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-DZ-WILAYAS-CURRENT-2021').update(value=69),'DZ_DENOMINATORS')
 r('DZ_PREMATURE_COMMUNE',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-DZ-COMMUNE-X','entity_type':'dz_commune'}),'DZ_PREMATURE_LOWER')
 r('DZ_WRONG_PARENT',lambda d:next(x for x in d['relationships']).update(parent_id='ENT-DZ-WILAYA-01'),'DZ_PARENT')
 r('DZ_DEPTH_PUBLISHED',lambda d:next(x for x in d['claims'] if x.get('predicate')=='food_dish').update(published=True),'DZ_DEPTH_UNPUBLISHED')
 r('DZ_COUSCOUS_EXCLUSIVE',lambda d:next(x for x in d['claims'] if x.get('predicate')=='food_dish' and x['value']['data'].get('name')=='الكسكس').update(classification='national'),'DZ_SHARED_NOT_EXCLUSIVE')
 r('DZ_DIALECT_PROMOTED',lambda d:next(x for x in d['claims'] if x.get('predicate')=='dialect_profile').update(verification_status='verified'),'DZ_DEPTH_STATUS')
 r('DZ_LANG_DROPPED',lambda d:d['claims'].__setitem__(slice(None),[x for x in d['claims'] if x.get('predicate')!='language_presence']),'DZ_DEPTH_LANGS')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/algeria_negative_tests.json',{'schema_version':'2.0.0','country_code':'DZ','status':'PASS' if ok else 'FAIL','required':12,'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
