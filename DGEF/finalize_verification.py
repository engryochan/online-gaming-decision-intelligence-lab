from pathlib import Path
import csv,json,hashlib,sqlite3,re
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'reports/2026-10-04/dgef'
ast=json.loads((OUT/'qmd_parse.json').read_text(encoding='utf-8'))
with (ROOT/'DGEF/contracts/data_dictionary.csv').open(encoding='utf-8-sig',newline='') as f:dictionary=list(csv.DictReader(f))
with (ROOT/'reports/2026-10-04/tables/04_file_audit/file_inventory.csv').open(encoding='utf-8-sig',newline='') as f:old=list(csv.DictReader(f))
originals=[r for r in old if not r['path'].startswith('.Rproj')]
layout=json.loads((ROOT/'reports/2026-10-04/table_reclassification/migration_manifest.json').read_text(encoding='utf-8'))
relocated={r['old_path']:r['new_path'] for r in layout}
changed=[r['path'] for r in originals if hashlib.sha256((ROOT/relocated.get(r['path'],r['path'])).read_bytes()).hexdigest()!=r['sha256']]
allowed={'README.md','_大秦赋算筹_v1_3_9.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.html'}
allowed.update(json.loads((ROOT/'reports/2026-10-04/table_reclassification/reference_updates.json').read_text(encoding='utf-8')))
allowed.add('.gitignore')
assert set(changed)<=allowed,changed
c=sqlite3.connect((ROOT/'DGEF/artifacts/dgef.sqlite').as_uri()+'?mode=ro',uri=True)
c.execute('PRAGMA foreign_keys=ON')
q=(ROOT/'_大秦赋算筹_v1_3_9.qmd').read_text(encoding='utf-8');chapters=[int(x) for x in re.findall(r'^# (\d+)\.',q,re.M)]
result=dict(original_project_files_checked=len(originals),authorized_modified_paths=changed,other_original_files_unchanged=True,pandoc_full_parse='PASS',pandoc_api_version=ast['pandoc-api-version'],top_level_numbered_chapters=chapters,data_dictionary_columns=len(dictionary),table_exports=len(list((ROOT/'DGEF/artifacts/tables').rglob('*.csv'))),db_integrity=c.execute('PRAGMA integrity_check').fetchone()[0],foreign_key_errors=c.execute('PRAGMA foreign_key_check').fetchall(),quarto_execution='NOT_RUN')
assert result['db_integrity']=='ok' and not result['foreign_key_errors']
assert result['table_exports']==44
(OUT/'final_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
c.close();(OUT/'qmd_parse.json').unlink()
print(json.dumps(result,ensure_ascii=True,indent=2))
