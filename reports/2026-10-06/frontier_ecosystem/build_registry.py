"""Rebuild the reviewed frontier index and report from explicitly curated records.
No network requests. VERIFIED refers only to the stated public description.
"""
from pathlib import Path
import csv, json, re, hashlib
from collections import Counter

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'Reference/tables/06_frontier_ecosystem_20261006'
OUT.mkdir(parents=True, exist_ok=True)
DATE = '2026-10-06'
# domain|organization|country candidate|type|product/project leads|reviewed claim|source|state
DATA = '''GEOPOLITICS|RAND|US|RESEARCH_ORG|政策研究、FFRDC|公开开展政策、国家安全与国际事务研究|https://www.rand.org/about.html|VERIFIED
GEOPOLITICS|IISS|GB|THINK_TANK|The Military Balance、Strategic Survey|UNKNOWN：本轮页面仅返回 iframe，产品与覆盖待核实|https://www.iiss.org/about-us/|UNKNOWN
GEOPOLITICS|SIPRI|SE|RESEARCH_ORG|军费、军贸数据库与年鉴|公开开展冲突、军备与裁军研究|https://www.sipri.org/about|VERIFIED
GEOPOLITICS|CSIS|US|THINK_TANK|国际安全与政策研究|官网公开发布国际政策与安全研究|https://www.csis.org/|VERIFIED
GEOPOLITICS|Chatham House|GB|THINK_TANK|国际事务研究|官网公开发布国际事务研究|https://www.chathamhouse.org/|VERIFIED
GEOPOLITICS|HCSS|NL|THINK_TANK|战略研究、GINA 线索|官网公开提供战略研究|https://hcss.nl/|VERIFIED
GEOPOLITICS|ACLED|US|NONPROFIT|冲突与抗议事件数据|公开描述全球政治暴力与抗议数据分析|https://acleddata.com/about-acled|VERIFIED
GEOPOLITICS|GDELT Project||PROJECT|新闻事件数据库|公开提供全球新闻与事件数据项目|https://gdeltproject.org/|VERIFIED
STRATEGY|Janes|GB|COMPANY|国防情报数据库|官网描述开源国防与安全情报服务|https://www.janes.com/|VERIFIED
STRATEGY|RANE|US|COMPANY|风险情报平台、Stratfor 线索|官网描述企业风险情报服务|https://www.ranenetwork.com/|VERIFIED
STRATEGY|Control Risks|GB|COMPANY|地缘风险、尽调与咨询|官网描述全球风险咨询服务|https://www.controlrisks.com/|VERIFIED
STRATEGY|Recorded Future|US|COMPANY|威胁情报、MCP 接口线索|官网描述网络威胁情报服务；MCP 发布日未在本轮核实|https://www.recordedfuture.com/|VERIFIED
STRATEGY|Govini|US|COMPANY|Ark|UNKNOWN：访问原域名转向 air.ai，不能据此确认 Ark 当前产品状态|https://www.govini.com/|UNKNOWN
STRATEGY|Roke Manor Research|GB|COMPANY|Crucible|UNKNOWN：参考档产品线索待一手核实|https://www.roke.co.uk/|UNKNOWN
STRATEGY|BMI / GeoQuant||BUSINESS_UNIT|国别风险、量化地缘风险|UNKNOWN：提供方与产品关系待核实|https://www.fitchsolutions.com/|UNKNOWN
STRATEGY|Bellingcat|NL|NONPROFIT|开源调查与工具集|UNKNOWN：参考档线索待核实|https://www.bellingcat.com/|UNKNOWN
STRATEGY|Maltego|DE|COMPANY|OSINT 关系分析|官网描述开源情报与网络调查平台|https://www.maltego.com/|VERIFIED
STRATEGY|i2 Group||COMPANY|Analyst's Notebook|产品页描述实体关系与可视分析；官方说明2022年由Harris从IBM收购|https://i2group.com/solutions/i2-analysts-notebook|VERIFIED
STRATEGY|Meteomatics|CH|COMPANY|天气数据 API、气象情报|官网描述气象情报服务|https://www.meteomatics.com/|VERIFIED
STRATEGY|中科闻歌|CN|COMPANY|DIP、DOMA、Decitron|UNKNOWN：沿用旧批线索，本轮未复核|https://www.wenge.com/|UNKNOWN
STRATEGY|Earthian AI||UNRESOLVED|地缘风险 AI 线索|UNKNOWN：名称、法人和性能均待核实||UNKNOWN
STRATEGY|NERAI||UNRESOLVED|地缘风险 AI 线索|UNKNOWN：名称、法人和性能均待核实||UNKNOWN
DEFENSE|Palantir Technologies|US|COMPANY|Gotham、Foundry、AIP、Apollo、Maven、TITAN、Warp Core|Gotham公开描述国防情报融合与决策支持；不能外推具体部署栈|https://www.palantir.com/platforms/gotham/|VERIFIED
DEFENSE|Anduril Industries|US|COMPANY|Lattice、Menace|公开描述传感器与系统连接的指挥控制平台|https://www.anduril.com/lattice/command-and-control|VERIFIED
DEFENSE|Systematic|DK|COMPANY|SitaWare、IRIS、EWare|SitaWare产品页描述多域C4ISR；不等于北约规范标准|https://systematic.com/int/industries/defence/products/sitaware-suite/|VERIFIED
DEFENSE|Lockheed Martin|US|GROUP|C2BMC、CommandIQ、AIR6500、DIAMONDShield|C2BMC产品页描述指挥控制与战斗管理|https://www.lockheedmartin.com/en-us/products/command-control-battle-management-communications-c2bmc.html|VERIFIED
DEFENSE|Northrop Grumman|US|GROUP|IBCS、航天与传感器线索|官网公开航空、防务与太空业务|https://www.northropgrumman.com/|VERIFIED
DEFENSE|RTX|US|GROUP|Raytheon、Collins Aerospace、Pratt & Whitney|官网公开航空与防务业务|https://www.rtx.com/|VERIFIED
DEFENSE|BAE Systems|GB|GROUP|GXP、SOCET GXP、RAD 系列、BISim 线索|官网公开防务技术业务；逐款型号待核实|https://www.baesystems.com/en|VERIFIED
DEFENSE|L3Harris Technologies|US|GROUP|战术通信、航天与传感器|官网公开防务技术业务|https://www.l3harris.com/|VERIFIED
DEFENSE|General Dynamics|US|GROUP|任务系统、通信与平台|UNKNOWN：本轮访问失败|https://www.gd.com/|UNKNOWN
DEFENSE|Thales|FR|GROUP|防务、航天、通信、Luna|Athea官方材料确认Thales为合作方；其他型号本轮待核实|https://athea.tech/|VERIFIED
DEFENSE|Leonardo|IT|GROUP|航空、防务与安全|官网公开航空、防务与安全业务|https://www.leonardo.com/en/|VERIFIED
DEFENSE|Airbus|FR|GROUP|Defence and Space、Skywise、Pléiades Neo|防务官网公开防务业务；不将整个集团归为单一法国法人|https://www.airbus.com/en/products-services/defence|VERIFIED
DEFENSE|Boeing|US|GROUP|Defense Space & Security|官网公开防务与航天业务|https://www.boeing.com/defense|VERIFIED
DEFENSE|Saab|SE|GROUP|传感器、平台与任务系统|官网公开防务业务；不是Athea合作方证据|https://www.saab.com/|VERIFIED
DEFENSE|Helsing|DE|COMPANY|防务AI、Centaur、HX-2 线索|官网描述防务AI，并披露与Mistral合作|https://helsing.ai/company|VERIFIED
DEFENSE|Athea|FR|JOINT_VENTURE|主权大数据平台|官方明确由Thales与Eviden支持的主权大数据方案|https://athea.tech/|VERIFIED
DEFENSE|Eviden|FR|BUSINESS_UNIT|任务关键系统、Athea|官方任务关键系统页列出Athea|https://eviden.com/en/products/mission-critical-systems|VERIFIED
DEFENSE|Elbit Systems|IL|GROUP|C4ISR、电子与无人系统|官网公开防务技术业务|https://www.elbitsystems.com/|VERIFIED
DEFENSE|Israel Aerospace Industries|IL|GROUP|航空、航天与防务系统|官网公开航空航天与防务业务|https://www.iai.co.il/|VERIFIED
DEFENSE|ST Engineering|SG|GROUP|航空、数字与防务服务|UNKNOWN：本轮访问失败|https://www.stengg.com/|UNKNOWN
DEFENSE|中国航天科工集团 CASIC|CN|GROUP|航天与防务系统|UNKNOWN：本轮访问失败|https://www.casic.com.cn/|UNKNOWN
DEFENSE|中国电子科技集团 CETC|CN|GROUP|电子与信息系统|UNKNOWN：本轮访问失败|https://www.cetc.com.cn/|UNKNOWN
DEFENSE|中国航空工业集团 AVIC|CN|GROUP|航空工业|UNKNOWN：本轮访问失败|https://www.avic.com/|UNKNOWN
DEFENSE|中国兵器工业集团 NORINCO Group|CN|GROUP|陆地装备与防务|UNKNOWN：本轮访问失败|https://www.norincogroup.com.cn/|UNKNOWN
DEFENSE|Rostec|RU|GROUP|工业与防务|UNKNOWN：未在本轮核实|https://rostec.ru/|UNKNOWN
DEFENSE|Rheinmetall|DE|GROUP|车辆、传感器与防务|UNKNOWN：补充研究候选，未核实|https://www.rheinmetall.com/|UNKNOWN
DEFENSE|HENSOLDT|DE|COMPANY|防务传感器|UNKNOWN：补充候选，逐项能力未核实|https://www.hensoldt.net/|UNKNOWN
DEFENSE|Hanwha Aerospace|KR|GROUP|航空与防务|UNKNOWN：补充研究候选，未核实|https://www.hanwhaaerospace.com/|UNKNOWN
DEFENSE|国立中山科学研究院|TW|RESEARCH_ORG|防务研发|UNKNOWN：参考档线索待核实|https://www.ncsist.org.tw/|UNKNOWN
DEFENSE|汉翔航空工业|TW|COMPANY|航空研发与制造|UNKNOWN：参考档线索待核实|https://www.aidc.com.tw/|UNKNOWN
DEFENSE|乌克兰国防部|UA|PUBLIC_BODY|Delta|UNKNOWN：Delta版本、部署与架构须另取官方项目证据|https://mod.gov.ua/|UNKNOWN
DEFENSE|HADES / HDS FUSION||UNRESOLVED|多域C4ISR|UNKNOWN：参考档名称与提供方法人待消歧||UNKNOWN
SPACE|NASA|US|PUBLIC_BODY|cFS、GMAT、OpenMDAO、VEDA|官网公开航天探索与科研任务；框架逐项证据须分开|https://www.nasa.gov/|VERIFIED
SPACE|NASA JPL|US|RESEARCH_ORG|F Prime、SPICE|官网公开行星探索研究；是机构条目，不是独立集团|https://www.jpl.nasa.gov/|VERIFIED
SPACE|ESA||INTERGOVERNMENTAL|航天科学与任务|官网公开多国航天任务；不得编码为一个ISO国家|https://www.esa.int/|VERIFIED
SPACE|DLR|DE|RESEARCH_ORG|航天、航空与研究|官网公开航空航天研究|https://www.dlr.de/en|VERIFIED
SPACE|CNES|FR|PUBLIC_BODY|航天任务与研究|官网公开航天任务与研究|https://cnes.fr/|VERIFIED
SPACE|JAXA|JP|PUBLIC_BODY|航天航空研发与任务|官网公开航天航空研发|https://www.jaxa.jp/|VERIFIED
SPACE|ISRO|IN|PUBLIC_BODY|航天研发与任务|官网公开航天任务|https://www.isro.gov.in/|VERIFIED
SPACE|KARI|KR|RESEARCH_ORG|航空航天研发|官网公开航空航天研究|https://www.kari.re.kr/eng|VERIFIED
SPACE|中国航天科技集团 CASC|CN|GROUP|运载器、卫星与航天产业|官方业务页公开卫星应用与航天产业业务|https://www.spacechina.com/n25/n146/|VERIFIED
SPACE|CNSA|CN|PUBLIC_BODY|航天管理与任务|UNKNOWN：补充候选，未在本轮核实|https://www.cnsa.gov.cn/|UNKNOWN
SPACE|Roscosmos|RU|PUBLIC_BODY|航天任务|UNKNOWN：参考档线索，本轮未核实|https://www.roscosmos.ru/|UNKNOWN
SPACE|SpaceX|US|COMPANY|Falcon、Dragon、Starlink、Starship|UNKNOWN：首页无可读文本；内部栈与在轨节点数未核实|https://www.spacex.com/|UNKNOWN
SPACE|Blue Origin|US|COMPANY|New Glenn、New Shepard|官网公开航天运输与系统业务|https://www.blueorigin.com/|VERIFIED
SPACE|Rocket Lab|US|GROUP|Electron、Neutron、航天系统|官网公开发射与航天系统业务|https://rocketlabcorp.com/|VERIFIED
SPACE|OHB|DE|GROUP|卫星与航天系统|UNKNOWN：参考档线索待核实|https://www.ohb.de/|UNKNOWN
SPACE|Isar Aerospace|DE|COMPANY|Spectrum|UNKNOWN：参考档线索待核实|https://www.isaraerospace.com/|UNKNOWN
SPACE|Orbex|GB|COMPANY|Prime|UNKNOWN：参考档线索待核实|https://orbex.space/|UNKNOWN
SPACE|蓝箭航天 LandSpace|CN|COMPANY|朱雀系列|UNKNOWN：参考档线索待核实|https://www.landspace.com/|UNKNOWN
SPACE|星河动力 Galactic Energy|CN|COMPANY|谷神星、智神星|UNKNOWN：参考档线索待核实|https://www.galactic-energy.cn/|UNKNOWN
SPACE|COMSPOC|US|COMPANY|SSASuite|官网公开空间态势业务；精度与部署须产品级证据|https://www.comspoc.com/|VERIFIED
SPACE|GMV|ES|GROUP|Ecosstm|官方产品页描述SSA/SST/SDA/STM及编目、碰撞分析|https://www.gmv.com/en/products/space/ecosstm|VERIFIED
SPACE|LeoLabs|US|COMPANY|轨道监测与情报|官网公开轨道情报服务|https://leolabs.space/|VERIFIED
SPACE|Slingshot Aerospace|US|COMPANY|空间运营情报|官网公开空间运营情报服务|https://www.slingshot.space/|VERIFIED
SPACE|Neuraspace|PT|COMPANY|空间交通管理|官网公开空间交通管理服务|https://www.neuraspace.com/|VERIFIED
SPACE|OKAPI:Orbits|DE|COMPANY|轨道运营与交通管理|官网公开轨道运营服务|https://www.okapiorbits.space/en|VERIFIED
SPACE|Saber Astronautics||COMPANY|Space Cockpit、WINDU、Singularity|官网公开空间运营业务；产品与2026发布日期待核实|https://www.saberastro.com/|VERIFIED
SPACE|Aldoria|FR|COMPANY|空间监测|UNKNOWN：本轮访问失败|https://www.aldoria.com/|UNKNOWN
SPACE|ExoAnalytic Solutions|US|COMPANY|光学空间监测|UNKNOWN：本轮访问失败|https://www.exoanalytic.com/|UNKNOWN
SPACE|a.i. solutions|US|COMPANY|FreeFlyer|UNKNOWN：参考档线索待核实|https://ai-solutions.com/|UNKNOWN
GEOINT|Esri|US|COMPANY|ArcGIS Pro、Enterprise、AllSource、Defense Mapping|国防产品页公开军事GIS应用|https://www.esri.com/en-us/industries/defense/overview|VERIFIED
GEOINT|Planet Labs|US|COMPANY|PlanetScope、SkySat|官网公开卫星影像与地球数据分析|https://www.planet.com/|VERIFIED
GEOINT|ICEYE|FI|COMPANY|SAR影像与分析|官网公开SAR与地球观测服务|https://www.iceye.com/|VERIFIED
GEOINT|BlackSky|US|COMPANY|Spectra|官网公开空间情报业务；具体刷新率未核实|https://blacksky.com/|VERIFIED
GEOINT|Capella Space|US|COMPANY|SAR地球观测|官网公开全天候地球情报业务|https://www.capellaspace.com/|VERIFIED
GEOINT|HawkEye 360|US|COMPANY|RF空间情报|UNKNOWN：本轮访问失败|https://www.hawkeye360.com/|UNKNOWN
GEOINT|Maxar / Vantor|US|UNRESOLVED|WorldView Legion|UNKNOWN：参考档混用品牌，须分辨改名、资产与法人关系|https://www.maxar.com/|UNKNOWN
GEOINT|Hexagon|SE|GROUP|ERDAS IMAGINE、Luciad|UNKNOWN：参考档线索，本轮未核实|https://hexagon.com/|UNKNOWN
GEOINT|NV5 Geospatial|US|BUSINESS_UNIT|ENVI|UNKNOWN：当前归属与产品状态待核实|https://www.nv5geospatialsoftware.com/|UNKNOWN
AI|OpenAI|US|COMPANY|基础模型与AI研究|官方About页公开AI研究定位；不证明涉密部署|https://openai.com/about/|VERIFIED
AI|Google DeepMind|GB|BUSINESS_UNIT|Gemini、科学AI与机器人研究|官网公开AI模型与科研业务；具体版本性能未比较|https://deepmind.google/|VERIFIED
AI|Anthropic|US|COMPANY|Claude、模型研究与安全|官网公开AI模型业务|https://www.anthropic.com/|VERIFIED
AI|Mistral AI|FR|COMPANY|基础模型与企业AI|官网公开模型与主权AI服务|https://mistral.ai/|VERIFIED
AI|Meta AI|US|BUSINESS_UNIT|Llama、AI研究|UNKNOWN：本轮页面未取得足够可读内容|https://ai.meta.com/|UNKNOWN
AI|NVIDIA|US|COMPANY|GPU、AI软件、Omniverse、Earth-2|官网公开AI平台业务；具体装备采用未知|https://www.nvidia.com/en-us/ai/|VERIFIED
AI|Microsoft Research|US|RESEARCH_ORG|AI与计算研究|官网公开计算与技术研究|https://www.microsoft.com/en-us/research/|VERIFIED
AI|DeepSeek|CN|COMPANY|基础模型|官网公开模型与服务入口；性能未独立核实|https://www.deepseek.com/|VERIFIED
AI|Alibaba / Qwen|CN|BUSINESS_UNIT|Qwen模型|UNKNOWN：本轮入口访问失败|https://www.qwen.ai/|UNKNOWN
AI|xAI|US|COMPANY|Grok|UNKNOWN：入口显示SpaceXAI，当前法人归属与品牌须另核实|https://x.ai/|UNKNOWN
AI|Allen Institute for AI|US|RESEARCH_ORG|开放AI研究|UNKNOWN：ai2.org访问失败，不把孵化器网站当作研究院|https://ai2.org/|UNKNOWN
AI|Stanford HAI|US|UNIVERSITY_UNIT|以人为本AI研究|官网公开人本AI研究与政策活动|https://hai.stanford.edu/|VERIFIED
AI|MIT CSAIL|US|UNIVERSITY_UNIT|计算与AI研究|官网公开计算科学与AI研究|https://www.csail.mit.edu/|VERIFIED
AI|Berkeley BAIR|US|UNIVERSITY_UNIT|AI研究|UNKNOWN：本轮无可读文本|https://bair.berkeley.edu/|UNKNOWN
AI|Alan Turing Institute|GB|RESEARCH_ORG|数据科学与AI研究|官网公开数据科学与AI研究|https://www.turing.ac.uk/|VERIFIED
AI|Inria|FR|RESEARCH_ORG|数字科学与AI研究|UNKNOWN：本轮受到访问挑战|https://www.inria.fr/en|UNKNOWN
PUBLIC_RESEARCH|DARPA|US|PUBLIC_BODY|公开研发项目|官网公开先进研发项目；项目阶段须另取证|https://www.darpa.mil/|VERIFIED
PUBLIC_RESEARCH|LLNL|US|RESEARCH_ORG|国家安全科学、JCATS线索|官网公开国家安全与科学研究；JCATS需项目页|https://www.llnl.gov/|VERIFIED
PUBLIC_RESEARCH|AFRL|US|RESEARCH_ORG|AFSIM|UNKNOWN：本轮访问失败|https://www.afrl.af.mil/|UNKNOWN
PUBLIC_RESEARCH|US Naval Research Laboratory|US|RESEARCH_ORG|海军科研|UNKNOWN：本轮访问失败|https://www.nrl.navy.mil/|UNKNOWN
PUBLIC_RESEARCH|NATO||INTERGOVERNMENTAL|FMN、STANAG、公开研发|官网公开多国联盟活动；联盟标准须逐份核实|https://www.nato.int/en|VERIFIED
PUBLIC_RESEARCH|US Department of Defense|US|PUBLIC_BODY|公开采购与研发项目|UNKNOWN：参考档线索，项目独立取证|https://www.defense.gov/|UNKNOWN
PUBLIC_RESEARCH|US Space Force|US|PUBLIC_BODY|ATLAS、UDL、Space-Track|UNKNOWN：具体项目、承包方与当前状态待核实|https://www.spaceforce.mil/|UNKNOWN
PUBLIC_RESEARCH|DIA|US|PUBLIC_BODY|MARS|UNKNOWN：项目线索待核实|https://www.dia.mil/|UNKNOWN
PUBLIC_RESEARCH|NGA|US|PUBLIC_BODY|GEOINT|UNKNOWN：参考档线索待核实|https://www.nga.mil/|UNKNOWN
PUBLIC_RESEARCH|NRO|US|PUBLIC_BODY|公开航天侦察项目|UNKNOWN：不得据机构名称推断产品栈|https://www.nro.gov/|UNKNOWN
PUBLIC_RESEARCH|ODNI|US|PUBLIC_BODY|公开情报治理文件|UNKNOWN：参考档线索待核实|https://www.dni.gov/|UNKNOWN
PUBLIC_RESEARCH|NSA|US|PUBLIC_BODY|公开科研与标准|UNKNOWN：不得据机构名称推断产品栈|https://www.nsa.gov/|UNKNOWN
PUBLIC_RESEARCH|GCHQ|GB|PUBLIC_BODY|公开研究与安全|UNKNOWN：参考档线索待核实|https://www.gchq.gov.uk/|UNKNOWN
PUBLIC_RESEARCH|DGSE|FR|PUBLIC_BODY|公开机构职责|UNKNOWN：参考档线索待核实|https://www.dgse.gouv.fr/|UNKNOWN
PUBLIC_RESEARCH|以色列8200部队|IL|MILITARY_UNIT|公开项目线索|UNKNOWN：单位公开资料与项目须分别取证||UNKNOWN
ENGINEERING|Synopsys / Ansys|US|GROUP|STK、ODTK、SCADE、ModelCenter、Twin Builder|STK官方产品页描述数字任务工程；2025-07-17收购已完成|https://ansys.synopsys.com/products/missions/ansys-stk|VERIFIED
ENGINEERING|Dassault Systèmes|FR|GROUP|CATIA、3DEXPERIENCE|官方产业页描述航空航天与防务工程软件|https://www.3ds.com/industries/aerospace-defense|VERIFIED
ENGINEERING|Siemens|DE|GROUP|NX、Teamcenter、Altair PBS|UNKNOWN：本轮目标页面失败，产品归属另核实|https://www.sw.siemens.com/|UNKNOWN
ENGINEERING|PTC|US|COMPANY|Windchill|UNKNOWN：参考档线索待核实|https://www.ptc.com/|UNKNOWN
ENGINEERING|MathWorks|US|COMPANY|MATLAB、Simulink、Stateflow|UNKNOWN：参考档线索待核实|https://www.mathworks.com/|UNKNOWN
ENGINEERING|BISim|US|COMPANY|VBS4、VBS Blue IG|UNKNOWN：独立运营实体与母集团关系待核实|https://bisimulations.com/|UNKNOWN
ENGINEERING|WarfareSims||COMPANY|Command Professional Edition|UNKNOWN：产品与提供方关系待核实|https://www.warfaresims.com/|UNKNOWN
ENGINEERING|Rolands & Associates|US|COMPANY|JTLS|UNKNOWN：参考档JTLS提供方补充候选|https://www.rolands.com/|UNKNOWN
ENGINEERING|Simulation & Analysis Center / SPA|US|UNRESOLVED|GCAM、Cyber Assassin|UNKNOWN：参考档缩写与提供方须消歧||UNKNOWN
INFRASTRUCTURE|Green Hills Software|US|COMPANY|INTEGRITY-178、tuMP|UNKNOWN：具体平台与认证版本待核实|https://www.ghs.com/|UNKNOWN
INFRASTRUCTURE|Lynx|US|COMPANY|MOSA.ic、LynxSecure|UNKNOWN：具体平台与认证版本待核实|https://www.lynx.com/|UNKNOWN
INFRASTRUCTURE|Wind River|US|COMPANY|VxWorks、VxWorks 653|UNKNOWN：具体平台与认证版本待核实|https://www.windriver.com/|UNKNOWN
INFRASTRUCTURE|SYSGO|DE|COMPANY|PikeOS|UNKNOWN：具体平台与认证版本待核实|https://www.sysgo.com/|UNKNOWN
INFRASTRUCTURE|Trustworthy Systems / seL4 Foundation||RESEARCH_COMMUNITY|seL4|UNKNOWN：研究团队、基金会与认证对象应分别建实体|https://sel4.systems/|UNKNOWN
INFRASTRUCTURE|RTEMS Project||PROJECT|RTEMS|UNKNOWN：具体任务部署待核实|https://www.rtems.org/|UNKNOWN
INFRASTRUCTURE|QNX / BlackBerry|CA|BUSINESS_UNIT|QNX|UNKNOWN：当前业务归属与认证版本待核实|https://www.qnx.com/|UNKNOWN
INFRASTRUCTURE|Concurrent Real-Time|US|COMPANY|RedHawk Linux|UNKNOWN：版本与发布日未核实|https://www.concurrent-rt.com/|UNKNOWN
INFRASTRUCTURE|OpenC3|US|COMPANY|COSMOS|UNKNOWN：公开地面系统线索待核实|https://openc3.com/|UNKNOWN
INFRASTRUCTURE|Microchip Technology|US|COMPANY|SAMRH|UNKNOWN：产品与任务部署待核实|https://www.microchip.com/|UNKNOWN
INFRASTRUCTURE|Frontgrade Gaisler|SE|COMPANY|LEON处理器|UNKNOWN：原文Cobham Gaisler历史名称须另核实|https://www.gaisler.com/|UNKNOWN
INFRASTRUCTURE|AMD|US|COMPANY|Versal、Alveo|UNKNOWN：具体任务采用待核实|https://www.amd.com/|UNKNOWN
INFRASTRUCTURE|Intel / Altera|US|UNRESOLVED|FPGA、PAC|UNKNOWN：当前法人及资产归属须分开核实|https://www.altera.com/|UNKNOWN
INFRASTRUCTURE|Getac|TW|COMPANY|加固终端|UNKNOWN：参考档线索待核实|https://www.getac.com/|UNKNOWN
INFRASTRUCTURE|Panasonic|JP|GROUP|Toughbook|UNKNOWN：参考档线索待核实|https://connect.panasonic.com/|UNKNOWN
INFRASTRUCTURE|Utimaco|DE|COMPANY|HSM|UNKNOWN：参考档线索待核实|https://utimaco.com/|UNKNOWN
INFRASTRUCTURE|Oracle|US|GROUP|OCI、Roving Edge|UNKNOWN：具体Lattice部署与产品授权待核实|https://www.oracle.com/|UNKNOWN
INFRASTRUCTURE|AWS|US|BUSINESS_UNIT|GovCloud|UNKNOWN：区域、服务与授权边界须另核实|https://aws.amazon.com/govcloud-us/|UNKNOWN
INFRASTRUCTURE|Microsoft|US|GROUP|Azure Government、Sentinel|UNKNOWN：服务、区域、授权与部署须分别核实|https://azure.microsoft.com/|UNKNOWN
INFRASTRUCTURE|IBM|US|GROUP|watsonx、研究与计算|UNKNOWN：本輪读取量子页不足以证明AI产品条目|https://www.ibm.com/|UNKNOWN
INFRASTRUCTURE|Databricks|US|COMPANY|数据与AI平台|UNKNOWN：国防项目采用待核实|https://www.databricks.com/|UNKNOWN
INFRASTRUCTURE|Snowflake|US|COMPANY|数据云、政府服务|UNKNOWN：国防项目采用待核实|https://www.snowflake.com/|UNKNOWN
INFRASTRUCTURE|SAP|DE|GROUP|企业与供应链系统|UNKNOWN：国防项目采用待核实|https://www.sap.com/|UNKNOWN
INFRASTRUCTURE|华为|CN|GROUP|工业数字与AI平台|UNKNOWN：旧批线索未在本轮复核|https://www.huawei.com/|UNKNOWN
INFRASTRUCTURE|C3 AI|US|COMPANY|企业AI|UNKNOWN：合同与具体部署待核实|https://c3.ai/|UNKNOWN
INFRASTRUCTURE|Scale AI|US|COMPANY|数据、评估与AI服务|UNKNOWN：合同与具体部署待核实|https://scale.com/|UNKNOWN
INFRASTRUCTURE|Sift|US|COMPANY|工程遥测分析|UNKNOWN：不可将其直接写为SpaceX自研|https://www.siftstack.com/|UNKNOWN
INFRASTRUCTURE|Eutelsat Group|FR|GROUP|卫星通信与遥测|UNKNOWN：600+卫星及InfluxDB性能数字未核实|https://www.eutelsat.com/|UNKNOWN
INFRASTRUCTURE|InfluxData|US|COMPANY|InfluxDB、Telegraf|官网描述时序数据库与遥测分析；具体客户性能不外推|https://www.influxdata.com/|VERIFIED
INFRASTRUCTURE|Timescale / Tiger Data|US|COMPANY|TimescaleDB|原入口转向Tiger Data并公开时序PostgreSQL服务；法人改名另核实|https://www.tigerdata.com/|VERIFIED
INFRASTRUCTURE|QuestDB|GB|COMPANY|QuestDB|官网描述低延迟时序数据库；数值性能未独立测量|https://questdb.com/|VERIFIED
INFRASTRUCTURE|Apache Software Foundation|US|NONPROFIT|Airflow、Superset、ECharts、DolphinScheduler、IoTDB、Kafka、Flink、Spark、Iceberg|官网确认开源软件基金会；各项目归属与任务采用需独立核实|https://www.apache.org/|VERIFIED
INFRASTRUCTURE|OSGeo||NONPROFIT|GDAL、PROJ、QGIS、PostGIS、GeoServer|官网公开开源地理空间基金会；项目治理关系各自核实|https://www.osgeo.org/|VERIFIED
INFRASTRUCTURE|Grafana Labs|US|COMPANY|Grafana、可观测性平台|官网描述可观测性业务；渲染插件与军方部署未知|https://grafana.com/|VERIFIED
GEOINT|Cesium|US|COMPANY|CesiumJS、3D地理空间|官网描述3D地理空间平台；当前母集团关系另核实|https://cesium.com/|VERIFIED
INFRASTRUCTURE|SchedMD|US|COMPANY|Slurm|官网公开Slurm支持与开发服务|https://www.schedmd.com/|VERIFIED
INFRASTRUCTURE|Red Hat|US|COMPANY|OpenShift、Linux|官网公开企业开源技术服务；国防项目部署另核实|https://www.redhat.com/en|VERIFIED
INFRASTRUCTURE|Qualcomm|US|COMPANY|计算与处理器|官网公开计算技术业务；机智号型号与架构另核实|https://www.qualcomm.com/|VERIFIED
INFRASTRUCTURE|Texas Instruments|US|COMPANY|模拟与嵌入式处理器|官网公开模拟与嵌入式处理业务；具体航天采用待核实|https://www.ti.com/|VERIFIED
PUBLIC_RESEARCH|OGC||STANDARDS_ORG|地理空间开放标准|官网公开地理空间标准工作；标准版本逐份核实|https://www.ogc.org/|VERIFIED
PUBLIC_RESEARCH|CCSDS||STANDARDS_ORG|航天数据与通信标准|UNKNOWN：本轮访问失败|https://public.ccsds.org/|UNKNOWN
PUBLIC_RESEARCH|UNOOSA||PUBLIC_BODY|空间条约与公开登记|UNKNOWN：参考档线索，未在本轮核实|https://www.unoosa.org/|UNKNOWN
PUBLIC_RESEARCH|COSPAR||SCIENTIFIC_ORG|行星保护与科学研究|UNKNOWN：参考档线索，未在本轮核实|https://cosparhq.cnes.fr/|UNKNOWN
PUBLIC_RESEARCH|NIST|US|PUBLIC_BODY|SP800系列、FIPS、密码与安全标准|UNKNOWN：标准版本与适用范围逐份核实|https://www.nist.gov/|UNKNOWN
INFRASTRUCTURE|StarRocks Project||PROJECT|StarRocks|官方功能页描述实时分析数据库；不证明某国军工部署|https://docs.starrocks.io/docs/introduction/Features/|VERIFIED
INFRASTRUCTURE|TAOS Data||COMPANY|TDengine|UNKNOWN：参考档线索待核实|https://www.tdengine.com/|UNKNOWN
PUBLIC_RESEARCH|清华大学|CN|UNIVERSITY_UNIT|IoTDB研究线索|UNKNOWN：研究团队、ASF项目与商业提供方不可混算|https://www.tsinghua.edu.cn/|UNKNOWN
PUBLIC_RESEARCH|北京邮电大学|CN|UNIVERSITY_UNIT|卫星与IoTDB线索|UNKNOWN：具体卫星任务与数据栈待核实|https://www.bupt.edu.cn/|UNKNOWN
INFRASTRUCTURE|ClickHouse|US|COMPANY|ClickHouse|UNKNOWN：任务采用与企业法人待核实|https://clickhouse.com/|UNKNOWN
INFRASTRUCTURE|Redpanda|US|COMPANY|流数据平台|UNKNOWN：参考档线索待核实|https://www.redpanda.com/|UNKNOWN
INFRASTRUCTURE|Dagster Labs|US|COMPANY|Dagster|UNKNOWN：参考档线索待核实|https://dagster.io/|UNKNOWN
INFRASTRUCTURE|Plotly||COMPANY|Plotly、Dash|UNKNOWN：参考档线索待核实|https://plotly.com/|UNKNOWN
INFRASTRUCTURE|Salesforce|US|GROUP|Tableau|UNKNOWN：产品归属与任务采用待核实|https://www.salesforce.com/|UNKNOWN
INFRASTRUCTURE|Elastic||COMPANY|Elasticsearch、Kibana|UNKNOWN：参考档线索待核实|https://www.elastic.co/|UNKNOWN
INFRASTRUCTURE|Cisco / Splunk|US|GROUP|Splunk|UNKNOWN：法人、收购与产品层关系待核实|https://www.splunk.com/|UNKNOWN
INFRASTRUCTURE|CrowdStrike|US|COMPANY|Falcon|UNKNOWN：参考档线索待核实|https://www.crowdstrike.com/|UNKNOWN
INFRASTRUCTURE|MISP Project||PROJECT|威胁情报共享|UNKNOWN：治理组织与具体采用待核实|https://www.misp-project.org/|UNKNOWN
GEOINT|ADS-B Exchange||UNRESOLVED|航空数据|UNKNOWN：参考档提供方与数据覆盖待核实|https://www.adsbexchange.com/|UNKNOWN
GEOINT|MarineTraffic||UNRESOLVED|船舶与AIS数据|UNKNOWN：当前母集团与数据覆盖待核实|https://www.marinetraffic.com/|UNKNOWN
GEOINT|Liveuamap||UNRESOLVED|事件地图|UNKNOWN：来源与提供方身份待核实|https://liveuamap.com/|UNKNOWN
GEOINT|Sentinel Hub / Sinergise||UNRESOLVED|遥感数据接口|UNKNOWN：提供方、母集团与数据产品关系待核实|https://www.sentinel-hub.com/|UNKNOWN
SPACE|USGS|US|PUBLIC_BODY|Landsat与地球观测|UNKNOWN：NASA与USGS职责需项目级证据|https://www.usgs.gov/|UNKNOWN
DEFENSE|经纬航太|TW|COMPANY|无人系统|UNKNOWN：参考档线索待核实||UNKNOWN
DEFENSE|创未来|TW|COMPANY|通信与传感器线索|UNKNOWN：名称与法人待核实||UNKNOWN'''

