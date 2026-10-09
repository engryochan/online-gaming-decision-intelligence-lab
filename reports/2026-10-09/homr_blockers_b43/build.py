from pathlib import Path
import csv, json, hashlib, subprocess, datetime, math, sqlite3, collections

O = Path(__file__).resolve().parent
R = O.parents[2]
T = R / 'Reference/tables/67_homr_blockers_b43_20261009'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return list(csv.DictReader(p.open(encoding='utf-8-sig')))

def write(name, rows):
    assert rows
    with (T / name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def period(a):
    d = a.get('date', {})
    try:
        b = datetime.date.fromisoformat(d.get('beginDate', '')[:10])
    except (ValueError, TypeError):
        return 'BEGIN_UNKNOWN_OR_UNPARSEABLE'
    e = d.get('endDate', '')
    try:
        e = datetime.date.max if e == 'Present' else datetime.date.fromisoformat(e[:10])
    except (ValueError, TypeError):
        return 'END_UNKNOWN_OR_UNPARSEABLE'
    if b > e:
        return 'REVERSED_INTERVAL'
    return 'FULL_2024' if b <= datetime.date(2024, 1, 1) and e >= datetime.date(2024, 12, 31) else 'NOT_FULL_2024'

def distance(a, b, c, d):
    a, b, c, d = map(math.radians, (a, b, c, d))
    v = math.sin((c-a)/2)**2 + math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2
    return 6371.0088*2*math.asin(min(1, math.sqrt(max(0, v))))

assert not (O / 'baseline.json').exists(), 'Never refresh an existing baseline'
T.mkdir()
tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=R).decode().split('\0')
protected = {p: sha(R/p) for p in tracked if p and Path(p).suffix in ('.md', '.qmd') and (R/p).is_file()}
baseline = dict(head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip(),
                starting_status=subprocess.check_output(['git', 'status', '--porcelain'], cwd=R).decode(), protected=protected)
(O/'baseline.json').write_text(json.dumps(baseline, indent=2)+'\n', encoding='utf-8')
prior = read(R/'Reference/tables/66_homr_alternate_b42_20261009/registry_latest_40_station_adjudication.csv')
pending = {r['gsod_station_id'] for r in prior if 'LOCATION_CORROBORATED' not in r['current_state']}
assert len(prior) == 40 and len(pending) == 25
old = {r['USAF']+r['WBAN']: r for r in read(R/'Reference/tables/54_weather_station_b29_20261009/registry_station_history.csv')}
official = {r['GHCN_ID']: r for r in read(R/'Reference/tables/63_station_mapping_b39_20261009/registry_full_ghcnh_station_list.csv')}
receipts, candidates, query_states = [], [], []
for batch, directory in [('B41', '65_homr_remaining_b41_20261009'), ('B42', '66_homr_alternate_b42_20261009')]:
    for q in read(R/'Reference/tables'/directory/'registry_homr_fetch_receipts.csv'):
        station = q['gsod_station_id']
        if station not in pending:
            continue
        assert q['file'] and sha(R/q['file']) == q['sha256'], 'Source evidence mismatch'
        receipts.append(dict(batch=batch, gsod_station_id=station, source_file=q['file'], sha256=q['sha256'],
                             source_url=q['url'], fetched_utc=q['fetched_utc'], verified_this_batch='LOCAL_BYTES_ONLY_NOT_REFETCHED'))
        ss = json.loads((R/q['file']).read_bytes())['stationCollection'].get('stations', [])
        query_states.append(dict(batch=batch, gsod_station_id=station, returned_records=len(ss),
                                 empty_result=not ss, ghcnh_records=sum(any(i.get('idType')=='GHCNH' for i in s.get('identifiers', [])) for s in ss)))
        h = old[station]
        for n, s in enumerate(ss, 1):
            ids = s.get('identifiers', [])
            icaos = [i for i in ids if i.get('idType') == 'ICAO' and i.get('id') == h['ICAO']]
            for g in [i for i in ids if i.get('idType') == 'GHCNH']:
                blockers = []
                gp = period(g)
                if gp != 'FULL_2024': blockers.append('GHCNH_'+gp)
                if not icaos: blockers.append('EXACT_ICAO_ABSENT_IN_RETURNED_RECORD')
                elif not any(period(i) == 'FULL_2024' for i in icaos):
                    blockers.extend('ICAO_'+p for p in sorted({period(i) for i in icaos}))
                deltas = []
                for loc in s.get('location', {}).get('latLonPairs', []):
                    if period(loc) == 'FULL_2024':
                        try:
                            v = distance(float(h['LAT']), float(h['LON']), float(loc['latitude_dec']), float(loc['longitude_dec']))
                            if math.isfinite(v): deltas.append(v)
                        except (ValueError, KeyError):
                            pass
                if not deltas: blockers.append('NO_PARSEABLE_FULL_2024_COORDINATE_PAIR')
                elif max(deltas) > 1: blockers.append('LOCATION_EXCEEDS_1KM_ENGINEERING_PARAMETER')
                gid = g.get('id', '')
                if gid not in official: blockers.append('GHCNH_ABSENT_FROM_B39_STATION_LIST')
                # Keep namespace/time blockers separate; do not join identifiers across records.
                candidates.append(dict(batch=batch, gsod_station_id=station, source_station_row=n,
                    ncdc_station_id=s.get('ncdcStnId', ''), ghcnh_identifier=gid, old_icao=h['ICAO'],
                    exact_icao_count=len(icaos), ghcnh_period=gp, matching_icao_periods_json=json.dumps([period(i) for i in icaos]),
                    active_distance_km_json=json.dumps(deltas), blocker_codes_json=json.dumps(sorted(set(blockers))),
                    raw_identifiers_json=json.dumps(ids), source_file=q['file'], source_sha256=q['sha256'],
                    evidence_retrieval='PRIOR_BATCH_NOT_REFETCHED'))
