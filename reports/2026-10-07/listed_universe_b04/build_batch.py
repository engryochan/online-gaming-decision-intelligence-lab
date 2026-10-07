from pathlib import Path
import csv,json,hashlib,sqlite3,collections
csv.field_size_limit(16*1024*1024)
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;T=R/'Reference/tables/22_listed_universe_b04_20261007';T.mkdir(exist_ok=True)
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def dump(p,rows):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
p=O/'raw/ASXListedCompanies.csv';lines=p.read_text(encoding='utf-8-sig').splitlines();assert lines[0].startswith('ASX listed companies as at ')
data=list(csv.DictReader(lines[2:]));assert len(data)>1000 and all(None not in x for x in data)
asx=[dict(record_id=f'ASX:{i}',company_name=x['Company name'],listing_code=x['ASX code'],source_industry_group=x['GICS industry group'],market_iso_alpha2='AU',issuer_domicile='UNKNOWN',issuer_legal_identity='UNRESOLVED',as_of_source_text=lines[0],raw_fields_json=json.dumps(x,ensure_ascii=False)) for i,x in enumerate(data,1)]
assert len({x['listing_code'] for x in asx})==len(asx)
dump(T/'registry_asx_company_directory.csv',asx)
g=collections.Counter(x['source_industry_group'] for x in asx);dump(T/'asx_industry_analysis.csv',[dict(source_industry_group=k,directory_rows=v) for k,v in sorted(g.items())])
gaps=[dict(feed=f,url='https://nsearchives.nseindia.com/'+path,state='ACCESS_DENIED_NO_DATA_INGESTED',attempted_on='2026-10-07',market_iso_alpha2='IN') for f,path in [('NSE_EQUITY','content/equities/EQUITY_L.csv'),('NSE_SME','emerge/corporates/content/SME_EQUITY_L.csv'),('NSE_NAMECHANGE','content/equities/namechange.csv'),('NSE_SYMBOLCHANGE','content/equities/symbolchange.csv')]]
dump(T/'source_access_gaps.csv',gaps)
db=O/'financial_universe_v1.sqlite';assert not db.exists();con=sqlite3.connect(db)
con.execute('CREATE TABLE raw_records(namespace TEXT, source_table TEXT, source_row INTEGER, fields_json TEXT, PRIMARY KEY(namespace,source_table,source_row))')
manifest=[];inputs=[]
for folder,ns in [('19_global_listed_company_universe_20261007','LISTED_B01'),('20_global_listed_universe_b02_20261007','LISTED_B02'),('21_currency_broker_b03_20261007','CURRENCY_BROKER_B03')]:
 for p in sorted((R/'Reference/tables'/folder).glob('*.csv')):inputs.append((p,ns))
inputs.append((T/'registry_asx_company_directory.csv','LISTED_B04'))
for p,ns in inputs:
 records=read(p);headers=list(records[0]);con.executemany('INSERT INTO raw_records VALUES (?,?,?,?)',[(ns,p.stem,i,json.dumps(x,ensure_ascii=False)) for i,x in enumerate(records,1)])
 restored=[json.loads(x[0]) for x in con.execute('SELECT fields_json FROM raw_records WHERE namespace=? AND source_table=? ORDER BY source_row',(ns,p.stem))];assert restored==records
 manifest.append(dict(namespace=ns,path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=len(records),fields_json=json.dumps(headers,ensure_ascii=False)))
con.execute('CREATE TABLE listing_records(record_id TEXT PRIMARY KEY,namespace TEXT,market_iso_alpha2 TEXT,listing_code TEXT,source_name TEXT,source_record_json TEXT,issuer_identity_state TEXT)')
normalized=[]
for x in read(R/'Reference/tables/19_global_listed_company_universe_20261007/registry_listed_security.csv'):
 normalized.append(('B01:'+x['security_record_id'],'LISTED_B01',x['market_country_iso_alpha2'],x['symbol'],x['security_name'],json.dumps(x,ensure_ascii=False),'UNRESOLVED'))
