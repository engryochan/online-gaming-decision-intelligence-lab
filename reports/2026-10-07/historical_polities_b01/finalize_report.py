from pathlib import Path
O=Path(__file__).parent;R=O.parents[2];p=O/'map_template.html';s=p.read_text(encoding='utf-8');a="document.getElementById('count').textContent=";b="if(!visible.some(r=>r[0]===selected)){selected='';info.textContent='點選圖形或名稱以查看來源時段。'}"+a
assert s.count(a)==1;s=s.replace(a,b);p.write_text(s,encoding='utf-8');(R/'Reference/Historical_Polities_Timeline_Map_B01_20261007.html').write_text(s.replace('__PAYLOAD__',(O/'map_payload.json').read_text(encoding='utf-8').replace('<','\\u003c')),encoding='utf-8');(O/'map_script_check.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0].replace('__PAYLOAD__','[]'),encoding='utf-8')
p=R/'Reference/Global_Historical_Polities_B01_20261007.qmd';s=p.read_text(encoding='utf-8');s+='''
## 並行變更保留回執

收尾工作區掃描另發現既有`Inteligent_egaming_platform_ref_v000.000.001.qmd`有一增一刪的變更，以及新增版本與對話存檔文件；它們不在本輪交付写入範圍，沒有恢復、合併或覆寫，未推定其作者。原基線沒有刷新。嚴格「整個工作區僅有預定改動」驗收未通過；本輪交付範圍核查則通過，兩者分別記錄。

- [交付範圍及並行變更完整回執](../reports/2026-10-07/historical_polities_b01/final_acceptance.json)
- [747項工作逐列保留、COW年度／時段對賬與原始來源指紋](../reports/2026-10-07/historical_polities_b01/additional_acceptance.json)

全部舊資料庫與原宇航報告均保持原指紋，三份索引原字節前綴保留；沒有刪除既有文件。新增文件現況掃描不是這些新文件內容已實質核實的證明。
''';p.write_text(s,encoding='utf-8');print('Selection state reset and concurrent-change disclosure recorded')
