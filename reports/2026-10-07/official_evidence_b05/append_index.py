from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='OFFICIAL_EVIDENCE_B05_20261007'
addition='\n\n<!-- OFFICIAL_EVIDENCE_B05_20261007 -->\n\n## 官方證據增補 B05（2026-10-07）\n\n[神經科技器件、人體研究與許可範圍](Official_Evidence_B05_20261007.qmd)新增五條來源、七條限定主張、三份器件概況及四條廠商試驗連結。Layer 7-T 的 FDA 決定限定於器件及少於 30 天的適用範圍；試驗登記正文未讀取成功，臨床階段與招募現況 UNKNOWN。未新增國家 N0～N7 能力或排名。\n'
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
