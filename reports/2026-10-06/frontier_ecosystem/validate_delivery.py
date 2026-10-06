"""Read-only checks of delivery files; write audit receipts only.
Never restore deleted files, normalize source files, or regenerate documents.
"""
from pathlib import Path
import csv, hashlib, json, re

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'Reference/tables/06_frontier_ecosystem_20261006'
def read(name):
    return list(csv.DictReader((OUT/name).open(encoding='utf-8-sig')))
entities=read('registry_frontier_organizations.csv')
claims=read('registry_frontier_claims.csv')
sources=read('registry_frontier_sources.csv')
eids={e['entity_id'] for e in entities}; sids={s['source_id'] for s in sources}
assert len(eids)==len(entities)==196
assert len({c['claim_id'] for c in claims})==len(claims)==196
assert len(sids)==len(sources)
assert all(c['entity_id'] in eids for c in claims)
assert all(not c['source_id'] or c['source_id'] in sids for c in claims)
assert sum(c['evidence_state']=='VERIFIED' for c in claims)==83
assert all(c['performance_state']==c['deployment_state']==c['regulatory_state']=='UNKNOWN' for c in claims)
report=ROOT/'Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd'
text=report.read_text(encoding='utf-8')
assert set(re.findall(r'\| (FRO\d{4}) \|',text))==eids
assert len(re.findall(r'\| (FRO\d{4}) \|',text))==196
for line in text.splitlines():
    if line.startswith('| FRO'):
        assert line.count('|')==6, line[:80]
ref=ROOT/'Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd'
assert ref.read_text(encoding='utf-8').count('<!-- FRONTIER_REVIEW_20261006_START -->')==1
htmls=[report.with_suffix('.html'),ref.with_suffix('.html')]
for p in htmls:
    data=p.read_text(encoding='utf-8')
    assert 'sec-frontier-review' in data if p==htmls[1] else 'FRO0196' in data
    assert '<html' in data

result={'checked_on':'2026-10-06','organizations':196,'verified_public_descriptions':83,
        'unknown':113,'checks':{'unique_ids_and_foreign_keys':True,'report_csv_row_parity':True,
        'markdown_table_shape':True,'review_index_unique':True,'both_html_rendered':True},
        'render_warning':'Quarto zh-TW translation fallback warning; HTML created successfully',
        'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in [report,ref,*htmls]},
        'scope_limit':'Structural acceptance and public-description review; not exhaustive global coverage or independent performance validation'}
(Path(__file__).parent/'acceptance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
receipt=Path(__file__).parent/'review_receipt.json'
r=json.loads(receipt.read_text(encoding='utf-8'));r['render_status']='BOTH_HTML_RENDERED_NO_EXECUTE_FOR_REFERENCE'
receipt.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in {'sha256','restored_previous_tracked_assets'}},ensure_ascii=False))
