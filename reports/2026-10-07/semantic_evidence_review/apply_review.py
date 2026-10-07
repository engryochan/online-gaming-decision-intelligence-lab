"""Apply narrow editorial corrections and scoped evidence, preserving pre-edit versions."""
from pathlib import Path
import csv,json,hashlib,re,sqlite3,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
expected={r['path']:r['sha256'] for r in csv.DictReader((ROOT/'reports/2026-10-06/workspace_change_audit/semantics_20261007_start_files.csv').open(encoding='utf-8-sig'))}
def sha(b): return hashlib.sha256(b).hexdigest()
claims=[
 ('C01','MAGE','MAGE 由 NGA 與 BIT Systems 合作開發；不是 Esri ArcGIS 內含產品','VERIFIED_SCOPED','開發歸屬與官方 MIT 授權描述；不證明所有場景性能或安全認證','https://ngageoint.github.io/MAGE/about/','About paragraphs on developer and license'),
 ('C02','Athea','2021-05-27 Thales 與 Atos 宣布成立 Athea；原 Helsing×Saab 說法錯誤','VERIFIED_HISTORICAL','歷史成立公告；不單獨核實2026股權或Eviden當期關係','https://www.thalesgroup.com/en/print/pdf/node/13916','2021-05-27 press release page 1'),
 ('C03','Ansys|Synopsys','Synopsys 在 2025-07-17 完成收購 Ansys','VERIFIED_EVENT','收購完成事件；預期協同與收益未因此成為實現值','https://investor.synopsys.com/news/news-details/2025/Synopsys-Completes-Acquisition-of-Ansys/default.aspx','July 17 2025 announcement first paragraph'),
 ('C04','FMN','FMN 為包含人員、流程與技術的受治理框架','VERIFIED_DEFINITION','官方框架定義；工具組合等效性與符合性尚未驗證','https://coi.nato.int/FMNPublic/SitePages/Home_RML_2.aspx','What is FMN?'),
 ('C05','Open.Meteo','Free/Open-Access API 方案不提供商業使用；付費方案提供商業授權','VERIFIED_SERVICE_TERMS','2026-10-07 所讀服務方案條件；不擴展為資料或自架授權判定','https://open-meteo.com/en/pricing','Commercial Use Licence and plan table')]
