from pathlib import Path
import csv,json,hashlib,sqlite3,collections,datetime,re
import openpyxl
from lxml import html
csv.field_size_limit(16*1024*1024)
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;T=R/'Reference/tables/23_listed_universe_b05_20261007';T.mkdir(exist_ok=True)
def dump(n,rows):
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
sources=[];tmx=[];cells=[];summary=[]
p=O/'raw/tmx_listed_companies.xlsx';w=openpyxl.load_workbook(p,read_only=True,data_only=True)
for sheet in w:
 sheet.reset_dimensions();values=[[v.isoformat() if isinstance(v,(datetime.date,datetime.datetime)) else v for v in row] for row in sheet.values];headers=values[9];exchange='TSXV' if 'TSXV' in sheet.title else 'TSX'
 for i,row in enumerate(values,1):cells.append(dict(sheet=sheet.title,excel_row=i,cells_json=json.dumps(row,ensure_ascii=False)))
 before=len(tmx)
 for i,row in enumerate(values[10:],11):
  if not any(v is not None for v in row):continue
  assert len(row)<=len(headers);raw=dict(zip(headers,row+[None]*(len(headers)-len(row))))
  assert raw['Co_ID'] and raw['Name'] and raw['Exchange']==exchange
  tmx.append(dict(record_id=f'{exchange}:{i}',source_issuer_id=raw['Co_ID'],exchange=exchange,issuer_name=raw['Name'],root_ticker=raw['Root\nTicker'],sector=raw['Sector'],market_iso_alpha2='CA',issuer_domicile='UNKNOWN',source_hq_region=raw['HQ\nRegion'],as_of='2026-08-31',raw_fields_json=json.dumps(raw,ensure_ascii=False)))
 count=len(tmx)-before;reported=values[7][3 if exchange=='TSXV' else 2];assert count==reported
 summary.append(dict(exchange=exchange,source_reported_issuers=reported,extracted_records=count,as_of='2026-08-31',reconciled=True))
assert len(tmx)==3768
dump('registry_tmx_issuer_records.csv',tmx);dump('tmx_workbook_rows.csv',cells);dump('tmx_count_reconciliation.csv',summary)
sources.append(dict(source='TMX_WORKBOOK',url='https://www.tsx.com/en/resource/571',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),records=len(tmx),as_of='2026-08-31',scope='TSX_TSXV_WORKBOOK_ALL_ROWS'))
p=O/'raw/nzsx.html';doc=html.fromstring(p.read_bytes());script=doc.xpath('//script[@id="__NEXT_DATA__"]')[0].text;data=json.loads(script);queries=data['props']['pageProps']['dehydratedState']['queries'];bykey={tuple(q['queryKey']):q['state']['data'] for q in queries}
active=bykey[('activeInstruments',)];quotes=bykey[('marketInstruments','NZSX')];info=bykey[('marketInfo','NZSX')];assert len(active)==len({x['code'] for x in active})
rows=[dict(record_id='NZX:'+x['code'],code=x['code'],source_security_name=x['name'],source_company_id=x['companyId'],ISIN=x['isin'],market_type=x['marketType'],trading_board=x['tradingBoard'],category=x['category'],subcategory=x['subCategory'],currency_code=x['currencyCode'],market_iso_alpha2='NZ',issuer_domicile='UNKNOWN',raw_fields_json=json.dumps(x,ensure_ascii=False)) for x in active]
qrows=[dict(code=x['code'],source_issuer_code=x['issuerCode'],source_issuer_name=x['issuerName'],currency=x['currency'],last_updated_at=x['lastUpdatedAt'],raw_fields_json=json.dumps(x,ensure_ascii=False)) for x in quotes]
table=doc.xpath('//table')[1];codes=[tr.xpath('./td')[0].text_content().strip() for tr in table.xpath('.//tr') if tr.xpath('./td')];display=int(re.search(r'Instrument Count:(\d+)',doc.xpath('//table')[0].text_content()).group(1))
assert set(codes)=={x['code'] for x in quotes}=={x['code'] for x in active if x['marketType']=='NZSX'} and len(codes)==display
dump('registry_nzx_active_instruments.csv',rows);dump('registry_nzsx_quote_issuer_records.csv',qrows)
reconciliation=[dict(displayed_mainboard_count=display,mainboard_table_rows=len(codes),market_quote_rows=len(quotes),active_mainboard_records=sum(x['marketType']=='NZSX' for x in active),embedded_market_info_count=info['instrumentCount'],embedded_count_agrees=info['instrumentCount']==display,market_info_raw_json=json.dumps(info,ensure_ascii=False),evidence_state='INTERNAL_SOURCE_COUNT_DISCREPANCY' if info['instrumentCount']!=display else 'SOURCE_COUNTS_AGREE')]
dump('nzx_count_reconciliation.csv',reconciliation)
sources.append(dict(source='NZX_MAINBOARD_PAGE',url='https://www.nzx.com/markets/NZSX',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),records=len(rows),as_of='RETRIEVED_2026-10-07_RECORD_TIMESTAMPS_PRESERVED',scope='EMBEDDED_ACTIVE_INSTRUMENTS_INCLUDES_OTHER_MARKET_TYPES'))
p=O/'raw/nzx_participants.html';doc=html.fromstring(p.read_bytes());participants=[]
for tr in doc.xpath('//table//tr'):
 td=tr.xpath('./td')
 if len(td)==13:
  name=' '.join(td[0].text_content().split());links=td[0].xpath('.//a/@href');flags=[]
  for x in td[1:]:
   flags.append(dict(text=' '.join(x.text_content().split()),icon_refs=x.xpath('.//*[local-name()="use"]/@href'),cell_html=html.tostring(x,encoding='unicode')))
  participants.append(dict(record_id=f'NZX_PARTICIPANT:{len(participants)+1}',participant_name=name,website=links[0] if links else '',market_iso_alpha2='NZ',issuer_domicile='UNKNOWN',regulatory_license_state='UNKNOWN_EXCHANGE_MEMBERSHIP_ONLY',membership_cells_json=json.dumps(flags,ensure_ascii=False),raw_row_html=html.tostring(tr,encoding='unicode')))
