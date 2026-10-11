from pathlib import Path
import hashlib, json, csv, subprocess, sys

O=Path(__file__).resolve().parent
R=O.parents[2]
def sha(data): return hashlib.sha256(data).hexdigest()
base=json.loads((O/'baseline.json').read_text(encoding='utf-8'))
app=base['authorized_append']; data=(R/app['path']).read_bytes()
assert sha(data[:app['prefix_bytes']])==app['prefix_sha256']
receipt=json.loads((O/'append_receipt.json').read_text(encoding='utf-8'))
assert sha(data[app['prefix_bytes']:])==receipt['append_sha256']
changed=[p for p,h in base['protected'].items() if p!=app['path'] and (not (R/p).is_file() or sha((R/p).read_bytes())!=h)]
assert not changed, 'Protected documents changed after this batch began: '+repr(changed)
assert not json.loads((O/'credential_scan.json').read_text())['candidates'], 'Credential candidate requires review'
rows=list(csv.DictReader((R/'Reference/tables/75_access_resolution_b52_20261011/registry_source_receipts.csv').open(encoding='utf-8-sig')))
stats=json.loads((O/'validation_receipt.json').read_text())
assert len(rows)==stats['source_receipts']
assert stats['starshield_visible_page_observed']
assert stats['noaa_2019_objects']==365 and stats['partial_csv_columns']>0
for name in ['registry_esri_catalog.csv','registry_esri_item_terms.csv','registry_esri_service_schema.csv','preserved_registry_commercial_products.csv','preserved_registry_product_workqueue.csv','preserved_registry_preserved_498_asf_work.csv']:
    prior=list(csv.DictReader((R/'Reference/tables/74_platform_details_b51_20261011'/name).open(encoding='utf-8-sig')))
    carried=list(csv.DictReader((R/'Reference/tables/75_access_resolution_b52_20261011'/('preserved_'+name)).open(encoding='utf-8-sig')))
    assert prior==carried
range_row=next(r for r in rows if r['source_id']=='B52NOAAZIPHEADER')
assert range_row['http_status']=='206' and range_row['saved_bytes']=='65536' and range_row['partial_response']=='True'
for row in rows:
    if not row['source_file']: continue
    assert sha((R/row['source_file']).read_bytes())==row['sha256']
    if row.get('evidence_scope','NEW_FETCH')=='PRIOR_FETCH_LOCAL_BYTES_CHECKED':
        assert sha(subprocess.check_output(['git','show','HEAD:'+row['source_file']],cwd=R))==row['sha256']
if '--preflight' not in sys.argv:
    from publish import SCOPES
    names=[n for n in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).decode().split('\0') if n]
    assert names and all(any(n==s or n.startswith(s+'/') for s in SCOPES) for n in names), 'Unexpected staged path'
    # Compare through Git's configured clean filters; prior raw evidence above
    # is independently checked with SHA256 and is never newline-normalized.
    for n in names:
        expected=subprocess.check_output(['git','hash-object','--path='+n,n],cwd=R).strip()
        actual=subprocess.check_output(['git','rev-parse',':'+n],cwd=R).strip()
        assert expected==actual, 'Staged content differs after configured Git filters: '+n
    for row in rows:
        if row.get('evidence_scope','NEW_FETCH')=='NEW_FETCH' and row['source_file']:
            assert sha(subprocess.check_output(['git','show',':'+row['source_file']],cwd=R))==row['sha256'], 'Raw evidence bytes changed in index'
    acceptance=dict(staged_files=len(names),other_protected_document_hashes_unchanged=True,
                    authorized_main_append_only=True,original_main_prefix_sha256_verified=True,
                    starting_worktree_status=base['starting_status'],source_receipt_rows=len(rows),
                    verified_source_files=sum(bool(r['source_file']) for r in rows),raw_staged_sha256_verified=True,
                    credential_candidates=0,staged_scope_verified=True,staged_git_filtered_content_verified=True)
    (O/'staged_acceptance.json').write_text(json.dumps(acceptance,indent=2)+'\n',encoding='utf-8')
print('PASS: current baseline, prior source bytes, credentials and applicable staging checks')
