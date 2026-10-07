from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='OFFICIAL_EVIDENCE_B08_20261007'
addition='\n\n<!-- OFFICIAL_EVIDENCE_B08_20261007 -->\n\n## 官方證據增補 B08（2026-10-07）\n\n[Deep TMS 器件特定監管範圍](Official_Evidence_B08_20261007.qmd)新增四條 FDA 來源、五條限定主張及兩筆器件決定，分別登記成人 OCD 輔助治療與短期戒菸輔助。TMS 刺激功能未延伸為思想讀取、語義寫入或遠程能力；未宣稱系列監管歷史完整。原登記與查詢快照保留。\n'
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
