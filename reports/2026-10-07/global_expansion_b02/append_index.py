from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='GLOBAL_EXPANSION_B02_20261007'
addition='\n\n<!-- GLOBAL_EXPANSION_B02_20261007 -->\n\n## 全球金融與歷史關係增補 B02\n\n[本輪全量名冊與時序檢查](Global_Universe_Expansion_B02_20261007.qmd)接收Euronext 3,834條股票工具與292條會員記錄，逐頁對賬；保留全部歷史feature，展開9,345個來源政治關係、427段未觀測時段及169條歷史貨幣日期。v5保留舊金融與歷史資料，現行747項工作及史前缺口仍OPEN。\n'
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
