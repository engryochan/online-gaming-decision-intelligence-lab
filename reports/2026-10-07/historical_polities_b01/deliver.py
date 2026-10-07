from pathlib import Path
import json,csv,hashlib,sqlite3
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;T=R/'Reference/tables/26_historical_polities_b01_20261007';s=json.loads((O/'validation.json').read_text());sha=(O/'pinned_commit.txt').read_text().strip()
payload=(O/'map_payload.json').read_text(encoding='utf-8');template=(O/'map_template.html').read_text(encoding='utf-8');target=R/'Reference/Historical_Polities_Timeline_Map_B01_20261007.html';assert not target.exists();target.write_text(template.replace('__PAYLOAD__',payload.replace('<','\\u003c')),encoding='utf-8')
script=template.split('<script>',1)[1].split('</script>',1)[0].replace('__PAYLOAD__','[]');(O/'map_script_check.js').write_text(script,encoding='utf-8')
body=f'''---
title: "全球歷史政治實體登記 B01：實測年代、疆域與現行金融範圍"
date: 2026-10-07
format:
  html:
    toc: true
---

## 實際接收與範圍

本輪將研究範圍擴展至歷史政治實體，不以現行249條目作總量上限。完整接收Cliopatria固定提交`{sha}`的{ s['features']:,}個年代／疆域記錄，涉及{s['source_named_entities']:,}個來源名稱；其中POLITY {s['source_types']['POLITY']:,}條、RELATION {s['source_types']['RELATION']:,}條。來源名稱與類型分組不等於唯一國家身份，時段記錄也不等於國家數。

[維護者說明](https://github.com/Seshat-Global-History-Databank/cliopatria)的資料涵蓋公元前3400年至2024年，疆域採來源歷史重建，名稱、年代及邊界可能有不同學術見解。來源所有屬性、Components／MemberOf關係、Wikidata／Seshat識別資訊及完整未簡化幾何均保留；尚未逐項獨立核實，不升級為VERIFIED。原始ZIP、固定提交、授權與SHA256均封存。

## 年代與疆域圖

[開啟可篩選年份及名稱的完整年代圖](Historical_Polities_Timeline_Map_B01_20261007.html)。圖形可點選，RELATION關係層另行勾選；並未用疆域面積或色彩推算軍力、經濟、外交影響力。這些勢力指標需另有逐時段證據。

<iframe src="Historical_Polities_Timeline_Map_B01_20261007.html" title="歷史政治實體年代圖" style="width:100%;height:900px;border:1px solid #ccd;"></iframe>

地圖顯示為等經緯度投影，0.15度容差簡化並取四位小數；它只是顯示衍生物，原始多邊形沒有簡化或覆寫。跨日界線與極區顯示須審閱，不適用精確邊界或面積量測。空白區域表示來源未覆蓋，不能當作當年不存在政治組織。

來源FromYear／ToYear為包含端點的時段，負數BCE、正數CE；保留来源整数年，不自行解讀年0。每個名稱的最早／最晚來源年僅表示資料跨度，不代表中間連續存在、建國／滅亡日期。名稱相同亦未自動合併跨来源身份，未將帝國、王朝、城邦、聯盟、殖民地、考古文化視作同一種國家。

## COW獨立定義與大國年代

完整接收[COW v2024](https://correlatesofwar.org/data-sets/state-system-membership/)：{s['cow_rows']['statelist2024']}條國家體系參與時段、{s['cow_state_codes']}個來源國家代碼、{s['cow_rows']['system2024']:,}條國家年，以及{s['cow_rows']['majors2024']}條大國資格時段。COW按人口與外交／組織參與等操作定義選取成員；體系加入／退出日期不是所有國家的建國／滅亡日期，大國資格亦不是國力排名。來源截至2024年末的端點不能當成那些國家當天滅亡。

所有欄位、日期及版本保留，年度與大國代碼均能連回來源國家代碼；COW與Cliopatria保持來源分層，不以英文名稱或近似ISO代碼自動混合。

## 現行名錄實測與金融工作延續

本日實際接收[聯合國M49英文下載表](https://unstats.un.org/unsd/methodology/m49/overview/)，量得{s['live_UN_M49_rows']}個國家／地區列；項目既有母表量得{s['project_mother_rows']}列。兩者代碼聯集{s['union_codes']}，項目獨有TW，聯合國來源獨有0。這是兩份來源範圍差異，不是刪除台灣的依據，也不是已實測ISO官方現行全集的證明。既有母表全部保留，原文名稱、區域層級及標誌均存入比對表；名稱／法律地位仍待核實。

保留[金融B07](Global_Financial_Universe_B07_20261007.qmd)的全部747項逐國工作列，接入歷史查詢庫；來源金融庫指紋記錄不變。現有金融資料仍為43,410條上市工具／公司目錄來源、7,162條ESMA公司／分支、449條現行與歷史貨幣來源，不能當作世界所有公司、證券行與貨幣已收齊。歷史政體增加不能關閉現行金融缺口，也不能把沒有近代證券制度證據的古代政體直接標為零。

## 尚未完成的年代與證據

幾萬年以前至公元前3400年，需按區域考古、聚落、治理與年代測定證據繼續登記；本輪尚無可支持完整國家清單及疆界的來源。公元前3400年至2024年亦可能有未列入實體、不同重建或有爭議年代；2025年至今的變動另待增量核實。所有存在過的國家沒有由這批資料得到可證實的全球總數，不能宣稱窮盡。

登記規則要求分別記錄國家／政治組織類型、來源時段、日期不確定範圍、前後繼、隸属與聯盟、實際控制／主張疆界／影響力、逐主張來源及核實狀態。此次保留來源已有內容，未知欄位維持UNKNOWN；不憑空添加勢力多邊形或建國日期。

## 完整資料及驗收

'''
for p in sorted(T.glob('*.csv')):body+=f'- [{p.name}](tables/{T.name}/{p.name})\n'
body+='\n- [SQLite時序查詢庫](../reports/2026-10-07/historical_polities_b01/historical_polities_v1.sqlite)\n- [來源指紋](../reports/2026-10-07/historical_polities_b01/source_manifest.json)及[驗收](../reports/2026-10-07/historical_polities_b01/validation.json)\n\n完整13,797筆原始feature已逐項解壓往返對照，所有屬性與幾何一致；SQLite完整性通過。這是接收完整性驗收，不是每個歷史主張皆已實質核實。Cliopatria資料及本圖衍生幾何遵循CC BY 4.0，注明來源與顯示簡化改動。\n'
p=R/'Reference/Global_Historical_Polities_B01_20261007.qmd';assert not p.exists();p.write_text(body,encoding='utf-8')
queries={'entities_at_1800':"SELECT name,source_type,from_year,to_year FROM historical_features WHERE from_year<=1800 AND to_year>=1800 ORDER BY name",'source_type_counts':'SELECT source_type,COUNT(*) FROM historical_features GROUP BY source_type','financial_tasks':'SELECT stream,COUNT(*) FROM financial_workstreams GROUP BY stream','source_cow_counts':'SELECT source,COUNT(*) FROM source_records GROUP BY source','live_country_union':'SELECT COUNT(*) FROM current_country_checks'}
c=sqlite3.connect(O/'historical_polities_v1.sqlite');a={k:c.execute(q).fetchall() for k,q in queries.items()};c.close();assert a['live_country_union']==[(249,)] and all(r[1]==249 for r in a['financial_tasks'])
(O/'query_acceptance.json').write_text(json.dumps(a,indent=2)+'\n',encoding='utf-8');(O/'queries.sql').write_text('\n'.join('-- '+k+'\n'+q+';' for k,q in queries.items())+'\n',encoding='utf-8')
old=R/'reports/2026-10-07/financial_universe_b07';x=(old/'append_index.py').read_text(encoding='utf-8');a=x.index('addition=');b=x.index('\nsaved=',a);addition='\n\n<!-- HISTORICAL_POLITIES_B01_20261007 -->\n\n## 全球歷史政治實體與年代圖增補\n\n[歷史政治實體B01](Global_Historical_Polities_B01_20261007.qmd)接收13,797條來源年代／疆域記錄及COW全量國家、大國時段與年度表，提供年份篩選圖；現行名錄實測、747項金融工作與史前／當代缺口分層保留，未宣稱全球所有歷史國家皆已核實。\n';x=x[:a]+'addition='+repr(addition)+x[b:];x=x.replace("marker='FINANCIAL_UNIVERSE_B07_20261007'","marker='HISTORICAL_POLITIES_B01_20261007'");(O/'append_index.py').write_text(x,encoding='utf-8')
manifest=[]
for p in T.glob('*.csv'):manifest.append(dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
with (T/'integration_input_manifest.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=['path','sha256']);w.writeheader();w.writerows(manifest)
x=(old/'validate_preservation.py').read_text(encoding='utf-8').replace('iso249_b07_start','historical_polities_b01_start').replace('iso249_b07_finish','historical_polities_b01_finish').replace('25_iso249_financial_universe_b07_20261007','26_historical_polities_b01_20261007').replace('financial_universe_v4.sqlite','historical_polities_v1.sqlite').replace('Global_Financial_Universe_B07','Global_Historical_Polities_B01');(O/'validate_preservation.py').write_text(x,encoding='utf-8')
print('Historical report, complete interactive map, queries and preservation helpers created')
