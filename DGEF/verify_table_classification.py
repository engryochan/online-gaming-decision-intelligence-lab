"""Verify migration bytes, exhaustive table inventory and export layout."""
from pathlib import Path
import hashlib,json,sqlite3
from table_layout import table_category
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'reports/2026-10-04/table_reclassification'
rows=json.loads((OUT/'migration_manifest.json').read_text(encoding='utf-8'))
for r in rows:
    p=ROOT/r['new_path']
    assert p.is_file(),r
    assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],r
    assert p.stat().st_size==r['bytes'],r
    if r['moved']:assert not (ROOT/r['old_path']).exists(),r
c=sqlite3.connect((ROOT/'DGEF/artifacts/dgef.sqlite').as_uri()+'?mode=ro',uri=True)
names=[r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
for n in names:assert (ROOT/'DGEF/artifacts/tables'/table_category(n)/(n+'.csv')).is_file(),n
assert len(list((ROOT/'DGEF/artifacts/tables').rglob('*.csv')))==len(names)==44
assert not list((ROOT/'Reference').glob('*.csv'))
assert not list((ROOT/'Reference').glob('*.xlsx'))
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not c.execute('PRAGMA foreign_key_check').fetchall()
c.close()
result={'files_checked':len(rows),'files_moved':sum(r['moved'] for r in rows),'all_bytes_sha256_preserved':True,'classified_dgef_exports':44,'database_integrity':'ok','foreign_key_errors':[]}
(OUT/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