latest = []
for r in prior:
    station = r['gsod_station_id']
    cs = [c for c in candidates if c['gsod_station_id'] == station]
    qs = [q for q in query_states if q['gsod_station_id'] == station]
    codes = sorted({b for c in cs for b in json.loads(c['blocker_codes_json'])})
    if station in pending:
        if not cs:
            codes = ['BOTH_QUERY_RESULTS_EMPTY_NOT_ABSENCE_PROOF'] if all(q['empty_result'] for q in qs) else ['NO_GHCNH_IDENTIFIER_IN_EITHER_QUERY_RESULT']
        assert codes, 'Unexpected zero-blocker pending candidate requires independent review'
    latest.append(dict(gsod_station_id=station, previous_b42_state=r['current_state'],
        current_state='PENDING_EXPLICIT_BLOCKERS' if station in pending else 'CARRIED_PRIOR_2024_ASSOCIATION_LOCATION_CORROBORATED',
        ghcnh_identifier=r['ghcnh_identifier'], candidate_evidence_rows=len(cs), blocker_codes_json=json.dumps(codes),
        queries_reviewed=len(qs), physical_continuity='NOT_ESTABLISHED', weather_values_approved=False,
        global_complete=False))
assert len(receipts) == 50 and len(latest) == 40
write('registry_verified_source_lineage.csv', receipts)
write('registry_query_outcomes.csv', query_states)
write('registry_candidate_blocker_details.csv', candidates)
write('registry_latest_40_station_adjudication.csv', latest)
con = sqlite3.connect(T/'homr_blockers_b43.sqlite')
counts = {}
for p in T.glob('*.csv'):
    rows = read(p); keys = list(rows[0])
    con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')')
    con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in keys)+')', [[r[k] for k in keys] for r in rows])
    counts[p.stem] = len(rows)
con.commit()
assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
for k,v in counts.items(): assert con.execute('SELECT COUNT(*) FROM "'+k+'"').fetchone()[0] == v
con.close()
assert all(sha(R/p) == h for p,h in protected.items())
stats = dict(stations=40, prior_corroborated_retained=15, unresolved=25, prior_source_queries_verified=len(receipts),
             candidate_evidence_rows=len(candidates), candidate_blocker_counts=dict(collections.Counter(b for c in candidates for b in json.loads(c['blocker_codes_json']))),
             sqlite_counts=counts, prior_documents_preserved=True, external_sources_refetched=False, global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats, indent=2)+'\n', encoding='utf-8')
