from pathlib import Path
import csv, json, hashlib, subprocess, urllib.request, datetime, collections, sqlite3
from decimal import Decimal, InvalidOperation
from pypdf import PdfReader

O=Path(__file__).resolve().parent; R=O.parents[2]
T=R/'Reference/tables/68_ssod_evidence_b44_20261009'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    assert rs
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0])); w.writeheader(); w.writerows(rs)
assert not (O/'baseline.json').exists(), 'Do not refresh an existing baseline'
T.mkdir(); (O/'raw').mkdir()
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
protected={p:sha(R/p) for p in tracked if p and Path(p).suffix in ('.md','.qmd') and (R/p).is_file()}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),
    starting_status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),protected=protected),indent=2)+'\n',encoding='utf-8')
urls=[
 ('ssod_landing.html','https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C01690'),
 ('ssod_geoportal.html','https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C01690/html'),
 ('ssod_metadata.xml','https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C01690/xml'),
 ('documentation_listing.xml','https://www.ncei.noaa.gov/oa/synoptic-summary-of-the-day/?list-type=2&prefix=v2/doc/'),
 ('ssodv2_DOCUMENTATION.pdf','https://www.ncei.noaa.gov/oa/synoptic-summary-of-the-day/v2/doc/ssodv2_DOCUMENTATION.pdf'),
 ('cc0_deed.html','https://creativecommons.org/publicdomain/zero/1.0/'),
 ('cc0_legalcode.html','https://creativecommons.org/publicdomain/zero/1.0/legalcode'),
 ('spdx_cc0.html','https://spdx.org/licenses/CC0-1.0')]
