from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='OFFICIAL_EVIDENCE_INTEGRATION_V2_20261007'
addition='\n\n<!-- OFFICIAL_EVIDENCE_INTEGRATION_V2_20261007 -->\n\n## 官方證據整合查詢 v2（2026-10-07）\n\n[研究、監管與更正整合視圖](Official_Evidence_Integration_v2_20261007.qmd)納入原全球 B04 及官方證據 B01～B08，保留46份表的1,657筆記錄，連結372個單位與407條主張。器件許可、論文結果及機構自述分開查詢；原371條主張、舊快照與歷史資料保留。未新增國家能力或排名。\n'
saved=OUT/'originals';assert not saved.exists();saved.mkdir()
receipt=[]
for name in names:
    p=ROOT/'Reference'/name;old=p.read_bytes();assert marker.encode() not in old
    (saved/name).write_bytes(old)
    current=hashlib.sha256(old).hexdigest();assert hashlib.sha256(p.read_bytes()).hexdigest()==current
    p.write_bytes(old+addition.encode('utf-8'))
    assert p.read_bytes().startswith(old)
    receipt.append(dict(path=p.relative_to(ROOT).as_posix(),original_sha256=current,updated_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),original_bytes_preserved=True))
(OUT/'append_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
