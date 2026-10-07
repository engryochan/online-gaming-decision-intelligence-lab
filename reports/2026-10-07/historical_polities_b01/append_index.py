from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
names=['Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Global_Technology_ISO249_Registry.qmd','Project_Information_Integration_20261007.qmd']
marker='HISTORICAL_POLITIES_B01_20261007'
addition='\n\n<!-- HISTORICAL_POLITIES_B01_20261007 -->\n\n## 全球歷史政治實體與年代圖增補\n\n[歷史政治實體B01](Global_Historical_Polities_B01_20261007.qmd)接收13,797條來源年代／疆域記錄及COW全量國家、大國時段與年度表，提供年份篩選圖；現行名錄實測、747項金融工作與史前／當代缺口分層保留，未宣稱全球所有歷史國家皆已核實。\n'
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
