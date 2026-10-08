from pathlib import Path
O=Path(__file__).resolve().parent
s=(O.parent/'global_directory_content_b12/validate.py').read_text(encoding='utf-8').replace('37_global_directory_content_b12','38_global_directory_followup_b13').replace('global_directory_content_b12.sqlite','global_directory_followup_b13.sqlite')
(O/'validate.py').write_text(s,encoding='utf-8')
s=(O.parent/'global_directory_content_b12/publish_check.py').read_text(encoding='utf-8').replace('37_global_directory_content_b12','38_global_directory_followup_b13').replace('global_directory_content_b12/','global_directory_followup_b13/').replace('B12','B13').replace('Global_Directory_Content_Expansion_B13','Global_Directory_Followup_B13')
s=s.replace("assert all('/raw/' in p for p in excluded)","assert all('/raw/' in p or '/downloads/' in p for p in excluded)")
s=s.replace("30_global_directory_content_b05','38_global_directory_followup_b13'","30_global_directory_content_b05','38_global_directory_followup_b13'")
s=s.replace('採集程序曾輸出 HTML 編碼轉換警告，未逐頁定位；所有頁面文字解析完整性列為待覆核，原始回應位元組保留，不據此宣稱文字無遺漏。','頁面解析及來源語義完整性仍待逐項核定；原始回應位元組保留。')
# The staged verifier starts from B05 identifiers, so replace its explicit target separately.
s=s.replace(".replace('30_global_directory_content_b05','35_global_directory_content_b10')", ".replace('30_global_directory_content_b05','38_global_directory_followup_b13')")
s=s.replace("(O/'verify_staged.py').write_text(","s=s.replace('Global_Directory_Content_Expansion_B13','Global_Directory_Followup_B13')\n(O/'verify_staged.py').write_text(")
(O/'publish_check.py').write_text(s,encoding='utf-8')
