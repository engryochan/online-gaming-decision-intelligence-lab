from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='FINANCIAL_UNIVERSE_B05_20261007'
addition='\n\n<!-- FINANCIAL_UNIVERSE_B05_20261007 -->\n\n## 全球金融全量來源增補 B05\n\n[TMX與NZX來源與統一快照v2](Global_Financial_Universe_B05_20261007.qmd)新增TSX／TSXV 3,768條、NZX嵌入工具431條、主板明細179條及市場參與者26條。加拿大兩表總數對賬通過；NZX摘要180與明細179的差異明列。先前資料逐列完整保留，工具／目錄來源累計41,060條，並非公司總數。全球全量及唯一法人核對尚未完成。\n'
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
