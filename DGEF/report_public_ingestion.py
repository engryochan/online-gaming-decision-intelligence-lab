from pathlib import Path
import csv,json,sqlite3
import fabric as f
OUT=f.ROOT/'reports/2026-10-04/dgef'
c=sqlite3.connect((f.HERE/'artifacts/dgef.sqlite').as_uri()+'?mode=ro',uri=True)
c.execute('ATTACH DATABASE ? AS baseline',((OUT/'before_public_ingestion.sqlite').as_uri()+'?mode=ro',))
counts={n:c.execute(f'SELECT count(*) FROM {n}').fetchone()[0] for n in f.SPECS}
base=c.execute('SELECT count(*) FROM baseline.registry_entity').fetchone()[0]
gap={
'registry_astrobiology_evidence':'尚未接入带论文与误差的生命证据记录；不把无确认生命写成每个对象为0',
'registry_settlement':'ROR城市信息不是完整聚落库，未接入官方地名或人口资料',
'registry_infrastructure':'需按具体设施类型核实主管者、公开资料与许可',
'registry_person_public_role':'本轮范围机构为主，尚未核对公开任职及生效时期',
'registry_virtual_world':'现实网页不证明某虚拟世界已运行；需产品版本与公开场景证据',
'registry_virtual_entity':'须先有虚拟世界记录，不以现实实体强填',
'registry_simulation_run':'须实际运行日志；网上模型介绍不能冒作本项目运行记录',
'registry_synthetic_population':'须真实生成过程与参数；不得为填表编造人口',
}
rows=[]
for n,(ddl,zh,grain) in f.SPECS.items():
 rows.append(dict(table=n,name_zh=zh,grain=grain,records=counts[n],status='POPULATED' if counts[n] else 'EMPTY_EXPLICIT',source_route='registry_source → registry_dataset → registry_ingest_record/claim/evidence' if counts[n] else 'PENDING',gap_reason=gap.get(n,'尚无通过本表粒度与来源校验的记录') if not counts[n] else '数据为有边界的快照，不宣称全球穷尽'))
with (OUT/'表施工与数据覆盖对账.csv').open('w',encoding='utf-8-sig',newline='') as stream:
 w=csv.DictWriter(stream,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
text=['# 网站查证与真实数据入库复审','',
'再次对照《参考_册三.txt》：此前已建表结构，本轮已从26个公开API／官网响应接入真实记录。新增原行账用于保存外部响应中的每一条记录；现为44张表、10视图，旧43张表全部保留。','',
f'实体由{base}增至{counts["registry_entity"]}，本轮累计新增{counts["registry_entity"]-base}个。各表记录数不是独立公司数，不得相加。科研表及公署表可属于同一实体，快照记录也可能重复表达同一组织。','',
'| 已填领域 | 当前记录数 | 核验范围 |','|---|---|---|']
for n in ('registry_research_org','registry_legal_entity','registry_public_body','registry_public_facility','registry_entity_relation','registry_celestial_object','registry_observation','registry_entity_location','registry_ephemeris_solution','registry_space_org','registry_space_program','registry_space_mission','registry_space_asset','registry_space_vehicle','registry_ground_facility_public','registry_space_research_output'):
 text.append(f'| {f.SPECS[n][1]} / {n} | {counts[n]} | 对应来源支持的字段；不继承顶尖排名、全球完整性或独立性能验证 |')
text += ['','## 再次核实后的关键校正','',
'- ROR查询返回科研相关组织，不是“全球全部顶尖研究所”名单；本轮用8个关键词，覆盖中国科学院、清华、哈尔滨工业大学及全球宇航科研相关机构，检索命中不等于质量排名。ROR组织类型可支持government或facility分类，不替代法定职责核验。',
'- ROR的GeoNames坐标是所在城市信息，不是实验室、基地或园区精确位置；未进入地球设施位置账。关系只接受双方端点均已返回且身份明确的ROR关系；未取得的端点不猜补。',
'- GLEIF按中国、美国、德国、日本、印度取公开法人记录；这些是查询样本，不是五国顶尖企业排名。LEI不是全部企业，停用或失效LEI也不等于法人不存在。个人独资类别本轮跳过，未根据名字自动判国企民企。',
'- NASA档案20条系外行星记录与JPL5个小天体、3个太阳系对象已入账；6条星历向量逐数回验。星历是源模型计算解，不冒充直接观测；参考系为源响应所述J2000黄道、太阳中心、TDB、AU与AU/day。',
'- 天体物理观测表保存SBDB公布参数与引用，方法标为catalog retrieval；未知单位或误差明确保留。科研成果表保存SBDB列出的文献引用，不宣称已读全文、取得完整篇名或DOI。',
'- 国家航天局公开报道用于嫦娥五号历史任务及相关探测器／长征五号遥五记录；NASA官网用于Artemis／Artemis I／Orion／SLS与公开中心记录。历史已发射不自动变成今天仍运营。',
'- JPL首次取数遇证书错误，改用Windows现有Schannel信任库后取得响应；未使用跳过证书验证参数，也未安装证书或改变安全设置。',
'- 官网与权威库优先；论坛、镜像、所谓野网只可作线索。可访问不等于事实成立、可训练或可再发布；本轮未采集未知敏感位置，也未训练模型。','',
'## 空表为何保留','',
'| 空表 | 下一步所需证据 |','|---|---|']
for r in rows:
 if not r['records']:text.append(f'| {r["table"]} | {r["gap_reason"]} |')
text+=['','## 可复查实物','',
'- DGEF/inbox/manifest.json：26个请求、抓取时间、TLS后端、响应文件与SHA256。',
'- DGEF/artifacts/dgef.sqlite及tables目录：真实数据库与44份CSV。',
'- 表施工与数据覆盖对账.csv：逐表粒度、记录数、空缺原因。',
'- before_public_ingestion.sqlite：入库前数据库备份；测试逐表检查所有旧行仍在且原值未变。',
'- public_acceptance_tests.txt：实际响应指纹、法人字段、星历向量、外键、基线保全与非虚构填充验收。','',
'结论：所述表可以依据不同公开来源逐类填实，本轮已完成第一批跨域入库；不能用“任何网站”替代证据分级，也不能把未取到或未运行的数据伪造为完成。','']
(OUT/'网站查证与真实数据入库复审.md').write_text('\n'.join(text),encoding='utf-8')
print(json.dumps({'tables':len(rows),'populated':sum(bool(r['records']) for r in rows),'empty':[r['table'] for r in rows if not r['records']],'cumulative_new_entities':counts['registry_entity']-base},ensure_ascii=True))
c.close()
