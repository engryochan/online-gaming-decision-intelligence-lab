from pathlib import Path
import csv,json,hashlib,sqlite3,collections
from decimal import Decimal
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/56_weather_units_b31_20261009'
assert not (O/'validation_receipt.json').exists(),'Preserve completed batch'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
receipts=json.loads((O/'source_receipts.json').read_text());doc=next(r for r in receipts if r['file'])
assert hashlib.sha256((R/doc['file']).read_bytes()).hexdigest()==doc['sha256']
rules={'TEMP':('F','C','9999.9'),'DEWP':('F','C','9999.9'),'SLP':('mb','hPa','9999.9'),'STP':('mb','hPa','9999.9'),'VISIB':('mi','m','999.9'),'WDSP':('kn','m/s','999.9'),'MXSPD':('kn','m/s','999'),'GUST':('kn','m/s','999.9'),'MAX':('F','C','9999.9'),'MIN':('F','C','9999.9'),'PRCP':('in','mm','99.99'),'SNDP':('in','mm','999.9')}
dictionary=[dict(field=k,source_unit=v[0],normalized_unit=v[1],missing_sentinel=v[2],documentation_url=doc['url'],rule='EXACT_DOCUMENTED_SENTINEL_NOT_GENERIC_ALL_NINES',original_precision='UNCHANGED_BY_CONVERSION') for k,v in rules.items()]
write('registry_variable_units.csv',dictionary)
def convert(value,unit):
    v=Decimal(value)
    if unit=='F':return (v-32)*Decimal(5)/9
    if unit=='kn':return v*Decimal(1852)/3600
    if unit=='mi':return v*Decimal('1609.344')
    if unit=='in':return v*Decimal('25.4')
    return v
assert convert('32','F')==0 and convert('1','in')==Decimal('25.4')
rs=read(R/'Reference/tables/55_weather_observation_b30_20261009/registry_daily_observation_rows.csv');values=[];daily=[]
for row in rs:
    f=json.loads(row['raw_fields_json']);daily.append(dict(station_id=row['station_id'],date=row['date'],frshtt_raw=f.get('FRSHTT',''),event_zero_semantics='NO_OR_NOT_REPORTED_NOT_CONFIRMED_ABSENCE',prcp_attribute=f.get('PRCP_ATTRIBUTES',''),prcp_day_completeness='INCOMPLETE_OR_UNREPORTED' if f.get('PRCP_ATTRIBUTES','') in ['H','I'] else 'ACCUMULATION_WINDOW_REVIEW_NOT_AUTOMATIC_MIDNIGHT_DAY',max_attribute=f.get('MAX_ATTRIBUTES',''),min_attribute=f.get('MIN_ATTRIBUTES',''),max_min_window='REPORT_TIME_VARIES_BY_SOURCE',day_basis='GMT_SOURCE_SUMMARY_NOT_LOCAL_CALENDAR'))
    for field,(unit,target,sentinel) in rules.items():
        raw=f.get(field,'');clean=raw.strip();status='PRESENT';normalized=''
        try:
            v=Decimal(clean)
            if v==Decimal(sentinel):status='MISSING_DOCUMENTED_SENTINEL'
            elif v.is_finite():normalized=format(convert(clean,unit).quantize(Decimal('0.000001')),'f')
            else:status='NONFINITE_REVIEW'
        except Exception:status='PARSE_REVIEW'
        flag=f.get(field+'_ATTRIBUTES','')
        eligibility='RAW_SOURCE_MEASUREMENT_NOT_MODEL_VALIDATED'
        if status!='PRESENT':eligibility='NO_NUMERIC_ANALYSIS'
        elif field=='PRCP' and flag in ['H','I']:eligibility='INCOMPLETE_OR_UNREPORTED_NOT_COMPLETE_DAILY_TOTAL'
        values.append(dict(source_url=row['source_url'],source_row=row['source_row'],station_id=row['station_id'],date=row['date'],field=field,raw_value=raw,source_unit=unit,normalized_value=normalized,normalized_unit=target,missing_state=status,attribute_raw=flag,analysis_eligibility=eligibility,normalization_rule='B31_DOCUMENTED_UNITS_V1'))
write('registry_normalized_weather_values.csv',values);write('registry_daily_quality_context.csv',daily)
summary=[]
for station in sorted({r['station_id'] for r in values}):
    for field in rules:
        a=[r for r in values if r['station_id']==station and r['field']==field]
        summary.append(dict(station_id=station,field=field,source_rows=len(a),missing_sentinels=sum(r['missing_state']=='MISSING_DOCUMENTED_SENTINEL' for r in a),parse_or_nonfinite=sum(r['missing_state'] not in ['PRESENT','MISSING_DOCUMENTED_SENTINEL'] for r in a),numeric_values=sum(bool(r['normalized_value']) for r in a),incomplete_precipitation=sum(r['analysis_eligibility'].startswith('INCOMPLETE') for r in a),climate_statistics='NOT_COMPUTED_NOT_GLOBAL_SAMPLE'))