def write_csv(name, rows):
    with (OUT/name).open('w', newline='', encoding='utf-8-sig') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

entities=[]; claims=[]; sources=[]
for i, line in enumerate(DATA.splitlines(), 1):
    domain, name, country, kind, products, claim, url, state=line.split('|')
    eid=f'FRO{i:04d}'; sid=f'FRS{i:04d}' if url else ''
    entities.append(dict(entity_id=eid,display_name=name,entity_type=kind,primary_domain=domain,
        country_candidate_iso_alpha2=country,country_assignment_status='EDITORIAL_CANDIDATE_NOT_LEGAL_DOMICILE',
        legal_entity_status='UNRESOLVED' if kind=='UNRESOLVED' else 'DISPLAY_ORG_NOT_LEGAL_REGISTRY_VERIFIED',
        selection_status='FRONTIER_RESEARCH_CANDIDATE_NOT_RANKED',source_id=sid,as_of=DATE))
    claims.append(dict(claim_id=f'FRC{i:04d}',entity_id=eid,claim=claim,evidence_state=state,
        verification_scope='PUBLIC_DESCRIPTION_ONLY' if state=='VERIFIED' else 'NOT_VERIFIED_IN_BATCH',
        product_project_leads=products,product_leads_state='UNKNOWN_UNLESS_EXPLICIT_IN_CLAIM',
        performance_state='UNKNOWN',deployment_state='UNKNOWN',regulatory_state='UNKNOWN',
        source_id=sid,reviewed_on=DATE))
    if url:
        sources.append(dict(source_id=sid,url=url,supports=claim,
            source_class='P0' if kind in {'PUBLIC_BODY','INTERGOVERNMENTAL','RESEARCH_ORG','UNIVERSITY_UNIT','PROJECT','NONPROFIT'} else 'P1',
            access_state='READABLE_SUPPORT' if state=='VERIFIED' else 'UNVERIFIED_SEE_CLAIM',
            checked_on=DATE if state=='VERIFIED' or '本轮' in claim or '本輪' in claim else '',
            published_on='',archive_state='NO_RAW_HTTP_ARCHIVE',license_state='UNKNOWN'))
