from pathlib import Path
import csv, json, hashlib, subprocess, collections, re, zipfile, io
from urllib.parse import urlparse, urldefrag

csv.field_size_limit(2147483647)
O=Path(__file__).resolve().parent
R=O.parents[2]
T=R/'Reference/tables/49_global_registry_review_b24_20261008'
T.mkdir(parents=True,exist_ok=True)
assert not (O/'review_receipt.json').exists(), 'Preserve completed review'
def read(p):
    return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n, rows):
    if not rows:return
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
protected=[R/'Reference/Aerospace_Ecosystem_Report.qmd',R/'Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd',R/'Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']+list(R.glob('Reference/geo_defense_space_handoff_v2_3_0*'))
baseline={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),protected=baseline),indent=2)+'\n',encoding='utf-8')
batches=[('B19','44_global_directory_followup_b19_20261008'),('B21','46_global_directory_followup_b21_20261008'),('B23','48_global_directory_followup_b23_20261008')]
metrics=[];seen=set();hostcounts=collections.Counter()
for label,folder in batches:
    rows=read(R/'Reference/tables'/folder/'pagination_fetch_manifest.csv')
    urls={urldefrag(r['url'])[0] for r in rows};hosts=collections.Counter(urlparse(u).hostname for u in urls)
    top,n=hosts.most_common(1)[0]
    metrics.append(dict(batch=label,receipts=len(rows),unique_urls=len(urls),hosts=len(hosts),largest_host=top,largest_host_urls=n,largest_host_share=round(n/len(urls),4),exact_prior_url_overlap=len(urls&seen)))
    seen.update(urls);hostcounts.update(hosts)
write('registry_pagination_concentration.csv',metrics)
base=R/'Reference/tables/48_global_directory_followup_b23_20261008'
gaps=read(base/'registry_pagination_gaps.csv')
groups=collections.defaultdict(list)
for r in gaps:groups[urlparse(r['target_url']).hostname].append(r)
# A reviewable, host-balanced preview; no live requests and no old generator changes.
selected=[]
for depth in range(max(map(len,groups.values()),default=0)):
    for host in sorted(groups,key=lambda h:(hostcounts[h],h)):
        if depth<min(len(groups[host]),5):selected.append(dict(groups[host][depth],preview_rank=len(selected)+1,host_prior_pagination_receipts=hostcounts[host],decision='PREVIEW_BODY_AND_DIRECTORY_SCOPE_REVIEW'))
    if len(selected)>=100:break
