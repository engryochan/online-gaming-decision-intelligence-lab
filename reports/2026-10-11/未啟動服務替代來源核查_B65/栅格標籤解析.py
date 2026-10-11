import struct
類型={1:('B',1),2:('s',1),3:('H',2),4:('I',4),5:('',8),6:('b',1),7:('B',1),8:('h',2),9:('i',4),10:('',8),11:('f',4),12:('d',8),13:('I',4),16:('Q',8),17:('q',8),18:('Q',8)}
目標={256:'像元列數',257:'像元行數',258:'每樣本位數',259:'壓縮代碼',277:'每像元樣本數',322:'塊列數',323:'塊行數',339:'樣本型態代碼',33550:'像元比例原值',33922:'模型連結點原值',34264:'模型轉換矩陣原值',34735:'地理鍵目錄原值',34736:'地理雙精度參數原值',34737:'地理文字參數原值',42113:'無資料值原文'}
def 解析(讀):
    頭=讀(0,16);assert 頭[:2] in [b'II',b'MM'],'不是標籤影像格式位元序'
    e='<' if 頭[:2]==b'II' else '>';magic=struct.unpack(e+'H',頭[2:4])[0];assert magic in [42,43],'不是標準或大檔標籤影像格式'
    big=magic==43
    if big:assert struct.unpack(e+'HH',頭[4:8])==(8,0)
    offset=struct.unpack(e+('Q' if big else 'I'),頭[8:16] if big else 頭[4:8])[0];assert offset>0
    countsize=8 if big else 2;entrysize=20 if big else 12;inline=8 if big else 4
    n=struct.unpack(e+('Q' if big else 'H'),讀(offset,countsize))[0];assert 0<n<=1024,'標籤數超出核查上限'
    data=讀(offset+countsize,n*entrysize);out={'格式中譯':'大檔標籤影像格式' if big else '標準標籤影像格式','原格式識別碼':magic,'位元序中譯':'小端序' if e=='<' else '大端序','第一影像目錄位移':offset,'第一影像目錄標籤數':n}
    for i in range(n):
        r=data[i*entrysize:(i+1)*entrysize];tag,t=struct.unpack(e+'HH',r[:4]);c=struct.unpack(e+('Q' if big else 'I'),r[4:12] if big else r[4:8])[0]
        if tag not in 目標:continue
        assert t in 類型;fmt,size=類型[t];length=size*c;assert 0<length<=65536,'元資料標籤長度超過上限'
        v=r[12:20] if big else r[8:12]
        b=v[:length] if length<=inline else 讀(struct.unpack(e+('Q' if big else 'I'),v)[0],length)
        if t==2:value=b.rstrip(b'\0').decode('utf-8','replace')
        elif fmt:value=list(struct.unpack(e+fmt*c,b));value=value[0] if c==1 else value
        else:value={'未解析原有理數':b.hex()}
        out[目標[tag]]=value
    assert out.get('像元列數',0)>0 and out.get('像元行數',0)>0
    return out
