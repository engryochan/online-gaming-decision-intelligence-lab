from pathlib import Path
import csv
OUT=Path(__file__).resolve().parent
entries=[
('NRI','V','https://www.nri.com/en/','官网确认咨询、智库与IT服务；未核价格和成效'),
('Gartner','V','https://www.gartner.com/en','官网确认研究、专家咨询与决策工具；未核排名和成效'),
('SHL','V','https://support.shl.com/viewArticle.html?d=SHL-Client-Article-12&hl=en','官方支持文档确认TalentCentral测评项目与报告管理；主站403'),
('Gallup','V','https://www.gallup.com/cliftonstrengths/en/home.aspx','官网确认CliftonStrengths测评；未核独立效度'),
('Aon','V','https://www.aon.com/en/capabilities/talent-and-rewards','官网确认人才与薪酬服务；未核独立效度'),
('Talogy','P','https://talogy.com/en/','确认Talogy人才策略服务；此合并条目的Caliper归属及现行规格仍待核'),
('Thomas International','V','https://www.thomas.co/','官网确认Thomas CXI测评、团队分析与咨询服务；未核独立效度'),
('The Predictive Index','V','https://www.predictiveindex.com/','官网确认人才优化定位；未核独立效度'),
('HireVue','V','https://www.hirevue.com/','官网确认招聘人才决策服务；未据此核实Pymetrics或Traitify归属'),
('Criteria','V','https://www.criteriacorp.com/','官网确认雇前测评服务；未核独立效度'),
('The Myers-Briggs Company','V','https://www.themyersbriggs.com/','官网确认学习发展测评；未核岗位预测效果'),
('Lightcast','V','https://lightcast.io/','官网确认劳动力市场情报；未核完整覆盖与准确率'),
('Eightfold','V','https://eightfold.ai/','官网确认人才智能平台；未核独立效果'),
('Gloat','V','https://gloat.com/','官网确认HR与人员配置平台；未核独立效果'),
('Plum','V','https://www.phenom.com/blog/phenom-acquires-plum','Phenom官网2026-04-28声明收购Plum并介绍行为测评；不继承营销准确率数字'),
('Millennium Institute','V','https://www.millennium-institute.org/publications-and-reports','机构官方报告页确认iSDG模型研究；未执行模型或核实各国实施'),
('EUROMOD','P','https://euromod-web.jrc.ec.europa.eu/','确认欧盟官方项目入口与当前发布消息；主页未提供充分模型规格'),
('OpenFisca','V','https://openfisca.org/doc/','官方文档确认税收福利模拟与需要自行补充法规覆盖；未实跑'),
('PolicyEngine','V','https://www.policyengine.org/us','官网确认开源税收福利分析；所读入口是美国版，未扩展为全球覆盖'),
('REMI','V','https://www.remi.com/','官网确认经济政策模拟、PI+等模型及咨询；未核预测效果'),
('Simudyne','V','https://simudyne.com/','官网确认企业模拟软件定位；未实跑'),
('Leadership Connect','V','https://leadershipconnect.io/','独立官网确认政府关系、利益相关者图谱和立法追踪；未确认与Altrata集团关系'),
]
p=OUT/'tables/03_sources_evidence/live_checks.tsv'
with p.open(encoding='utf-8-sig',newline='') as f: old=list(csv.DictReader(f,delimiter='\t'))
keys={r[0] for r in entries}
rows=[r for r in old if r['key'] not in keys]+[dict(zip(('key','status','url','verified_scope'),r)) for r in entries]
with p.open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=('key','status','url','verified_scope'),delimiter='\t');w.writeheader();w.writerows(rows)
p=OUT/'tables/02_catalogue_extraction/catalogue_seed.tsv'
with p.open(encoding='utf-8-sig',newline='') as f: seeds=list(csv.DictReader(f,delimiter='\t'))
for r in seeds:
 if r['name']=='Altrata / BoardEx / Boardroom Insiders / Leadership Connect':
  r['name']='Altrata / BoardEx / Boardroom Insiders'
  r['aliases']='Altrata|BoardEx|Boardroom Insiders'
  r['role']='高管与董事关系资料；已核Altrata定位，旗下各品牌归属仍待逐项核对'
 if r['name']=='Plum':r['role']='人才行为测评；Phenom官网声明已收购，不继承其营销效果数字'
if not any(r['name']=='Leadership Connect' for r in seeds):
 seeds.append(dict(category='关系图谱与企业情报',name='Leadership Connect',aliases='Leadership Connect',role='政府关系、利益相关者图谱和立法追踪；单列核验，不与Altrata合并归属'))
with p.open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=seeds[0].keys(),delimiter='\t');w.writeheader();w.writerows(seeds)
print('Added checks:',len(entries),'Total checks:',len(rows),'Seeds:',len(seeds))
