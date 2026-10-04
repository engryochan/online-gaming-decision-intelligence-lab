from pathlib import Path
import csv,json,re,collections,hashlib
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[1]
texts=json.loads((OUT/'extracted_text.json').read_text(encoding='utf-8'))
def load_csv(name,delim=','):
    with (OUT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=delim))
seeds=load_csv('catalogue_seed.tsv','\t'); checks=load_csv('live_checks.tsv','\t')
preferred=sorted(texts,key=lambda p:(p.startswith('.Rproj'),p.endswith('.html'),not p.startswith('Reference/'), 'v2_4' not in p, p))
ascii_fold=str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')
folded={p:t.translate(ascii_fold) for p,t in texts.items()}
registry=[]; missing=[]; evidence=[]
for s in seeds:
    al=s['aliases'].split('|'); matches=[]
    for p in preferred:
        t=texts[p]
        if not any(a.translate(ascii_fold) in folded[p] for a in al): continue
        positions=[]
        for a in al:
            low=a.translate(ascii_fold); pos=folded[p].find(low)
            while pos>=0:
                end=pos+len(a)
                word=lambda ch:ch.isascii() and (ch.isalnum() or ch=='_')
                left=not(a[0].isascii() and a[0].isalnum() and pos>0 and word(t[pos-1]))
                right=not(a[-1].isascii() and a[-1].isalnum() and end<len(t) and word(t[end]))
                if left and right:positions.append((pos,end));break
                pos=folded[p].find(low,pos+1)
        if positions:
            pos,end=min(positions)
            line=t.count('\n',0,pos)+1
            context=t[t.rfind('\n',0,pos)+1:t.find('\n',end) if t.find('\n',end)>=0 else len(t)].strip()
            matches.append((p,line,context))
    if not matches:missing.append(s);continue
    live=next((x for x in sorted(checks,key=lambda x:len(x['key']),reverse=True) if x['key'].casefold() in s['name'].casefold()),None)
    p,line,context=matches[0]
    row=dict(id=f'E{len(registry)+1:04d}',category=s['category'],name=s['name'],role=s['role'],status=live['status'] if live else 'U',verification_url=live['url'] if live else '',verified_scope=live['verified_scope'] if live else '仅核实项目出现；本轮未独立复核现况、归属、效果与价格',source_file=p,source_line=line,source_context=context[:600],matching_files=len(matches))
    registry.append(row)
    for ep,ei,ec in matches:
        if not ep.startswith('.Rproj'):evidence.append(dict(id=row['id'],name=row['name'],path=ep,line=ei,context=ec[:600]))
main=next(p for p in texts if p.startswith('Reference/') and 'v2_4_' in p and p.endswith('.md'))
raw=[]; group=''
for i,line in enumerate(texts[main].splitlines(),1):
    if line.startswith('### '): group=line.lstrip('# ').strip()
    if 500<=i<=819 and re.match(r'^\|\s*\d+\s+[★◎○△]',line):
        c=line.split('|'); raw.append(dict(number=re.search(r'\d+',c[1]).group(),category=group,label=c[2].strip(),original_claim=c[3].strip(),boundary=' | '.join(c[4:-1]).strip(),path=main,line=i,status='PROJECT_QUOTE_NOT_REVERIFIED'))
assert len(raw)==172 and sorted(int(x['number']) for x in raw)==list(range(1,173)),len(raw)
industry=next(p for p in texts if p.startswith('Reference/') and p.startswith('Reference/顶级在线百家乐平台_'))
industry_rows=[]
for i,line in enumerate(texts[industry].splitlines(),1):
    if line.startswith('## §3'):break
    if re.match(r'^\|\s*\d+\s*\|',line):
        c=line.split('|'); num=int(c[1].strip())
        if len(industry_rows)>=70:break
        label=c[2].strip(); name=re.sub(r'\*+','',label)
        industry_rows.append(dict(number=num,name=name,original_description=' | '.join(c[3:-1]),path=industry,line=i,status='U'))
