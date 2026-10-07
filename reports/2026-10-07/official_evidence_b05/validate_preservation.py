from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
AUDIT=ROOT/'reports/2026-10-06/workspace_change_audit'
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
old={r['path']:r for r in read(AUDIT/'official_evidence_b05_20261007_start_files.csv')}
new={r['path']:r for r in read(AUDIT/'official_evidence_b05_20261007_finish_files.csv')}
changed=[p for p in old if p in new and old[p]['sha256']!=new[p]['sha256']]
deleted=sorted(old.keys()-new.keys())
receipts=json.loads((OUT/'append_receipt.json').read_text(encoding='utf-8'))
allowed={r['path'] for r in receipts}
runtime=[p for p in changed if p.startswith('.Rproj.user/')]
unexpected=[p for p in changed if p not in allowed and p not in runtime]
assert not deleted and not unexpected,(deleted,unexpected)
for r in receipts:
    p=ROOT/r['path'];original=(OUT/'originals'/p.name).read_bytes()
    assert p.read_bytes().startswith(original)
for r in read(OUT/'baseline_manifest.csv'):
    assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256']
assert (ROOT/'Reference/Official_Evidence_B05_20261007.html').exists()
result=dict(pass_check=True,changed_existing_files=changed,deleted_existing_files=deleted,unexpected_changes=unexpected,rstudio_runtime_changes_not_attributed_to_this_batch=runtime,baseline_and_prior_batches_unchanged=True,old_html_unchanged=True,original_aerospace_unchanged=True,appended_original_bytes_preserved=True,new_html_rendered=True,scan_limit='RStudio lock skipped; runtime changes recorded separately; hash inventory is not semantic verification')
(OUT/'final_acceptance.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
