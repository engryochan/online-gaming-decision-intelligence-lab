from pathlib import Path
import csv,json,sqlite3,io,zipfile,hashlib,openpyxl
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/33_global_workbook_content_b08_20261008'
con=sqlite3.connect(T/'global_workbook_content_b08.sqlite');manifest={r['workbook_sha256']:r for r in csv.DictReader((T/'registry_workbook_manifest.csv').open(encoding='utf-8-sig'))};repairs=[]
with (T/'registry_workbook_rows.csv').open('a',encoding='utf-8',newline='') as f:
    fields=['workbook_sha256','sheet_index','sheet_name','row_number','values_json','types_json','formats_json','extras_json'];writer=csv.DictWriter(f,fieldnames=fields)
    for r in csv.DictReader((T/'registry_worksheet_dimensions.csv').open(encoding='utf-8-sig')):
        count=con.execute('SELECT count(*) FROM workbook_rows WHERE workbook_sha256=? AND sheet_index=?',(r['workbook_sha256'],int(r['sheet_index']))).fetchone()[0]
        if count==int(r['rows']):continue
        assert count==0 and r['rows']=='1' and r['columns']=='1'
        location=manifest[r['workbook_sha256']]['object_path'].split('::');data=(R/location[0]).read_bytes()
        for member in location[1:]:
            with zipfile.ZipFile(io.BytesIO(data)) as z:data=z.read(member)
        assert hashlib.sha256(data).hexdigest()==r['workbook_sha256']
        book=openpyxl.load_workbook(io.BytesIO(data),read_only=False);sheet=book.worksheets[int(r['sheet_index'])-1];assert list(sheet.iter_rows())==[];book.close()
        row=dict(workbook_sha256=r['workbook_sha256'],sheet_index=int(r['sheet_index']),sheet_name=r['sheet_name'],row_number=1,values_json='[null]',types_json='["n"]',formats_json='["General"]',extras_json='{"reader_note":"IMPLICIT_EMPTY_WORKSHEET_RECTANGLE"}')
        writer.writerow(row);con.execute('INSERT INTO workbook_rows VALUES (?,?,?,?,?,?,?,?)',[row[k] for k in fields]);repairs.append(row)
con.commit();con.close()
summary=json.loads((O/'extraction_acceptance.json').read_text());summary['rows']+=len(repairs);summary['cells']+=len(repairs);summary['implicit_empty_sheet_rows']=len(repairs)
(O/'extraction_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');(O/'empty_sheet_reconciliation.json').write_text(json.dumps(repairs,indent=2)+'\n',encoding='utf-8');print('implicit empty rows',len(repairs))
