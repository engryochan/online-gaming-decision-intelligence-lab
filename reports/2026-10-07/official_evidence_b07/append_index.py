from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='OFFICIAL_EVIDENCE_B07_20261007'
addition='\n\n<!-- OFFICIAL_EVIDENCE_B07_20261007 -->\n\n## 官方證據增補 B07（2026-10-07）\n\n[語音 BCI 機構研究與更正關係](Official_Evidence_B07_20261007.qmd)增補 UC Davis 研究單位、五筆分條件公告指標及 BrainGate 試驗關係；Crossmark 更正關係已確認，但更正正文未讀取，對原指標影響 UNKNOWN。未將機構公告當作原始論文驗證，舊數值及查詢快照保留。\n'
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
