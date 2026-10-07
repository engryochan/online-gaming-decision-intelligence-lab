from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='FINANCIAL_UNIVERSE_B06_20261007'
addition='\n\n<!-- FINANCIAL_UNIVERSE_B06_20261007 -->\n\n## 全球金融市場與身份增補 B06\n\n[ISO市場全表、公司及券商對照](Global_Financial_Universe_B06_20261007.qmd)接收MIC全表2,883條、上市／上櫃／興櫃公司來源2,350條及两份各64條券商表，代碼集合對賬一致；新增11條官方統一編號來源匹配。統一快照v3逐列保留舊資料，來源工具／目錄／公司記錄累計43,410條，並非全球唯一公司數。逐國全量缺口仍明列。\n'
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
