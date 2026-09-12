#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_iraq import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('IQ_18_CURRENT',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x['id']!='ENT-IQ-GOVERNORATE-19']),'IQ_COUNTS')
 r('IQ_HALABJA_PRE_2025',lambda d:next(x for x in d['entities'] if x['id']=='ENT-IQ-GOVERNORATE-19').update(valid_from='2014-01-01'),'IQ_HALABJA_LAW')
 r('IQ_DUPLICATE_KRI_HALABJA',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-IQ-KRI-HALABJA'}),'IQ_COUNTS')
 r('IQ_KRI_COUNT_3',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-IQ-KRI-PROFILE').update(value=3),'IQ_DENOMINATORS')
 r('IQ_WRONG_PROFILE',lambda d:next(x for x in d['claims'] if x['predicate']=='administrative_profile')['value'].update(data='kri'),'IQ_PROFILE')
 r('IQ_DISPUTED_WITHOUT_SOURCE',lambda d:next(x for x in d['entities'] if x['id']=='ENT-IQ-GOVERNORATE-04').update(status='disputed'),'IQ_UNSUPPORTED_OVERLAY')
 r('IQ_PREMATURE_SUBDISTRICT',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-IQ-SUBDISTRICT-X','entity_type':'iq_subdistrict'}),'IQ_PREMATURE_LOWER')
 r('IQ_REMOVE_LAW_CLAIM',lambda d:d['claims'].__setitem__(slice(None),[x for x in d['claims'] if x['predicate']!='federal_establishment_law']),'IQ_HALABJA_LAW')
 r('IQ_FABRICATED_QADA',lambda d:d['entities'].append({**next(x for x in d['entities'] if x['entity_type']=='iq_district'),'id':'ENT-IQ-DISTRICT-X','canonical_name':'قضاء مختلق'}),'IQ_COUNTS')
 r('IQ_QADA_PROMOTED',lambda d:next(x for x in d['entities'] if x['entity_type']=='iq_district' and x['verification_status']=='probable').update(verification_status='verified'),'IQ_QADA_FIXTURE')
 r('IQ_DISPUTED_ENTRY_UPGRADED',lambda d:next(x for x in d['entities'] if x['entity_type']=='iq_district' and x['verification_status']=='unverified').update(verification_status='probable'),'IQ_QADA_FIXTURE')
 r('IQ_QADA_POP_PUBLISHED',lambda d:next(x for x in d['claims'] if x.get('predicate')=='population').update(published=True),'IQ_QADA_POP')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/iraq_negative_tests.json',{'schema_version':'2.0.0','country_code':'IQ','status':'PASS' if ok else 'FAIL','required':12,'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
