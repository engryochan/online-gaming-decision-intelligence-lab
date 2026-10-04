"""Public-source real-world service evidence, without mutating accepted DGEF facts."""
from pathlib import Path
import csv,hashlib,json,sqlite3,zipfile
import strengthen_documents as review
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'reports/2026-10-04/realworld_ecosystems'
TABLES=ROOT/'Reference/tables/05_realworld_ecosystems_20261004'
DATE='2026-10-04'
PROVIDERS=[
('中科闻歌','STRATEGY_AI','DIP／DOMA／Decitron','企业本体、数据融合、决策情景与智能体','AI与产业决策','https://www.wenge.com/aboutnew/index.html','官网名称与架构，不核实排名或预测效度'),
('华为','INDUSTRIAL_DIGITAL','智能制造与工业网络','设备连接、工业网络与制造数字化','产业基础设施','https://e.huawei.com/au/industries/manufacturing','制造网络方案，不证明本项目已兼容部署'),
('中国航天科技集团','SPACE_INDUSTRY','航天服务业','卫星地面运营、国际化及信息软件服务','制造—运营—服务','https://www.spacechina.com/n25/n146/n234/n252/index.html','集团公开业务范围，非子公司合同全集'),
('Control Risks','GEOPOLITICS','地缘风险与战略情报服务','国别、监管、尽调、情景与企业风险','风险分析—决策','https://www.controlrisks.com/our-services/intelligence-and-analysis','提供方业务描述，不证明所有效果或最大规模'),
('Eurasia Group','GEOPOLITICS','Geo-technology','AI、通信、技术供应链与地缘政策咨询','技术—地缘交叉','https://www.eurasiagroup.net/services/geotechnology','官网列出的专题，不是预测成绩'),
('RANE','GEOPOLITICS','Enterprise Risk Intelligence','信号、专家分析、情景、行业暴露与API','风险工作流','https://www.ranenetwork.com/','服务架构与API描述，专有内容未下载'),
('Janes','DEFENCE_MARKET','公开防务与安全情报','防务预算、项目、市场与结构化数据','公开产业情报','https://www.janes.com/','仅用于公开宏观与采购产业分析，不展开作战使用'),
('McKinsey','STRATEGY','地缘韧性与情景规划','企业组织、地区暴露与经营韧性方法','咨询—组织实施','https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/can-your-company-remain-global-and-if-so-how/','方法文章可核，效果非本轮独立验证'),
('BCG','STRATEGY','2026全球贸易情景研究','贸易结构、企业策略与情景分析','贸易—战略','https://www.bcg.com/publications/2026/how-prepare-patchwork-world-order','情景不是实际未来结果'),
('PEMANDU Associates','STRATEGY_DELIVERY','8-step BFR','组织转型与交付方法','策略—执行','https://pemandu.org/about-us/','全球候选；不由机构位置推用户居所'),
('Palantir','STRATEGY_AI','AIP／Ontology','企业本体、模型集成、智能体、评估和工作流','数据—AI—决策','https://www.palantir.com/docs/foundry/architecture-center/aip-architecture','产品架构，不证明本地部署或同等安全'),
('Altana','SUPPLY_CHAIN_AI','Value Chain平台','多层供应链映射、集中度与合规筛查','贸易—供应链图谱','https://altana.ai/platform','能力描述；推断边不得充当确认供应关系'),
('Airbus','SPACE_DEFENCE_INDUSTRY','公开供应商接入与采购','分采购类别、供应链质量与网络安全要求','采购—供应链治理','https://www.airbus.com/en/becoming-an-airbus-supplier','流程可核，不推断特定供货合同'),
('Thales','CYBER_DEFENCE','Cyber Detection & Response','跨行业网络检测、事件响应与防御服务','安全—运维','https://www.thalesgroup.com/en/solutions-catalogue/cybersecurity/cybersecurity-services/cyber-detection-response','提供方防御服务说明，无本项目安全认证'),
('Planet','EARTH_OBSERVATION','公开客户案例','农业、资源、灾害与供应链遥感应用','观测—产业应用','https://www.planet.com/company/customer-stories/','客户案例由提供方发布，量化收益另核'),
('PolicyEngine','POLICY_RULES','税收福利政策模型','规则、校准、验证及政策改革分析','公共政策—规则计算','https://www.policyengine.org/us','已读美国页面；全球不意味着任一法域直接可用'),
('OpenFisca','POLICY_RULES','Rules as Code','法规可计算化、Python与JSON API','法规—公共服务','https://openfisca.org/en/','平台与国别包能力；具体法律须按现行法域验收'),
('Intelligence Online','SPECIALIST_MEDIA','情报外交专业报道','专门新闻与产业线索','报道—待核线索','https://www.intelligenceonline.com/info/aboutus','只核出版定位，不证明付费文章或所谓内幕事实')]

