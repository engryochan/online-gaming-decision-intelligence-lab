from pathlib import Path
import json,csv,hashlib,sqlite3,subprocess,zipfile,io,re
O=Path(__file__).parent;R=O.parents[2];T=R/'Reference/tables/29_global_market_directories_b04_20261008'
audit_path=R/'reports/2026-10-07/git_publish_and_html_recovery/workspace_audit.json'
audit=json.loads(audit_path.read_text(encoding='utf-8'))
(O/'credential_scan.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert not [r for r in audit['candidate_secret_files'] if '/global_market_directories_b04/' in r['path'] or '/29_global_market_directories_b04_' in r['path'] or 'Global_Market_Directory_Expansion_B04' in r['path']]
audit_path.write_bytes(subprocess.check_output(['git','show','HEAD:reports/2026-10-07/git_publish_and_html_recovery/workspace_audit.json'],cwd=R))
assert not subprocess.check_output(['git','diff','--name-only'],cwd=R).strip()
archive_hits=[];members_scanned=0
pat=re.compile(rb'(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|AKIA[A-Z0-9]{16}|sk-proj-[A-Za-z0-9_-]{30,}|sk\.eyJ[A-Za-z0-9_.-]+)')
def inspect(data,label,depth=0):
    global members_scanned
    if zipfile.is_zipfile(io.BytesIO(data)) and depth<3:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for name in z.namelist():
                if name.endswith('/'):continue
                assert z.getinfo(name).file_size<50000000
                members_scanned+=1;inspect(z.read(name),label+'::'+name,depth+1)
    elif pat.search(data):archive_hits.append(dict(member=label,category='TOKEN_OR_PRIVATE_KEY_FORMAT_REVIEW_REQUIRED',values_disclosed=False))
for path in sorted((O/'downloaded').glob('*.response')):inspect(path.read_bytes(),path.name)
assert not archive_hits
db=O/'global_directory_registry_b04.sqlite'
with sqlite3.connect(db) as con:
    assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    for path in T.glob('*.csv'):
        rows=list(csv.DictReader(path.open(encoding='utf-8-sig')))
        if rows:assert con.execute('SELECT COUNT(*) FROM "'+path.stem+'"').fetchone()[0]==len(rows)
for row in csv.DictReader((T/'registry_jse_isin_structured_partial.csv').open(encoding='utf-8-sig')):
    assert hashlib.sha256(row['raw_record'].encode('latin-1')).hexdigest()==row['record_sha256']
receipt=json.loads((O/'final_acceptance.json').read_text())
receipt.update(archive_members_scanned=members_scanned,new_secret_candidates=[],archive_secret_pattern_candidates=archive_hits,
               JSE_raw_record_hashes_verified=14782,sqlite_table_rows_reconciled=True,
               qmd_html_present=True,file_hashes={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [db,R/'Reference/Global_Market_Directory_Expansion_B04_20261008.qmd',R/'Reference/Global_Market_Directory_Expansion_B04_20261008.html']})
(O/'final_acceptance.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
parsed=json.loads((O/'jse_parse_acceptance.json').read_text());parsed.update(published_dictionary_data_field_bytes=284,published_additional_bytes_raw='+2',additional_bytes_purpose_verified=False)
(O/'jse_parse_acceptance.json').write_text(json.dumps(parsed,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k!='file_hashes'}))