assert len(participants)==26
dump('registry_nzx_market_participants.csv',participants)
sources.append(dict(source='NZX_PARTICIPANTS',url='https://new.nzx.com/services/market-participants/all-market-participants',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),records=len(participants),as_of='RETRIEVED_2026-10-07_SOURCE_ASOF_UNKNOWN',scope='ALL_PAGE_PARTICIPANTS_NOT_ALL_LICENSEES'))
dump('source_manifest.csv',sources)
base=R/'reports/2026-10-07/listed_universe_b04/financial_universe_v1.sqlite';db=O/'financial_universe_v2.sqlite';assert not db.exists();old=sqlite3.connect(base);con=sqlite3.connect(db);old.backup(con);before_raw=old.execute('SELECT COUNT(*) FROM raw_records').fetchone()[0]
prior_manifest=read(R/'Reference/tables/22_listed_universe_b04_20261007/integration_input_manifest.csv')
assert len(prior_manifest)==18
for x in prior_manifest:assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']
new=[]
for x in tmx:new.append(('B05:'+x['record_id'],'LISTED_B05_TMX','CA',x['root_ticker'],x['issuer_name'],json.dumps(x,ensure_ascii=False),'SOURCE_CO_ID_LEGAL_ID_UNRESOLVED'))
for x in rows:new.append(('B05:'+x['record_id'],'LISTED_B05_NZX','NZ',x['code'],x['source_security_name'],json.dumps(x,ensure_ascii=False),'SOURCE_COMPANY_ID_LEGAL_ID_UNRESOLVED'))
con.executemany('INSERT INTO listing_records VALUES (?,?,?,?,?,?,?)',new)
coverage=[json.loads(x[0]) for x in old.execute('SELECT fields_json FROM country_coverage ORDER BY iso_alpha2')];counts=dict(con.execute('SELECT * FROM market_listing_counts'))
for x in coverage:
 x['listing_source_records']=counts.get(x['iso_alpha2'],0);x['listing_feed_state']='PARTIAL_SOURCE_INGESTION' if x['listing_source_records'] else 'NOT_YET_INGESTED'
 if x['iso_alpha2']=='NZ':x['broker_coverage']='EXCHANGE_PARTICIPANTS_ONLY_REGULATORY_FULL_LIST_PENDING'
 con.execute('UPDATE country_coverage SET fields_json=? WHERE iso_alpha2=?',(json.dumps(x,ensure_ascii=False),x['iso_alpha2']))
dump('registry_country_financial_coverage.csv',coverage)
manifest=[]
for p in sorted(T.glob('*.csv')):
 records=read(p)
 con.executemany('INSERT INTO raw_records VALUES (?,?,?,?)',[('FINANCIAL_B05',p.stem,i,json.dumps(x,ensure_ascii=False)) for i,x in enumerate(records,1)])
 assert [json.loads(x[0]) for x in con.execute('SELECT fields_json FROM raw_records WHERE namespace=? AND source_table=? ORDER BY source_row',('FINANCIAL_B05',p.stem))]==records
 manifest.append(dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=len(records)))
for table in ['raw_records','listing_records']:
 original=old.execute('SELECT * FROM '+table+' ORDER BY 1,2,3').fetchall();retained=con.execute('SELECT * FROM '+table+" WHERE "+("namespace!='FINANCIAL_B05'" if table=='raw_records' else "namespace NOT LIKE 'LISTED_B05%'")+' ORDER BY 1,2,3').fetchall();assert original==retained
assert con.execute('SELECT COUNT(*) FROM currency_entries').fetchone()[0]==449 and con.execute('SELECT COUNT(*) FROM fsa_firms').fetchone()[0]==1951
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';result=dict(tmx_records=len(tmx),nzsx_mainboard_records=len(quotes),nzx_active_instruments=len(active),nzx_participants=len(participants),nzx_other_markets=dict(collections.Counter(x['marketType'] for x in active)),nzx_embedded_count_discrepancy=info['instrumentCount']!=display,prior_raw_records_retained=before_raw,total_listing_source_records=con.execute('SELECT COUNT(*) FROM listing_records').fetchone()[0],total_raw_records=con.execute('SELECT COUNT(*) FROM raw_records').fetchone()[0],new_tables=len(manifest),prior_table_rows_exactly_retained=True,new_csv_roundtrip=True,global_complete=False)
con.close();old.close();dump('integration_input_manifest.csv',manifest)
(O/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');(O/'prior_snapshot_manifest.json').write_text(json.dumps(dict(path=base.relative_to(R).as_posix(),sha256=hashlib.sha256(base.read_bytes()).hexdigest()),indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
