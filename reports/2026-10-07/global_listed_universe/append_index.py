from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='GLOBAL_LISTED_UNIVERSE_20261007'
addition='\n\n<!-- GLOBAL_LISTED_UNIVERSE_20261007 -->\n\n## 全球上市證券全量來源接收與神經互動證據\n\n[全量證券母表首批](Global_Listed_Company_Universe_20261007.qmd)已接收官方兩份完整名錄共13,285筆證券，保留全部原始欄位、249國家／地區覆蓋狀態及SQLite查詢；全球全部公司尚未完成，發行人解析仍有缺口。另登記BrainNet作者版本所支持的EEG／網路／TMS有限決策互動及能力界限。\n'
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
