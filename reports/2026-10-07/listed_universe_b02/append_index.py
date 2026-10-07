from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Global_Listed_Company_Universe_20261007.qmd','Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='GLOBAL_LISTED_B02_20261007'
addition='\n\n<!-- GLOBAL_LISTED_B02_20261007 -->\n\n## 全量上市名錄 B02\n\n[東證與港交所完整來源增補](Global_Listed_Company_Universe_B02_20261007.qmd)新增21,653筆記錄，連同首批累計34,938筆來源記錄；不是公司總數。全部上市公司的逐國收錄仍在進行，原始欄位、官方分類與覆蓋缺口均保留。\n'
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
