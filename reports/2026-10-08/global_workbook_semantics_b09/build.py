from pathlib import Path
import csv,json,sqlite3,hashlib,unicodedata,re,collections,datetime
O=Path(__file__).resolve().parent;R=O.parents[2];P=R/'Reference/tables/33_global_workbook_content_b08_20261008';T=R/'Reference/tables/34_global_workbook_semantics_b09_20261008';T.mkdir(parents=True,exist_ok=True)
assert not (T/'global_workbook_semantics_b09.sqlite').exists(),'Preserve completed output'
def read(n):return list(csv.DictReader((P/n).open(encoding='utf-8-sig')))
def norm(v):return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',str(v or '').casefold()) if not unicodedata.combining(c)).split())
def ident(v):return ' '.join(unicodedata.normalize('NFKC',str(v or '')).casefold().split())
def dumps(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'))
roles={r['workbook_sha256']:r for r in read('registry_workbook_business_scope.csv')};manifest={r['workbook_sha256']:r for r in read('registry_workbook_manifest.csv')}
source=sqlite3.connect('file:'+str(P/'global_workbook_content_b08.sqlite')+'?mode=ro',uri=True);con=sqlite3.connect(T/'global_workbook_semantics_b09.sqlite');source.backup(con)
names=['nome da instituicao','nome do operador','nome da firma','nome do agente','nome do comerciante','comerciante','name of member','name of company','company','name of individual or entity','nome']
trade=['nome comercial','denominacao','firma','estabelecimento'];ids=['code no','reference','isin','code','member id']
records=[];annotations=[];schemas=[];dates=[];workbooks=[]
for sha,r in roles.items():
    url=r['source_url'];role=r['business_role']
    if 'goodbody.ie' in url:role='PRIIPS_FUND_SHARE_CLASS_PERFORMANCE_SCENARIO'
    elif 'bdcb.gov.bn' in url:role='HISTORICAL_DESIGNATED_PERSON_OR_ENTITY_SOURCE_LIST'
    elif 'icexindia.com' in url:role='BLANK_MEMBER_GST_REGISTRATION_TEMPLATE'
    elif 'agentes-banc' in url:role='HISTORICAL_BANK_AGENT_NETWORK'
    elif sha.startswith(('486442','2a2716')):role='HISTORICAL_BANK_BRANCH_DISTRIBUTION_MATRIX'
    workbooks.append(dict(workbook_sha256=sha,source_url=url,prior_role=r['business_role'],reviewed_role=role,scope_evidence='SOURCE_URL_PLUS_OBSERVED_HEADERS_AND_SHEET_CONTENT',current_license_status='UNKNOWN'))
lookup={r['workbook_sha256']:r for r in workbooks}
for dim in read('registry_worksheet_dimensions.csv'):
    sha=dim['workbook_sha256'];si=int(dim['sheet_index']);sn=dim['sheet_name'];role=lookup[sha]['reviewed_role'];url=lookup[sha]['source_url']
    rows=[dict(row=n,values=json.loads(v),types=json.loads(t)) for n,v,t in source.execute('SELECT row_number,values_json,types_json FROM workbook_rows WHERE workbook_sha256=? AND sheet_index=? ORDER BY row_number',(sha,si))]
    sheetrole=role
    if norm(sn)=='lista negra':sheetrole='HISTORICAL_BLACKLIST_SHEET_NOT_CURRENT_LICENSE'
    elif norm(sn)=='indeferimentos':sheetrole='HISTORICAL_REFUSED_APPLICATION_SHEET_NOT_LICENSE'
    elif norm(sn) in ['comentarios','version control']:sheetrole='SOURCE_NOTES_OR_VERSION_HISTORY'
    elif norm(sn) in ['tabela','sheet2'] and role.startswith('HISTORICAL_MICROCREDIT'):sheetrole='PROVINCE_AGGREGATE_NOT_ENTITY_REGISTER'
    header=None;keys=[]
    for row in rows[:30]:
        normalized=[norm(x) for x in row['values']]
        match=any(x in names+ids+['fund','mnemonic'] for x in normalized)
        if match and sum(bool(x) for x in normalized)>=2:
            header=row['row'];keys=normalized;break
    if role=='EXCLUDED_SECURITY_LIST_NOT_ISSUER_UNIVERSE':header=1;keys=['symbol']
    if sheetrole in ['SOURCE_NOTES_OR_VERSION_HISTORY','PROVINCE_AGGREGATE_NOT_ENTITY_REGISTER','HISTORICAL_BANK_BRANCH_DISTRIBUTION_MATRIX','BLANK_MEMBER_GST_REGISTRATION_TEMPLATE']:header=None;keys=[]
    nameindex=next((keys.index(k) for k in names if k in keys),None);tradeindex=next((keys.index(k) for k in trade if k in keys),None);idindex=next((keys.index(k) for k in ids+['symbol','mnemonic'] if k in keys),None)
    count=0;section='';rawheaders=next((r['values'] for r in rows if r['row']==header),[])
    for row in rows:
        loc=dict(workbook_sha256=sha,sheet_index=si,sheet_name=sn,row_number=row['row']);values=row['values'];present=[v for v in values if v is not None and str(v).strip()!=''];kind='UNPROJECTED_BUSINESS_ROW_REVIEW'
        if not present:kind='BLANK'
        elif header is not None and row['row']<header:kind='PREAMBLE'
        elif row['row']==header:kind='HEADER'
        elif header is not None:
            name=values[nameindex] if nameindex is not None and nameindex<len(values) else '';trading=values[tradeindex] if tradeindex is not None and tradeindex<len(values) else '';code=values[idindex] if idindex is not None and idindex<len(values) else ''
            if (name or code or ('fund' in keys and values[keys.index('fund')])) and [norm(x) for x in values]!=keys:
                kind='SOURCE_RECORD';count+=1
                fund=values[keys.index('fund')] if 'fund' in keys else '';subfund=values[keys.index('sub-fund')] if 'sub-fund' in keys else ''
                if role=='PRIIPS_FUND_SHARE_CLASS_PERFORMANCE_SCENARIO':name=subfund or fund
                candidate_name=str(name or '').strip();keyparts=[sheetrole,ident(candidate_name),ident(trading)]
                if code:keyparts+=[ident(code)]
                candidate=hashlib.sha256(dumps(keyparts).encode()).hexdigest() if candidate_name or code else ''
                fields=[dict(column=i+1,header=rawheaders[i] if i<len(rawheaders) else '',value=v,type=row['types'][i]) for i,v in enumerate(values)]
                record=dict(**loc,source_url=url,business_role=sheetrole,section_label=section,name=candidate_name,trading_name=str(trading or ''),source_identifier=str(code or ''),candidate_group_key=candidate,identity_status='TEXT_MATCH_CANDIDATE_NOT_VERIFIED_ENTITY',url_years_json=dumps(re.findall(r'20\d{2}',url)),sheet_years_json=dumps(re.findall(r'20\d{2}',sn)),fields_json=dumps(fields),source_values_json=dumps(values),source_types_json=dumps(row['types']),current_license_status='UNKNOWN')
                records.append(record)
                for i,k in enumerate(keys):
                    if ('data' in k or 'date' in k) and i<len(values) and values[i] not in [None,'']:
                        v=values[i];iso='';policy='UNPARSED_RAW_DATE_RETAINED'
                        try:
                            if row['types'][i]==3 and isinstance(v,(float,int)):
                                mode=int(manifest[sha].get('date_mode') or 0)
                                if mode==0 and 60<=v<61:raise ValueError('EXCEL_FICTITIOUS_DAY')
                                base=datetime.datetime(1904,1,1) if mode else datetime.datetime(1899,12,30 if v>=61 else 31)
                                iso=(base+datetime.timedelta(days=v)).isoformat();policy='EXCEL_DATE_TYPED_SERIAL_WITH_WORKBOOK_DATEMODE'
                            else:
                                s=str(v).strip()
                                for fmt in ['%d.%m.%Y','%d/%m/%Y','%Y-%m-%d %H:%M:%S','%Y-%m-%d']:
                                    try:iso=datetime.datetime.strptime(s,fmt).isoformat();policy='EXPLICIT_DATE_PATTERN';break
                                    except ValueError:pass
                        except Exception:pass
                        dates.append(dict(**loc,column=i+1,header=rawheaders[i],raw_json=dumps(v),raw_type=row['types'][i],iso_projection=iso,policy=policy))
            else:
                kind='SECTION_OR_NOTE'
                if len(present)==1:section=str(present[0])
        annotations.append(dict(**loc,classification=kind,business_role=sheetrole,header_row=header or '',raw_row_available_in='workbook_rows'))
    schemas.append(dict(workbook_sha256=sha,sheet_index=si,sheet_name=sn,business_role=sheetrole,header_row=header or '',headers_json=dumps(rawheaders),projection_rows=count,total_rows=len(rows),name_column=(nameindex+1) if nameindex is not None else '',identifier_column=(idindex+1) if idindex is not None else '',evidence='EXACT_HEADER_TOKEN_REVIEW_UNPROJECTED_ROWS_RETAINED',blank_or_unstructured_scope='UNKNOWN' if header is None else 'HEADER_OBSERVED'))
groups=collections.defaultdict(list);duplicates=collections.defaultdict(list)
for r in records:
    if r['candidate_group_key']:groups[r['candidate_group_key']].append(r)
    digest=hashlib.sha256(dumps([r['source_values_json'],r['source_types_json']]).encode()).hexdigest();duplicates[digest].append(r)
group_rows=[dict(candidate_group_key=k,business_role=v[0]['business_role'],name=v[0]['name'],source_identifier=v[0]['source_identifier'],observations=len(v),workbooks=len({r['workbook_sha256'] for r in v}),sheets=len({(r['workbook_sha256'],r['sheet_index']) for r in v}),url_years_json=dumps(sorted({year for r in v for year in json.loads(r['url_years_json'])})),locations_json=dumps([{k:r[k] for k in ['workbook_sha256','sheet_index','row_number']} for r in v]),identity_status='CANDIDATE_GROUP_NO_LEGAL_ENTITY_MERGE') for k,v in groups.items()]
duplicate_rows=[dict(raw_row_signature=k,observations=len(v),locations_json=dumps([{k:r[k] for k in ['workbook_sha256','sheet_index','row_number','business_role']} for r in v]),decision='PRESERVE_ALL_EXACT_VALUE_AND_TYPE_REPEATS') for k,v in duplicates.items() if len(v)>1]
tables={'registry_workbook_scope_review':workbooks,'registry_sheet_schema_review':schemas,'registry_row_semantic_classification':annotations,'registry_source_business_records':records,'registry_candidate_identity_groups':group_rows,'registry_exact_record_repetitions':duplicate_rows,'registry_date_projections':dates}
for name,items in tables.items():
    keys=list(dict.fromkeys(k for r in items for k in r))
    with (T/(name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(items)
    if keys:
        con.execute('CREATE TABLE "'+name+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')');con.executemany('INSERT INTO "'+name+'" VALUES ('+','.join('?' for k in keys)+')',[[r.get(k,'') for k in keys] for r in items])
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';assert len(annotations)==con.execute('SELECT count(*) FROM workbook_rows').fetchone()[0];con.close();source.close()
summary=dict(source_rows_preserved=len(annotations),reviewed_workbooks=len(workbooks),reviewed_sheets=len(schemas),business_records=len(records),candidate_groups=len(group_rows),repeated_candidate_groups=sum(r['observations']>1 for r in group_rows),exact_repeat_groups=len(duplicate_rows),date_fields=len(dates),parsed_dates=sum(bool(r['iso_projection']) for r in dates),row_classification_counts=dict(collections.Counter(r['classification'] for r in annotations)),record_role_counts=dict(collections.Counter(r['business_role'] for r in records)),workbook_role_counts=dict(collections.Counter(r['reviewed_role'] for r in workbooks)),global_complete=False,verified_unique_legal_entities='UNKNOWN')
(O/'build_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))
