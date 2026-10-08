from pathlib import Path
import sys,json
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/37_global_directory_content_b12_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'));import intake
intake.O=O;intake.T=T
s=(O.parent/'global_directory_content_b05/security.py').read_text(encoding='utf-8').replace('B05_20261008','B12_20261008')
exec(compile(s,str(O/'publish_check.py'),'exec'))
excluded=sorted({r['path'].split('::')[0] for r in findings})
assert all('/raw/' in p for p in excluded),'Derivative credential candidate requires review before publication'
p=R/'.gitignore';old=p.read_text(encoding='utf-8');marker='# B12 credential candidates: local only'
if excluded and marker not in old:p.write_text(old+'\n'+marker+'\n'+'\n'.join('/'+x for x in excluded)+'\n',encoding='utf-8')
p=R/'.gitattributes';old=p.read_text(encoding='utf-8');rule='reports/2026-10-08/global_directory_content_b12/**/*.response -text'
if rule not in old:p.write_text(old+'\n'+rule+'\n',encoding='utf-8')
q=R/'Reference/Global_Directory_Content_Expansion_B12_20261008.qmd';text=q.read_text(encoding='utf-8')
if '## 發佈與解析核查' not in text:q.write_text(text+f'\n## 發佈與解析核查\n\n採集程序曾輸出 HTML 編碼轉換警告，未逐頁定位；所有頁面文字解析完整性列為待覆核，原始回應位元組保留，不據此宣稱文字無遺漏。憑證模式掃描發現 {len(excluded)} 個原始頁面候選檔，僅留本機並排除推送；未輸出候選值。\n',encoding='utf-8')
s=(O.parent/'global_directory_content_b05/verify_staged.py').read_text(encoding='utf-8').replace('B05_20261008','B12_20261008').replace('30_global_directory_content_b05','37_global_directory_content_b12').replace('global_directory_content_b05/','global_directory_content_b12/')
(O/'verify_staged.py').write_text('from pathlib import Path\nimport sys\nO=Path(__file__).resolve().parent;R=O.parents[2];T=R/"Reference/tables/37_global_directory_content_b12_20261008"\nsys.path.insert(0,str(O.parent/"global_directory_content_b05"));import intake\nintake.O=O;intake.T=T\n'+s,encoding='utf-8')
