#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_somalia import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
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
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/somalia_negative_tests.json',{'schema_version':'2.0.0','country_code':'SO','status':'PASS' if ok else 'FAIL','required':10,'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