for x in read(R/'Reference/tables/20_global_listed_universe_b02_20261007/registry_listing_records.csv'):
 normalized.append(('B02:'+x['record_id'],'LISTED_B02',x['market_iso_alpha2'],x['security_code'],x['security_name'],json.dumps(x,ensure_ascii=False),'UNRESOLVED'))
for x in asx:normalized.append(('B04:'+x['record_id'],'LISTED_B04','AU',x['listing_code'],x['company_name'],json.dumps(x,ensure_ascii=False),'UNRESOLVED'))
con.executemany('INSERT INTO listing_records VALUES (?,?,?,?,?,?,?)',normalized)
coverage=read(R/'Reference/tables/21_currency_broker_b03_20261007/registry_country_financial_coverage.csv')
markets=collections.Counter(x[2] for x in normalized)
for x in coverage:
 x['listing_source_records']=markets[x['iso_alpha2']];x['listing_feed_state']='PARTIAL_SOURCE_INGESTION' if x['listing_source_records'] else 'NOT_YET_INGESTED';x['as_of_snapshot']='2026-10-07'
dump(T/'registry_country_financial_coverage.csv',coverage)
con.execute('CREATE TABLE country_coverage(iso_alpha2 TEXT PRIMARY KEY,fields_json TEXT)');con.executemany('INSERT INTO country_coverage VALUES (?,?)',[(x['iso_alpha2'],json.dumps(x,ensure_ascii=False)) for x in coverage])
con.execute("CREATE VIEW fsa_firms AS SELECT source_row,fields_json FROM raw_records WHERE namespace='CURRENCY_BROKER_B03' AND source_table='registry_fsa_financial_instrument_firms'")
con.execute("CREATE VIEW currency_entries AS SELECT source_row,fields_json FROM raw_records WHERE namespace='CURRENCY_BROKER_B03' AND source_table='registry_iso4217_all_entries'")
con.execute('CREATE VIEW market_listing_counts AS SELECT market_iso_alpha2,COUNT(*) AS source_records FROM listing_records GROUP BY market_iso_alpha2')
checks={
 'prior_listing_rows_retained':con.execute("SELECT COUNT(*) FROM listing_records WHERE namespace IN ('LISTED_B01','LISTED_B02')").fetchone()[0]==34938,
 'new_asx_rows':con.execute("SELECT COUNT(*) FROM listing_records WHERE namespace='LISTED_B04'").fetchone()[0]==len(asx),
 'all_249_countries':con.execute('SELECT COUNT(*) FROM country_coverage').fetchone()[0]==249,
 'fsa_all_1951':con.execute('SELECT COUNT(*) FROM fsa_firms').fetchone()[0]==1951,
 'currency_all_449':con.execute('SELECT COUNT(*) FROM currency_entries').fetchone()[0]==449,
 'all_csv_rows_roundtrip':True}
assert all(checks.values());con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';raw_count=con.execute('SELECT COUNT(*) FROM raw_records').fetchone()[0];con.close()
dump(T/'integration_input_manifest.csv',manifest)
sources=[dict(source='ASX_OFFICIAL_DIRECTORY_CSV',url='https://www.asx.com.au/asx/research/ASXListedCompanies.csv',sha256=hashlib.sha256((O/'raw/ASXListedCompanies.csv').read_bytes()).hexdigest(),rows=len(asx),as_of_raw=lines[0],scope='SOURCE_DIRECTORY_ALL_ROWS_COUNTRY_ALL_ISSUERS_NOT_CERTIFIED')];dump(T/'source_manifest.csv',sources)
result=dict(asx_directory_rows=len(asx),listing_source_records=len(normalized),raw_csv_records=raw_count,input_tables=len(inputs),market_counts=dict(markets),checks=checks,global_complete=False)
(O/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
(O/'queries.sql').write_text("SELECT * FROM market_listing_counts;\nSELECT COUNT(*) FROM fsa_firms;\nSELECT COUNT(*) FROM currency_entries;\nSELECT namespace,source_table,COUNT(*) FROM raw_records GROUP BY namespace,source_table;\nSELECT listing_code,source_name FROM listing_records WHERE market_iso_alpha2='AU' ORDER BY listing_code;\n",encoding='utf-8')
print(json.dumps(result))
