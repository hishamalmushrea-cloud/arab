#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_oman import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('OM_DROP_JABAL_AKHDAR',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x['id']!='ENT-OM-WILAYA-0509']),'OM_ADDITIONS')
 r('OM_DROP_SINAW',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x['id']!='ENT-OM-WILAYA-0907']),'OM_ADDITIONS')
 r('OM_WRONG_PARENT',lambda d:next(x for x in d['relationships'] if x['child_id']=='ENT-OM-WILAYA-0509').update(parent_id='ENT-OM-GOVERNORATE-09'),'OM_WILAYAT_PARENT')
 r('OM_LEGACY_61',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-OM-WILAYATS-2022').update(value=61),'OM_DENOMINATORS')
 r('OM_FAKE_NIYABAH',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-OM-NIYABA-X','entity_type':'om_niyaba'}),'OM_NIYABA')
 r('OM_FAKE_NIYABAH_DENOM',lambda d:next(x for x in d['manifest']['hierarchy'] if x['entity_type']=='om_niyaba').update(denominator=12,scope_status='closed'),'OM_NIYABA_DENOM')
 r('OM_OMIT_SADAH',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x['id']!='ENT-OM-WILAYA-0210']),'OM_DHOFAR')
 r('OM_QISHN_SILENT_RENAME',lambda d:next(x for x in d['entities'] if x['id']=='ENT-OM-WILAYA-0208').update(canonical_name='قشن'),'OM_DHOFAR')
 r('OM_DEPTH_PUBLISHED',lambda d:next(x for x in d['claims'] if x.get('predicate')=='food_dish').update(published=True),'OM_DEPTH_UNPUBLISHED')
 r('OM_HARES_EXCLUSIVE',lambda d:next(x for x in d['claims'] if x.get('predicate')=='food_dish' and x['value']['data'].get('name')=='الهريس').update(classification='national'),'OM_SHARED_NOT_EXCLUSIVE')
 r('OM_LANG_DROPPED',lambda d:d['claims'].__setitem__(slice(None),[x for x in d['claims'] if x.get('predicate')!='language_presence']),'OM_DEPTH_LANGS')
 r('OM_DIALECT_PROMOTED',lambda d:next(x for x in d['claims'] if x.get('predicate')=='dialect_profile').update(verification_status='verified'),'OM_DEPTH_STATUS')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/oman_negative_tests.json',{'schema_version':'2.0.0','country_code':'OM','status':'PASS' if ok else 'FAIL','required':12,'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
