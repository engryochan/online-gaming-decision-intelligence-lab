from pathlib import Path
import csv,json,re,sqlite3,collections
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/74_platform_details_b51_20261011'
out=T/'registry_esri_terms_review.csv';assert not out.exists(),'Do not overwrite review'
rows=list(csv.DictReader((T/'registry_esri_item_terms.csv').open(encoding='utf-8-sig')));review=[]
for r in rows:
    raw=json.loads(r['license_info_json']);text=re.sub('<[^>]+>',' ',raw or '');text=' '.join(text.split());low=text.lower()
    review.append(dict(item_id=r['item_id'],license_text_present=bool(text),master_license_mentioned='master license agreement' in low,
        subscription_mentioned='subscription' in low,developer_account_mentioned='developer account' in low,
        no_credits_phrase_observed='does not consume credits' in low,
        classification='TERMS_PRESENT_SCOPE_AND_LINKED_AGREEMENT_REVIEW_OPEN' if text else 'NO_INLINE_TERMS_NOT_ASSUMED_UNRESTRICTED',
        commercial_redistribution_approved=False,source_file=r['source_file'],source_sha256=r['source_sha256']))
with out.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(review[0]));w.writeheader();w.writerows(review)
rs=list(csv.DictReader(out.open(encoding='utf-8-sig')));ks=list(rs[0]);con=sqlite3.connect(T/'platform_details_b51.sqlite')
con.execute('CREATE TABLE "'+out.stem+'" ('+','.join('"'+k+'" TEXT' for k in ks)+')')
con.executemany('INSERT INTO "'+out.stem+'" VALUES ('+','.join('?' for k in ks)+')',[[r[k] for k in ks] for r in rs]);con.commit()
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and con.execute('SELECT COUNT(*) FROM '+out.stem).fetchone()[0]==68;con.close()
stats=json.loads((O/'validation_receipt.json').read_text());stats['sqlite_counts'][out.stem]=68
stats['inline_terms_present']=sum(r['license_text_present'] for r in review)
stats['subscription_text_mentions']=sum(r['subscription_mentioned'] for r in review)
stats['no_credits_phrase_mentions']=sum(r['no_credits_phrase_observed'] for r in review)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
report=R/'Reference/Platform_Details_B51_20261011.qmd'
with report.open('a',encoding='utf-8') as f:
    f.write('\n## 條款與存取實測補核\n\n68項詳細元資料均為public可見，其中66項有內嵌條款；另2項沒有內嵌文字，不能視作自由授權。逐item文本標記見[條款複核表](tables/74_platform_details_b51_20261011/registry_esri_terms_review.csv)。部分條款提及Master License Agreement、組織訂閱／developer帳戶及不消耗credits；不消耗credits不等於免費帳戶、無限制商用或可重分發。服務實測20項均為HTTP 200內含499 Token Required，故可取得服務schema為0；保留API錯誤原文，未登入或繞過。星盾替代官網入口本地HTTP 522，保留官方搜尋索引產品主張及直接取用缺口，未宣稱完成頁面全文核驗。\n\n更新統計：'+json.dumps(stats,ensure_ascii=False)+'。\n')
print(json.dumps({k:stats[k] for k in ['inline_terms_present','subscription_text_mentions','no_credits_phrase_mentions']}))
