#!/usr/bin/env python3
"""United Arab Emirates depth-cycle release gate layered after accepted Phase 5."""
import hashlib,json,subprocess,sys
from pathlib import Path
from model import ROOT,read_jsonl,write_json
MANAGED=['data/entities/entities.jsonl','data/aliases/aliases.jsonl','data/relationships/relationships.jsonl','data/claims/claims.jsonl','data/coverage/denominators.jsonl','data/coverage/coverage.jsonl','data/snapshots/snapshots.jsonl','manifests/AE.yml','data/cultural/uae_domain_status.json','data/imports/uae/fixtures/source_catalog.json','data/imports/uae/snapshot_manifest.json','data/imports/uae/fixtures/administrative_profile.json','data/imports/uae/fixtures/cultural_claims.json','data/imports/uae/fixtures/cultural_depth_2026.json']
DEPTH_LAYERS={'unesco_intangible_heritage','world_heritage_inscribed','world_heritage_tentative_list','heritage_places','classified_local_knowledge'}
class Gate:
 def __init__(self): self.checks,self.errors={},[]
 def require(self,ok,name,detail):
  self.checks[name]={'status':'pass' if ok else 'fail','detail':detail}
  if not ok:self.errors.append(f'{name}: {detail}')
 def command(self,name,command):
  r=subprocess.run(command,cwd=ROOT,text=True,capture_output=True);display=['python3',*command[1:]] if command and command[0]==sys.executable else command;self.checks[name]={'status':'pass' if not r.returncode else 'fail','command':' '.join(display),'returncode':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip()}
  if r.returncode:self.errors.append(f'{name}: exit {r.returncode}')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hashes():return {p:sha(ROOT/p) for p in MANAGED}
def source_hashes():
 out={}
 for p in sorted((ROOT/'data/sources').glob('*.json')):
  r=json.loads(p.read_text(encoding='utf8'))
  if 'AE' in (r.get('country_codes') or []):out[str(p.relative_to(ROOT))]=sha(p)
 return out
def non_uae_hash():
 e=read_jsonl(ROOT/'data/entities/entities.jsonl');ids={r['id'] for r in e if r.get('country_code')=='AE'};payload={'entities':[r for r in e if r['id'] not in ids],'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r['entity_id'] not in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r['child_id'] not in ids and r['parent_id'] not in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r['subject_id'] not in ids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r['country_code']!='AE'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r['country_code']!='AE'],'snapshots':[r for r in read_jsonl(ROOT/'data/snapshots/snapshots.jsonl') if not r['id'].startswith('SNP-AE-')]};return hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 g=Gate();before=source_hashes();g.command('uae_source_refresh',[sys.executable,'scripts/build_uae_sources.py']);after=source_hashes();g.require(len(after)==27 and before==after,'uae_source_idempotence',f'AE-scoped atomic sources={len(after)}/27, unchanged={before==after}')
 bf,bo=hashes(),non_uae_hash();g.command('uae_import_refresh',[sys.executable,'scripts/import_uae_phase5.py']);af,ao=hashes(),non_uae_hash();g.require(bf==af,'uae_import_idempotence',f'all {len(MANAGED)} managed hashes unchanged={bf==af}');g.require(bo==ao,'non_uae_preservation',f'canonical non-UAE SHA-256 unchanged={ao}')
 g.command('general_validation',[sys.executable,'scripts/validate.py']);g.command('uae_semantic_validation',[sys.executable,'scripts/validate_uae.py']);g.command('uae_negative_tests',[sys.executable,'scripts/test_uae_negative.py'])
 sample=ROOT/'reports/uae_review_samples.json';bs=sha(sample);g.command('uae_review_sample_refresh',[sys.executable,'scripts/build_uae_review_samples.py']);g.require(bs==sha(sample),'uae_review_sample_idempotence',f'full-population sample unchanged={bs==sha(sample)}')
 br=sha(ROOT/'reports/uae_independent_review.json');g.command('uae_independent_review',[sys.executable,'scripts/review_uae.py']);g.require(br==sha(ROOT/'reports/uae_independent_review.json'),'uae_review_idempotence',f'independent review unchanged={br==sha(ROOT/"reports/uae_independent_review.json")}');g.command('generated_freshness',[sys.executable,'scripts/generate.py','--check'])
 v=json.loads((ROOT/'reports/uae_validation.json').read_text());n=json.loads((ROOT/'reports/uae_negative_tests.json').read_text());r=json.loads((ROOT/'reports/uae_independent_review.json').read_text());m=json.loads((ROOT/'manifests/AE.yml').read_text())
 g.require(v.get('status')=='PASS' and v.get('p0')==v.get('critical_p1')==0,'uae_findings_closed',f"status={v.get('status')}, P0={v.get('p0')}, critical P1={v.get('critical_p1')}")
 d=v.get('checks',{}).get('depth',{});g.require(d.get('claims')==70 and d.get('published')==33 and d.get('unpublished')==37 and d.get('national_elements')==1 and d.get('deferred_files')==13 and d.get('tentative_files')==15 and d.get('places')==3,'uae_depth_cycle_shape',f"depth claims={d.get('claims')} published={d.get('published')} national={d.get('national_elements')} deferred={d.get('deferred_files')} tentative={d.get('tentative_files')} places={d.get('places')}")
 g.require(n.get('status')=='PASS' and n.get('detected')==n.get('required')==27,'uae_required_mutations',f"detected={n.get('detected')}/{n.get('required')}")
 g.require(r.get('status')=='PASS' and r.get('total_sampled')==r.get('total_passed')==45,'uae_review_threshold',f"full review passed={r.get('total_passed')}/{r.get('total_sampled')}")
 snaps={r.get('id'):r for r in read_jsonl(ROOT/'data/snapshots/snapshots.jsonl') if str(r.get('id','')).startswith('SNP-AE-')}
 g.require({l.get('layer') for l in m.get('pilot_layers',[])}>=DEPTH_LAYERS and m.get('snapshot',{}).get('snapshot_id')=='SNP-AE-PILOT-20260815' and set(snaps)=={'SNP-AE-PILOT-20260815','SNP-AE-DEPTH-20260923'} and snaps['SNP-AE-DEPTH-20260923'].get('captured_at')=='2026-09-23','uae_depth_layers_declared',f"layers={len(m.get('pilot_layers',[]))}, pilot={m.get('snapshot',{}).get('snapshot_id')}, snapshots={sorted(snaps)}")
 for q in ['reports/UAE_PILOT_FINAL.md','reports/UAE_DEPTH_CLOSEOUT.md','reports/NEXT_COUNTRY_DECISION.md']:g.require((ROOT/q).is_file(),'artifact_'+Path(q).stem.lower(),f'{q} exists')
 status=subprocess.run(['git','status','--porcelain'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip();g.require(not status,'uae_clean_worktree',f'git worktree clean={not status}')
 report={'schema_version':'2.0.0','country_code':'AE','snapshot_date':'2026-08-15','depth_snapshot_date':'2026-09-23','status':'pass' if not g.errors else 'fail','checks':g.checks,'errors':g.errors};write_json(ROOT/'reports/uae_gate.json',report)
 for name,res in g.checks.items():print(f"[{'PASS' if res['status']=='pass' else 'FAIL'}] {name}: {res.get('detail',res.get('command',''))}")
 if g.errors:
  for e in g.errors:print('- '+e,file=sys.stderr)
  return 1
 print(f'UAE depth-cycle gate passed ({len(g.checks)} checks).');return 0
if __name__=='__main__':raise SystemExit(main())