write_csv('registry_frontier_organizations.csv',entities)
write_csv('registry_frontier_claims.csv',claims)
write_csv('registry_frontier_sources.csv',sources)

MASTER=ROOT/'Reference/tables/01_country_area/registry_country_area_iso3166_20261004_enhanced.csv'
countries=list(csv.DictReader(MASTER.open(encoding='utf-8-sig')))
assert len(countries)==249 and len({r['iso_alpha2'] for r in countries})==249
assert all(not e['country_candidate_iso_alpha2'] or e['country_candidate_iso_alpha2'] in {r['iso_alpha2'] for r in countries} for e in entities)
assert len({e['entity_id'] for e in entities})==len(entities)
assert all(c['source_id'] in {s['source_id'] for s in sources} for c in claims if c['evidence_state']=='VERIFIED')

REF=ROOT/'Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd'
raw=REF.read_text(encoding='utf-8-sig')
start='<!-- FRONTIER_REVIEW_20261006_START -->'; end='<!-- FRONTIER_REVIEW_20261006_END -->'
raw=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\s*', '', raw, flags=re.S)
audit=dict(document=str(REF.relative_to(ROOT)),line_count=len(raw.splitlines()),
    question_heading_count=len(re.findall(r'^# 提問',raw,re.M)),
    markdown_url_count=len(re.findall(r'\]\(https?://',raw)),
    expiring_url_occurrences=len(re.findall(r'X-Amz-(?:Signature|Expires)=',raw)),
    orphan_web_citation_occurrences=len(re.findall(r'cite',raw)),
    scope='Whole-file structural scan; substantive external review focuses on questions 39 and 40 and the aerospace report. Not all historical claims verified.')
