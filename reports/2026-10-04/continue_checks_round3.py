from pathlib import Path
import csv
o=Path(__file__).resolve().parent
new=[
('Truity','V','https://www.truity.com/','官网确认性格与职业测评；未核独立效度'),
('16Personalities','V','https://www.16personalities.com/','官网确认性格测评与建议；不据此证明岗位预测效度'),
('Apply Magic Sauce','P','https://www.applymagicsauce.com/','入口未能读取；功能与当前可用性仍待核'),
('Personos.ai','P','https://personos.ai/','入口未能读取；同名实体及当前产品仍待核'),
('Social Science Automation','P','https://www.socialscience.net/','入口未能读取；Profiler Plus现行可用性仍待核'),
('FARI','V','https://www.fari.brussels/','官方页确认公共利益AI研究机构；不当作普通商业咨询公司'),
('Harvard Growth Lab','P','https://atlas.hks.harvard.edu/','本次入口未能读取；Atlas现行功能仍待核'),
('EU Knowledge4Policy','V','https://knowledge-for-policy.ec.europa.eu/home_en','欧盟官方知识政策入口；不当作商业策略公司'),
('Esri','V','https://www.esri.com/en-us/arcgis/products/arcgis-urban/overview','官方页确认ArcGIS Urban规划设计软件；未实跑或核价格'),
('OpenCorporates','V','https://opencorporates.com/','官网确认法人实体数据、核验及尽调用途；不继承全部覆盖数字'),
('CB Insights','P','https://www.cbinsights.com/','官网403；未完成业务现况核实'),
('Tracxn','V','https://tracxn.com/','官网确认创投及企业发展数据服务；未核完整覆盖及准确率'),
('Preqin','V','https://www.preqin.com/','官网确认私募市场数据并标示BlackRock旗下；未独立核数据效果'),
('PEMANDU','V','https://pemandu.org/','官网确认战略工作坊、Lab、交付单位与PMO支持；未证明唯一可及、会面保证或方法完整复制'),
]
p=o/'live_checks.tsv'
with p.open(encoding='utf-8-sig',newline='') as f:r=list(csv.DictReader(f,delimiter='\t'))
keys={x[0] for x in new};r=[x for x in r if x['key'] not in keys]+[dict(zip(('key','status','url','verified_scope'),x)) for x in new]
with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=r[0].keys(),delimiter='\t');w.writeheader();w.writerows(r)
print('Reviewed:',len(new),'Total ledger:',len(r))