report = '''---
title: "B43：未結站史的明確阻塞原因與提交失敗中止機制"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 核查範圍與證據

本輪合併審閱25項未結測站的B41 ICAO與B42 WBAN／精確站名查詢證據，共50份原始JSON逐份重新核對SHA256。使用既有官方來源證據，沒有重新下載，亦不宣稱外部資料已更新。既有15項共時／位置佐證保留，所有40站仍在最新判定表。

## 明確區分待核原因

逐個來源站史與GHCNH識別碼分開記錄：缺少完全相符ICAO、日期Unknown或不能涵蓋2024全年、沒有可解析全年有效坐標、位置超出1公里工程參數、或官方站表缺項。同一候選可以具有多項阻塞，計數不能相加當作測站數；不同查詢與平台的識別碼不拼接成一項已核實配對。

這也保留B41的BGTL位置差異證據，避免B42站名查詢沒有GHCNH時將原有位置待核原因掩蓋。BALTASOUND的站名查詢雖回傳全年GHCNH與相符坐標，該記錄沒有相符ICAO，因此不誤標為單純日期不符。KNXP的Unknown日期保持Unknown。

## 交付與驗收

'''+ '統計：`'+json.dumps(stats)+'`。\n\n'+'''
[候選明細](tables/67_homr_blockers_b43_20261009/registry_candidate_blocker_details.csv)、[50份來源譜系](tables/67_homr_blockers_b43_20261009/registry_verified_source_lineage.csv)、[查詢結果](tables/67_homr_blockers_b43_20261009/registry_query_outcomes.csv)、[最新40站判定](tables/67_homr_blockers_b43_20261009/registry_latest_40_station_adjudication.csv)、[SQLite](tables/67_homr_blockers_b43_20261009/homr_blockers_b43.sqlite)。來源API規則參見[官方HOMR文件](https://www.ncei.noaa.gov/access/homr/api)；本輪分類是本地證據分析。

新提交工具以每個子程序的非零退出碼立即中止，驗收未通過不得提交或推送；使用注入驗收失敗測試確認後續命令不執行。B42的失敗回執與原基線保留，不改寫過往驗收結果。本輪基線記錄開始時Inteligent文件已有的工作區修改，該文件不列入本輪提交。

下一步續查新版量測缺值規則，以及日期Unknown、識別碼不符與位置差異的正式證據。125筆舊風速衝突及全球金融、工商、歷史政治實體清單保持開放，不宣稱全球收齊。所有既有報告保留，Untitled不恢復。
'''
(R/'Reference/HOMR_Blockers_B43_20261009.qmd').write_text(report, encoding='utf-8')
notes = {
 'redteam':'同名、跨平台、跨記錄識別碼拼接及Unknown日期補造均可能產生假配對。',
 'critic':'B42粗分類不能當作日期不符證明；本輪保留原結果並附加逐候選原因。',
 'killcritic':'50份來源原始字節已核對；沒有外部重新下載，原有結論可追溯而非假稱最新。',
 'blindspot':'B42名字查詢可能掩蓋B41位置待核證據；必須同時保留兩類查詢結果。',
 'blueprint':'查詢收據、候選原因、40站判定分層；提交工具對每個命令退出碼強制中止。',
 'cheatsheet':'15項保留、25項未結；候選原因可多選，計數不等於獨立測站數。',
 'actionplan':'先驗證失敗即中止流程，再核新版缺值定義及Unknown／ICAO／位置缺口；其他全球待辦仍開放。'}
for n,v in notes.items():
    (R/n/'homr_blockers_b43_20261009.md').write_text('# '+n+' | B43\n\n'+v+'\n\n[報告](../Reference/HOMR_Blockers_B43_20261009.qmd)。\n', encoding='utf-8')
print(json.dumps(stats))
