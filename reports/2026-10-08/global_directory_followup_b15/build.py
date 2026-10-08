from pathlib import Path
O=Path(__file__).resolve().parent
s=(O.parent/'global_directory_followup_b13/deliver.py').read_text(encoding='utf-8').replace('38_global_directory_followup_b13','40_global_directory_followup_b15').replace('global_directory_followup_b13','global_directory_followup_b15').replace('B13','B15')
start=s.index("s=(O.parent/'global_directory_content_b12/ledger.py')");end=s.index("(O/'ledger.py').write_text",start)
s=s[:start]+"s=(O.parent/'global_directory_content_b14/ledger.py').read_text(encoding='utf-8').replace(\"T=R/'Reference/tables/39_global_directory_content_b14_20261008'\",\"T=R/'Reference/tables/40_global_directory_followup_b15_20261008'\").replace(\"'39_global_directory_content_b14_20261008']\",\"'39_global_directory_content_b14_20261008','40_global_directory_followup_b15_20261008']\")\n"+s[end:]
s=s.replace("if 'inf_mensal_cra' in low:","if 'inf_mensal_cri' in low:").replace('BRAZIL_CRA_MONTHLY','BRAZIL_CRI_MONTHLY')
s=s.replace("elif 'bandwidthreport' in low:role='TECHNICAL_BANDWIDTH_REPORT'","elif 'bandwidthreport' in low:role='TECHNICAL_BANDWIDTH_REPORT'\n    elif 'membership' in low and 'members.xlsx' in low:role='EXCHANGE_MEMBER_LIST_SCOPE_AND_DATE_REVIEW'\n    elif 'monthly-funds-report' in low:role='HISTORICAL_MONTHLY_FUNDS_REPORT_NOT_COMPANY_DIRECTORY'\n    elif 'cboe-listed-volume' in low:role='LISTED_INSTRUMENT_VOLUME_NOT_LEGAL_ENTITY_LIST'\n    elif 'otc.nfmf.no' in low:role='HISTORICAL_COMPANY_FINANCIAL_WORKBOOK'\n    elif 'guyanastockexchange' in low:role='INDIVIDUAL_SECURITY_HISTORICAL_TRADES'\n    elif 'online-brokers' in low:role='HISTORICAL_ONLINE_ACCOUNT_OPENING_BROKER_SUBSET'\n    elif 'samples' in low or 'form.xlsx' in low:role='FORM_OR_TEMPLATE_NOT_REGISTERED_ENTITY_LIST'")
s=s.replace('接續 B12 的 232 條頁面連結及 B10 的 3,785 條新連結','接續 B14 的 144 條頁面連結及 B13 的 3,723 條新連結')
s=s.replace('來源包括保加利亞 CSD 結算失敗年報、巴西 CVM CRA 月報與元數據、Nodal 衍生工具合約及持倉限制。它們分別服務於歷史結算風險、监管申報、工具條款及交易限制分析。','來源觀測包括 Nasdaq 交易所會員工作簿、Cboe 成交量及澳洲基金月報、巴西 CVM CRI 月報、挪威 OTC 歷史財報、圭亞那單項證券成交資料、PSX 歷史券商子集與會員申請範本。分別服務於交易所參與者、產品交易、歷史申報與公司財務分析；名稱與網址僅作用途初步分類，逐檔內容、時點與監管範圍仍待核定。')
(O/'deliver.py').write_text(s,encoding='utf-8')
for n in ['validate.py','publish_check.py']:
    s=(O.parent/'global_directory_followup_b13'/n).read_text(encoding='utf-8').replace('38_global_directory_followup_b13','40_global_directory_followup_b15').replace('global_directory_followup_b13','global_directory_followup_b15').replace('B13','B15')
    (O/n).write_text(s,encoding='utf-8')