note=f'''{start}
# 核實與校訂索引（2026-10-06） {{#sec-frontier-review}}

本檔是多模型問答工作底稿。模型相互重複、回答中自稱「P0/P1」、列出網址，均不等於已核實。**本輪完成全檔結構掃描，實質外部核實集中於提問卅九、卌及宇航報告；未宣稱全檔每項歷史主張均已查證。** 空白回答模板不計作證據。下列校訂優先於後文保留的原模型回答。

| 原文主張／用語 | 本輪審閱裁定 | 一手來源／後續要求 |
|---|---|---|
| Athea＝Helsing×Saab 合資 | 錯誤；Athea官方列Thales與Eviden | [Athea](https://athea.tech/) |
| IBM i2 作為現行提供方 | 名稱過時；官方說明2022年由Harris從IBM收購 | [i2官方說明](https://i2group.com/articles/2024-08-09pressrelease) |
| ITAR/EAR/CMMC＝中國起源軟件全面禁入美歐白名單 | 缺乏支持，撤回此一般斷言；須按物項、交易、用途、合同與司法管轄核實 | [BIS許可判定](https://www.bis.gov/licensing)、[DDTC](https://www.pmddtc.state.gov/ddtc_public)、[CMMC](https://www.acq.osd.mil/asda/dpc/cp/cyber/cmmc.html) |
| StarRocks只能秒級／上游不可能使用／百萬點必崩 | 無同負載測試，不能成立；OLAP用途與硬實時控制需分層 | [StarRocks功能](https://docs.starrocks.io/docs/introduction/Features/) |
| SitaWare是北約標準、ArcGIS幾乎覆蓋全部軍用GIS | 產品用途可核實；市場全面性與正式標準身份尚未核實 | [SitaWare](https://systematic.com/int/industries/defence/products/sitaware-suite/)、[Esri](https://www.esri.com/en-us/industries/defense/overview) |
| Ansys仍是獨立母集團 | 2025-07-17 Synopsys宣布完成收購；產品品牌與法人分開 | [收購公告](https://investors.ansys.com/news-releases/news-release-details/synopsys-completes-acquisition-ansys) |
| NASA VEDA採用Airflow | 官方NASA-IMPACT倉庫支持存在相關實作；不外推所有NASA任務或全行業採用率 | [官方倉庫](https://github.com/NASA-IMPACT/veda-data-airflow) |
| 2026收入、認證、發佈日、Eutelsat衛星數、SpaceX完整栈 | 本輪未逐項取得充分一手證據，維持UNKNOWN，不轉成已核實結論 | 後續按claim逐條核實 |
| 中俄全閉源／某國全部用一個栈／新加坡與馬來西亞合併 | 無法支持國家整體結論；每個組織與項目獨立登記 | ISO國家／地區FK＋組織＋項目＋claim |
| N0～N7國家能力等級 | 未有定義、可重現測試與項目證據，不填國家級分數；缺證不等於N0 | 神經技術另建registry_neurotechnology_global；本輪未進行神經技術普查 |

本輪逐機構索引、CSV及證據邊界見 [更新宇航報告](Aerospace_Ecosystem_Report.qmd) 與 [資料字典](tables/06_frontier_ecosystem_20261006/README.md)。VERIFIED只覆蓋具體claim的公開描述，不能連帶驗證產品線索、實際性能、軍方部署、监管许可或國家排名。全檔連結結構掃描見 [審閱回執](../reports/2026-10-06/frontier_ecosystem/review_receipt.json)，未聲稱全數URL均可訪問。

{end}

'''
front_end=raw.find('\n---',4)+len('\n---')
assert raw.startswith('---') and front_end>3
REF.write_text(raw[:front_end]+'\n\n'+note+raw[front_end:].lstrip('\n'),encoding='utf-8')

