from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='FINANCIAL_UNIVERSE_B04_20261007'
addition='\n\n<!-- FINANCIAL_UNIVERSE_B04_20261007 -->\n\n## 全球金融全量來源增補與統一查詢 B04\n\n[ASX與金融母表統一查詢](Global_Financial_Universe_B04_20261007.qmd)新增ASX官方全量目錄1,923條，上市來源記錄累計36,861條；統一18張輸入表共63,863條原表記錄，完整保留前三批欄位與快照，逐列還原驗證通過。印度四項官方下載被拒絕，缺口明列；全球唯一公司數及每國全部收錄仍未宣稱完成。\n'
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
