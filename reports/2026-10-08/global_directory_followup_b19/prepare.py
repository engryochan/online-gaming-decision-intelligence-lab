from pathlib import Path
import subprocess,json,hashlib,shutil
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/44_global_directory_followup_b19_20261008';T.mkdir(parents=True,exist_ok=True)
b={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'status':subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),'protected':{}}
for p in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']:b['protected'][p]=hashlib.sha256((R/p).read_bytes()).hexdigest()
(O/'baseline.json').write_text(json.dumps(b,indent=2)+'\n',encoding='utf-8')
for n in ['registry_download_links.csv','registry_pagination_links.csv']:shutil.copyfile(R/'Reference/tables/43_global_directory_content_b18_20261008'/n,T/n)
s=(O.parent/'global_directory_followup_b17/paginate.py').read_text(encoding='utf-8').replace("T=R/'Reference/tables/42_global_directory_followup_b17_20261008'","T=R/'Reference/tables/44_global_directory_followup_b19_20261008'").replace('40_global_directory_followup_b15_20261008/registry_pagination_link_observations.csv','42_global_directory_followup_b17_20261008/registry_pagination_link_observations.csv').replace("'41_global_directory_content_b16_20261008']","'41_global_directory_content_b16_20261008','42_global_directory_followup_b17_20261008','43_global_directory_content_b18_20261008']").replace('B17 explicit','B19 explicit')
(O/'paginate.py').write_text(s,encoding='utf-8')
s=(O.parent/'global_directory_followup_b17/files.py').read_text(encoding='utf-8').replace('42_global_directory_followup_b17','44_global_directory_followup_b19').replace("'40_global_directory_followup_b15_20261008']","'40_global_directory_followup_b15_20261008','42_global_directory_followup_b17_20261008']")
s=s.replace('selected=set(byurl)',"selected={u for u in byurl if urlparse(u).hostname!='historical-lou-files.gleif.org'}")
(O/'files.py').write_text(s,encoding='utf-8')
s=(O.parent/'global_directory_followup_b17/deliver.py').read_text(encoding='utf-8').replace('42_global_directory_followup_b17','44_global_directory_followup_b19').replace('global_directory_followup_b17','global_directory_followup_b19').replace('B17','B19')
start=s.index("s=(O.parent/'global_directory_content_b16/ledger.py')");end=s.index("(O/'ledger.py').write_text",start)
s=s[:start]+"s=(O.parent/'global_directory_content_b18/ledger.py').read_text(encoding='utf-8').replace(\"T=R/'Reference/tables/43_global_directory_content_b18_20261008'\",\"T=R/'Reference/tables/44_global_directory_followup_b19_20261008'\").replace(\"'43_global_directory_content_b18_20261008']\",\"'43_global_directory_content_b18_20261008','44_global_directory_followup_b19_20261008']\")\n"+s[end:]
s=s.replace('接續 B16 的 179 條頁面連結及 B15 的 3,024 條新連結','接續 B18 的 46 條頁面連結及 B17 的 3,066 條新連結')
start=s.index('來源觀測包括巴西');end=s.index('## 可回溯交付',start)
s=s[:start]+'''本輪下載可能包含技術文件、歷史行情、申報、申請範本或會員資料，逐檔來源角色另表覆核。來源文件不自動成為公司名錄。ZIP 內嵌文件本輪保留原始壓縮檔並核對成員雜湊；僅直接 CSV/XLSX 行已抽取，內嵌 CSV、舊 XLS、PDF 與完整工作簿物件待後續解析。全球完整性仍為 UNKNOWN。

遵循 [來源覆核合同](../V2.0.1/governance/source_review_contract.md)，未匯入 Windows Downloads 文件或明細；本批來源為網站清單的公開回應。

'''+s[end:]
s=s.replace('全部嘗試；','本輪選取 {b["selected_links"]} 個網址，另 {b["pending_unselected"]} 個歷史封存包待大小、版次及內容去重核查；')
(O/'deliver.py').write_text(s,encoding='utf-8')
for n in ['validate.py','publish_check.py']:
    s=(O.parent/'global_directory_followup_b17'/n).read_text(encoding='utf-8').replace('42_global_directory_followup_b17','44_global_directory_followup_b19').replace('global_directory_followup_b17','global_directory_followup_b19').replace('B17','B19');(O/n).write_text(s,encoding='utf-8')