verified=sum(c['evidence_state']=='VERIFIED' for c in claims)
groups=Counter(e['primary_domain'] for e in entities)
header='''---
title: "世界前沿地緣戰略、軍工、宇航與人工智能生態登記報告"
subtitle: "OGDIL — 機構、能力主張與證據分層；ISO國家母表擴展接口"
author: "Ryo Eng（雷欧）"
date: 2026-10-06
lang: zh-TW
format:
  html:
    theme: cosmo
    toc: true
    toc-depth: 3
    number-sections: true
    embed-resources: true
    page-layout: full
  pdf:
    toc: true
execute:
  echo: false
---

## 研究範圍與可回答的問題

本輪以世界前沿研究與產業生態為入口，逐間列出公司、集團、組織、研究所與大學單位，涵蓋地緣研究、策略服務、軍工、宇航、GEOINT、AI及工程基礎設施。這是一份**可追溯研究登記冊，不是全球排名或全世界機構普查完成聲明**。同一集團的產品不冒充不同公司；研究所、政府機構和跨國組織也不混算為企業。

「世界級最前沿兼頂尖高端」以跨國研究／服務、公開前沿技術、全球關聯資料或專業任务系统作為候選篩選方向。只有官方描述支持的用途可寫為VERIFIED；各家的世界排名、性能優勢、軍方部署與採購資格本輪均未獨立比較。傳統軍工主承包商、前沿AI與自主系統公司、航天機構、資料服務及學術研究分層比較，不能用一個營收或模型分數統一排序。地方性、只在單國營運的條目保留為生態與原文覆蓋線索，不自動授予「頂尖」稱號。

本報告取代舊版未充分佐證的「更高維度」「霸主」「唯一重度重疊」「某國全部使用某栈」結論。參考問答檔是候選來源，不是一手資料；本輪核實採用政府、研究機構、供應商與官方開源倉庫。日期為查閱日期，不是每項主張的發布或生效日期。

## 證據規則

| 欄位／等級 | 精確含義 |
|---|---|
| VERIFIED | 已讀官方頁面支持本列具體公開描述；供應商自述不等於獨立測效 |
| UNKNOWN | 未核實、訪問失敗、證據不充分或名稱待消歧；不等於不存在或能力為零 |
| P0／P1 | 來源類別：公共／研究官方或供應商官方；與claim驗證狀態分開 |
| 產品／項目線索 | 研究入口；只有claim明確涵蓋的名稱可視作本輪已核實 |
| 國家候選 | 供後續ISO關聯的編輯定位，並非法定註冊地核驗或服務覆蓋清單 |
| performance／deployment／regulatory | 均維持UNKNOWN，後續按產品版本、任務、合同與證據逐項補齊 |

官網頁面無內容、訪問挑戰或域名轉向其他品牌時，不能把頁面存在當作能力證據。例如Govini入口轉向air.ai、SpaceX首頁無可讀文本，已明列UNKNOWN。沒有保存原始HTTP響應，文件SHA256只證明本批本地文件完整性，不證明網頁原文存檔。

## 參考檔與舊版報告的核對裁定

| 問題 | 校訂與核實依據 |
|---|---|
| Athea提供方寫成Helsing×Saab | 改為Thales與Eviden；[Athea官方](https://athea.tech/)明列合作方。Helsing、Saab另列機構 |
| IBM i2現行歸属 | 使用i2 Group；[官方2024說明](https://i2group.com/articles/2024-08-09pressrelease)確認2022年Harris從IBM收購 |
| Ansys母集團 | [官方公告](https://investors.ansys.com/news-releases/news-release-details/synopsys-completes-acquisition-ansys)確認2025-07-17完成收購；STK仍為產品品牌 |
| 起源國即決定全面禁用 | 撤回。ITAR涉及防務物項／服務與技術資料，EAR需判定物項及交易，CMMC為合同相關網絡安全要求；三者不能合併成所有美歐國防通用軟件黑名單。[DDTC](https://www.pmddtc.state.gov/ddtc_public)、[BIS](https://www.bis.gov/licensing)、[CMMC](https://www.acq.osd.mil/asda/dpc/cp/cyber/cmmc.html) |
| StarRocks秒級上限、百萬點必崩 | 撤回未測試數值；[官方功能頁](https://docs.starrocks.io/docs/introduction/Features/)定位為實時分析。是否適合特定遥测分析須測試寫入、p99時延與故障語義 |
| ECharts上萬通道必卡、Grafana必為WebGL | 無實測與具體渲染插件證據，不成立；應按點數、刷新率、瀏覽器、抽樣與引擎比較 |
| NASA VEDA採用Airflow | [NASA-IMPACT官方倉庫](https://github.com/NASA-IMPACT/veda-data-airflow)支持存在VEDA攝取實作；不能證明航空航天通用標配 |
| 用供應商合同名單否定開源庫使用 | 公司承包商名單與開源依賴清單粒度不同，無法據前者得出後者不存在 |
| SitaWare北約標準與跨國採用數 | 官方[產品頁](https://systematic.com/int/industries/defence/products/sitaware-suite/)支持C4ISR用途，未核實正式標準身份與原文各項2026里程碑 |
| SpaceX完整栈、Eutelsat600+、UDL日記錄量 | 缺少本輪具體一手證據；保持UNKNOWN，取消數值性能結論 |
| cFS、F Prime、COSMOS、RTOS混列 | 飛行軟件框架、地面指控與操作系統不同；NASA及OpenC3項目需各自版本與任務證據 |
| 中俄體制100%、國家單一栈、新馬合列 | 撤回整體概括。SG與MY分別關聯；無公開證據不能反推弱勢或全閉源 |
| 全年營收22億vs71.9億、最新MCP發布月 | 本輪不取用；須按具體日期與公司公告重新核實 |

參考檔新增優先校訂索引，保留原模型回答供溯源。全檔已作結構掃描；實質查證集中在提問卅九、卌與本報告，其他歷史主張仍須逐項審核。

## 按場景比較平台，避免虛構通用技術栈

| 場景 | 需要的能力 | 研究入口 | 必須另驗證 |
|---|---|---|---|
| 地緣戰略與風險 | 事件來源、可重現指標、情景與分析 | RAND、SIPRI、CSIS、HCSS、Janes、ACLED、RANE、Control Risks | 樣本偏差、覆蓋、修訂與資料許可 |
| 情報融合與指揮支持 | 實體、來源、權限、可審計工作流 | Palantir、Systematic、Anduril、Athea、i2、Esri | 實際任務部署、授權環境與人員監督 |
| 航天工程與任務分析 | 軌道、幾何、模型、誤差與接口 | Synopsys/Ansys、GMV、NASA、Dassault Systèmes | 模型適用性、版本、精度與驗收 |
| GEOINT與空间情报 | 光學／SAR／RF與來源時間 | Planet、ICEYE、Capella、BlackSky、LeoLabs、Slingshot | 解析度、延遲、重訪、錯誤率與再分發權 |
| AI研究與模型 | 推理、視覺、科學模型、評估與治理 | OpenAI、DeepMind、Anthropic、Mistral、DeepSeek、NVIDIA、大學研究單位 | 同條件基準、訓練許可、任務安全與漂移 |
| 遙測分析與數據管線 | 寫入、查詢、保留、回放、DQ | 時序庫／OLAP／流處理與Airflow按需求選型 | 同負載吞吐、p99時延、失效恢復與時序語義 |
| 安全關鍵控制 | 決定性、分區、WCET與认证 | RTOS、隔離內核與飛行框架候選 | 指定版本、目標硬件、認證範圍；不能用數倉基準代替 |

硬實時控制與地面分析的邊界由任務安全要求決定。數倉、GIS、模型和指揮平台可共存，不構成一條「高級／低級」替換鏈。Airflow可編排含HPC提交的工作流，但不取代PBS/Slurm資源調度。跨氣隙交付也須指定實際轉運與驗證機制，不能僅由pull/push判定可行。

## 逐機構登記索引

'''
report=header+f'本批登記 **{len(entities)} 個機構／項目候選**：**{verified}** 條公開描述為VERIFIED，**{len(entities)-verified}** 條為UNKNOWN。每列有獨立ID，所有候選均列出，無法讀取的來源保留待核實。此處產品列為線索，證據只覆蓋用途主張。\n\n'
labels={'GEOPOLITICS':'地緣研究與全球事件','STRATEGY':'策略服務與OSINT','DEFENSE':'軍工、指揮與防務AI','SPACE':'宇航機構、企業與空間態勢','GEOINT':'GEOINT與遥感','AI':'前沿AI與大學研究','PUBLIC_RESEARCH':'政府、軍方公開研究與多國組織','ENGINEERING':'工程、仿真與兵棋','INFRASTRUCTURE':'基礎軟件、設備與數據服務'}
for domain,label in labels.items():
    report+=f'### {label}\n\n| ID | 機構／類型 | ISO候選 | 產品／項目線索 | 本輪公開描述與狀態 |\n|---|---|---|---|---|\n'
    for e,c in zip(entities,claims):
        if e['primary_domain']!=domain: continue
        source=next((s['url'] for s in sources if s['source_id']==e['source_id']), '')
        name=f"[{e['display_name']}]({source})" if source else e['display_name']
        report+=f"| {e['entity_id']} | {name}／{e['entity_type']} | {e['country_candidate_iso_alpha2'] or '未分配／跨國'} | {c['product_project_leads']} | **{c['evidence_state']}**：{c['claim']} |\n"
    report+='\n'
