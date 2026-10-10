#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""地緣產業研究：完全離線的 Prompt 與情境登記驗證。

只審核清單結構與審核狀態，不會連線、偵測網絡或存取任何正式系統。
範例：
  python geostrategy_scenario_audit.py
  python geostrategy_scenario_audit.py --self-test
  python geostrategy_scenario_audit.py --json report.json
  python geostrategy_scenario_audit.py --strict  # 若尚有關鍵測試未通過，以2結束
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCENARIO = HERE / 'Geostrategy_Scenario_Risk_Registry_20261009.csv'
PROMPTS = HERE / 'Geostrategy_Prompt_Traceability_20261009.csv'
COMPOUND = HERE / 'Geostrategy_Compound_Scenarios_20261009.csv'
STATES = {'NOT_RUN', 'PASS', 'FAIL', 'BLOCKED', 'NOT_APPLICABLE'}
PRIORITY = {'CRITICAL','HIGH','MEDIUM','LOW'}
GATES = {'G0','G1','G2','G3','G4','G5'}


def load_csv(path):
    with Path(path).open('r', encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        return list(reader), set(reader.fieldnames or [])


def validate(scenarios, prompts, compounds=None):
    """回傳結構錯誤及精確統計，沒有以紅字代替證據。"""
    errors = []
    s_ids = [row.get('scenario_id','') for row in scenarios]
    p_tags = [row.get('prompt_tag','') for row in prompts]
    dup_s = sorted(k for k,v in Counter(s_ids).items() if v > 1)
    dup_p = sorted(k for k,v in Counter(p_tags).items() if v > 1)
    if dup_s: errors.append(f'重複情境 ID: {dup_s}')
    if dup_p: errors.append(f'重複提示標籤: {dup_p}')
    s_set = set(s_ids)
    p_set = set(p_tags)
    mapped = set()
    scenario_prompt_tags = set()
    for row in scenarios:
        sid = row.get('scenario_id', '<missing>')
        status = row.get('test_status','')
        if status not in STATES: errors.append(f'{sid}: 非法測試狀態 {status}')
        if row.get('severity') not in PRIORITY: errors.append(f'{sid}: 非法優先級')
        if row.get('gate') not in GATES: errors.append(f'{sid}: 非法閘門')
        if status == 'PASS' and not all(row.get(key, '').strip() for key in ('evidence_ref','reviewer','reviewed_at')):
            errors.append(f'{sid}: 無證據／審核者／時間戳不得標 PASS')
        if status == 'NOT_APPLICABLE' and not row.get('evidence_ref', '').strip():
            errors.append(f'{sid}: N/A 必須有理由與紀錄')
        if not row.get('scenario') or not row.get('detection') or not row.get('mitigation'):
            errors.append(f'{sid}: 情境描述、偵測與緩解缺項')
        scenario_prompt_tags.update(x for x in row.get('mapped_prompt_tags','').split(';') if x)
    for row in prompts:
        tag = row.get('prompt_tag','')
        sid = row.get('mapped_scenario_id','')
        if not tag.endswith('/'): errors.append(f'標籤錯誤: {tag}')
        if sid not in s_set: errors.append(f'{tag}: 參照的情境 ID {sid} 不存在')
        else: mapped.add(tag)
        if row.get('coverage_claim') != 'MAPPED_TO_DESIGN':
            errors.append(f'{tag}: 不合法的覆蓋聲稱')
        if row.get('actual_test_status') == 'PASS':
            errors.append(f'{tag}: 不能單憑情境映射將整個提示方法標為 PASS')
    if scenario_prompt_tags != p_set:
        errors.append(f'情境與提示反向對應不一致: 遺漏 {sorted(p_set-scenario_prompt_tags)} / 額外 {sorted(scenario_prompt_tags-p_set)}')
    if len(prompts) != 85:
        errors.append(f'與來源提示清單不一致，應85種，現有 {len(prompts)} 種')
    if sum(int(x.get('requested_occurrences','0')) for x in prompts) != 88:
        errors.append('原始提示出現次數與來源88項不一致')
    counts = Counter(row.get('test_status') for row in scenarios)
    applicable = sum(row.get('test_status') != 'NOT_APPLICABLE' for row in scenarios)
    verified = counts['PASS']
    critical = [s for s in scenarios if s.get('severity') == 'CRITICAL']
    critical_open = [s['scenario_id'] for s in critical if s.get('test_status') != 'PASS']
    compound_errors = []
    compounds = [] if compounds is None else compounds
    for c in compounds:
        cid=c.get('compound_id','<missing>')
        if c.get('scenario_a') not in s_set or c.get('scenario_b') not in s_set:
            compound_errors.append(f'{cid}: 交互失效引用不存在的子情境')
        if c.get('test_status') not in STATES:
            compound_errors.append(f'{cid}: 測試狀態錯誤')
        if c.get('test_status')=='PASS' and not all(c.get(k,'').strip() for k in ('evidence_ref','reviewer','reviewed_at')):
            compound_errors.append(f'{cid}: 無證據不得標 PASS')
    compound_ids = [c.get('compound_id','') for c in compounds]
    if len(compound_ids)!=len(set(compound_ids)):
        compound_errors.append('雙重故障 ID 重複')
    errors.extend(compound_errors)
    report = {
        'compound_scenario_count': len(compounds),
        'compound_scenario_verified': sum(c.get('test_status')=='PASS' for c in compounds),
        'compound_critical_unverified_count': sum(c.get('severity')=='CRITICAL' and c.get('test_status')!='PASS' for c in compounds),
        'overall_registered_validation': round((verified+sum(c.get('test_status')=='PASS' for c in compounds)) / (applicable + sum(c.get('test_status')!='NOT_APPLICABLE' for c in compounds)),4) if (applicable + len(compounds)) else None,
        'scenario_count': len(scenarios),
        'domains': len(set(s.get('domain') for s in scenarios)),
        'prompt_count_unique': len(p_set),
        'prompt_count_original': sum(int(x.get('requested_occurrences','0')) for x in prompts),
        'prompt_traceability': round(len(mapped)/len(p_set),4) if p_set else None,
        'registered_scenario_validation': round(verified/applicable,4) if applicable else None,
        'test_status_counts': dict(sorted(counts.items())),
        'critical_count': len(critical),
        'critical_unverified_count': len(critical_open),
        'critical_unverified_ids': critical_open,
        'global_scenario_completeness': None,
        'structural_errors': errors,
        'certified_or_operational': False,
        'remark': '所有數字僅對本 CSV 中已登記情境有效；不證明未知世界情境之全面覆蓋。'
    }
    return report


def self_test():
    from copy import deepcopy
    scenarios, _ = load_csv(SCENARIO)
    prompts, _ = load_csv(PROMPTS)
    compounds,_=load_csv(COMPOUND)
    result = validate(scenarios,prompts,compounds)
    assert not result['structural_errors'], result['structural_errors']
    assert result['scenario_count']==48 and result['domains']==12 and result['compound_scenario_count']==12
    assert result['prompt_count_unique']==85 and result['prompt_count_original']==88
    assert result['registered_scenario_validation']==0
    assert result['prompt_traceability']==1.0
    assert result['critical_unverified_count']>0
    bad = deepcopy(scenarios)
    bad[0]['test_status']='PASS'  # 無證據不可認證
    assert any('不得標 PASS' in e for e in validate(bad,prompts)['structural_errors'])
    bad = deepcopy(scenarios)
    bad[0]['test_status']='NOT_APPLICABLE'  # 無理由不可刪分母
    assert any('N/A' in e for e in validate(bad,prompts)['structural_errors'])
    bad = deepcopy(scenarios)
    bad.append(dict(bad[0]))
    assert any('重複情境' in e for e in validate(bad,prompts)['structural_errors'])
    badp = deepcopy(prompts)
    badp[0]['mapped_scenario_id']='SC-999'
    assert any('不存在' in e for e in validate(scenarios,badp)['structural_errors'])
    badp = deepcopy(prompts)
    badp[0]['prompt_tag']='renamed/'
    assert validate(scenarios,badp)['structural_errors']
    badc=deepcopy(compounds)
    badc[0]['scenario_a']='SC-999'
    assert any('交互失效' in e for e in validate(scenarios,prompts,badc)['structural_errors'])
    print('SELF-TEST PASS: 11 checks (coverage, types, gating, reverse mapping, tampering, compound refs)')
    return result


def main():
    parser=argparse.ArgumentParser(description='完全離線的情境登記/Prompt覆蓋稽核')
    parser.add_argument('--self-test', action='store_true', help='執行本地合成負向測試')
    parser.add_argument('--strict', action='store_true', help='未通過高嚴重度測試則退出碼2')
    parser.add_argument('--json', type=Path, help='選用 JSON 輸出路徑')
    args=parser.parse_args()
    if args.self_test:
        report=self_test()
    else:
        a,_=load_csv(SCENARIO)
        b,_=load_csv(PROMPTS)
        c,_=load_csv(COMPOUND)
        report=validate(a,b,c)
    output=json.dumps(report,ensure_ascii=False,indent=2)
    print(output)
    if args.json:
        args.json.write_text(output+'\n',encoding='utf-8')
    if report['structural_errors']:
        return 1
    if args.strict and (report['critical_unverified_count'] or report['compound_critical_unverified_count']):
        return 2
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
