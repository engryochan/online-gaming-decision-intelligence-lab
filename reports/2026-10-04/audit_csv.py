from pathlib import Path
import csv,json,collections
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def rows(p):
    with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
p_old='Reference/tables/01_country_area/registry_country_area_iso3166_20261003.csv'
p_new='Reference/tables/01_country_area/registry_country_area_iso3166_m49_e164_20261004.csv'
p_admin='Reference/tables/02_admin_units/registry_admin_units_iso3166_2_20261004.csv'
p_games='Reference/tables/04_gaming_catalogue/大秦赋算筹_游戏下载清单_20261002.csv'
p_tables='V2.0.1/feature/ods-data-dictionary-governance/docs/03_Data_Dictionary/01_ODS_TABLE_LIST.csv'
p_columns='V2.0.1/feature/ods-data-dictionary-governance/docs/03_Data_Dictionary/02_ODS_FULL_DATA_DICTIONARY.csv'
old,new,admin,games,tables,columns=[rows(p) for p in (p_old,p_new,p_admin,p_games,p_tables,p_columns)]
def dup(items):return [k for k,v in collections.Counter(items).items() if v>1]
by_code={x['iso_alpha2']:x for x in new}; actual=collections.Counter(x['country_iso_alpha2'] for x in admin)
table_keys={(x['TABLE_SCHEMA'],x['TABLE_NAME']) for x in tables}
column_keys=[(x['TABLE_SCHEMA'],x['TABLE_NAME'],x['COLUMN_NAME']) for x in columns]
ordinal=collections.defaultdict(list)
for x in columns:ordinal[(x['TABLE_SCHEMA'],x['TABLE_NAME'])].append(int(x['ORDINAL_POSITION']))
summary={
 'row_counts':{p:len(rs) for p,rs in zip((p_old,p_new,p_admin,p_games,p_tables,p_columns),(old,new,admin,games,tables,columns))},
 'old_country_duplicate_alpha2':dup(x['iso_alpha2'] for x in old),
 'new_country_duplicate_alpha2':dup(x['iso_alpha2'] for x in new),
 'old_new_country_key_difference':sorted({x['iso_alpha2'] for x in old}^{x['iso_alpha2'] for x in new}),
 'admin_duplicate_codes':dup(x['subdivision_code'] for x in admin),
 'admin_unknown_country_codes':sorted(set(actual)-set(by_code)),
 'admin_declared_count_mismatches':[dict(code=k,declared=v['iso3166_2_subdivision_count'],actual=actual[k]) for k,v in by_code.items() if int(v['iso3166_2_subdivision_count'])!=actual[k]],
 'nsgt_true_rows':sum(x['un_nsgt_status']=='TRUE' for x in new),
 'space_status_counts':dict(collections.Counter(x['space_ecosystem_status'] for x in new)),
 'download_flag_counts':dict(collections.Counter(x['安装包已下载'] for x in games)),
 'ods_duplicate_table_keys':dup((x['TABLE_SCHEMA'],x['TABLE_NAME']) for x in tables),
 'ods_duplicate_column_keys':dup(column_keys),
 'ods_column_tables_not_in_table_list':sorted(set(ordinal)-table_keys),
 'ods_tables_without_column_rows':sorted(table_keys-set(ordinal)),
 'ods_noncontiguous_ordinals':[k for k,v in ordinal.items() if sorted(v)!=list(range(1,len(v)+1))],
 'empty_project_files':[p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and '.Rproj.user' not in p.parts and 'reports' not in p.parts and p.stat().st_size==0]
}
(OUT/'csv_audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=True,indent=2))
