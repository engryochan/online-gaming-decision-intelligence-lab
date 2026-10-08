import intake,json,hashlib,csv,subprocess
O,T,R=intake.O,intake.T,intake.R
scan=json.loads((O/'credential_scan.json').read_text())
excluded=[r['path'] for r in scan['candidates']]
ignore=R/'.gitignore';old=ignore.read_text(encoding='utf-8')
addition='\n# B05 raw credential candidates: preserve locally, exclude from publication\n'+'\n'.join('/'+p for p in excluded)+'\n'
if excluded and '# B05 raw credential candidates:' not in old:ignore.write_text(old+addition,encoding='utf-8')
attrs=R/'.gitattributes';old=attrs.read_text(encoding='utf-8');rule='reports/2026-10-08/global_directory_content_b05/**/*.response -text'
if rule not in old:attrs.write_text(old+'\n'+rule+'\n',encoding='utf-8')
verified=[]
for name in ['directory_fetch_manifest.csv','pagination_fetch_manifest.csv','direct_file_fetch_manifest.csv']:
    for row in csv.DictReader((T/name).open(encoding='utf-8-sig')):
        if row.get('file'):
            path=R/row['file'];digest=hashlib.sha256(path.read_bytes()).hexdigest();assert digest==row['sha256'],row['file']
            verified.append(dict(path=row['file'],sha256=digest,publication='LOCAL_ONLY_CREDENTIAL_CANDIDATE' if row['file'] in excluded else 'ELIGIBLE_AFTER_SCAN'))
(O/'raw_byte_verification.json').write_text(json.dumps(dict(verified=len(verified),files=verified),indent=2)+'\n',encoding='utf-8')
qmd=R/'Reference/Global_Directory_Content_Expansion_B05_20261008.qmd'
text=qmd.read_text(encoding='utf-8')
note='\n## 發佈保留\n\n壓縮成員及可解碼字串一併進行憑證候選掃描，未輸出任何候選值。11 個原始 HTML 回應含需審核的憑證字串，按使用者指示僅保留於本機，不推送；來源清單與雜湊仍保存。這些字串尚未判定為有效密碼。其餘本輪新增交付未發現上述掃描模式的候選值；掃描不是所有可能機密形式的完整證明。\n'
if '## 發佈保留' not in text:qmd.write_text(text+note,encoding='utf-8')
print(json.dumps(dict(raw_receipts_verified=len(verified),local_only_candidates=len(excluded))))
