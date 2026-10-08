from pathlib import Path
import csv,json,sqlite3,hashlib
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;T=R/'Reference/tables/27_global_expansion_b02_20261007';csv.field_size_limit(32*1024*1024);c=sqlite3.connect(O/'global_universe_v5.sqlite')
for name in ['registry_source_access_gaps','dataset_business_definitions']:
 c.execute('CREATE TABLE '+name+'(source_row INTEGER PRIMARY KEY,fields_json TEXT)')
 with (T/(name+'.csv')).open(encoding='utf-8-sig') as f:
  for i,r in enumerate(csv.DictReader(f),1):
   j=json.dumps(r,ensure_ascii=False);c.execute('INSERT INTO '+name+' VALUES(?,?)',(i,j));c.execute('INSERT INTO raw_records VALUES(?,?,?,?)',('GLOBAL_EXPANSION_B02',name,i,j))
c.commit();assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok';n=c.execute('SELECT COUNT(*) FROM raw_records').fetchone()[0];c.close();s=json.loads((O/'validation.json').read_text());old=s['total_raw_records'];s['total_raw_records']=n;s['currency_date_precision_counts']={'MONTH':153,'SOURCE_TEXT_REQUIRES_REVIEW':16};s['access_gaps_and_business_definitions_in_database']=True;(O/'validation.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
p=R/'Reference/Global_Universe_Expansion_B02_20261007.qmd';text=p.read_text(encoding='utf-8').replace(f'{old:,}列',f'{n:,}列');text+='\n169條貨幣日期中153條為單一月份，16條保留來源文字待核實。歷史空窗按來源整數年定位；跨BCE／CE的區間不自行定義年0。來源名稱可能同名異體，空窗表不是已消歧的同一國家生命週期。會員來源的授權有效時點仍需另核實，不能將接收日期當成全面有效授權日期。\n';p.write_text(text,encoding='utf-8')
manifest=[dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(T.glob('*.csv')) if p.name!='integration_input_manifest.csv']
with (T/'integration_input_manifest.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=['path','sha256']);w.writeheader();w.writerows(manifest)
print('Supplemental definitions and gaps retained in database; raw rows',n)
