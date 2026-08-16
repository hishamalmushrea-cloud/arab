#!/usr/bin/env python3
"""Sudan production release gate layered after accepted Phase 5."""
import hashlib,json,subprocess,sys
from pathlib import Path
from model import ROOT,read_jsonl,write_json
MANAGED=['data/entities/entities.jsonl','data/aliases/aliases.jsonl','data/relationships/relationships.jsonl','data/claims/claims.jsonl','data/coverage/denominators.jsonl','data/coverage/coverage.jsonl','data/snapshots/snapshots.jsonl','manifests/SD.yml','data/cultural/sudan_domain_status.json','data/imports/sudan/source_catalog.json']
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
  if r.get('country_codes')==['SD']:out[str(p.relative_to(ROOT))]=sha(p)
 return out
def non_sudan_hash():
 e=read_jsonl(ROOT/'data/entities/entities.jsonl');ids={r['id'] for r in e if r.get('country_code')=='SD'};payload={'entities':[r for r in e if r['id'] not in ids],'aliases':[r for r in read_jsonl(ROOT/'data/aliases/aliases.jsonl') if r['entity_id'] not in ids],'relationships':[r for r in read_jsonl(ROOT/'data/relationships/relationships.jsonl') if r['child_id'] not in ids and r['parent_id'] not in ids],'claims':[r for r in read_jsonl(ROOT/'data/claims/claims.jsonl') if r['subject_id'] not in ids],'denominators':[r for r in read_jsonl(ROOT/'data/coverage/denominators.jsonl') if r['country_code']!='SD'],'coverage':[r for r in read_jsonl(ROOT/'data/coverage/coverage.jsonl') if r['country_code']!='SD'],'snapshots':[r for r in read_jsonl(ROOT/'data/snapshots/snapshots.jsonl') if not r['id'].startswith('SNP-SD-PRODUCTION-')]};return hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 g=Gate();before=source_hashes();g.command('sudan_source_refresh',[sys.executable,'scripts/build_sudan_sources.py']);after=source_hashes();g.require(len(after)==3 and before==after,'sudan_source_idempotence',f'atomic sources={len(after)}/3, unchanged={before==after}')
 bf,bo=hashes(),non_sudan_hash();g.command('sudan_import_refresh',[sys.executable,'scripts/import_sudan_production.py']);af,ao=hashes(),non_sudan_hash();g.require(bf==af,'sudan_import_idempotence',f'all {len(MANAGED)} managed hashes unchanged={bf==af}');g.require(bo==ao,'non_sudan_preservation',f'canonical non-Sudan SHA-256 unchanged={ao}')
 g.command('general_validation',[sys.executable,'scripts/validate.py']);g.command('sudan_semantic_validation',[sys.executable,'scripts/validate_sudan.py']);g.command('sudan_negative_tests',[sys.executable,'scripts/test_sudan_negative.py'])
 sample=ROOT/'data/review/sudan_review_samples.json';bs=sha(sample);g.command('sudan_review_sample_refresh',[sys.executable,'scripts/build_sudan_review_samples.py']);g.require(bs==sha(sample),'sudan_review_sample_idempotence',f'full-population sample unchanged={bs==sha(sample)}')
 br=sha(ROOT/'reports/sudan_independent_review.json');g.command('sudan_independent_review',[sys.executable,'scripts/review_sudan.py']);g.require(br==sha(ROOT/'reports/sudan_independent_review.json'),'sudan_review_idempotence',f'independent review unchanged={br==sha(ROOT/"reports/sudan_independent_review.json")}');g.command('generated_freshness',[sys.executable,'scripts/generate.py','--check'])
 v=json.loads((ROOT/'reports/sudan_validation.json').read_text());n=json.loads((ROOT/'reports/sudan_negative_tests.json').read_text());r=json.loads((ROOT/'reports/sudan_independent_review.json').read_text());g.require(v.get('status')=='PASS' and v.get('p0')==v.get('critical_p1')==0,'sudan_findings_closed',f"status={v.get('status')}, P0={v.get('p0')}, critical P1={v.get('critical_p1')}");g.require(n.get('status')=='PASS' and n.get('detected')==n.get('required')==9,'sudan_required_mutations',f"detected={n.get('detected')}/{n.get('required')}");g.require(r.get('status')=='PASS' and r.get('total_sampled')==r.get('total_passed')==68,'sudan_review_threshold',f"full review passed={r.get('total_passed')}/{r.get('total_sampled')}")
 for q in ['reports/SUDAN_PRODUCTION_CLOSEOUT.md','reports/LESSONS_LEARNED_SUDAN.md','reports/EXPANSION_LESSONS.md','reports/NEXT_COUNTRY_DECISION.md'] :g.require((ROOT/q).is_file(),'artifact_'+Path(q).stem.lower(),f'{q} exists')
 status=subprocess.run(['git','status','--porcelain'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip();g.require(not status,'sudan_clean_worktree',f'git worktree clean={not status}')
 report={'schema_version':'2.0.0','country_code':'SD','snapshot_date':'2026-08-17','status':'pass' if not g.errors else 'fail','checks':g.checks,'errors':g.errors};write_json(ROOT/'reports/sudan_gate.json',report)
 for name,res in g.checks.items():print(f"[{'PASS' if res['status']=='pass' else 'FAIL'}] {name}: {res.get('detail',res.get('command',''))}")
 if g.errors:
  for e in g.errors:print('- '+e,file=sys.stderr)
  return 1
 print(f'Sudan production gate passed ({len(g.checks)} checks).');return 0
if __name__=='__main__':raise SystemExit(main())
