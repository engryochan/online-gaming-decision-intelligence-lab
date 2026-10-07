from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='FINANCIAL_UNIVERSE_B07_20261007'
addition='\n\n<!-- FINANCIAL_UNIVERSE_B07_20261007 -->\n\n## ISO 249 全球金融增補 B07\n\n[全部249條目覆蓋與ESMA完整登記](Global_Financial_Universe_B07_20261007.qmd)：747項逐國工作列保留實際來源與缺口；新增31個來源母國標籤的7,162條公司／分支記錄及75,368條活動／歷史。統一快照v4保留舊列，全球全部公司與券商仍待逐國完成，未宣稱收齊。\n'
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
