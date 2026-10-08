from pathlib import Path
import sys,json,hashlib,csv,subprocess
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/35_global_directory_content_b10_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'))
import intake
intake.O=O;intake.T=T
source=(O.parent/'global_directory_content_b05/security.py').read_text(encoding='utf-8').replace('B05_20261008','B10_20261008')
exec(compile(source,str(O/'publish_check.py'),'exec'))
excluded=sorted({r['path'].split('::')[0] for r in findings})
ignore=R/'.gitignore';old=ignore.read_text(encoding='utf-8');marker='# B10 credential candidates: local only'
if excluded and marker not in old:ignore.write_text(old+'\n'+marker+'\n'+'\n'.join('/'+p for p in excluded)+'\n',encoding='utf-8')
attrs=R/'.gitattributes';old=attrs.read_text(encoding='utf-8');rule='reports/2026-10-08/global_directory_content_b10/**/*.response -text'
if rule not in old:attrs.write_text(old+'\n'+rule+'\n',encoding='utf-8')
verified=[]
for name in ['directory_fetch_manifest.csv','pagination_fetch_manifest.csv','direct_file_fetch_manifest.csv']:
    for row in csv.DictReader((T/name).open(encoding='utf-8-sig')):
        if row.get('file'):
            digest=hashlib.sha256((R/row['file']).read_bytes()).hexdigest();assert digest==row['sha256'];verified.append(row['file'])
(O/'raw_verification.json').write_text(json.dumps(dict(receipts_verified=len(verified),excluded_raw_files=excluded,values_disclosed=False),indent=2)+'\n',encoding='utf-8')
qmd=R/'Reference/Global_Directory_Content_Expansion_B10_20261008.qmd';text=qmd.read_text(encoding='utf-8')
if '## 發佈掃描' not in text:qmd.write_text(text+f'\n## 發佈掃描\n\n本輪原始檔及壓縮成員按項目憑證模式掃描，{len(excluded)} 個候選檔案僅保留本機，不推送。未輸出候選值；掃描不能證明所有可能機密形式均已排除。{len(verified)} 個回應／下載收據的原始位元組雜湊核對通過。\n',encoding='utf-8')
print(json.dumps(dict(verified=len(verified),local_only=len(excluded))))
