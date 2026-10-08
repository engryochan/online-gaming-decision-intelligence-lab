from pathlib import Path
import argparse,sqlite3,json,gzip
DEFAULT=Path(__file__).resolve().parents[3]/'Reference/tables/36_historical_instrument_csv_b11_20261008/historical_instrument_csv_b11.sqlite'
def connect(path=DEFAULT):
    con=sqlite3.connect('file:'+str(Path(path).resolve())+'?mode=ro',uri=True)
    con.create_function('csv_block_json',1,lambda value:gzip.decompress(value).decode('utf-8'),deterministic=True)
    con.execute('CREATE TEMP VIEW csv_rows AS SELECT b.content_sha256,b.first_row+cast(j.key AS INTEGER) AS row_number,j.value AS cells_json FROM csv_blocks b,json_each(csv_block_json(b.payload_gzip)) j')
    return con
if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Read-only query of losslessly compressed CSV rows. No workbook or source mutation.')
    parser.add_argument('--database',default=str(DEFAULT));parser.add_argument('--url-contains',default='');parser.add_argument('--limit',type=int,default=10);args=parser.parse_args()
    assert 1<=args.limit<=10000
    con=connect(args.database)
    rows=con.execute("SELECT f.url,r.row_number,r.cells_json FROM file_manifest f JOIN csv_rows r ON r.content_sha256=json_extract(f.receipt_json,'$.content_sha256') WHERE instr(f.url,?)>0 ORDER BY f.url,r.row_number LIMIT ?",(args.url_contains,args.limit))
    for url,n,cells in rows:print(json.dumps(dict(source_url=url,row_number=n,cells=json.loads(cells)),ensure_ascii=True))
    con.close()
