from pathlib import Path
import subprocess,json,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2]
b={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'status':subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),'protected':{}}
for p in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']:b['protected'][p]=hashlib.sha256((R/p).read_bytes()).hexdigest()
(O/'baseline.json').write_text(json.dumps(b,indent=2)+'\n',encoding='utf-8')
s=(O.parent/'global_directory_content_b16/collect.py').read_text(encoding='utf-8').replace('41_global_directory_content_b16','43_global_directory_content_b18').replace('B16 pending','B18 pending')
needle="coverage=collections.Counter(urlparse(r['url']).hostname for r in previous)"
s=s.replace(needle,"previous+=read(R/'Reference/tables/41_global_directory_content_b16_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/41_global_directory_content_b16_20261008/pagination_fetch_manifest.csv')+read(R/'Reference/tables/42_global_directory_followup_b17_20261008/pagination_fetch_manifest.csv')\n"+needle)
(O/'collect.py').write_text(s,encoding='utf-8')
s=(O.parent/'global_directory_content_b16/ledger.py').read_text(encoding='utf-8').replace("T=R/'Reference/tables/41_global_directory_content_b16_20261008'","T=R/'Reference/tables/43_global_directory_content_b18_20261008'").replace("'41_global_directory_content_b16_20261008']","'41_global_directory_content_b16_20261008','42_global_directory_followup_b17_20261008','43_global_directory_content_b18_20261008']")
(O/'ledger.py').write_text(s,encoding='utf-8')
for name in ['deliver.py','validate.py','publish_check.py']:
    s=(O.parent/'global_directory_content_b16'/name).read_text(encoding='utf-8').replace('41_global_directory_content_b16','43_global_directory_content_b18').replace('global_directory_content_b16','global_directory_content_b18').replace('B16','B18')
    if name=='deliver.py':s=s.replace('B14、B15 已嘗試','B14、B15、B16、B17 已嘗試')
    if name=='deliver.py':s=s.replace('## 可回溯數據及價值','## 可回溯數據及價值\n\n本批次遵循 [來源覆核合同](../V2.0.1/governance/source_review_contract.md)，未匯入 Windows Downloads 的原始文件或明細；來源為清單中的公開網站回應。')
    (O/name).write_text(s,encoding='utf-8')
