from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='OFFICIAL_EVIDENCE_B06_20261007'
addition='\n\n<!-- OFFICIAL_EVIDENCE_B06_20261007 -->\n\n## 官方證據增補 B06（2026-10-07）\n\n[Synchron SWITCH 論文與更正核查](Official_Evidence_B06_20261007.qmd)新增兩條期刊來源、六條限定主張、一筆論文及七筆研究指標，保留樣本、測試條件與更正關係。訊號 Hz 不轉換為資訊 bits/s，BCI 配合眼動成績不當作 BCI 單獨性能；未新增國家能力或監管判定。\n'
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
