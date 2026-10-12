from pathlib import Path
import csv,json,hashlib,subprocess,importlib.util
工作=Path(__file__).resolve().parent;根=工作.parents[2];表=根/'Reference/tables/95_全球金融未嘗試來源續查_B73_20261012'
def 讀(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
基=json.loads((工作/'基線.json').read_text(encoding='utf-8'))
原=根/'Reference/tables/50_global_directory_content_b25_20261008/registry_all_4849_work_progress.csv'
assert hashlib.sha256(原.read_bytes()).hexdigest()==基['來源SHA256']
舊=讀(原);新=讀(表/'全4849項接續進度.csv');收=讀(表/'來源取得收據.csv');選=讀(表/'本輪選定來源.csv')
assert len(新)==len(舊)==4849 and len(收)==len(選)==120
assert {x['work_id'] for x in 收}=={x['work_id'] for x in 選}
ids={x['work_id'] for x in 收}
for a,b in zip(舊,新):
    assert a['work_id']==b['work_id'] and a['target_url']==b['target_url']
    assert int(b['attempt_observations'] or 0)==int(a['attempt_observations'] or 0)+(a['work_id'] in ids)
    assert a['completeness']==b['completeness'] and a['directory_completeness']==b['directory_completeness']
for x in 收:
    assert x['checked_on']=='2026-10-12'
    if x.get('file'):assert hashlib.sha256((根/x['file']).read_bytes()).hexdigest()==x['sha256']
assert not subprocess.check_output(['git','diff',基['提交'],'--','*.md','*.qmd'],cwd=根),'既有正文有變動'
範圍=[工作.relative_to(根).as_posix(),表.relative_to(根).as_posix(),'Reference/全球金融未嘗試來源續查_B73_20261012.qmd','Reference/全球金融未嘗試來源續查_B73_20261012.html','Reference/全球金融未嘗試來源續查_B73_20261012_files','.gitignore','.gitattributes']+[p+'/全球金融未嘗試來源續查_B73_20261012.md' for p in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']]
spec=importlib.util.spec_from_file_location('安全核查',根/'reports/2026-10-11/未啟動服務替代來源核查_B65/驗證與提交.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.工作=工作;m.範圍=範圍;m.密碼掃描()
assert (根/'Reference/全球金融未嘗試來源續查_B73_20261012.html').stat().st_size>1000
(工作/'交付驗收.json').write_text(json.dumps({'原工作項保留':4849,'新增嘗試':120,'完整性升級':0,'原來源保留':True,'既有正文保留':True,'來源雜湊通過':True,'隔離頁':6},ensure_ascii=False,indent=2),encoding='utf-8')
print('本輪全量對賬、原文保留、來源雜湊及密碼掃描通過。')
