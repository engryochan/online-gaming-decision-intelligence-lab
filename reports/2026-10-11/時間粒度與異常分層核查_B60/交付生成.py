from pathlib import Path
import json, hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2]
assert not (工作/'附加收據.json').exists()
結=json.loads((工作/'核查結果.json').read_text(encoding='utf-8'))
名='時間粒度與異常分層核查_B60_20261011'
正文='''本批是2019年1月1日歷史樣本核查；查證日期為2026年10月11日，不代表2026年現況。

7516408行原始資料形成7515889個精確時間鍵。鍵為MMSI（海上移動通信業務識別碼）與BaseDateTime（基準日期時間）的原字串，不進行取整或型態改寫。519組有多行，其中4組有不同的17欄向量，共涉及8行；其餘完全相同向量的多餘行為515。雜湊僅用於256分區，實際以完整原字串比較。不同向量不是已證實的錯誤或身份衝突，根因仍待來源證據。

整分鐘時間行114633；非整分鐘時間行7401775。官方2019年[處理歷程](https://www.fisheries.noaa.gov/inport/item/62733)描述一分鐘採樣頻率，不能將採樣頻率等同於時間戳必須落在整分鐘；因此非零秒數不能單獨判作品質錯誤，也不應自動抹除。

吃水負值2712行分成六種原值；非九位數字識別碼11490行按原長度及收發器類別分層。保留原值，沒有自動修復、刪行或推斷船舶身份。異常根因、逐用途授權及全球覆蓋尚未核定。本批尚未進行跨日核查；相鄰檔驗收另見接續批次。

## 表格與適用範圍

'''
for p in sorted((根/'Reference/tables/83_時間粒度與異常分層核查_B60_20261011').glob('*.csv')):
    正文+=f'- [{p.stem}](tables/83_時間粒度與異常分層核查_B60_20261011/{p.name})。\n'
正文+='\n原始壓縮檔再次完整讀至末尾並通過校验；原始檔和逐行分區只留本機。統計可重現，但不證明全年品質或全球完整性。停止擴大2019年度下載，下一步核對最新官方目錄的觀測時段與發布日期。\n'
(根/'Reference'/f'{名}.qmd').write_text('---\ntitle: "時間粒度與異常分層核查：第六十批"\ndate: 2026-10-11\nlang: zh-TW\nformat:\n  html:\n    toc: true\n    embed-resources: true\n---\n\n'+正文,encoding='utf-8')
基=json.loads((工作/'基線.json').read_text(encoding='utf-8'));p=根/基['主報告'];原=p.read_bytes()
assert len(原)==基['原文位元組'] and hashlib.sha256(原).hexdigest()==基['原文雜湊']
附=f'\n\n## 2026-10-11 時間粒度與異常分層核查：第六十批\n\n[核查報告]({名}.qmd)：歷史樣本7516408行，4組同一原時間鍵有不同向量；採樣頻率與時間戳精度分別核對。保留異常原值，不推斷身份或全球完成。\n'.encode()
p.write_bytes(原+附);(工作/'附加收據.json').write_text(json.dumps({'附加雜湊':hashlib.sha256(附).hexdigest()},ensure_ascii=False),encoding='utf-8')
for d,t in [('redteam','對抗審核'),('critic','批判核對'),('killcritic','批判再審'),('blindspot','盲點核查'),('blueprint','施工藍圖'),('cheatsheet','速查要點'),('actionplan','行動清單')]:
    (根/d/f'{名}.md').write_text(f'# {t}｜第六十批\n\n精確時間鍵不同向量不等於已證實錯誤；一分鐘採樣不等於時間秒數必須為零。歷史觀測年份與查證日期分列，異常原值保留。根因及全球覆蓋仍待核。\n\n[完整報告](../Reference/{名}.qmd)。\n',encoding='utf-8')