selected=selected[:100]
write('registry_next_pagination_balanced_preview.csv',selected)
write('registry_remaining_pagination_preview.csv',[dict(r,decision='PRESERVED_PENDING') for r in gaps if r['target_url'] not in {x['target_url'] for x in selected}])
# Evaluate candidate lineage without logging any matched value or original cell.
source=(R/'reports/2026-10-07/git_publish_and_html_recovery/audit.py').read_text(encoding='utf-8');ns={'re':re}
exec(source[source.index('patterns='):source.index('for name in paths:')],ns)
scan=json.loads((R/'reports/2026-10-08/global_directory_followup_b23/credential_scan.json').read_text())
lineage=[]
manifest=read(base/'direct_file_fetch_manifest.csv')
for hit in scan['candidates']:
    if '::' not in hit['path']:continue
    file,member=hit['path'].split('::',1)
    with zipfile.ZipFile(R/file) as z:data=z.read(member)
    values=[]
    for kind,pat in ns['patterns']:
        for m in pat.finditer(data):
            value=m[1] if kind=='CREDENTIAL_LITERAL' else m[0]
            low=value.decode('utf-8','ignore').lower().strip()
            if kind=='CREDENTIAL_LITERAL' and (low in ns['placeholders'] or low.startswith(('your_','your-','${','{{','<','process.env','os.environ')) or len(low)>256):continue
            values.append(value.decode('utf-8','ignore'))
    urls={r['url'] for r in manifest if r.get('file')==file}
    matching=0;source_rows=0
    with (base/'registry_download_workbook_rows.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r['url'] not in urls:continue
            source_rows+=1
            cells=json.loads(r['cells_json'])
            if any(v in str(c) for c in cells if c is not None for v in values):matching+=1
    lineage.append(dict(source_file=file,archive_member=member,candidate_match_count=len(values),source_workbook_rows=source_rows,rows_containing_exact_candidate_value=matching,release_decision='HOLD_NO_AUTOMATIC_RECLASSIFICATION',limitation='Exact-value lineage only; not proof of secret validity or exhaustive detection'))
write('registry_credential_lineage_review.csv',lineage)
actions=[dict(priority='P0',action='Review held workbook candidate validity and derived lineage before release',state='LINEAGE_CHECKED_RELEASE_HELD'),dict(priority='P1',action='Validate source directory role and host-balanced pagination preview before fetching',state='PREVIEW_READY_NOT_FETCHED'),dict(priority='P1',action='Acquire next original queue sources with jurisdiction coverage and authoritative scope review',state='2828_ORIGINAL_WORK_ROWS_PENDING'),dict(priority='P2',action='Review 25 historical archive releases, sizes and overlapping content',state='PRESERVED_PENDING'),dict(priority='P2',action='Resolve issuer, security, broker and membership identities with versioned evidence',state='UNIQUE_ENTITY_DENOMINATOR_UNKNOWN')]
write('registry_actionplan.csv',actions)
texts={
'redteam':'來源冒牌、頁面截斷、壓縮內嵌憑證、CSV 公式與機械身份合併均可造成錯誤交付。原始 SHA256 只證明版本，不證明來源權威或內容真實；工作簿候選仍 HOLD，未因衍生表未匹配掃描模式而自動放行。',
'critic':'先看 registry_pagination_concentration.csv。分頁網址不重複仍可能同站高度集中、內容不屬公司名錄。HTTP 200、下載數、表格行與角色投影不得當作唯一法人數或全球覆蓋率。',
'killcritic':'可證偽門檻：精確 URL 重複需為零；候選網址須有來源血統與內容用途；正文與證據主張對應；讀取行數與入庫行數一致；憑證候選及衍生鏈未裁定前不發布。零精確值匹配只限於該檢查，不能證明所有內容沒有憑證。',
'blindspot':'目前原清單尚有 2,828 項未嘗試；動態 API、非拉丁文字、證券與法人區分、券商牌照與交易所會員差異、貨幣有效年代、歷史疆界爭議及神經技術人體證據仍需獨立工作。ISO 母表不是完整性分母，也不是歷史國家全集。',
'blueprint':'原件本機／隔離存儲 → 來源與版本血統 → 逐用途解析 → 時態身份與關係 → 逐國覆蓋與缺口 → 安全可發布投影。先以本機可對賬資料模型完成身份與來源用途，規模證據成立後才導入分散式系統。主鍵分職：法人、證券、上市、牌照、會員、貨幣與政治實體。',
'cheatsheet':'UNKNOWN≠0；來源存在≠已採集；HTTP200≠完整內容；SHA256一致≠來源權威；表格行≠法人；LEI≠所有企業；會員≠持牌券商；ISO地區≠主權國家；本機驗收≠已公開交付；預覽排程≠已實測採集。',
'actionplan':'本輪已執行來源集中度、精確網址重疊、工作簿憑證衍生鏈核查及下一輪平衡排程預覽。按 registry_actionplan.csv 續作；禁止以增加下載數取代身份核實，也不以重新下載大型資料作為優化指標。'}
for name,body in texts.items():
    p=R/name/'global_registry_b24_20261008.md';p.parent.mkdir(exist_ok=True);assert not p.exists()
    p.write_text('# '+name+'｜全球清單 B24\n\n'+body+'\n\n本輪證據：[B24 審查報告](../Reference/Global_Registry_Review_B24_20261008.qmd)。這是工程審查，不聲稱全球完整收錄。\n',encoding='utf-8')
receipt=dict(pagination_metrics=metrics,credential_lineage=lineage,pagination_gap_observations=len(gaps),preview_rows=len(selected),preview_only=True,global_complete=False)
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in baseline.items())
(O/'review_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
report='''---
title: "全球登記 B24：七向審查與下一輪施工校正"
date: 2026-10-08
format:
  html:
    toc: true
    embed-resources: true
---

本輪先審查施工品質，再調整排程。完整保留舊批次、主報告及使用者交接文件；沒有取得新的公司名錄，沒有聲稱全球完整。

## 實測分頁集中度

'''+ '\n'.join(f"- {m['batch']}：{m['unique_urls']} 個網址、{m['hosts']} 個主機；最大主機 {m['largest_host']} 占 {m['largest_host_share']:.1%}，與已審查前批精確 URL 重疊 {m['exact_prior_url_overlap']}。" for m in metrics)+'''

這只能衡量三批收據；不能推導公司、國家或全項目覆蓋率。精確網址不重複也不證明頁面內容不重複。平衡預覽每主機最多 5 個網址，先輪替主機，仍須核定名錄用途，不能憑頁碼直接提升優先級。

## 憑證衍生鏈

'''+ '\n'.join(f"- 內嵌候選 {x['candidate_match_count']} 處；該來源工作表行 {x['source_workbook_rows']} 條，包含候選精確值的衍生行 {x['rows_containing_exact_candidate_value']} 條。" for x in lineage)+'''

未輸出候選值或單元格內容。此為精確值血統查核，不是完整語義或安全驗收；B23 工作簿原件、行表與資料庫繼續保留本機，不自動解封。

## 七向施工文件

'''+ '\n'.join(f'- [{n}](../{n}/global_registry_b24_20261008.md)' for n in texts)+'''

## 下一步及可對賬資料

優先確認來源用途與憑證衍生鏈，再依原清單逐法域補齊身份資料；同時以主機平衡排程避免頁碼網站壟斷採集。歷史封存包 25 項及原清單 2,828 項待辦沒有結案。

[集中度](tables/49_global_registry_review_b24_20261008/registry_pagination_concentration.csv)、[衍生鏈元資料](tables/49_global_registry_review_b24_20261008/registry_credential_lineage_review.csv)、[下一輪預覽](tables/49_global_registry_review_b24_20261008/registry_next_pagination_balanced_preview.csv)、[餘下候選](tables/49_global_registry_review_b24_20261008/registry_remaining_pagination_preview.csv)、[行動清單](tables/49_global_registry_review_b24_20261008/registry_actionplan.csv)。預覽未發送網路请求，不是新增收錄。
'''
(R/'Reference/Global_Registry_Review_B24_20261008.qmd').write_text(report,encoding='utf-8')
print(json.dumps(receipt))
