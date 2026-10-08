from pathlib import Path
import csv,json,sqlite3,hashlib,subprocess
O=Path(__file__).resolve().parent;R=O.parents[2];P=R/'Reference/tables/33_global_workbook_content_b08_20261008'
roles={r['workbook_sha256']:r for r in csv.DictReader((P/'registry_workbook_business_scope.csv').open(encoding='utf-8-sig'))}
con=sqlite3.connect('file:'+str(P/'global_workbook_content_b08.sqlite')+'?mode=ro',uri=True);items=[]
for r in csv.DictReader((P/'registry_worksheet_dimensions.csv').open(encoding='utf-8-sig')):
    rows=con.execute('SELECT row_number,values_json FROM workbook_rows WHERE workbook_sha256=? AND sheet_index=? ORDER BY row_number LIMIT 25',(r['workbook_sha256'],int(r['sheet_index']))).fetchall()
    values=[dict(row=n,values=json.loads(v)) for n,v in rows if any(x is not None and x!='' for x in json.loads(v))]
    items.append(dict(**r,role=roles[r['workbook_sha256']]['business_role'],url=roles[r['workbook_sha256']]['source_url'],sample=values[:10]))
con.close();(O/'input_review.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
baseline=dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),protected={})
for p in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']:
    baseline['protected'][p]=hashlib.sha256((R/p).read_bytes()).hexdigest()
(O/'baseline.json').write_text(json.dumps(baseline,indent=2)+'\n',encoding='utf-8')
for i in items:
    if i['role']!='SOURCE_WORKBOOK_BUSINESS_SCOPE_PENDING':print(json.dumps(dict(sha=i['workbook_sha256'][:12],sheet=i['sheet_name'],index=i['sheet_index'],role=i['role'],url=i['url'],sample=i['sample'][:4])))
print('pending URLs',json.dumps(sorted({i['url'] for i in items if i['role']=='SOURCE_WORKBOOK_BUSINESS_SCOPE_PENDING'})))
