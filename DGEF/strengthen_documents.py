"""Read-only corpus audit, then prefix-preserving additions to two documents."""
from pathlib import Path
import ast,csv,hashlib,io,json,sqlite3,zipfile
csv.field_size_limit(64*1024*1024)
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'reports/2026-10-04/document_strengthening'
TARGETS=[ROOT/'Reference/真实版人物分析与治国策略服务_名录与九十日行令_v2_4_全球行政通信宇航生命证据增强版_20261004.md',ROOT/'_大秦赋算筹_v1_3_9.qmd']
TEXT={'.md','.qmd','.txt','.html','.css','.js','.py','.sql','.json','.tsv','.csv','.toml','.yml','.yaml'}
def sha(b):return hashlib.sha256(b).hexdigest()
def audit():
    OUT.mkdir(parents=True,exist_ok=True); inventory=[]
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or '.git' in p.relative_to(ROOT).parts or OUT in p.parents:continue
        try:b=p.read_bytes()
        except OSError as e:
            inventory.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':'','review_level':'UNREADABLE','notes':'REVIEW_ERROR '+type(e).__name__+': '+str(e)});continue
        r={'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'review_level':'BINARY_INTEGRITY_ONLY','notes':''}
        try:
            if p.suffix.lower() in TEXT or p.name in {'LICENSE','.gitignore','.editorconfig'}:
                text=b.decode('utf-8-sig');r['review_level']='FULL_TEXT_READ_STATIC'
                if p.suffix=='.json':json.loads(text);r['notes']='JSON_PARSE_OK'
                if p.suffix=='.py':
                    try:ast.parse(text);r['notes']='PYTHON_AST_OK'
                    except SyntaxError as e:r['notes']=f'EXISTING_SYNTAX_ERROR line {e.lineno}: {e.msg}'
                if p.suffix in {'.csv','.tsv'}:
                    data=list(csv.reader(io.StringIO(text),delimiter='\t' if p.suffix=='.tsv' else ','))
                    width=len(data[0]) if data else 0
                    r['notes']=f'rows={max(0,len(data)-1)}; columns={width}; ragged_rows={sum(len(x)!=width for x in data[1:])}'
            elif p.suffix in {'.sqlite','.db'}:
                c=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True)
                names=[x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
                counts={n:c.execute('SELECT count(*) FROM "'+n.replace('"','""')+'"').fetchone()[0] for n in names}
                r['review_level']='DATABASE_SCHEMA_COUNTS_INTEGRITY';r['notes']=json.dumps({'integrity':c.execute('PRAGMA integrity_check').fetchone()[0],'tables':counts,'fk_errors':c.execute('PRAGMA foreign_key_check').fetchall()});c.close()
            elif p.suffix in {'.zip','.xlsx'}:
                with zipfile.ZipFile(p) as z:
                    assert z.testzip() is None
                    if p.suffix=='.xlsx':
                        import xml.etree.ElementTree as ET
                        for n in z.namelist():
                            if n.endswith('.xml'):ET.fromstring(z.read(n))
                r['review_level']='ARCHIVE_CRC_XML' if p.suffix=='.xlsx' else 'ARCHIVE_CRC';r['notes']='NO_VISUAL_OR_HISTORICAL_FACT_CERTIFICATION'
        except Exception as e:r['notes']='REVIEW_ERROR '+type(e).__name__+': '+str(e)
        inventory.append(r)
    with (OUT/'file_review_inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=inventory[0]);w.writeheader();w.writerows(inventory)
    (OUT/'file_review_inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
    return inventory

BLOCK='''
### 本轮执行修订：旧条款留存，以下限定优先适用

**正名、稽实、试效、留责。** 以下为现代编者拟句，不冒称古籍原文。华夏古史与春秋战国诸子百家为文化和史料主线；古典概念与现代科学方法之间须有明确映射，不能凭文化身份认定技术先进。

| 原条款或盲区 | 本轮执行口径 | 验收证据 |
|---|---|---|
| “现实无一家机构”与“售结论者皆妄” | 前者限定为本项目已核样本内尚未证明存在完整组合服务；后者为旧修辞，不是对所有现实服务商的事实裁定 | 按产品、法人、服务范围、版本分别记录，反例可使结论更新 |
| CBDB直接取战国秦汉千人、三千边 | 先查实际年代覆盖；不得把固定规模当现成数据或强造关系。先秦史料另作来源目录、异文与人物消歧 | CBDB官网说明主要7至19世纪；数量改为取数后报告真实n与缺口 |
| 前两阶段花费为零 | 改为争取无新增采购；人力、算力、联网、许可及维护成本仍记账 | 工时和资源账，不虚报零成本 |
| 默认马来西亚三十年情景 | 改为由问题、数据与模型支持范围选法域、时间和政策变量；旧案例只作可选示例 | 无默认用户国籍、居所、政治身份或单一区域过滤 |
| PEMANDU会面为任务 | 保留为全球候选之一，所在城市只是机构位置；公开方法笔记也可替代，不设强制联系或采购 | 方法来源、许可、适配条件与项目需求；本文不授权发消息 |
| 文言人物分值与κ≥0.7 | 首先评价文本编码；标注体裁、时代、代笔、转述、翻译和篇章依赖。阈值是预设目标，不是已达结果或人格诊断 | 独立标注、混淆表、置信区间及留出篇章；不得据转述推私人忠诚或心理 |
| 37件下载与待核条目清零 | 非空可为失败、未定位、许可待核；UNKNOWN只在有证据时转换，不为达标改成确认 | 每项保留处理状态及原因，不绕过访问控制 |
| “顶尖／军工／国安级” | 作为高可靠目标；当前仅是本地SQLite原型和文档方案 | 安全、性能、兼容性、恢复演练与适用认证分别验收，不借供应商资质替系统认证 |

### redteam／墨家验伪：从错误反推试题

红队用隔离副本检验品牌冒充法人、镜像重复互证、网页提示注入、错年代、同名人物、未知填零、城市坐标冒充设施、模拟混入现实及许可缺失。每例记录输入、预期、实际、影响和复查人；测试失败保留证据，禁止用删测试制造通过。已有16项测试覆盖结构与部分入库规则，不能外推为全部语义或安全已通过。

### critic／名家正名：事实、主张、方案分账

目录405行是服务候选，科研160条与法人92条是不同粒度；政府、设施、任务等表可能共用实体，不能相加成机构总数。44表、10视图是施工规模，不是科研水平或全球覆盖率。官网说明证明相应陈述来自官网，效果、因果与独立验证另记。HISTORY、REAL-TWIN、SIM、FICTION保留；REAL-TWIN内部现实／孪生语义尚未完全分离。

### killcritic／止讹闸：可驳、可撤、可恢复

此项定义为检验并处理批评，不是消除异议。批评进入“证据支持／待核／已反驳”三态，附理由与反例。新增主张必须能回源；来源失效标STALE，冲突并列而非静默覆盖。训练、再发布和商业使用各自核许可；无许可即未放行。数据库使用方必须开启外键；本地SQL约束不代替权限服务。

### blindspot／道家知止：五项仍未实现

当前未完成古籍逐篇校勘、全球机构全量、私人心理有效测量、生产安全部署及亿级性能评测。8张空领域表保留明确缺口，模拟记录必须来自实际运行。PDF视觉／内容、二进制资源及历史压缩包内事实未因哈希检查而获认证；项目静态扫描也不证明所有外部事实正确。SHA256和CRC验证完整性，不证明来源真实性或作者身份。

### cheatsheet／检籍便览：一问一据

| 所问 | 查何处 | 何时止步 |
|---|---|---|
| 表在哪里、是否改值 | 分类索引、旧新路径和SHA256 | 65文件、61迁移仅指当轮分类集合；以后新增另立批次 |
| 有何真实数据 | 数据库、44份分类CSV、26响应清单和逐表覆盖账 | 本地快照不是实时刷新，也不是全部全球实体 |
| 古人言辞能否分析 | 篇名、版本、页／卷、原文、译注、说话者／编者、年代区间、异文 | 未核原句不引号；编者拟句明示，不补造先秦样本 |
| 能否部署AI | 许可、特征合同、留出集、来源引用及人工复查 | 当前0条获准训练数据，未训练神经网络 |
| 能否正式决策 | 目标、预算、约束、反事实、误差、适用范围与责任人 | 单一综合分不得代替逐项证据 |

### blueprint／分官守职：保留底座，分层接入

`古籍／公开原始资料 → 版本与证据账 → 身份消歧 → 分领域事实 → 文本编码或政策规则 → 情景计算 → 人工审议 → 结果追踪`。

现有库继续作事实底座；检索增强生成优先输出带来源的摘要，模型输出先入待审区，不直接写canonical事实。先做只读SQL和可复算规则，数据与许可成熟后再评估机器学习。古籍研究建议新增source_work、text_witness、passage、historical_person_assertion、annotation、review等合同；此处是待建方案，不冒称已建表。每个史料片段至少保留出处、文本版本、叙述层级、年代区间、不确定性和授权范围。

防御目标参考[NIST生成式AI风险框架](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)与[OWASP提示注入防护](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)：把检索文档视为数据，工具权限最小化，工具调用在模型之外验证，输出经审核后执行；这些是拟采用控制，未声称已部署或能消灭全部风险。

### actionplan／九十日修订：按证据过门，不按篇幅过门

| 时段 | 交付 | 可核验的过门条件 |
|---|---|---|
| 1–15日：立籍 | 版本快照、问题登记、古籍来源覆盖、许可清单 | 100%所选输入有来源与版本；无证据的字段留未知 |
| 16–30日：正名 | 少量先秦篇章与实体试标，真实样本n、歧义和异文账 | 每条试标可回篇章；盲评与错误样例留存，不规定虚构千人目标 |
| 31–45日：试效 | 文言编码试验、只读查询、预算规则原型 | 与人工／简单基线比较；训练测试按篇章或来源分组防泄漏 |
| 46–60日：验伪 | 恶意检索隔离测试、性能及兼容性测量、恢复演练 | 记录p50/p95、内存、样本规模、失败率和恢复用时；未测不得填PASS |
| 61–75日：列策 | 自选法域的一项公开政策或资源分配问题，多情景敏感性分析 | 单位、预算守恒、假设与不确定性齐全；政治偏好不作为KPI |
| 76–90日：复议 | 独立复核、撤回册、需求缺口、采购判断 | 能复算和回源才发布；证据未到保持待核，不以“清零”伪造确认 |

**良策**：先把“全知全能大系统”化成“一个可回源的问题、一个可复算的方案、一次可恢复的运行”。春秋战国文化主线落在史料版本与中文知识结构，高科技目标落在可测验收；二者互相增益，均不取代证据。

CBDB年代覆盖核验：[官方项目简介](https://cbdb.hsites.harvard.edu/)（本轮读取2026-10-04）；官网的2026-05规模说明不冒充下载后测得的先秦样本数。
'''

def main():
    inventory=audit();before={p.relative_to(ROOT).as_posix():p.read_bytes() for p in TARGETS}
    with zipfile.ZipFile(OUT/'before_two_document_updates.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
        for n,b in before.items():z.writestr(n,b)
    for p in TARGETS:
        b=before[p.relative_to(ROOT).as_posix()]
        header='\n\n## v2.4 本轮七策复审与九十日执行修订（2026-10-04）\n' if p.suffix=='.md' else '\n\n## 45.8 七策复审、古史校勘与九十日执行修订\n'
        if header.strip() in b.decode('utf-8-sig'):raise RuntimeError('Already appended')
        prefix='../' if p.parent.name=='Reference' else ''
        links=f'\n复查实物：[全项目复审清单]({prefix}reports/2026-10-04/document_strengthening/file_review_inventory.csv)、[表分类索引]({prefix}reports/2026-10-04/table_reclassification/README.md)、[逐表数据覆盖]({prefix}reports/2026-10-04/dgef/tables/coverage/表施工与数据覆盖对账.csv)、[DGEF工程说明]({prefix}DGEF/README.md)。\n'
        p.write_bytes(b+(header+BLOCK+links).encode('utf-8'))
        assert p.read_bytes().startswith(b)
    result={'reviewed_files':len(inventory),'review_levels':{k:sum(r['review_level']==k for r in inventory) for k in sorted({r['review_level'] for r in inventory})},'existing_parse_findings':[{'path':r['path'],'notes':r['notes']} for r in inventory if 'ERROR' in r['notes']],'targets':{n:{'before_sha256':sha(b),'after_sha256':sha((ROOT/n).read_bytes()),'original_prefix_preserved':True} for n,b in before.items()},'scope':'All non-Git files read; static text/schema checks and binary integrity only; no universal fact or runtime certification'}
    (OUT/'review_and_preservation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True))
if __name__=='__main__':main()
