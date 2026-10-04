from pathlib import Path
import hashlib,json,zipfile
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[1]
term='本'+'土'
replacements=[
('九门之中唯一'+term+'可及、且方法论可整套照搬者 ── 见第十节','提供执行与转型咨询；采购、授权与方法适配须核实 ── 见第十节'),
('九门之中唯一'+term+'可及、方法论可整套照搬者','提供执行与转型咨询；采购、授权与方法适配须核实'),
('九门唯一'+term+'可及可整套照搬者','其服务可供进一步评估，采购与方法适配须核实'),
('九门中唯一'+term+'可洽者','采购与合作条件须向供应商核实'),
('唯 PEMANDU 为'+term+'，两附件虽列其名，却未点明「此乃唯一可亲身求教者」','PEMANDU 是候选供应商之一；所在地不证明只有它可以面谈或合作'),
(term+'、可面谈、方法公开者','可联系询问；会面、方法授权与适配条件须核实'),
(term+'、可面谈、方法公开','可联系询问；会面、方法授权与适配条件须核实'),
(term+'可及、方法可整套照搬','可联系评估；采购与方法适配须核实'),
('四家里只有 TM 是'+term,'四家供应商的公司所在地与服务覆盖须分别记录；TM 为马来西亚公司'),
('仅 TM '+term,'TM 为马来西亚公司；各供应商服务覆盖须分别核实'),
('是·'+term+'可及','采购与合作条件待核'),
(term+'可洽','可联系询问，合作条件待核'),
(term+'可及','服务可及性待核'),
(term+'可行之 PEMANDU','须核实可行性与适配条件的 PEMANDU'),
('美国'+term,'美国境内'),('英国'+term,'英国境内'),('印度'+term+'语言','印度地区语言'),
('中国'+term,'中国市场'),(term+'国防企业','所在国家的国防企业'),
(term+'化','地区适配'),(term+'性缺席','地区服务覆盖待核'),(term+'盲','地区覆盖盲区'),
(term+'三角','互补服务组合'),(term+'产业','地区产业'),(term+'语言','地区语言'),
(term,'地区覆盖'),
]
targets=[p for p in ROOT.rglob('*') if p.suffix.lower() in ('.md','.qmd','.txt','.html') and not any(x in p.relative_to(ROOT).parts for x in ('.git','.Rproj.user','reports'))]
targets += [OUT/'build_catalogue.py',OUT/'续核与建议修订稿.md',OUT/'catalogue_seed.tsv']
changes=[]
backup=OUT/'terminology_before_correction_all_text.zip'
with zipfile.ZipFile(backup,'x',compression=zipfile.ZIP_DEFLATED) as z:
 for p in targets:
  b=p.read_bytes()
  try:t=b.decode('utf-8')
  except UnicodeDecodeError:continue
  if term not in t:continue
  new=t
  for a,c in replacements:new=new.replace(a,c)
  # Withdraw the copyability inference even where it was not joined to the geographic label.
  new=new.replace('方法论可整套照搬','方法授权与适配须核实')
  rel=p.relative_to(ROOT).as_posix();z.writestr(rel,b)
  nb=new.encode('utf-8');p.write_bytes(nb)
  changes.append(dict(path=rel,replaced_occurrences=t.count(term),before_sha256=hashlib.sha256(b).hexdigest(),after_sha256=hashlib.sha256(nb).hexdigest(),lines_preserved=t.count('\n')==new.count('\n')))
(OUT/'terminology_correction_all_text_audit.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
assert all(r['lines_preserved'] for r in changes)
print(json.dumps(dict(files=len(changes),occurrences=sum(r['replaced_occurrences'] for r in changes)),ensure_ascii=False))
