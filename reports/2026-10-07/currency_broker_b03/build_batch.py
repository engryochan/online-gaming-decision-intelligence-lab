from pathlib import Path
import csv,json,hashlib,sqlite3,unicodedata,re,datetime
import xml.etree.ElementTree as E
import openpyxl
from lxml import html
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;T=R/'Reference/tables/21_currency_broker_b03_20261007';T.mkdir(exist_ok=True)
def dump(name,rows):
 with (T/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def key(s):
 s=unicodedata.normalize('NFKD',s).upper().replace('(THE)','');return ''.join(c for c in s if c.isalnum() and not unicodedata.combining(c))
with (R/'Reference/tables/01_country_area/registry_country_area_iso3166_m49_e164_20261004.csv').open(encoding='utf-8-sig') as f:mother=list(csv.DictReader(f))
assert len(mother)==249
names={key(n):r['iso_alpha2'] for r in mother for n in [r['name_en'],r['official_name_en']] if n}
aliases={'BOLIVIA (PLURINATIONAL STATE OF)':'BO','CONGO (THE DEMOCRATIC REPUBLIC OF THE)':'CD','CONGO (THE)':'CG','FALKLAND ISLANDS (THE) [MALVINAS]':'FK','HOLY SEE (THE)':'VA','IRAN (ISLAMIC REPUBLIC OF)':'IR','KOREA (THE DEMOCRATIC PEOPLE’S REPUBLIC OF)':'KP','KOREA (THE REPUBLIC OF)':'KR','LAO PEOPLE’S DEMOCRATIC REPUBLIC (THE)':'LA','MICRONESIA (FEDERATED STATES OF)':'FM','MOLDOVA (THE REPUBLIC OF)':'MD','RUSSIAN FEDERATION (THE)':'RU','TAIWAN (PROVINCE OF CHINA)':'TW','TÜRKİYE':'TR','UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND (THE)':'GB','UNITED STATES OF AMERICA (THE)':'US','VENEZUELA (BOLIVARIAN REPUBLIC OF)':'VE','VIRGIN ISLANDS (BRITISH)':'VG','VIRGIN ISLANDS (U.S.)':'VI'}
aliasmap={key(k):v for k,v in aliases.items()};currency=[];sources=[]
for fname,tag,state in [('list-one.xml','CcyNtry','CURRENT'),('list-three.xml','HstrcCcyNtry','HISTORICAL')]:
 p=O/'raw'/fname;root=E.parse(p).getroot();entries=list(root.iter(tag));sources.append(dict(source=fname,url='https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/'+fname,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),as_of=root.attrib.get('Pblshd'),records=len(entries)))
 for i,x in enumerate(entries,1):
  n=x.findtext('CtryNm','');a=names.get(key(n),aliasmap.get(key(n),''));method='NORMALIZED_EXISTING_MOTHER_NAME' if key(n) in names else ('EXPLICIT_NAME_ALIAS_REVIEW_REQUIRED' if key(n) in aliasmap else 'UNMAPPED_OR_NON_COUNTRY_ENTITY')
  currency.append(dict(record_id=f'{state}:{i}',state=state,source_entity_name=n,iso_alpha2=a,link_method=method,currency_name=x.findtext('CcyNm',''),alphabetic_code=x.findtext('Ccy',''),numeric_code=x.findtext('CcyNbr',''),minor_unit=x.findtext('CcyMnrUnts',''),withdrawal_date=x.findtext('WthdrwlDt',''),is_fund=x.find('CcyNm').attrib.get('IsFund','') if x.find('CcyNm') is not None else '',raw_xml=E.tostring(x,encoding='unicode')))
dump('registry_iso4217_all_entries.csv',currency);dump('country_name_aliases.csv',[dict(source_entity_name=k,iso_alpha2=v,evidence_state='EDITORIAL_NAME_CROSSWALK_REVIEW_REQUIRED') for k,v in aliases.items()])
coverage=[]
for r in mother:
 hits=[x for x in currency if x['iso_alpha2']==r['iso_alpha2'] and x['state']=='CURRENT']
 coverage.append(dict(iso_alpha2=r['iso_alpha2'],name_en=r['name_en'],current_source_rows=len(hits),current_codes=';'.join(sorted({x['alphabetic_code'] for x in hits if x['alphabetic_code']})),currency_state='SOURCE_RELATION_FOUND_COUNTRY_LEGAL_STATUS_NOT_CERTIFIED' if hits else 'UNRESOLVED',all_locally_used_currencies='UNKNOWN',broker_coverage='FSA_AND_JPX_SOURCE_BATCH_ONLY' if r['iso_alpha2']=='JP' else 'NOT_YET_INGESTED',all_brokers_complete='UNKNOWN',all_listed_companies_complete='UNKNOWN'))
