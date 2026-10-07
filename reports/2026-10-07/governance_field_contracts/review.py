"""Interpret historical governance fields; build a dated official-evidence work queue."""
from pathlib import Path
import csv,json,hashlib,collections
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not (OUT/'validation.json').exists(),'Use a new batch'
old=ROOT/'reports/2026-10-07/catalogue_field_review/field_semantics_v7.csv'
country=ROOT/'Reference/tables/01_country_area/registry_country_area_iso3166_20261004_enhanced.csv'
monarchy=ROOT/'Reference/tables/03_governance_monarchies/registry_sovereign_monarchies_20261004.csv'
sources={p:sha(p) for p in [old,country,monarchy]}
definitions={
 'iso_entry_class':'本地 ISO 條目範圍分類；條目存在不構成本批主權判定',
 'un_state_class':'本地 UN 國家／地區分類標籤；須另核官方口徑與有效期',
 'sovereign_parent_or_association':'本地上級或關聯政治實體描述，不直接推定單一主權或控制關係',
 'is_sovereign_monarchy':'本地君主政體選入標記；布林值是本批歷史分類，非即時憲制認證',
 'head_of_state_holder':'歷史資料記錄的元首姓名或共治姓名組合；不視為現任已核實',
 'head_of_state_title_en':'歷史元首職銜英文表述；須與國別及任期合讀',
 'head_of_state_title_local':'歷史元首職銜的本地語表述；不自動代表規範法律用語',
 'head_of_state_title_zh':'歷史元首職銜中文譯名；翻譯不新增權限證據',
 'head_of_state_title_class':'本地元首職銜分類，不等同於憲法權力類型',
 'monarchy_system':'歷史君主政體描述；須另核憲制來源，不作能力排名',
 'formal_power_class':'本地形式權力分類，非實際政治影響或軍事能力測量',
 'succession_type':'歷史元首產生／繼承方式分類；須按適用制度與日期核查',
 'commander_in_chief_status':'本地統帥權查核狀態或描述；職銜不自動推定指揮權限',
 'head_of_state_data_status':'历史人物／職銜資料施工及核查狀態；帶日期 VERIFIED 不延續為今日認證',
 'head_of_state_source':'歷史元首證據連結或待核來源說明；非本批取得原始響應的證明',
 'power_model_eligible':'本地模型候選範圍標記；True 不核准訓練、不證明指標已齊備',
 'national_power_data_status':'國家能力指標接入施工狀態，非實際能力分數',
 'verification_as_of':'此版本聲稱的核查截止日期；不以本批執行日期覆寫',
 'country':'歷史君主名錄的國家展示名稱；關聯以 ISO 鍵判定',
 'holder':'歷史君主名錄的元首姓名或共治姓名組合，未在本批核實現任',
 'title_en':'歷史君主名錄的英文職銜',
 'title_local':'歷史君主名錄的本地語職銜',
 'title_zh':'歷史君主名錄的中文譯名',
 'title_class':'歷史君主名錄的職銜分類，不等同權力分類',
 'system':'歷史君主名錄的政體描述，未在本批核實現行憲制',
 'source':'歷史君主名錄引用來源；連結不代表已核全文或現任',
}
a=read(old);b=[dict(r) for r in a];changes=[]
for r in b:
    p=ROOT/r['path']
    if p not in [country,monarchy] or r['definition_status']!='UNRESOLVED':continue
    assert sha(p)==r['source_sha256'];c=r['column_name'];assert c in definitions
    r['definition']=definitions[c];r['definition_status']='PROPOSED_BASELINE_CONTEXT_REVIEW'
    r['definition_locator']=r['path']+':1; contextual reading of historical columns; owner review required'
    changes.append(dict(path=r['path'],column_name=c,definition=definitions[c],owner_approval='PENDING',current_fact_verification='NOT_PERFORMED'))
assert len(changes)==28
assert len(a)==len(b)==1989
for x,y in zip(a,b):
    if x!=y:assert {k for k in x if x[k]!=y[k]}=={'definition','definition_status','definition_locator'}
assert sum(x!=y for x,y in zip(a,b))==28
remaining=[r for r in b if r['definition_status']=='UNRESOLVED'];assert len(remaining)==264
countries=read(country);monarchies=read(monarchy)
index={r['iso_alpha2']:r for r in countries};assert len(index)==249
assert len({r['iso_alpha2'] for r in monarchies})==43
mapping={'holder':'head_of_state_holder','title_en':'head_of_state_title_en','title_local':'head_of_state_title_local','title_zh':'head_of_state_title_zh','title_class':'head_of_state_title_class','system':'monarchy_system','formal_power_class':'formal_power_class','succession_type':'succession_type'}
differences=[]
for m in monarchies:
    assert m['iso_alpha2'] in index
    c=index[m['iso_alpha2']]
    for k,target in mapping.items():
        if m[k]!=c[target]:differences.append(dict(iso_alpha2=m['iso_alpha2'],monarchy_column=k,country_column=target,monarchy_value=m[k],country_value=c[target]))
queue=[]
for c in countries:
    queue.append(dict(iso_alpha2=c['iso_alpha2'],iso_alpha3=c['iso_alpha3'],historical_status=c['head_of_state_data_status'],historical_verification_as_of=c['verification_as_of'],historical_power_model_eligible=c['power_model_eligible'],review_status='PENDING_OFFICIAL_EVIDENCE',required_evidence='dated official holder/role source; applicable constitutional source; local status review if territory',current_holder_verified='UNKNOWN',current_power_verified='UNKNOWN',training_permission='NOT_GRANTED_BY_THIS_QUEUE'))
for p,h in sources.items():assert sha(p)==h
write('definition_changes.csv',changes);write('field_semantics_v8.csv',b);write('remaining_unresolved.csv',remaining);write('official_evidence_queue.csv',queue)
write('source_manifest.csv',[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in sources.items()])
if differences:write('cross_table_differences.csv',differences)
result=dict(pass_check=True,definitions_added=28,unchanged_records=1961,unresolved=264,queue_rows=len(queue),monarchy_rows=43,compared_columns_per_monarchy=8,cross_table_differences=len(differences),historical_status_counts=dict(collections.Counter(c['head_of_state_data_status'] for c in countries)),historical_power_eligible_counts=dict(collections.Counter(c['power_model_eligible'] for c in countries)),source_files_unchanged=3,current_facts_verified=False,owner_approval='PENDING')
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=True))
