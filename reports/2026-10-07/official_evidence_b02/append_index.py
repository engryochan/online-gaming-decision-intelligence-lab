from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='OFFICIAL_EVIDENCE_B02_20261007'
addition='\n\n<!-- '+marker+' -->\n\n## 官方證據增補 B02（2026-10-07）\n\n[經緯航太、創未來與 SPA 公開資料核查](Official_Evidence_B02_20261007.qmd)新增三條官方來源、三條限定主張與十四條名稱／服務描述。SPA 原複合名稱身份仍待查；VERIFIED 僅限公開描述，法人、性能、部署、監管與排名 UNKNOWN。原登記及 B01 資料保留。\n'
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
