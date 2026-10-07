from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Global_Listed_Company_Universe_B02_20261007.qmd','Global_Listed_Company_Universe_20261007.qmd','Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='CURRENCY_BROKER_B03_20261007'
addition='\n\n<!-- CURRENCY_BROKER_B03_20261007 -->\n\n## 貨幣與證券行完整來源增補 B03\n\n[ISO4217與監管名錄](Global_Currency_and_Securities_Firms_B03_20261007.qmd)完整接收280條現行與169條歷史貨幣／基金記錄、FSA 1,951家業者（第一種旗標293家，含限制）及JPX 158條參與者。249條目貨幣來源關係已建立；每國全部實際貨幣、證券行與上市公司仍需逐項核對，未宣稱全球完成。\n'
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
