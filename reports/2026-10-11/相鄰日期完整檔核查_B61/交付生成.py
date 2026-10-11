from pathlib import Path
import json,hashlib,subprocess
工作=Path(__file__).resolve().parent;根=工作.parents[2];名='相鄰日期完整檔核查_B61_20261011';主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd'
assert not (工作/'基線.json').exists(),'禁止刷新基線'
H=lambda b:hashlib.sha256(b).hexdigest()
原=(根/主).read_bytes();paths=subprocess.check_output(['git','ls-files','-z'],cwd=根).decode().split('\0')
基={'提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=根).decode().strip(),'主報告':主,'原文位元組':len(原),'原文雜湊':H(原),'原有文件':{p:H((根/p).read_bytes()) for p in paths if p.endswith(('.md','.qmd')) and (根/p).is_file()}}
(工作/'基線.json').write_text(json.dumps(基,ensure_ascii=False,indent=2),encoding='utf-8')
文='''本批驗收已取得的2019年1月2日歷史檔，查證日期為2026年10月11日。停止擴大2019年度下載，後续工作转向最新官方資料；歷史核查仍完整保留。

完整下載276171098位元組，讀取7169185行，壓縮成員完整讀至末尾并通過循環冗餘校驗。所有資料行欄數相符、時間可解析且日期均為2019年1月2日；前日7516408行全部屬2019年1月1日，合計14685593行。

兩檔原時間日期集合不相交，故包含完整原時間的精確鍵及17欄完整向量跨日重複為零。這是日期集合的邏輯判定，沒有聲稱逐船運動連續性、近似重複、午夜接收缺口或身份一致性已通過。不把跨日時間不同但其他欄相似視為已排除。

[日期核查](tables/84_相鄰日期完整檔核查_B61_20261011/相鄰完整檔日期核查.csv)、[日期分布](tables/84_相鄰日期完整檔核查_B61_20261011/相鄰完整檔日期分布.csv)。[原始公開來源](https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2019/AIS_2019_01_02.zip)。原始資料僅留本機，不推送逐行記錄。

## 接續

全年及全球品質、異常根因、逐用途授權尚未核實。下一步以2025與2026年官方目錄實際可得範圍為準，分列觀測時段、來源更新日期及查證日期；不得把元資料發布日期誤作觀測年份。
'''
(根/'Reference'/f'{名}.qmd').write_text('---\ntitle: "相鄰日期完整檔核查：第六十一批"\ndate: 2026-10-11\nlang: zh-TW\nformat:\n  html:\n    toc: true\n    embed-resources: true\n---\n\n'+文,encoding='utf-8')
附=f'\n\n## 2026-10-11 相鄰日期完整檔核查：第六十一批\n\n[報告]({名}.qmd)：兩日歷史檔共14685593行，日期集合不相交，含原時間的精確跨日鍵及完整向量重複為零；不外推運動連續性或全年品質。接續核對最新資料，不擴大2019年度下載。\n'.encode()
assert (根/主).read_bytes()==原;(根/主).write_bytes(原+附);(工作/'附加收據.json').write_text(json.dumps({'附加雜湊':H(附)},ensure_ascii=False),encoding='utf-8')
for d in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']:
    (根/d/f'{名}.md').write_text(f'# 相鄰日期核查｜第六十一批\n\n日期不相交只排除包含完整原時間的精確鍵重複，不能排除近似重複或接收缺口。已取得歷史證據保留，優先核最新目錄。\n\n[中文報告](../Reference/{名}.qmd)。\n',encoding='utf-8')
碼=(工作.parent/'時間粒度與異常分層核查_B60/驗證與提交.py').read_text(encoding='utf-8').replace('時間粒度與異常分層核查_B60','相鄰日期完整檔核查_B61').replace('83_','84_').replace('第六十批：核實完整單日時間鍵、原值異常分層及秒分布','第六十一批：驗收相鄰歷史完整檔及精確跨日日期判定')
a=碼.index("    收=json.loads");b=碼.index('    if 暫存:',a)
碼=碼[:a]+'''    收=json.loads((工作/'取得收據.json').read_text(encoding='utf-8'))
    p=Path(收['本機原始檔']);assert p.is_file()
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    assert h.hexdigest()==收['來源雜湊']==結['來源雜湊']
    assert p.stat().st_size==收['實得位元組']==276171098
    日期=讀表('相鄰完整檔日期核查.csv')
    assert len(日期)==3 and all(int(r['不符資料行'])==0 and int(r['分母'])==7169185 for r in 日期)
    assert 結['兩日合計資料行']==結['相鄰完整資料行']+結['前日完整資料行']==14685593
    assert 結['精確原時間鍵跨日重複行']==0 and 結['相鄰壓縮校驗通過'] and not 結['全球完成'] and not 結['全年完成']
'''+碼[b:]
(工作/'驗證與提交.py').write_text(碼,encoding='utf-8')
(工作/'發布阻斷測試.py').write_text((工作.parent/'時間粒度與異常分層核查_B60/發布阻斷測試.py').read_text(encoding='utf-8'),encoding='utf-8')
