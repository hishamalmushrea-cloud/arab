#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_mauritania import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('MR_NOUAKCHOTT_AS_NEIGHBORHOOD',lambda d:next(x for x in d['entities'] if 'Nouakchott' in x['canonical_name']).update(entity_type='neighborhood'),'MR_COUNTS')
 r('MR_WRONG_PROFILE',lambda d:next(x for x in d['claims'] if x['predicate']=='administrative_profile')['value'].update(data='wrong'),'MR_PROFILE')
 r('MR_MOUGHATAA_57',lambda d:next(x for x in d['claims'] if x['predicate']=='moughataa_count')['value'].update(data=57),'MR_COUNTS_CLAIMS')
 r('MR_COMMUNE_220_DEFAULT',lambda d:next(x for x in d['manifest']['hierarchy'] if x['entity_type']=='mr_commune').update(denominator=220),'MR_COMMUNE_CONFLICT')
 r('MR_COMMUNE_219_DEFAULT',lambda d:next(x for x in d['manifest']['hierarchy'] if x['entity_type']=='mr_commune').update(denominator=219),'MR_COMMUNE_CONFLICT')
 r('MR_PREMATURE_MOUGHATAA',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-MR-MOUGHATAA-X','entity_type':'mr_moughataa'}),'MR_PREMATURE_LOWER')
 r('MR_DENOM_16',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-MR-WILAYAS').update(value=16),'MR_DENOMINATORS')
 r('MR_CLOSE_MOUGHATAA_NO_RECORDS',lambda d:next(x for x in d['manifest']['hierarchy'] if x['entity_type']=='mr_moughataa').update(scope_status='closed'),'MR_MOUGHATAA_SCOPE')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/mauritania_negative_tests.json',{'schema_version':'2.0.0','country_code':'MR','status':'PASS' if ok else 'FAIL','required':8,'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
