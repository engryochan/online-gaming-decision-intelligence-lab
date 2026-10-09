from pathlib import Path
import csv,json,sqlite3,collections
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/59_pending_recheck_b35_20261009'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(p,rs):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
p=T/'registry_new_station_normalized_values.csv';rs=read(p);conflicts=[]
for r in rs:
    if r['field']=='MXSPD' and r['raw_value'].strip()=='999.9':
        conflicts.append(dict(station_id=r['station_id'],date=r['date'],source_url=r['source_url'],source_row=r['source_row'],field=r['field'],raw_value=r['raw_value'],documented_sentinel='999',assessment='SUSPECTED_SENTINEL_DOCUMENTATION_SOURCE_CONFLICT_NOT_ADJUDICATED',action='PRESERVE_RAW_WITHHOLD_NUMERIC_ANALYSIS'))
        r.update(normalized_value='',missing_state='DOCUMENTATION_SOURCE_SENTINEL_CONFLICT_REVIEW',analysis_eligibility='NO_NUMERIC_ANALYSIS_PENDING_SENTINEL_ADJUDICATION')
assert len(conflicts)==125;write(p,rs);write(T/'registry_mxspd_sentinel_conflicts.csv',conflicts)
counts=collections.Counter(r['station_id'] for r in conflicts)
q=T/'registry_new_station_quality_summary.csv';summary=read(q)
for r in summary:r['sentinel_documentation_conflicts']=counts[r['station_id']]
write(q,summary)
con=sqlite3.connect(T/'pending_recheck_b35.sqlite')
for name,rows in [('registry_new_station_normalized_values',rs),('registry_new_station_quality_summary',summary),('registry_mxspd_sentinel_conflicts',conflicts)]:
    con.execute('DROP TABLE IF EXISTS "'+name+'"');keys=list(rows[0]);con.execute('CREATE TABLE "'+name+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')');con.executemany('INSERT INTO "'+name+'" VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rows]);assert con.execute('SELECT COUNT(*) FROM "'+name+'"').fetchone()[0]==len(rows)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close()
s=json.loads((O/'validation_receipt.json').read_text(encoding='utf-8'));s.update(sentinel_documentation_conflicts=125,conflicting_values_withheld=True);s['sqlite_counts']['registry_mxspd_sentinel_conflicts']=125;(O/'validation_receipt.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=R/'Reference/Pending_Recheck_B35_20261009.qmd';text=p.read_text(encoding='utf-8');text=text.replace('解析／非有限數覆核0項。','解析／非有限數覆核0項；另有125筆MXSPD=999.9與官方說明缺值999不一致，列為DOCUMENTATION_SOURCE_SENTINEL_CONFLICT_REVIEW，保留原值、標準化值留空，尚未裁定為缺值或有效量測。');text=text.replace('## 可對賬交付','[125筆風速缺值衝突台帳](tables/59_pending_recheck_b35_20261009/registry_mxspd_sentinel_conflicts.csv)須在後續模型輸入前單獨裁定；不沿用舊六站沒有該值而未觸發的情況。\n\n## 可對賬交付');p.write_text(text,encoding='utf-8')
for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']:
    p=R/n/'pending_recheck_b35_20261009.md';p.write_text(p.read_text(encoding='utf-8')+'\n新增125筆MXSPD=999.9與說明999衝突；原值保留，數值分析暫扣，不能當作極大風速。\n',encoding='utf-8')
print('PASS: 125 suspect MXSPD values withheld; CSV/SQLite revised and aligned')