receipts=[]
for name,url in urls:
    r=dict(evidence_scope='NEW_FETCH',source_file='',sha256='',url=url,fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',error='')
    try:
        with urllib.request.urlopen(url,timeout=20) as response:
            b=response.read(5000001); r['http_status']=response.status
        assert len(b)<=5000000
        p=O/'raw'/name; p.write_bytes(b); r.update(source_file=p.relative_to(R).as_posix(),sha256=sha(p))
    except Exception as e:
        r.update(error=type(e).__name__,http_status=getattr(e,'code',r['http_status']))
    receipts.append(r)
assert (O/'raw/ssod_landing.html').is_file() and (O/'raw/ssodv2_DOCUMENTATION.pdf').is_file()
landing=(O/'raw/ssod_landing.html').read_text(encoding='utf-8')
assert 'CC0-1.0' in landing and 'publicdomain/zero/1.0' in landing
rights=[dict(dataset='gov.noaa.ncdc:C01690',scope='SSOD_VERSION_2_DATASET_ONLY',spdx='CC0-1.0',
    copyright_state='OFFICIAL_DATASET_LANDING_PAGE_EXPLICIT_CC0',commercial_copyright_use='PERMITTED_BY_CC0_WITH_OTHER_RIGHTS_UNCHANGED',
    citation='KEEP_NCEI_REQUESTED_AUTHOR_SUBSET_ACCESS_DATE_CITATION',doi_state='SOURCE_STILL_HAS_DOI_PLACEHOLDER_NOT_RESOLVED',
    quality_state='LICENSE_DOES_NOT_CERTIFY_VALUES_OR_IDENTITIES',other_sources='NOT_APPLIED_TO_GSOD_OR_ALL_NOAA_DATA',
    source_file='reports/2026-10-09/ssod_evidence_b44/raw/ssod_landing.html',source_sha256=sha(O/'raw/ssod_landing.html'))]
write('registry_dataset_rights_adjudication.csv',rights)
pdf=PdfReader(O/'raw/ssodv2_DOCUMENTATION.pdf')
text='\n'.join(p.extract_text() or '' for p in pdf.pages)
(O/'raw/ssodv2_DOCUMENTATION.txt').write_text(text,encoding='utf-8')
old_pdf=R/'reports/2026-10-09/ssod_schema_b38/raw/ssodv2_DOCUMENTATION.pdf'
pdf_same=sha(old_pdf)==sha(O/'raw/ssodv2_DOCUMENTATION.pdf')
# Token hits are evidence-search aids, not proof that a semantic rule exists.
doc_audit=[dict(document='SSODv2_PDF',pages=len(pdf.pages),sha256=sha(O/'raw/ssodv2_DOCUMENTATION.pdf'),same_bytes_as_b38=pdf_same,
    negative_9999_9_token_found='-9999.9' in text,negative_9999_token_found='-9999' in text,
    missing_word_occurrences=text.lower().count('missing'),formal_sentinel_rule_state='NOT_ESTABLISHED_BY_THIS_REVIEW',
    numeric_release=False)]
write('registry_document_recheck.csv',doc_audit)
fields=['mean_temperature','mean_dew_point_temperature','mean_sea_level_pressure','mean_station_level_pressure','mean_visibility',
        'mean_wind_speed','max_wind_speed','max_wind_gust','max_temperature','min_temperature','total_precipitation','snow_depth']
samples=[R/'reports/2026-10-09/ssod_schema_b38/raw/SSOD_USW00003812_2023.csv']+sorted((R/'reports/2026-10-09/station_mapping_b39/raw').glob('SSOD_*_2024.csv'))
assert len(samples)==4
profiles=[];suspects=[];total_days=0
for p in samples:
    rows=read(p); assert len(rows[0])==31
    total_days+=len(rows)
    receipts.append(dict(evidence_scope='PRIOR_FETCH_LOCAL_BYTES_CHECKED',source_file=p.relative_to(R).as_posix(),sha256=sha(p),url='',fetched_utc='',http_status='',error=''))
    for field in fields:
        counts=collections.Counter();attrs=collections.Counter()
        for n,r in enumerate(rows,1):
            raw=r[field];category='FINITE_RAW_VALUE_NOT_RELEASED'
            if not raw.strip(): category='EMPTY_TOKEN'
            else:
                try:
                    d=Decimal(raw)
                    if not d.is_finite(): category='NONFINITE_TOKEN'
                    elif d==Decimal('-9999.9'): category='OBSERVED_NEGATIVE_9999_9_PENDING_FORMAL_RULE'
                except InvalidOperation: category='UNPARSEABLE_TOKEN'
            counts[category]+=1
            attr=r.get(field+'_Measurement_Code','')
            if category!='FINITE_RAW_VALUE_NOT_RELEASED':
                attrs[attr]+=1
                suspects.append(dict(source_file=p.relative_to(R).as_posix(),source_sha256=sha(p),source_row=n,
                    station=r['STATION'],date=r['DATE'],field=field,raw_value=raw,raw_measurement_code=attr,
                    category=category,normalized_value='',numeric_release=False))
        assert sum(counts.values())==len(rows)
        profiles.append(dict(source_file=p.relative_to(R).as_posix(),station=rows[0]['STATION'],field=field,rows=len(rows),
            observed_negative_9999_9=counts['OBSERVED_NEGATIVE_9999_9_PENDING_FORMAL_RULE'],empty_tokens=counts['EMPTY_TOKEN'],
            nonfinite_tokens=counts['NONFINITE_TOKEN'],unparseable_tokens=counts['UNPARSEABLE_TOKEN'],
            finite_other_tokens=counts['FINITE_RAW_VALUE_NOT_RELEASED'],suspect_measurement_codes_json=json.dumps(dict(attrs)),
            numeric_release=False))
assert sum(r['observed_negative_9999_9'] for r in profiles if r['station']=='USW00003812')==514
write('registry_source_receipts.csv',receipts)
write('registry_48_field_missing_profiles.csv',profiles)
write('registry_suspect_value_evidence.csv',suspects)
con=sqlite3.connect(T/'ssod_evidence_b44.sqlite');counts={}
for p in T.glob('*.csv'):
    rows=read(p);keys=list(rows[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')')
    con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rows]);counts[p.stem]=len(rows)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for k,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+k+'"').fetchone()[0]==v