DATA_SOURCES=[
('DS01','SIPRI','军费统计','https://www.sipri.org/media/press-release/2026/global-military-spending-rise-continues-european-and-asian-expenditures-surge','2026-04-27','2025','8条手工核对统计；非全库下载','军费包括人员、运行等，不能当军工订单；增幅为不变2024价'),
('DS02','OECD','TiVA／ICIO','https://www.oecd.org/en/topics/sub-issues/trade-in-value-added.html','','2025 edition','入口与方法已核；未导入完整投入产出矩阵','增加值与总额贸易分开；版次不是所有观察年份'),
('DS03','UN Comtrade','商品贸易','https://comtrade.un.org/','','','公开入口已核；未导入贸易流','reporter／partner／flow／period／HS版／unit必须齐备')]
OBS=[
('WORLD','military_expenditure',2887,'USD_billion_current_prices',''),
('WORLD','military_expenditure_real_growth',2.9,'percent','2024'),
('WORLD','military_expenditure_share_gdp',2.5,'percent','GDP'),
('EUROPE','military_expenditure',864,'USD_billion_current_prices',''),
('ASIA_OCEANIA','military_expenditure',681,'USD_billion_current_prices',''),
('US','military_expenditure',954,'USD_billion_current_prices',''),
('CN','military_expenditure',336,'USD_billion_current_prices',''),
('CN','military_expenditure_real_growth',7.4,'percent','2024')]

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'before_documents.zip').exists():raise RuntimeError('Already installed; explicit update required')
    source_rows=[];provider_rows=[]
    for i,(name,domain,product,cap,stage,url,scope) in enumerate(PROVIDERS,1):
        sid=f'RW{i:03d}'
        source_rows.append(dict(source_id=sid,publisher=name,url=url,checked_on=DATE,published_on='',source_tier='PUBLISHER_SELF_DESCRIPTION',access_mode='PUBLIC_WEB_TOOL_READ',raw_http_snapshot='NOT_ARCHIVED',scope=scope,redistribution_license='UNKNOWN',training_permission='UNKNOWN',supremacy_verified='NO'))
        provider_rows.append(dict(record_id=sid,provider_label=name,legal_entity_resolution='NOT_RECONFIRMED_IN_THIS_BATCH',domain=domain,product_or_service=product,capability=cap,chain_role=stage,source_id=sid,evidence_state='VERIFIED_PUBLIC_DESCRIPTION_ONLY',performance_state='NOT_INDEPENDENTLY_TESTED',world_scope='REAL_WORLD',as_of=DATE))
    for sid,publisher,title,url,pub,period,status,note in DATA_SOURCES:
        source_rows.append(dict(source_id=sid,publisher=publisher,url=url,checked_on=DATE,published_on=pub,source_tier='STATISTICAL_PUBLISHER',access_mode='PUBLIC_WEB_TOOL_READ',raw_http_snapshot='NOT_ARCHIVED',scope=status+'；'+note,redistribution_license='UNKNOWN',training_permission='UNKNOWN',supremacy_verified='NO'))
    observation_rows=[dict(observation_id=f'M{i:02d}',region_or_country=region,metric=metric,value=value,unit=unit,comparison_base=base,observation_period='2025',published_on='2026-04-27',checked_on=DATE,price_basis='CONSTANT_2024_PRICES' if 'growth' in metric else 'CURRENT_USD' if unit.startswith('USD') else 'RATIO_AS_REPORTED',source_id='DS01',evidence_state='PUBLISHED_STATISTICAL_ESTIMATE',limitation='Not contractor revenue, equipment orders or operational capability') for i,(region,metric,value,unit,base) in enumerate(OBS,1)]
    relations=[dict(relation_id='R01',subject='Planet',object='Bayer',relation_type='PUBLISHER_REPORTED_CUSTOMER_PARTNERSHIP',source_id='RW015',source_date='',checked_on=DATE,contract_value='',supplier_tier='',scope='官网客户案例描述合作；非独立合同核定'),dict(relation_id='R02',subject='Janes',object='Seerist',relation_type='PUBLISHER_ANNOUNCED_WORKFLOW_COLLABORATION',source_id='RW007',source_date='2026-09-29',checked_on=DATE,contract_value='',supplier_tier='',scope='Janes首页公告标题可见；公告全文未取得')]
    routes=[dict(stage_id=f'L{i:02d}',stage=stage,required_evidence=evidence,join_keys=keys,status='DESIGN_CONTRACT_NOT_FULL_DATA',operational_scope='PUBLIC_NON_OPERATIONAL_INDUSTRY_ANALYSIS') for i,(stage,evidence,keys) in enumerate([
    ('原材料与能源','贸易流、投入产出、价格及单位','HS/ISIC+period+country'),('部件与工业软件','法人、产品、质量与公开合同','entity+product+contract+version'),('集成制造与交付','公开订单、交付、收入与产能口径','legal_entity+segment+period'),('宇航与地面服务','公开任务、运营状态与服务合同','mission+operator+as_of'),('观测与行业应用','授权遥感、观测时间、分辨率与产业标签','dataset+epoch+region+license'),('咨询与地缘情报','主张、证据、范围、误差与版本','source+claim+validity'),('AI与决策计算','真实输入、规则、模型、回测与许可','feature_contract+model_version+run'),('防御与运维','安全控制、恢复演练及可核资质','control+asset_class+test_date'),('公共政策与结果','预算、就业、民生、环境指标','jurisdiction+rule_version+period')],1)]
    for filename,rows in [('sources.csv',source_rows),('provider_capabilities.csv',provider_rows),('realworld_observations.csv',observation_rows),('public_relationships.csv',relations),('industry_chain_contracts.csv',routes)]:write_csv(TABLES/filename,rows)
    attempts=[{'url':'https://www.oxan.com/','status':'REDIRECT_TARGET_UNAVAILABLE','note':'Redirect reported to Dow Jones; no current services certified'},{'url':'https://www.pemandu.org/','status':'UNAVAILABLE_HOST_VARIANT','note':'Verified non-www pemandu.org about-us source instead'},{'url':'https://www.intelligenceonline.com/','status':'HOME_TIMEOUT','note':'Public about-us successfully read; subscriber articles not accessed'},{'url':'https://www.janes.com/osint-insights/defence-and-national-security-analysis/post/seerist-and-janes-bring-real-time-global-risk-signals-and-validated-military-intelligence-into-one-workflow','status':'FULL_ARTICLE_UNAVAILABLE','note':'Only dated homepage announcement used'},{'query':'CASIC／AVIC official service search','status':'NOT_CONFIRMED_THIS_BATCH','note':'Secondary results not promoted to verified current official capability'}]
    (OUT/'access_attempts.json').write_text(json.dumps(attempts,ensure_ascii=False,indent=2),encoding='utf-8')
    # Review the existing project again after collecting evidence, before changing the two documents.
    review.OUT=OUT/'corpus_review';inventory=review.audit()
    targets=review.TARGETS;before={p.relative_to(ROOT).as_posix():p.read_bytes() for p in targets}
    baseline_db_hash=sha(ROOT/'DGEF/artifacts/dgef.sqlite')
    with zipfile.ZipFile(OUT/'before_documents.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
        for n,b in before.items():z.writestr(n,b)
    for p in targets:
        prefix='../' if p.parent.name=='Reference' else ''
        heading='## 现实百业生态、地缘与策略产业链更新（2026-10-04）' if p.suffix=='.md' else '## 45.9 现实百业生态、地缘与策略产业链更新（2026-10-04）'
        text='\n\n'+heading+'\n\n'+CONTENT
        text+='\n### 本轮核实的公开能力目录\n\n| 服务商／平台 | 现实能力与产业链角色 | 可核出处 |\n|---|---|---|\n'
        for name,domain,product,cap,stage,url,scope in PROVIDERS:text+=f'| {name} · {product} | {cap}；{stage} | [官网]({url}) |\n'
        text+=f'\n本轮独立增补台账：[18条服务能力]({prefix}Reference/tables/05_realworld_ecosystems_20261004/provider_capabilities.csv)、[21条来源]({prefix}Reference/tables/05_realworld_ecosystems_20261004/sources.csv)、[8条现实统计]({prefix}Reference/tables/05_realworld_ecosystems_20261004/realworld_observations.csv)、[2条公开关系]({prefix}Reference/tables/05_realworld_ecosystems_20261004/public_relationships.csv)、[9层产业链合同]({prefix}Reference/tables/05_realworld_ecosystems_20261004/industry_chain_contracts.csv)。[本轮复审回执]({prefix}reports/2026-10-04/realworld_ecosystems/README.md)。这些表为独立来源批次，未改旧DGEF44表及其根号，未强行将品牌消歧为法人。\n'
        p.write_bytes(before[p.relative_to(ROOT).as_posix()]+text.encode('utf-8'))
    assert baseline_db_hash==sha(ROOT/'DGEF/artifacts/dgef.sqlite')
    result={'checked_on':DATE,'provider_records':18,'sources':21,'observations':8,'public_relationships':2,'chain_contracts':9,'corpus_files_inventoried':len(inventory),'dge_database_unchanged':True,'targets':{n:{'before_sha256':hashlib.sha256(b).hexdigest(),'after_sha256':sha(ROOT/n),'original_prefix_preserved':(ROOT/n).read_bytes().startswith(b)} for n,b in before.items()},'table_sha256':{p.name:sha(p) for p in TABLES.glob('*.csv')},'fact_scope':'Observed public descriptions and selected 2025 statistics; no comprehensive 2026 annual results, performance ranking, private leak verification or full industry graph'}
    (OUT/'build_receipt.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'README.md').write_text(REPORT,encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True))

CONTENT='''**现行任务口径，以本节为准：分析现实生活的百业生态产业链，服务现实决策。** 上节古人样本、先秦篇章试标、历史人物画像与历史情景步骤保留为历史编辑记录，退出当前执行计划和验收必选项。春秋战国诸子百家、文言文与华夏习俗文化继续作为中文知识组织、制度隐喻和表达主线；不以古人评分代替现实机构、产业、预算、贸易和民生数据。以下拟句为现代编者所作：**名正而籍清，数实而策审，百业相联，功过可稽。**

时点为2026-10-04所读资料，区分抓取／核对日、发布日、观察期、有效期与修订版。网页可见但未标发布日期者，不倒推出某项功能在当年何日上线；“前沿／顶尖”保留为目标与候选筛选要求，未经独立基准不写成排名事实。选择中外公开技术生态时以需求、许可、兼容性、成本、稳定性、可复算性和安全验证作决定，文化主线不因技术来源改变。

### redteam／验伪：三类现实链都要有反例

地缘链审验“事件／政策→能源、贸易、融资、物流→企业暴露→民生结果”；策略链审验“数据→规则与分析→方案→责任与执行→结果”；军工宇航国安产业链审验“公开需求／预算→研发与供应→制造交付→运营维护→公开服务”。用错年、错币种、镜像重复、营销升级为独立证据、遥感误读、同名实体、伪造供货边、预测当实绩和注入文本作隔离测试。只记录公开宏观、产业、韧性与防御信息，不生成设施薄弱点、目标选择或操作性攻击方案。

### critic／正名：服务、订单、收入、效果各守其籍

本轮18条官网能力记录不等于18个已消歧法人，也不等于独立测试通过。地缘咨询与专业报道是不同角色；Intelligence Online公开介绍证明其专业媒体定位，不能使付费传闻直接成为事实。Altana的供应链推断不等于已确认供货；Janes与Seerist的首页公告只支持公开宣布的工作流合作，Planet与Bayer案例只支持提供方发布的合作描述。合同金额、交付数量与供应层级未知即留空。

中科闻歌官网现列DIP、DOMA与Decitron；旧DIOS资料作为旧名称／版本保留，不能据字符串相近断定全部产品同一。华为制造网络、中国航天科技集团服务、Airbus供应商流程、Thales防御服务和Planet行业案例属于不同产业层，不混成万能“治国平台”。

### killcritic／复议止讹：只在证据范围内确认

每条主张有来源、发布日期或未注明标记、核对日、支持范围、观察期、许可与撤回理由。发布者自述标PUBLISHER_SELF_DESCRIPTION；统计机构估计标PUBLISHED_STATISTICAL_ESTIMATE；采购／合同、监管披露、独立研究和媒体线索分层。审查意见可反驳、待核或采纳，不抹除批评。外网失败保持失败；非www的PEMANDU官网已核，不将www失败误作机构不存在。访问订阅内容依授权，不绕过登录、付费墙或访问控制。

### blindspot／知未详：现实数据也有边界

截至本轮未取得完整企业交易、所有多层供应商或未公开预算，未测试服务商付费平台，未核实全部主张及私有材料。OID、LEI、统一社会信用代码、集团、品牌和产品需要逐层消歧。国防支出不等于装备采购、军工收入、产能或作战效能；遥感可辅助生产活动研究，但不能单凭影像认定秘密设施用途。保留未知、样本选择偏差、年度修订与本币换算误差。

### cheatsheet／检籍：先看真实计量再看名录

| 所问 | 本轮事实与方法 | 限定 |
|---|---|---|
| 军工产业宏观需求 | SIPRI于2026-04-27发布2025年全球军费2887十亿美元、实质同比2.9% | 是2025观察，不是2026全年；实质同比采用不变价，金额另列当年美元 |
| 中国公开宏观支出 | 同一来源估计2025年336十亿美元、实质同比7.4% | 来源方法与统计估计，不等于订单或企业营收 |
| 百业跨境联系 | UN Comtrade看商品贸易，OECD TiVA／ICIO看增加值与投入产出 | 入口与方法已核；本轮未下载完整贸易流或矩阵 |
| 高端地缘服务 | Control Risks、Eurasia Group、RANE、Janes | 本轮核业务描述；不认证预测准确率 |
| 高端策略与现实计算 | McKinsey、BCG、PEMANDU、Palantir、中科闻歌、Altana、PolicyEngine、OpenFisca | 方法、平台、交付和国别规则包不可互换 |
| 宇航与防御产业 | 中国航天科技集团、华为、Airbus、Thales、Planet | 公开能力与案例；不是完整供应链或安全认证 |

统计依据：[SIPRI 2026发布的2025军费](https://www.sipri.org/media/press-release/2026/global-military-spending-rise-continues-european-and-asian-expenditures-surge)；产业链方法依据：[OECD TiVA](https://www.oecd.org/en/topics/sub-issues/trade-in-value-added.html)、[UN Comtrade](https://comtrade.un.org/)。同比、存量、流量、预算、执行与收益分别记账。

### blueprint／现实百业母体：从清单升级为证据图

`公开源／授权企业数据 → 发布版本与许可 → 法人、产品、行业消歧 → 贸易／合同／生产／预算／事件事实 → 有出处的产业关系 → 规则计算和可验证情景 → 人工审议 → 现实结果追踪`。

人物层只保留与问题相关的公开任职、责任与有效时期，不做私人心理、忠诚或隐秘意图推定。与历史人物研究分流。实体图采用关系类型、原始证据、有效期、置信状态与是否推断，禁止“图上有线就有交易”。投入产出行业边不降格解释为两家企业直接供货。生产模型先以简单可复算基线比较；大模型负责检索、归纳、候选匹配与解释，数值由版本化规则和分析程序复核。

高科技栈以本体／知识图谱、地理时序、投入产出分析、规则引擎、概率校准、离线评测和只读检索为候选；智能体执行在人工审批与最小权限内。私有化、多模型兼容、冷热存储、SBOM、密钥管理、访问分层和灾备均需独立施工与测试；当前本地SQL原型不能继承厂商“军工级”或安全宣传。

### actionplan／九十日现实执行：撤出古人试标门槛

| 时段 | 现实交付 | 验收 |
|---|---|---|
| 1–15日 | 选一个现实百业问题，定义企业／行业／地区、预算、指标与许可；本轮能力台账作候选源 | 观察期与发布期分开；输入无默认马来西亚过滤 |
| 16–30日 | 接入一个产业的官方贸易、企业披露或公开合同，核法人、币种、单位与版本 | 每条采纳事实可回源，明确覆盖分母；无据关系不确认 |
| 31–45日 | 建产业证据图，分供应、客户、持股、合作、同业与推断；计算集中度与投入产出暴露 | 附金额口径与行业粒度；未知不填零，不做设施级弱点分析 |
| 46–60日 | 比较简单基线与候选AI；按时间／实体留出，做误差、校准、漂移及注入测试 | 报真实样本n、错误案例、p50/p95与成本；不以宣传认定高效率 |
| 61–75日 | 真实产业的预算／采购／供应韧性三方案，敏感性与可行性审查 | 固定输入版可复算；预测与实际分栏，不预言未来 |
| 76–90日 | 结果追踪、独立复核、恢复演练与采购裁定 | 有据才扩大；无授权私有数据保持缺口，保留撤回与回滚 |

本轮五份CSV为已落实实物；9层产业链合同是分析定义，不伪称已有全链交易数据；新神经网络、生产安全系统和上述后续运行仍是待验收工作。
'''

REPORT='''# 现实百业产业链更新与核验回执

本轮遵从用户新口径：现实数据分析现实百业，古史文化用于表达和知识组织，不把历史人物画像当当前任务。

已浏览官网、统计发布及专业媒体公开介绍；21条来源、18条服务能力、8条2025观察统计、2条提供方公开关系和9层分析合同分别存表。出处与范围逐行记载，未获取全部付费产品、未经授权内幕材料或所有贸易流。网站读取通过web工具，不冒称原始HTTP响应已在本地归档。

取得来源后再次静态读取项目，清单见corpus_review/file_review_inventory.csv。二进制仅做完整性，锁文件及原有Python语法问题保留；不外推为全项目专家语义认证或运行通过。

两份目标文档在原字节末尾新增现行口径、七策、公开能力表和现实九十日计划，退出古人试标必选步骤；原文仍保留。before_documents.zip和build_receipt.json记录恢复点与摘要。DGEF既有数据库不改，品牌不自动建成法人。

SIPRI数据为2025观察、2026发布；官网性能和排名未独立复测。Intelligence Online只核公开媒体介绍，不将未读文章认定事实。Oxford Analytica跳转目标未取得，CASIC／AVIC本轮官网能力未确认，均不伪填核实；访问问题详见access_attempts.json。

新增五表位于Reference/tables/05_realworld_ecosystems_20261004，属于新增批次，不改变旧65文件分类快照。行业合同不是现实交易记录，许可UNKNOWN也不代表允许训练或再发布全文。
'''
if __name__=='__main__':main()
