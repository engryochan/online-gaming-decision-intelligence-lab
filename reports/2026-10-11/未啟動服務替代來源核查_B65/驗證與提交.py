from pathlib import Path
import csv, json, hashlib, subprocess, sys, argparse, re, zipfile, io

工作=Path(__file__).resolve().parent;根=工作.parents[2]
表=根/'Reference/tables/88_未啟動服務替代來源核查_B65_20261011'
主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd'
範圍=[主,'.gitattributes',工作.relative_to(根).as_posix(),表.relative_to(根).as_posix(),'Reference/未啟動服務替代來源核查_B65_20261011.qmd','Reference/未啟動服務替代來源核查_B65_20261011.html']+[p+'/未啟動服務替代來源核查_B65_20261011.md' for p in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']]
範圍.append('中文交付與中譯規則.md')
雜湊=lambda b:hashlib.sha256(b).hexdigest()
def 逐步執行(命令集,執行器=subprocess.run):
    for 命令 in 命令集:
        結果=執行器(命令,cwd=根,check=True,capture_output=True)
        print('版本控制步驟完成：'+{'add':'暫存','commit':'提交','push':'推送'}.get(命令[1] if len(命令)>1 else '', '核查'))
def 讀表(名稱):
    with (表/名稱).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def 密碼掃描():
    原碼=(根/'reports/2026-10-07/git_publish_and_html_recovery/audit.py').read_text(encoding='utf-8')
    ns={'re':re};exec(原碼[原碼.index('patterns='):原碼.index('for name in paths:')],ns)
    發現=[];數量=0
    for 範 in 範圍:
        p=根/範
        for f in (p.rglob('*') if p.is_dir() else [p]):
            if not f.is_file() or '__pycache__' in f.parts or f.name=='密碼掃描.json':continue
            數量+=1;b=f.read_bytes();decoded=re.sub(rb'\\x([0-9a-fA-F]{2})',lambda m:bytes([int(m[1],16)]),b)
            decoded=re.sub(rb'\\u00([0-9a-fA-F]{2})',lambda m:bytes([int(m[1],16)]),decoded)
            hits=set()
            for kind,pattern in ns['patterns']:
                for match in pattern.finditer(decoded):
                    value=match[1] if kind=='CREDENTIAL_LITERAL' else match[0];low=value.decode('utf-8','ignore').lower().strip()
                    if kind=='CREDENTIAL_LITERAL' and (low in ns['placeholders'] or low.startswith(('your_','your-','${','{{','<','process.env','os.environ')) or len(low)>256):continue
                    hits.add(kind)
            if hits:發現.append({'路徑':f.relative_to(根).as_posix(),'類型':sorted(hits),'狀態':'待人工覆核，禁止提交，不顯示值'})
    (工作/'密碼掃描.json').write_text(json.dumps({'掃描文件':數量,'候選':發現,'密碼值披露':False},ensure_ascii=False,indent=2),encoding='utf-8')
    assert not 發現,'發現密碼候選，停止提交與推送'
    print('密碼掃描通過；未發現候選。')
def 核查(暫存=False):
    基=json.loads((工作/'基線.json').read_text(encoding='utf-8'));data=(根/主).read_bytes();n=基['原文位元組']
    assert 雜湊(data[:n])==基['原文雜湊'],'主報告原文有變更，停止'
    assert 雜湊(data[n:])==json.loads((工作/'附加收據.json').read_text(encoding='utf-8'))['附加雜湊']
    assert all((根/p).is_file() and 雜湊((根/p).read_bytes())==h for p,h in 基['原有文件'].items() if p!=主),'原有文件有變更，停止'
    結=json.loads((工作/'核查結果.json').read_text(encoding='utf-8'))
    收=json.loads((工作/'來源收據.json').read_text(encoding='utf-8'))+json.loads((工作/'標準來源收據.json').read_text(encoding='utf-8'))
    for r in 收:assert 雜湊((根/r['原始檔']).read_bytes())==r['來源雜湊']
    產品=讀表('官方替代來源與栅格結構.csv');差=讀表('投影無資料值與來源差異.csv')
    assert len(產品)==len(差)==結['同年官方替代來源數']==3
    assert all(r['栅格標籤解析通過']=='True' and r['原服務已恢復']=='False' for r in 產品)
    assert sum(int(r['完整檔宣告位元組']) for r in 產品)==1255855479
    assert sum(int(r['限定範圍取得位元組']) for r in 產品)==結['範圍實得總位元組']==3942
    assert len(收)==結['原始來源回應數']+2==29
    from 栅格標籤解析 import 解析
    for row in 產品:
        年=row['觀測年份'];片=[r for r in 收 if r['中文來源']==年+'年栅格元資料範圍']
        assert all(r['狀態碼']==206 and (根/r['原始檔']).stat().st_size==r['實得位元組'] for r in 片)
        def 讀(o,n):
            for r in 片:
                lo=r['請求起點'];hi=lo+r['實得位元組']
                if lo<=o and o+n<=hi:return (根/r['原始檔']).read_bytes()[o-lo:o-lo+n]
            raise AssertionError('保存片段不足以重現元資料')
        assert 解析(讀)==json.loads(row['第一影像目錄標籤JSON'])
    assert not 結['完整產品已取得'] and not 結['逐像元品質已核'] and not 結['全球覆蓋已核']
    if 暫存:
        名=[p for p in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=根).decode().split('\0') if p]
        assert 名 and all(any(p==s or p.startswith(s+'/') for s in 範圍) for p in 名),'暫存範圍不符'
        for p in 名:
            assert subprocess.check_output(['git','hash-object','--path='+p,p],cwd=根).strip()==subprocess.check_output(['git','rev-parse',':'+p],cwd=根).strip(),'暫存內容不一致'
        for r in 收:
            assert subprocess.check_output(['git','show',':'+r['原始檔']],cwd=根)==(根/r['原始檔']).read_bytes(),'原始回應暫存位元組不一致'
        (工作/'交付驗收.json').write_text(json.dumps({'暫存文件':len(名),'原文保留':True,'來源雜湊核對':True,'範圍核對':True,'新提交訊息':'中文','歷史提交不改寫':True},ensure_ascii=False,indent=2),encoding='utf-8')
    print('文件保留、資料表計數、原始證據雜湊及適用暫存核查通過。')
def main():
    parser=argparse.ArgumentParser(description='中文交付驗證與提交');parser.add_argument('--提交推送',action='store_true');parser.add_argument('--續作暫存',action='store_true');args=parser.parse_args()
    已存=[p for p in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=根).decode().split('\0') if p]
    assert not 已存 or (args.續作暫存 and all(any(p==s or p.startswith(s+'/') for s in 範圍) for p in 已存)),'暫存區已有其他內容或未明示續作，停止'
    密碼掃描();核查()
    if args.提交推送:
        逐步執行([['git','add','--']+範圍]);核查(True)
        逐步執行([['git','add','--',str(工作/'交付驗收.json')]]);核查(True)
        逐步執行([['git','add','--',str(工作/'交付驗收.json')],['git','commit','-m','第六十五批：補核三項未啟動服務官方替代檔及投影差異'],['git','push']])
if __name__=='__main__':main()
