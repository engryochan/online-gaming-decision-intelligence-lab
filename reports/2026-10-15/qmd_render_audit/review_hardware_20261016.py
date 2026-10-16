"""Bounded continuation from individually read official sources on 2026-10-16."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
items=[
 ('GTT0024','Gazebo Sim','官方文件描述其為機械人模擬器，提供物理、渲染及感測器模型。','https://gazebosim.org/libs/sim/','Readme / Gazebo Sim: A Robotic Simulator'),
 ('GTT0025','BCI2000 授權','官方授權頁列明可依 GPL 使用，並另述商業使用與衍生軟件源碼提供條件。','https://www.bci2000.org/mediawiki/index.php/BCI2000_Licensing','GNU General Public License; Commercial Use'),
 ('GTT0027','Stentrode','Synchron 描述其 Stentrode 透過頸靜脈植入。','https://synchron.com/','Introduction before Explore the technology'),
 ('GTT0028','Connexus','Paradromics 描述 Connexus 為可植入、將神經意圖轉為溝通的腦機介面。','https://paradromics.com/','Connexus BCI'),
 ('GTT0029','g.Nautilus Research','g.tec 描述 g.Nautilus Research 為無線 EEG 記錄系統。','https://www.gtec.at/product/gnautilus-research-wireless-eeg-system/','Product introduction; research platform'),
 ('GTT0030','Enobio','Neuroelectrics 將 Enobio 描述為 EEG 記錄系統。','https://www.neuroelectrics.com/products/research/enobio','Enobio EEG systems'),
 ('GTT0031','Starstim','Neuroelectrics 描述 Starstim 研究平台具 tES 刺激與 EEG 監測功能。','https://www.neuroelectrics.com/products/research/starstim','Starstim tES-EEG systems'),
 ('GTT0032','Deep TMS','BrainsWay 將 Deep TMS 描述為非侵入式治療產品。','https://www.brainsway.com/','Who is BrainsWay; Our Treatments'),
 ('GTT0033','Spot','Boston Dynamics 將 Spot 描述為用於感測與檢查的移動機械人。','https://bostondynamics.com/products/spot/','Spot - The Agile Mobile Robot'),
 ('GTT0034','Atlas','Boston Dynamics 將 Atlas 描述為人形機械人。','https://bostondynamics.com/products/atlas/','Atlas; Meet the new industrial revolution'),
 ('GTT0035','Stretch','Boston Dynamics 將 Stretch 描述為倉庫箱件搬運機械人。','https://bostondynamics.com/products/stretch/','Automate your warehouse with Stretch; Elevate case handling'),
 ('GTT0036','Orbit','Boston Dynamics 將 Orbit 描述為機械人機隊管理軟件。','https://bostondynamics.com/products/','The Portal to Your Fleet & Facilities'),
 ('GTT0037','da Vinci','Intuitive 將 da Vinci 描述為機械人手術系統。','https://www.intuitive.com/en-us/products-and-services/da-vinci','Intuitive da Vinci'),
 ('GTT0038','Ion','Intuitive 將 Ion 描述為供周邊肺部活檢的機械人支氣管鏡平台。','https://www.intuitive.com/en-us/products-and-services/ion','Ion Robotic Bronchoscopy'),
 ('GTT0043','3DFabric','TSMC 描述 3DFabric 為3D矽堆疊及先進封裝解決方案系列。','https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/3DFabric.htm','TSMC 3DFabric introduction'),
 ('GTT0044','Open Innovation Platform','TSMC 描述 OIP 透過生態合作支援半導體設計。','https://www.tsmc.com/english/dedicatedFoundry/oip','OIP ecosystem collaboration'),
]
ledger_path=OUT/'verified_facts.json';ledger=json.loads(ledger_path.read_text(encoding='utf-8'))
for n,(rid,name,claim,url,loc) in enumerate(items,71):
    ident=f'F{n:03}'
    if any(f['id']==ident for f in ledger['facts']):continue
    ledger['facts'].append(dict(id=ident,claim=claim,status='SUPPORTED',source=url,locator=loc,
        document='Reference/Global_Technology_ISO249_Registry.qmd',registry_id=rid,checked_on='2026-10-16',
        boundary='限官方公開類型／用途或授權頁文字；未獨立核實效能、比較排名、臨床招募現況、醫療許可、法律適用性或本項目已部署。'))
ledger['last_updated']='2026-10-16'
ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
p=ROOT/'Reference/Global_Technology_ISO249_Registry.qmd';raw=p.read_bytes();marker='<!-- HARDWARE_FACT_REVIEW_20261016 -->'
if marker.encode() not in raw:
    before=hashlib.sha256(raw).hexdigest();(OUT/'original_bytes'/f'{before}.bin').write_bytes(raw)
    text='\n\n'+marker+'\n\n## 2026-10-16 具名產品與授權文字續核\n\n'
    text+='以下16項只核對官方描述或授權頁文字。人體研究、療效、FDA／CE許可、產品性能排名及法律適用性均不因產品頁存在而一併通過。原歷史 CSV 與上方歷史狀態保留。\n\n'
    text+='| 登記 ID | 項目 | 本次支持的窄義主張 | 一手來源 |\n| --- | --- | --- | --- |\n'
    text+=''.join(f'| {rid} | {name} | {claim} | [來源]({url}) |\n' for rid,name,claim,url,loc in items)
    text+='\nGazebo（GTT0024）本次從官方子文件取得正文，更新的是本次基本用途判讀，並不否認前輪首頁沒有可讀正文。Orekit 官方主站與治理文件仍回傳存取挑戰；搜尋索引的歷史摘錄僅作線索，沒有當作完整讀取或當前版本核實。BCI2000 的商業使用仍須遵守適用授權條款；本節不以免費下載推導無條件商用。\n'
    with p.open('ab') as f:f.write(text.replace('\n','\r\n').encode())
    after=hashlib.sha256(p.read_bytes()).hexdigest()
    receipt=dict(checked_on='2026-10-16',before_sha256=before,after_sha256=after,
        original_bytes_preserved=p.read_bytes().startswith(raw),supported_claim_ids=[f'F{n:03}' for n in range(71,87)],
        pending=[dict(registry_id='GTT0023',source='https://www.orekit.org/doc/orekit_governance_v4.pdf',result='Access Denied challenge; indexed excerpt retained only as lead')],
        external_fact_review_complete=False)
    (OUT/'hardware_review_20261016_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
    changes=json.loads((OUT/'source_changes.json').read_text(encoding='utf-8'))
    entry=next(x for x in changes if x['path']==p.relative_to(ROOT).as_posix());entry['after_sha256']=after
    entry['change']='bounded quantum, software and product-description reviews; all pre-existing bytes preserved'
    (OUT/'source_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
print('ledger facts',len(ledger['facts']))
