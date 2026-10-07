"""Small snapshot benchmark: in-memory copies, three secondary indexes only."""
from pathlib import Path
import sqlite3,time,statistics,hashlib,json,sys,platform
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent
queries={'country_coverage':'SELECT * FROM v_country_evidence_coverage ORDER BY iso_alpha2','missing_sources':"SELECT claim_id,entity_id,evidence_state,verification_scope FROM v_claims_with_source WHERE source_id=''",'metrics_with_context':'SELECT * FROM v_metrics_with_context','neuro_missing_bandwidth':'SELECT * FROM v_neuro_bandwidth_missing'}
source=sqlite3.connect((OUT/'global_registry_b04_query.sqlite').as_uri()+'?mode=ro',uri=True)
results=[];expected={}
for indexed in (True,False):
    db=sqlite3.connect(':memory:');source.backup(db)
    if not indexed:
        for name in ('claims_entity','candidate_country','relations_country'):db.execute('DROP INDEX '+name)
    for name,sql in queries.items():
        rows=db.execute(sql).fetchall();digest=hashlib.sha256(repr(rows).encode()).hexdigest()
        if indexed:expected[name]=digest
        else:assert digest==expected[name],'Different answers'
        times=[]
        for _ in range(30):
            start=time.perf_counter_ns();db.execute(sql).fetchall();times.append((time.perf_counter_ns()-start)/1e6)
        plan=[r[3] for r in db.execute('EXPLAIN QUERY PLAN '+sql)]
        results.append(dict(query=name,secondary_indexes_enabled=indexed,result_rows=len(rows),result_sha256=digest,p50_ms=statistics.median(times),p95_ms=sorted(times)[28],rounds=30,plan=plan))
    db.close()
source.close()
receipt=dict(scope='1514_SOURCE_ROWS_SINGLE_CONNECTION_WARM_IN_MEMORY_COPY',comparison='three secondary indexes present versus removed; primary indexes retained',sqlite_version=sqlite3.sqlite_version,python_version=platform.python_version(),os=platform.system(),limits='not disk-cold, concurrent, distributed, production or worldwide performance evidence',source_database_modified=False,results=results)
(OUT/'query_benchmark.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{k:r[k] for k in ('query','secondary_indexes_enabled','p50_ms','p95_ms')} for r in results],ensure_ascii=False,indent=2))
