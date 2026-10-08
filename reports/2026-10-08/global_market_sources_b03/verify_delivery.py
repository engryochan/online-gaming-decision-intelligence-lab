from pathlib import Path
import subprocess,json,hashlib,sqlite3,re,zipfile,io
O=Path(__file__).parent;R=O.parents[2]
audit_path=R/'reports/2026-10-07/git_publish_and_html_recovery/workspace_audit.json'
audit=audit_path.read_bytes()
(O/'credential_scan.json').write_bytes(audit)
# Restore only this turn's generated audit change, after saving the new result.
audit_path.write_bytes(subprocess.check_output(['git','show','HEAD:reports/2026-10-07/git_publish_and_html_recovery/workspace_audit.json'],cwd=R))
receipt=json.loads((O/'final_acceptance.json').read_text())
receipt.pop('old_source_files_unchanged',None)
receipt['preservation_scope']='ADDITIVE_NEW_OUTPUTS_OLD_SOURCE_FILES_NOT_WRITTEN'
receipt['interrupted_pending_responses']=1
old_changes=subprocess.check_output(['git','diff','--name-only'],cwd=R).decode().splitlines()
receipt['tracked_existing_file_changes']=old_changes
assert not old_changes
db=O/'global_source_registry_b03.sqlite';data=db.read_bytes()
pattern=re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|AKIA[A-Z0-9]{16}|sk-proj-[A-Za-z0-9_-]{30,}|xox[baprs]-[A-Za-z0-9-]{20,})')
hits=list(pattern.finditer(data));logical_hits=0
with sqlite3.connect(db) as con:
    assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    for hit in hits:
        value=hit.group().decode()
        for (table,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            for row in con.execute('PRAGMA table_info("'+table+'")').fetchall():
                logical_hits+=con.execute('SELECT COUNT(*) FROM "'+table+'" WHERE instr("'+row[1]+'",?)>0',(value,)).fetchone()[0]
assert logical_hits==0
receipt['credential_candidate_review']=dict(binary_token_pattern_hits=len(hits),logical_database_value_hits=logical_hits,
    decision='BINARY_SERIALIZATION_BOUNDARY_FALSE_POSITIVE_NO_MATCHING_DATABASE_VALUE',secret_values_disclosed=False)
receipt['qmd_html_created']=all((R/'Reference'/('Global_Market_Source_Coverage_B03_20261008'+s)).exists() for s in ('.qmd','.html'))
receipt['file_hashes']={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [db,R/'Reference/Global_Market_Source_Coverage_B03_20261008.qmd',R/'Reference/Global_Market_Source_Coverage_B03_20261008.html']}
(O/'final_acceptance.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=True))
