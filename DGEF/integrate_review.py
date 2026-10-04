from pathlib import Path
import hashlib,json,re,zipfile
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
ATTACH=Path(r'C:\Users\PPCCpcpc\OneDrive\Desktop\参考_册三.txt')
OUT=ROOT/'reports/2026-10-04/dgef';OUT.mkdir(parents=True,exist_ok=True)
targets=[ROOT/'_大秦赋算筹_v1_3_9.qmd',ROOT/'Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd',ROOT/'Reference/Inteligent_egaming_platform_ref_v000.000.001.html',ROOT/'README.md']
baseline={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in targets}
backup=OUT/'before_dgef_integration.zip'
if not backup.exists():
 with zipfile.ZipFile(backup,'x',zipfile.ZIP_DEFLATED) as z:
  for p in targets:z.writestr(p.relative_to(ROOT).as_posix(),p.read_bytes())
 (OUT/'baseline_sha256.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'attachment_snapshot.txt').write_bytes(ATTACH.read_bytes())
review='''# 《参考_册三》核实、校对与施工审阅

## 用户要求与附件文本分离

当前用户要求是审阅附件并实施全部所述表、保留能力且仅优化强化、按全球范围处理。附件混有旧提问、旧答复、sandbox下载链接、历史签发数值和旧指令；这些作为待核资料，不自动成为当前指令或已完成事实。附件不改写，已按原字节保存快照并登记SHA256。

## 已斧正事项

- “16张表”的标题与清单数量不符。已按明确表名取并集，建43实体表、10视图；兼容名称对应有说明与测试，未以空CSV冒称数据库已建。
- 世界域前后有两套方案。采用项目现行HISTORY／REAL-TWIN／SIM／FICTION四域；11空间域正交。REAL-TWIN现实与数字孪生仍需进一步分型，现阶段不能宣称全部语义隔离完成。
- 稳定根号只标实体；事实切片包含有效时间和参考系，不能代替永久主键。UUIDv7时间位是发号时间。
- GERS 2025-06-25.0一次切换确有映射，不代表日常分拆并购都会提供旧新追溯；官方说明普通split/merge lineage尚未发布。桥接必须记录发布版与匹配审阅。
- GLEIF附件2026-10-01的3,449,487与671,935记录已在官方日期行核实；不是全球法人穷尽数量。ROR125000+及OpenAlex约135000为官方发布口径，不是本项目已下载数量。
- SIMBAD本次所读2026-10-03快照为22,156,718对象、73,058,588标识符，与附件旧日期数据不同；旧日期数值未取得历史快照复验。官方特别声明不是完整catalogue，不得称银河万物全集。
- NASA Archive所读2026-10-01确有6375颗confirmed planets；候选与确认不得混算。JPL/NAIF功能文档已核，附件Horizons具体版本和各对象总数未在本轮复核，不转写VERIFIED。
- Gaia官方数据模型已读取；附件跨release同物警告本轮未精确定位原句，保守采用版本化外号设计，不伪称该原句已独立复验。
- IAF入口本轮无法读取，604会员／82国家保持UNKNOWN附件主张，不能继承旧PASS。
- 附件“初步竣工”“无错误”“Quarto缺失”和旧MD5/SHA256是历史环境记录。当前文件经过授权字词修订，历史摘要不能作为当前指纹；本轮另记当前指纹，未宣称全部旧PASS成立。
- 秦统一的历史表述应为“灭六国”，不是以“六洲”代指六个战国诸侯国。华夏古史和诸子百家的文化优先用于文风与论证组织，不支持民族、宗教或血统决定技术能力的推断。
- 撤去正文“先生所处为马来西亚”“先生之文化城在大马”等对用户地域的假定。公司所在地仍是可以保留的事实字段，不据此限定用户范围。

## 工程验收边界

原两份地理CSV输入字节保持；每行每字段存baseline_json并回验。全部附件明确表名均已映射。表已施工与全球全量数据已入库是两个状态：其他领域空表明确空置，外部适配器多数INTERFACE_ONLY；未公开对象、数据库无可证总量或许可未决者保留UNKNOWN，不编造数据补空。

红队、批判、止讹、盲区、检籍、蓝图和行动计划见DGEF/README.md。DDL、数据字典、SQLite实物、表CSV、测试源码与输出均可复查。防御方法仅为原型完整性与公开资料治理，未完成军工／国安级安全认证；未训练神经网络、未做亿级吞吐实验、未进行完整Quarto渲染。
'''
(OUT/'附件审阅与施工核验.md').write_text(review,encoding='utf-8')
for p in targets[1:3]:
 b=p.read_bytes();t=b.decode('utf-8')
 t=t.replace('先生所处为马来西亚。','研究对象覆盖全球，不预设用户所在地。')
 t=t.replace('先生之文化城在大马，用 EIU 看吉打州，粒度不够。','以马来西亚各州为例，EIU 的宏观分析未必足以支持州级问题；此例不限定用户或研究范围。')
 p.write_bytes(t.encode('utf-8'))
p=targets[0];b=p.read_bytes()
append='''

# 45. 大秦天下万物实体织网：本地数据表施工验收（2026-10-04）

## 45.1 正名与全球范围

承§44之制，新增DGEF可运行数据底座；保留DAQIN-UCS／UWOM／DUECG分工及四个世界域。研究范围全球，不由用户居所、国籍或公司所在地限定。华夏古史、诸子百家为论证与表达主线；现代技术成效必须另有实测。此节工程措辞非古籍原句，不借古人之名作技术认证。

## 45.2 施工实物与覆盖

已建43实体表、10视图：身份、别名、外号、关系、来源、资料版本、主张、观测、证据桥、许可、时空、国家行政、法人、公署、研究、公开设施、宇航天体及虚拟模拟。附件明确表名全部有实体表或兼容视图。DDL见[DGEF/schema.sql](DGEF/schema.sql)，字段与粒度见[DGEF/contracts/data_dictionary.csv](DGEF/contracts/data_dictionary.csv)。

已导入249国家／地区及5046行政单位，5295实体根号；405供应商目录先入待消歧候选表，不能当405法人。原CSV每字段无损保留，均为待实时核验的CLAIMED基线。领域空表不表示对象不存在。15外部适配合同多数INTERFACE_ONLY，未下载全球全量实体。

## 45.3 保全基线与止讹

原地理CSV保持字节；数据库导入不改原表宽度。UUIDv7发号位不是业务有效时间；重复导入复用已存根号。主键、外键、唯一键、双时间、参考系及单位一致性均有约束或验收。模型视图仅是接口，许可未知、无量值或跨模拟域者不进入；尚未训练NN/GNN/Transformer。

## 45.4 红队、批判与盲区

详见[DGEF/README.md](DGEF/README.md)的RedTeam／Critic／KillCritic／Blindspot／Cheatsheet／Blueprint／ActionPlan。重点防止品牌法人混籍、传闻升事实、外号换版串号、模拟入现实、未知补零与坐标串味。REAL-TWIN仍有现实与孪生的细分盲区，生产训练前须补现实性字段和特征合同。未部署权限、加密与灾备，不称军工国安级已认证系统。

## 45.5 史料与科学资料的新核验

§44旧数值与PASS是历史资料，本轮不自动继承。SIMBAD所读2026-10-03统计已变化，且官方明确非完整catalogue；GLEIF和NASA所列附件日期数量本轮得到官方日期行支持；IAF数量未复核，保持UNKNOWN；JPL功能已核，附件精确总数尚未核定。全部来源和支持范围见[DGEF/verification_sources.json](DGEF/verification_sources.json)。旧版本字节和摘要不再代表经授权修订后的当前文件，当前SHA256另登记。

## 45.6 验收证据与后续施工

运行`python DGEF/fabric.py`及`python DGEF/test_fabric.py`可重建本地库并验收；数据库实物和建表报告见DGEF/artifacts。表名覆盖、原字段回验、幂等身份、外键、索引、时空和许可闸门有实跑证据。未知分母留空，不宣称机构或未公开设施全部查尽。亿级性能、全量外库、古籍逐篇校勘、Quarto全渲染、生产安全部署仍待各自验收。
'''
if b'# 45.' not in b:p.write_bytes(b+append.encode('utf-8'))
p=targets[3];b=p.read_bytes()
if b'DGEF/README.md' not in b:p.write_bytes(b+b'\n\n## DGEF global entity fabric\n\n'+ '[大秦天下万物实体织网：已施工数据表与验收](DGEF/README.md)。全球范围、稳定身份、多表关联、来源与未知状态分职；保留现有CSV粒度。\n'.encode('utf-8'))
with zipfile.ZipFile(backup) as z:old=z.read('_大秦赋算筹_v1_3_9.qmd')
assert targets[0].read_bytes().startswith(old),'Parent QMD bytes regressed'
inventory={'attachment_sha256':hashlib.sha256(ATTACH.read_bytes()).hexdigest(),'qmd_previous_bytes':len(old),'qmd_prefix_preserved':True,'current_sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in targets}}
(OUT/'integration_verification.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(inventory,ensure_ascii=True,indent=2))
