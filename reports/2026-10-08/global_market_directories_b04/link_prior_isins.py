from pathlib import Path
import csv,json,hashlib,collections
O=Path(__file__).parent;R=O.parents[2];T=R/'Reference/tables/29_global_market_directories_b04_20261008'
with (T/'registry_jse_isin_structured_partial.csv').open(encoding='utf-8-sig') as f:jse=list(csv.DictReader(f))
lookup=collections.defaultdict(list);inputs=[]
for folder in sorted((R/'Reference/tables').iterdir()):
    if not any(folder.name.startswith(x) for x in ('19_','20_','21_','22_','23_','24_','25_','27_')):continue
    for path in sorted(folder.glob('registry_*.csv')):
        with path.open(encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f);fields=reader.fieldnames or []
            key=next((k for k in fields if k.lower()=='isin'),None)
            if not key:continue
            data=list(reader)
        inputs.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),rows=len(data),ISIN_column=key))
        for number,row in enumerate(data,1):
            isin=row[key].strip()
            if isin:lookup[isin].append(dict(prior_table=path.relative_to(R).as_posix(),prior_source_row=number,prior_row_json=json.dumps(row,ensure_ascii=False)))
links=[]
for row in jse:
    for prior in lookup.get(row['ISIN'],[]):
        links.append(dict(JSE_source_line=row['source_line'],ISIN=row['ISIN'],**prior,evidence='EXACT_ISIN_MATCH_NOT_COMPANY_OR_LISTING_STATUS_VERIFICATION'))
def write(name,rows,fields=None):
    fields=fields or list(dict.fromkeys(k for row in rows for k in row))
    with (T/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
write('prior_ISIN_input_manifest.csv',inputs)
write('registry_jse_prior_ISIN_matches.csv',links,['JSE_source_line','ISIN','prior_table','prior_source_row','prior_row_json','evidence'])
groups=collections.defaultdict(list)
for row in jse:groups[row['ISIN']].append(row)
dups=[dict(ISIN=k,source_rows=len(v),source_lines_json=json.dumps([r['source_line'] for r in v]),issuer_names_json=json.dumps(sorted({r['issuer_name'] for r in v})),decision='KEEP_ALL_SOURCE_RECORDS_PENDING_REVIEW') for k,v in groups.items() if len(v)>1]
write('registry_jse_duplicate_ISIN_review.csv',dups)
anna=list(csv.DictReader((T/'registry_anna_prefix_numbering_agency_source.csv').open(encoding='utf-8-sig')))
reviews=[dict(issue='LU_NO_EXACT_PREFIX',evidence_rows_json=json.dumps([r for r in anna if 'Luxembourg' in r.get('Jurisdiction','')],ensure_ascii=False),decision='JURISDICTION_REFERENCE_REVIEW_NO_AUTOMATIC_PREFIX_COUNTRY_REWRITE'),
dict(issue='BQ_NO_EXACT_PREFIX',evidence_rows_json=json.dumps([r for r in anna if r.get('ISIN Prefix')=='AN'],ensure_ascii=False),decision='FORMER_JURISDICTION_OR_SUBSTITUTE_REVIEW_NO_AUTOMATIC_SUCCESSOR_ASSIGNMENT'),
dict(issue='ANNA_DECLARED_120_MEMBERS_VS_TABLE_119_MEMBER_STATUS',evidence_rows_json=json.dumps({'declared_members':120,'observed_member_status_rows':sum(r.get('Membership Status')=='Member' for r in anna),'suspended_status_rows':sum(r.get('Membership Status')=='currently suspended' for r in anna)}),decision='PRESERVE_SOURCE_DISCREPANCY_AS_OF_DATE_AND_STATUS_REVIEW')]
write('registry_anna_semantic_review.csv',reviews)
summary=dict(prior_ISIN_tables=len(inputs),prior_ISIN_rows=sum(r['rows'] for r in inputs),exact_match_observations=len(links),matched_JSE_lines=len({r['JSE_source_line'] for r in links}),duplicate_ISIN_groups=len(dups),source_records_not_deleted=True)
(O/'isin_link_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))