con.close();assert all(sha(R/p)==h for p,h in protected.items())
stats=dict(new_source_requests=8,fetch_errors=sum(bool(r['error']) for r in receipts),dataset_rights='OFFICIAL_SSODV2_CC0_1_0',
    documentation_same_as_b38=pdf_same,prior_sample_files=4,sample_days=total_days,field_profiles=len(profiles),
    suspect_values=len(suspects),sample_cells_audited=total_days*12,numeric_release=False,
    sqlite_counts=counts,old_documents_preserved=True,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
report='''---
title: "B44：SSODv2授權補證、現行文件與四份樣本缺值覆核"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 授權證據補齊

[NCEI官方SSODv2落地頁](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C01690)明列資料集適用CC0-1.0，已保存原始頁面與SHA256；先前Geoportal視圖沒有同等完整展示，不再以該視圖的缺項當作授權未公布。這是C01690／SSODv2資料集的版權證據，不擴展到所有NOAA產品或舊GSOD。

[CC0條款](https://creativecommons.org/publicdomain/zero/1.0/legalcode)允許版權範圍內的重用、修改與商業用途，其他權利與免責條件仍須按條款處理。保留NCEI要求的作者、子集與存取日期引用，不將它誤寫成CC0強制署名條件；官方DOI仍為佔位字串，不能捏造DOI。授權證據不代替值品質、身份映射與商業收益驗證。

## 文件與缺值覆核

重新取得現行SSODv2格式PDF並比對B38原始字節，讀取全部頁面。四份既有樣本為2023 ASHEVILLE及2024 ENJA、ENSB、GVAC，僅重新核對本地字節與原值，不聲稱四份觀測已重新下載或具有全球代表性。12個量測欄位逐站統計，所有疑似缺值保留原值及對應屬性碼，沒有產生已放行的數值。

缺值規則仍未由本輪來源明確建立，觀察到的-9999.9僅列待核；不得借用上游GHCNh或舊GSOD規則替代SSODv2定義。有限文件prefix查詢亦不能當作掃遍整個官方網站。

## 交付與下一步

'''+ '統計：`'+json.dumps(stats)+'`。\n\n'+'''
[授權裁定](tables/68_ssod_evidence_b44_20261009/registry_dataset_rights_adjudication.csv)、[來源收據](tables/68_ssod_evidence_b44_20261009/registry_source_receipts.csv)、[48項欄位統計](tables/68_ssod_evidence_b44_20261009/registry_48_field_missing_profiles.csv)、[逐值待核證據](tables/68_ssod_evidence_b44_20261009/registry_suspect_value_evidence.csv)、[文件比對](tables/68_ssod_evidence_b44_20261009/registry_document_recheck.csv)、[SQLite](tables/68_ssod_evidence_b44_20261009/ssod_evidence_b44.sqlite)。

15項測站佐證與25項未結保留於B43，不在本輪重作身份裁定。125筆舊風速衝突、全球金融、工商與歷史政治實體清單仍開放。下一步以欄位特定正式規則核缺值與屬性碼，再決定是否能作新舊量測比較；SDG業務分析保持凍結，Untitled不恢復。
'''
(R/'Reference/SSOD_Evidence_B44_20261009.qmd').write_text(report,encoding='utf-8')
notes={'redteam':'CC0不等於來源無錯，也不擴及所有NOAA資料集。','critic':'先前Geoportal視圖不完整；新增官方落地頁證據補齊而不改寫歷史批次。',
 'killcritic':'明列CC0足以更新資料集版權判定，不應因數值缺口否定已取得的授權證據。','blindspot':'引用要求與CC0條件分開；DOI佔位不可補造；四站樣本不代表全球。',
 'blueprint':'資料授權、來源版本、缺值／屬性碼及身份映射分層裁定。','cheatsheet':'SSODv2 CC0有來源；缺值尚待定；原值保留，数值未放行。',
 'actionplan':'按48项欄位統計查正式缺值與屬性定義，B43測站缺口與其他全球工作保持開放。'}
for n,v in notes.items():(R/n/'ssod_evidence_b44_20261009.md').write_text('# '+n+' | B44\n\n'+v+'\n\n[報告](../Reference/SSOD_Evidence_B44_20261009.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