write('registry_variable_quality_summary.csv',summary)
con=sqlite3.connect(T/'weather_units_b31.sqlite');counts={}
for p in T.glob('*.csv'):
    a=read(p);keys=list(a[0]);q=lambda s:'"'+s.replace('"','""')+'"';con.execute('CREATE TABLE '+q(p.stem)+' ('+','.join(q(k)+' TEXT' for k in keys)+')');con.executemany('INSERT INTO '+q(p.stem)+' VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in a]);counts[p.stem]=len(a)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for n,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==v
con.close();assert len(values)==len(rs)*12 and len(daily)==len(rs)
assert all(not r['normalized_value'] for r in values if r['missing_state']=='MISSING_DOCUMENTED_SENTINEL')
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in json.loads((O/'baseline.json').read_text())['protected'].items())
stats=dict(input_days=len(rs),variable_rows=len(values),missing_values=sum(r['missing_state']=='MISSING_DOCUMENTED_SENTINEL' for r in values),parse_review=sum(r['missing_state']=='PARSE_REVIEW' for r in values),incomplete_precipitation_rows=sum(r['analysis_eligibility'].startswith('INCOMPLETE') for r in values),sqlite_counts=counts,raw_values_preserved=True,missing_zero_fill=False,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
notes={'redteam':'每欄精確缺值規則，禁止999值全局替換；原始值及標記完整保存，缺值不轉零。','critic':'轉換單位不提升來源量測精度；六站不是全球樣本，不發佈全球氣候指标。','killcritic':'2125日×12變數對賬；缺值標準化值为空；32F→0C與1英寸→25.4mm檢查，CSV/SQL與雜湊驗收。','blindspot':'降水H/I不完整；0降水可能含trace；FRSHTT=0含未報告；極值與降水窗口不一定是本地午夜日。','blueprint':'不可變原值→版本化單位/缺值字典→長表→逐變數品質上下文→待核模型輸入；原日期與屬性獨立。','cheatsheet':'缺值≠0；事件0≠確定沒有；單位轉換≠精度提高；ISSUED/ISO/LEI問題與氣象模型證據分職。','actionplan':'已核定12欄單位及缺值，產生長表和72個站×變數摘要；下一步核對觀測窗口、站点/來源精度，再擴展分層站點及回測。'}
for n,s in notes.items():(R/n/'weather_units_b31_20261009.md').write_text('# '+n+'｜B31\n\n'+s+'\n\n[報告](../Reference/Weather_Units_B31_20261009.qmd)。\n',encoding='utf-8')
report='''---
title: "B31：NOAA日摘要單位、缺值與品質標準化"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 實測结果

'''+f"B30的 {len(rs)} 個站日，逐12變數展開為 {len(values)} 條長表；標記 {stats['missing_values']} 個官方缺值、{stats['parse_review']} 個解析待核、{stats['incomplete_precipitation_rows']} 條H/I降水品質限制。原值與屬性完整保留，缺值標準化為空／SQL文字空值，不填0；另有missing_state明示，未冒充SQL NULL。"+'''

## 官方證據與规则

[NOAA官方GSOD格式文件](https://www.ncei.noaa.gov/data/global-summary-of-the-day/doc/readme.txt)本輪成功下載；文件與HTTP收據及SHA256保存。12欄逐欄缺值，華氏轉攝氏、節轉米每秒、英里轉米、英寸轉毫米，毫巴數值等同hPa。轉換值保留6小數是運算格式，不代表來源精度提高。MXSPD依本版文件用999，未自行假定其他缺值變體。

原始日摘要以GMT為基础；極值與降水彙整窗口可能不同。H/I降水記錄維持不完整／未報告類別；零降水可包括微量，事件0含未報告。空值與品質限制不能當零降水或確定沒有事件，不計年度降水或災害率。

## 對賬交付與限制

[單位字典](tables/56_weather_units_b31_20261009/registry_variable_units.csv)、[標準化長表](tables/56_weather_units_b31_20261009/registry_normalized_weather_values.csv)、[逐日品質上下文](tables/56_weather_units_b31_20261009/registry_daily_quality_context.csv)、[逐變數摘要](tables/56_weather_units_b31_20261009/registry_variable_quality_summary.csv)、[SQLite](tables/56_weather_units_b31_20261009/weather_units_b31.sqlite)。全部行數、完整性及保護文件雜湊通過；原始B30與B29不覆寫。六站僅管線測試，非全球氣候樣本或預報能力核實。原金融、法人、歷史與分頁待辦保留，SDG業務分析保持凍結，沒有商業收益證據。
'''
(R/'Reference/Weather_Units_B31_20261009.qmd').write_text(report,encoding='utf-8');print(json.dumps(stats))
