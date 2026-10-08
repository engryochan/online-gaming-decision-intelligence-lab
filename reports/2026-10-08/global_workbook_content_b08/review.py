from pathlib import Path
import json,csv,sqlite3,collections,hashlib,re
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/33_global_workbook_content_b08_20261008'
def read(name):return list(csv.DictReader((T/name).open(encoding='utf-8-sig')))
def write(name,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (T/name).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
manifests=read('registry_workbook_manifest.csv');dimensions=read('registry_worksheet_dimensions.csv')
con=sqlite3.connect(T/'global_workbook_content_b08.sqlite');reviews=[];roles=[]
for r in manifests:
    u=r['source_url'].lower();role='SOURCE_WORKBOOK_BUSINESS_SCOPE_PENDING'
    if 'microcr' in u:role='HISTORICAL_MICROCREDIT_OPERATOR_REGISTER_NOT_EQUITY_BROKER_LIST'
    elif 'bancomoc.mz' in u:role='HISTORICAL_FINANCIAL_INSTITUTION_REGISTER_LICENSE_SCOPE_PENDING'
    elif 'IBTTypeCodes'.lower() in u:role='TECHNICAL_INSTRUMENT_TYPE_CODE_DICTIONARY'
    elif 'Acquisition_of_Shares'.lower() in u:role='SHARE_ACQUISITION_SOURCE_RECORD_NOT_CURRENT_COMPANY_UNIVERSE'
    elif 'List-of-Online-Brokers'.lower() in u:role='HISTORICAL_2024_ONLINE_BROKER_SOURCE_LIST'
    elif 'dtc.xlsx' in u:role='SINGLE_SECURITY_HISTORICAL_TRADE_SERIES'
    elif 'Excluded_Securities'.lower() in u:role='EXCLUDED_SECURITY_LIST_NOT_ISSUER_UNIVERSE'
    roles.append(dict(workbook_sha256=r['workbook_sha256'],source_url=r['source_url'],business_role=role,date_tokens_json=json.dumps(re.findall(r'20\d{2}',u)),current_status='UNKNOWN_SOURCE_DATE_AND_LICENSE_SCOPE_REVIEW'))
for r in dimensions:
    rows=con.execute('SELECT row_number,values_json,types_json,extras_json FROM workbook_rows WHERE workbook_sha256=? AND sheet_index=? ORDER BY row_number',(r['workbook_sha256'],int(r['sheet_index']))).fetchall()
    observed=len(rows);expected=int(r['rows']);assert observed==expected
    assert [row[0] for row in rows]==list(range(1,expected+1))
    nonempty=0;errors=0;formulas=0;head=[]
    for number,values,types,extras in rows:
        values=json.loads(values);types=json.loads(types);extras=json.loads(extras)
        assert len(values)==int(r['columns']),r
        if any(x is not None and x!='' for x in values):
            nonempty+=1
            if len(head)<8:head.append(dict(row=number,values=values))
        errors+=sum(x in ['e',5] for x in types);formulas+=sum(x=='f' for x in types)
    reviews.append(dict(workbook_sha256=r['workbook_sha256'],sheet_index=r['sheet_index'],sheet_name=r['sheet_name'],expected_rows=expected,observed_rows=observed,columns=r['columns'],nonempty_rows=nonempty,blank_rows=expected-nonempty,error_typed_cells=errors,ooxml_formula_cells=formulas,first_nonempty_rows_json=json.dumps(head,ensure_ascii=False),dimension_reconciled=True))
write('registry_workbook_business_scope.csv',roles);write('registry_worksheet_reconciliation.csv',reviews)
for name in ['registry_workbook_business_scope.csv','registry_worksheet_reconciliation.csv']:
    rows=read(name);keys=list(rows[0]);table=Path(name).stem
    con.execute('CREATE TABLE "'+table+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')');con.executemany('INSERT INTO "'+table+'" VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rows])
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close()
baseline=json.loads((O/'baseline.json').read_text());protected=[]
for path,digest in baseline['files'].items():
    current=hashlib.sha256((R/path).read_bytes()).hexdigest()
    if 'Inteligent' not in path:assert current==digest
    protected.append(dict(path=path,baseline=digest,current=current,unchanged=digest==current,batch_action='NO_WRITE'))
summary=dict(reconciled_worksheets=len(reviews),rows=sum(r['observed_rows'] for r in reviews),nonempty_rows=sum(r['nonempty_rows'] for r in reviews),blank_rows=sum(r['blank_rows'] for r in reviews),error_typed_cells=sum(r['error_typed_cells'] for r in reviews),ooxml_formula_cells=sum(r['ooxml_formula_cells'] for r in reviews),role_counts=dict(collections.Counter(r['business_role'] for r in roles)),protected=protected,global_complete=False)
(O/'review_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in summary.items() if k!='protected'}))