assert len(industry_rows)==70
def write_csv(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
write_csv('strategy_services_registry.csv',registry);write_csv('entity_source_evidence.csv',evidence);write_csv('original_172_entries.csv',raw);write_csv('gaming_70_entries.csv',industry_rows)
(OUT/'unmatched_seed.json').write_text(json.dumps(missing,ensure_ascii=False,indent=2),encoding='utf-8')
groups=collections.defaultdict(list)
for x in registry:groups[x['category']].append(x)
inventory=load_csv('file_inventory.csv')
main_files=[x for x in inventory if not x['path'].startswith('.Rproj')]
cache_files=[x for x in inventory if x['path'].startswith('.Rproj')]
counts=collections.Counter(x['status'] for x in registry)
summary=dict(inventory_files=len(inventory),project_files=len(main_files),editor_cache_files=len(cache_files),catalogue_records=len(registry),categories=len(groups),status=dict(counts),raw_directory_entries=len(raw),gaming_entries=len(industry_rows),unmatched_seeds=[x['name'] for x in missing])
(OUT/'audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
def link(p,n):return f'[来源](<{ROOT.as_posix()}/{p}:{n}>)'
report=['# 现实策略服务公司与平台：全项目审阅及分类名录','', '审阅日期：2026-10-04（Asia/Tbilisi）。范围：此工作区当前文件快照，不是全球所有公司全集。','',
f'纳入文件 {len(inventory)} 个：项目及渲染依赖 {len(main_files)} 个，RStudio 隐藏缓存 {len(cache_files)} 个；不把 Git 对象、Git 历史或本轮产物算作项目正文。每个文件的字节、SHA-256、提取方法见 file_inventory.csv。', '',
'本轮完成全文件清点、可读文件全文程序扫描、表格与名称提取、重复核对、三个原有 Python 文件静态语法检查，以及关键策略段落的语义审阅和部分官网复核。**这不等于所有句子均逐句完成事实核验，也不等于代码、QMD、网页和模型已经实跑验证。** HTML 提取可见文字，未执行脚本；PDF 提取七页文字，未逐页验版。一个零字节 RStudio lock_file 因占用／权限未能读取；字体、二进制缓存仅清点与指纹登记。', '',
'目录中 V 表示本轮取得官网正文／官方文档，能支持所列定位；P 表示部分核实、重定向、访问受限或仅核到一项交易；U 表示仅核实项目出现，当前状态仍待核。**V 不证明产品最佳、预测有效、采购可行或效果独立验证。** 原文 ◎ 不自动继承为本轮 V。','',
f'主目录为 {len(registry)} 条公司／产品族／研究资源记录，分 {len(groups)} 类。公司与产品族合并，跨集团产品、公共机构、标准与研究对象另注明，**不能称为 {len(registry)} 家独立公司**。另附原名录全部 172 编号及行业原表 70 条，二者与主目录有交集，不能相加。','',
'## 已确认的校对与审阅问题','',
'| 项目 | 发现与处理意见 |', '|---|---|',
'| 根目录生成器 | create_ogdil.py 第 107 行起的三引号未闭合，静态解析失败；第 128 行即截断。此次登记问题，未执行可能写入文件的生成器。 |',
'| 重复稿 | Report-Optimized-V2.md 与 Taige-Real-World-Report-V2-Enhanced.md SHA-256 相同；不能作两个独立来源。Aerospace_Ecosystem_Report.md 与 .qmd 也逐字节相同。 |',
'| 172 条口径 | 编号 1–172 连续，既含重复机构又含一个条目多机构及标准、科学发现，不能作为公司唯一数。 |',
'| CSV 台账实物 | .gitignore 忽略 *.csv，初始 rg 文件列表不能证明 CSV 缺失。完整清点确认国家／地区旧表、新表均 249 行，行政单位 5,046 行，游戏 37 行，ODS 表清单 129 行、字段 2,291 行；主键与表间核验见 csv_audit.json。 |',
'| CSV 内部一致性 | 六表所检主键无重复；旧、新国家键相同；行政表国家外键与声明数量一致；ODS 字段与表清单对应、序号连续。游戏旗标为 True 3 条、False 34 条，旗标不证明安装包现存。249 行 space_ecosystem_status 全为 TO_RESOLVE，尚非逐地区宇航实体清单。 |',
'| 空治理文档 | 03_ODS_DATA_DICTIONARY_GOVERNANCE.md、04_ODS_SCHEMA_VERSIONING.md 等当前为零字节。存在生成脚本不代表规范已经写入。完整空文件清单见 csv_audit.json。 |',
'| 版本口径 | 根 README 同时出现 Foundation v2.0.1、徽章 v0.1.0、页尾 v0.1.0；V2.0.1/README.md 写 Foundation v2.0.0。 |',
'| PEMANDU 与地理术语斧正 | 已按用户定义撤去地球内部的排他地理标签，撤去唯一可及及整套照搬断言；统一记录服务定位、具体地点及待核采购条件。第 907 行价格断言仍待正式报价核验。 |',
'| 行数定义 | ChatGPT 篇本轮逻辑行数为 924，文件中宣称 923。LF 计数与最后一个无换行行的逻辑计数须区分，不能直接认定差一行就是内容遗失。 |',
'| 绝对市场结论 | “现实无一家”“售结论者皆妄”等改为“本项目本轮核验范围未发现满足指定标准者”；商业咨询本就提供建议与结论，应评估证据、假设与责任。 |',
'| Sift 同名与归属 | 风控 Sift 与遥测 Sift Stack 不同。航天报告将后者写成 SpaceX 自研不正确；其官网说明创办人是前 SpaceX 工程师。 |',
'| 续核品牌边界 | Leadership Connect 已从 Altrata 合并条目拆出，以独立官网核验，不能据 Altrata 官网认定它属于同一集团。Talogy 已核服务定位，Caliper 仍待核，因此合并条目标 P。 |',
'| Plum 现况 | 原网址现跳转 Phenom 的 2026-04-28 收购说明；更新为人才行为测评及官方收购声明，不继承其准确率营销数字。 |',
'| GeoQuant | 原产品 URL 当前跳转 Geo Risk Signals；旧名称及历史规格不能直接宣称现行，完整变更仍待核。 |',
'| 缺证性能与采用断言 | 航天报告“不可能用 StarRocks”“国际航天白名单”“ECharts 上万通道会卡死”等缺可复现实验、任务边界或明确清单来源，降为待核观点。 |',
'| 历史与现售 | Senturion、RAND RSAS、IBM Watson Personality Insights、Cambridge Analytica 与现售产品分开；现有论文不证明今天可采购。 |',
'| 人物测评 | DISC、Big Five、问卷、文本估计、面部识别不是同一能力；原文“一类强效度”不构成每个产品独立效度验证。岗位测评不等于治理能力或私人忠诚评分。 |',
'| 合并与交割 | 官网可支持 SpaceX 收购 xAI，以及 NVIDIA 宣布收购 Hugging Face。并购公告、签约、交割与集团业务结构要分字段记录；本轮不确认全部估值、持股与上市数字。 |',
'| 引用与网页 | 原文带 utm_source=chatgpt.com 的链接仍可能指向一手来源；参数不是证据真伪的判据。应读目标文档、记录日期与论断对应关系。 |',
'| 校对字词 | “核验标志 v2”与“核验标记法”对 ◎ 的描述不一致；v2.4 #161 的“设计ations”有明显混写；繁简贡献稿中的“開髮”应按语义校正。 |', '',
'以下定位摘自项目并作分类校正；凡 U 不把描述当成今天已确认的业务事实。通用云、BI、数据库、集团、榜单与公共数据可支持策略研究，不能全部称为“策略咨询公司”。', '']
for cat,rows in groups.items():
    report+=['## '+cat,'','| 编号 | 公司／平台／产品族 | 项目定位与边界 | 本轮状态 | 来源与核验入口 |','|---|---|---|---|---|']
    for x in rows:
        web=f"；[官方核验入口]({x['verification_url']})" if x['verification_url'] else ''
        report.append(f"| {x['id']} | {x['name']} | {x['role']} | {x['status']} | {link(x['source_file'],x['source_line'])}{web} |")
    report.append('')
report+=['## 在线游戏平台、风控与自动化：行业补充 70 条','',
'这是项目行业资料原表逐项列出，**本轮均为 U，未验证各平台当前牌照、地域开放、并购归属、模型效果或预测真实性**。集团、品牌与产品并列保留，原表“70 家”不继承为独立公司数。Oracle Baccarat Predictor、BACC.BOT、BaccaratAI 等名称只证明原文提及，不证明能预测牌局或可合法购买。','','| 原序 | 名称 | 本轮状态 | 项目来源 |','|---|---|---|---|']
for x in industry_rows:report.append(f"| {x['number']} | {x['name']} | U | {link(x['path'],x['line'])} |")
report+=['','## 原 172 编号条目的完整对账','',
'以下为原名录标题层的完整保留，不是重新认证其原文数字与主张。详细原断言和边界在 original_172_entries.csv；标准、数据集、科研对象与机构仍应分开管理。','','| 原序 | 原条目标题 | 项目来源 |','|---|---|---|']
for x in raw:
    label=re.sub(r'\[([^\]]+)\]\([^\)]+\)',r'\1',x['label']).replace('**','')
    report.append(f"| {x['number']} | {label} | {link(x['path'],x['line'])} |")
report+=['','## 文件审阅覆盖与可复查证据','',
'- file_inventory.csv：所有纳入文件、字节、SHA-256、提取行数与审阅方式。',
'- strategy_services_registry.csv：分类名录、V/P/U、官网核验范围与来源上下文。',
'- entity_source_evidence.csv：每条名录在每个非缓存来源文件中的首个匹配位置；用于定位，不是自动认定所有同名词均为同一实体。',
'- original_172_entries.csv 与 gaming_70_entries.csv：原目录逐行对账，未经复核的原主张明确标记。',
'- duplicate_files.json：字节重复组；重复正文、HTML、缓存不算独立互证。',
'- csv_audit.json：六份原始 CSV 的记录数、重复键、表间对应、行政单位计数与空文件检查。',
'- live_checks.tsv：本轮实际复核入口与支持范围；未对每个实体逐家联网认证。','',
'本轮已获用户授权直接斧正地理用词及 PEMANDU 相关断言；修改前文件与前后指纹另行保留，历史未修改验证记录只适用于之前轮次。未提交、推送或运行原项目生成器。覆盖声明限于当前工作区提取与已审阅证据，不宣称全球穷尽、全部句子正确或模型部署验收通过。','']
(OUT/'现实策略服务_审阅与分类名录_20261004.md').write_text('\n'.join(report),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=True,indent=2))
