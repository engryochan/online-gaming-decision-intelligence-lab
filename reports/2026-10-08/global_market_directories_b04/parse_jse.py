from pathlib import Path
import csv,json,hashlib,zipfile,io,collections
from urllib.request import Request,urlopen
from urllib.error import HTTPError
O=Path(__file__).parent;R=O.parents[2];T=R/'Reference/tables/29_global_market_directories_b04_20261008';T.mkdir(parents=True,exist_ok=True)
raw=(R/'reports/2026-10-08/global_market_sources_b03/raw/JSE_ISIN_FULL.response').read_bytes()
archive=zipfile.ZipFile(io.BytesIO(raw));rows=[]
url='https://www.jse.co.za/sites/default/files/media/documents/2020-11/ISIN%20Equities%20Record%20Structure.pdf'
try:
    with urlopen(Request(url,headers={'User-Agent':'ResearchDirectoryInventory/1.0'}),timeout=20) as response:
        dictionary=response.read();status=response.status
except HTTPError as e:dictionary=e.read();status=e.code
except Exception as e:dictionary=b'';status=type(e).__name__
(O/'JSE_record_structure.response').write_bytes(dictionary)
def check_isin(value):
    if len(value)!=12 or not value[:2].isalpha() or not value[-1:].isdigit() or not value.isalnum():return False
    expanded=''.join(str(ord(c)-55) if c.isalpha() else c for c in value.upper())
    return sum((int(c)*2//10+int(c)*2%10) if i%2 else int(c) for i,c in enumerate(reversed(expanded)))%10==0
for name in archive.namelist():
    if name.endswith('/'):continue
    for number,line in enumerate(archive.read(name).splitlines(),1):
        text=line.decode('latin-1')
        rows.append(dict(source_member=name,source_line=number,ISIN=text[:12],issuer_name_raw=text[12:67],
            issuer_name=text[12:67].strip(),issue_description_raw=text[67:178],issue_description=text[67:178].strip(),
            unresolved_remainder_raw=text[178:],source_record_bytes=len(line),raw_record=text,record_sha256=hashlib.sha256(line).hexdigest(),
            ISIN_check_digit_valid=check_isin(text[:12]),source_layout_status='FIRST_178_BYTES_SPEC_LAYOUT_REMAINDER_UNRESOLVED',text_projection='LATIN1_REVERSIBLE_BYTE_MAPPING_ENCODING_UNCONFIRMED',
            company_classification='UNKNOWN_NOT_ALL_INSTRUMENTS_ARE_COMPANY_SHARES',active_listing_status='UNKNOWN'))
def write(name,values):
    fields=list(dict.fromkeys(k for row in values for k in row))
    with (T/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(values)
write('registry_jse_isin_structured_partial.csv',rows)
groups=collections.defaultdict(list)
for row in rows:groups[row['issuer_name']].append(row)
write('registry_jse_source_issuer_name_groups.csv',[dict(issuer_name=n,instrument_source_rows=len(v),unique_ISINs=len({r['ISIN'] for r in v}),
    classification='SOURCE_NAME_GROUP_NOT_VERIFIED_LEGAL_ENTITY_OR_LISTED_COMPANY',source_lines_json=json.dumps([r['source_line'] for r in v])) for n,v in sorted(groups.items())])
assert len(rows)==14782
assert all(len(r['raw_record'])==277 for r in rows)
assert all(r['issuer_name_raw']+r['issue_description_raw']+r['unresolved_remainder_raw']==r['raw_record'][12:] for r in rows)
summary=dict(source_records=len(rows),issuer_name_groups=len(groups),ISIN_check_digits_valid=sum(r['ISIN_check_digit_valid'] for r in rows),
            unique_ISINs=len({r['ISIN'] for r in rows}),record_length_bytes=277,published_dictionary_full_length_bytes=286,
            dictionary_url=url,dictionary_download_status=status,dictionary_response_sha256=hashlib.sha256(dictionary).hexdigest(),
            archive_sha256=hashlib.sha256(raw).hexdigest(),full_field_schema_verified=False,all_records_retained=True)
(O/'jse_parse_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary),flush=True)
