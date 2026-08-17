#!/usr/bin/env python3
import copy
from model import ROOT,write_json
from validate_yemen import data,validate
def main():
 b=data(); o=[]
 def r(n,fn,c):
  d=copy.deepcopy(b); fn(d); o.append({'mutation':n,'expected_code':c,'detected':any(x['code']==c for x in validate(d))})
 r('YE_AMANAT_AS_GOVERNORATE_ALIAS',lambda d:d['aliases'].append({'entity_id':'ENT-YE-CAPITAL-MUNICIPALITY-01','name':'محافظة أمانة العاصمة'}),'YE_AMANAT_ALIAS')
 r('YE_SOCOTRA_REMOVED_FROM_CURRENT',lambda d:d['entities'].__setitem__(slice(None),[x for x in d['entities'] if x['id']!='ENT-YE-GOVERNORATE-22']),'YE_COUNTS')
 r('YE_LEGACY_DENOMINATOR_AS_CURRENT',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-YE-FIRST-LEVEL').update(value=21),'YE_DENOMINATORS')
 r('YE_LEGAL_LIST_AS_DE_FACTO',lambda d:next(x for x in d['entities'] if x['id']=='ENT-YE-GOVERNORATE-03').update(status='de_facto'),'YE_UNSUPPORTED_OVERLAY')
 r('YE_DESTROYED_WITHOUT_DATED_SOURCE',lambda d:next(x for x in d['entities'] if x['id']=='ENT-YE-GOVERNORATE-05').update(status='destroyed'),'YE_UNSUPPORTED_OVERLAY')
 r('YE_UNATTESTED_DISTRICT_ADDED',lambda d:d['entities'].append({**next(x for x in d['entities'] if x['entity_type']=='ye_district'),'id':'ENT-YE-DISTRICT-X','canonical_name':'مديرية مختلقة'}),'YE_COUNTS')
 r('YE_PREMATURE_UZLA',lambda d:d['entities'].append({**d['entities'][-1],'id':'ENT-YE-UZLA-X','entity_type':'ye_uzla'}),'YE_PREMATURE_LOWER')
 r('YE_DISTRICT_PROMOTED_TO_VERIFIED',lambda d:next(x for x in d['entities'] if x['entity_type']=='ye_district').update(verification_status='verified'),'YE_DISTRICT_STATUS')
 r('YE_DISTRICT_FRAME_SHRUNK',lambda d:next(x for x in d['denominators'] if x['id']=='DEN-YE-DISTRICTS').update(value=332),'YE_DENOMINATORS')
 r('YE_FABRICATED_LANE_ADDED',lambda d:d['entities'].append({**next(x for x in d['entities'] if x['entity_type']=='lane'),'id':'ENT-YE-LANE-X','canonical_name':'حارة مختلقة'}),'YE_COUNTS')
 r('YE_LANE_PROMOTED_TO_VERIFIED',lambda d:next(x for x in d['entities'] if x['entity_type']=='lane').update(verification_status='verified'),'YE_LANE_STATUS')
 r('YE_LANE_POP_PUBLISHED_AS_CURRENT',lambda d:next(x for x in d['claims'] if x.get('predicate')=='population' and x['subject_id'].startswith('ENT-YE-LANE')).update(published=True),'YE_LANE_POP')
 r('YE_NARRATIVE_PROMOTED_TO_FACT',lambda d:next(x for x in d['claims'] if x.get('predicate')=='name_origin_narrative').update(verification_status='verified'),'YE_LANE_NARRATIVE')
 r('YE_LANE_COVERAGE_FORCED_COMPLETE',lambda d:next(x for x in d['coverage'] if x['id']=='COV-YE-AMANAT-LANES').update(matched=791,missing=0,complete=True),'YE_LANE_COVERAGE')
 r('YE_WRONG_PARENT',lambda d:next(x for x in d['relationships'] if x['child_id']=='ENT-YE-GOVERNORATE-22').update(parent_id='ENT-YE-GOVERNORATE-04'),'YE_PARENT')
 r('YE_STALE_COVERAGE',lambda d:next(x for x in d['coverage'] if x['id']=='COV-YE-FIRST-LEVEL').update(snapshot_date='2013-12-18'),'YE_COVERAGE_FRESHNESS')
 r('YE_EFFECTIVE_CLAUSE_FABRICATED',lambda d:next(x for x in d['claims'] if x.get('predicate')=='establishment_instrument')['value']['data'].update(effective_clause_verified=True),'YE_SOCOTRA_LAW')
 ok=all(x['detected'] for x in o); write_json(ROOT/'reports/yemen_negative_tests.json',{'schema_version':'2.0.0','country_code':'YE','status':'PASS' if ok else 'FAIL','required':len(o),'detected':sum(x['detected'] for x in o),'mutations':o}); print(o); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
