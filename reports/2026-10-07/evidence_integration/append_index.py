from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='OFFICIAL_EVIDENCE_INTEGRATION_20261007'
addition='\n\n<!-- OFFICIAL_EVIDENCE_INTEGRATION_20261007 -->\n\n## 官方證據整合查詢（2026-10-07）\n\n[分批證據查詢與未決事項](Official_Evidence_Integration_20261007.qmd)提供獨立 SQLite 快照，保留 22 份輸入表的 1,577 筆記錄與所有解碼欄位，連結 371 個機構及 382 條主張。11 條補充主張與原 UNKNOWN 並存；各驗證範圍分開統計，未新增國家能力或排名認證。\n'
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
