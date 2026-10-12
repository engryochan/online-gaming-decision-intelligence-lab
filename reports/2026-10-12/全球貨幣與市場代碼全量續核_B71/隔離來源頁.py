from pathlib import Path
import json,hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2]
來源=工作/'原始來源/市場代碼官方發布頁.html'
目標=根/'reports/安全隔離/B71/市場代碼官方發布頁.html'
assert 來源.resolve().is_relative_to(根.resolve()) and 目標.resolve().is_relative_to(根.resolve())
assert 來源.is_file() and not 目標.exists()
目標.parent.mkdir(parents=True,exist_ok=True);來源.rename(目標)
收=json.loads((工作/'來源收據.json').read_text(encoding='utf-8'))
for r in 收:
    if r['中文來源']=='市場代碼官方發布頁.html':
        assert hashlib.sha256(目標.read_bytes()).hexdigest()==r['來源雜湊']
        r['原始檔']=目標.relative_to(根).as_posix();r['禁止推送']=True;r['隔離原因']='含憑證字串候選，尚未確認是否有效；不披露值'
(工作/'來源收據.json').write_text(json.dumps(收,ensure_ascii=False,indent=2),encoding='utf-8')
忽略=根/'.gitignore';原=忽略.read_bytes();新增=b'\n/reports/\xe5\xae\x89\xe5\x85\xa8\xe9\x9a\x94\xe9\x9b\xa2/B71/\n';忽略.write_bytes(原+新增)
(工作/'隔離收據.json').write_text(json.dumps({'原始頁雜湊保留':True,'原始页推送':False,'原因':'掃描發現憑證字串候選，保留待核','原始候選值披露':False,'原忽略文件位元組':len(原),'原忽略文件雜湊':hashlib.sha256(原).hexdigest()},ensure_ascii=False,indent=2),encoding='utf-8')
報=根/'Reference/全球貨幣與市場代碼全量續核_B71_20261012.qmd'
報.write_bytes(報.read_bytes()+'\n\n## 發布保留事項\n\n官方市場代碼發布頁原始HTML含憑證字串候選，已隔離為本機保留且禁止推送；未判定其是否有效，不披露候選值。六份回應均留存雜湊，五份原始來源可交付，一份頁面隔離；完整市場CSV與兩份貨幣XML不受此隔離影響。\n'.encode('utf-8'))
print('一份來源頁已隔離；候選值未披露。')
