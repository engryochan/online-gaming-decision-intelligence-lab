"""Independent coverage, recovery and untouched-file checks; never repairs inputs."""
from pathlib import Path
import csv, hashlib, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
plan=json.loads((OUT/'delivery_plan.json').read_text(encoding='utf-8'))
manifest=list(csv.DictReader((OUT/'source_manifest.csv').open(encoding='utf-8-sig')))
ledger=list(csv.DictReader((OUT/'block_coverage.csv').open(encoding='utf-8-sig')))
preview='--preview' in sys.argv
targetroot=OUT/'preview' if preview else ROOT
targets={p:(targetroot/p).read_bytes() for p in plan['families']}
errors=[]
recovered={}
for p,meta in plan['families'].items():
    raw=targets[p]
    if sha(raw)!=meta['output_sha256']: errors.append('output hash: '+p)
    start=raw.index(b'\n<!-- INTEGRATION_20261007_BEGIN -->')
    end=raw.index(b'<!-- INTEGRATION_20261007_END -->\n')+len(b'<!-- INTEGRATION_20261007_END -->\n')
    annex=raw.index(b'\n<!-- SOURCE_ANNEX_20261007_BEGIN -->')
    original=raw[:start]+raw[end:annex]
    recovered[p]=original.decode('utf-8-sig')
    if sha(original)!=meta['original_sha256']: errors.append('original recovery: '+p)
texts={p:b.decode('utf-8-sig') for p,b in targets.items()}
sources={}
for m in manifest:
    archive=(ROOT/m['snapshot']).read_bytes()
    if sha(archive)!=m['sha256']: errors.append('archive hash: '+m['path'])
    sources[m['path']]=archive.decode('utf-8-sig').splitlines(keepends=True)
for r in ledger:
    lines=sources[r['source']]; offset=int(r['source_line'])-1; remain=int(r['characters']); block=''
    while remain:
        part=lines[offset][:remain]; block+=part; remain-=len(part); offset+=1
    if sha(block.encode())!=r['block_sha256']: errors.append('source block hash: '+r['source'])
    shown=re.sub(r'https?://[^\s<>\]\)]+',lambda m: m.group(0).split('?')[0]+'?[SIGNED_QUERY_REDACTED]' if re.search(r'(?i)(signature=|x-amz-|sig=|token=|credential=)',m.group(0)) else m.group(0),block)
    if block not in texts[r['target']] and shown not in texts[r['target']] and block not in recovered[r['target']]: errors.append('uncovered: '+r['source']+':'+r['source_line'])
unchanged=0; runtime_changes=[]
for row in csv.DictReader((ROOT/plan['baseline']).open(encoding='utf-8-sig')):
    p=row['path']
    if p in plan['families']: continue
    f=ROOT/p
    if not f.exists() or sha(f.read_bytes())!=row['sha256']:
        if p.startswith('.Rproj.user/') or p=='.Rhistory': runtime_changes.append(p)
        else: errors.append('unexpected baseline mutation: '+p)
    else: unchanged+=1
if (ROOT/'Reference/Report-Optimized-V2.md').exists(): errors.append('user-deleted file restored')
receipt=dict(mode='preview' if preview else 'delivered',status='PASS' if not errors else 'FAIL',coverage_records_checked=len(ledger),original_targets_recovered=len(targets),unchanged_baseline_files=unchanged,runtime_changes=runtime_changes,errors=errors,external_fact_check='PARTIAL',business_semantics='REVIEW_REQUIRED')
(OUT/('preview_validation.json' if preview else 'independent_validation.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
if errors: raise SystemExit(1)
