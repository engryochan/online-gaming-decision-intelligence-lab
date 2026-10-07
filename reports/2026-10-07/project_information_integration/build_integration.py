"""Lossless local document consolidation. Preview by default; guarded --apply."""
from pathlib import Path
import csv, hashlib, io, json, re, sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
prior_plan=json.loads((OUT/'delivery_plan.json').read_text(encoding='utf-8')) if '--apply' in sys.argv else None
BASE = ROOT / 'reports/2026-10-06/workspace_change_audit/integration_20261007_start_files.csv'
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return (ROOT/p).read_bytes()
def csvout(name, rows, fields):
    with (OUT/name).open('w', encoding='utf-8-sig', newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
baseline=list(csv.DictReader(BASE.open(encoding='utf-8-sig')))
paths=[r['path'] for r in baseline]
ref='Reference/'
geo=ref+'Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report'
aero=ref+'Aerospace_Ecosystem_Report'
families={
 'geostrategy': (geo+'.qmd', [geo+'_meta.md',geo+'_web_version.qmd',ref+'地緣軍事宇航策略平臺_全量問答與本對話回覆_20261006.md',ref+'ChatGPT_上一輪回覆_地緣軍事宇航技術生態_20261006.md',ref+'地緣宇航開源生態_商業化增量章節_20261006.md',ref+'附件核查与报告补齐草案.md']),
 'aerospace': (aero+'.qmd',[aero+'_web_version.qmd']),
 'daqin': ('_大秦赋算筹_v1_3_9.qmd',[p for p in paths if (p.startswith('_大秦赋算筹') or p.startswith('归档/')) and p.endswith('.qmd') and p!='_大秦赋算筹_v1_3_9.qmd']+[p for p in paths if p.endswith('DaqinFu-SuanChou-V1-2-2-Enhanced.md')]),
 'real_world': (ref+'真实版人物分析与治国策略服务_名录与九十日行令_v2_4_全球行政通信宇航生命证据增强版_20261004.md',[p for p in paths if p.startswith(ref+'真实版人物分析与治国策略服务') and p.endswith('.md') and '全球行政通信宇航生命' not in p]+[ref+'Taige-Real-World-Report.md',ref+'Taige-Real-World-Report-V2-Enhanced.md',ref+'compass_artifact_wf-6a2ba288-4cf0-5fbe-bfb6-8ca465509bca_text_markdown.md']),
 'whitepaper': (ref+'Whitepaper-Perfect-Baccarat-AI-Quant-Governance-V3-1-0.md',[ref+'Whitepaper-Perfect-Baccarat-AI-Quant-Governance-V3-0-0.md',ref+'Whitepaper-Online-Gaming-Baccarat-AI-V2-0-0.md',ref+'全球在线博彩娱乐_AI量化科技与安全治理白皮书_2026-09-27.md',ref+'perfect-baccarat-report.md',ref+'Baccarat-Ai-Automation-Report.md',ref+'顶级在线百家乐平台_AI与跨行业量化科技_移植总表_v1_0_0.md']),
 'three_value_draft': (ref+'在线博彩娱乐白皮书_完美真人百家乐_三价值统一架构_v0_3_0_DRAFT.md',[ref+'在线博彩娱乐白皮书_完美真人百家乐_三价值统一架构_v0_2_0_DRAFT.md',ref+'在线博彩娱乐白皮书_百家乐体育彩券_三价值统一架构_v0_1_0_DRAFT.md'])
}
shared_geo=[ref+'地緣軍事宇航策略平臺_全量問答與本對話回覆_20261006.md',ref+'ChatGPT_上一輪回覆_地緣軍事宇航技術生態_20261006.md',ref+'地緣宇航開源生態_商業化增量章節_20261006.md',ref+'地緣學、軍事、宇航、策略服務平臺提問.txt']
families['geostrategy'][1].extend(shared_geo)
families['aerospace'][1].extend(shared_geo)
families['real_world'][1].extend([ref+'查证现实策略服务.txt',ref+'查证现实策略服务之ChatGPT篇.txt'])
def blocks(s):
    """Contiguous paragraph/fence blocks; preserve exact characters, no normalization."""
    lines=s.splitlines(keepends=True); result=[]; buf=[]; start=1; fence=None
    for n,line in enumerate(lines,1):
        if not buf: start=n
        buf.append(line)
        m=re.match(r'^\s*(`{3,}|~{3,})',line)
        if m:
            token=m.group(1)
            if fence is None: fence=token
            elif token[0]==fence[0] and len(token)>=len(fence): fence=None
        if not line.strip() and fence is None:
            result.append((start,''.join(buf))); buf=[]
    if buf: result.append((start,''.join(buf)))
    assert ''.join(b for _,b in result)==s
    return result
COMMON='''本輪整合日期：2026-10-07。原主文件正文與換行保留；本節及文末「來源增補」為新增內容。來源增補保存舊版與附件中尚未出現在主文的段落，以來源、行號及雜湊追溯；舊說法、模型答覆、程式碼及商業構想均屬歷史資料，不能因收錄而視作已核實事實。重複段落的覆蓋位置見整合台帳，原始來源檔仍保留。

本輪完成的是本地版本與內容覆蓋校對，並對下列關鍵主張作審校。其餘逐項外部事實核實尚未完成；未核實能力、數值、收入、合規及排名維持 UNKNOWN／待審。來源類別 P0/P1、模型引用標記、廠商宣傳及舊驗收回執均不等於 VERIFIED。

各版本相互矛盾時保留兩者，依主張、版本、時間、場景及證據裁決，不能用最新檔名自動判定真偽。主文件的版本名稱保留，整合日期另記。
'''
TECH='''### 技術、部署與證據審校

1. 機構、產品、軟體組件、技術能力、部署案例及認證須分開登記。一般企業分析、地面遙測、即時控制、飛行軟體及任務安全要求不同；不能從列名推論產品不適用，也不能把某產品宣稱為所有國家通用標準。StarRocks、Airflow、DolphinScheduler 等的適用性須以實際負載、延遲、可用性、部署與授權條件驗證。
2. NASA cFS 是飛行軟體框架，Open MCT 是任務控制視覺化框架。框架收錄或兩者並列不代表已有整合、任務認證或特定安全等級。商用 RTOS、開源 RTOS、框架、地面工具及 HPC 排程器不可混為同類。[NASA cFS](https://github.com/nasa/cFS)、[Open MCT](https://nasa.github.io/openmct/)。
3. NATO FMN 包括受治理的人員、流程與技術；Mattermost、Keycloak、WireGuard 等是候選組件，不能直接稱作 FMN 或等效替代。[NATO FMN](https://coi.nato.int/FMNPublic/SitePages/Home_RML_2.aspx)。STANAG 4778 涉及元資料綁定機制，不宜簡化為泛稱「完整性標籤」；是否符合標準仍須按版次、實作及測試核實。[NATO NISP](https://nhqc3s.hq.nato.int/Apps/Architecture/NISP/pdf/NISP-Vol2-v15-release.pdf)。
4. Palantir Apollo 的連線模式有實際條件：無預期連線的環境不會獲發部署計畫，轉送模式涉及 bundle 傳輸。不能把產品名稱當作無網路部署已解決的證據。[Apollo 連線設定](https://www.palantir.com/docs/apollo/managing-environments/environment-connection-settings)。
5. 開源、免費使用、可商用、可再散布及權重授權是不同問題；逐版本核對。Open-Meteo 免費 API 限非商業用途，資料授權與商業 API 訂閱亦不同。收益、毛利、零成本及最高效率等說法須有成本、客戶、授權及負載模型，現階段只作業務假設。[Open-Meteo 定價與授權](https://open-meteo.com/en/pricing)。
6. DO-178C 相關工具資格、單一任務軟體符合性與整間公司認證不同；SLSA、SBOM、NIST 等被引用不表示已符合或取得認證。VxWorks 版本與任務配對、SpaceOS 任務數、Maxar／Planet 資料量、未公開後端技術及性能數字，須逐條取得可定位來源，目前不得提升為 VERIFIED。
7. 原文中「StarRocks 不可能使用」「唯一通用標準」「某國全面禁用」「高毛利／無成本」等絕對說法不作本次整合結論。國別出口管制、採購規則、臨床監管、資料保護及跨境限制須按司法區、產品與日期另作核實。
'''
GEO='''### 合併後的研究閱讀順序

先讀本節的證據邊界，再讀既有機構登記、ISO 母表及 B02／B03／B04 批次索引，最後讀來源增補。meta.md 是既有主文件的歷史前綴，逐段台帳證明其內容已被覆蓋；web_version 與全量問答中的新增方案已保留在來源增補。

以 ISO 3166-1 國家／地區代碼連結機構與證據；249 是母表條目口徑，不表示 249 個主權國家，也不代表每國已有頂尖科技查證。批次表是版本快照，不能跨批次直接累加機構數。公司母子關係、研究所、政府機關、產品與別名使用不同 ID；研究登記不等同排名。

神經技術的侵入性、EEG／ECoG／微電極／fNIRS／TMS、讀取／寫入／雙向、人體試驗、帶寬、部署距離與監管狀態分欄。未公開值為 UNKNOWN，不填零；遠端網路存取不等於遠距腦訊號讀取。N0～N7 須先建立可測試定義，現有未證實資料不能據此判級。
'''
def redact(s):
    # Preserve byte-identical local originals; prevent publishing signed URL credentials in annexes.
    return re.sub(r'https?://[^\s<>\]\)]+',lambda m: m.group(0).split('?')[0]+'?[SIGNED_QUERY_REDACTED]' if re.search(r'(?i)(signature=|x-amz-|sig=|token=|credential=)',m.group(0)) else m.group(0),s)
OUT.mkdir(parents=True,exist_ok=True)
preview=OUT/'preview'; preview.mkdir(exist_ok=True)
coverage=[]; manifest=[]; outputs={}; snapshots=OUT/'originals'; snapshots.mkdir(exist_ok=True)
for family,(target,sources) in families.items():
    allpaths=list(dict.fromkeys([target]+sources))
    original=read(target); body=original.decode('utf-8-sig')
    if 'INTEGRATION_20261007_BEGIN' in body: raise SystemExit('Already integrated; do not rebaseline or duplicate.')
    known={sha(b.encode()):(target,n) for n,b in blocks(body)}
    annex=[]; added=0
    for source in allpaths:
        raw=read(source); digest=sha(raw); archive=snapshots/(digest+Path(source).suffix)
        if archive.exists() and archive.read_bytes()!=raw: raise SystemExit('Snapshot collision')
        if not archive.exists(): archive.write_bytes(raw)
        manifest.append(dict(family=family,path=source,sha256=digest,bytes=len(raw),target=target,snapshot=archive.relative_to(ROOT).as_posix()))
        fresh=[]
        for n,b in blocks(raw.decode('utf-8-sig')):
            h=sha(b.encode())
            if h in known:
                loc,ln=known[h]; state='ALREADY_COVERED'
            else:
                loc,ln=target,n; state='APPENDED_SOURCE_BLOCK'; known[h]=(target,n); fresh.append((n,b,h)); added+=1
            coverage.append(dict(family=family,source=source,source_line=n,block_sha256=h,characters=len(b),state=state,target=loc,source_snapshot=archive.relative_to(ROOT).as_posix(),redacted_display=redact(b)!=b))
        if fresh:
            rel=Path(__import__('os').path.relpath(ROOT/source,(ROOT/target).parent)).as_posix()
            annex.append('\n### 來源：'+source+'\n\n[原始來源](<'+rel+'>)；SHA256：`'+digest+'`。下列為未覆蓋段落；歷史主張未經收錄自動驗證。\n')
            for n,b,h in fresh:
                shown=redact(b); longest=max([len(x) for x in re.findall(r'`+',shown)]+[2]); fence='`'*(longest+1)
                annex.append('\n::: {.callout-note collapse="true"}\n來源第 '+str(n)+' 行；段落 '+h[:16]+'；UNKNOWN_INHERITED。\n\n'+fence+'text\n'+shown+('' if shown.endswith('\n') else '\n')+fence+'\n::: \n')
    intro='\n<!-- INTEGRATION_20261007_BEGIN -->\n## 2026-10-07 整合與審校說明\n\n'+COMMON
    if family in ('geostrategy','aerospace'): intro+=TECH
    if family=='geostrategy': intro+=GEO
    if family=='aerospace': intro+='\n### 報告用途\n\n本文件保留宇航資料栈比較原文；本輪併入網頁版的新增資訊。機構生態與全球登記的主入口仍為 `Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd` 及 ISO 母表。資料栈選擇依任務需求和可重現測試，原比較表不可當作全球供應商採用調查。\n'
    intro+='\n<!-- INTEGRATION_20261007_END -->\n'
    # Insert immediately after YAML, leaving every original byte intact and recoverable.
    offset=0
    if original.startswith(b'---'):
        m=re.search(rb'\r?\n---(?:\r?\n|$)',original[3:]); assert m
        offset=3+m.end()
    suffix='\n<!-- SOURCE_ANNEX_20261007_BEGIN -->\n## 2026-10-07 來源增補與歷史差異\n\n本章保留 '+str(added)+' 個先前未覆蓋段落。段落可能反映不同時期或相互矛盾的觀點；以來源台帳與審校說明解讀。簽名網址的查詢憑證只在原始本地來源保存，閱讀副本作遮蔽。\n'+''.join(annex)+'\n<!-- SOURCE_ANNEX_20261007_END -->\n'
    result=original[:offset]+intro.encode()+original[offset:]+suffix.encode()
    restored=result[:offset]+result[offset+len(intro.encode()):-len(suffix.encode())]
    assert restored==original
    dest=preview/target; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(result)
    outputs[target]=dict(original_sha256=sha(original),output_sha256=sha(result),bytes=len(result),added_blocks=added,original_byte_recovery=True)

assets=[]; columns=[]
familylookup={p:(fam,target) for fam,(target,sources) in families.items() for p in [target]+sources}
for row in baseline:
    p=row['path']; ext=Path(p).suffix.lower(); fam,target=familylookup.get(p,('independent',''))
    if p.startswith('.Rproj.user/') or p=='.Rhistory': role='runtime_metadata'; value='工作環境重現；不作科研證據'
    elif ext in ('.csv','.tsv','.json','.sqlite','.parquet'): role='structured_data'; value='實體／主張／來源／測量的查詢與追溯；粒度待逐表確認'
    elif ext in ('.qmd','.md','.txt','.tex','.bib'): role='source_document'; value='研究論述、來源與決策脈絡；歷史版本及待證主張亦保留'
    elif ext in ('.html','.pdf','.docx'): role='rendered_or_attachment'; value='交付閱讀或附件證據；不以渲染副本覆蓋來源'
    elif ext in ('.py','.r','.sql','.js','.yml','.yaml','.toml'): role='code_or_configuration'; value='可重現加工、計算及設定；須版本化與執行環境'
    else: role='other_asset'; value='媒體、樣式、依賴或其他資產；需人工業務定義'
    assets.append(dict(asset_id=sha(p.encode())[:24],path=p,sha256=row['sha256'],bytes=row['bytes'],role=role,family=fam,canonical_target=target,business_value_proposal=value,definition_status='PROPOSED_REVIEW_REQUIRED'))
    if ext in ('.csv','.tsv') and role!='runtime_metadata':
        try:
            with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:
                reader=csv.reader(f,delimiter='\t' if ext=='.tsv' else ','); header=next(reader); records=list(reader)
            for i,name in enumerate(header):
                vals=[r[i] if i<len(r) else '' for r in records]
                columns.append(dict(path=p,column_index=i+1,column_name=name,row_count=len(records),blank_count=sum(not v.strip() for v in vals),business_definition_status='REVIEW_REQUIRED',business_definition='保留原欄名；需確認粒度、單位、時效、來源、空值與業務用途'))
        except Exception as e: columns.append(dict(path=p,column_index=0,column_name='',row_count='',blank_count='',business_definition_status='PARSE_ERROR',business_definition=type(e).__name__))
csvout('source_manifest.csv',manifest,list(manifest[0])); csvout('block_coverage.csv',coverage,list(coverage[0])); csvout('asset_catalog.csv',assets,list(assets[0])); csvout('column_catalog.csv',columns,list(columns[0]))
(OUT/'delivery_plan.json').write_text(json.dumps(dict(baseline=str(BASE.relative_to(ROOT)),families=outputs,source_documents=len(manifest),block_records=len(coverage),assets=len(assets),columns=len(columns)),ensure_ascii=False,indent=2),encoding='utf-8')
dbpath=OUT/'project_information_catalog.sqlite'
if dbpath.exists(): dbpath.unlink()
with sqlite3.connect(dbpath) as db:
    for table,rows in [('assets',assets),('source_versions',manifest),('block_coverage',coverage),('columns',columns)]:
        fields=list(rows[0]); db.execute('CREATE TABLE "'+table+'" ('+','.join('"'+f+'" TEXT' for f in fields)+')')
        db.executemany('INSERT INTO "'+table+'" VALUES ('+','.join('?' for _ in fields)+')',[tuple(str(r[f]) for f in fields) for r in rows])
    db.execute('CREATE UNIQUE INDEX assets_path ON assets(path)'); db.execute('CREATE INDEX coverage_hash ON block_coverage(block_sha256)')
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
if '--apply' in sys.argv:
    if outputs!=prior_plan['families']: raise SystemExit('Reviewed preview differs; apply rejected.')
    expected={r['path']:r['sha256'] for r in baseline}
    for m in manifest:
        if sha(read(m['path']))!=expected[m['path']]: raise SystemExit('Baseline changed: '+m['path'])
    for target,plan in outputs.items():
        candidate=(preview/target).read_bytes()
        if sha(candidate)!=plan['output_sha256']: raise SystemExit('Preview hash mismatch')
        (ROOT/target).write_bytes(candidate)
    (OUT/'validation_receipt.json').write_text(json.dumps(dict(status='PASS_LOCAL_CONTENT_COVERAGE',original_bytes_preserved=True,all_selected_source_blocks_covered=True,external_fact_check='PARTIAL_NOT_COMPLETE',deleted_Report_Optimized_V2_absent=not (ROOT/ref/'Report-Optimized-V2.md').exists(),**dict(families=outputs,source_documents=len(manifest),blocks=len(coverage),assets=len(assets),columns=len(columns))),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(mode='apply' if '--apply' in sys.argv else 'preview',families=outputs,source_documents=len(manifest),blocks=len(coverage),assets=len(assets),columns=len(columns)),ensure_ascii=False,indent=2))
