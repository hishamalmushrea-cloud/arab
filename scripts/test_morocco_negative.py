#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_morocco import data,validate
def main():
 b=data();o=[]
 def r(n,fn,c):d=copy.deepcopy(b);fn(d);o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('MA_PREFECTURE_AS_PROVINCE',lambda d:next(x for x in d['entities'] if x['entity_type']=='ma_prefecture').update(entity_type='ma_province'),'MA_COUNTS')
 r('MA_WRONG_REGION',lambda d:next(x for x in d['relationships'] if 'PREFECTURE' in x['child_id']).update(parent_id='ENT-MA-REGION-ORIENTAL'),'MA_PARENT_SET')
 r('MA_75_TO_83',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-MA-PREFECTURES').update(value=21),'MA_DENOMINATORS')
 r('MA_FAKE_COMMUNE',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-MA-COMMUNE-X','entity_type':'ma_commune'}),'MA_PREMATURE_COMMUNE')
 r('MA_CLOSE_COMMUNES',lambda d:next(x for x in d['manifest']['hierarchy'] if x['entity_type']=='ma_commune').update(scope_status='closed'),'MA_COMMUNE_SCOPE')
 r('MA_DROP_REGION',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x['entity_type']!='ma_region']),'MA_COUNTS')
 r('MA_COUNT_TAMPER',lambda d:next(x for x in d['claims'])['value']['data'].update(ma_province=99),'MA_COUNT_CLAIM')
 r('MA_PARENT_MISSING',lambda d:d['relationships'].pop(),'MA_PARENT_SET')
 r('MA_DEPTH_PUBLISHED',lambda d:next(x for x in d['claims'] if x.get('predicate')=='food_dish').update(published=True),'MA_DEPTH_UNPUBLISHED')
 r('MA_COUSCOUS_EXCLUSIVE',lambda d:next(x for x in d['claims'] if x.get('predicate')=='food_dish' and x['value']['data'].get('name')=='الكسكس').update(classification='national'),'MA_COUSCOUS_SHARED')
 r('MA_DIALECT_PROMOTED',lambda d:next(x for x in d['claims'] if x.get('predicate')=='dialect_profile').update(verification_status='verified'),'MA_DEPTH_STATUS')
 r('MA_LANG_DROPPED',lambda d:d['claims'].__setitem__(slice(None),[x for x in d['claims'] if x.get('predicate')!='language_presence']),'MA_DEPTH_LANGS')
 ok=all(x['detected'] for x in o);write_json(ROOT/'reports/morocco_negative_tests.json',{'schema_version':'2.0.0','country_code':'MA','status':'PASS' if ok else 'FAIL','required':12,'detected':sum(x['detected'] for x in o),'mutations':o});print(o);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
