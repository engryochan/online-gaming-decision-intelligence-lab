"""Read-only local ISO baseline audit; contextual definitions remain owner-pending."""
from pathlib import Path
import csv,json,hashlib,collections,re
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not (OUT/'validation.json').exists(),'Use a new revision batch'
old=ROOT/'reports/2026-10-07/reference_field_contracts/field_semantics_v4.csv'
rows=read(old);manifest={old:sha(old)}
country_def={
 'iso_numeric':'ISO 數字代碼的三位字串，保留前導零；不視為統計數值',
 'name_en':'本地版本中的英文名稱；不是本批對現行名稱逐國認證',
 'official_name_en':'本地版本的英文正式名稱；空值不代表該地區沒有正式名稱',
 'coverage_required':'是否要求列入本項目覆蓋核查的標記；不表示資料已查全',
 'inhabited_status':'本地版本的居住狀態描述／待核標記；不是網格、住戶或普查證明',
 'population_layer':'擬議人口資料來源層／接入指引；不是已導入人口觀測',
 'settlement_layer':'擬議聚落資料來源層／接入指引；不是全部聚落名錄',
 'organization_layer':'擬議組織與法人來源層／接入指引；不是已核實機構全集',
 'govtech_layer':'擬議政府數位科技來源層；有來源入口不代表已有全部國別指標',
 'scope_note':'此國家／地區版本的粒度、來源及查核範圍說明',
}
admin_def={
 'subdivision_code':'本地 ISO 3166-2 行政區代碼；須保留國別前綴，不能當純數字',
 'name':'本地快照中的行政區名稱，未逐區重新查證現行名稱',
 'type':'本地快照的行政區類型；跨國標籤不可直接推定同級權限',
 'parent_code':'本地快照的上級行政區代碼；空值不推定無上級治理機關',
 'source_standard':'本地資料引用的標準名稱與版次，不等於全部快照實際更新日期',
 'standard_status':'本地記錄宣稱的標準狀態；不等於已查證所有區域現行有效',
 'snapshot_library':'提供本地行政區快照的軟件庫及版本；區別於 ISO 官方即時發布',
 'un_salb_validation_source':'建議行政邊界核查來源入口；不是已驗證 SALB 邊界的證明',
 'national_geospatial_authority_validation_required':'要求國家地理主管機關核查的標記；TRUE 不表示已完成',
 'live_validation_required':'要求即時核查的標記；TRUE 不表示已完成即時核查',
 'scope_note':'行政區快照範圍限制；不宣称涵蓋所有市鎮、村落或政治單位',
}
changes=[];datasets={}
for r in rows:
    if r['definition_status']!='UNRESOLVED' or r['role']!='REFERENCE_DATA':continue
    country=r['path'].startswith('Reference/tables/01_country_area/registry_country_area_iso3166')
    admin=r['path']=='Reference/tables/02_admin_units/registry_admin_units_iso3166_2_20261004.csv'
    definitions=country_def if country else admin_def if admin else {}
    if r['column_name'] not in definitions:continue
    p=ROOT/r['path'];manifest[p]=sha(p);assert sha(p)==r['source_sha256']
    if r['path'] not in datasets:datasets[r['path']]=read(p)
    previous=r['definition'];definition=definitions[r['column_name']]
    # Header plus scope-bearing data; this is an interpretation, not an external fact certification.
    r['definition']=definition;r['definition_status']='PROPOSED_BASELINE_CONTEXT_REVIEW'
    r['definition_locator']=r['path']+':1; contextual interpretation of header and scope_note'
    changes.append(dict(path=r['path'],column_name=r['column_name'],previous_definition=previous,definition=definition,definition_locator=r['definition_locator'],business_approval='PENDING',current_external_fact_verification='NOT_PERFORMED'))
assert len(changes)==41,len(changes)
countries={p:r for p,r in datasets.items() if '/01_country_area/' in p}
sets=[];results=[]
for p,data in countries.items():
    codes=[r['iso_alpha2'] for r in data];assert len(data)==len(set(codes))==249
    assert len({r['iso_alpha3'] for r in data})==249
    assert len({r['iso_numeric'] for r in data})==249
    assert all(re.fullmatch('[A-Z]{2}',r['iso_alpha2']) and re.fullmatch('[A-Z]{3}',r['iso_alpha3']) and re.fullmatch('[0-9]{3}',r['iso_numeric']) for r in data)
    sets.append({(r['iso_alpha2'],r['iso_alpha3'],r['iso_numeric']) for r in data})
    results.append(dict(path=p,rows=len(data),unique_iso_alpha2=249,blank_official_name=sum(not r['official_name_en'] for r in data)))
assert all(s==sets[0] for s in sets)
admin_path='Reference/tables/02_admin_units/registry_admin_units_iso3166_2_20261004.csv'
admin=datasets[admin_path];keys={r['subdivision_code'] for r in admin};assert len(keys)==len(admin)==5046
parent_errors=[r for r in admin if r['parent_code'] and r['parent_code'] not in keys]
country_codes={x[0] for x in sets[0]};prefix_errors=[r for r in admin if not r['subdivision_code'].startswith(r['country_iso_alpha2']+'-') or r['country_iso_alpha2'] not in country_codes]
mapping={x[0]:x[1] for x in sets[0]};alpha3_errors=[r for r in admin if mapping.get(r['country_iso_alpha2'])!=r['country_iso_alpha3']]
by_key={r['subdivision_code']:r for r in admin};cross_parents=[r for r in admin if r['parent_code'] and by_key[r['parent_code']]['country_iso_alpha2']!=r['country_iso_alpha2']]
cycles=[]
for start in keys:
    seen=set();current=start
    while current:
        if current in seen:cycles.append(start);break
        seen.add(current);current=by_key[current]['parent_code']
counts=collections.Counter(r['country_iso_alpha2'] for r in admin)
enhanced=next(data for path,data in countries.items() if 'm49_e164' in path)
count_mismatches=[r['iso_alpha2'] for r in enhanced if int(r['iso3166_2_subdivision_count'])!=counts[r['iso_alpha2']]]
assert not parent_errors+prefix_errors+alpha3_errors+cross_parents+cycles+count_mismatches
write('definition_changes.csv',changes);write('field_semantics_v5.csv',rows)
write('remaining_unresolved.csv',[r for r in rows if r['definition_status']=='UNRESOLVED'])
write('source_manifest.csv',[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in manifest.items()])
write('country_baseline_checks.csv',results)
for p,h in manifest.items():assert sha(p)==h
result=dict(records=len(rows),definitions_added=41,unchanged_semantic_records=1948,unresolved_before=375,unresolved_after=334,country_baselines=results,code_triples_equal=True,admin_rows=5046,parent_links=sum(bool(r['parent_code']) for r in admin),parent_reference_errors=0,parent_cycles=0,country_code_errors=0,subdivision_count_mismatches=0,source_files_unchanged=len(manifest),current_iso_list_completeness='NOT_VERIFIED',political_or_head_of_state_facts='NOT_REVERIFIED',business_approval='PENDING')
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