report+='''## ISO 3166-1母表與後續全國家擴展

本倉库已有[ISO國家／地區母表](tables/01_country_area/registry_country_area_iso3166_20261004_enhanced.csv)。本輪本地檢查為249行、249個不重複alpha-2；這是既有快照的結構核驗，並非重新取得ISO全量官方授權版本。ISO條目包含屬地及地緣區域，不等同249個主權國家。本輪不製造「249國×空表」或聲稱每國所有機構已完成。

後續使用關聯表`registry_org_country_presence`記錄entity_id、iso_alpha2、presence_role、valid_from/to、source_id、evidence_state。角色至少區分法定註冊、總部、研究站、製造、服務、公開合同與成員國。ESA／NATO用多對多成員關係，不造EU或NATO的ISO alpha-2；母集團、子公司、部門與研究所另用entity_relation，避免重複計數。

逐國覆蓋應以「ISO條目×領域×搜尋日期×來源×結果」記錄SEARCHED_WITH_RECORDS、SEARCHED_NO_PUBLIC_RECORD、NOT_YET_SEARCHED。未找到公開項目不能填能力零。國家能力彙總只可來自產品／項目層已有證據的claim，不能由公司所在地外推國家全部能力。

沿用同一原則，神經技術另建`registry_neurotechnology_global`，粒度為機構×項目／設備×版本×試驗，外鍵連至ISO母表與組織表。預留侵入性、EEG/ECoG/微電極/fNIRS/TMS、讀取／寫入／雙向、remote_mode及操作距離、帶寬及計量方法、受試人數／試驗註冊ID、臨床階段、論文DOI、專利公開號、監管機構／適應症／決定日與claim證據。無線數據傳輸、遠程操作和遠距腦訊號感測不得混為一類；放大器採樣率不等於解碼資訊帶寬。

N0～N7須先有版本化操作定義、輸入输出、測試條件與可重現門檻，才可給項目分級；國家層最多匯總已公開驗證的項目上限與覆蓋，不把未公開能力猜成某級。本輪只提供擴展合同，未生成神經技術普查或臨床主張。

## 數據交付與限制

CSV與資料字典見[本批資料目錄](tables/06_frontier_ecosystem_20261006/README.md)：組織、claim、來源分開；既有ISO及DGEF表保持原快照。本批只保存簡短審閱摘要與來源URL，未知許可不等於可抓取全文、用於訓練或再發布。

查證集中於機構身份線索與公開業務描述。每項产品的技术细节、全部国家所有机构、正式法人注册、专利论文穷举、实际部署与独立性能比较仍未完成，均明确标示边界。后续优先补产品级官方文档、任务／合同文件、研究论文和许可，再按国家系统推进。
'''
(ROOT/'Reference/Aerospace_Ecosystem_Report.qmd').write_text(report,encoding='utf-8')
readme=f'''# 世界前沿生態登記 — 2026-10-06

{len(entities)}個研究候選；{verified}條VERIFIED公開描述；{len(entities)-verified}條UNKNOWN。不聲稱全球全量或世界排名。

| 文件 | 粒度／主鍵 |
|---|---|
| registry_frontier_organizations.csv | 機構／項目候選；entity_id |
| registry_frontier_claims.csv | 一條本輪描述；claim_id，entity_id外鍵 |
| registry_frontier_sources.csv | 來源指針與支持範圍；source_id |

VERIFIED只驗證claim文字；product_project_leads未被claim明確覆蓋時為UNKNOWN。法人、性能、部署、監管與市場排名沒有連帶驗證。country_candidate_iso_alpha2是編輯定位，非官方法人註冊地；服務覆蓋另建多對多presence。空國家碼不填造假代碼。

來源P0/P1只是類別，不代表獨立測效；UNKNOWN來源URL可只是待查入口。checked_on僅對本輪讀取或嘗試訪問的來源填寫，published_on未知留空。未保存HTTP原文。License UNKNOWN不能當再分發／模型訓練許可。

ISO外鍵對既有249條母表做結構驗證；本輪不重新核准ISO快照，也不建249行空白能力表。擴展presence與神經技術合同見報告。表均UTF-8 BOM CSV，所有ID在本批穩定；重建資料時勿重排DATA，新增應在末尾，避免ID變動。

重建：以Python執行 reports/2026-10-06/frontier_ecosystem/build_registry.py。生成報告、CSV、參考檔校訂索引與本地驗收回執；不聯網、不更新歷史HTML。驗收回執只是本地結構結果，不是獨立事實審核。
'''
(OUT/'README.md').write_text(readme,encoding='utf-8')
audit.update(organizations=len(entities),verified_public_descriptions=verified,unknown=len(entities)-verified,
    domains=dict(groups),country_master_rows=249,checks={'unique_ids':True,'iso_candidate_fk':True,'verified_source_fk':True},
    reviewed_on=DATE,render_status='NOT_RUN')
audit['sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.csv')}
(Path(__file__).parent/'review_receipt.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:audit[k] for k in ('organizations','verified_public_descriptions','unknown','domains','country_master_rows')},ensure_ascii=False))