rows=[dict(claim_id=i,topic=pattern,statement=s,evidence_state=e,verification_scope=scope,primary_url=url,locator=loc,reviewed_on='2026-10-07',source_body_snapshot='NOT_SAVED_WEB_TOOL_READ',reviewer='Codex scoped review') for i,pattern,s,e,scope,url,loc in claims]
def output(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader();w.writerows(rows)
geo='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd'; aero='Reference/Aerospace_Ecosystem_Report.qmd'
targets=[geo,aero,'Reference/Project_Data_Architecture_20261007.qmd','Reference/Project_Information_Integration_20261007.qmd']
updates={}; manifests=[]; locations=[]; archive=OUT/'originals';archive.mkdir(exist_ok=True)
for p in targets:
    original=(ROOT/p).read_bytes(); assert sha(original)==expected[p],'User changed '+p
    snapshot=archive/(sha(original)+'.qmd'); snapshot.write_bytes(original)
    text=original.decode('utf-8'); before=text
    if p in (geo,aero):
        for n,line in enumerate(text.splitlines(),1):
            for row in rows:
                if re.search(row['topic'],line,re.I): locations.append(dict(claim_id=row['claim_id'],path=p,baseline_sha256=sha(original),baseline_line=n,baseline_snapshot=snapshot.relative_to(ROOT).as_posix(),match_state='KEYWORD_LOCATOR_NOT_INDIVIDUAL_CLAIM_VERIFICATION'))
        note='\n<!-- SEMANTIC_REVIEW_20261007_BEGIN -->\n### 本輪一手證據裁決與欄位盤點補正\n\nMAGE 應與 Esri ArcGIS 分列，官方資料記錄由 NGA 與 BIT Systems 合作開發；Athea 的 2021 年成立公告為 Thales／Atos，原 Helsing×Saab 說法有誤，當期股權另核。Synopsys 於 2025-07-17 完成收購 Ansys。FMN 不是聊天／身份／網路工具清單；Open-Meteo 免費 API 方案不提供商業使用。裁決只涵蓋明確主張，不推論性能、軍方驗收或當期法規。\n\n[一手來源、適用範圍、欄位業務定義與 DGEF 對接](Project_Semantics_Evidence_Review_20261007.qmd)。欄位盤點修復大型 JSON 儲存格解析後為 1,989 筆；其中 768 筆仍待定義。歷史異文保留於原始快照／來源附錄；本節為當期裁決。\n<!-- SEMANTIC_REVIEW_20261007_END -->\n'
        assert text.count('<!-- INTEGRATION_20261007_END -->')==1
        text=text.replace('<!-- INTEGRATION_20261007_END -->',note+'<!-- INTEGRATION_20261007_END -->')
        if p==aero:
            fixes=[('| **Athea** | Helsing × Saab 合资 | 欧洲主权化战场 AI；与 Palantir 同场竞标 | P2 |','| **Athea** | 2021 年由 Thales × Atos 宣布成立 | 国防、情报与内部安全大数据／AI 平台；2026股权与竞争／部署主张另核 | 历史成立公告已核；其他待核 |'),('**Esri ArcGIS Pro / Enterprise / ArcGIS for Defense**（含 MAGE、军标符号库 MIL-STD-2525）——几乎所有现代军事 GIS 的基础（P1）','**Esri ArcGIS Pro / Enterprise / ArcGIS for Defense**（军标符号支持须按产品版本核对）。**MAGE 单列**：NGA 与 BIT Systems 合作开发的移动态势感知软件；普遍采用及性能主张另核。'),('Snowflake + Databricks + Airflow + Teamcenter；Athea（Helsing×Saab）','Snowflake + Databricks + Airflow + Teamcenter（本行国别采用仍需案例）；Athea 不作为德国／Helsing×Saab 归属证据，2021年成立关系为 Thales×Atos')]
            for old,new in fixes:
                assert old in text.split('<!-- SOURCE_ANNEX_20261007_BEGIN -->')[0], 'Expected original wording absent'
                text=text.replace(old,new,1)
            # Reverse edits independently proves all non-targeted text was preserved.
            restored=text
            for old,new in reversed(fixes): restored=restored.replace(new,old,1)
            assert restored.replace(note,'',1)==before
        else: assert text.replace(note,'',1)==before
    elif 'Data_Architecture' in p:
        text+='\n## 本輪已核對的既有底座\n\nDGEF/artifacts/dgef.sqlite 已有 44 張表，本輪唯讀完整性與外鍵檢查通過。它承接實體、主張、證據、觀測、授權與時間；本文件的 PostgreSQL 等是擴展方案，不能理解為項目尚無資料底座。新文件目錄與語義目錄均為旁側目錄，未替換或改寫 DGEF。[核查與對接方案](Project_Semantics_Evidence_Review_20261007.qmd)。\n'
        assert text.startswith(before)
    else:
        text+='\n## 業務語義與一手查證續批\n\n[本輪續批報告](Project_Semantics_Evidence_Review_20261007.qmd)：修復大型 JSON 欄位盤點缺口，現為 1,989 筆欄位記錄；提出具體定義與價值用途，列出仍未決定義。五項一手主張裁決已連回兩份主報告，既有 DGEF 44 表完成唯讀結構核查。前述 1,983 為上一批目錄口徑；舊驗收回執只適用其原版本雜湊。\n'
        assert text.startswith(before)
    result=text.encode(); updates[p]=result
    manifests.append(dict(path=p,before_sha256=sha(original),after_sha256=sha(result),before_snapshot=snapshot.relative_to(ROOT).as_posix(),untargeted_text_preserved=True))
for p in targets: assert sha((ROOT/p).read_bytes())==expected[p],'Concurrent edit '+p
for p,b in updates.items(): (ROOT/p).write_bytes(b)
output('claim_review.csv',rows);output('claim_locations.csv',locations); output('edit_manifest.csv',manifests)
with sqlite3.connect(OUT/'semantic_catalog.sqlite') as db:
    for table,data in [('claim_review',rows),('claim_locations',locations)]:
        db.execute('create table '+table+' ('+','.join('"'+k+'" TEXT' for k in data[0])+')')
        db.executemany('insert into '+table+' values ('+','.join('?' for _ in data[0])+')',[tuple(str(v) for v in r.values()) for r in data])
    assert db.execute('pragma integrity_check').fetchone()[0]=='ok'
(OUT/'editorial_validation.json').write_text(json.dumps(dict(status='PASS',targets=len(targets),claim_decisions=len(rows),keyword_locations=len(locations),edits=manifests,original_data_and_dgef_unchanged=True),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(status='PASS',targets=len(targets),claim_decisions=len(rows),keyword_locations=len(locations)),ensure_ascii=False))
