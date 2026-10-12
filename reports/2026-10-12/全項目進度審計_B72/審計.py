from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import csv,json,hashlib,os,subprocess,sqlite3
工作=Path(__file__).resolve().parent;根=工作.parents[2];H=lambda b:hashlib.sha256(b).hexdigest()
表=根/'Reference/tables/94_全項目進度審計_B72_20261012';表.mkdir(parents=True,exist_ok=True)
def git(*a):return subprocess.check_output(['git',*a],cwd=根)
def 讀(p):
    with (根/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def 寫(n,rows,fields=None):
    with (表/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
assert not (工作/'基線.json').exists(),'不得刷新基線'
tracked={p for p in git('ls-files','-z').decode().split('\0') if p}
基={'提交':git('rev-parse','HEAD').decode().strip(),'上游提交':git('rev-parse','@{u}').decode().strip(),'初始工作區狀態':git('status','--porcelain').decode(),'既有正文':{p:H((根/p).read_bytes()) for p in tracked if p.endswith(('.md','.qmd')) and (根/p).is_file()}}
(工作/'基線.json').write_text(json.dumps(基,ensure_ascii=False,indent=2),encoding='utf-8')
文件=[];跳=[]
for directory,dirs,files in os.walk(根,followlinks=False):
    dirs[:]=[d for d in dirs if d!='.git' and not (Path(directory)/d).is_symlink()]
    for name in files:
        p=Path(directory)/name
        if p.is_symlink():跳.append({'路徑':p.relative_to(根).as_posix(),'原因':'符號連結不追蹤'});continue
        rel=p.relative_to(根).as_posix()
        if p.is_relative_to(工作) or p.is_relative_to(表):continue
        try:
            before=p.stat();h=hashlib.sha256()
            with p.open('rb') as f:
                for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
            after=p.stat()
            文件.append({'路徑':rel,'位元組':before.st_size,'SHA256':h.hexdigest(),'Git已追蹤':rel in tracked,'掃描期間穩定':(before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns)})
        except OSError as e:跳.append({'路徑':rel,'原因':type(e).__name__})
寫('全項目文件雜湊快照.csv',文件);寫('跳過與讀取失敗.csv',跳,['路徑','原因'])
print('完成文件快照',len(文件),flush=True)
金融=讀('Reference/tables/50_global_directory_content_b25_20261008/registry_all_4849_work_progress.csv')
逐國=讀('Reference/tables/50_global_directory_content_b25_20261008/registry_all_country_cumulative_source_progress.csv')
科技=讀('Reference/tables/07_global_technology_iso249_20261006/registry_country_technology_coverage.csv')
神經=讀('Reference/tables/07_global_technology_iso249_20261006/registry_neurotechnology_global.csv')
counts={'金融工作總項':len(金融),'金融已嘗試工作':sum(int(r['attempt_observations'] or 0)>0 for r in 金融),'金融末次HTTP200工作':sum(r['last_http_status']=='200' for r in 金融),'金融完整性狀態':dict(Counter(r['directory_completeness'] for r in 金融)),'金融逐國母表行':len(逐國),'金融上市公司完整性狀態':dict(Counter(r['listed_company_completeness'] for r in 逐國)),'金融券商完整性狀態':dict(Counter(r['broker_completeness'] for r in 逐國)),'科技逐國母表行':len(科技),'科技N0至N7狀態':dict(Counter(r['N0_N7_level'] for r in 科技)),'科技研究完成狀態':dict(Counter(r['research_completion_state'] for r in 科技)),'神經科技登記行':len(神經),'神經科技證據狀態':dict(Counter(r['evidence_state'] for r in 神經))}
html=[]
for r in 文件:
    p=根/r['路徑']
    if p.suffix.lower()=='.html' and '_files' not in '/'.join(p.parts) and (p.parent==根 or p.is_relative_to(根/'Reference')) and not p.with_suffix('.qmd').is_file():
        html.append({'HTML路徑':r['路徑'],'SHA256':r['SHA256'],'處置':'成品候選待人工分類；不直接認定來源遺失','同名QMD存在':False})
寫('無同名源文件的成品候選.csv',html,['HTML路徑','SHA256','處置','同名QMD存在'])
舊=json.loads((根/'reports/2026-10-07/git_publish_and_html_recovery/recovery_manifest.json').read_text(encoding='utf-8'))['records'];恢=[]
for r in 舊:
    p=根/r['html'];q=根/r['qmd']
    恢.append({'HTML路徑':r['html'],'QMD路徑':r['qmd'],'HTML存在':p.is_file(),'QMD存在':q.is_file(),'HTML與當時快照雜湊一致':p.is_file() and H(p.read_bytes())==r['sha256'],'核查邊界':'本輪檢查存在與快照；未重新渲染字節一致性'})
寫('歷史源文件重建成果現況.csv',恢)
近期=[]
for d in sorted((根/'reports').glob('2026-*/*')):
    if any(d.name.endswith('_B'+str(i)) for i in range(64,72)):
        p=d/'交付驗收.json'
        if p.exists():近期.append({'批次目錄':d.relative_to(根).as_posix(),'交付回執存在':True,'回執SHA256':H(p.read_bytes()),'核查結果存在':(d/'核查結果.json').exists(),'狀態':'回執存在不是全項目完成證明'})
寫('近期交付回執核對.csv',近期)
db=根/'Reference/tables/50_global_directory_content_b25_20261008/global_directory_content_b25.sqlite'
with sqlite3.connect(db.as_uri()+'?mode=ro',uri=True) as con:完整=con.execute('PRAGMA quick_check').fetchall()
counts.update({'文件快照行':len(文件),'文件快照不穩定數':sum(not r['掃描期間穩定'] for r in 文件),'文件跳過或失敗數':len(跳),'無同名QMD成品候選':len(html),'歷史重建清單行':len(恢),'歷史重建QMD缺失數':sum(not r['QMD存在'] for r in 恢),'歷史重建HTML較當時快照不同數':sum(not r['HTML與當時快照雜湊一致'] for r in 恢),'近期回執數':len(近期),'金融資料庫快速檢查':完整,'審計UTC':datetime.now(timezone.utc).isoformat(),'整體完成率可計算':False,'理由':'全球所有歷史政治實體、上市公司、券商、貨幣與科技項目的可信總分母尚未核定；不能用批次或來源行數當完成率'})
(工作/'審計結果.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(counts,ensure_ascii=False),flush=True)
