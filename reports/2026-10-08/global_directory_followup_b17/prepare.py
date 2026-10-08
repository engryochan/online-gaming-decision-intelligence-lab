from pathlib import Path
import subprocess,json,hashlib,shutil
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/42_global_directory_followup_b17_20261008';T.mkdir(parents=True,exist_ok=True)
b={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'status':subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),'protected':{}}
for p in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']:b['protected'][p]=hashlib.sha256((R/p).read_bytes()).hexdigest()
(O/'baseline.json').write_text(json.dumps(b,indent=2)+'\n',encoding='utf-8')
for n in ['registry_download_links.csv','registry_pagination_links.csv']:shutil.copyfile(R/'Reference/tables/41_global_directory_content_b16_20261008'/n,T/n)
s=(O.parent/'global_directory_followup_b15/paginate.py').read_text(encoding='utf-8').replace("T=R/'Reference/tables/40_global_directory_followup_b15_20261008'","T=R/'Reference/tables/42_global_directory_followup_b17_20261008'").replace('38_global_directory_followup_b13_20261008/registry_pagination_link_observations.csv','40_global_directory_followup_b15_20261008/registry_pagination_link_observations.csv')
s=s.replace("'39_global_directory_content_b14_20261008']","'39_global_directory_content_b14_20261008','40_global_directory_followup_b15_20261008','41_global_directory_content_b16_20261008']").replace('B15 explicit','B17 explicit')
(O/'paginate.py').write_text(s,encoding='utf-8')
s=(O.parent/'global_directory_followup_b15/files.py').read_text(encoding='utf-8').replace('40_global_directory_followup_b15','42_global_directory_followup_b17')
s=s.replace("'38_global_directory_followup_b13_20261008']","'38_global_directory_followup_b13_20261008','40_global_directory_followup_b15_20261008']")
(O/'files.py').write_text(s,encoding='utf-8')
s=(O.parent/'global_directory_followup_b15/deliver.py').read_text(encoding='utf-8').replace('40_global_directory_followup_b15','42_global_directory_followup_b17').replace('global_directory_followup_b15','global_directory_followup_b17').replace('B15','B17')
start=s.index("s=(O.parent/'global_directory_content_b14/ledger.py')");end=s.index("(O/'ledger.py').write_text",start)
s=s[:start]+"s=(O.parent/'global_directory_content_b16/ledger.py').read_text(encoding='utf-8').replace(\"T=R/'Reference/tables/41_global_directory_content_b16_20261008'\",\"T=R/'Reference/tables/42_global_directory_followup_b17_20261008'\").replace(\"'41_global_directory_content_b16_20261008']\",\"'41_global_directory_content_b16_20261008','42_global_directory_followup_b17_20261008']\")\n"+s[end:]
s=s.replace('inf_mensal_cri','inf_mensal_ots').replace('BRAZIL_CRI_MONTHLY','BRAZIL_OTS_MONTHLY')
s=s.replace('接續 B14 的 144 條頁面連結及 B13 的 3,723 條新連結','接續 B16 的 179 條頁面連結及 B15 的 3,024 條新連結')
a=s.index('來源觀測包括 Nasdaq');z=s.index('會員申請範本',a)
s=s[:a]+'來源觀測包括巴西 CVM OTS 月報與元數據、圭亞那單項證券歷史成交資料、監管網站歷史指定人士／實體清單及會員申請／聯絡表。它們服務於歷史申報、工具交易、合規證據及流程分析；逐檔內容、時點及監管範圍仍須核定。'+s[z:]
s=s.replace('ZIP 成員原始內容留在原始壓縮檔，本輪核對成員雜湊，尚未把所有內嵌 CSV/PDF/XML 解析為業務表。舊 XLS 本輪保留原始檔，尚未抽取所有單元格；XLSX 保留可讀行及公式文字，完整工作簿物件仍需後續檢查。全球名錄完整性仍為 UNKNOWN。','本輪另以 archives.py 展開原始 ZIP 的 CSV 與文字字典成員，逐成員雜湊與行數對賬保留於 archive_acceptance.json；來源行不等於獨立公司。其他工作簿物件及字典語義仍待核查，全球完整性仍為 UNKNOWN。')
(O/'deliver.py').write_text(s,encoding='utf-8')
for n in ['validate.py','publish_check.py']:
    s=(O.parent/'global_directory_followup_b15'/n).read_text(encoding='utf-8').replace('40_global_directory_followup_b15','42_global_directory_followup_b17').replace('global_directory_followup_b15','global_directory_followup_b17').replace('B15','B17')
    (O/n).write_text(s,encoding='utf-8')