dump('registry_country_financial_coverage.csv',coverage)
p=O/'raw/kinyushohin.xlsx';w=openpyxl.load_workbook(p,read_only=True,data_only=True);cells=[];firms=[]
for s in w:
 s.reset_dimensions();values=[[v.isoformat() if isinstance(v,(datetime.date,datetime.datetime)) else v for v in row] for row in s.values]
 for i,row in enumerate(values,1):
  cells.append(dict(sheet=s.title,excel_row=i,cells_json=json.dumps(row,ensure_ascii=False)))
  if i>=14 and isinstance(row[1],str) and '第' in row[1] and row[3]:
   firms.append(dict(record_id=f'FSA:{i}',registration_number=row[1],registered_name=row[3],corporate_number=str(row[4]) if row[4] is not None else '',jurisdiction_iso_alpha2='JP',registration_date_source_serial=str(row[2]),type_one_flag=row[8],type_two_flag=row[9],advice_agency_flag=row[10],investment_management_flag=row[11],securities_related_flag=row[12],as_of='2026-08-31',raw_cells_json=json.dumps(row,ensure_ascii=False)))
assert len(firms)==1951 and sum(str(r['type_one_flag']).startswith('○') for r in firms)==293
dump('registry_fsa_financial_instrument_firms.csv',firms);dump('fsa_workbook_rows.csv',cells)
sources.append(dict(source='kinyushohin.xlsx',url='https://www.fsa.go.jp/menkyo/menkyoj/kinyushohin.xlsx',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),as_of='2026-08-31',records=len(firms)))
doc=html.parse(str(O/'raw/jpx_participants.html'));participants=[]
for tr in doc.xpath('//table[contains(@class,"widetable")]//tr'):
 td=tr.xpath('./td')
 if len(td)==7:
  v=[' '.join(x.text_content().split()) for x in td];participants.append(dict(record_id=f'JPX:{len(participants)+1}',participant_name=v[0],tse_general=v[1],ose_futures=v[2],ose_government_bond_futures=v[3],ose_commodity_futures=v[4],tocom_broker=v[5],tocom_trade=v[6],market_iso_alpha2='JP',entity_domicile='UNKNOWN',license_state='EXCHANGE_MEMBERSHIP_ONLY',raw_cells_json=json.dumps(v,ensure_ascii=False)))
assert len(participants)>100
dump('registry_jpx_trading_participants.csv',participants)
p=O/'raw/jpx_participants.html';sources.append(dict(source='jpx_participants.html',url='https://www.jpx.co.jp/english/rules-participants/participants/list/',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),as_of='RETRIEVED_2026-10-07',records=len(participants)));dump('source_manifest.csv',sources)
db=O/'currency_broker.sqlite';assert not db.exists();con=sqlite3.connect(db)
for name,rows in [('currency_entries',currency),('country_coverage',coverage),('fsa_firms',firms),('fsa_workbook_rows',cells),('jpx_participants',participants),('sources',sources)]:
 fields=list(rows[0]);con.execute('CREATE TABLE '+name+' ('+','.join('"'+x+'" TEXT' for x in fields)+')');con.executemany('INSERT INTO '+name+' VALUES ('+','.join('?' for x in fields)+')',[[None if r[x] is None else str(r[x]) for x in fields] for r in rows])
con.execute("CREATE VIEW type_one_firms AS SELECT * FROM fsa_firms WHERE type_one_flag LIKE '○%'")
assert [json.loads(x[0]) for x in con.execute('SELECT cells_json FROM fsa_workbook_rows')]==[json.loads(r['cells_json']) for r in cells]
for x in currency:assert E.fromstring(x['raw_xml']).findtext('CtryNm')==x['source_entity_name']
con.commit();con.close()
result=dict(current_entries=sum(x['state']=='CURRENT' for x in currency),historical_entries=sum(x['state']=='HISTORICAL' for x in currency),current_unique_codes=len({x['alphabetic_code'] for x in currency if x['state']=='CURRENT' and x['alphabetic_code']}),country_relations_found=sum(x['current_source_rows']>0 for x in coverage),unresolved_countries=[x['iso_alpha2'] for x in coverage if not x['current_source_rows']],fsa_firms=len(firms),fsa_type_one=293,jpx_participants=len(participants),raw_roundtrip=True,global_complete=False)
(O/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
