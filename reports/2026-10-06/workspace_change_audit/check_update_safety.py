"""Check document routing, preview-only default, and stale-baseline rejection.
Creates a baseline for this reviewed delivery, never writes report bodies.
"""
from pathlib import Path
import hashlib,json,subprocess,sys

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).parent
FRONTIER=ROOT/'reports/2026-10-06/frontier_ecosystem'
NEW='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd'
REF='Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before=json.loads((HERE/'before_summary.json').read_text(encoding='utf-8'))
import csv
inventory={r['path']:r for r in csv.DictReader((HERE/'before_files.csv').open(encoding='utf-8-sig'))}
protected=[p for p in inventory if p.startswith('Reference/Aerospace_Ecosystem_Report')]
assert all((ROOT/p).exists() and sha(ROOT/p)==inventory[p]['sha256'] for p in protected)
tables=list((ROOT/'Reference/tables/06_frontier_ecosystem_20261006').glob('*.csv'))
assert all(sha(p)==inventory[p.relative_to(ROOT).as_posix()]['sha256'] for p in tables)
managed=[NEW,REF,'Reference/tables/06_frontier_ecosystem_20261006/README.md',
    'reports/2026-10-06/frontier_ecosystem/review_receipt.json',
    *(p.relative_to(ROOT).as_posix() for p in tables)]
fingerprints={p:sha(ROOT/p) for p in managed}
run=subprocess.run([sys.executable,str(FRONTIER/'build_registry.py')],cwd=ROOT,capture_output=True,text=True)
assert run.returncode==0,run.stderr
assert all(sha(ROOT/p)==h for p,h in fingerprints.items()),'Default generation touched published outputs.'
proposal=FRONTIER/'preview'/NEW
assert proposal.exists() and not (FRONTIER/'preview/Reference/Aerospace_Ecosystem_Report.qmd').exists()
assert proposal.read_text(encoding='utf-8')==(ROOT/NEW).read_text(encoding='utf-8'), 'Report proposal differs from reviewed document.'
baseline={'created_on':'2026-10-06','git_head_at_review':before['head'],
    'report_role':'Frontier registry; never the historical aerospace comparison',
    'sha256':fingerprints}
(FRONTIER/'delivery_baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf-8')
# Supply a deliberately stale temporary baseline, not a modified real document.
stale=json.loads(json.dumps(baseline));stale['sha256'][NEW]='0'*64
test_path=HERE/'stale_test_baseline.json'
assert not test_path.exists(), 'Existing test baseline must not be overwritten.'
try:
    test_path.write_text(json.dumps(stale),encoding='utf-8')
    blocked=subprocess.run([sys.executable,str(FRONTIER/'build_registry.py'),'--apply','--baseline',str(test_path)],
        cwd=ROOT,capture_output=True,text=True)
    assert blocked.returncode!=0 and 'Refusing overwrite' in blocked.stderr
finally:
    test_path.unlink(missing_ok=True)
assert all(sha(ROOT/p)==h for p,h in fingerprints.items()),'Failed preflight modified outputs.'
assert all(sha(ROOT/p)==inventory[p]['sha256'] for p in protected)
result={'historical_report_and_assets_unchanged':True,'protected_files':len(protected),
    'registry_csv_unchanged':True,'default_preview_does_not_modify_delivery':True,
    'new_report_proposal_matches_reviewed_content':True,'stale_baseline_rejected_without_writes':True,
    'checked_on':'2026-10-06','deleted_legacy_md_not_restored':not (ROOT/'Reference/Aerospace_Ecosystem_Report.md').exists()}
(HERE/'safety_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
