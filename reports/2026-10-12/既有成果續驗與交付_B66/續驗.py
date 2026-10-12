from pathlib import Path
import hashlib, json, subprocess, sys, csv

工作 = Path(__file__).resolve().parent
根 = 工作.parents[2]
舊 = 根 / 'reports/2026-10-11/未啟動服務替代來源核查_B65'
雜湊 = lambda b: hashlib.sha256(b).hexdigest()
sys.path.insert(0, str(舊))
from 栅格標籤解析 import 解析

def 核查():
    基 = json.loads((工作/'基線.json').read_text(encoding='utf-8'))
    for p, h in 基['既有文件'].items():
        assert 雜湊((根/p).read_bytes()) == h, '既有文件改動：'+p
    收 = json.loads((舊/'來源收據.json').read_text(encoding='utf-8')) + json.loads((舊/'標準來源收據.json').read_text(encoding='utf-8'))
    assert len(收) == 29
    for r in 收:
        assert 雜湊((根/r['原始檔']).read_bytes()) == r['來源雜湊']
    表 = 根/'Reference/tables/88_未啟動服務替代來源核查_B65_20261011/官方替代來源與栅格結構.csv'
    with 表.open(encoding='utf-8-sig', newline='') as f:
        產品 = list(csv.DictReader(f))
    assert len(產品) == 3
    for row in 產品:
        片 = [r for r in 收 if r['中文來源'] == row['觀測年份']+'年栅格元資料範圍']
        def 讀(o,n):
            for r in 片:
                lo = r['請求起點']
                if lo <= o and o+n <= lo+r['實得位元組']:
                    return (根/r['原始檔']).read_bytes()[o-lo:o-lo+n]
            raise AssertionError('缺少重現片段')
        assert 解析(讀) == json.loads(row['第一影像目錄標籤JSON'])
    html = 根/'Reference/未啟動服務替代來源核查_B65_20261011.html'
    assert html.is_file() and html.stat().st_size > 1000
    結 = {'驗收日期':'2026-10-12','基線提交':基['提交'],'既有文件保留數':len(基['既有文件']), '原始回應雜湊通過數':29,'標籤重現通過數':3,'第六十五批成品雜湊':雜湊(html.read_bytes()),'完整栅格品質已核':False,'全球覆蓋已核':False}
    (工作/'交付驗收.json').write_text(json.dumps(結,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(結,ensure_ascii=False))

if __name__ == '__main__':
    核查()
