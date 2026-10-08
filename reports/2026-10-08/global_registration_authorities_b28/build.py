from pathlib import Path
import csv,json,hashlib,collections,sqlite3,datetime,urllib.request
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent;T=R/'Reference/tables/53_global_registration_authorities_b28_20261008'
assert not (O/'validation_receipt.json').exists(),'Preserve completed batch'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
receipt=json.loads((O/'fetch_receipt.json').read_text());raw=R/receipt['file'];assert hashlib.sha256(raw.read_bytes()).hexdigest()==receipt['sha256']
authorities=read(raw);write('registry_registration_authorities_v1_9.csv',authorities)
codes=[r['Registration Authority Code'] for r in authorities]
write('registry_authority_code_multiplicity.csv',[dict(authority_code=c,source_rows=n,review='PRESERVE_JURISDICTION_VARIANTS_NOT_AUTOMATIC_DUPLICATES') for c,n in collections.Counter(codes).items() if n>1])
country_counts=collections.Counter(r['Country Code'] for r in authorities if r['Country Code'])
mother=read(R/'Reference/tables/28_global_market_sources_b03_20261008/registry_all_country_source_coverage.csv')
coverage=[dict(iso_alpha2=r['iso_alpha2'],authority_rows=country_counts[r['iso_alpha2']],authority_index_status='PRESENT_IN_GLEIF_RA_LIST' if country_counts[r['iso_alpha2']] else 'NOT_OBSERVED_IN_THIS_RA_RELEASE',all_local_authorities_complete='UNKNOWN',all_companies_complete='UNKNOWN') for r in mother]
write('registry_all_country_authority_coverage.csv',coverage)
write('registry_nonmother_authority_codes.csv',[dict(country_code=c,authority_rows=n,review='SOURCE_CODE_OUTSIDE_CURRENT_MOTHER_MAPPING_REVIEW') for c,n in country_counts.items() if c not in {r['iso_alpha2'] for r in mother}] or [dict(country_code='',authority_rows=0,review='NO_OUTSIDE_CODES_OBSERVED')])
bycode={r['Registration Authority Code']:r for r in authorities};identity=[]
man=read(R/'Reference/tables/52_global_registry_identity_b27_20261008/source_fetch_manifest.csv')
for r in man:
    if 'api.gleif.org' not in r['url']:continue
    p=R/r['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
    a=json.loads(p.read_bytes())['data']['attributes'];e=a['entity'];reg=a['registration'];ra=e['registeredAt']['id'];local=e['registeredAs'];authority=bycode.get(ra,{})
    identity.append(dict(lei=a['lei'],registration_authority_code=ra,registration_authority_name=authority.get('International name of Register',''),local_registration_number=local,registration_authority_website=authority.get('Website',''),authority_code_match='MATCHED_V1_9' if authority else 'UNRESOLVED',gleif_entity_status=e.get('status',''),lei_registration_status=reg.get('status',''),entity_creation_date=e.get('creationDate',''),lei_initial_registration_date=reg.get('initialRegistrationDate',''),lei_last_update=reg.get('lastUpdateDate',''),lei_next_renewal=reg.get('nextRenewalDate',''),gleif_validation_authority=reg.get('validatedAt',{}).get('id',''),gleif_validated_registration_number=reg.get('validatedAs',''),local_registry_result='NOT_INDEPENDENTLY_QUERIED',evidence='GLEIF_RECORD_AND_AUTHORITY_CODE_LIST_JOIN_NOT_LOCAL_REGISTRY_VERIFICATION'))
write('registry_lei_local_registration_bridge.csv',identity)
write('registry_local_registry_workqueue.csv',[dict(lei=r['lei'],authority_code=r['registration_authority_code'],local_registration_number=r['local_registration_number'],authority_url=r['registration_authority_website'],action='SEARCH_OFFICIAL_REGISTER_BY_LOCAL_ID',result='PENDING_ENTITY_EXTRACT',company_coverage='UNKNOWN') for r in identity])
con=sqlite3.connect(T/'global_registration_authorities_b28.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);keys=list(rs[0]);q=lambda s:'"'+s.replace('"','""')+'"';con.execute('CREATE TABLE '+q(p.stem)+' ('+','.join(q(k)+' TEXT' for k in keys)+')');con.executemany('INSERT INTO '+q(p.stem)+' VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for n,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==v
con.close();assert len(coverage)==249 and len(identity)==6 and all(r['authority_code_match']=='MATCHED_V1_9' for r in identity)
for p,h in json.loads((O/'baseline.json').read_text())['protected'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
stats=dict(authority_rows=len(authorities),unique_authority_codes=len(set(codes)),distinct_nonempty_country_codes=len(country_counts),repeated_code_source_rows=len(codes)-len(set(codes)),source_rows_without_country_code=sum(not r['Country Code'] for r in authorities),mother_rows=len(coverage),mother_areas_with_authorities=sum(r['authority_rows']>0 for r in coverage),mother_areas_without_observed_authorities=sum(r['authority_rows']==0 for r in coverage),lei_bridges=6,local_registry_entity_extracts=0,sqlite_counts=counts,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
notes={'redteam':'登記機關代碼只指定來源，不能證明已取得該公司的工商結果；特殊RA代碼及空國碼完整保留。','critic':'登記機關數不是公司數，GLEIF機關清單不是所有工商來源全集。','killcritic':'全表行數及不同機關代碼、重複代碼多司法管轄區行、249母表、6個LEI對應與CSV/SQL對賬；當地工商提取數0，明列待辦。','blindspot':'空國碼、地區/司法管轄區差異、地方登記、基金驗證機關、歷史代碼、改名與有效年代不機械合併。','blueprint':'LEI→RA代碼→當地登記號→官方工商結果；保留每層來源、版本和時間。續期日期不是公司有效期。','cheatsheet':'機關代碼匹配≠工商已核實；LEI續期≠上市有效期；來源未列≠該地區沒有登記機關；代碼空值≠0家公司。','actionplan':'已完成官方RA v1.9全表及249逐地區索引，6個工商登記號已展開查詢待辦；原清單2608項及分頁/封存缺口繼續保留。'}
for n,s in notes.items():(R/n/'global_registry_b28_20261008.md').write_text('# '+n+'｜B28\n\n'+s+'\n\n[報告](../Reference/Global_Registration_Authorities_B28_20261008.qmd)。\n',encoding='utf-8')
report='''---
title: "全球登記 B28：官方登記機關全表與逐地區身份來源索引"
date: 2026-10-08
format:
  html:
    toc: true
    embed-resources: true
---

## 實測交付

'''+f"保存 GLEIF RA v1.9 全部 {stats['authority_rows']} 條來源行、{stats['unique_authority_codes']} 個唯一機關代碼，包含 {stats['distinct_nonempty_country_codes']} 個非空國家／地區代碼及 {stats['source_rows_without_country_code']} 條空國碼來源。249條母表全部保留，{stats['mother_areas_with_authorities']} 個母表地區有來源機關，{stats['mother_areas_without_observed_authorities']} 個未在此版觀測到。"+'''

同一機關代碼可能跨司法管轄區重複出現，保留全部來源行與多重性表，不能按機關代碼機械丟棄。

## 法人身份橋與時間

六個B27 LEI全部匹配RA000156；當地登記號保持字串及前導零。RA000156對應Croatian Court Registry。分開記錄法人創建日期、LEI初始登記、最後更新及下次續期；續期不是法人或上市有效期。六個工商查詢工作列完整展開，尚未取得逐家公司工商提取結果，不升級為獨立身份核實。

## 官方證據與限制

[GLEIF官方來源頁](https://www.gleif.org/en/lei-data/code-lists/gleif-registration-authorities-list)提供[2026-09-30 RA v1.9 CSV](https://www.gleif.org/lei-data/code-lists/gleif-registration-authorities-list/2026-09-30_ra-list-v1.9.csv)。來源包含登記或驗證機關，不能視為全球工商來源全集，更不能視為全部公司名錄。

[Croatian Court Registry](https://sudreg.pravosudje.hr/)的官方搜索頁提供MBS與OIB查詢欄位；本輪只核定入口及RA映射，未提交每家公司查詢，不虛報已取得工商結果。未在此RA版出現不代表該地區沒有政府登記機關。母表是沿用現有249版次，未宣稱重新核定現行ISO全集；歷史政治實體另庫保留。

## 可對賬成果

[全機關表](tables/53_global_registration_authorities_b28_20261008/registry_registration_authorities_v1_9.csv)、[249逐地區索引](tables/53_global_registration_authorities_b28_20261008/registry_all_country_authority_coverage.csv)、[身份橋](tables/53_global_registration_authorities_b28_20261008/registry_lei_local_registration_bridge.csv)、[工商待辦](tables/53_global_registration_authorities_b28_20261008/registry_local_registry_workqueue.csv)、[SQLite](tables/53_global_registration_authorities_b28_20261008/global_registration_authorities_b28.sqlite)。全表、CSV／SQLite、來源雜湊及保護文件核對通過。七向文件更新；原清單2608項未嘗試及所有歷史／分頁待辦未結案。未匯入Windows Downloads文件。全球完整性UNKNOWN。
'''
(R/'Reference/Global_Registration_Authorities_B28_20261008.qmd').write_text(report,encoding='utf-8');print(json.dumps(stats))
